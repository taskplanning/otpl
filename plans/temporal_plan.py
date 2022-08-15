from enum import Enum
from logging import raiseExceptions
import numpy as np
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.domain import Domain
from pddl.problem import Problem
from pddl.grounding import Grounding
from pddl.time_spec import TimeSpec
from pddl.timed_initial_literal import TimedInitialLiteral
from pddl.state import State
from temporal_networks.temporal_network import TemporalNetwork, TimePoint, Constraint
import re


class HappeningType(Enum):
    PLAN_START   = "PLAN_START"
    ACTION_START = "ACTION_START"
    ACTION_END   = "ACTION_END"
    TIMED_INITIAL_LITERAL = "TIMED_INITIAL_LITERAL"
    
class Happening:
    def __init__(self, id : int, time : float, type : HappeningType, action_id : int = -1, til : TimedInitialLiteral = None):
        self.id = id
        self.time = time
        self.type = type
        self.action_id = action_id
        self.til = til
    
    def __repr__(self):
        if self.type == HappeningType.PLAN_START:
            return "Happening(time={}, type={})".format(self.time, self.type)
        elif self.type == HappeningType.TIMED_INITIAL_LITERAL:
            return "Happening(time={}, type={}, til_id={})".format(self.time, self.type, self.til)
        else:
            return "Happening(time={}, type={}, action_id={})".format(self.time, self.type, self.action_id)

class PlanTemporalNetwork:
    """
    Represents the plan as a temporal network.
    """

    def __init__(self, domain : Domain, problem : Problem):
        self.domain : Domain = domain
        self.problem : Problem = problem
        self.grounding : Grounding = problem.grounding

        self.epsilon = 0.01
        self.infinity = 1000000000
        
        # map temporal network nodes to happenings
        self.temporal_network : TemporalNetwork = None
        self.happenings : list[Happening] = []
        self.time_sorted_happenings : list[Happening] = []

    def read_from_file(self, plan_file):
        """
        Parses a plan from file and constructs a temporal network.
        Nodes in the network correspond to action start and ends, the plan start, and TILs.
        Edges in the network correspond to action durations and ordering constraints.
        Expects the file to be in correct format, one action per line:
        time: (action) [duration]
        """
        if self.domain is None or self.problem is None:
            raise Exception("Domain and problem must be set before reading plan from file.")

        if not self.grounding.grounded:
            self.grounding.ground_problem(self.domain, self.problem)
        
        self.temporal_network = TemporalNetwork()

        # add plan start happening to network
        self.temporal_network.add_time_point(TimePoint(0, "PLAN_START"))
        self.happenings = [Happening(0, 0, HappeningType.PLAN_START)]

        # add action and TIL nodes to network
        self.parse_actions(plan_file)
        self.construct_til_nodes()

        # sort happenings by time
        self.time_sorted_happenings = [hap for hap in self.happenings]
        self.time_sorted_happenings.sort(key=lambda hap: hap.time)

        # add edges to network
        self.construct_ordering_constraints()

    def construct_til_nodes(self):
        # Gets the start node in the temporal network
        start_tp = self.temporal_network.get_timepoint_by_id(0)

        for til in self.problem.timed_initial_literals:

            # create node for TIL
            node_id = len(self.happenings)
            til_node = Happening(node_id, til.time, HappeningType.TIMED_INITIAL_LITERAL, til=til)
            end_tp = TimePoint(node_id, label="TIL: "+str(til.effect))
            self.temporal_network.add_time_point(end_tp)
            self.happenings.append(til_node)

            # create edge from TIL to plan start
            self.temporal_network.add_constraint(Constraint("TIL: "+str(til.effect), start_tp, end_tp, "stc", {"lb": til.time, "ub": til.time}))

    def parse_actions(self, plan_file):
        # read actions and create nodesx
        # Regular expression to match actions from planner output
        action_str = re.compile("\d+\.\d+:\s+\(.*\)\s+\[\d+\.\d+\]")
        # Stores the lines containing the plans
        plans = []
        # Used to keep track of whether a new plan has been found.
        new_plan = False
        with open(plan_file, 'r') as f:
            for line in f:
                match = action_str.findall(line)
                # If the new plan flag is set to False and we find a match then this means we have
                # found a new plan. We set it to True and initialise the new plan as an empty list
                if new_plan == False and match:
                    new_plan = True
                    plan = [match[0]]
                # Adds action to current plan
                elif match:
                    plan.append(match[0])
                # If the new plan flag is set to True and the current line is not a match then we have
                # got to the end of the plan. We reset the flag to False and add the plan to the list of
                # plans
                elif new_plan == True and not match:
                    new_plan = False
                    plans.append(plan)
        # If the new plan finishes on the last line, add the plan
        if new_plan == True:
            plans.append(plan)
        # Sets the plan to the best plan i.e. the last plan in the planner output
        plan = plans[-1]
        for line in plan:
            # parse line
            time = float(line.split(':')[0])
            action = line.split(":")[1].split("[")[0].strip()
            duration = float(line.split("[")[1].split("]")[0])

            # get the action name and parameters
            tokens = action.replace("(","").replace(")","").split()
            op = self.domain.operators[tokens[0]]
            if not op: raise Exception("Action " + action + " not found in domain.")

            objects = tokens[1:]
            if len(objects) != len(op.formula.typed_parameters):
                raise Exception("Action " + action + " has wrong number of parameters.")

            # get grounded action ID
            parameters = []
            for param, object in zip(op.formula.typed_parameters, objects):
                parameters.append(TypedParameter(param.type, param.label, object))
            formula = AtomicFormula(tokens[0], parameters)
            action_id = self.grounding.get_id_from_action_formula(formula)
                
            # action start happening
            node_id = len(self.happenings)
            action_start = Happening(node_id, time, HappeningType.ACTION_START, action_id)
            start_tp = TimePoint(node_id, label=formula.print_pddl() + "_start")
            self.temporal_network.add_time_point(start_tp)
            self.happenings.append(action_start)

            # action end happening
            node_id = len(self.happenings)
            action_end = Happening(node_id, time + duration, HappeningType.ACTION_END, action_id)
            end_tp = TimePoint(node_id, label=formula.print_pddl() + "_end")
            self.temporal_network.add_time_point(end_tp)
            self.happenings.append(action_end)

            # create edge for action duration
            action_edge = Constraint(formula.print_pddl(), start_tp, end_tp, "stc", {"lb": duration, "ub": duration})
            self.temporal_network.add_constraint(action_edge)


    def construct_ordering_constraints(self):
        """
        Constructs ordering constraints between happenings.
        """

        for index, happening in enumerate(self.time_sorted_happenings):

            # find time spec of happening
            if happening.type == HappeningType.ACTION_START:
                time_spec = TimeSpec.AT_START
            elif happening.type == HappeningType.ACTION_END:
                time_spec = TimeSpec.AT_END
            else: continue

            # get simple conditions of happening
            pos, neg = self.grounding.get_simple_action_condition_from_id(happening.action_id, time_spec)

            # if happening is an action start, add overall conditions
            if time_spec == TimeSpec.AT_START:
                p, n = self.grounding.get_simple_action_condition_from_id(happening.action_id, TimeSpec.OVER_ALL)
                np.logical_or(pos, p, out=pos)
                np.logical_or(neg, n, out=neg)

            # loop backwards through happenings to find latest achiever
            for prev_index in range(index - 1, -1, -1):

                prev = self.time_sorted_happenings[prev_index]
                time_spec = TimeSpec.AT_END if prev.type == HappeningType.ACTION_END else TimeSpec.AT_START
                
                # get simple effects of previous happening
                if prev.type == HappeningType.TIMED_INITIAL_LITERAL:
                    adds, dels = self.grounding.get_simple_til_effect(prev.til)              
                elif prev.type == HappeningType.PLAN_START:
                    adds = self.problem.get_initial_state().logical
                    dels = np.zeros(self.grounding.proposition_count, dtype=bool)
                else:
                    adds, dels = self.grounding.get_simple_action_effect_from_id(prev.action_id, time_spec)              

                # check if the effects support the conditions
                pos_support = np.logical_and(pos, adds)
                neg_support = np.logical_and(neg, dels)
                if np.any(pos_support) or np.any(neg_support):

                    # add new edge to the temporal network
                    start_tp = self.temporal_network.get_timepoint_by_id(happening.id)
                    end_tp = self.temporal_network.get_timepoint_by_id(prev.id)
                    self.temporal_network.add_constraint(Constraint("Ordering Constraint between {} and {}".format(start_tp.id, end_tp.id), start_tp, end_tp, "stc", {"lb": self.epsilon, "ub": self.infinity}))

                    # remove the now-supported conditions
                    np.logical_xor(pos, pos_support, out=pos)
                    np.logical_xor(neg, neg_support, out=neg)

                    # check interference with the supported conditions
                    if time_spec == TimeSpec.AT_START:
                        # supported overall conditions
                        p, n = self.grounding.get_simple_action_condition_from_id(happening.action_id, TimeSpec.OVER_ALL)
                        np.logical_and(pos_support, p, out=p)
                        np.logical_and(neg_support, n, out=n)
                        if np.any(p) or np.any(n):
                            self.add_interference_edges(index, prev_index, p, n, TimeSpec.OVER_ALL)
                        
                        # supported start conditions
                        np.logical_xor(pos_support, p, out=pos_support)
                        np.logical_xor(neg_support, n, out=neg_support)
                        if np.any(pos_support) or np.any(neg_support):
                            self.add_interference_edges(index, prev_index, pos_support, neg_support, TimeSpec.AT_START)
                    elif time_spec == TimeSpec.AT_END:
                        # supported end conditions
                        self.add_interference_edges(index, prev_index, pos_support, neg_support, TimeSpec.AT_END)
                
                # stop looking backwards when no unsupported conditions are remaining
                if not np.any(pos) and not np.any(neg):
                    break

            # add edge to plan start if any conditions remain
            if np.any(pos) or np.any(neg):
                print("WARNING: Unsupported conditions remain after planning.")
                # self.temporal_network.add_edge(happening.id, 0, 0.0)

    def add_interference_edges(self, happening_index, support_index, pos_support, neg_support, condition_time_spec):

        for inter_index in range(len(self.time_sorted_happenings)):
            
            if inter_index == happening_index or inter_index == support_index:
                continue

            # fetch effects of happening
            if self.time_sorted_happenings[inter_index].type == HappeningType.TIMED_INITIAL_LITERAL:
                adds, dels = self.grounding.get_simple_til_effect(self.time_sorted_happenings[inter_index].til)
            elif self.time_sorted_happenings[inter_index].type == HappeningType.ACTION_START:
                adds, dels = self.grounding.get_simple_action_effect_from_id(self.time_sorted_happenings[inter_index].action_id, TimeSpec.AT_START)
            elif self.time_sorted_happenings[inter_index].type == HappeningType.ACTION_END:
                adds, dels = self.grounding.get_simple_action_effect_from_id(self.time_sorted_happenings[inter_index].action_id, TimeSpec.AT_END)
            else: continue

            # check if the effects interfere with the support
            if np.any(np.logical_and(pos_support, dels)) or np.any(np.logical_and(neg_support, adds)):
                
                # choose ordering based on order in original plan
                source, sink = -1, -1
                if inter_index < support_index:
                    # interference action goes before support action
                    source = self.time_sorted_happenings[support_index].id
                    sink = self.time_sorted_happenings[inter_index].id
                    distance = -self.epsilon
                elif happening_index < inter_index and condition_time_spec != TimeSpec.OVER_ALL:
                    # interference action goes after support complete
                    source = self.time_sorted_happenings[inter_index].id
                    sink = self.time_sorted_happenings[happening_index].id
                    distance = -self.epsilon
                elif happening_index < inter_index and condition_time_spec == TimeSpec.OVER_ALL:
                    # interference action goes after overall constraint
                    source = self.time_sorted_happenings[inter_index].id
                    sink = self.time_sorted_happenings[happening_index+1].id
                    distance = 0.0
                    
                # add edge to temporal network
                if source != -1 and sink != -1:
                    start_tp = self.temporal_network.get_timepoint_by_id(source)
                    end_tp = self.temporal_network.get_timepoint_by_id(sink)
                    dist = self.temporal_network.find_shortest_path(start_tp, end_tp)
                    if -self.epsilon < dist:
                        self.temporal_network.add_constraint(Constraint("Interference Constraint between {} and {}".format(start_tp.id, end_tp.id), start_tp, end_tp, "stc", {"lb": self.epsilon, "ub": self.infinity}))

    # =================== #
    # simulated execution #
    # =================== #

    def simulate_execution(self, problem : Problem = None, until_time : float = None) -> tuple[State,list[TimedInitialLiteral]]:
        """
        Execute the plan on the given problem, returning the resultant state and remaining TILs.
        Actions still executing are converted into TILs and TIFs. Note that the returned TILs and TIFs will
        include some effects that are not normally allowed in PDDL as TIL/TIF, for example conditional effects
        and more complex numeric effects. These will not appear in a printed PDDL problem.
        param problem: The problem on which to execute the plan, if none then the problem used to parse the plan.
        param until_time: Float time to stop execution, if none then the whole plan is executed.
        """
        if problem is None: problem = self.problem
        current_state = problem.get_initial_state()
        current_happening_index = 0
        current_actions : set[int] = set()
        until_time = until_time if until_time is not None else self.time_sorted_happenings[-1].time

        while current_happening_index < len(self.time_sorted_happenings):

            # move time forwards
            happening = self.time_sorted_happenings[current_happening_index]
            if until_time < happening.time:
                current_state.time = until_time
                break
            current_state.time = happening.time

            # apply effects of the happening
            if happening.type == HappeningType.PLAN_START:
                pass
            elif happening.type == HappeningType.TIMED_INITIAL_LITERAL:
                problem.grounding.apply_simple_til_effects(happening.til, current_state)
            elif happening.type == HappeningType.ACTION_START:
                problem.grounding.apply_simple_action_effects(happening.action_id, current_state, time_spec=TimeSpec.AT_START)
                current_actions.add(happening.id)
            elif happening.type == HappeningType.ACTION_END:
                problem.grounding.apply_simple_action_effects(happening.action_id, current_state, time_spec=TimeSpec.AT_END)
                current_actions.remove(happening.id - 1)

            # move to next happening
            current_happening_index += 1

        # create new tils for currently executing actions
        tils = [ ]
        for happening_id in current_actions:
            time = self.happenings[happening_id+1].time
            action = problem.grounding.get_action_from_id(self.happenings[happening_id].action_id)
            effect = action.effect.filter_effects_to_time_spec(TimeSpec.AT_END)
            tils.append(TimedInitialLiteral(time, effect))

        return current_state, tils
