# Generated from pddl22.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pddl22Parser import pddl22Parser
else:
    from pddl22Parser import pddl22Parser

# This class defines a complete listener for a parse tree produced by pddl22Parser.
class pddl22Listener(ParseTreeListener):

    # Enter a parse tree produced by pddl22Parser#pddl_file.
    def enterPddl_file(self, ctx:pddl22Parser.Pddl_fileContext):
        pass

    # Exit a parse tree produced by pddl22Parser#pddl_file.
    def exitPddl_file(self, ctx:pddl22Parser.Pddl_fileContext):
        pass


    # Enter a parse tree produced by pddl22Parser#domain.
    def enterDomain(self, ctx:pddl22Parser.DomainContext):
        pass

    # Exit a parse tree produced by pddl22Parser#domain.
    def exitDomain(self, ctx:pddl22Parser.DomainContext):
        pass


    # Enter a parse tree produced by pddl22Parser#require_def.
    def enterRequire_def(self, ctx:pddl22Parser.Require_defContext):
        pass

    # Exit a parse tree produced by pddl22Parser#require_def.
    def exitRequire_def(self, ctx:pddl22Parser.Require_defContext):
        pass


    # Enter a parse tree produced by pddl22Parser#require_key.
    def enterRequire_key(self, ctx:pddl22Parser.Require_keyContext):
        pass

    # Exit a parse tree produced by pddl22Parser#require_key.
    def exitRequire_key(self, ctx:pddl22Parser.Require_keyContext):
        pass


    # Enter a parse tree produced by pddl22Parser#types_def.
    def enterTypes_def(self, ctx:pddl22Parser.Types_defContext):
        pass

    # Exit a parse tree produced by pddl22Parser#types_def.
    def exitTypes_def(self, ctx:pddl22Parser.Types_defContext):
        pass


    # Enter a parse tree produced by pddl22Parser#untyped_list.
    def enterUntyped_list(self, ctx:pddl22Parser.Untyped_listContext):
        pass

    # Exit a parse tree produced by pddl22Parser#untyped_list.
    def exitUntyped_list(self, ctx:pddl22Parser.Untyped_listContext):
        pass


    # Enter a parse tree produced by pddl22Parser#typed_list.
    def enterTyped_list(self, ctx:pddl22Parser.Typed_listContext):
        pass

    # Exit a parse tree produced by pddl22Parser#typed_list.
    def exitTyped_list(self, ctx:pddl22Parser.Typed_listContext):
        pass


    # Enter a parse tree produced by pddl22Parser#pddl_type.
    def enterPddl_type(self, ctx:pddl22Parser.Pddl_typeContext):
        pass

    # Exit a parse tree produced by pddl22Parser#pddl_type.
    def exitPddl_type(self, ctx:pddl22Parser.Pddl_typeContext):
        pass


    # Enter a parse tree produced by pddl22Parser#constants_def.
    def enterConstants_def(self, ctx:pddl22Parser.Constants_defContext):
        pass

    # Exit a parse tree produced by pddl22Parser#constants_def.
    def exitConstants_def(self, ctx:pddl22Parser.Constants_defContext):
        pass


    # Enter a parse tree produced by pddl22Parser#predicates_def.
    def enterPredicates_def(self, ctx:pddl22Parser.Predicates_defContext):
        pass

    # Exit a parse tree produced by pddl22Parser#predicates_def.
    def exitPredicates_def(self, ctx:pddl22Parser.Predicates_defContext):
        pass


    # Enter a parse tree produced by pddl22Parser#atomic_formula_skeleton.
    def enterAtomic_formula_skeleton(self, ctx:pddl22Parser.Atomic_formula_skeletonContext):
        pass

    # Exit a parse tree produced by pddl22Parser#atomic_formula_skeleton.
    def exitAtomic_formula_skeleton(self, ctx:pddl22Parser.Atomic_formula_skeletonContext):
        pass


    # Enter a parse tree produced by pddl22Parser#untyped_var_list.
    def enterUntyped_var_list(self, ctx:pddl22Parser.Untyped_var_listContext):
        pass

    # Exit a parse tree produced by pddl22Parser#untyped_var_list.
    def exitUntyped_var_list(self, ctx:pddl22Parser.Untyped_var_listContext):
        pass


    # Enter a parse tree produced by pddl22Parser#typed_var_list.
    def enterTyped_var_list(self, ctx:pddl22Parser.Typed_var_listContext):
        pass

    # Exit a parse tree produced by pddl22Parser#typed_var_list.
    def exitTyped_var_list(self, ctx:pddl22Parser.Typed_var_listContext):
        pass


    # Enter a parse tree produced by pddl22Parser#functions_def.
    def enterFunctions_def(self, ctx:pddl22Parser.Functions_defContext):
        pass

    # Exit a parse tree produced by pddl22Parser#functions_def.
    def exitFunctions_def(self, ctx:pddl22Parser.Functions_defContext):
        pass


    # Enter a parse tree produced by pddl22Parser#action_def.
    def enterAction_def(self, ctx:pddl22Parser.Action_defContext):
        pass

    # Exit a parse tree produced by pddl22Parser#action_def.
    def exitAction_def(self, ctx:pddl22Parser.Action_defContext):
        pass


    # Enter a parse tree produced by pddl22Parser#goal_descriptor.
    def enterGoal_descriptor(self, ctx:pddl22Parser.Goal_descriptorContext):
        pass

    # Exit a parse tree produced by pddl22Parser#goal_descriptor.
    def exitGoal_descriptor(self, ctx:pddl22Parser.Goal_descriptorContext):
        pass


    # Enter a parse tree produced by pddl22Parser#atomic_formula.
    def enterAtomic_formula(self, ctx:pddl22Parser.Atomic_formulaContext):
        pass

    # Exit a parse tree produced by pddl22Parser#atomic_formula.
    def exitAtomic_formula(self, ctx:pddl22Parser.Atomic_formulaContext):
        pass


    # Enter a parse tree produced by pddl22Parser#term.
    def enterTerm(self, ctx:pddl22Parser.TermContext):
        pass

    # Exit a parse tree produced by pddl22Parser#term.
    def exitTerm(self, ctx:pddl22Parser.TermContext):
        pass


    # Enter a parse tree produced by pddl22Parser#function_comparison.
    def enterFunction_comparison(self, ctx:pddl22Parser.Function_comparisonContext):
        pass

    # Exit a parse tree produced by pddl22Parser#function_comparison.
    def exitFunction_comparison(self, ctx:pddl22Parser.Function_comparisonContext):
        pass


    # Enter a parse tree produced by pddl22Parser#binary_comparison.
    def enterBinary_comparison(self, ctx:pddl22Parser.Binary_comparisonContext):
        pass

    # Exit a parse tree produced by pddl22Parser#binary_comparison.
    def exitBinary_comparison(self, ctx:pddl22Parser.Binary_comparisonContext):
        pass


    # Enter a parse tree produced by pddl22Parser#expression.
    def enterExpression(self, ctx:pddl22Parser.ExpressionContext):
        pass

    # Exit a parse tree produced by pddl22Parser#expression.
    def exitExpression(self, ctx:pddl22Parser.ExpressionContext):
        pass


    # Enter a parse tree produced by pddl22Parser#binary_operator.
    def enterBinary_operator(self, ctx:pddl22Parser.Binary_operatorContext):
        pass

    # Exit a parse tree produced by pddl22Parser#binary_operator.
    def exitBinary_operator(self, ctx:pddl22Parser.Binary_operatorContext):
        pass


    # Enter a parse tree produced by pddl22Parser#effect.
    def enterEffect(self, ctx:pddl22Parser.EffectContext):
        pass

    # Exit a parse tree produced by pddl22Parser#effect.
    def exitEffect(self, ctx:pddl22Parser.EffectContext):
        pass


    # Enter a parse tree produced by pddl22Parser#c_effect.
    def enterC_effect(self, ctx:pddl22Parser.C_effectContext):
        pass

    # Exit a parse tree produced by pddl22Parser#c_effect.
    def exitC_effect(self, ctx:pddl22Parser.C_effectContext):
        pass


    # Enter a parse tree produced by pddl22Parser#conditional_effect.
    def enterConditional_effect(self, ctx:pddl22Parser.Conditional_effectContext):
        pass

    # Exit a parse tree produced by pddl22Parser#conditional_effect.
    def exitConditional_effect(self, ctx:pddl22Parser.Conditional_effectContext):
        pass


    # Enter a parse tree produced by pddl22Parser#p_effect.
    def enterP_effect(self, ctx:pddl22Parser.P_effectContext):
        pass

    # Exit a parse tree produced by pddl22Parser#p_effect.
    def exitP_effect(self, ctx:pddl22Parser.P_effectContext):
        pass


    # Enter a parse tree produced by pddl22Parser#assign_operator.
    def enterAssign_operator(self, ctx:pddl22Parser.Assign_operatorContext):
        pass

    # Exit a parse tree produced by pddl22Parser#assign_operator.
    def exitAssign_operator(self, ctx:pddl22Parser.Assign_operatorContext):
        pass


    # Enter a parse tree produced by pddl22Parser#durative_action_def.
    def enterDurative_action_def(self, ctx:pddl22Parser.Durative_action_defContext):
        pass

    # Exit a parse tree produced by pddl22Parser#durative_action_def.
    def exitDurative_action_def(self, ctx:pddl22Parser.Durative_action_defContext):
        pass


    # Enter a parse tree produced by pddl22Parser#duration_constraint.
    def enterDuration_constraint(self, ctx:pddl22Parser.Duration_constraintContext):
        pass

    # Exit a parse tree produced by pddl22Parser#duration_constraint.
    def exitDuration_constraint(self, ctx:pddl22Parser.Duration_constraintContext):
        pass


    # Enter a parse tree produced by pddl22Parser#simple_duration_constraint.
    def enterSimple_duration_constraint(self, ctx:pddl22Parser.Simple_duration_constraintContext):
        pass

    # Exit a parse tree produced by pddl22Parser#simple_duration_constraint.
    def exitSimple_duration_constraint(self, ctx:pddl22Parser.Simple_duration_constraintContext):
        pass


    # Enter a parse tree produced by pddl22Parser#duration_op.
    def enterDuration_op(self, ctx:pddl22Parser.Duration_opContext):
        pass

    # Exit a parse tree produced by pddl22Parser#duration_op.
    def exitDuration_op(self, ctx:pddl22Parser.Duration_opContext):
        pass


    # Enter a parse tree produced by pddl22Parser#durative_action_goal_descriptor.
    def enterDurative_action_goal_descriptor(self, ctx:pddl22Parser.Durative_action_goal_descriptorContext):
        pass

    # Exit a parse tree produced by pddl22Parser#durative_action_goal_descriptor.
    def exitDurative_action_goal_descriptor(self, ctx:pddl22Parser.Durative_action_goal_descriptorContext):
        pass


    # Enter a parse tree produced by pddl22Parser#timed_goal_descriptor.
    def enterTimed_goal_descriptor(self, ctx:pddl22Parser.Timed_goal_descriptorContext):
        pass

    # Exit a parse tree produced by pddl22Parser#timed_goal_descriptor.
    def exitTimed_goal_descriptor(self, ctx:pddl22Parser.Timed_goal_descriptorContext):
        pass


    # Enter a parse tree produced by pddl22Parser#time_specifier_prefix.
    def enterTime_specifier_prefix(self, ctx:pddl22Parser.Time_specifier_prefixContext):
        pass

    # Exit a parse tree produced by pddl22Parser#time_specifier_prefix.
    def exitTime_specifier_prefix(self, ctx:pddl22Parser.Time_specifier_prefixContext):
        pass


    # Enter a parse tree produced by pddl22Parser#time_specifier.
    def enterTime_specifier(self, ctx:pddl22Parser.Time_specifierContext):
        pass

    # Exit a parse tree produced by pddl22Parser#time_specifier.
    def exitTime_specifier(self, ctx:pddl22Parser.Time_specifierContext):
        pass


    # Enter a parse tree produced by pddl22Parser#durative_action_effect.
    def enterDurative_action_effect(self, ctx:pddl22Parser.Durative_action_effectContext):
        pass

    # Exit a parse tree produced by pddl22Parser#durative_action_effect.
    def exitDurative_action_effect(self, ctx:pddl22Parser.Durative_action_effectContext):
        pass


    # Enter a parse tree produced by pddl22Parser#timed_effect.
    def enterTimed_effect(self, ctx:pddl22Parser.Timed_effectContext):
        pass

    # Exit a parse tree produced by pddl22Parser#timed_effect.
    def exitTimed_effect(self, ctx:pddl22Parser.Timed_effectContext):
        pass


    # Enter a parse tree produced by pddl22Parser#function_assign_durative.
    def enterFunction_assign_durative(self, ctx:pddl22Parser.Function_assign_durativeContext):
        pass

    # Exit a parse tree produced by pddl22Parser#function_assign_durative.
    def exitFunction_assign_durative(self, ctx:pddl22Parser.Function_assign_durativeContext):
        pass


    # Enter a parse tree produced by pddl22Parser#expression_durative.
    def enterExpression_durative(self, ctx:pddl22Parser.Expression_durativeContext):
        pass

    # Exit a parse tree produced by pddl22Parser#expression_durative.
    def exitExpression_durative(self, ctx:pddl22Parser.Expression_durativeContext):
        pass


    # Enter a parse tree produced by pddl22Parser#assign_op_t.
    def enterAssign_op_t(self, ctx:pddl22Parser.Assign_op_tContext):
        pass

    # Exit a parse tree produced by pddl22Parser#assign_op_t.
    def exitAssign_op_t(self, ctx:pddl22Parser.Assign_op_tContext):
        pass


    # Enter a parse tree produced by pddl22Parser#expression_t.
    def enterExpression_t(self, ctx:pddl22Parser.Expression_tContext):
        pass

    # Exit a parse tree produced by pddl22Parser#expression_t.
    def exitExpression_t(self, ctx:pddl22Parser.Expression_tContext):
        pass


    # Enter a parse tree produced by pddl22Parser#derived_predicate_def.
    def enterDerived_predicate_def(self, ctx:pddl22Parser.Derived_predicate_defContext):
        pass

    # Exit a parse tree produced by pddl22Parser#derived_predicate_def.
    def exitDerived_predicate_def(self, ctx:pddl22Parser.Derived_predicate_defContext):
        pass


    # Enter a parse tree produced by pddl22Parser#problem.
    def enterProblem(self, ctx:pddl22Parser.ProblemContext):
        pass

    # Exit a parse tree produced by pddl22Parser#problem.
    def exitProblem(self, ctx:pddl22Parser.ProblemContext):
        pass


    # Enter a parse tree produced by pddl22Parser#object_declaration.
    def enterObject_declaration(self, ctx:pddl22Parser.Object_declarationContext):
        pass

    # Exit a parse tree produced by pddl22Parser#object_declaration.
    def exitObject_declaration(self, ctx:pddl22Parser.Object_declarationContext):
        pass


    # Enter a parse tree produced by pddl22Parser#init.
    def enterInit(self, ctx:pddl22Parser.InitContext):
        pass

    # Exit a parse tree produced by pddl22Parser#init.
    def exitInit(self, ctx:pddl22Parser.InitContext):
        pass


    # Enter a parse tree produced by pddl22Parser#init_element.
    def enterInit_element(self, ctx:pddl22Parser.Init_elementContext):
        pass

    # Exit a parse tree produced by pddl22Parser#init_element.
    def exitInit_element(self, ctx:pddl22Parser.Init_elementContext):
        pass


    # Enter a parse tree produced by pddl22Parser#goal.
    def enterGoal(self, ctx:pddl22Parser.GoalContext):
        pass

    # Exit a parse tree produced by pddl22Parser#goal.
    def exitGoal(self, ctx:pddl22Parser.GoalContext):
        pass


    # Enter a parse tree produced by pddl22Parser#metric_spec.
    def enterMetric_spec(self, ctx:pddl22Parser.Metric_specContext):
        pass

    # Exit a parse tree produced by pddl22Parser#metric_spec.
    def exitMetric_spec(self, ctx:pddl22Parser.Metric_specContext):
        pass


    # Enter a parse tree produced by pddl22Parser#optimization.
    def enterOptimization(self, ctx:pddl22Parser.OptimizationContext):
        pass

    # Exit a parse tree produced by pddl22Parser#optimization.
    def exitOptimization(self, ctx:pddl22Parser.OptimizationContext):
        pass


    # Enter a parse tree produced by pddl22Parser#ground_function_expression.
    def enterGround_function_expression(self, ctx:pddl22Parser.Ground_function_expressionContext):
        pass

    # Exit a parse tree produced by pddl22Parser#ground_function_expression.
    def exitGround_function_expression(self, ctx:pddl22Parser.Ground_function_expressionContext):
        pass


    # Enter a parse tree produced by pddl22Parser#variable.
    def enterVariable(self, ctx:pddl22Parser.VariableContext):
        pass

    # Exit a parse tree produced by pddl22Parser#variable.
    def exitVariable(self, ctx:pddl22Parser.VariableContext):
        pass


    # Enter a parse tree produced by pddl22Parser#name.
    def enterName(self, ctx:pddl22Parser.NameContext):
        pass

    # Exit a parse tree produced by pddl22Parser#name.
    def exitName(self, ctx:pddl22Parser.NameContext):
        pass



del pddl22Parser