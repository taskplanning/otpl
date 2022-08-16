"""
This file defines and implements the basic effects for PDDL2.2.
The implementation of assignment goals is implemented in DomainAssignment.
"""
from enum import Enum
from pddl.goal_descriptor import GoalDescriptor
from pddl.expression import ExprComposite
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.time_spec import TimeSpec
        

class EffectType(Enum):
    EMPTY       = "empty"
    CONJUNCTION = "conjunction"
    FORALL      = "forall"
    CONDITIONAL = "conditional"
    SIMPLE      = "add"
    NEGATIVE    = "delete"
    ASSIGN      = "numeric"
    TIMED       = "timed"
    CONTINUOUS  = "continuous"

class Effect:

    def __init__(self, effect_type : EffectType = EffectType.EMPTY) -> None:
        self.effect_type = effect_type

    def __repr__(self) -> str:
        return "()"

    def copy(self) -> 'Effect':
        """
        Returns a deep copy of the effect.
        """
        return Effect()

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        """
        Calls the visit function on self and recurses through the visit methods of members.
        param visit_function: the function to call on self.
        param valid_types: a set of types to visit. If None, all types are visited.
        """
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Effect':
        """
        Binds the parameters of a copy of the effect to the given list of parameters.
        """
        return Effect()

    def filter_effects_to_time_spec(self, time_spec : TimeSpec) -> 'Effect':
        """
        Filters the effects to the given time spec.
        """
        return self

class EffectConjunction(Effect):

    def __init__(self, effects : list[Effect]) -> None:
        super().__init__(effect_type=EffectType.CONJUNCTION)
        self.effects = effects

    def __repr__(self) -> str:
        return "(and " + " ".join([repr(e) for e in self.effects]) + ")"

    def copy(self) -> 'Effect':
        """
        Returns a deep copy of the effect.
        """
        return EffectConjunction([e.copy() for e in self.effects])

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        for e in self.effects:
            e.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Effect':
        return EffectConjunction([e.bind_parameters(parameters) for e in self.effects])

    def filter_effects_to_time_spec(self, time_spec : TimeSpec) -> 'Effect':
        effects = [e.filter_effects_to_time_spec(time_spec) for e in self.effects]
        return EffectConjunction([e for e in effects if e])

class EffectForall(Effect):

    def __init__(self, 
            typed_parameters : list[TypedParameter],
            effect : Effect,
            ) -> None:
        super().__init__(effect_type=EffectType.FORALL)
        self.typed_parameters = typed_parameters
        self.effect = effect

    def __repr__(self) -> str:
        return "(forall (" \
            + ' '.join([p.label + " - " + p.type for p in self.typed_parameters]) \
            + ") " + repr(self.effect) + ")"

    def copy(self) -> 'Effect':
        """
        Returns a deep copy of the effect.
        """
        params = [ TypedParameter(p.type, p.label, p.value) for p in self.typed_parameters ]
        return EffectForall(params, self.effect.copy())

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        for p in self.typed_parameters:
            p.visit(visit_function, valid_types, args, kwargs)
        self.effect.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Effect':
        """
        Binds the unquantified parameters of the effect to the given list of parameters.
        """
        return EffectForall(self.typed_parameters, self.effect.bind_parameters(parameters))


class EffectConditional(Effect):

    def __init__(self, 
            condition : GoalDescriptor,
            effect : Effect,
            ) -> None:
        super().__init__(effect_type=EffectType.CONDITIONAL)
        self.condition = condition
        self.effect = effect

    def __repr__(self) -> str:
        return "(when " + repr(self.condition) + " " + repr(self.effect) + ")"

    def copy(self) -> 'Effect':
        """
        Returns a deep copy of the effect.
        """
        return EffectConditional(self.condition.copy(), self.effect.copy())

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        self.condition.visit(visit_function, valid_types, args, kwargs)
        self.effect.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Effect':
        return EffectConditional(self.condition.bind_parameters(parameters), self.effect.bind_parameters(parameters))

class EffectSimple(Effect):

    def __init__(self, formula : AtomicFormula) -> None:
        super().__init__(effect_type=EffectType.SIMPLE)
        self.formula = formula

    def __repr__(self) -> str:
        return self.formula.print_pddl()

    def copy(self) -> 'Effect':
        """
        Returns a deep copy of the effect.
        """
        return EffectSimple(self.formula.copy())

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        self.formula.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Effect':
        return EffectSimple(self.formula.bind_parameters(parameters))

class EffectNegative(EffectSimple):

    def __init__(self, formula : AtomicFormula) -> None:
        super().__init__(formula)
        self.effect_type = EffectType.NEGATIVE

    def __repr__(self) -> str:
        return "(not " + self.formula.print_pddl() + ")"

    def copy(self) -> 'Effect':
        """
        Returns a deep copy of the effect.
        """
        return EffectNegative(self.formula.copy())

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Effect':
        return EffectNegative(self.formula.bind_parameters(parameters))

class TimedEffect(Effect):

    def __init__(self, time_spec : TimeSpec, effect : Effect) -> None:
        super().__init__(effect_type=EffectType.TIMED)
        self.time_spec = time_spec
        self.effect = effect

    def __repr__(self) -> str:
        return "(" + self.time_spec.value + " " + str(self.effect) + ")"

    def copy(self) -> 'Effect':
        """
        Returns a deep copy of the effect.
        """
        return TimedEffect(self.time_spec, self.effect.copy())

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        self.effect.visit(visit_function, valid_types, args, kwargs)

    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Effect':
        return TimedEffect(self.time_spec, self.effect.bind_parameters(parameters))

    def filter_effects_to_time_spec(self, time_spec : TimeSpec) -> 'Effect':
        if time_spec == self.time_spec:
            return self.effect
        return None