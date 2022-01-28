grammar pddl22;

pddl_file
  : domain
  | problem
  ;

/*--------*/
/* domain */
/*--------*/

domain
  : '(define' '(' 'domain' name ')'
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
  : '(:types' typed_list* untyped_list* ')'
  ;

untyped_list
  :  name+
  ;

typed_list
  : name+ '-' pddl_type
  ;

pddl_type
  : (name | '(either' name+ ')')
  ;

/*-----------*/
/* constants */
/*-----------*/

constants_def
  : '(:constants' typed_list* untyped_list* ')'
  ;

/*------------*/
/* predicates */
/*------------*/

predicates_def
  : '(:predicates' atomic_formula_skeleton* ')'
  ;

atomic_formula_skeleton
  : '(' name typed_var_list* untyped_var_list* ')'
  ;

untyped_var_list
  :  variable+
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
  ':parameters (' untyped_var_list* untyped_var_list ')' 
  (':precondition' goal_descriptor)?
  (':effect' effect)?
  ')'
  ;

/*-------*/
/* goals */
/*-------*/

goal_descriptor
  : '()'
  | atomic_formula
  | '(and' atomic_formula* ')'
  | '(or' atomic_formula* ')'
  | '(not' goal_descriptor ')'
  | '(imply' goal_descriptor goal_descriptor ')'
  | '(exists' '(' typed_var_list ')' goal_descriptor ')'
  | '(forall' '(' typed_var_list ')' goal_descriptor ')'
  | function_comparison
  ;

atomic_formula
  : '(' name term* ')'
  ;

term
  : variable
  | name
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
  : NUMBER
  | '(' binary_operator expression expression ')'
  | '(' '-' expression ')'
  | atomic_formula
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
  : '()'
  | '(and' c_effect* ')'
  ;

c_effect
  : '(forall' '(' typed_var_list ')' effect ')'
  | '(when' goal_descriptor conditional_effect ')'
  | p_effect
  ;

conditional_effect
  : '(and' p_effect* ')'
  | p_effect
  ;

p_effect
  : '(' assign_operator atomic_formula expression ')'
  | '(not' atomic_formula ')'
  | atomic_formula
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

durative_action_def
  : '(:durative-action' name
  ':parameters (' typed_var_list* untyped_var_list* ')' 
  ':duration' duration_constraint
  ':condition' durative_action_goal_descriptor
  ':effect' durative_action_effect
  ')'
  ;

duration_constraint
  : '()'
  | '(and' simple_duration_constraint ')'
  | simple_duration_constraint
  ;

simple_duration_constraint
  : '(' duration_op '?duration' expression ')'
  | '(at' time_specifier simple_duration_constraint ')'
  ;

duration_op
  : '<='
  | '>='
  | '='
  ;

durative_action_goal_descriptor
  : '()'
  | '(and' timed_goal_descriptor+ ')'
  | timed_goal_descriptor ')'
  ;

timed_goal_descriptor
  : time_specifier_prefix time_specifier goal_descriptor ')' 
  ;

time_specifier_prefix
  : '(at'
  | '(over'
  ;
 
time_specifier
  : 'start'
  | 'end'
  | 'all'
  ;

durative_action_effect
  : '()'
  | '(and' durative_action_effect* ')'
  | timed_effect
  | '(forall' '(' typed_var_list ')' durative_action_effect ')'
  | '(when' durative_action_goal_descriptor timed_effect ')'
  | '(' assign_operator atomic_formula expression_durative ')'
  ;

timed_effect
  : '(at' time_specifier c_effect ')'
  | '(at' time_specifier function_assign_durative ')'
  | '(' assign_op_t atomic_formula expression_t ')'
  ;

function_assign_durative
  : '(' assign_operator atomic_formula expression_durative ')'
  ;

expression_durative
  : '(' binary_operator expression_durative expression_durative ')'
  | '(-' expression_durative ')'
  | '?duration'
  | expression
  ;

assign_op_t
  : 'increase'
  | 'decrease'
  ;

expression_t
  : '(*' expression '#t)'
  | '(*' '#t' expression ')'
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
  : '(define' '(' 'problem' name ')'
  '(:domain' name ')'
  require_def?
  object_declaration?
  init
  goal
  metric_spec?
  ')'
  ;

object_declaration
  : '(:objects' typed_list* untyped_list* ')'
  ;

init
  : '(:init' init_element* ')'
  ;

init_element
  : atomic_formula
  | '(=' atomic_formula ')'
  | '(at' NUMBER atomic_formula ')'
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
  : NUMBER
  | '(' binary_operator ground_function_expression ground_function_expression ')'
  | '(' '-' ground_function_expression ')'
  | '(' name name* ')'
  | 'total-time'
  ;

/*-------*/
/* LEXER */
/*-------*/

variable
  : VARIABLE
  ;

name
  : NAME
  ;

VARIABLE
  : '?' NAME
  ;


NAME
  : ('a'..'z' | 'A'..'Z')('a'..'z' | 'A'..'Z' | '0'..'9' | '_' | '-')*
  ;

NUMBER
  : ('0'..'9')+
  | ('0'..'9')+ '.' ('0'..'9')+
  ;

COMMENT
  : ';' ~[\r\n]* -> skip
  ;

WS
  : [ \t\r\n]+ -> channel(HIDDEN)
  ;
