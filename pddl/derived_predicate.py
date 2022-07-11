from pddl.goal_descriptor import GoalDescriptor
from pddl.atomic_formula import AtomicFormula, TypedParameter


class DerivedPredicate:

    def __init__(self, condition : GoalDescriptor, predicate : AtomicFormula) -> None:
        self.condition = condition
        self.predicate = predicate

    def __repr__(self) -> str:
        return "(:derived " + self.predicate.print_pddl() + " " + repr(self.condition) + ")"

    def bind_parameters(self, parameters: list[TypedParameter]) -> 'DerivedPredicate':
        """
        Binds the parameters of the derived predicate to the given parameters.
        """
        return DerivedPredicate(self.condition.bind_parameters(parameters), self.predicate.bind_parameters(parameters))