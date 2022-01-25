from typing import List

class DomainFormula:
    """
    A class used to represent an atomic formula from the domain.
    """
    
    class TypedParameter:
        def __init__(self, type : str, name : str, value : str = None) -> None:
            self.type = type
            self.name = name
            self.value = value

    def __init__(self, name : str, typed_parameters : List[TypedParameter] = [], grounded : bool = False) -> None:
        self.name = name
        self.typed_parameters = typed_parameters
        self.grounded = grounded

    def __repr__(self) -> str:
        if self.grounded:
            return "(" + self.name \
                    + (' ' if self.typed_parameters else '') \
                    + ' '.join([p.value for p in self.typed_parameters]) \
                    + ")"
        else:
            return "(" + self.name \
                    + (' ' if self.typed_parameters else '') \
                    + ' '.join([p.name + " - " + p.type for p in self.typed_parameters]) \
                    + ")"
