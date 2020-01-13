"""Different methods for decision taking :
   Unit-specific filter methods
       -> maybe change to instance method, or too much clutter ?
   Strategies and helpful methods
"""
from numpy import linalg as LA

from tools.cache import cache
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
        return LA.norm(other.coords - unit.coords)

    return distance


def direction(unit, other):
    """Orientation towards other unit."""
    delta = other.coords - unit.coords
    return delta / LA.norm(delta)


def focus(unit, target):
    """Focus on one specific enemy.
    If within reach attack, otherwise approach.
    """
    if distance_from(unit)(target) <= unit.reach:
        return unit.attack(target)
    return unit.move(direction(unit, target))


def find_centurion(allies):
    for ally in allies:
        if ally.is_centurion and not ally.is_dead:
            return True, ally
    return [False]


def is_close_from_centurion(unit, centurion, threshold):
    if LA.norm(unit.coords - centurion.coords) < threshold:
        return True
    return False


def burst_of_braveness(unit):
    p = random.random()
    if p < 0.1:
        unit.reset_braveness()
        unit.speed = 2**unit.speed
        unit.strength *= 2


def moral_damage(unit, allies, enemies, search_result):
    """Units take moral damage at every step, their braveness decreases."""
    if unit.braveness == 0:
        burst_of_braveness(unit)
        unit.time_fleeing += 1
        if unit.time_fleeing == 5:
            unit.health = 0

    @cache
    def distance_to_enemies(_unit):
        return sum(distance_from(_unit)(enemy) for enemy in enemies)
    remote = distance_to_enemies(unit)
    remote_allies = [distance_to_enemies(ally) for ally in allies] + [remote]
    sorted_remote_allies = sorted(remote_allies)
    index = sorted_remote_allies.index(remote)
    if search_result[0]:  # there is a centurion
        centurion = search_result[1]
        if is_close_from_centurion(unit, centurion, 7):
            return unit.reset_braveness()
    return unit.moral_damage(10)


def do_something(unit, target, enemies):
    if unit.braveness == 0:
        @cache
        def barycenter(enemies):
            """finding barycenter of enemy units"""
            nb_enemies = len(enemies)
            x_bar = (1/nb_enemies)*sum(enemy.coords[0] for enemy in enemies)
            y_bar = (1/nb_enemies)*sum(enemy.coords[1] for enemy in enemies)
            return [x_bar, y_bar]
        dir_to_bar = (barycenter(enemies)-unit.coords) / \
            LA.norm(barycenter(enemies)-unit.coords)
        return unit.move(-dir_to_bar)
    else:
        if distance_from(unit)(target) <= unit.reach:
            return unit.attack(target)
        return unit.move(direction(unit, target))


def strategy(distance=0, health=0):
    """Order are based on preference between proximity and weakness."""

    def order(unit, all_units):
        others = [unit for unit in all_units if not unit.is_dead]
        allies = list(filter(ally_of(unit), others))
        enemies = list(filter(enemy_of(unit), others))
        search_result = find_centurion(allies)
        if not enemies or unit.is_dead:
            return delay(lambda: None)()

        def criteria(other):
            return distance * distance_from(unit)(other) + health * other.health

        target = sorted(enemies, key=criteria)[0]

        return do_something(unit, target, enemies) + moral_damage(unit, allies, enemies, search_result)

    return order


# todo: blocking, fleeing, teaming up...
