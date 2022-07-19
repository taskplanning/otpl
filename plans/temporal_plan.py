from enum import Enum
from logging import raiseExceptions
from time import time
import numpy as np
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.domain import Domain
from pddl.effect import Effect, EffectType
from pddl.goal_descriptor import GoalDescriptor, GoalType
from pddl.problem import Problem
from pddl.grounding import Grounding
from pddl.operator import Operator
from pddl.time_spec import TimeSpec
from temporal_networks.temporal_network import TemporalNetwork

class HappeningType(Enum):
    PLAN_START   = "PLAN START"
    ACTION_START = "ACTION_START"
    ACTION_END   = "ACTION_END"
    
class Happening:
    def __init__(self, id : int, time : float, type : HappeningType, action_id : int = -1):
        self.id = id
        self.time = time
        self.action_id = action_id
        self.type = type
    
    def __repr__(self):
        return "Happening(time={}, type={}, action_id={})".format(self.time, self.type, self.action_id)

class PlanTemporalNetwork:
    """
    Represents the plan as a temporal network.
    """

    def __init__(self, domain : Domain, problem : Problem, grounding : Grounding = None):
        self.domain : Domain = domain
        self.problem : Problem = problem

        if grounding is None:
            grounding = Grounding()
            grounding.ground_problem(domain, problem)

        self.grounding : Grounding = grounding

        self.epsilon = 0.01
        
        # map temporal network nodes to happenings
        self.temporal_network : TemporalNetwork = None
        self.happening_dict : dict[int, Happening] = {}
        self.happenings : list[Happening] = []

    def read_from_file(self, plan_file):
        """
        Parses a plan from file and constructs a temporal network.
        Nodes in the network correspond to action start and ends.
        Edges in the network correspond to action durations and ordering constraints.
        Expects the file to be in correct format, one action per line:
        time: (action) [duration]
        """
        if self.domain is None or self.problem is None:
            raise Exception("Domain and problem must be set before reading plan from file.")

        if not self.grounding.grounded:
            self.grounding.ground_problem(self.domain, self.problem)

        self.temporal_network = TemporalNetwork()
        node_id = 0

        # add plan start happening to network
        self.temporal_network.add_node(node_id, "PLAN_START")
        self.happening_dict[node_id] = Happening(0, 0, HappeningType.PLAN_START)
        node_id += 1

        self.parse_actions(plan_file, node_id)
        self.construct_ordering_constraints()

    def parse_actions(self, plan_file, node_id):
        # read actions and create nodes
        with open(plan_file, 'r') as f:
            for line in f:
                # parse line, ignoring temporal information
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
                action_start = Happening(node_id, time, HappeningType.ACTION_START, action_id)
                self.temporal_network.add_node(node_id, label=formula.print_pddl() + "_start")
                self.happening_dict[node_id] = action_start
                node_id += 1

                # action end happening
                action_end = Happening(node_id, time + duration, HappeningType.ACTION_END, action_id)
                self.temporal_network.add_node(node_id, label=formula.print_pddl() + "_end")
                self.happening_dict[node_id] = action_end
                node_id += 1

                # create two edges for action duration
                self.temporal_network.add_edge(node_id - 2, node_id - 1, duration)
                self.temporal_network.add_edge(node_id - 1, node_id - 2, -duration)
        
        self.happenings = list(self.happening_dict.values())
        self.happenings.sort(key=lambda hap: hap.time)

    def construct_ordering_constraints(self):
        """
        Constructs ordering constraints between happenings.
        """
        init = self.grounding.get_initial_state_spike()

        for index, happening in enumerate(self.happenings):

            # find time spec of happening
            if happening.type == HappeningType.ACTION_START:
                time_spec = TimeSpec.AT_START
            elif happening.type == HappeningType.ACTION_END:
                time_spec = TimeSpec.AT_END
            else: continue

            # get simple conditions of happening
            pos, neg = self.grounding.get_action_condition_spike_from_id(happening.action_id, time_spec)

            # if happening is an action start, add overall conditions
            if time_spec == TimeSpec.AT_START:
                p, n = self.grounding.get_action_condition_spike_from_id(happening.action_id, TimeSpec.OVER_ALL)
                np.logical_or(pos, p, out=pos)
                np.logical_or(neg, n, out=neg)

            for prev_index in range(index - 1, -1, -1):
                prev = self.happenings[prev_index]
                if prev.type == HappeningType.ACTION_START:
                    time_spec = TimeSpec.AT_START
                elif prev.type == HappeningType.ACTION_END:
                    time_spec = TimeSpec.AT_END
                else: continue

                # get simple effects of previous happening
                adds, dels = self.grounding.get_action_effect_spike_from_id(prev.action_id, time_spec)              

                # check if the effects support the conditions
                pos_support = np.logical_and(pos, adds)
                neg_support = np.logical_and(neg, dels)
                if np.any(pos_support) or np.any(neg_support):

                    # add new edge to the temporal network
                    self.temporal_network.add_edge(happening.id, prev.id, -self.epsilon)

                    # remove the now-supported conditions
                    np.logical_xor(pos, pos_support, out=pos)
                    np.logical_xor(neg, neg_support, out=neg)

                    if time_spec == TimeSpec.AT_START:
                        p, n = self.grounding.get_action_condition_spike_from_id(happening.action_id, TimeSpec.OVER_ALL)
                        np.logical_and(pos_support, p, out=p)
                        np.logical_and(neg_support, n, out=n)
                        if np.any(p) or np.any(n):
                            self.add_interference_edges(index, prev_index, p, n, TimeSpec.OVER_ALL)
                        np.logical_xor(pos_support, p, out=pos_support)
                        np.logical_xor(neg_support, n, out=neg_support)
                        if np.any(pos_support) or np.any(neg_support):
                            self.add_interference_edges(index, prev_index, pos_support, neg_support, TimeSpec.AT_START)
                    elif time_spec == TimeSpec.AT_END:
                        self.add_interference_edges(index, prev_index, pos_support, neg_support, TimeSpec.AT_END)
                
                # stop if no conditions are remaining
                if not np.any(pos) and not np.any(neg):
                    break

            # add edge to plan start if any conditions remain
            if np.any(pos) or np.any(neg):
                self.temporal_network.add_edge(happening.id, 0, 0.0)

    def add_interference_edges(self, happening_index, support_index, pos_support, neg_support, condition_time_spec):

        for inter_index in range(len(self.happenings)):
            
            if inter_index == happening_index or inter_index == support_index:
                continue

            # find time spec of happening
            if self.happenings[inter_index].type == HappeningType.ACTION_START:
                time_spec = TimeSpec.AT_START
            elif self.happenings[inter_index].type == HappeningType.ACTION_END:
                time_spec = TimeSpec.AT_END
            else: continue

            adds, dels = self.grounding.get_action_effect_spike_from_id(self.happenings[inter_index].action_id, time_spec)

            # TODO fix interference not being found in the match domain

            # check if the effects interfere with the support
            if np.any(np.logical_and(pos_support, dels)) or np.any(np.logical_and(neg_support, adds)):
                source, sink = -1, -1
                if inter_index < support_index:
                    source = self.happenings[support_index].id
                    sink = self.happenings[inter_index].id
                    distance = -self.epsilon
                elif happening_index < inter_index and condition_time_spec != TimeSpec.OVER_ALL:
                    source = self.happenings[inter_index].id
                    sink = self.happenings[happening_index].id
                    distance = -self.epsilon
                elif happening_index < inter_index and condition_time_spec == TimeSpec.OVER_ALL:
                    
                    source = self.happenings[inter_index].id
                    sink = self.happenings[happening_index+1].id
                    distance = 0.0
                
                if source != -1 and sink != -1:
                    dist = self.temporal_network.find_shortest_path(source, sink)
                    if -self.epsilon < dist:
                        self.temporal_network.add_edge(source, sink, distance)