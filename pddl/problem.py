import numpy as np
from pddl.domain import Domain
from pddl.effect import EffectNegative, EffectSimple
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
        self.problem_name : str = problem_name
        self.domain_name : str = domain.domain_name
        self.domain = domain
        self.requirements : list[str] = []
        self.objects_type_map : dict[str,str] = {}
        self.type_objects_map : dict[str,list[str]] = {}
        self.propositions : list[AtomicFormula] = []
        self.functions : list[tuple[float,AtomicFormula]] = []
        self.timed_initial_literals : list[TimedInitialLiteral] = []
        self.goal : GoalDescriptor = None
        self.metric : Metric = None
        self.current_time = 0.0

    # =============== #
    # Problem cloning #
    # =============== #

    def copy(self) -> 'Problem':
        """
        Returns a deep copy of the problem.
        """
        clone = Problem(self.problem_name, self.domain)
        clone.requirements = self.requirements.copy()

        clone.objects_type_map = self.objects_type_map.copy()
        for type in self.type_objects_map:
            clone.type_objects_map[type] = self.type_objects_map[type].copy()
        
        # TODO do a deep copy here
        for prop in self.propositions: clone.propositions.append(prop.copy())
        for val,func in self.functions: clone.functions.append((val,func.copy()))
        for til in self.timed_initial_literals: clone.timed_initial_literals.append(til.copy())

        # TODO do any kind of copy here
        clone.goal = self.goal.copy()
        clone.metric = self.metric.copy()

        clone.current_time = self.current_time
        return clone

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

    def add_proposition_from_str(self, predicate_name : str, params : list[str] = []):
        """
        Adds a new proposition to the initial state using AtomicFormula.from_string()
        param name: the name of the proposition to add.
        param params: list of parameter values.
        """
        if predicate_name not in self.domain.predicates:
            raise Exception("Predicate {.s} does not exist.".format(predicate_name))
        if len(self.domain.predicates[predicate_name].typed_parameters) != len(params):
            raise Exception("Proposition {.s} has wrong number of parameters.".format(predicate_name))
        typed_params = []
        for param, value in zip(self.domain.predicates[predicate_name].typed_parameters, params):
            typed_params.append(TypedParameter(param.type, param.label,value))
        self.add_proposition(AtomicFormula(predicate_name, typed_params))

    def add_proposition(self, proposition : AtomicFormula):
        """
        Adds a new proposition to the initial state.
        param propition: the new proposition to add.
        """
        for prop in self.propositions:
            if prop.name != proposition.name: continue
            if len(prop.typed_parameters) != len(proposition.typed_parameters): continue
            match = True
            for param1, param2 in zip(prop.typed_parameters, proposition.typed_parameters):
                if param1.value != param2.value:
                    match = False
                    break
            if match: return
        self.propositions.append(proposition)

    def add_til_from_str(self, time : float, predicate_name : str, params : list[str] = [], negative : bool = False):
        """
        Adds a new TIL to the problem using AtomicFormula.from_string()
        param time: the time at which the TIL should occur.
        param name: the name of the timed proposition.
        param params: list of parameter values.
        param negative: True if the TIL is negative.
        """
        if predicate_name not in self.domain.predicates:
            raise Exception("Predicate {.s} does not exist.".format(predicate_name))
        if len(self.domain.predicates[predicate_name].typed_parameters) != len(params):
            raise Exception("Proposition {.s} has wrong number of parameters.".format(predicate_name))
        typed_params = []
        for param, value in zip(self.domain.predicates[predicate_name].typed_parameters, params):
            typed_params.append(TypedParameter(param.type, param.label,value))
        formula = AtomicFormula(predicate_name, typed_params)
        effect = EffectNegative(formula) if negative else EffectSimple(formula)
        self.timed_initial_literals.append(TimedInitialLiteral(time, effect))

    def add_til(self, timed_initial_literal : TimedInitialLiteral):
        """
        Adds a timed initial literal to the initial state.
        """
        self.timed_initial_literals.append(timed_initial_literal)

    def add_assignment_from_str(self, value : float, function_name : str, params : list[str] = []):
        """
        Adds a new function assignment to the initial state using AtomicFormula.from_string()
        param value: the value to be assigned.
        param name: the name of the function to add.
        param params: list of parameter values.
        """
        if function_name not in self.domain.functions:
            raise Exception("Function {.s} does not exist.".format(function_name))
        if len(self.domain.functions[function_name].typed_parameters) != len(params):
            raise Exception("Function {.s} has wrong number of parameters.".format(function_name))
        typed_params = []
        for param, value in zip(self.domain.functions[function_name].typed_parameters, params):
            typed_params.append(TypedParameter(param.type, param.label,value))
        self.add_assignment(value, AtomicFormula(function_name, typed_params))

    def add_assignment(self, value : float, function : AtomicFormula):
        """
        Adds a function assignment to the initial state.
        """
        for val, func in self.functions:
            if func.name != function.name: continue
            if len(func.typed_parameters) != len(function.typed_parameters): continue
            match = True
            for param1, param2 in zip(func.typed_parameters, function.typed_parameters):
                if param1.value != param2.value:
                    match = False
                    break
            if match: return
        self.functions.append((value,function))

    def add_simple_goal_from_str(self, predicate_name : str, params : list[str] = []):
        """
        Adds a propositional goal from string using AtomicFormula.from_string()
        param name: the name of the predicate to add.
        param values: list of parameter values.
        """
        if predicate_name not in self.domain.predicates:
            raise Exception("Predicate {.s} does not exist.".format(predicate_name))
        if len(self.domain.predicates[predicate_name].typed_parameters) != len(params):
            raise Exception("Proposition {.s} has wrong number of parameters.".format(predicate_name))
        typed_params = []
        for param, value in zip(self.domain.predicates[predicate_name].typed_parameters, params):
            typed_params.append(TypedParameter(param.type, param.label,value))
        self.add_simple_goal(AtomicFormula(predicate_name, typed_params))

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
            return_string += "  (= " + func[1].print_pddl() + " " + str(func[0]) + ")\n"
        for til in self.timed_initial_literals:
            return_string += "  " + repr(til) + "\n"
        return_string += ")\n"

        # goal & metric
        if self.goal: return_string += "(:goal " + repr(self.goal) + ")\n"
        if self.metric: return_string += repr(self.metric) + "\n"

        # end problem
        return_string += ')'

        return return_string
        