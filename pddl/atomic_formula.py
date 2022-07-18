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
        self.typed_parameters : list[TypedParameter] = typed_parameters if typed_parameters else []
        self.function_value = 0.0

    def from_string(name : str, parameters : dict[str,str] = {}, values : dict[str,str] = {}) -> 'AtomicFormula':
        """
        Create an AtomicFormula from strings.
        - All PDDL parameter labels must begin with "?"
        - Untyped parameters (of type object) must be ordered after all typed parameters.
        - Values optionally maps some labels to bound objects or constants.
        param name: The name of the formula.
        param parameters: Dictionary mapping labels to types.
        param values: Dictionary mapping labels to values.
        """
        typed_parameters = []
        untyped = False
        for label, type in parameters.items():
            if not label.startswith("?"):
                raise Exception("PDDL parameters must begin with \"?\"")
            if type == "object":
                untyped = True
            elif untyped:
                raise Exception("Untyped parameters with type object must come after typed parameters.")

            if label in values:
                typed_parameters.append(TypedParameter(label=label, type=type, value=values[label]))
            else:
                typed_parameters.append(TypedParameter(label=label, type=type))
        return AtomicFormula(name, typed_parameters=typed_parameters)

    def print_pddl(self, include_types=False):
        """
        Prints as PDDL atomic formula, either using the parameter label or the bound object name if available.
        """
        return "(" + self.name \
            + (' ' if self.typed_parameters else '') \
            + ' '.join([
                (p.value if p.value else p.label) \
                + (" - " + p.type if include_types and not p.value else '') \
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