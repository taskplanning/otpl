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
    
    def __init__(self, name : str, typed_parameters : List[TypedParameter] = None, grounded : bool = False) -> None:
        self.name = name
        self.typed_parameters = typed_parameters if typed_parameters else []
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

    def __repr__(self):
        return self.print_pddl(False)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'AtomicFormula':
        """
        Binds the parameters of a copy of the atomic formula to the given list of parameters.
        """
        bound_parameters : list[TypedParameter] = []
        for parameter in self.typed_parameters:
            bound_parameters.append(TypedParameter(parameter.type, parameter.label))
            for p in parameters:
                if p.label == parameter.label:
                    bound_parameters[-1].value = p.value
                    break                
        return AtomicFormula(self.name, bound_parameters)