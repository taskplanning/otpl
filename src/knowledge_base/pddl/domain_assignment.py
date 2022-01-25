from enum import Enum
from domain_formula import DomainFormula
from domain_expression import ExprComposite

class DomainAssignment:
    """
    A class used to store the numeric effects of an action.
    """

    class AssignmentType(Enum):
        ASSIGN      = "assign"
        INCREASE    = "increase"
        DECREASE    = "decrease"
        SCALE_UP    = "scale up"
        SCALE_DOWN  = "scale down"
        ASSIGN_CTS  = "assign continuous"

    def __init__(self, assign_type : AssignmentType, lhs : DomainFormula, rhs : ExprComposite) -> None:
        self.assign_type = assign_type
        self.LHS = lhs
        self.RHS = rhs
        # catch possible mismatch between LHS/RHS groundedness
        assert(lhs.grounded == rhs.grounded)
        self.grounded = lhs.grounded

    def __repr__(self) -> str:
        return "(" + self.assign_type.name + self.lhs + ' ' + self.rhs + ')' 