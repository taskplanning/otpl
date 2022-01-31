from pddl.domain_effect import EffectSimple


class TimedInitialLiteral:

    def __init__(self, time : float, effect : EffectSimple) -> None:
        self.time = time
        self.effect = effect

    def __repr__(self) -> str:
        return "(at " + str(self.time) + " " + repr(self.effect) + ")"