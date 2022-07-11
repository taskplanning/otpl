from pddl.duration import Duration
from pddl.atomic_formula import AtomicFormula, TypedParameter
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
    
    def print_pddl(self) -> str:
        return self.formula.print_pddl(include_types=False)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Operator':
        """
        parameters: list of TypedParameter whose type and label must match the type and label of the operator.
        returns a copy of the operator whose conditions and effects have been grounded with the given values.
        """
        return Operator(
            self.formula.bind_parameters(parameters),
            durative=self.durative,
            duration=self.duration.bind_parameters(parameters),
            condition=self.condition.bind_parameters(parameters),
            effect=self.effect.bind_parameters(parameters)
        )