from typing import List
from domain_type import DomainType
from object import Object
from domain_operator import DomainOperator
from domain_formula import DomainFormula

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
        self.types : List[DomainType] = []
        self.constants : List[Object] = []
        self.predicates : List[DomainFormula] = []
        self.functions : List[DomainFormula] = []
        self.operators : List[DomainOperator] = []

    def print_problem(self):
        pass