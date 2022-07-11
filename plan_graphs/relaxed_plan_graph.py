import numpy as np
from pddl.domain import Domain
from pddl.grounding import Grounding
from pddl.problem import Problem

class RelaxedPlanGraph:

    def __init__(self, domain : Domain, problem : Problem, grounding : Grounding) -> None:
        self.domain    : Domain = domain
        self.problem   : Problem = problem
        self.grounding : Grounding= grounding
        self.fact_layers = None
        self.action_layers = None
        self.fix_point_reached = False
        self.goal_reached = False

    def build_graph(self, stop_at_goal = True) -> None:
        """
        Builds the relaxed plan graph.
        """
        self.fact_layers = [ self.grounding.get_initial_state_spike() ]
        self.action_layers = [ np.zeros(self.grounding.action_count, dtype=np.bool) ]

        self.goal_reached = self.check_goal()
        self.fix_point_reached = False

        while not (self.goal_reached and stop_at_goal) and not self.fix_point_reached:

            # action layer
            self.action_layers.append(np.zeros(self.grounding.action_count, dtype=np.bool))
            np.logical_or(self.action_layers[-1], self.action_layers[-2], self.action_layers[-1])
            for id in np.asarray(self.action_layers[-1]==0).nonzero()[0]:            
                pos, _ = self.grounding.get_action_condition_spike_from_id(id)

                # check positive preconditions
                if np.any(np.logical_xor(pos, np.logical_and(self.fact_layers[-1], pos))):
                    continue

                # action is applicable 
                self.action_layers[-1][id] = True


            # fact layer
            self.fact_layers.append(np.zeros(self.grounding.proposition_count, dtype=bool))
            np.logical_or(self.fact_layers[-1], self.fact_layers[-2], self.fact_layers[-1])
            for id in np.nonzero(self.action_layers[-1])[0]:
                pos, _ = self.grounding.get_action_effect_spike_from_id(id)
                np.logical_or(self.fact_layers[-1], pos, self.fact_layers[-1])

            # check goal
            self.goal_reached = self.check_goal()
            
            # check if fix point has been reached
            if not np.any(np.logical_xor(self.fact_layers[-1], self.fact_layers[-2])):
                self.fix_point_reached = True

    def check_goal(self) -> bool:
        """
        Checks if the goal has been reached.
        :return: True if the goal has been reached in the latest layer, False otherwise.
        """
        positive_conditions = np.zeros(self.grounding.proposition_count, dtype=np.bool)
        negative_conditions = np.zeros(self.grounding.proposition_count, dtype=np.bool)
        self.grounding.get_simple_conditions(self.problem.goal, positive_conditions, negative_conditions)
        return not np.any(np.logical_xor(positive_conditions, np.logical_and(positive_conditions, self.fact_layers[-1])))

    def print_graph(self) -> None:
        """
        Prints the relaxed plan graph as a list of layers.
        Propositions and actions are printed one per line as PDDL formula.
        """
        layer = 0
        for fact, action in zip(self.fact_layers, self.action_layers):
            print ("Fact layer: {}".format(layer))
            for id in np.nonzero(fact)[0]:
                print ("\t{}".format(self.grounding.get_proposition_from_id(id)))
            print ("Action layer: {}".format(layer))
            for id in np.nonzero(action)[0]:
                print ("\t{}".format(self.grounding.get_action_from_id(id).print_pddl()))
            layer += 1

    def get_relaxed_plan(self) -> None:
        """
        If the goal has been reached returns the relaxed plan.
        Otherwise returns None.
        """
        if not self.goal_reached:
            return None

        return None

