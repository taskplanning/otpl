# Generated from pddl22.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pddl22Parser import pddl22Parser
else:
    from pddl22Parser import pddl22Parser

# This class defines a complete generic visitor for a parse tree produced by pddl22Parser.

class pddl22Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by pddl22Parser#pddl_file.
    def visitPddl_file(self, ctx:pddl22Parser.Pddl_fileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#domain.
    def visitDomain(self, ctx:pddl22Parser.DomainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#require_def.
    def visitRequire_def(self, ctx:pddl22Parser.Require_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#require_key.
    def visitRequire_key(self, ctx:pddl22Parser.Require_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#types_def.
    def visitTypes_def(self, ctx:pddl22Parser.Types_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#untyped_list.
    def visitUntyped_list(self, ctx:pddl22Parser.Untyped_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#typed_list.
    def visitTyped_list(self, ctx:pddl22Parser.Typed_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#pddl_type.
    def visitPddl_type(self, ctx:pddl22Parser.Pddl_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#constants_def.
    def visitConstants_def(self, ctx:pddl22Parser.Constants_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#predicates_def.
    def visitPredicates_def(self, ctx:pddl22Parser.Predicates_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#atomic_formula_skeleton.
    def visitAtomic_formula_skeleton(self, ctx:pddl22Parser.Atomic_formula_skeletonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#untyped_var_list.
    def visitUntyped_var_list(self, ctx:pddl22Parser.Untyped_var_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#typed_var_list.
    def visitTyped_var_list(self, ctx:pddl22Parser.Typed_var_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#functions_def.
    def visitFunctions_def(self, ctx:pddl22Parser.Functions_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#action_def.
    def visitAction_def(self, ctx:pddl22Parser.Action_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#goal_descriptor.
    def visitGoal_descriptor(self, ctx:pddl22Parser.Goal_descriptorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#atomic_formula.
    def visitAtomic_formula(self, ctx:pddl22Parser.Atomic_formulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#term.
    def visitTerm(self, ctx:pddl22Parser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#function_comparison.
    def visitFunction_comparison(self, ctx:pddl22Parser.Function_comparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#binary_comparison.
    def visitBinary_comparison(self, ctx:pddl22Parser.Binary_comparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression.
    def visitExpression(self, ctx:pddl22Parser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#binary_operator.
    def visitBinary_operator(self, ctx:pddl22Parser.Binary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#effect.
    def visitEffect(self, ctx:pddl22Parser.EffectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#c_effect.
    def visitC_effect(self, ctx:pddl22Parser.C_effectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#conditional_effect.
    def visitConditional_effect(self, ctx:pddl22Parser.Conditional_effectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#p_effect.
    def visitP_effect(self, ctx:pddl22Parser.P_effectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#assign_operator.
    def visitAssign_operator(self, ctx:pddl22Parser.Assign_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_def.
    def visitDurative_action_def(self, ctx:pddl22Parser.Durative_action_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#duration_constraint.
    def visitDuration_constraint(self, ctx:pddl22Parser.Duration_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#simple_duration_constraint.
    def visitSimple_duration_constraint(self, ctx:pddl22Parser.Simple_duration_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#duration_op.
    def visitDuration_op(self, ctx:pddl22Parser.Duration_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_goal_descriptor.
    def visitDurative_action_goal_descriptor(self, ctx:pddl22Parser.Durative_action_goal_descriptorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#timed_goal_descriptor.
    def visitTimed_goal_descriptor(self, ctx:pddl22Parser.Timed_goal_descriptorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#time_specifier_prefix.
    def visitTime_specifier_prefix(self, ctx:pddl22Parser.Time_specifier_prefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#time_specifier.
    def visitTime_specifier(self, ctx:pddl22Parser.Time_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_effect.
    def visitDurative_action_effect(self, ctx:pddl22Parser.Durative_action_effectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#timed_effect.
    def visitTimed_effect(self, ctx:pddl22Parser.Timed_effectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#function_assign_durative.
    def visitFunction_assign_durative(self, ctx:pddl22Parser.Function_assign_durativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression_durative.
    def visitExpression_durative(self, ctx:pddl22Parser.Expression_durativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#assign_op_t.
    def visitAssign_op_t(self, ctx:pddl22Parser.Assign_op_tContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression_t.
    def visitExpression_t(self, ctx:pddl22Parser.Expression_tContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#derived_predicate_def.
    def visitDerived_predicate_def(self, ctx:pddl22Parser.Derived_predicate_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#problem.
    def visitProblem(self, ctx:pddl22Parser.ProblemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#object_declaration.
    def visitObject_declaration(self, ctx:pddl22Parser.Object_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#init.
    def visitInit(self, ctx:pddl22Parser.InitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#init_element.
    def visitInit_element(self, ctx:pddl22Parser.Init_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#goal.
    def visitGoal(self, ctx:pddl22Parser.GoalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#metric_spec.
    def visitMetric_spec(self, ctx:pddl22Parser.Metric_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#optimization.
    def visitOptimization(self, ctx:pddl22Parser.OptimizationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#ground_function_expression.
    def visitGround_function_expression(self, ctx:pddl22Parser.Ground_function_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#variable.
    def visitVariable(self, ctx:pddl22Parser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#name.
    def visitName(self, ctx:pddl22Parser.NameContext):
        return self.visitChildren(ctx)



del pddl22Parser