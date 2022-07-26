from pddl.effect import EffectSimple


class TimedInitialLiteral:

    def __init__(self, time : float, effect : EffectSimple) -> None:
        self.time = time
        self.effect = effect

    def __repr__(self) -> str:
        return "(at " + str(self.time) + " " + repr(self.effect) + ")"

    def print_pddl(self, current_time : float) -> str:
        assert(current_time <= self.time)
        return "(at " + str(self.time - current_time) + " " + repr(self.effect) + ")"

    def copy(self) -> "TimedInitialLiteral":
        return TimedInitialLiteral(self.time, self.effect.copy())