from typing import Union
from enum import Enum
from pddl.domain_formula import DomainFormula
from pddl.domain_inequality import DomainInequality
from pddl.domain_effect import TIME_SPEC 

class Condition:
    """
    This class describes a simple condition for instant action or goal spec.
    """

    def __init__(self, condition : Union[DomainFormula,DomainInequality], negative : bool = False) -> None:
        self.condition = condition
        self.negative = negative

    def __repr__(self) -> str:
        if self.negative: return "(not " + str(self.condition) + ")"
        else: return str(self.condition)


class TimedCondition(Condition):
    """
    This class describes a simple add or delete effect with time specifier for durative action.
    """

    def __init__(self, time_spec : TIME_SPEC, condition : Union[DomainFormula,DomainInequality], negative : bool = False) -> None:
        super().__init__(condition, negative)
        self.time_spec = time_spec

    def __repr__(self) -> str:
        return "(" + self.time_spec.value + " " + str(self.effect) + ")"