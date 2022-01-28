from typing import List

from defer import return_value
from pddl.domain_type import DomainType
from pddl.object import Object
from pddl.domain_operator import DomainOperator
from pddl.domain_formula import DomainFormula

class Domain:
    """
    A class that describes a PDDL domain model, including:
    - requirements
    - type heirarchy
    - constants
    - predicates & functions
    - operators
    """

    def __init__(self, domain_name : str) -> None:
        self.domain_name = domain_name    
        self.requirements : List[str] = []
        self.types : List[DomainType] = []
        self.constants : List[Object] = []
        self.predicates : List[DomainFormula] = []
        self.functions : List[DomainFormula] = []
        self.operators : List[DomainOperator] = []

    def __str__(self) -> str:

        # header
        return_string = "(define (" + self.domain_name + ")\n" \
            + "(:requirements " + " ".join(self.requirements) + ")\n"

        # types
        # TODO print type tree in order
        if self.types:
            return_string += "(:types\n"
            for type in self.types:
                return_string += "  " + type.name + " - " + type.parent + "\n"
            return_string += ")\n"

        # constants
        if self.constants:
            return_string += "(:constants\n"
            for constant in self.constants:
                return_string += "  " + constant.name + " - " + constant.type + "\n"
            return_string += ")\n"

        # predicates
        if self.predicates:
            return_string += "(:predicates\n"
            for pred in self.predicates:
                return_string += "  " + str(pred) + "\n"
            return_string += ")\n"

        # functions
        if self.functions:
            return_string += "(:functions\n"
            for func in self.functions:
                return_string += "  " + str(func) + "\n"
            return_string += ")\n"

        # operators
        for op in self.operators:
            return_string += str(op) + "\n"

        # end domain
        return_string += ')'

        return return_string