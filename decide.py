"""Different methods for decision taking :
   Unit-specific filter methods
       -> maybe change to instance method, or too much clutter ?
   Strategies and helpful methods
"""
from numpy import linalg as LA
from delay import delay
import copy


def enemy_of(unit):
    """Filter enemies."""

    def is_enemy(other):
        return other.side != unit.side

    return is_enemy


def ally_of(unit):
    """Filter allies."""
    def is_ally(other):
        return other.side == unit.side

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


def focus(unit, target, fleeing_prob):
    """Focus on one specific enemy.
    If within reach attack, otherwise approach.
    """
    unit.flee(fleeing_prob)

    if distance_from(unit)(target) <= unit.reach:
        return unit.attack(target)
    return unit.move(direction(unit, target))


def has_coward(unit, allies, enemies):
    """Return true if this unit may have
    fleeing individuals, false else"""
    dis = sum(distance_from(unit)(enemy)
              for enemy in enemies if not enemy.is_dead)
    dis_allies = sum(sum(distance_from(ally)(enemy)
                      for enemy in enemies if not enemy.is_dead) for ally in allies)
    return 2*dis/dis_allies


def strategy(distance=0, health=0):
    """Order are based on preference between proximity and weakness."""
    def order(unit, others):
        others2 = copy.deepcopy(others)
        allies = list(filter(ally_of(unit), others))
        enemies = list(filter(enemy_of(unit), others2))
        if not enemies or unit.is_dead:
            return delay(lambda: None)

        def criteria(other):
            return distance * distance_from(unit)(other) + health * unit.health
        # todo: normalization

        target = sorted(enemies, key=criteria)[0]
        return focus(unit, target, has_coward(unit, allies, enemies))

    return order


# todo: blocking, fleeing, teaming up...
