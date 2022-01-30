from enum import Enum
from pddl.domain_condition import GoalDescriptor, GoalType
from pddl.domain_expression import ExprComposite


class DomainInequality(GoalDescriptor):
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
        
        super().__init__(goal_type=GoalType.COMPARISON)
        self.comparison_type = comparison_type
        self.lhs = lhs
        self.rhs = rhs
    
    def __repr__(self) -> str:
        return "(" + self.comparison_type.value + " " + str(self.lhs) + " " + str(self.rhs) + ")"