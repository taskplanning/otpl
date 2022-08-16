class TypedParameter:
    def __init__(self, type : str, label : str, value : str = None) -> None:
        self.type = type
        self.label = label
        self.value = value

    def __repr__(self):
        return "(" \
            + (self.type if self.type else "") \
            + "," + (self.label if self.label else "") \
            + "," + (self.value if self.value else "") \
            + ")"

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)

class AtomicFormula:
    """
    A class used to represent an atomic formula from the domain.
    """
    
    def __init__(self, name : str, typed_parameters : list[TypedParameter] = None) -> None:
        self.name = name
        self.typed_parameters : list[TypedParameter] = typed_parameters if typed_parameters else []

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

    # ======== #
    # visiting #
    # ======== #

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}):
        """
        Calls the given function with this atomic formula, if in valid_types.
        param visit_function: The function to call.
        param valid_types: A set of types to call the function on. If None, all types are accepted.
        """
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        for p in self.typed_parameters:
            p.visit(visit_function, valid_types, args, kwargs)

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

    # ======== #
    # printing #
    # ======== #

    def print_pddl(self, include_types=False):
        """
        Prints as PDDL atomic formula, either using the parameter label or the bound object name if available.
        """
        return "(" + self.name \
            + (' ' if self.typed_parameters else '') \
            + ' '.join([
                (p.value if p.value else p.label) \
                + (" - " + p.type if include_types and not p.value and not p.type=="object" else '') \
                for p in self.typed_parameters]) + ")"

    def __repr__(self):
        return self.print_pddl(False)

    def copy(self) -> 'AtomicFormula':
        """
        Returns a deep copy of the atomic formula.
        """
        return AtomicFormula(
            self.name,
            typed_parameters=[ TypedParameter(p.type, p.label, p.value) for p in self.typed_parameters])
