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
            action += self.focus(info.enemies, info.sum_health, info.sum_distances)
        return action


    @tools(clock=True)
    def focus(self, enemies, sum_health, sum_distances):
        """Choose targetted unit based on strategy parameters.
        If close enough attack, else move closer.
        """
        def criteria(other):
            close = self.closer * other.distance(self)/sum_distances
            weak = self.weaker * other.health/sum_health

            return close + weak

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
        if centurion is not None and self.distance(centurion) < 3:
            return delay(self.reset_braveness)()
        a_1 = 15 # Moral damage taken by the furthest unit from the enemies
        b_1 = 10 # Moral increase for the closest unit from the enemies
        m_1 = int(-(a_1 + b_1) * remote + b_1)
        a_2 = 15 # Moral damage is enemy army is way larger
        b_2 = 10 # Moral increase if enemy army is way smaller
        m_2 = int(a_2 - (a_2 + b_2) * (a_2/(a_2 + b_2))**ratio)
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
        if random() < .07:
            self.reset_braveness()
            self.speed *= 2
            self.strength *= 2
        else:
            self.time_fleeing += 1
            if self.time_fleeing == 10:
                self.health = 0
