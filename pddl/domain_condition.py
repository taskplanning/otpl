"""
This file defines and implements the basic goal descriptors for PDDL2.2.
The implementation of comparison goals is implemented in DomainInequality.
"""
from typing import Union, List
from enum import Enum
from pddl.domain_formula import DomainFormula, TypedParameter
from pddl.domain_time_spec import TIME_SPEC 


class GoalType(Enum):
    EMPTY       = "empty"
    SIMPLE      = "conjunction"
    CONJUNCTION = "inequality"
    DISJUNCTION = "timed"
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


class GoalSimple(GoalDescriptor):

    def __init__(self, atomic_formula : DomainFormula) -> None:
        super().__init__(goal_type=GoalType.SIMPLE)
        self.atomic_formula = atomic_formula

    def __repr__(self) -> str:
        return self.atomic_formula.print_pddl(include_types=False)


class GoalConjunction(GoalDescriptor):

    def __init__(self, goals : List[GoalDescriptor]) -> None:
        super().__init__(goal_type=GoalType.CONJUNCTION)
        self.goals = goals

    def __repr__(self) -> str:
        return "(and " + " ".join([repr(g) for g in self.goals]) + ")"


class GoalDisjunction(GoalDescriptor):

    def __init__(self, goals : List[GoalDescriptor]) -> None:
        super().__init__(goal_type=GoalType.DISJUNCTION)
        self.goals = goals

    def __repr__(self) -> str:
        return "(or " + " ".join([repr(g) for g in self.goals]) + ")"


class GoalNegative(GoalDescriptor):

    def __init__(self, goal : GoalDescriptor) -> None:
        super().__init__(goal_type=GoalType.NEGATIVE)
        self.goal = goal

    def __repr__(self) -> str:
        return "(not " + repr(self.goal) + ")"
        

class GoalImplication(GoalDescriptor):

    def __init__(self, antecedent : GoalDescriptor, consequent : GoalDescriptor) -> None:
        super().__init__(goal_type=GoalType.IMPLICATION)
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self) -> str:
        return "(imples " + repr(self.antecedent) + " " + repr(self.consequent) + ")"


class GoalQuantified(GoalDescriptor):

    def __init__(self,
            typed_parameters : List[TypedParameter],
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


class TimedGoal(GoalDescriptor):
    """
    This class describes a simple add or delete effect with time specifier for durative action.
    """

    def __init__(self, time_spec : TIME_SPEC, goal : GoalDescriptor) -> None:
        super().__init__(goal_type=GoalType.TIMED)
        self.time_spec = time_spec
        self.goal = goal

    def __repr__(self) -> str:
        return "(" + self.time_spec.value + " " + str(self.goal) + ")"