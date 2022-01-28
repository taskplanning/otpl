from ast import Expression
from enum import Enum
import sys
from antlr4 import CommonTokenStream, FileStream
from parsing.pddl22Lexer import pddl22Lexer
from parsing.pddl22Parser import pddl22Parser
from parsing.pddl22Visitor import pddl22Visitor
from pddl.domain import Domain
from pddl.domain_type import DomainType
from pddl.object import Object
from pddl.domain_formula import DomainFormula, TypedParameter
from pddl.domain_inequality import DomainInequality
from pddl.domain_operator import DomainOperator
from pddl.domain_duration import DomainDuration

class Parser(pddl22Visitor):
    """
    A class that visits the PDDL2.2 parse tree and constructs python objects to store domain and problem instances.
    """

    class ParsingState(Enum):
        NONE           = 0
        EXPRESSION     = 1
        COMPARISON     = 2
        DURATION       = 3

    def __init__(self) -> None:
        self.domain = None
        self.problem = None
        self.inequality = None
        self.expression = None

        self.parsing_state = Parser.ParsingState.NONE

    #============#
    # typed list #
    #============#
    
    def visitTyped_var_list(self, ctx:pddl22Parser.Typed_var_listContext):
        typed_parameters = []
        parent_type = ctx.pddl_type().getText()
        for param in ctx.variable():
            typed_parameters.append(TypedParameter(parent_type, param.getText()))
        return typed_parameters

    #================#
    # domain formula #
    #================#

    # parse atomic formula skeleton (ungrounded) into DomainFormula
    def visitAtomic_formula_skeleton(self, ctx:pddl22Parser.Atomic_formula_skeletonContext):

        formula = DomainFormula(ctx.name().getText(), typed_parameters=[])

        # typed parameters
        for param_list in ctx.typed_var_list():
            formula.typed_parameters.extend(self.visit(param_list))

        # primitive parameters
        for param in ctx.untyped_var_list():
            formula.typed_parameters.append(TypedParameter("object", param.getText()))

        return formula

    # parse atomic formula into DomainFormula
    def visitAtomic_formula(self, ctx:pddl22Parser.Atomic_formulaContext):
        return self.visitChildren(ctx)

    #=============#
    # expressions #
    #=============#

    def visitExpression(self, ctx:pddl22Parser.ExpressionContext):
        print(ctx.getText())
        return self.visitChildren(ctx)

    #=============#
    # comparisons #
    #=============#

    def visitDuration_constraint(self, ctx:pddl22Parser.Duration_constraintContext):
        # TODO update domain operator to match actual definition
        # should also include empty duration
        # should also include (and)
        # should also include time specifier
        self.parsing_state = Parser.ParsingState.DURATION
        ineq = self.visitChildren(ctx)
        self.parsing_state = Parser.ParsingState.NONE
        return ineq

    def visitFunction_comparison(self, ctx:pddl22Parser.Function_comparisonContext):
        self.parsing_state = Parser.ParsingState.COMPARISON
        ineq = DomainInequality(
            DomainInequality.COMPARISON_TYPE(ctx.binary_comparison.getText()),
            self.visit(ctx.expression[0]),
            self.visit(ctx.expression[1])
        )
        self.parsing_state = Parser.ParsingState.NONE
        return ineq

    #================#
    # parsing domain #
    #================#

    # TODO simplify parsing by passing 

    def visitDomain(self, ctx:pddl22Parser.DomainContext):
        self.domain = Domain(ctx.name().getText())
        self.visitChildren(ctx)

    def visitRequire_key(self, ctx:pddl22Parser.Require_keyContext):
        self.domain.requirements.append(ctx.getText())

    def visitTypes_def(self, ctx:pddl22Parser.Types_defContext):
        # sub-types
        # TODO (either types)
        for type_list in ctx.typed_list():
            parent_type = type_list.pddl_type().getText()
            for type_name in type_list.name():
                self.domain.types.append(DomainType(type_name.getText(),parent_type))

        # primitive types
        for type_name in ctx.untyped_list():
            self.domain.types.append(DomainType(type_name.getText()))

    def visitConstants_def(self, ctx:pddl22Parser.Constants_defContext):
        # typed objects
        # TODO assert that either types are not used here
        for obj_list in ctx.typed_list():
            parent_type = obj_list.pddl_type().getText()
            for object in obj_list.name():
                self.domain.constants.append(Object(object.getText(),parent_type))

        # primitive objects
        for object in ctx.untyped_list():
            self.domain.constants.append(Object(object.getText()))

    def visitPredicates_def(self, ctx:pddl22Parser.Predicates_defContext):
        for formula in ctx.atomic_formula_skeleton():
            pred = self.visit(formula)
            self.domain.predicates.append(pred)

    def visitFunctions_def(self, ctx:pddl22Parser.Functions_defContext):
        for formula in ctx.atomic_formula_skeleton():
            func = self.visit(formula)
            self.domain.functions.append(func)

    #=================#
    # parsing actions #
    #=================#

    def visitAction_def(self, ctx:pddl22Parser.Action_defContext):
        """
        action_def
        : '(:action' name
        ':parameters (' typed_list* untyped_list* ')' 
        (':precondition' goal_descriptor)?
        (':effect' effect)?
        ')'
        ;
        """
        op_formula = DomainFormula(ctx.name().getText())
        for param_list in ctx.typed_var_list():
            op_formula.typed_parameters.extend(self.visit(param_list))

        self.operator = DomainOperator(op_formula,DomainDuration())
        self.domain.operators.append(self.operator)

    def visitDurative_action_def(self, ctx:pddl22Parser.Durative_action_defContext):
        """
        durative_action_def
          : '(:durative-action' name
          ':parameters (' typed_var_list* untyped_var_list* ')' 
          ':duration' duration_constraint
          ':condition' durative_action_goal_descriptor
          ':effect' durative_action_effect
          ')'
          ;
        """
        op_formula = DomainFormula(ctx.name().getText())
        for param_list in ctx.typed_var_list():
            op_formula.typed_parameters.extend(self.visit(param_list))

        op_duration = DomainDuration()

        self.operator = DomainOperator(op_formula,op_duration)
        self.domain.operators.append(self.operator)

    #=================#
    # parsing problem #
    #=================#

if __name__ == "__main__":               
    # lexer
    data = FileStream(sys.argv[1])
    lexer = pddl22Lexer(data)
    stream = CommonTokenStream(lexer)
    
    # parser
    parser = pddl22Parser(stream)
    tree = parser.pddl_file()

    # evaluator
    visitor = Parser()
    visitor.visit(tree)
    print(visitor.domain)