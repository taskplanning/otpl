from typing import Dict, List
from pddl.domain_condition import GoalDescriptor
from pddl.domain_formula import DomainFormula
from pddl.metric import Metric
from pddl.timed_initial_literal import TimedInitialLiteral


class Problem:
    """
    A class that describes a PDDL instance, including:
    - current objects
    - current state
    - goals & metric
    """

    def __init__(self, problem_name : str, domain_name : str) -> None:
        self.problem_name = problem_name
        self.domain_name = domain_name
        self.requirements : List[str] = []
        self.objects_type_map : Dict[str,str] = {}
        self.type_objects_map : Dict[str,List[str]] = {}
        self.propositions : List[DomainFormula] = []
        self.functions : List[DomainFormula] = []
        self.timed_initial_literals : List[TimedInitialLiteral] = []
        self.goal : GoalDescriptor = None
        self.metric : Metric = None

    def __str__(self) -> str:

        # header
        return_string = "(define (problem " + self.problem_name + ")\n" \
            + "(:domain " + self.domain_name + ")\n"

        # optional requirements
        if self.requirements:
            return_string = return_string + "(:requirements " + " ".join(self.requirements) + ")\n"

        # optional object declaration
        if self.objects_type_map:
            return_string += "(:objects\n"
            for obj, type in self.objects_type_map.items():
                return_string += "  " + obj + " - " + type + "\n"
            return_string += ")\n"

        # initial state     
        return_string += "(:init\n"
        for pred in self.propositions:
            return_string += "  " + pred.print_pddl() + "\n"
        for func in self.functions:
            return_string += "  (= " + func.print_pddl() + " " + str(func.function_value) + ")\n"
        for til in self.timed_initial_literals:
            return_string += "  " + repr(til) + "\n"
        return_string += ")\n"

        # goal & metric
        if self.goal: return_string += "(:goal " + repr(self.goal) + ")\n"
        if self.metric: return_string += repr(self.metric) + "\n"

        # end problem
        return_string += ')'

        return return_string
        