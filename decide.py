"""Different methods for decision taking :
   Unit-specific filter methods
       -> maybe change to instance method, or too much clutter ?
   Strategies and helpful methods
"""
from numpy import linalg as LA

from tools.cache import cache
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

def moral_damage(unit, enemies):
    """Units take moral damage at every step,
    their braveness decreases"""
    if unit.braveness == 0:
        return
    else:
        return unit.moral_damage(2)

def flee(unit, enemies):
    """Units with 0 braveness try to escape from
    the closest enemy"""
    if not enemies or unit.braveness != 0:
        return

    if unit.braveness == 0:
        @cache
        def closest_enemy(_unit):
            _closest_enemy = enemies[0]
            for enemy in enemies[1:]:
                if distance_from(_unit)(enemy) < distance_from(_unit)(_closest_enemy):
                    if (enemy.coords != unit.coords).any() and not enemy.is_dead:
                        _closest_enemy = enemy
                return _closest_enemy
        enemy_to_flee = closest_enemy(unit)
        print("enemy_to_flee coords")
        print(enemy_to_flee.coords)
        print("unit coords")
        print(unit.coords)
        return unit.move(-direction(unit, enemy_to_flee))

def strategy(distance=0, health=0):
    """Order are based on preference between proximity and weakness."""

    def order(unit, all_units):
        others = [unit for unit in all_units if not unit.is_dead]
        allies = list(filter(ally_of(unit), others))
        enemies = list(filter(enemy_of(unit), others))
        if not enemies or unit.is_dead:
            return delay(lambda: None)()

        def criteria(other):
            return distance * distance_from(unit)(other) + health * other.health

        target = sorted(enemies, key=criteria)[0]


        return focus(unit, target) + moral_damage(unit, enemies)

    return order


# todo: blocking, fleeing, teaming up...
