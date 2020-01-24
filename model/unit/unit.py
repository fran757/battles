from random import random
import numpy as np

from tools import tools

from .order import delay
from .base import UnitBase
from .field import UnitField
from .strategy import Strategy


class Unit(UnitBase, UnitField, Strategy):
    """Complete unit, adding decision-taking logic."""

    def __init__(self, base, field, strategy):
        """Build unit from component prototypes."""
        for prototype in (base, field, strategy):
            for name, dfield in prototype.__dataclass_fields__.items():
                value = getattr(prototype, name)
                if not isinstance(value, dfield.type):
                    tools(log=f"wrong type: {name}, {dfield.type}, {value}")()
                setattr(self, name, value)

    @tools(clock=True)
    def decide(self, info):
        """Take a decision based on all other units on the field.
        Flee or focus on an enemy, then update braveness."""
        if not info.enemies or self.is_dead:
            return delay(lambda: None)()

        action = self.moral_update(info.centurion, info.remote, info.ratio)
        if self.is_fleeing:
            action += self.flee(info.barycenter)
        else:
            action += self.focus(info.enemies)
        return action


    @tools(clock=True)
    def focus(self, enemies):
        """Choose targetted unit based on strategy parameters.
        If close enough attack, else move closer.
        """
        def criteria(other):
            close = self.closer * self.distance(other)
            weak = self.weaker * other.health
            strong = self.stronger * other.strength

            return close + weak + strong

        target = enemies[np.argmin(list(map(criteria, enemies)))]

        if self.distance(target) <= self.reach:
            return self.attack(target)
        return self.move(self.direction(target.coords))

    @tools(clock=True)
    def flee(self, enemy):
        """Run away, and maybe come back stronger."""
        return self.adrenaline() + self.move(-self.direction(enemy))

    @tools(clock=True)
    def moral_update(self, centurion, remote, ratio):
        """If a centurion is close, be brave.
        Puss out if enemies are far.
        """
        if centurion is not None and self.distance(centurion) < 5:
            return delay(self.reset_braveness)()

        m_1 = int(5 * (1 - 3 * remote))
        m_2 = int(5 * ((3 / 2) * ratio))
        return delay(self.change_moral)(m_1 + m_2)

    @delay
    def attack(self, target):
        target.health -= self.strength

    @delay
    def move(self, direction):
        self.coords += self.speed * direction

    @delay
    def adrenaline(self):
        """If lucky, get a burst of adrenaline, otherwise stay fleeing."""
        if random() < .1:
            self.reset_braveness()
            self.speed *= 2
            self.strength *= 2
        else:
            self.time_fleeing += 1
            if self.time_fleeing == 5:
                self.health = 0
