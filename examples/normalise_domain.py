from examples.create_temporal_domain import create_temporal_domain
from pddl.atomic_formula import TypedParameter
from pddl.domain import Domain
from pddl.operator import Operator

def normalise_domain(dom : Domain) -> None:
    """
    Removes all types from domain, maps constants to "object" instead.
    Adds unary predicates to domain for each type.
    """
    for type in dom.type_tree.values():
        dom.add_predicate_from_str(type.name, {"?o" : "object"})
    dom.type_tree.clear()
    dom.constants_type_map = { name : "object" for name in dom.constants_type_map.keys() }
    dom.type_constants_map = { "object" : [ constant for constant in dom.constants_type_map.keys() ] }

    # remove types from operators
    dom.visit(normalise, (TypedParameter,Operator))

def normalise(element) -> None:
    """
    Visits domain elements recursively and replaces all types with "object".
    In operator, adds unary predicates for each typed parameter to the condition.
    """
    if isinstance(element, TypedParameter):
        element.type = "object"
    elif isinstance(element, Operator):
        for parameter in element.formula.typed_parameters:
            if parameter.type != "object":
                element.add_simple_condition_from_str(parameter.type, { "?o": parameter.label } )

if __name__ == "__main__":

    domain = create_temporal_domain()

    print("Original domain")
    print("===============")
    print(domain)
    print()

    # Normalise the domain by removing types
    normalise_domain(domain)

    print("Normalised domain")
    print("=================")
    print(domain)