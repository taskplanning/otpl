from typing import List

class TypedParameter:
    def __init__(self, type : str, label : str, value : str = None) -> None:
        self.type = type
        self.label = label
        self.value = value

class AtomicFormula:
    """
    A class used to represent an atomic formula from the domain.
    """
    
    def __init__(self, name : str, typed_parameters : List[TypedParameter] = [], grounded : bool = False) -> None:
        self.name = name
        self.typed_parameters = typed_parameters
        self.grounded = grounded
        self.function_value = 0.0

    def print_pddl(self, include_types=False):
        """
        Prints as PDDL atomic formula, either using the parameter label or the bound object name if available.
        """
        return "(" + self.name \
            + (' ' if self.typed_parameters else '') \
            + ' '.join([
                (p.value if p.value else p.label) \
                + (" - " + p.type if include_types else '') \
                for p in self.typed_parameters]) + ")"