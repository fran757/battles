from dataclasses import dataclass
import numpy as np


@dataclass
class UnitField:
    """Unit on the field."""
    side: int
    coords: np.ndarray
    is_centurion: bool
    braveness: int = 100
    time_fleeing: int = 0

    @property
    def is_fleeing(self):
        return self.braveness <= 0

    def is_enemy(self, other):
        return other is not self and other.side != self.side

    def is_ally(self, other):
        return other is not self and other.side == self.side

    def distance(self, other):
        return np.linalg.norm(other.coords - self.coords)

    def direction(self, target):
        delta = target - self.coords
        if all(delta == 0):
            return np.zeros(2)
        return delta / np.linalg.norm(delta)

    def reset_braveness(self):
        self.braveness = 100
        self.time_fleeing = 0

    def change_moral(self, value):
        self.braveness += value
