from enum import Enum
from pddl.atomic_formula import AtomicFormula, TypedParameter

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

    def copy(self) -> 'ExprBase':
        """
        Returns a deep copy of the expression.
        """
        if self.expr_type == ExprBase.ExprType.CONSTANT:
            return ExprBase(ExprBase.ExprType.CONSTANT, constant=self.constant)
        elif self.expr_type == ExprBase.ExprType.FUNCTION:
            return ExprBase(ExprBase.ExprType.FUNCTION, function=self.function.copy())
        elif self.expr_type == ExprBase.ExprType.BINARY_OPERATOR:
            return ExprBase(ExprBase.ExprType.BINARY_OPERATOR, op=self.op)
        elif self.expr_type == ExprBase.ExprType.UMINUS:
            return ExprBase(ExprBase.ExprType.UMINUS)
        elif self.expr_type == ExprBase.ExprType.SPECIAL:
            return ExprBase(ExprBase.ExprType.SPECIAL, special_type=self.special_type)

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        if self.expr_type == ExprBase.ExprType.FUNCTION:
            self.function.visit(visit_function, valid_types, args, kwargs)
        
    def bind_parameters(self, parameters : list[TypedParameter]) -> 'ExprBase':
        """
        Binds the parameters of a copy of the expression to the given list of parameters.
        """
        if self.expr_type == ExprBase.ExprType.CONSTANT:
            return ExprBase(ExprBase.ExprType.CONSTANT, constant=self.constant)
        elif self.expr_type == ExprBase.ExprType.FUNCTION:
            return ExprBase(ExprBase.ExprType.FUNCTION, function=self.function.bind_parameters(parameters))
        elif self.expr_type == ExprBase.ExprType.BINARY_OPERATOR:
            return ExprBase(ExprBase.ExprType.BINARY_OPERATOR, op=self.op)
        elif self.expr_type == ExprBase.ExprType.UMINUS:
            return ExprBase(ExprBase.ExprType.UMINUS)
        elif self.expr_type == ExprBase.ExprType.SPECIAL:
            return ExprBase(ExprBase.ExprType.SPECIAL, special_type=self.special_type)

class ExprComposite:   
    """
    A class used to represent a numerical expression (composite)
    Stores a list of ExprBase in prefix notation.
    """

    def __init__(self, tokens : list[ExprBase]) -> None:
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

    def copy(self) -> 'ExprComposite':
        """
        Returns a copy of the expression.
        """
        return ExprComposite([token.copy() for token in self.tokens])

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        for token in self.tokens:
            token.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'ExprComposite':
        """
        Binds the parameters of a copy of the expression to the given list of parameters.
        """
        return ExprComposite([token.bind_parameters(parameters) for token in self.tokens])