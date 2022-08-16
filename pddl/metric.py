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

    def visit(self, visit_function: callable, valid_types: tuple[type] = None, args=(), kwargs={}) -> None:
        """
        Calls the given visit function on the metric expression.
        param visit_function: The function to call.
        param valid_types: A set of types to visit. If None, all types are visited.
        """
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        self.expression.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters: list[TypedParameter]) -> 'Metric':
        """
        Binds the parameters of the metric to the given parameters.
        """
        return Metric(self.metric_spec, self.expression.bind_parameters(parameters))