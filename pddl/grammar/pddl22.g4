grammar pddl22;

pddl_file
  : domain
  | problem
  ;

/*--------*/
/* domain */
/*--------*/

domain
  : '(' DEFINE '(' 'domain' name ')'
  require_def?
  types_def?
  (constants_def | predicates_def | functions_def)+?
  (action_def | durative_action_def | derived_predicate_def)+?
  ')'
  ;

/*--------------*/
/* requirements */
/*--------------*/

require_def
  : '(:requirements' require_key+ ')'
  ;

require_key
  : ':strips'
  | ':typing'
  | ':negative-preconditions'
  | ':disjunctive-preconditions'
  | ':equality'
  | ':existential-preconditions'
  | ':universal-preconditions'
  | ':quantified-preconditions'
  | ':conditional-effects'
  | ':fluents'
  | ':adl'
  | ':durative-actions'
  | ':duration-inequalities'
  | ':continuous-effects'
  | ':derived-predicates'
  | ':timed-initial-literals'
  | ':preferences'
  | ':constraints'
  ;

/*-------*/
/* types */
/*-------*/

types_def
  : '(:types' typed_type_list* untyped_type_list? ')'
  ;

untyped_type_list
  :  name+
  ;

typed_type_list
  : name+ '-' pddl_type
  ;

pddl_type
  : name
  | '(' EITHER name+ ')'
  ;

/*-----------*/
/* constants */
/*-----------*/

constants_def
  : '(:constants' typed_name_list* untyped_name_list? ')'
  ;

untyped_name_list
  :  name+
  ;

typed_name_list
  : name+ '-' pddl_type
  ;

/*------------*/
/* predicates */
/*------------*/

predicates_def
  : '(:predicates' atomic_formula_skeleton* ')'
  ;

atomic_formula_skeleton
  : '(' name typed_var_list* untyped_var_list? ')'
  ;

untyped_var_list
  : variable+
  ;

typed_var_list
  : variable+ '-' pddl_type
  ;

/*-----------*/
/* functions */
/*-----------*/

functions_def
  : '(:functions' atomic_formula_skeleton* ')'
  ;

/*---------------*/
/* simple action */
/*---------------*/

action_def
  : '(:action' name
  ':parameters (' typed_var_list* untyped_var_list? ')' 
  (':precondition' goal_descriptor)?
  (':effect' effect)?
  ')'
  ;

/*-------*/
/* goals */
/*-------*/

goal_descriptor
  : '()' #goal_descriptor_empty
  | atomic_formula #goal_descriptor_simple
  | '(' AND goal_descriptor* ')' #goal_descriptor_conjunction
  | '(' OR goal_descriptor* ')' #goal_descriptor_disjunction
  | '(' NOT goal_descriptor ')' #goal_descriptor_negative
  | '(' IMPLY goal_descriptor goal_descriptor ')' #goal_descriptor_implication
  | '(' EXISTS '(' typed_var_list* untyped_var_list? ')' goal_descriptor ')' #goal_descriptor_existential
  | '(' FORALL '(' typed_var_list* untyped_var_list? ')' goal_descriptor ')' #goal_descriptor_universal
  | function_comparison #goal_descriptor_comparison
  ;

atomic_formula
  : '(' name term_list ')'
  ;

term_list
  : term*
  ;

term
  : variable #term_var
  | name #term_name
  ;

function_comparison
  :  '(' binary_comparison expression expression ')'
  ;

binary_comparison
  : '>'
  | '<'
  | '>='
  | '<='
  ;

expression
  : number #expression_number
  | '(' binary_operator expression expression ')' #expression_binary_op
  | '(' '-' expression ')' #expression_uminus
  | atomic_formula #expression_function
  ;

binary_operator
  : '+'
  | '-'
  | '*'
  | '/'
  ;

/*---------*/
/* effects */
/*---------*/

effect
  : '()' #effect_empty
  | '(' AND c_effect* ')' #effect_conjunction
  | c_effect #effect_c_effect
  ;

c_effect
  : '(' FORALL '(' typed_var_list* untyped_var_list? ')' effect ')' #c_effect_forall
  | '(' WHEN goal_descriptor conditional_effect ')' #c_effect_conditional
  | p_effect #c_effect_primitive
  ;

conditional_effect
  : '(' AND p_effect* ')' #conditional_effect_conjunction
  | p_effect #conditional_effect_primitive
  ;

p_effect
  : '(' assign_operator atomic_formula expression ')' #p_effect_assign
  | '(' NOT atomic_formula ')' #p_effect_negative
  | atomic_formula #p_effect_simple
  ;

assign_operator
  : 'assign'
  | 'scale-up'
  | 'scale-down'
  | 'increase'
  | 'decrease'
  ;

/*------------------*/
/* durative actions */
/*------------------*/

time_specifier
  : AT TIME_SPECIFIER_SUFFIX
  | OVER_ALL
  ;

durative_action_def
  : '(:durative-action' name
  ':parameters (' typed_var_list* untyped_var_list? ')' 
  ':duration' duration_constraint
  (':condition' durative_action_goal_descriptor)?
  (':effect' durative_action_effect)?
  ')'
  ;

duration_constraint
  : '()' #duration_constraint_empty
  | '(' AND simple_duration_constraint* ')' #duration_constraint_conjunction
  | simple_duration_constraint #duration_constraint_simple
  ;

simple_duration_constraint
  : '(' duration_op '?duration' expression ')' #simple_duration_constraint_simple
  | '(' AT TIME_SPECIFIER_SUFFIX simple_duration_constraint ')' #simple_duration_constraint_timed
  ;

duration_op
  : '<='
  | '>='
  | '='
  ;

durative_action_goal_descriptor
  : '()' #durative_action_goal_descriptor_empty
  | '(' AND timed_goal_descriptor+ ')' #durative_action_goal_descriptor_conjunction
  | timed_goal_descriptor #durative_action_goal_descriptor_timed
  ;

timed_goal_descriptor
  : '(' time_specifier goal_descriptor ')' 
  ;

durative_action_effect
  : '()' #durative_action_effect_empty
  | '(' AND durative_action_effect* ')' #durative_action_effect_conjunction
  | timed_effect #durative_action_effect_timed
  | '(' FORALL '(' typed_var_list* untyped_var_list? ')' durative_action_effect ')' #durative_action_effect_forall
  | '(' WHEN durative_action_goal_descriptor timed_effect ')' #durative_action_effect_conditional
  ;

timed_effect
  : '(' AT TIME_SPECIFIER_SUFFIX c_effect ')' #timed_effect_timed
  | '(' AT TIME_SPECIFIER_SUFFIX function_assign_durative ')' #timed_effect_assign
  | '(' assign_op_t atomic_formula expression_t ')' #timed_effect_continuous
  ;

function_assign_durative
  : '(' assign_operator atomic_formula expression_durative ')'
  ;

expression_durative
  : '(' binary_operator expression_durative expression_durative ')' #expression_durative_operator
  | '(' '-' expression_durative ')' #expression_durative_uminus
  | '?duration' #expression_durative_duration
  | expression #expression_durative_expression
  ;

assign_op_t
  : 'increase'
  | 'decrease'
  ;

expression_t
  : '(' '*' expression '#t)'
  | '(' '*' '#t' expression ')'
  | '#t'
  ;

/*--------------------*/
/* derived predicates */
/*--------------------*/

derived_predicate_def
  : '(:derived' atomic_formula_skeleton goal_descriptor ')'
  ;

/*---------*/
/* problem */
/*---------*/

problem
  : '(' DEFINE '(' 'problem' name ')'
  '(:domain' name ')'
  require_def?
  object_declaration?
  init
  goal
  metric_spec?
  ')'
  ;

object_declaration
  : '(:objects' typed_name_list* untyped_name_list? ')'
  ;

init
  : '(:init' init_element* ')'
  ;

init_element
  : atomic_formula #init_element_simple
  | '(' '=' atomic_formula number ')' #init_element_assign
  | '(' AT number p_effect ')' #init_element_til
  ;

goal
  : '(:goal' goal_descriptor ')'
  ;

metric_spec
  : '(:metric' optimization ground_function_expression ')'
  ;

optimization
  : 'minimize'
  | 'maximize'
  ;

ground_function_expression
  : number #ground_function_expression_number
  | '(' binary_operator ground_function_expression ground_function_expression ')' #ground_function_expression_binary
  | '(' '-' ground_function_expression ')' #ground_function_expression_uminus
  | '(' name name* ')' #ground_function_expression_function
  | 'total-time' #ground_function_expression_total_time
  | '(' ground_function_expression ')' #ground_function_expression_parenthesis
  ;

/*-------*/
/* LEXER */
/*-------*/

variable
  : VARIABLE
  ;

name // allows 'at' as predicate name, etc.
  : NAME
  | AT 
  | OVER_ALL
  | NOT
  | OR
  | AND
  | IMPLY
  | FORALL
  | EXISTS
  | EITHER
  | WHEN
  | DEFINE
  | TIME_SPECIFIER_SUFFIX
  ;

number
  : NUMBER
  ;

VARIABLE
  : '?' (NAME | AT | TIME_SPECIFIER_SUFFIX)
  ;

AT
  : ('at' | 'AT')
  ;

NOT
  : ('not' | 'NOT')
  ;

OR 
  : ('or' | 'OR')
  ;

AND 
  : ('and' | 'AND')
  ;

IMPLY 
  : ('imply' | 'IMPLY')
  ;

FORALL 
  : ('forall' | 'FORALL')
  ;

EXISTS 
  : ('exists' | 'EXISTS')
  ;

EITHER 
  : ('either' | 'EITHER')
  ;

WHEN 
  : ('when' | 'WHEN')
  ;

DEFINE 
  : ('define' | 'DEFINE')
  ;

TIME_SPECIFIER_SUFFIX
  : ('start' | 'end' | 'END' | 'START')
  ;

OVER_ALL
  : ('over' | 'OVER')(' ')+('all' | 'ALL')
  ;

NAME
  : ('a'..'z' | 'A'..'Z')('a'..'z' | 'A'..'Z' | '0'..'9' | '_' | '-')*
  ;

NUMBER
  : ('-')?('0'..'9')+
  | ('-')?('0'..'9')+ '.' ('0'..'9')+
  ;

COMMENT
  : ';' ~[\r\n]* -> skip
  ;

WS
  : [ \t\r\n]+ -> skip
  ;