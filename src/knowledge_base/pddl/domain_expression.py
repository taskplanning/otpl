from enum import Enum
from typing import List
from domain_formula import DomainFormula

class ExprBase:
    """
    A class used to represent a numerical expression (base types)
    """

    class EXPR_TYPE(Enum):
        CONSTANT = "constant"
        FUNCTION = "function"
        OPERATOR = "operator"
        SPECIAL  = "special"

    class OPERATOR(Enum):
        ADD    = "+"
        SUB    = "-"
        MUL    = "*"
        DIV    = "/"
        UMINUS = "-"

    class SPECIAL_TYPE(Enum):
        HASHT      = "#t"
        TOTAL_TIME = "?total-time"
        DURATION   = "?duration"

    def __init__(self,
            expr_type : EXPR_TYPE,
            constant : float = 0.0,
            function : DomainFormula = None,
            op : OPERATOR = None,
            special_type : SPECIAL_TYPE = None) -> None:
        self.expr_type = expr_type
        self.constant = constant
        self.function = function
        self.op = op
        self.special_type = special_type
    
    def __repr__(self) -> str:
        if self.expr_type == ExprBase.EXPR_TYPE.CONSTANT:
            return str(self.value)
        if self.expr_type == ExprBase.EXPR_TYPE.FUNCTION:
            return str(function)
        if self.expr_type == ExprBase.EXPR_TYPE.OPERATOR:
            return self.op.value
        if self.expr_type == ExprBase.EXPR_TYPE.SPECIAL:
            return self.special_type.value

class ExprComposite:   
    """
    A class used to represent a numerical expression (composite)
    Stores a list of ExprBase in prefix notation.
    """

    def __init__(self, tokens : List[ExprBase]) -> None:
        self.tokens = tokens