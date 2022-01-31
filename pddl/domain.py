from typing import Dict, List
from pddl.derived_predicate import DerivedPredicate
from pddl.domain_type import DomainType
from pddl.operator import Operator
from pddl.atomic_formula import AtomicFormula

class Domain:
    """
    A class that describes a PDDL domain model, including:
    - *requirements* as a list of strings.
    - *type heirarchy* as a list of pddl.domain_type.DomainType.
    - *constants* as two dicts mapping: (a) object name to type (str->str) (b) type to object names (str->List[str]).
    - *predicates* & *functions* both as a list of pddl.domain_formula.DomainFormula.
    - *operators* as a list of pddl.domain_operator.DomainOperator.
    """

    def __init__(self, domain_name : str) -> None:
        self.domain_name = domain_name    
        self.requirements : List[str] = []
        self.types : List[DomainType] = []
        self.constants_type_map : Dict[str,str] = {}
        self.type_constants_map : Dict[str,List[str]] = {}
        self.predicates : List[AtomicFormula] = []
        self.functions : List[AtomicFormula] = []
        self.operators : List[Operator] = []
        self.derived_predicates : List[DerivedPredicate] = []

    def __str__(self) -> str:

        # header
        return_string = "(define (domain " + self.domain_name + ")\n" \
            + "(:requirements " + " ".join(self.requirements) + ")\n"

        # types
        # TODO print type tree in order
        if self.types:
            return_string += "(:types\n"
            for type in self.types:
                return_string += "  " + type.name + " - " + type.parent + "\n"
            return_string += ")\n"

        # constants
        if self.constants_type_map:
            return_string += "(:constants\n"
            for constant, type in self.constants_type_map.items():
                return_string += "  " + constant + " - " + type + "\n"
            return_string += ")\n"

        # predicates
        if self.predicates:
            return_string += "(:predicates\n"
            for pred in self.predicates:
                return_string += "  " + pred.print_pddl(include_types=True) + "\n"
            return_string += ")\n"

        # functions
        if self.functions:
            return_string += "(:functions\n"
            for func in self.functions:
                return_string += "  " + func.print_pddl(include_types=True) + "\n"
            return_string += ")\n"

        # derived predicates
        for der in self.derived_predicates:
            return_string += str(der) + "\n"

        # operators
        for op in self.operators:
            return_string += str(op) + "\n"

        # end domain
        return_string += ')'

        return return_string