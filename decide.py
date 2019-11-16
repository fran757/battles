"""Different methods for decision taking :
   Unit-specific filter methods
       -> maybe change to instance method, or too much clutter ?
   Strategies and helpful methods
"""
from numpy import linalg as LA
from delay import delay


def enemy_of(unit):
    """Filter enemies."""

    def is_enemy(other):
        return other.side != unit.side

    return is_enemy


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


def strategy(action):
    """If alone, do nothing. (decorator)"""

    def order(unit, others):
        if not others or unit.is_dead:
            return delay(lambda: None)
        return action(unit, others)

    return order


@strategy
def target_closest(unit, others):
    """'Focus' on closest enemy (if none just be idle)."""
    enemies = list(filter(enemy_of(unit), others))
    if not enemies:
        return delay(lambda: None)
    closest = sorted(enemies, key=distance_from(unit))[0]
    return focus(unit, closest)


@strategy
def target_weakest(unit, others):
    """'Focus' on weakest enemy (if none just be idle)."""
    # todo: target closest among the weakest
    enemies = list(filter(enemy_of(unit), others))
    if not enemies:
        return delay(lambda: None)
    weakest = sorted(enemies, key=lambda unit: unit.health)[0]
    return focus(unit, weakest)


# todo: blocking, fleeing, teaming up...
