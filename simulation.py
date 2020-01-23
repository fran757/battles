"""Run and manage simulations, file I/O."""
from copy import deepcopy
from dataclasses import dataclass
from itertools import islice
from typing import List
import numpy as np

from unit import Factory, Unit, UnitBase, UnitField, Strategy, Centurion
from tools import tools, Bar


@dataclass
class Simulation:
    """Container for successive steps of a battle."""
    states: List[List["Centurion"]]

    @property
    def size(self):
        """Length of battle (number of steps)."""
        return len(self.states)

    def state(self, i):
        """Accessor for a specific state (step number i)."""
        units = []
        for side in self.states[i]:
            units += side.units
        return units

    @property
    def units(self):
        """Access units from latest state of the battle.
        Equivalent to state(self, -1).
        """
        return self.states[-1]

    @property
    def volume(self):
        """Total health on each side."""
        return [s.health for s in self.states[-1]]

    @tools(clock=True, log="Armies' health: {self.volume}")
    def update(self):
        """Generate and append new state to simulation."""
        if self.is_finished:
            return None
        self.states.append(deepcopy(self.states[-1]))
        side1, side2 = self.states[-1]  # todo: clean this up
        (side1.decide(side2) + side2.decide(side1))()
        return self.states[-1]

    @property
    def is_finished(self):
        """Tell whether the battle is over (one side has no health)."""
        return not np.all(self.volume)


@tools(clock=True)
def prepare_battle():
    """Generate initial state of a custom battle.
    Here we have on each side :
    - 10 rows of 11 infantrymen, led by a centurion
    - 1 row of 11 archers led by a crossbow, covering from behind.
    """
    strategies = [(1., 0.), (1., 1.)]  # each side has one uniform strategy

    def array(fun):
        return lambda *a: np.array(fun(*a), float)
    positions = map(array, [lambda i, j: (i, j), lambda i, j: (30 - i, j)])

    centurions = []
    for side, (position, strategy) in enumerate(zip(positions, strategies)):
        factory = Factory(side)
        for i, j in np.indices((2, 11)).reshape((2, -1)).T:
            factory("archer", position(-5+i, j), strategy)
        for i, j in np.indices((10, 11)).reshape((2, -1)).T:
            factory("infantry", position(i, j), strategy)
        factory("centurion", position(10, 5), strategy, True)
        factory("crossbow", position(-4, 5), strategy, True)
        centurions.append(factory.centurion)
    return centurions


@tools(clock=True)
def read_battle(file_name):
    """Parse file for successive steps of a battle."""
    with open(file_name, 'r') as file:
        types = [int, float, lambda x: {"True": True, "False": False}[x]]
        base_cast = [0, 1, 0, 0, 0, 0]
        coord_cast = [1, 1]
        field_cast = [2]
        strat_cast = [1, 1, 1]

        def cast(values, index):
            return [types[i](values.pop(0)) for i in index]

        states = []
        status = file.readline().split()
        while status:
            state = islice(file, int(status[0]))
            sides = [[], []]
            for line in state:
                unit = line.split(" ")
                base = UnitBase(*cast(unit, base_cast))

                side, = cast(unit, [0])
                coords = np.array(cast(unit, coord_cast))
                field = UnitField(side, coords, *cast(unit, field_cast))

                strat = Strategy(*cast(unit, strat_cast))

                sides[field.side].append(Unit(base, field, strat))
            states.append([Centurion(units) for units in sides])
            status = file.readline().split()
        return states


def write_battle(sides, file_name, mode):
    """Write given both sides of a battle to file.
    mode tells whether to append or overwrite file.
    """
    with open(file_name, mode) as file:
        units = sum([side.units for side in sides], [])
        file.write(f"{len(units)}\n")
        for unit in units:
            assert unit.braveness is not True
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
            file.write("\n")


@tools(clock=True)
def make_battle(init, file_name: str):
    """Generate battle from initial state and write it to file.
    Will display a progress bar indicating health of losing army.
    """
    write_battle(init, file_name, "w")
    simulation = Simulation([init])
    bar = Bar(min(simulation.volume))
    for state in iter(simulation.update, None):
        bar.advance(min(simulation.volume))
        write_battle(state, file_name, "a")
    print()
