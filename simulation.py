"""Run and manage simulations, file I/O."""
from copy import deepcopy
from dataclasses import dataclass
from itertools import islice
from typing import List
import numpy as np

from unit import Unit, UnitBase, UnitField, Strategy
from tools import tools, Cache


@dataclass
class Simulation:
    """Container for successive steps of a battle."""
    states: List[List[Unit]]

    @property
    def size(self):
        """Length of battle (number of steps)."""
        return len(self.states)

    def state(self, i):
        return self.states[i]

    @property
    def units(self):
        """Access units from latest state of the battle."""
        return self.states[-1]

    @property
    def volume(self):
        """Total health on each side."""
        return [sum([u.health for u in self.units if u.side == s]) for s in (0, 1)]

    @tools(log="{self.volume}")
    def update(self):
        """Generate and append new state to simulation."""
        Cache.reset()
        self.states.append(deepcopy(self.units))
        sum((unit.decide(self.units) for unit in self.units), None)()
        return self.units if self.is_finished else None

    @property
    def is_finished(self):
        """Tell whether battle is over (one side has no health)."""
        return np.all(self.volume)


def prepare_battle():
    """Generate initial state of custom battle."""
    infantryman = UnitBase(4, 1.5, 1, 5)
    archer = UnitBase(2, 10., 1, 3)
    centurion = UnitBase(100, 1.5, 1, 1000)
    strategies = [Strategy(1., 0.), Strategy(0., 1.)]

    def array(fun):
        return lambda *a: np.array(fun(*a), float)
    positions = map(array, [lambda i, j: (i, j), lambda i, j: (30 - i, j)])

    units = []
    for side, (position, strategy) in enumerate(zip(positions, strategies)):
        for j in range(11):
            field = UnitField(side, position(-5, j), False, 1000, 0)
            units.append(Unit(archer, field, strategies[0]))
        for i, j in np.indices((10, 11)).reshape((2, -1)).T:
            field = UnitField(side, position(i, j), False, 100, 0)
            units.append(Unit(infantryman, field, strategy))

        field = UnitField(side, position(10, 5), True)
        units.append(Unit(centurion, field, Strategy(1, 0)))
        field = UnitField(side, position(-4, 5), False, 1000, 0)
        units.append(Unit(archer, field, strategies[0]))
    return units


def read_battle(file_name):
    """Parse file for successive steps of a battle."""
    with open(file_name, 'r') as file:
        strat_lines = [file.readline().split() for _ in range(2)]

        states = []
        types = [int, float, lambda x: {"True": True, "False": False}[x]]
        base_cast = [0, 1, 0, 0]
        coord_cast = [1, 1]
        field_cast = [2, 0, 0]
        strat_cast = [1, 1]

        def cast(values, index):
            return [types[i](values.pop(0)) for i in index]

        strategies = [cast(line, strat_cast) for line in strat_lines]

        status = file.readline().split()
        while status:
            state = islice(file, int(status[0]))
            units = []
            for line in state:
                unit = line.split(" ")
                base = UnitBase(*cast(unit, base_cast))

                side, = cast(unit, [0])
                coords = np.array(cast(unit, coord_cast))
                field = UnitField(side, coords, *cast(unit, field_cast))

                strat = Strategy(*strategies[field.side])
                units.append(Unit(base, field, strat))
            states.append(units)
            status = file.readline().split()
        return states


def make_battle(init, file_name: str):
    """Generate battle from initial state and write it to file."""
    with open(file_name, 'w') as file:
        file.write("1 0\n")
        file.write("0 1\n")

        for state in iter(Simulation([init]).update, None):
            file.write(f"{len(state)}\n")
            for unit in state:
                file.write(" ".join(map(str, [
                    unit.strength,
                    unit.reach,
                    unit.speed,
                    unit.health
                ])))
                file.write(" ")
                file.write(" ".join(map(str, [
                    unit.side,
                    *unit.coords,
                    unit.is_centurion,
                    unit.braveness,
                    unit.time_fleeing
                ])))
                file.write("\n")
