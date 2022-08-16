import numpy as np

from pddl.domain import Domain
from pddl.effect import EffectNegative, EffectSimple, EffectType
from pddl.goal_descriptor import GoalConjunction, GoalDescriptor, GoalSimple, GoalType
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.metric import Metric
from pddl.state import State
from pddl.timed_initial_literal import TimedInitialLiteral
from pddl.grounding import Grounding

class Problem:
    """
    A class that describes a PDDL instance, including:
    - current objects
    - current state
    - goals & metric
    """

    def __init__(self, problem_name : str, domain : Domain) -> None:

        # problem header
        self.problem_name : str = problem_name
        self.domain_name : str = domain.domain_name
        self.domain = domain
        self.requirements : list[str] = []

        # current time (subtracted from TILs on printing)        
        self.current_time = 0.0

        # objects
        self.objects_type_map : dict[str,str] = {}
        self.type_objects_map : dict[str,list[str]] = {}

        # initial state (ungrounded form)
        self.propositions : list[AtomicFormula] = []
        self.functions : list[tuple[float,AtomicFormula]] = []
        self.timed_initial_literals : list[TimedInitialLiteral] = []

        # grounding
        self.grounding = Grounding()

        # goal and metric
        self.goal : GoalDescriptor = None
        self.metric : Metric = None

    # ========= #
    # grounding #
    # ========= #

    def ground(self):
        self.grounding.ground_problem(self.domain, self)

    # ====== #
    # states #
    # ====== #

    def get_initial_state(self) -> State:
        """
        return numpy array of propositional initial state.
        """
        if not self.grounding.grounded:
            self.grounding.ground_problem(self.domain, self)

        state = State()
        state.time = self.current_time
        state.logical = np.zeros(self.grounding.proposition_count, dtype=bool)
        state.numeric = np.array([np.nan] * self.grounding.function_count, dtype=float)
        state.logical[[ self.grounding.get_id_from_proposition(p) for p in self.propositions ]] = True
        for value, pne in self.functions:
            state.numeric[self.grounding.get_id_from_pne(pne)] = value
        return state


    def update_with_state(self, state : State) -> None:
        """
        Update the problem object to the given state.
        """
        self.current_time = state.time

        # propositions
        self.propositions.clear()
        for id in np.nonzero(state.logical)[0]:
            self.propositions.append(self.grounding.get_proposition_from_id(id))

        # functions
        self.functions.clear()
        for id in np.nonzero(np.logical_not(np.isnan(state.numeric)))[0]:
            self.functions.append((state.numeric[id], self.grounding.get_pne_from_id(id)))

    # ======= #
    # cloning #
    # ======= #

    def copy(self) -> 'Problem':
        """
        Returns a deep copy of the problem.
        """
        clone = Problem(self.problem_name, self.domain)
        clone.requirements = self.requirements.copy()

        clone.objects_type_map = self.objects_type_map.copy()
        for type in self.type_objects_map:
            clone.type_objects_map[type] = self.type_objects_map[type].copy()
        
        for prop in self.propositions: clone.propositions.append(prop.copy())
        for val,func in self.functions: clone.functions.append((val,func.copy()))
        for til in self.timed_initial_literals: clone.timed_initial_literals.append(til.copy())

        clone.goal = self.goal.copy() if self.goal else None
        clone.metric = self.metric.copy() if self.metric else None
        
        clone.current_time = self.current_time

        return clone

    def copy_with_state(self, state : State) -> 'Problem':
        """
        Returns a copy of the problem with the given state.
        """
        clone = self.copy()
        clone.update_with_state(state)
        return clone

    # ======== #
    # visiting #
    # ======== #

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}):
        """
        Calls the visit function on self and recurses through the visit methods of members.
        param visit_function: the function to call on self.
        param valid_types: a set of types to visit. If None, all types are visited.
        """
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        
        for prop in self.propositions:
            prop.visit(visit_function, valid_types, args, kwargs)
        
        for val,func in self.functions:
            func.visit(visit_function, valid_types, args, kwargs)
        
        for til in self.timed_initial_literals:
            til.visit(visit_function, valid_types, args, kwargs)
        
        if self.goal:
            self.goal.visit(visit_function, valid_types, args, kwargs)

        if self.metric:
            self.metric.visit(visit_function, valid_types, args, kwargs)

    # ======= #
    # setters #
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
            raise Exception("Predicate {} does not exist.".format(predicate_name))
        if len(self.domain.predicates[predicate_name].typed_parameters) != len(params):
            raise Exception("Proposition {} has wrong number of parameters.".format(predicate_name))
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
            raise Exception("Predicate {} does not exist.".format(predicate_name))
        if len(self.domain.predicates[predicate_name].typed_parameters) != len(params):
            raise Exception("Proposition {} has wrong number of parameters.".format(predicate_name))
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
        # TODO add effect matching here to avoid duplicates
        self.timed_initial_literals.append(timed_initial_literal)

    def add_assignment_from_str(self, value : float, function_name : str, params : list[str] = []):
        """
        Adds a new function assignment to the initial state using AtomicFormula.from_string()
        param value: the value to be assigned.
        param name: the name of the function to add.
        param params: list of parameter values.
        """
        if function_name not in self.domain.functions:
            raise Exception("Function {} does not exist.".format(function_name))
        if len(self.domain.functions[function_name].typed_parameters) != len(params):
            raise Exception("Function {} has wrong number of parameters.".format(function_name))
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
            if match and value == val: 
                return
            if match:
                # new assignment overrides the previous
                self.functions.remove((val,func))
                break
        self.functions.append((value,function))

    def add_simple_goal_from_str(self, predicate_name : str, params : list[str] = []):
        """
        Adds a propositional goal from string using AtomicFormula.from_string()
        param name: the name of the predicate to add.
        param values: list of parameter values.
        """
        if predicate_name not in self.domain.predicates:
            raise Exception("Predicate {} does not exist.".format(predicate_name))
        if len(self.domain.predicates[predicate_name].typed_parameters) != len(params):
            raise Exception("Proposition {} has wrong number of parameters.".format(predicate_name))
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
    # printing #
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
            if self.current_time <= til.time:
                return_string += "  " + til.print_pddl(self.current_time) + "\n"
        return_string += ")\n"

        # goal & metric
        if self.goal: return_string += "(:goal " + repr(self.goal) + ")\n"
        if self.metric: return_string += repr(self.metric) + "\n"

        # end problem
        return_string += ')'

        return return_string
        