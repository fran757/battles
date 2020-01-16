from copy import deepcopy
from dataclasses import dataclass
from itertools import islice
from typing import List
import numpy as np

from unit import Unit, UnitBase, UnitField, Strategy
from tools import tools, Cache


@dataclass
class Simulation:
    states: List[List[Unit]]

    @property
    def size(self):
        return len(self.states)

    @property
    def units(self):
        return self.states[-1]

    @property
    def volume(self):
        return [sum([u.health for u in self.units if u.side == s]) for s in (0, 1)]

    @tools(log="{self.volume}")
    def update(self):
        Cache.reset()
        self.states.append(deepcopy(self.units))
        sum((unit.decide(self.units) for unit in self.units), None)()
        return self.units if self.is_finished else None

    @property
    def is_finished(self):
        health = np.zeros(2, int)
        for unit in self.units:
            health[unit.side] += unit.health
        return np.all(health > 0)


def prepare_battle():
    infantryman = UnitBase(4, 1.5, 1, 5)
    centurion = UnitBase(100, 1.5, 1, 1000)
    strategies = [Strategy(1, 0), Strategy(0, 1)]

    def array(fun):
        return lambda *a: np.array(fun(*a), float)
    positions = map(array, [lambda i, j: (i, j), lambda i, j: (30 - i, j)])

    units = []
    for side, (position, strategy) in enumerate(zip(positions, strategies)):
        for i, j in np.indices((10, 11)).reshape((2, -1)).T:
            field = UnitField(side, position(i, j), False, 100, 0)
            units.append(Unit(infantryman, field, strategy))

        field = UnitField(side, position(10, 5), True)
        units.append(Unit(centurion, field, Strategy(1, 0)))
    return units


def read_battle(file_name):
    with open(file_name, 'r') as file:
        lines_strat = [file.readline().split() for _ in range(2)]
        strategies = np.array(lines_strat, int)

        states = []
        types = [int, float, lambda x: {"True": True, "False": False}[x]]
        base_cast = [0, 1, 0, 0]
        coord_cast = [1, 1]
        field_cast = [2, 0, 0]

        def cast(values, index):
            return [types[i](values.pop(0)) for i in index]

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

                strat = Strategy(strategies[field.side])
                units.append(Unit(base, field, strat))
            states.append(units)
            status = file.readline().split()
        return states


def make_battle(init, file_name: str):
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
