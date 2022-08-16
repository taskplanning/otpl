import argparse
import sys
import time

import numpy as np
from pddl.atomic_formula import TypedParameter
from pddl.grounding import Grounding
from pddl.operator import Operator
from pddl.domain import Domain
from pddl.problem import Problem

class PlanSequential:
    """
    Represents a plan as a list of STRIPS actions.
    """

    def __init__(self, domain : Domain, problem : Problem):
        self.domain : Domain = domain
        self.problem : Problem = problem
        self.action_list : list[Operator] = []

    def read_from_file(self, plan_file):
        """
        Parses a plan from file into a list of grounded actions.
        Expects the file to be in correct format, one action per line:
        time: (action) [duration]
        """
        if self.domain is None or self.problem is None:
            raise Exception("Domain and problem must be set before reading plan from file.")

        with open(plan_file, 'r') as f:
            for line in f:
                # parse line, ignoring temporal information
                action = line.split(":")[1].split("[")[0].strip()

                # get the action name and parameters
                tokens = action.replace("(","").replace(")","").split()
                op = self.domain.operators[tokens[0]]
                if not op: raise Exception("Action " + action + " not found in domain.")

                objects = tokens[1:]
                if len(objects) != len(op.formula.typed_parameters):
                    raise Exception("Action " + action + " has wrong number of parameters.")

                # create grounded action
                parameters = []
                for param, object in zip(op.formula.typed_parameters, objects):
                    parameters.append(TypedParameter(param.type, param.label, object))
                op = op.bind_parameters(parameters)
                self.action_list.append(op)

    #============#
    # validation #
    #============#

    def check_plan(self, print_results=False) -> bool:

        state = self.problem.get_initial_state()
        grounding = self.problem.grounding

        # check if the plan is executable
        for action in self.action_list:

            pos, neg = grounding.get_simple_action_condition(action)
            result = np.logical_xor(pos, np.logical_and(pos, state.logical))
            if np.any(result):
                if print_results:
                    print("Action " + str(action.formula) + " is not applicable.")
                    for index in np.nonzero(result)[0]:
                        print("Positive condition is not met: " + str(grounding.get_proposition_from_id(index)))
                return False

            result = np.logical_xor(neg, np.logical_and(neg, np.logical_not(state.logical)))
            if np.any(result):
                if print_results:
                    print("Action " + str(action.formula) + " is not applicable.")        
                    for index in np.nonzero(result)[0]:
                        print("Negative condition is not met: " + str(grounding.get_proposition_from_id(index)))
                return False

            # apply action effects
            action_id = grounding.get_id_from_action(action)
            grounding.apply_simple_action_effects(action_id, state)

        if print_results:
            print("Plan is executable.")

        # check if goal is satisfied
        positive_conditions = np.zeros(grounding.proposition_count, dtype=bool)
        negative_conditions = np.zeros(grounding.proposition_count, dtype=bool)
        grounding.get_simple_conditions(self.problem.goal, positive_conditions, negative_conditions)
        
        # positive goals
        goal_achieved = True
        result = np.logical_xor(positive_conditions, np.logical_and(positive_conditions, state.logical))
        if np.any(result):
            if print_results:
                print("Goal is not satisfied.")
                for index in np.nonzero(result)[0]:
                    print("Positive goal is not met: " + str(grounding.get_proposition_from_id(index)))
            goal_achieved = False

        # negative goals
        result = np.logical_xor(negative_conditions, np.logical_and(negative_conditions, np.logical_not(state.logical)))
        if np.any(result):
            if print_results:
                print("Goal is not satisfied.")
                for index in np.nonzero(result)[0]:
                    print("Negative goal is not met: " + str(grounding.get_proposition_from_id(index)))
            goal_achieved = False

        if goal_achieved and print_results:
            print("Goal is satisfied.")

        return goal_achieved

    #==================#
    # printing methods #
    #==================#

    def print_plan(self, step_size=0.1):
        """
        Prints the plan one action per line.
        """
        time = 0.0
        for action in self.action_list:
            print("{:.2f}:".format(time), str(action.formula), "["+str(step_size)+"]")
            time = time + step_size

    def print_actions(self):
        """
        Prints the actions in the plan.
        """
        for action in self.action_list:
            print(str(action))