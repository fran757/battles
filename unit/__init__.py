from random import random
from dataclasses import dataclass
import numpy as np

from tools import tools
from delay import delay

from .base import UnitBase
from .field import UnitField
from .strategy import Strategy


# todo: delay is broken


@dataclass(init=False)
class Unit(UnitBase, UnitField, Strategy):

    def __init__(self, base, field, strategy):
        for prototype in (base, field, strategy):
            for name in prototype.__dataclass_fields__:
                setattr(self, name, getattr(prototype, name))

    def decide(self, all_units):
        others = [unit for unit in all_units if not unit.is_dead]
        allies = list(filter(self.is_ally, others))
        enemies = list(filter(self.is_enemy, others))

        if not enemies or self.is_dead:
            return delay(lambda: None)()

        action = (self.flee if self.is_fleeing else self.focus)(enemies)
        return action + self.moral_update(allies, enemies)

    @delay
    def focus(self, enemies):
        def criteria(other):
            close = self.closer * self.distance(other)
            weak = self.weaker * other.health
            return close + weak

        target = sorted(enemies, key=criteria)[0]
        assert target is not self

        if self.distance(target) <= self.reach:
            self.attack(target)
        self.move(self.direction(target.coords))

    @delay
    def flee(self, enemies):
        self.adrenaline()

        self.time_fleeing += 1
        if self.time_fleeing == 5:
            self.health = 0

        barycenter = [np.mean([e.coords[i] for e in enemies]) for i in (0, 1)]
        self.move(-self.direction(barycenter))

    @delay
    def moral_update(self, allies, enemies):
        for ally in allies:
            if ally.is_centurion and self.distance(ally) < 5:
                self.reset_braveness()
                break

        @tools(cache=True)
        def distance_to_enemies(unit):
            return sum(map(unit.distance, enemies))

        remote = distance_to_enemies(self)
        remote_side = list(map(distance_to_enemies, allies)) + [remote]
        coeff = sorted(remote_side).index(remote) / len(remote_side)
        m_1 = int(5 * (1 - 3 * coeff))
        coeff_2 = len(allies) / len(enemies)
        m_2 = int(5 * ((3 / 2) * coeff_2 - 1))
        self.change_moral(m_1 + m_2)

    def attack(self, target):
        target.health -= self.strength

    def move(self, direction):
        self.coords += self.speed * direction

    def adrenaline(self):
        if random() < .1:
            self.reset_braveness()
            self.speed *= 2
            self.strength *= 2
