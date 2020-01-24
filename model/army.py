from dataclasses import dataclass
from typing import List
import numpy as np

from .field import UnitField
from tools import tools


@dataclass
class Info:
    """Information container for unit decision-taking,
    passed by centurion to his suboordinates.
    """
    centurion: "Unit"
    remote: float
    ratio: float
    barycenter: np.ndarray
    enemies: List["Unit"]  # todo: just give target ?


class Army(UnitField):
    """Abstract unit controlling an army, for computing centralization."""
    def __init__(self, units):
        self.units = units
        self._coords = None

    @property
    def health(self):
        """Total health of army."""
        return sum([unit.health for unit in self.units])

    @property
    def coords(self):
        """Barycenter of suboordinate units."""
        if self._coords is None:
            self._coords = np.mean([u.coords for u in self.units], 0)
        return self._coords

    @tools(clock=True)
    def decide(self, enemy):
        """Compute useful info and pass it to each unit's decision logic."""
        dist = enemy.distance(self)
        # tools(log=f"{dist:.3}")()

        centurion = None
        for unit in self.units:
            if unit.is_centurion:
                centurion = unit
                break
        ranked = sorted(self.units, key=enemy.distance)
        ratio = len(self.units) / len(enemy.units)
        enemies = [u for u in enemy.units if not u.is_dead]
        action = None

        for rank, unit in enumerate(ranked):
            remote = rank / len(ranked)
            info = Info(centurion, remote, ratio, enemy.coords, enemies)
            action += unit.decide(info)
        self._coords = None
        return action
