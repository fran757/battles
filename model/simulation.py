"""Container and controller for successive battle steps."""
from copy import deepcopy
from dataclasses import dataclass
from typing import List
import numpy as np

from tools import tools

from .army import Army


@dataclass
class Simulation:
    """Container for successive steps of a battle."""
    states: List[List[Army]]

    @property
    def size(self):
        """Length of battle (number of steps)."""
        return len(self.states)

    def units(self, i):
        """Accessor for a specific state (step number i)."""
        units = []
        for side in self.states[i]:
            units += side.units
        return units

    def state(self, i):
        """Provide both sides of given battle state."""
        return self.states[i]

    @property
    def volume(self):
        """Total health on each side."""
        return [s.health for s in self.states[-1]]

    @tools(clock=True, log="Armies' health: {self.volume}")
    def update(self):
        """Generate and append new state to simulation."""
        if self.is_finished:
            return None
        new_state = deepcopy(self.states[-1])
        self.states.append(new_state)

        ways = new_state, reversed(new_state)
        sum([army.decide(enemy) for army, enemy in zip(*ways)], None)()
        return self.states[-1]

    @property
    def is_finished(self):
        """Tell whether the battle is over (one side has no health)."""
        return not np.all(self.volume)
