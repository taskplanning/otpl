from enum import Enum
from typing import List, Union
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.goal_descriptor_inequality import Inequality
from pddl.time_spec import TimeSpec


class Duration:
    """
    A class used to represent a domain duration.
    Sub-types represent one of the following types:
    - empty ()
    - conjunction (and duration_constraint duration_constraint ...)
    - inequality (comparison_op ?duration expression)
    - timed inequality (at end (comparison_op ?duration expression))
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

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Duration':
        """
        Binds the parameters of a copy of the duration to the given list of parameters.
        """
        return Duration()


class DurationInequality(Duration):
    """
    Duration such as (comparison_op ?duration expression)
    """
    def __init__(self, inequality : Inequality) -> None:
        super().__init__(Duration.DurationType.INEQUALITY)
        self.ineq = inequality

    def __repr__(self) -> str:
        return repr(self.ineq)
  
    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Duration':
        return DurationInequality(self.ineq.bind_parameters(parameters))

class DurationTimed(Duration):
    """
    Duration such as (at end (comparison_op ?duration expression))
    """

    def __init__(self, time_spec : TimeSpec, inequality : Inequality) -> None:
        super().__init__(Duration.DurationType.TIMED)
        self.time_spec = time_spec
        self.ineq = inequality

    def __repr__(self) -> str:
        return '(' + self.time_spec + ' ' + repr(self.ineq) + ')'

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Duration':
        return DurationTimed(self.time_spec, self.ineq.bind_parameters(parameters))

class DurationConjunction(Duration):
    """
    Duration such as (and duration_constraint duration_constraint ...)
    """
    def __init__(self, constraints : List[Union[DurationInequality,DurationTimed]] = []) -> None:
        super().__init__(Duration.DurationType.CONJUNCTION)
        self.constraints = constraints

    def __repr__(self) -> str:
        return '(and\n  ' + '\n  '.join(repr(c) for c in self.constraints) + '\n)'

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Duration':
        bound_contraints = [ dur.bind_parameters(parameters) for dur in self.constraints ]
        return DurationConjunction(bound_contraints)