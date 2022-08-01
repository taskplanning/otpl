from examples.create_temporal_problem import create_temporal_problem
from examples.normalise_domain import normalise
from pddl.atomic_formula import TypedParameter
from pddl.domain_type import DomainType
from pddl.operator import Operator
from pddl.problem import Problem

def normalise_problem(problem : Problem):
    """
    Removes all types from domain and problem.
    Adds unary predicates to domain for each type.
    Sets unary type propositions in the initial state.
    """  
    # make unary predicates for each type
    for type in problem.domain.type_tree.values():
        problem.domain.add_predicate_from_str(type.name, {"?o" : "object"})

    for type_name in problem.type_objects_map.keys():
        make_unary_type_proposition(problem, problem.domain.type_tree[type_name], problem.domain.type_tree[type_name])
    problem.visit(normalise, (TypedParameter))

    # remove types from domain
    problem.domain.type_tree.clear()
    problem.domain.constants_type_map = { name : "object" for name in problem.domain.constants_type_map.keys() }
    problem.domain.type_constants_map = { "object" : [ constant for constant in problem.domain.constants_type_map.keys() ] }

    # remove types from operators
    problem.domain.visit(normalise, (TypedParameter,Operator))
    

def make_unary_type_proposition(problem : Problem, sub_type : DomainType, parent_type : DomainType):
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

    print("Original problem")
    print("================")
    print(problem)
    print()

    # Normalise the problem, removing types
    normalise_problem(problem)

    print("Normalised problem and domain")
    print("==================")
    print(problem.domain)
    print()
    print(problem)