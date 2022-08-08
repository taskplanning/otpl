# Generated from pddl22.g4 by ANTLR 4.10.1
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


    # Visit a parse tree produced by pddl22Parser#untyped_type_list.
    def visitUntyped_type_list(self, ctx:pddl22Parser.Untyped_type_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#typed_type_list.
    def visitTyped_type_list(self, ctx:pddl22Parser.Typed_type_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#pddl_type.
    def visitPddl_type(self, ctx:pddl22Parser.Pddl_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#constants_def.
    def visitConstants_def(self, ctx:pddl22Parser.Constants_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#untyped_name_list.
    def visitUntyped_name_list(self, ctx:pddl22Parser.Untyped_name_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#typed_name_list.
    def visitTyped_name_list(self, ctx:pddl22Parser.Typed_name_listContext):
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


    # Visit a parse tree produced by pddl22Parser#goal_descriptor_empty.
    def visitGoal_descriptor_empty(self, ctx:pddl22Parser.Goal_descriptor_emptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#goal_descriptor_simple.
    def visitGoal_descriptor_simple(self, ctx:pddl22Parser.Goal_descriptor_simpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#goal_descriptor_conjunction.
    def visitGoal_descriptor_conjunction(self, ctx:pddl22Parser.Goal_descriptor_conjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#goal_descriptor_disjunction.
    def visitGoal_descriptor_disjunction(self, ctx:pddl22Parser.Goal_descriptor_disjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#goal_descriptor_negative.
    def visitGoal_descriptor_negative(self, ctx:pddl22Parser.Goal_descriptor_negativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#goal_descriptor_implication.
    def visitGoal_descriptor_implication(self, ctx:pddl22Parser.Goal_descriptor_implicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#goal_descriptor_existential.
    def visitGoal_descriptor_existential(self, ctx:pddl22Parser.Goal_descriptor_existentialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#goal_descriptor_universal.
    def visitGoal_descriptor_universal(self, ctx:pddl22Parser.Goal_descriptor_universalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#goal_descriptor_comparison.
    def visitGoal_descriptor_comparison(self, ctx:pddl22Parser.Goal_descriptor_comparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#atomic_formula.
    def visitAtomic_formula(self, ctx:pddl22Parser.Atomic_formulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#term_list.
    def visitTerm_list(self, ctx:pddl22Parser.Term_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#term_var.
    def visitTerm_var(self, ctx:pddl22Parser.Term_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#term_name.
    def visitTerm_name(self, ctx:pddl22Parser.Term_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#function_comparison.
    def visitFunction_comparison(self, ctx:pddl22Parser.Function_comparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#binary_comparison.
    def visitBinary_comparison(self, ctx:pddl22Parser.Binary_comparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression_number.
    def visitExpression_number(self, ctx:pddl22Parser.Expression_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression_binary_op.
    def visitExpression_binary_op(self, ctx:pddl22Parser.Expression_binary_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression_uminus.
    def visitExpression_uminus(self, ctx:pddl22Parser.Expression_uminusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression_function.
    def visitExpression_function(self, ctx:pddl22Parser.Expression_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#binary_operator.
    def visitBinary_operator(self, ctx:pddl22Parser.Binary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#effect_empty.
    def visitEffect_empty(self, ctx:pddl22Parser.Effect_emptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#effect_conjunction.
    def visitEffect_conjunction(self, ctx:pddl22Parser.Effect_conjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#effect_c_effect.
    def visitEffect_c_effect(self, ctx:pddl22Parser.Effect_c_effectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#c_effect_forall.
    def visitC_effect_forall(self, ctx:pddl22Parser.C_effect_forallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#c_effect_conditional.
    def visitC_effect_conditional(self, ctx:pddl22Parser.C_effect_conditionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#c_effect_primitive.
    def visitC_effect_primitive(self, ctx:pddl22Parser.C_effect_primitiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#conditional_effect_conjunction.
    def visitConditional_effect_conjunction(self, ctx:pddl22Parser.Conditional_effect_conjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#conditional_effect_primitive.
    def visitConditional_effect_primitive(self, ctx:pddl22Parser.Conditional_effect_primitiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#p_effect_assign.
    def visitP_effect_assign(self, ctx:pddl22Parser.P_effect_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#p_effect_negative.
    def visitP_effect_negative(self, ctx:pddl22Parser.P_effect_negativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#p_effect_simple.
    def visitP_effect_simple(self, ctx:pddl22Parser.P_effect_simpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#assign_operator.
    def visitAssign_operator(self, ctx:pddl22Parser.Assign_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#time_specifier.
    def visitTime_specifier(self, ctx:pddl22Parser.Time_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_def.
    def visitDurative_action_def(self, ctx:pddl22Parser.Durative_action_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#duration_constraint_empty.
    def visitDuration_constraint_empty(self, ctx:pddl22Parser.Duration_constraint_emptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#duration_constraint_conjunction.
    def visitDuration_constraint_conjunction(self, ctx:pddl22Parser.Duration_constraint_conjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#duration_constraint_simple.
    def visitDuration_constraint_simple(self, ctx:pddl22Parser.Duration_constraint_simpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#simple_duration_constraint_simple.
    def visitSimple_duration_constraint_simple(self, ctx:pddl22Parser.Simple_duration_constraint_simpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#simple_duration_constraint_timed.
    def visitSimple_duration_constraint_timed(self, ctx:pddl22Parser.Simple_duration_constraint_timedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#duration_op.
    def visitDuration_op(self, ctx:pddl22Parser.Duration_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_goal_descriptor_empty.
    def visitDurative_action_goal_descriptor_empty(self, ctx:pddl22Parser.Durative_action_goal_descriptor_emptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_goal_descriptor_conjunction.
    def visitDurative_action_goal_descriptor_conjunction(self, ctx:pddl22Parser.Durative_action_goal_descriptor_conjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_goal_descriptor_timed.
    def visitDurative_action_goal_descriptor_timed(self, ctx:pddl22Parser.Durative_action_goal_descriptor_timedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#timed_goal_descriptor.
    def visitTimed_goal_descriptor(self, ctx:pddl22Parser.Timed_goal_descriptorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_effect_empty.
    def visitDurative_action_effect_empty(self, ctx:pddl22Parser.Durative_action_effect_emptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_effect_conjunction.
    def visitDurative_action_effect_conjunction(self, ctx:pddl22Parser.Durative_action_effect_conjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_effect_timed.
    def visitDurative_action_effect_timed(self, ctx:pddl22Parser.Durative_action_effect_timedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_effect_forall.
    def visitDurative_action_effect_forall(self, ctx:pddl22Parser.Durative_action_effect_forallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#durative_action_effect_conditional.
    def visitDurative_action_effect_conditional(self, ctx:pddl22Parser.Durative_action_effect_conditionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#timed_effect_timed.
    def visitTimed_effect_timed(self, ctx:pddl22Parser.Timed_effect_timedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#timed_effect_assign.
    def visitTimed_effect_assign(self, ctx:pddl22Parser.Timed_effect_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#timed_effect_continuous.
    def visitTimed_effect_continuous(self, ctx:pddl22Parser.Timed_effect_continuousContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#function_assign_durative.
    def visitFunction_assign_durative(self, ctx:pddl22Parser.Function_assign_durativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression_durative_operator.
    def visitExpression_durative_operator(self, ctx:pddl22Parser.Expression_durative_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression_durative_uminus.
    def visitExpression_durative_uminus(self, ctx:pddl22Parser.Expression_durative_uminusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression_durative_duration.
    def visitExpression_durative_duration(self, ctx:pddl22Parser.Expression_durative_durationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#expression_durative_expression.
    def visitExpression_durative_expression(self, ctx:pddl22Parser.Expression_durative_expressionContext):
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


    # Visit a parse tree produced by pddl22Parser#init_element_simple.
    def visitInit_element_simple(self, ctx:pddl22Parser.Init_element_simpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#init_element_assign.
    def visitInit_element_assign(self, ctx:pddl22Parser.Init_element_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#init_element_til.
    def visitInit_element_til(self, ctx:pddl22Parser.Init_element_tilContext):
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


    # Visit a parse tree produced by pddl22Parser#ground_function_expression_number.
    def visitGround_function_expression_number(self, ctx:pddl22Parser.Ground_function_expression_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#ground_function_expression_binary.
    def visitGround_function_expression_binary(self, ctx:pddl22Parser.Ground_function_expression_binaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#ground_function_expression_uminus.
    def visitGround_function_expression_uminus(self, ctx:pddl22Parser.Ground_function_expression_uminusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#ground_function_expression_function.
    def visitGround_function_expression_function(self, ctx:pddl22Parser.Ground_function_expression_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#ground_function_expression_total_time.
    def visitGround_function_expression_total_time(self, ctx:pddl22Parser.Ground_function_expression_total_timeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#ground_function_expression_parenthesis.
    def visitGround_function_expression_parenthesis(self, ctx:pddl22Parser.Ground_function_expression_parenthesisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#variable.
    def visitVariable(self, ctx:pddl22Parser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#name.
    def visitName(self, ctx:pddl22Parser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pddl22Parser#number.
    def visitNumber(self, ctx:pddl22Parser.NumberContext):
        return self.visitChildren(ctx)



del pddl22Parser