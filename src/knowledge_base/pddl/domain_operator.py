from typing import List
from pddl.domain_formula import DomainFormula
from pddl.domain_assignment import DomainAssignment
from pddl.domain_inequality import DomainInequality
from pddl.probabilistic_effect import ProbabilisticEffect
from pddl.domain_effect import Effect, TimedEffect
from pddl.domain_condition import Condition, TimedCondition


class DomainOperator:
    """ 
    A class used to represent an operator in the domain.
    """

    def __init__(self,
            # header
            formula  : DomainFormula,
            duration : DomainInequality,
            condition : List[Condition] = [],
            effects : List[Effect] = [],
            ) -> None:
        # TODO assert duration includes "?duration" special type.
        self.formula = formula
        self.duration = duration
        self.condition = condition
        self.effects = effects

    def __str__(self) -> str:
        # TODO checking for empty parameters and conditions
        return "(durative-action " + self.formula.name + "\n" \
                + "  :parameters (" + str(self.formula).partition(' ')[2][:-1] + ")\n" \
                + "  :duration " + str(self.duration) + "\n" \
                + "  :condition (and\n  " \
                + "    " + "\n  ".join([c for c in self.condition]) + "\n" \
                + "  )\n" \
                + "  :effect (and\n  " \
                + "    " + "\n  ".join([e for e in self.effects]) + "\n" \
                + "  )\n" \
                + ")"
    

