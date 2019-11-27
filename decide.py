"""Different methods for decision taking :
   Unit-specific filter methods
       -> maybe change to instance method, or too much clutter ?
   Strategies and helpful methods
"""
from numpy import linalg as LA

from cache import cache
from delay import delay


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


def has_coward(unit, allies, enemies):
    """Units further from the enemy might have fleeing issues.
    Return probability of such issues.
    """

    @cache
    def distance_to_enemies(_unit):
        return sum(distance_from(_unit)(enemy) for enemy in enemies)

    remote = distance_to_enemies(unit)
    remote_allies = sum(distance_to_enemies(ally) for ally in allies)
    return 2 * remote / remote_allies


def strategy(distance=0, health=0):
    """Order are based on preference between proximity and weakness."""

    def order(unit, others):
        allies = list(filter(ally_of(unit), others))
        enemies = list(filter(enemy_of(unit), others))
        if not enemies or unit.is_dead:
            return delay(lambda: None)()

        def criteria(other):
            return distance * distance_from(unit)(other) + health * unit.health

        # todo: normalization

        weakness = has_coward(unit, allies, enemies)
        target = sorted(enemies, key=criteria)[0]
        return focus(unit, target) + unit.flee(weakness)

    return order


# todo: blocking, fleeing, teaming up...
