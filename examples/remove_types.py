from examples.create_temporal_problem import create_temporal_problem
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.domain import Domain
from pddl.domain_type import DomainType
from pddl.effect import EffectConditional, EffectConjunction, EffectForall, EffectType
from pddl.goal_descriptor import GoalConjunction, GoalQuantified, GoalSimple, GoalType
from pddl.operator import Operator
from pddl.problem import Problem

# ====== #
# domain #
# ====== #

def remove_types_from_domain(dom : Domain) -> None:
    """
    Removes all types from domain, maps constants to type "object" instead.
    Adds unary predicates to domain for each type.
    """
    for type in dom.type_tree.values():
        dom.add_predicate_from_str(type.name, {"?o" : "object"})
    dom.type_tree.clear()
    dom.constants_type_map = { name : "object" for name in dom.constants_type_map.keys() }
    dom.type_constants_map = { "object" : [ constant for constant in dom.constants_type_map.keys() ] }

    # remove types from operators
    dom.visit(remove_types_from_element, (TypedParameter,Operator,GoalQuantified,EffectForall))

def remove_types_from_element(element) -> None:
    """
    Visits elements recursively and replaces all types with "object".
    In operator, adds unary predicates for each typed parameter to the condition.
    In forall and exists conditions, adds unary predicates for each typed parameter to the condition.
    """
    if isinstance(element, TypedParameter):
        element.type = "object"
    elif isinstance(element, Operator):
        for parameter in element.formula.typed_parameters:
            if parameter.type != "object":
                element.add_simple_condition_from_str(parameter.type, { parameter.label : "object" } ) 
    elif isinstance(element, GoalQuantified):
        if element.goal.goal_type != GoalType.CONJUNCTION:
            element.goal = GoalConjunction([element.goal])
        for parameter in element.typed_parameters:
            if parameter.type != "object":
                element.goal.goals.append(GoalSimple(AtomicFormula.from_string(parameter.type, { parameter.label : "object" } )))
    elif isinstance(element, EffectForall):
        if element.effect.effect_type != EffectType.CONDITIONAL:
            element.effect = EffectConditional(GoalConjunction([]),element.effect)
        if element.effect.condition.goal_type != GoalType.CONJUNCTION:
            element.effect.condition = GoalConjunction([element.effect.condition])
        for parameter in element.typed_parameters:
            if parameter.type != "object":
                element.effect.condition.goals.append(GoalSimple(AtomicFormula.from_string(parameter.type, { parameter.label : "object" } )))

# ======= #
# problem #
# ======= #

def remove_types_from_problem(problem : Problem) -> None:
    """
    Removes all types from domain and problem.    
    Sets unary type propositions in the initial state.
    """  
    # make unary predicates for each type
    for type in problem.domain.type_tree.values():
        problem.domain.add_predicate_from_str(type.name, {"?o" : "object"})

    # add unary type propositions to initial state
    for type_name in problem.type_objects_map.keys():
        make_unary_type_proposition(problem, problem.domain.type_tree[type_name], problem.domain.type_tree[type_name])

    # remove types from initial state, goal, and metric
    problem.visit(remove_types_from_element, (TypedParameter))

    # remove types from domain
    problem.domain.type_tree.clear()
    problem.domain.constants_type_map = { name : "object" for name in problem.domain.constants_type_map.keys() }
    problem.domain.type_constants_map = { "object" : [ constant for constant in problem.domain.constants_type_map.keys() ] }

    # remove types from operators
    problem.domain.visit(remove_types_from_element, (TypedParameter,Operator,GoalQuantified,EffectForall))
    

def make_unary_type_proposition(problem : Problem, sub_type : DomainType, parent_type : DomainType) -> None:
    """
    Recursively adds a unary type facts to the initial state of the problem for the given subtype.
    param problem: the problem to add the unary type facts to.
    param sub_type: the exact type of the objects for which to add the facts.
    param parent_type: the type of unary predicate to add.
    """
    for obj in problem.type_objects_map[sub_type.name]:
        problem.add_proposition_from_str(parent_type.name, [obj])
        if parent_type.name != "object" and parent_type in problem.domain.type_tree:
            make_unary_type_proposition(problem.domain, problem, sub_type, problem.domain.type_tree[parent_type].parent)

if __name__ == "__main__":

    problem = create_temporal_problem()

    print("Original domain")
    print("================")
    print(problem.domain)
    print()

    print("Original problem")
    print("================")
    print(problem)
    print()

    # Normalise the problem, removing types
    remove_types_from_problem(problem)

    print("Normalised domain")
    print("==================")
    print(problem.domain)
    print()

    print("Normalised problem")
    print("==================")
    print(problem)