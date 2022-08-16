"""
This file defines and implements the basic goal descriptors for PDDL2.2.
The implementation of comparison goals is implemented in DomainInequality.
"""
from enum import Enum
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.time_spec import TimeSpec 


class GoalType(Enum):
    EMPTY       = "empty"
    SIMPLE      = "simple"
    CONJUNCTION = "conjunction"
    DISJUNCTION = "disjunction"
    NEGATIVE    = "negative"
    IMPLICATION = "implication"
    EXISTENTIAL = "existential"
    UNIVERSAL   = "universal"
    COMPARISON  = "comparison"
    TIMED       = "timed"


class GoalDescriptor:
    """
    This superclass describes a goal for action or goal spec.
    """

    def __init__(self, goal_type : GoalType = GoalType.EMPTY) -> None:
        self.goal_type = goal_type

    def __repr__(self) -> str:
        return "()"

    def copy(self) -> 'GoalDescriptor':
        """
        Returns a deep copy of the goal.
        """
        return GoalDescriptor()

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        """
        Calls the visit function on self and recurses through the visit methods of members.
        param visit_function: the function to call on self.
        param valid_types: a set of types to visit. If None, all types are visited.
        """
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'GoalDescriptor':
        """
        Binds the parameters of a copy of the goal to the given list of parameters.
        """
        return GoalDescriptor()
    
    def filter_goal_to_time_spec(self, time_spec : TimeSpec) -> 'GoalDescriptor':
        """
        Filters the goals to the given time spec.
        """
        return self

class GoalSimple(GoalDescriptor):

    def __init__(self, atomic_formula : AtomicFormula) -> None:
        super().__init__(goal_type=GoalType.SIMPLE)
        self.atomic_formula = atomic_formula

    def __repr__(self) -> str:
        return self.atomic_formula.print_pddl(include_types=False)

    def copy(self) -> 'GoalDescriptor':
        return GoalSimple(self.atomic_formula.copy())

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        self.atomic_formula.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'GoalDescriptor':
        return GoalSimple(self.atomic_formula.bind_parameters(parameters))

class GoalConjunction(GoalDescriptor):

    def __init__(self, goals : list[GoalDescriptor]) -> None:
        super().__init__(goal_type=GoalType.CONJUNCTION)
        self.goals = goals

    def __repr__(self) -> str:
        return "(and " + " ".join([repr(g) for g in self.goals]) + ")"

    def copy(self) -> 'GoalDescriptor':
        return GoalConjunction([g.copy() for g in self.goals])

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        for g in self.goals:
            g.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'GoalDescriptor':
        return GoalConjunction([g.bind_parameters(parameters) for g in self.goals])

    def filter_goal_to_time_spec(self, time_spec : TimeSpec) -> 'GoalDescriptor':
        goals = [g.filter_goal_to_time_spec(time_spec) for g in self.goals]
        return GoalConjunction([g for g in goals if g])

class GoalDisjunction(GoalDescriptor):

    def __init__(self, goals : list[GoalDescriptor]) -> None:
        super().__init__(goal_type=GoalType.DISJUNCTION)
        self.goals = goals

    def __repr__(self) -> str:
        return "(or " + " ".join([repr(g) for g in self.goals]) + ")"

    def copy(self) -> 'GoalDescriptor':
        return GoalDisjunction([g.copy() for g in self.goals])

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        for g in self.goals:
            g.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'GoalDescriptor':
        return GoalDisjunction([g.bind_parameters(parameters) for g in self.goals])

class GoalNegative(GoalDescriptor):

    def __init__(self, goal : GoalDescriptor) -> None:
        super().__init__(goal_type=GoalType.NEGATIVE)
        self.goal = goal

    def __repr__(self) -> str:
        return "(not " + repr(self.goal) + ")"

    def copy(self) -> 'GoalDescriptor':
        return GoalNegative(self.goal.copy())

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        self.goal.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'GoalDescriptor':
        return GoalNegative(self.goal.bind_parameters(parameters))

class GoalImplication(GoalDescriptor):

    def __init__(self, antecedent : GoalDescriptor, consequent : GoalDescriptor) -> None:
        super().__init__(goal_type=GoalType.IMPLICATION)
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self) -> str:
        return "(imples " + repr(self.antecedent) + " " + repr(self.consequent) + ")"

    def copy(self) -> 'GoalDescriptor':
        return GoalImplication(self.antecedent.copy(), self.consequent.copy())

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        self.antecedent.visit(visit_function, valid_types, args, kwargs)
        self.consequent.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'GoalDescriptor':
        return GoalImplication(self.antecedent.bind_parameters(parameters), self.consequent.bind_parameters(parameters))

class GoalQuantified(GoalDescriptor):

    def __init__(self,
            typed_parameters : list[TypedParameter],
            goal : GoalDescriptor,
            quantification : GoalType
            ) -> None:
        super().__init__(goal_type=quantification)
        assert(quantification==GoalType.EXISTENTIAL or self.goal_type==GoalType.UNIVERSAL)
        self.typed_parameters = typed_parameters
        self.goal = goal

    def __repr__(self) -> str:
        return ("(forall (" if self.goal_type==GoalType.UNIVERSAL else "(exists (") \
            + ' '.join([p.label + " - " + p.type for p in self.typed_parameters]) \
            + ") " + repr(self.goal) + ")"

    def copy(self) -> 'GoalDescriptor':
        params = [ TypedParameter(p.type, p.label, p.value) for p in self.typed_parameters ]
        return GoalQuantified(params, self.goal.copy(), self.goal_type)

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        for p in self.typed_parameters:
            p.visit(visit_function, valid_types, args, kwargs)
        self.goal.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'GoalDescriptor':
        """
        Binds the unquantified parameters of an ungrounded goal to the given list of parameters.
        """
        return GoalQuantified(self.typed_parameters, self.goal.bind_parameters(parameters), self.goal_type)

class TimedGoal(GoalDescriptor):
    """
    This class describes a simple add or delete effect with time specifier for durative action.
    """

    def __init__(self, time_spec : TimeSpec, goal : GoalDescriptor) -> None:
        super().__init__(goal_type=GoalType.TIMED)
        self.time_spec = time_spec
        self.goal = goal

    def __repr__(self) -> str:
        return "(" + self.time_spec.value + " " + str(self.goal) + ")"

    def copy(self) -> 'GoalDescriptor':
        return TimedGoal(self.time_spec, self.goal.copy())
        
    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        self.goal.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'GoalDescriptor':
        return TimedGoal(self.time_spec, self.goal.bind_parameters(parameters))

    def filter_goal_to_time_spec(self, time_spec : TimeSpec) -> 'GoalDescriptor':
        if time_spec == self.time_spec:
            return self
        return None