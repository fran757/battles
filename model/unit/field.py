from dataclasses import dataclass
import numpy as np

from tools import tools


@dataclass
class UnitField:
    """In-situ unit stats container and modyfiers."""
    side: int
    coords: np.ndarray
    is_centurion: bool = False

    def is_enemy(self, other):
        return other is not self and other.side != self.side

    def is_ally(self, other):
        return other is not self and other.side == self.side

    @tools(clock=True)
    def distance(self, other):
        """Distance to other unit."""
        return np.linalg.norm(other.coords - self.coords)

    def direction(self, target):
        delta = target - self.coords
        if all(delta == 0):
            return np.zeros(2)
        return delta / np.linalg.norm(delta)
