"""Run and manage simulations, file I/O."""
from copy import deepcopy
from dataclasses import dataclass
from itertools import islice
from typing import List
import numpy as np

from unit import Factory, Unit, UnitBase, UnitField, Strategy
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

    @tools(log="Armies' health: {self.volume}")
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


@tools(clock=True)
def prepare_battle():
    """Generate initial state of custom battle."""
    strategies = [(1., 0.), (0., 1.)]

    def array(fun):
        return lambda *a: np.array(fun(*a), float)
    positions = map(array, [lambda i, j: (i, j), lambda i, j: (30 - i, j)])

    units = []
    for side, (position, strategy) in enumerate(zip(positions, strategies)):
        factory = Factory(side)
        for j in range(11):
            units.append(factory("archer", position(-5, j), strategy))
        for i, j in np.indices((10, 11)).reshape((2, -1)).T:
            units.append(factory("infantry", position(i, j), strategy))
        units.append(factory("centurion", position(10, 5), strategy, True))
        units.append(factory("crossbow", position(-4, 5), strategy, True))
    return units


@tools(clock=True)
def read_battle(file_name):
    """Parse file for successive steps of a battle."""
    with open(file_name, 'r') as file:
        states = []
        types = [int, float, lambda x: {"True": True, "False": False}[x]]
        base_cast = [0, 1, 0, 0, 0, 0]
        coord_cast = [1, 1]
        field_cast = [2]
        strat_cast = [1, 1, 1]

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

                strat = Strategy(*cast(unit, strat_cast))

                units.append(Unit(base, field, strat))
            states.append(units)
            status = file.readline().split()
        return states


@tools(clock=True)
def make_battle(init, file_name: str):
    """Generate battle from initial state and write it to file."""
    with open(file_name, 'w') as file:
        for state in iter(Simulation([init]).update, None):
            file.write(f"{len(state)}\n")
            for unit in state:
                file.write(" ".join(map(str, [
                    unit.strength,
                    unit.reach,
                    unit.speed,
                    unit.health,
                    unit.braveness,
                    unit.time_fleeing,

                    unit.side,
                    *unit.coords,
                    unit.is_centurion,

                    unit.closer,
                    unit.weaker,
                    unit.stronger
                ])))
                file.write(" \n")
