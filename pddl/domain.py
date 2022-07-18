from typing import Dict, List
from pddl.derived_predicate import DerivedPredicate
from pddl.domain_type import DomainType
from pddl.operator import Operator
from pddl.atomic_formula import AtomicFormula, TypedParameter
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

    # ======= #
    # Setters #
    # ======= #

    def add_type(self, type_name : str, parent_type : str = "object"):
        """
        Adds a new type to the domain.
        param type_name: the name of the new type.
        param parent_type: the name of the parent type. If not specified, the parent type is "object".
        """
        self.add_domain_type(DomainType(type_name, parent_type))

    def add_domain_type(self, type : DomainType):
        """
        Adds a new type to the domain. If the parent type is not yet in the domain, it is added.
        param type: the new type to add.
        """
        if type.parent != "object" and type.parent not in self.type_tree:
            self.type_tree[type.parent] = DomainType(type.parent, "object")
        self.type_tree[type.name] = type
        self.type_constants_map[type.name] = []
        
    def add_constant(self, constant : str, type : str = "object"):
        """
        Adds a new constant to the domain.
        param constant: the name of the new constant.
        param type: the type of the new constant.
        """
        if type not in self.type_tree and type != "object":
            self.add_type(type)
        self.constants_type_map[constant] = type
        if type not in self.type_constants_map:
            self.type_constants_map[type] = []
        self.type_constants_map[type].append(constant)

    def add_predicate_from_str(self, name : str, parameters : dict[str,str] = {}, constants : dict[str,str] = {}):
        """
        Adds a new predicate to the domain using AtomicFormula.from_string()
        param name: the name of the predicate to add.
        param parameters: dictionary mapping label to type.
        param constants: dictionary mapping label to constant value.
        """
        self.add_predicate(AtomicFormula.from_string(name, parameters, constants))
            

    def add_predicate(self, predicate : AtomicFormula):
        """
        Adds a new predicate to the domain.
        param pred: the new predicate to add.
        """
        self.predicates[predicate.name] = predicate

    def add_function_from_str(self, name : str, parameters : dict[str,str] = {}, constants : dict[str,str] = {}):
        """
        Adds a new function to the domain using AtomicFormula.from_string()
        param name: the name of the function to add.
        param parameters: dictionary mapping label to type.
        param constants: dictionary mapping label to constant value.
        """
        self.add_function(AtomicFormula.from_string(name, parameters, constants))

    def add_function(self, function : AtomicFormula):
        """
        Adds a new function to the domain.
        param function: the new function to add.
        """
        self.functions[function.name] = function

    def add_operator_from_str(self, name : str, parameters : dict[str,str] = {}, durative : bool = False):
        """
        Adds a new operator to the domain using AtomicFormula.from_string()
        param name: the name of the operator to add.
        param parameters: dictionary mapping parameter label to type.
        """
        self.add_operator(Operator(AtomicFormula.from_string(name, parameters), durative=durative))

    def add_operator(self, operator : Operator):
        """
        Adds a new operator to the domain.
        param operator: the new operator to add.
        """
        self.operators[operator.formula.name] = operator


    # =================== #
    # Queries and utility #
    # =================== #


    def is_sub_type(self, type : str, parent : str) -> bool:
        """
        Checks if type is a subtype of parent.
        """
        if type == parent:
            return True
        if type not in self.type_tree:
            return False
        return self.is_sub_type(self.type_tree[type].parent, parent)
        
    # ======== #
    # Printing #
    # ======== #

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