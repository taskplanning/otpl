from enum import Enum
from typing import List
from pddl.atomic_formula import AtomicFormula

class ExprBase:
    """
    A class used to represent a numerical expression (base types)
    """

    class ExprType(Enum):
        CONSTANT        = "constant"
        FUNCTION        = "function"
        BINARY_OPERATOR = "operator"
        UMINUS          = "uminus"
        SPECIAL         = "special"

    class BinaryOperator(Enum):
        ADD    = "+"
        SUB    = "-"
        MUL    = "*"
        DIV    = "/"

    class SpecialType(Enum):
        HASHT      = "#t"
        TOTAL_TIME = "?total-time"
        DURATION   = "?duration"

    def __init__(self,
            expr_type : ExprType,
            constant : float = 0.0,
            function : AtomicFormula = None,
            op : BinaryOperator = None,
            special_type : SpecialType = None) -> None:
        self.expr_type = expr_type
        self.constant = constant
        self.function = function
        self.op = op
        self.special_type = special_type
    
    def __repr__(self) -> str:
        if self.expr_type == ExprBase.ExprType.CONSTANT:
            return str(self.constant)
        elif self.expr_type == ExprBase.ExprType.FUNCTION:
            return self.function.print_pddl()
        elif self.expr_type == ExprBase.ExprType.BINARY_OPERATOR:
            return self.op.value
        elif self.expr_type == ExprBase.ExprType.UMINUS:
            return "-"
        elif self.expr_type == ExprBase.ExprType.SPECIAL:
            return self.special_type.value

class ExprComposite:   
    """
    A class used to represent a numerical expression (composite)
    Stores a list of ExprBase in prefix notation.
    """

    def __init__(self, tokens : List[ExprBase]) -> None:
        self.tokens = tokens

    def __repr__(self) -> str:
        op_stack = 0
        return_string = ""
        for token in self.tokens:
            if token.expr_type == ExprBase.ExprType.BINARY_OPERATOR:
                return_string += "(" + repr(token) + " "
                op_stack = op_stack + 2
            else:
                return_string += repr(token)
                if op_stack==2:
                    return_string += " "
                    op_stack = op_stack - 1
                elif op_stack==1:
                    return_string += ")"
                    op_stack = 0
        return return_string
