from enum import Enum
from pddl.atomic_formula import TypedParameter
from pddl.goal_descriptor import GoalDescriptor, GoalType
from pddl.expression import ExprComposite


class Inequality(GoalDescriptor):
    """
    A class used to store the numeric effects of an action.
    """

    class ComparisonType(Enum):
        GREATER   = ">"
        GREATEREQ = ">="
        LESS      = "<"
        LESSEQ    = "<="
        EQUALS    = "="

    def __init__(self,
            comparison_type : ComparisonType,
            lhs : ExprComposite,
            rhs : ExprComposite,
            ) -> None:
        
        super().__init__(goal_type=GoalType.COMPARISON)
        self.comparison_type = comparison_type
        self.lhs = lhs
        self.rhs = rhs
    
    def __repr__(self) -> str:
        return "(" + self.comparison_type.value + " " + str(self.lhs) + " " + str(self.rhs) + ")"

    def copy(self) -> 'GoalDescriptor':
        return Inequality(self.comparison_type, self.lhs.copy(), self.rhs.copy())

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        self.lhs.visit(visit_function, valid_types, args, kwargs)
        self.rhs.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'GoalDescriptor':
        return Inequality(self.comparison_type, self.lhs.bind_parameters(parameters), self.rhs.bind_parameters(parameters))