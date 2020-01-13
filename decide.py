"""Different methods for decision taking :
   Unit-specific filter methods
       -> maybe change to instance method, or too much clutter ?
   Strategies and helpful methods
"""
import numpy as np

from tools import tools
from delay import delay

import random


def enemy_of(unit):
    """Filter enemies."""

    def is_enemy(other):
        return other is not unit and other.side != unit.side

    return is_enemy


def ally_of(unit):
    """Filter allies."""

    def is_ally(other):
        return other is not unit and other.side == unit.side

    return is_ally


def distance_from(unit):
    """Filter distances."""

    def distance(other):
        return np.linalg.norm(other.coords - unit.coords)

    return distance


def direction(unit, target):
    """Orientation from unit towards given point."""
    delta = target - unit.coords
    return delta / np.linalg.norm(delta)


def focus(unit, enemies, criteria):
    """Focus on one specific enemy.
    If within reach attack, otherwise approach.
    """
    target = sorted(enemies, key=criteria)[0]

    if distance_from(unit)(target) <= unit.reach:
        return unit.attack(target)
    return unit.move(direction(unit, target.coords))


def find_centurion(allies):
    """Find living centurion among allies, if present."""
    for ally in allies:
        if ally.is_centurion and not ally.is_dead:
            return ally
    return None


def burst_of_braveness(unit):
    """Boost unit stats and restore braveness, under a certain probability."""
    if random.random() < 0.1:
        unit.reset_braveness()
        unit.speed *= 2
        unit.strength *= 2


def moral_damage(unit, allies, enemies, centurion):
    """Units take moral damage at every step, decreasing their braveness."""
    if unit.braveness == 0:
        burst_of_braveness(unit)
        unit.time_fleeing += 1
        if unit.time_fleeing == 5:
            unit.health = 0

    if centurion is not None and distance_from(unit, centurion) < 5:
        return unit.reset_braveness()

    @tools(cache=True)
    def distance_to_enemies(_unit):
        return sum(distance_from(_unit)(enemy) for enemy in enemies)

    remote = distance_to_enemies(unit)
    remote_allies = [distance_to_enemies(ally) for ally in allies] + [remote]
    coeff = sorted(remote_allies).index(remote) / len(remote_allies)
    m_1 = int(5 * (1 - 3 * coeff))
    coeff_2 = len(allies) / len(enemies)
    m_2 = int(5 * ((3 / 2) * coeff_2 - 1))
    return unit.moral_update(m_1 + m_2)


def flee(unit, enemies):
    def barycenter(enemies):
        """Find barycenter of enemy units."""
        return [np.mean([e.coords[i] for e in enemies]) for i in (0, 1)]

    dir_to_bar = direction(unit, barycenter(enemies))
    return unit.move(-dir_to_bar)


def do_something(unit, enemies, criteria):
    if unit.braveness == 0:
        return flee(unit, enemies)
    else:
        return focus(unit, enemies, criteria)


def strategy(distance=0, health=0):
    """Order are based on preference between proximity and weakness."""

    @tools(clock=True)
    def order(unit, all_units):
        others = [unit for unit in all_units if not unit.is_dead]
        allies = list(filter(ally_of(unit), others))
        enemies = list(filter(enemy_of(unit), others))
        centurion = find_centurion(allies)
        if not enemies or unit.is_dead:
            return delay(lambda: None)()

        def criteria(other):
            close = distance * distance_from(unit)(other)
            weak = health * other.health
            return close + weak


        action = do_something(unit, enemies, criteria)
        moral = moral_damage(unit, allies, enemies, centurion)
        return action + moral

    return order
