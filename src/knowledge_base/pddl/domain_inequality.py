from enum import Enum
from domain_expression import ExprComposite


class DomainInequality:
    """
    A class used to store the numeric effects of an action.
    """

    class COMPARISON_TYPE(Enum):
        GREATER   = ">"
        GREATEREQ = ">="
        LESS      = "<"
        LESSEQ    = "<="
        EQUALS    = "="

    def __init__(self,
            comparison_type : COMPARISON_TYPE,
            lhs : ExprComposite,
            rhs : ExprComposite,
            ) -> None:
        self.comparison_type = comparison_type
        self.LHS = lhs
        self.RHS = rhs
    
    def __repr__(self) -> str:
        return "(" + self.comparison_type.value + " " + str(self.lhs) + " " + str(self.rhs) + ")"