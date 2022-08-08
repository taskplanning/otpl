from pddl.goal_descriptor import GoalDescriptor
from pddl.atomic_formula import AtomicFormula, TypedParameter


class DerivedPredicate:

    def __init__(self, condition : GoalDescriptor, predicate : AtomicFormula) -> None:
        self.condition = condition
        self.predicate = predicate

    def copy(self):
        """
        Returns a deep copy of the derived predicate.
        """
        return DerivedPredicate(self.condition.copy(), self.predicate.copy())

    # ======== #
    # visiting #
    # ======== #

    def visit(self, visit_function: callable, valid_types: tuple[type] = None, args=(), kwargs={}):
        """
        Calls the visit function on self, and recurses through the visit methods of members.
        param visit_function: the function to call on self.
        param valid_types: a set of types to visit. If None, all types are visited.
        """
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)

        self.condition.visit(visit_function, valid_types, args, kwargs)
        self.predicate.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters: list[TypedParameter]) -> 'DerivedPredicate':
        """
        Binds the parameters of the derived predicate to the given parameters.
        """
        return DerivedPredicate(self.condition.bind_parameters(parameters), self.predicate.bind_parameters(parameters))

    # ======== #
    # printing #
    # ======== #

    def __repr__(self) -> str:
        return "(:derived " + self.predicate.print_pddl() + " " + repr(self.condition) + ")"
