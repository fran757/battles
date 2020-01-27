"""Read simulations and write states to file."""
from itertools import islice
import numpy as np

from model import Simulation, Army, Unit, UnitBase, UnitField, Strategy
from tools import tools


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
            states.append([Army(units) for units in sides])
            status = file.readline().split()
        return Simulation(states)


def write_battle(sides, file_name, mode):
    """Write both sides of a battle to file.
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
