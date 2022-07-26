from enum import Enum
from pddl.atomic_formula import TypedParameter
from pddl.expression import ExprComposite

class MetricSpec(Enum):
    MIN = "minimize"
    MAX = "maximize"

class Metric:

    def __init__(self, metric_spec : MetricSpec, expression : ExprComposite) -> None:
        self.metric_spec = metric_spec
        self.expression = expression

    def __repr__(self) -> str:
        return "(:metric " + self.metric_spec.value + " " + repr(self.expression) + ")"

    def copy(self) -> 'Metric':
        """
        Returns a deep copy of the metric.
        """
        return Metric(self.metric_spec, self.expression.copy())

    def bind_parameters(self, parameters: list[TypedParameter]) -> 'Metric':
        """
        Binds the parameters of the metric to the given parameters.
        """
        return Metric(self.metric_spec, self.expression.bind_parameters(parameters))