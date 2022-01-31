from pddl.goal_descriptor import GoalDescriptor
from pddl.atomic_formula import AtomicFormula


class DerivedPredicate:

    def __init__(self, condition : GoalDescriptor, predicate : AtomicFormula) -> None:
        self.condition = condition
        self.predicate = predicate

    def __repr__(self) -> str:
        return "(:derived " + self.predicate.print_pddl() + " " + repr(self.condition) + ")"