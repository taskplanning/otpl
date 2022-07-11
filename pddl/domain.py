from typing import Dict, List
from pddl.derived_predicate import DerivedPredicate
from pddl.domain_type import DomainType
from pddl.operator import Operator
from pddl.atomic_formula import AtomicFormula
from pddl.symbol_table import SymbolTable

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
        self.type_tree : Dict[str, DomainType] = {}
        self.constants_type_map : Dict[str,str] = {}
        self.type_constants_map : Dict[str,List[str]] = {}
        self.predicates : Dict[str, AtomicFormula] = {}
        self.functions : Dict[str, AtomicFormula] = {}
        self.operators : Dict[str,Operator] = {}
        self.derived_predicates : List[DerivedPredicate] = []

    def is_sub_type(self, type : str, parent : str) -> bool:
        """
        Checks if type is a subtype of parent.
        """
        if type == parent:
            return True
        if type not in self.type_tree:
            return False
        return self.is_sub_type(self.type_tree[type].parent, parent)
        

    def __str__(self) -> str:

        # header
        return_string = "(define (domain " + self.domain_name + ")\n" \
            + "(:requirements " + " ".join(self.requirements) + ")\n"

        # types
        if self.type_tree:
            return_string += "(:types\n"
            for _, type in self.type_tree.items():
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
            for _, pred in self.predicates.items():
                return_string += "  " + pred.print_pddl(include_types=True) + "\n"
            return_string += ")\n"

        # functions
        if self.functions:
            return_string += "(:functions\n"
            for _, func in self.functions.items():
                return_string += "  " + func.print_pddl(include_types=True) + "\n"
            return_string += ")\n"

        # derived predicates
        for der in self.derived_predicates:
            return_string += str(der) + "\n"

        # operators
        for _, op in self.operators.items():
            return_string += str(op) + "\n"

        # end domain
        return_string += ')'

        return return_string