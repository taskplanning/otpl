from pddl.effect import Effect, EffectSimple, EffectType
from pddl.effect_assignment import Assignment, AssignmentType


class TimedInitialLiteral:

    def __init__(self, time : float, effect : EffectSimple) -> None:
        self.time = time
        self.effect = effect

    def __repr__(self) -> str:
        return "(at " + str(self.time) + " " + repr(self.effect) + ")"

    def print_pddl(self, current_time : float) -> str:
        assert(current_time <= self.time)
        return self._print_tils_from_effect(current_time, self.effect)

    def _print_tils_from_effect(self, current_time : float, effect : Effect) -> str:
        assert(current_time <= self.time)
        if effect.effect_type == EffectType.SIMPLE:
            return "(at {:0.2f} ".format(self.time - current_time) + repr(effect) + ")"
        elif effect.effect_type == EffectType.NEGATIVE:
            return "(at {:0.2f} ".format(self.time - current_time) + repr(effect) + ")"
        elif effect.effect_type == EffectType.CONJUNCTION:
            return_string = ""
            first = True
            for sub_effect in effect.effects:
                sub_string = self._print_tils_from_effect(current_time, sub_effect)
                if not first and sub_string != "":
                    return_string += "\n  "
                return_string += sub_string
                first = False
            return return_string
        elif effect.effect_type == EffectType.ASSIGN:
            # allow TIFs to be used in the initial state
            if effect.assign_type != AssignmentType.ASSIGN:
                return ""
            return "(at {:0.2f} ".format(self.time - current_time) + repr(effect) + ")"
        return ""

    def copy(self) -> "TimedInitialLiteral":
        return TimedInitialLiteral(self.time, self.effect.copy())

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}) -> None:
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
        self.effect.visit(visit_function, valid_types, args, kwargs)