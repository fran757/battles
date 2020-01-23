from dataclasses import dataclass
from typing import List
import numpy as np

from .field import UnitField
from tools import tools


@dataclass
class Info:
    leader: "Unit"
    remote: float
    ratio: float
    barycenter: np.ndarray
    enemies: List["Unit"]  # todo: just give target ?


class Centurion(UnitField):
    def __init__(self, units):
        self.units = units
        self._coords = None

    @property
    def health(self):
        return sum([unit.health for unit in self.units])

    @tools(clock=True)
    def distance(self, other):
        """Distance to other unit."""
        return np.linalg.norm(other.coords - self.coords)

    @property
    def coords(self):
        if self._coords is None:
            self._coords = np.mean([u.coords for u in self.units], 0)
        return self._coords

    @tools(clock=True)
    def decide(self, enemy):
        dist = enemy.distance(self)
        tools(log=f"{dist}")()

        leader = None
        for unit in self.units:
            if unit.is_centurion:
                leader = unit
                break
        ranked = sorted(self.units, key=enemy.distance)
        ratio = len(self.units) / len(enemy.units)
        enemies = [u for u in enemy.units if not u.is_dead]
        action = None

        for rank, unit in enumerate(ranked):
            remote = rank / len(ranked)
            info = Info(leader, remote, ratio, enemy.coords, enemies)
            action += unit.decide(info)
        self._coords = None
        return action
