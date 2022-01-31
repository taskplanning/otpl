from enum import Enum
from pddl.effect import Effect, EffectType
from pddl.atomic_formula import AtomicFormula
from pddl.expression import ExprComposite


class AssignmentType(Enum):
    ASSIGN       = "assign"
    INCREASE     = "increase"
    DECREASE     = "decrease"
    SCALE_UP     = "scale-up"
    SCALE_DOWN   = "scale-down"
    INCREASE_CTS = "increase continuous"
    DECREASE_CTS = "decrease continuous"


class Assignment(Effect):
    """
    A class used to store the numeric effects of an action.
    """

    def __init__(self, assign_type : AssignmentType, lhs : AtomicFormula, rhs : ExprComposite) -> None:
        super().__init__(effect_type=EffectType.ASSIGN)
        self.assign_type = assign_type
        self.lhs = lhs
        self.rhs = rhs
        # catch possible mismatch between LHS/RHS groundedness
        # TODO switch to method that can be handled by ExprComposite
        # assert(lhs.grounded == rhs.grounded)

    def __repr__(self) -> str:
        if self.assign_type == AssignmentType.INCREASE_CTS:
            return "(increase " + self.lhs.print_pddl() + ' ' + repr(self.rhs) + ')' 
        elif self.assign_type == AssignmentType.DECREASE_CTS:
            return "(decrease " + self.lhs.print_pddl() + ' ' + repr(self.rhs) + ')' 
        return "(" + self.assign_type.value + " " + self.lhs.print_pddl() + ' ' + repr(self.rhs) + ')' 