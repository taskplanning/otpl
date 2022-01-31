"""
This file defines and implements the basic effects for PDDL2.2.
The implementation of assignment goals is implemented in DomainAssignment.
"""
from typing import List, Union
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

class EffectConjunction(Effect):

    def __init__(self, effects : List[Effect]) -> None:
        super().__init__(effect_type=EffectType.CONJUNCTION)
        self.effects = effects

    def __repr__(self) -> str:
        return "(and " + " ".join([repr(e) for e in self.effects]) + ")"

class EffectForall(Effect):

    def __init__(self, 
            typed_parameters : List[TypedParameter],
            effect : Effect,
            ) -> None:
        super().__init__(effect_type=EffectType.FORALL)
        self.typed_parameters = typed_parameters
        self.effect = effect

    def __repr__(self) -> str:
        return "(forall (" \
            + ' '.join([p.label + " - " + p.type for p in self.typed_parameters]) \
            + ") " + repr(self.effect) + ")"


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

class EffectSimple(Effect):

    def __init__(self, formula : AtomicFormula) -> None:
        super().__init__(effect_type=EffectType.SIMPLE)
        self.formula = formula

    def __repr__(self) -> str:
        return self.formula.print_pddl()

class EffectNegative(EffectSimple):

    def __init__(self, formula : AtomicFormula) -> None:
        super().__init__(formula)
        self.effect_type = EffectType.NEGATIVE

    def __repr__(self) -> str:
        return "(not " + self.formula.print_pddl() + ")"


class TimedEffect(Effect):

    def __init__(self, time_spec : TimeSpec, effect : Effect) -> None:
        super().__init__(effect_type=EffectType.TIMED)
        self.time_spec = time_spec
        self.effect = effect

    def __repr__(self) -> str:
        return "(" + self.time_spec.value + " " + str(self.effect) + ")"