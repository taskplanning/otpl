from typing import Union
from enum import Enum
from pddl.domain_formula import DomainFormula
from pddl.domain_assignment import DomainAssignment
from pddl.domain_time_spec import TIME_SPEC
        

class EFFECT_TYPE(Enum):
    ADD     = "add"
    DELETE  = "delete"
    NUMERIC = "numeric"


class Effect:
    """
    This class describes an effect for an instant action.
    """

    def __init__(self, effect_type : EFFECT_TYPE, proposition : Union[DomainFormula,DomainAssignment]) -> None:
        self.effect_type = effect_type
        self.proposition = proposition

    def __repr__(self) -> str:
        if self.effect_type == EFFECT_TYPE.ADD:
            return str(self.proposition)
        else:
            return "(not " + str(self.proposition) + ")"


class TimedEffect(Effect):
    """
    This class describes a simple add or delete effect with time specifier for durative action.
    """

    def __init__(self, time_spec : TIME_SPEC, effect_type : EFFECT_TYPE, proposition : Union[DomainFormula,DomainAssignment]) -> None:
        super().__init__(effect_type, proposition)
        self.time_spec = time_spec

    def __repr__(self) -> str:
        return "(" + self.time_spec.value + " " + str(self.effect) + ")"