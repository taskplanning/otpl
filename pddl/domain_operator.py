from typing import List
from pddl.domain_duration import DomainDuration
from pddl.domain_formula import DomainFormula
from pddl.domain_assignment import DomainAssignment
from pddl.domain_inequality import DomainInequality
from pddl.probabilistic_effect import ProbabilisticEffect
from pddl.domain_effect import Effect, TimedEffect
from pddl.domain_condition import GoalDescriptor


class DomainOperator:
    """ 
    A class used to represent an operator in the domain.
    """

    def __init__(self,
            # header
            formula  : DomainFormula,
            durative : bool,
            duration : DomainDuration = DomainDuration(),
            condition : GoalDescriptor = GoalDescriptor(),
            effect : Effect = Effect(),
            ) -> None:
        self.formula = formula
        self.durative = durative
        self.duration = duration
        self.condition = condition
        self.effect = effect

    def __str__(self) -> str:
        # TODO checking for empty parameters and conditions
        return ("(durative-action " if self.durative else "(action ") \
                + self.formula.name + "\n" \
                + "  :parameters (" + self.formula.print_pddl(include_types=True).partition(' ')[2][:-1] + ")\n" \
                + ("  :duration " + str(self.duration) + "\n" if self.durative else "") \
                + ("  :condition " if self.durative else "  :precondition ") \
                + str(self.condition) + "\n" \
                + "  :effect " \
                + str(self.effect) + "\n" \
                + ")"
    

