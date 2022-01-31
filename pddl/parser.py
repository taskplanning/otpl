from enum import Enum
import sys
from typing import Type
from antlr4 import CommonTokenStream, FileStream
from pddl import domain_condition
from pddl.domain_assignment import AssignmentType, DomainAssignment
from pddl.domain_effect import Effect, EffectConditional, EffectConjunction, EffectForall, EffectNegative, EffectSimple, TimedEffect
from pddl.domain_expression import ExprBase, ExprComposite
from pddl.domain_time_spec import TIME_SPEC
from pddl.grammar.pddl22Lexer import pddl22Lexer
from pddl.grammar.pddl22Parser import pddl22Parser
from pddl.grammar.pddl22Visitor import pddl22Visitor
from pddl.domain import Domain
from pddl.domain_type import DomainType
from pddl.domain_formula import DomainFormula, TypedParameter
from pddl.domain_inequality import DomainInequality
from pddl.domain_operator import DomainOperator
from pddl.domain_duration import DomainDuration, DomainDurationConjunction, DomainDurationInequality, DomainDurationTimed
from pddl.domain_condition import GoalConjunction, GoalDescriptor, GoalDisjunction, GoalImplication, GoalNegative, GoalQuantified, GoalSimple, GoalType, TimedGoal
from pddl.metric import Metric, MetricSpec
from pddl.problem import Problem
from pddl.timed_initial_literal import TimedInitialLiteral

class Parser(pddl22Visitor):
    """
    A class that visits the PDDL2.2 parse tree and constructs python objects to store domain and problem instances.
    """

    def __init__(self) -> None:
        self.domain = None
        self.problem = None
        self.inequality = None
        self.expression = None

        self.parsing_state = "none"

    #==================#
    # typed parameters #
    #==================#
    
    def visitTyped_var_list(self, ctx:pddl22Parser.Typed_var_listContext):
        typed_parameters = []
        parent_type = ctx.pddl_type().getText()
        for param in ctx.variable():
            typed_parameters.append(TypedParameter(parent_type, param.getText()))
        return typed_parameters

    def visitUntyped_var_list(self, ctx:pddl22Parser.Untyped_var_listContext):
        typed_parameters = []
        for param in ctx.variable():
            typed_parameters.append(TypedParameter("object", param.getText()))
        return typed_parameters

    #==============#
    # object lists #
    #==============#

    def visitTyped_name_list(self, ctx:pddl22Parser.Typed_name_listContext):
        # TODO assert that either types are not used here
        objects = []
        parent_type = ctx.pddl_type().getText()
        for param in ctx.name():
            objects.append((param.getText(), parent_type))
        return objects

    def visitUntyped_name_list(self, ctx:pddl22Parser.Untyped_name_listContext):
        objects = []
        for param in ctx.name():
            objects.append((param.getText(), "object"))
        return objects

    #=======#
    # types #
    #=======#

    def visitTyped_type_list(self, ctx:pddl22Parser.Typed_type_listContext):
        # TODO assert that either types are not used here
        parent_type = ctx.pddl_type().getText()
        for param in ctx.name():
            self.domain.types.append(DomainType(param.getText(), parent_type))

    def visitUntyped_type_list(self, ctx:pddl22Parser.Untyped_type_listContext):
        for param in ctx.name():
            self.domain.types.append(DomainType(param.getText(), "object"))

    #============#
    # term lists #
    #============#
    
    def visitTerm_list(self, ctx: pddl22Parser.Term_listContext):
        terms = []
        for term in ctx.term(): terms.append(self.visit(term))
        return terms

    def visitTerm_var(self, ctx: pddl22Parser.Term_varContext):
        return TypedParameter(type="TODO term types", label=ctx.getText())

    def visitTerm_name(self, ctx: pddl22Parser.Term_nameContext):
        return TypedParameter(type="TODO term types", label="TODO term name", value=ctx.getText())

    #================#
    # atomic formula #
    #================#

    # parse atomic formula skeleton (ungrounded) into DomainFormula
    def visitAtomic_formula_skeleton(self, ctx:pddl22Parser.Atomic_formula_skeletonContext):
        formula = DomainFormula(ctx.name().getText(), typed_parameters=[])
        # typed parameters
        for param_list in ctx.typed_var_list(): formula.typed_parameters.extend(self.visit(param_list))
        # primitive parameters
        if ctx.untyped_var_list(): formula.typed_parameters.extend(self.visit(ctx.untyped_var_list()))
        return formula

    # parse atomic formula (of terms) into DomainFormula
    def visitAtomic_formula(self, ctx:pddl22Parser.Atomic_formulaContext):
        # TODO need a name and variable lookup table to get types
        return DomainFormula(ctx.name().getText(), typed_parameters=self.visit(ctx.term_list()))

    #=============#
    # expressions #
    #=============#

    def visitExpression_number(self, ctx: pddl22Parser.Expression_numberContext):
        number = ExprBase(expr_type=ExprBase.ExprType.CONSTANT, constant=float(ctx.number().getText()))
        return ExprComposite([number])

    def visitExpression_binary_op(self, ctx: pddl22Parser.Expression_binary_opContext):
        binary_op = ExprBase(expr_type=ExprBase.ExprType.BINARY_OPERATOR)
        binary_op.op = ExprBase.BinaryOperator(ctx.binary_operator().getText())
        lhs = self.visit(ctx.expression()[0])
        rhs = self.visit(ctx.expression()[1])
        return ExprComposite([binary_op] + lhs.tokens + rhs.tokens)

    def visitExpression_uminus(self, ctx: pddl22Parser.Expression_uminusContext):
        uminus = ExprBase(expr_type=ExprBase.ExprType.UMINUS)
        return ExprComposite([uminus] + self.visit(ctx.expression()))

    def visitExpression_function(self, ctx: pddl22Parser.Expression_functionContext):
        expr = ExprBase(expr_type=ExprBase.ExprType.FUNCTION)
        expr.function = self.visit(ctx.atomic_formula())
        return ExprComposite([expr])

    def visitExpression_durative_operator(self, ctx: pddl22Parser.Expression_durative_operatorContext):
        binary_op = ExprBase(expr_type=ExprBase.ExprType.BINARY_OPERATOR)
        binary_op.op = ExprBase.BinaryOperator(ctx.binary_operator().getText())
        lhs = self.visit(ctx.expression_durative()[0])
        rhs = self.visit(ctx.expression_durative()[1])
        return ExprComposite([binary_op] + lhs.tokens + rhs.tokens)

    def visitExpression_durative_uminus(self, ctx: pddl22Parser.Expression_durative_uminusContext):
        uminus = ExprBase(expr_type=ExprBase.ExprType.UMINUS)
        return ExprComposite([uminus] + self.visit(ctx.expression_durative()))

    def visitExpression_durative_duration(self, ctx: pddl22Parser.Expression_durative_durationContext):
        return ExprComposite([ExprBase(
                    expr_type=ExprBase.ExprType.SPECIAL,
                    special_type=ExprBase.SpecialType.DURATION)])

    def visitExpression_t(self, ctx: pddl22Parser.Expression_tContext):
        hasht = ExprBase(expr_type=ExprBase.ExprType.SPECIAL, special_type=ExprBase.SpecialType.HASHT)
        if ctx.expression():
            binary_op = ExprBase(expr_type=ExprBase.ExprType.BINARY_OPERATOR, op=ExprBase.BinaryOperator.MUL)
            expr = self.visit(ctx.expression())
            return ExprComposite([binary_op,hasht]+expr.tokens)
        else:
            return ExprComposite([hasht])

    #=============#
    # comparisons #
    #=============#

    def visitFunction_comparison(self, ctx:pddl22Parser.Function_comparisonContext):
        ineq = DomainInequality(
            DomainInequality.COMPARISON_TYPE(ctx.binary_comparison.getText()),
            self.visit(ctx.expression[0]),
            self.visit(ctx.expression[1])
        )
        return ineq

    def visitDuration_constraint_empty(self, ctx: pddl22Parser.Duration_constraint_emptyContext):
        return DomainDuration()

    def visitDuration_constraint_conjunction(self, ctx: pddl22Parser.Duration_constraint_conjunctionContext):
        constraints = []
        for c in ctx.simple_duration_constraint():
            constraints.append(self.visit(c))
        return DomainDurationConjunction(constraints)

    def visitSimple_duration_constraint_simple(self, ctx: pddl22Parser.Simple_duration_constraint_simpleContext):
        comparison_type=DomainInequality.COMPARISON_TYPE(ctx.duration_op().getText())
        lhs = self.visit(ctx.expression())
        rhs = self.visit(ctx.expression())
        return DomainDurationInequality(DomainInequality(comparison_type, lhs, rhs))

    def visitSimple_duration_constraint_timed(self, ctx: pddl22Parser.Simple_duration_constraint_timedContext):
        if ctx.time_specifier().getText() == "start":
            time_spec = TIME_SPEC.AT_START
        elif ctx.time_specifier().getText() == "end":
            time_spec = TIME_SPEC.AT_END
        inequality=self.visit(ctx.simple_duration_constraint())
        assert(inequality.duration_type == DomainDuration.DurationType.INEQUALITY)
        DomainDurationTimed(time_spec, inequality)

    #===============#
    # parsing goals #
    #===============#

    def visitGoal_descriptor_empty(self, ctx: pddl22Parser.Goal_descriptor_emptyContext):
        return GoalDescriptor()

    def visitGoal_descriptor_simple(self, ctx: pddl22Parser.Goal_descriptor_simpleContext):
        return GoalSimple(self.visit(ctx.atomic_formula()))

    def visitGoal_descriptor_conjunction(self, ctx: pddl22Parser.Goal_descriptor_conjunctionContext):
        goals = []
        for goal in ctx.goal_descriptor():
            goals.append(self.visit(goal))
        return GoalConjunction(goals)

    def visitGoal_descriptor_disjunction(self, ctx: pddl22Parser.Goal_descriptor_disjunctionContext):
        goals = []
        for goal in ctx.goal_descriptor():
            goals.append(self.visit(goal))
        return GoalDisjunction(goals)

    def visitGoal_descriptor_negative(self, ctx: pddl22Parser.Goal_descriptor_negativeContext):
        return GoalNegative(self.visit(ctx.goal_descriptor()))

    def visitGoal_descriptor_implication(self, ctx: pddl22Parser.Goal_descriptor_implicationContext):
        children = ctx.goal_descriptor()
        return GoalImplication(antecedent=self.visit(children[0]),consequent=self.visit(children[1]))

    def visitGoal_descriptor_existential(self, ctx: pddl22Parser.Goal_descriptor_existentialContext):
        goal = GoalQuantified(typed_parameters=[],
                goal=self.visit(ctx.goal_descriptor()),
                quantification=GoalType.EXISTENTIAL)
        # typed parameters
        for param_list in ctx.typed_var_list(): goal.typed_parameters.extend(self.visit(param_list))
        # primitive parameters
        if ctx.untyped_var_list(): goal.typed_parameters.extend(self.visit(ctx.untyped_var_list()))
        return goal

    def visitGoal_descriptor_universal(self, ctx: pddl22Parser.Goal_descriptor_universalContext):
        goal = GoalQuantified(typed_parameters=[],
                goal=self.visit(ctx.goal_descriptor()),
                quantification=GoalType.UNIVERSAL)
        # typed parameters
        for param_list in ctx.typed_var_list(): goal.typed_parameters.extend(self.visit(param_list))
        # primitive parameters
        if ctx.untyped_var_list(): goal.typed_parameters.extend(self.visit(ctx.untyped_var_list()))
        return goal

    def visitGoal_descriptor_comparison(self, ctx: pddl22Parser.Goal_descriptor_comparisonContext):
        return self.visit(ctx.function_comparison)

    #=====================#
    # parsing timed goals #
    #=====================#

    def visitDurative_action_goal_descriptor_empty(self, ctx: pddl22Parser.Durative_action_goal_descriptor_emptyContext):
        return GoalDescriptor()

    def visitDurative_action_goal_descriptor_conjunction(self, ctx: pddl22Parser.Durative_action_goal_descriptor_conjunctionContext):
        goals = []
        for goal in ctx.timed_goal_descriptor():
            goals.append(self.visit(goal))
        return GoalConjunction(goals)

    def visitTimed_goal_descriptor(self, ctx: pddl22Parser.Timed_goal_descriptorContext):
        if ctx.time_specifier().getText() == "start":
            assert(ctx.time_specifier_prefix().getText() == "(at")
            time_spec = TIME_SPEC.AT_START
        elif ctx.time_specifier().getText() == "end":
            assert(ctx.time_specifier_prefix().getText() == "(at")
            time_spec = TIME_SPEC.AT_END
        elif ctx.time_specifier().getText() == "all":
            assert(ctx.time_specifier_prefix().getText() == "(over")
            time_spec = TIME_SPEC.OVER_ALL
        return TimedGoal(time_spec=time_spec, goal=self.visit(ctx.goal_descriptor()))
        
    #=================#
    # parsing effects #
    #=================#

    def visitEffect_empty(self, ctx: pddl22Parser.Effect_emptyContext):
        return Effect()

    def visitEffect_conjunction(self, ctx: pddl22Parser.Effect_conjunctionContext):
        effects = []
        for effect in ctx.c_effect():
            effects.append(self.visit(effect))
        return EffectConjunction(effects)

    def visitC_effect_forall(self, ctx: pddl22Parser.C_effect_forallContext):
        effect = EffectForall(typed_parameters=[], effect=self.visit(ctx.effect()))
        # typed parameters
        for param_list in ctx.typed_var_list():
            effect.typed_parameters.extend(self.visit(param_list))
        # primitive parameters
        if ctx.untyped_var_list():
            effect.typed_parameters.extend(self.visit(ctx.untyped_var_list()))
        return effect
    
    def visitC_effect_conditional(self, ctx: pddl22Parser.C_effect_conditionalContext):
        return EffectConditional(
            self.visit(ctx.goal_descriptor()),
            self.visit(ctx.conditional_effect()))

    def visitConditional_effect_conjunction(self, ctx: pddl22Parser.Conditional_effect_conjunctionContext):
        effects = []
        for effect in ctx.p_effect():
            effects.append(self.visit(effect))
        return EffectConjunction(effects)

    def visitP_effect_assign(self, ctx: pddl22Parser.P_effect_assignContext):
        assign_op = AssignmentType(ctx.assign_operator().getText())
        formula = self.visit(ctx.atomic_formula())
        expression = self.visit(ctx.expression())
        return DomainAssignment(assign_op, lhs=formula, rhs=expression)

    def visitP_effect_negative(self, ctx: pddl22Parser.P_effect_negativeContext):
        return EffectNegative(self.visit(ctx.atomic_formula()))

    def visitP_effect_simple(self, ctx: pddl22Parser.P_effect_simpleContext):
        return EffectSimple(self.visit(ctx.atomic_formula()))

    #=======================#
    # parsing timed effects #
    #=======================#

    def visitDurative_action_effect_empty(self, ctx: pddl22Parser.Durative_action_effect_emptyContext):
        return Effect()

    def visitDurative_action_effect_conjunction(self, ctx: pddl22Parser.Durative_action_effect_conjunctionContext):
        effects = []
        for effect in ctx.durative_action_effect():
            effects.append(self.visit(effect))
        return EffectConjunction(effects)

    def visitDurative_action_effect_forall(self, ctx: pddl22Parser.Durative_action_effect_forallContext):
        effect = EffectForall(typed_parameters=[], effect=self.visit(ctx.durative_action_effect()))
        # typed parameters
        for param_list in ctx.typed_var_list():
            effect.typed_parameters.extend(self.visit(param_list))
        # primitive parameters
        if ctx.untyped_var_list():
            effect.typed_parameters.extend(self.visit(ctx.untyped_var_list()))
        return effect

    def visitDurative_action_effect_conditional(self, ctx: pddl22Parser.Durative_action_effect_conditionalContext):
        return EffectConditional(
            self.visit(ctx.durative_action_goal_descriptor()),
            self.visit(ctx.timed_effect()))

    def visitTimed_effect_timed(self, ctx: pddl22Parser.Timed_effect_timedContext):
        if ctx.time_specifier().getText() == "start":
            time_spec = TIME_SPEC.AT_START
        elif ctx.time_specifier().getText() == "end":
            time_spec = TIME_SPEC.AT_END
        return TimedEffect(time_spec, self.visit(ctx.c_effect()))

    def visitTimed_effect_assign(self, ctx: pddl22Parser.Timed_effect_assignContext):
        if ctx.time_specifier().getText() == "start":
            time_spec = TIME_SPEC.AT_START
        elif ctx.time_specifier().getText() == "end":
            time_spec = TIME_SPEC.AT_END
        return TimedEffect(time_spec, self.visit(ctx.c_effect()))

    def visitFunction_assign_durative(self, ctx: pddl22Parser.Function_assign_durativeContext):
        assign_op = AssignmentType(ctx.assign_operator().getText())        
        formula = self.visit(ctx.atomic_formula())
        expression = self.visit(ctx.expression_durative())
        return DomainAssignment(assign_op, lhs=formula, rhs=expression)

    def visitTimed_effect_continuous(self, ctx: pddl22Parser.Timed_effect_continuousContext):
        if ctx.assign_op_t().getText() == "increase":
            assign_op = AssignmentType.INCREASE_CTS
        elif ctx.assign_op_t().getText() == "increase":
            assign_op = AssignmentType.DECREASE_CTS
        formula = self.visit(ctx.atomic_formula())
        expression = self.visit(ctx.expression_t())
        return DomainAssignment(assign_op, lhs=formula, rhs=expression)

    #=================#
    # parsing actions #
    #=================#

    def visitAction_def(self, ctx:pddl22Parser.Action_defContext):

        op_formula = DomainFormula(ctx.name().getText())
        for param_list in ctx.typed_var_list():
            op_formula.typed_parameters.extend(self.visit(param_list))

        if ctx.goal_descriptor(): condition = self.visit(ctx.goal_descriptor())
        else: condition = GoalDescriptor()

        if ctx.effect(): effect = self.visit(ctx.effect())
        else: effect = Effect()

        self.operator = DomainOperator(op_formula,
            durative=False,
            condition=condition,
            effect=effect)

        self.domain.operators.append(self.operator)

    def visitDurative_action_def(self, ctx:pddl22Parser.Durative_action_defContext):

        op_formula = DomainFormula(ctx.name().getText())
        for param_list in ctx.typed_var_list():
            op_formula.typed_parameters.extend(self.visit(param_list))

        if ctx.durative_action_goal_descriptor():
            condition = self.visit(ctx.durative_action_goal_descriptor())
        else: condition = GoalDescriptor()

        if ctx.durative_action_effect():
            effect = self.visit(ctx.durative_action_effect())
        else: effect = Effect()

        self.operator = DomainOperator(op_formula,
            durative=True,
            duration=self.visit(ctx.duration_constraint()),
            condition=condition,
            effect=effect)
        self.domain.operators.append(self.operator)

    #================#
    # parsing domain #
    #================#

    def visitDomain(self, ctx:pddl22Parser.DomainContext):
        self.parsing_state = "domain"
        self.domain = Domain(ctx.name().getText())
        self.visitChildren(ctx)
        self.parsing_state = "none"

    def visitRequire_key(self, ctx:pddl22Parser.Require_keyContext):
        if self.parsing_state=="domain":
            self.domain.requirements.append(ctx.getText())
        elif self.parsing_state=="problem":
            self.problem.requirements.append(ctx.getText())

    def visitConstants_def(self, ctx:pddl22Parser.Constants_defContext):
        objects = []
        # typed objects
        for name in ctx.typed_name_list():
            for obj in self.visit(name):
                self.domain.constants_type_map[obj[0]] = obj[1]
                self.domain.type_constants_map[obj[1]] = obj[0]
        # primitive objects
        if ctx.untyped_name_list():
            for obj in self.visit(ctx.untyped_name_list()):
                self.domain.constants_type_map[obj[0]] = obj[1]
                self.domain.type_constants_map[obj[1]] = obj[0]

    def visitPredicates_def(self, ctx:pddl22Parser.Predicates_defContext):
        for formula in ctx.atomic_formula_skeleton():
            pred = self.visit(formula)
            self.domain.predicates.append(pred)

    def visitFunctions_def(self, ctx:pddl22Parser.Functions_defContext):
        for formula in ctx.atomic_formula_skeleton():
            func = self.visit(formula)
            self.domain.functions.append(func)

    #=================#
    # parsing problem #
    #=================#

    def visitProblem(self, ctx:pddl22Parser.DomainContext):
        self.parsing_state = "problem"
        self.problem = Problem(
            problem_name=ctx.name()[0].getText(),
            domain_name=ctx.name()[1].getText())
        self.visitChildren(ctx)
        self.parsing_state = "none"

    def visitObject_declaration(self, ctx: pddl22Parser.Object_declarationContext):
        objects = []
        # typed objects
        for name in ctx.typed_name_list():
            for obj in self.visit(name):
                self.problem.objects_type_map[obj[0]] = obj[1]
                self.problem.type_objects_map[obj[1]] = obj[0]
        # primitive objects
        if ctx.untyped_name_list():
            for obj in self.visit(ctx.untyped_name_list()):
                self.problem.objects_type_map[obj[0]] = obj[1]
                self.problem.type_objects_map[obj[1]] = obj[0]        

    def visitInit_element_simple(self, ctx: pddl22Parser.Init_element_simpleContext):
        self.problem.propositions.append(self.visit(ctx.atomic_formula()))

    def visitInit_element_assign(self, ctx: pddl22Parser.Init_element_assignContext):
        function = self.visit(ctx.atomic_formula())
        function.value = float(ctx.number().getText())
        self.problem.functions.append(function)

    def visitInit_element_til(self, ctx: pddl22Parser.Init_element_tilContext):
        til = TimedInitialLiteral(float(ctx.number().getText()),self.visit(ctx.p_effect()))
        self.problem.timed_initial_literals.append(til)

    def visitGoal(self, ctx: pddl22Parser.GoalContext):
        self.problem.goal = self.visit(ctx.goal_descriptor())

    def visitMetric_spec(self, ctx: pddl22Parser.Metric_specContext):
        metric_spec = MetricSpec(ctx.optimization().getText())
        metric = Metric(metric_spec, self.visit(ctx.ground_function_expression()))
        self.problem.metric = metric

    #==================#
    # ground functions #
    #==================#

    def visitGround_function_expression_number(self, ctx: pddl22Parser.Ground_function_expression_numberContext):
        number = ExprBase(expr_type=ExprBase.ExprType.CONSTANT, constant=float(ctx.number().getText()))
        return ExprComposite([number])

    def visitGround_function_expression_binary(self, ctx: pddl22Parser.Ground_function_expression_binaryContext):
        binary_op = ExprBase(expr_type=ExprBase.ExprType.BINARY_OPERATOR)
        binary_op.op = ExprBase.BinaryOperator(ctx.binary_operator().getText())
        lhs = self.visit(ctx.ground_function_expression()[0])
        rhs = self.visit(ctx.ground_function_expression()[1])
        return ExprComposite([binary_op] + lhs.tokens + rhs.tokens)

    def visitGround_function_expression_uminus(self, ctx: pddl22Parser.Ground_function_expression_uminusContext):
        uminus = ExprBase(expr_type=ExprBase.ExprType.UMINUS)
        return ExprComposite([uminus] + self.visit(ctx.ground_function_expression()))

    def visitGround_function_expression_function(self, ctx: pddl22Parser.Ground_function_expression_functionContext):
        expr = ExprBase(expr_type=ExprBase.ExprType.FUNCTION)
        name = ctx.name()[0].getText()
        params = []
        for param in ctx.name()[1:]:
            params.append(TypedParameter("TODO parse tables", "TODO parse tables", param.getText()))
        expr.function = DomainFormula(name, params)
        return ExprComposite([expr])

    def visitGround_function_expression_total_time(self, ctx: pddl22Parser.Ground_function_expression_total_timeContext):
        token = ExprBase(expr_type=ExprBase.ExprType.SPECIAL, special_type=ExprBase.SpecialType.TOTAL_TIME)
        return ExprComposite([token])


if __name__ == "__main__":  
    
    # lexer
    data = FileStream(sys.argv[1])
    lexer = pddl22Lexer(data)
    stream = CommonTokenStream(lexer)
    
    # parser
    parser = pddl22Parser(stream)
    tree = parser.pddl_file()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("PDDL Parser encountered syntax errors.")
        sys.exit(-1)

    # visitor
    visitor = Parser()
    visitor.visit(tree)
    print(visitor.problem)