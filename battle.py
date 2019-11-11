import random
from dataclasses import dataclass
from typing import List
import numpy as np

from decide import target_closest, target_weakest
from unit import Unit


@dataclass
class Battle:
    """Contain all units (no setter for adding units, just append).i
    Update method to take and enforce all decisions.
    String representation by integer grid approximation.
    """

    units: List[Unit]

    def __init__(self):
        self.units = []

    def update(self):
        """Make each unit take a decision, then enforce them."""
        actions = []
        for unit in self.units:
            others = filter(lambda other, self=unit: other is not self, self.units)
            actions.append(unit.decide(others))
        for action in actions:
            action()

    def __str__(self):
        """Print unit grid (rounded to integer positions).
        Grid size ajusted to unit max coords (should do min too).
        """

        def bound(axis, extr):
            return int(round(extr([unit.coords[axis] for unit in self.units]))) + 1

        width = bound(1, max)
        height = bound(0, max)
        grid = [["0" for _ in range(width)] for _ in range(height)]

        for unit in self.units:
            i, j = map(int, map(round, unit.coords))
            try:
                grid[i][j] = str(unit)
            except IndexError:
                message = f"Grid shape : {height} {width}\n"
                message += f"Attempted coords : {i} {j}\n"
                raise IndexError(message)

        return "\n".join([" ".join(line) for line in grid])


if __name__ == "__main__":
    # Can't see much, gotta reduce battle size or increase grid size.
    battle = Battle()
    random.seed()
    grid_size = 10
    battle_size = 5
    for side in range(2):
        for _ in range(battle_size):
            coords = np.array(np.random.randint(0, grid_size - 1, 2), float)
            strategy = [target_closest, target_weakest][side]
            battle.units.append(Unit(side, coords, strategy))
    # battle.units.append(Unit(0, np.array((5,0)), target_weakest))
    for _ in range(5):
        print(battle)
        print("*******")
        battle.update()
