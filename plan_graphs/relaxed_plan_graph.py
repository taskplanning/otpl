import numpy as np
from pddl.domain import Domain
from pddl.grounding import Grounding
from pddl.problem import Problem
from pddl.state import State

class RelaxedPlanGraph:

    def __init__(self, domain : Domain, problem : Problem) -> None:

        self.domain    : Domain = domain
        self.problem   : Problem = problem
        self.grounding : Grounding = problem.grounding
        
        self.grounding.ground_problem(domain, problem)

        # plan graph details
        self.last_layer = 0
        self.all_actions   : np.ndarray[bool] = None
        self.fact_membership = np.zeros(self.grounding.proposition_count, dtype=int)
        self.action_membership = np.zeros(self.grounding.proposition_count, dtype=int)
        self.action_layers : dict[int,set[int]] = {}
        self.action_counters = np.zeros(self.grounding.proposition_count, dtype=int)
                
        self.helpful_actions = None
        self.fix_point_reached = False
        self.goal_reached = False

        self.goal_cached = False
        self.problem_goal_spike = np.zeros(self.grounding.proposition_count, dtype=bool)

        # cached spike representations of action effects and conditions
        self.actions_cached = False
        self.action_add_effect_spikes = {}
        self.action_positive_condition_spikes = {}
        self.proposition_condition_map : dict[int, list[int]] = {}
        self.action_precondition_counts = {}

        # actions to be excluded (i.e. that can never be reached)
        self.excluded_actions = np.zeros(self.grounding.action_count, dtype=bool)
    
    def _cache_actions(self) -> None:
        """
        Caches the spike representations of action effects and conditions.
        This prevents excessive calls to the grounding.
        """
        self.actions_cached = True
        for action_id in range(self.grounding.action_count):
            pos, _ = self.grounding.get_simple_action_condition_from_id(action_id)
            adds, _ = self.grounding.get_simple_action_effect_from_id(action_id)
            self.action_add_effect_spikes[action_id] = adds
            self.action_positive_condition_spikes[action_id] = pos
            self.action_precondition_counts[action_id] = np.count_nonzero(pos)

            # cache precondition mapping
            for prop in np.nonzero(pos)[0]:
                if prop not in self.proposition_condition_map:
                    self.proposition_condition_map[prop] = []
                self.proposition_condition_map[prop].append(action_id)

    def build_graph(self, state : State = None, stop_at_goal = True) -> int:
        """
        Builds the relaxed plan graph from a given state, or the problem's
        initial state if state is None.
        """
        if not self.actions_cached:
            self._cache_actions()

        # initialise action membership
        self.action_layers = {}
        self.action_membership = np.zeros(self.grounding.action_count, dtype=int)
        self.action_counters = np.zeros(self.grounding.action_count, dtype=int)
        current_actions = []

        # initialise fact layer
        self.last_layer = 0
        self.action_layers[self.last_layer+1] = set()
        start_state = self.problem.get_initial_state().logical if state is None else state.logical
        self.fact_membership = np.ones(self.grounding.proposition_count, dtype=int) * -1
        for prop_id in np.nonzero(start_state)[0]:
            self.fact_membership[prop_id] = self.last_layer
            for action_id in self.proposition_condition_map[prop_id]:
                self.action_counters[action_id] += 1
                if self.action_counters[action_id] == self.action_precondition_counts[action_id]:
                    self.action_membership[action_id] = self.last_layer+1
                    self.action_layers[self.last_layer+1].add(action_id)
                    current_actions.append(action_id)
        self.helpful_actions = current_actions

        # initialise action memory
        self.all_actions = np.zeros(self.grounding.action_count, dtype=bool)
        self.remaining_actions = np.logical_not(self.excluded_actions)

        self.goal_reached = self.check_goal()
        self.fix_point_reached = False
        while not (self.goal_reached and stop_at_goal) and not self.fix_point_reached:

            # increment layer
            self.last_layer += 1

            # compute effects of actions in current layer
            next_actions = []
            self.fix_point_reached = True
            self.action_layers[self.last_layer+1] = set()
            for action_id in current_actions:

                # add action to action memory
                self.all_actions[action_id] = True
                self.remaining_actions[action_id] = False

                # add action effects to fact layer
                for prop_id in self.action_add_effect_spikes[action_id].nonzero()[0]:

                    # already achieved
                    if self.fact_membership[prop_id] >= 0:
                        continue
                    
                    # new in this layer
                    self.fact_membership[prop_id] = self.last_layer
                    self.fix_point_reached = False

                    # increment counters on action conditions
                    for a in self.proposition_condition_map[prop_id]:
                        self.action_counters[a] += 1
                        if self.action_counters[a] == self.action_precondition_counts[a] and self.action_membership[a] == 0:
                            # new action achievable
                            self.action_membership[a] = self.last_layer + 1
                            self.action_layers[self.last_layer+1].add(a)
                            next_actions.append(a)

            current_actions = next_actions

            # check goal
            self.goal_reached = self.check_goal()

        return self.last_layer

    def check_goal(self) -> bool:
        """
        Checks if the goal has been reached.
        :return: True if the goal has been reached in the latest layer, False otherwise.
        """
        if not self.goal_cached:
            negative_conditions = np.zeros(self.grounding.proposition_count, dtype=bool)
            self.grounding.get_simple_conditions(self.problem.goal, self.problem_goal_spike, negative_conditions)
            self.goal_cached = True
        for prop in self.problem_goal_spike.nonzero()[0]:
            if self.fact_membership[prop] < 0:
                return False
        return True

    def print_graph(self) -> None:
        """
        Prints the relaxed plan graph as a list of layers.
        Propositions and actions are printed one per line as PDDL formula.
        """
        for layer in range(self.last_layer):
            print("Layer {}".format(layer))
            props = list(filter(lambda x: self.fact_membership[x] == layer, range(len(self.fact_membership))))
            for prop in props:
                print ("\t{}".format(self.grounding.get_proposition_from_id(prop)))
            acts = list(filter(lambda x: self.action_membership[x] == layer+1, range(len(self.action_membership))))
            for act in acts:
                print ("\t{}".format(self.grounding.get_action_from_id(act).print_pddl()))

    def get_relaxed_plan(self) -> tuple[dict[list[int]],int]:
        """
        If the goal has been reached returns a tuple containing the relaxed plan and the number of actions in the plan.
        """
        if not self.goal_reached:
            return None

        goal_set : dict[set[int]] = {}
        marked_goals : dict[set[int]] = {}
        relaxed_plan : dict[list[int]] = {}
        for i in range(self.last_layer+1):
            goal_set[i] = { prop for prop in self.problem_goal_spike.nonzero()[0] if self.fact_membership[prop] == i }
            marked_goals[i] = set()
            relaxed_plan[i] = []

        action_count = 0
        for i in range(self.last_layer,0,-1):            
            for goal in goal_set[i]:
                if goal in marked_goals[i]:
                    continue
                for action in self.action_layers[i]:
                    if self.action_add_effect_spikes[action][goal]:
                        for prop in self.action_positive_condition_spikes[action].nonzero()[0]:
                            if self.fact_membership[prop] == 0:
                                continue
                            if prop in marked_goals[i-1]:
                                continue
                            goal_set[self.fact_membership[prop]].add(prop)
                        
                        for add in self.action_add_effect_spikes[action].nonzero()[0]:
                            marked_goals[i-1].add(add)
                            marked_goals[i].add(add)

                        relaxed_plan[i-1].append(action)
                        action_count += 1
                        break
        return relaxed_plan, action_count

    def print_relaxed_plan(self) -> None:
        """
        Prints the relaxed plan as a list of "layer: action".
        """
        plan, _ = self.get_relaxed_plan()
        for layer, actions in plan.items():
            for action_id in actions:
                print("%d: %s" % (layer, self.grounding.get_action_from_id(action_id).print_pddl()))