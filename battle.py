from dataclasses import dataclass

from unit import Unit
from cache import Cache
from timer import clock


class Battle:
    """Contain all units (no setter for adding units, just append).
    Update method to take and enforce all decisions.
    String representation by integer grid approximation.
    """

    def __init__(self):
        self.units = []

    @clock
    def update(self):
        """Chain and enforce unit decisions, then reset data for next round."""
        Cache.reset()
        sum((unit.decide(self.units) for unit in self.units), None)()

    def __repr__(self):
        """Print unit grid (rounded to integer positions).
        Grid size ajusted to max unit coords (should do min too).
        """
        def bound(axis, extr):
            return int(round(extr([unit.coords[axis] for unit in self.units]))) + 1

        width = bound(1, max)
        height = bound(0, max)
        grid = [[" " for _ in range(width)] for _ in range(height)]

        for unit in self.units:
            i, j = map(int, map(round, unit.coords))
            try:
                grid[i][j] = str(unit)
            except IndexError:
                message = f"Grid shape : {height} {width}\n"
                message += f"Attempted coords : {i} {j}\n"
                raise IndexError(message)

        return "\n".join([" ".join(line) for line in grid])
