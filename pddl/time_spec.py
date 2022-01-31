from enum import Enum


class TimeSpec(Enum):
    """
    An enumeration for durations, conditions, and effects of durative actions.
    """
    AT_START = "at start"
    OVER_ALL = "over all"
    AT_END   = "at end"