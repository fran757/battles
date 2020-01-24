"""Run and manage simulations, file I/O."""
from copy import deepcopy
from dataclasses import dataclass
from typing import List
import numpy as np

from model import Factory, Unit, UnitBase, UnitField, Strategy, Army
from tools import tools, Bar


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
        self.states.append(deepcopy(self.states[-1]))
        side1, side2 = self.states[-1]  # todo: clean this up
        (side1.decide(side2) + side2.decide(side1))()
        return self.states[-1]

    @property
    def is_finished(self):
        """Tell whether the battle is over (one side has no health)."""
        return not np.all(self.volume)
