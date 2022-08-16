
import numpy as np


class State:

    def __init__(self, time : float = 0, logical : np.ndarray = None, numeric : np.ndarray = None) -> None:
        self.time = time
        self.logical = logical if logical is not None else np.zeros(0, dtype=bool)
        self.numeric = numeric if numeric is not None else np.zeros(0, dtype=float)

    def copy(self) -> 'State':
        return State(self.time, self.logical.copy(), self.numeric.copy())