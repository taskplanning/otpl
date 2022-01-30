from enum import Enum
from typing import List, Union
from pddl.domain_formula import DomainFormula
from pddl.domain_inequality import DomainInequality
from pddl.domain_time_spec import TIME_SPEC

class DomainDuration:
    """
    A class used to represent a domain duration.
    Sub-types represent one of the following types:
    - empty ()
    - conjunction (and ...)
    - inequality (> ?duration expression)
    - timed inequality (at end (> ?duration expression))
    """

    class DurationType(Enum):
        EMPTY       = "unconstrained"
        CONJUNCTION = "conjunction"
        INEQUALITY  = "inequality"
        TIMED       = "timed"

    def __init__(self, duration_type : DurationType = DurationType.EMPTY) -> None:
        self.duration_type = duration_type

    def __repr__(self) -> str:
        return "()"


class DomainDurationInequality(DomainDuration):

    def __init__(self, inequality : DomainInequality) -> None:
        super().__init__(DomainDuration.DurationType.INEQUALITY)
        self.ineq = inequality

    def __repr__(self) -> str:
        return repr(self.ineq)


class DomainDurationTimed(DomainDuration):

    def __init__(self, time_spec : TIME_SPEC, inequality : DomainInequality) -> None:
        super().__init__(DomainDuration.DurationType.TIMED)
        self.time_spec = time_spec
        self.ineq = inequality

    def __repr__(self) -> str:
        return '(' + self.time_spec + ' ' + repr(self.ineq) + ')'


class DomainDurationConjunction(DomainDuration):

    def __init__(self, constraints : List[Union[DomainDurationInequality,DomainDurationTimed]] = []) -> None:
        super().__init__(DomainDuration.DurationType.CONJUNCTION)
        self.constraints = constraints

    def __repr__(self) -> str:
        return '(and\n  ' + '\n  '.join(repr(c) for c in self.constraints) + '\n)'
