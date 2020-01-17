from random import random
import numpy as np

from tools import tools
from delay import delay

from .base import UnitBase
from .field import UnitField
from .strategy import Strategy


class Unit(UnitBase, UnitField, Strategy):
    """Complete unit, adding decision-taking logic."""

    def __init__(self, base, field, strategy):
        """Build unit from component prototypes."""
        for prototype in (base, field, strategy):
            for name, field in prototype.__dataclass_fields__.items():
                value = getattr(prototype, name)
                if not isinstance(value, field.type):
                    tools(log=f"{name}, {type(value)}, {value}")()
                setattr(self, name, value)

    def decide(self, all_units):
        """Take a decision based on all other units on the field.
        Flee or focus on an enemy, then update braveness."""
        others = [unit for unit in all_units if not unit.is_dead]
        allies = list(filter(self.is_ally, others))
        enemies = list(filter(self.is_enemy, others))

        if not enemies or self.is_dead:
            return delay(lambda: None)()

        action = (self.flee if self.is_fleeing else self.focus)(enemies)
        moral = self.moral_update(allies, enemies)
        return action + moral

    def focus(self, enemies):
        """Choose targetted unit based on strategy parameters.
        If close enough attack, else move closer.
        """
        def criteria(other):
            close = self.closer * self.distance(other)
            weak = self.weaker * other.health

            return close + weak

        target = sorted(enemies, key=criteria)[0]

        if self.distance(target) <= self.reach:
            return self.attack(target)
        return self.move(self.direction(target.coords))

    def flee(self, enemies):
        """Run away, and maybe come back stronger."""
        barycenter = [np.mean([e.coords[i] for e in enemies]) for i in (0, 1)]
        return self.adrenaline() + self.move(-self.direction(barycenter))

    def moral_update(self, allies, enemies):
        """If a centurion is close, be brave.
        Puss out if enemies are far.
        """
        for ally in allies:
            if ally.is_centurion and self.distance(ally) < 5:
                return delay(self.reset_braveness)()

        @tools(cache=True)
        def distance_to_enemies(unit):
            return sum(map(unit.distance, enemies))

        remote = distance_to_enemies(self)
        remote_side = list(map(distance_to_enemies, allies)) + [remote]
        coeff = sorted(remote_side).index(remote) / len(remote_side)
        m_1 = int(5 * (1 - 3 * coeff))  # todo: wth do these mean
        coeff_2 = len(allies) / len(enemies)
        m_2 = int(5 * ((3 / 2) * coeff_2 - 1))
        return delay(self.change_moral)(m_1 + m_2)

    @delay
    def attack(self, target):
        target.health -= self.strength

    @delay
    def move(self, direction):
        self.coords += self.speed * direction

    @delay
    def adrenaline(self):
        if random() < .1:
            self.reset_braveness()
            self.speed *= 2
            self.strength *= 2

        self.time_fleeing += 1
        if self.time_fleeing == 5:
            self.health = 0
