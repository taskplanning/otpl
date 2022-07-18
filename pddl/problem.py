from typing import Dict, List
from pddl.domain import Domain
from pddl.goal_descriptor import GoalConjunction, GoalDescriptor, GoalSimple, GoalType
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.metric import Metric
from pddl.timed_initial_literal import TimedInitialLiteral


class Problem:
    """
    A class that describes a PDDL instance, including:
    - current objects
    - current state
    - goals & metric
    """

    def __init__(self, problem_name : str, domain : Domain) -> None:
        self.problem_name = problem_name
        self.domain_name = domain.domain_name
        self.domain = domain
        self.requirements : List[str] = []
        self.objects_type_map : Dict[str,str] = {}
        self.type_objects_map : Dict[str,List[str]] = {}
        self.propositions : List[AtomicFormula] = []
        self.functions : List[AtomicFormula] = []
        self.timed_initial_literals : List[TimedInitialLiteral] = []
        self.goal : GoalDescriptor = None
        self.metric : Metric = None

    # ======= #
    # Setters #
    # ======= #

    def add_object(self, name : str, type : str = "object"):
        """
        Adds a new object to the domain.
        param name: the name of the new object.
        param type: the type of the new object.
        """
        if type not in self.domain.type_tree and type != "object":
            self.domain.add_type(type)
        if type not in self.type_objects_map:
            self.type_objects_map[type] = []
        self.objects_type_map[name] = type
        self.type_objects_map[type].append(name)

    def add_proposition_from_str(self, name : str, values : list[str] = []):
        """
        Adds a new predicate to the domain using AtomicFormula.from_string()
        param name: the name of the predicate to add.
        param values: list of parameter values.
        """
        if name not in self.domain.predicates:
            raise Exception("Predicate {.s} does not exist.".format(name))
        if len(self.domain.predicates[name].typed_parameters) != len(values):
            raise Exception("Proposition {.s} has wrong number of parameters.".format(name))
        params = []
        for param, value in zip(self.domain.predicates[name].typed_parameters, values):
            params.append(TypedParameter(param.type, param.label,value))
        self.add_proposition(AtomicFormula(name, params))

    def add_proposition(self, proposition : AtomicFormula):
        """
        Adds a new proposition to the initial state.
        param propition: the new proposition to add.
        """
        self.propositions.append(proposition)

    def add_simple_goal_from_str(self, name : str, values : list[str] = []):
        """
        Adds a propositional goal from string using AtomicFormula.from_string()
        param name: the name of the predicate to add.
        param values: list of parameter values.
        """
        if name not in self.domain.predicates:
            raise Exception("Predicate {.s} does not exist.".format(name))
        if len(self.domain.predicates[name].typed_parameters) != len(values):
            raise Exception("Proposition {.s} has wrong number of parameters.".format(name))
        params = []
        for param, value in zip(self.domain.predicates[name].typed_parameters, values):
            params.append(TypedParameter(param.type, param.label,value))
        self.add_simple_goal(AtomicFormula(name, params))

    def add_simple_goal(self, predicate : AtomicFormula):
        """
        Adds a propositional goal.
        If the problem already has a non-conjunctive goal then the new and existing
        goals will be wrapped together within a new conjunctive goal.
        """
        condition = GoalSimple(predicate)
        if not self.goal or self.goal.goal_type == GoalType.EMPTY:
            self.goal = condition
        elif self.goal.goal_type == GoalType.CONJUNCTION:
            self.goal : GoalConjunction
            self.goal.goals.append(condition)
        else:
            self.goal = GoalConjunction(goals=[self.goal, condition])

    # ======== #
    # Printing #
    # ======== #

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
        