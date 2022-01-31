from pddl.domain_condition import GoalDescriptor
from pddl.domain_formula import DomainFormula


class DerivedPredicate:

    def __init__(self, condition : GoalDescriptor, predicate : DomainFormula) -> None:
        self.condition = condition
        self.predicate = predicate

    def __repr__(self) -> str:
        return "(:derived " + self.predicate.print_pddl() + " " + repr(self.condition) + ")"