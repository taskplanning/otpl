from typing import List
from pddl.duration import Duration
from pddl.atomic_formula import AtomicFormula
from pddl.effect import Effect
from pddl.goal_descriptor import GoalDescriptor


class Operator:
    """ 
    A class used to represent an operator in the domain.
    """

    def __init__(self,
            # header
            formula  : AtomicFormula,
            durative : bool,
            duration : Duration = Duration(),
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
    

