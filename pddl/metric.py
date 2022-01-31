from enum import Enum
from pddl.domain_expression import ExprComposite


class MetricSpec(Enum):
    MIN = "minimize"
    MAX = "maximize"


class Metric:

    def __init__(self, metric_spec : MetricSpec, expression : ExprComposite) -> None:
        self.metric_spec = metric_spec
        self.expression = expression

    def __repr__(self) -> str:
        return "(:metric " + self.metric_spec.value + " " + repr(self.expression) + ")"