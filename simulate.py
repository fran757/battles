from battle import Battle
from unit import Unit
from decide import strategy
import numpy as np


class Simulation:
    """
    A simple class to load a simulation from a file
    """
    def __init__(self, file_name):
        with open(file_name, 'r') as file:
            lines = [line.rstrip().split(' ') for line in file.readlines()]
            self.states = []
            self.strat = [lines[0][1], lines[1][1]]
            i = 2
            while i < len(lines):
                units = []
                size = int(lines[i][0])
                for j in range(1, size+1):
                    units.append([int(lines[i+j][0]),
                                  float(lines[i+j][1]),
                                  float(lines[i+j][2]),
                                  int(lines[i+j][3]),
                                  int(lines[i+j][4]),
                                  int(lines[i+j][5])])
                self.states.append(units)
                i += size + 1
        self._size = len(self.states)

    def get_state(self, number: int):
        """
        To get one particular state of the battle
        """
        return self.states[number]

    @property
    def size(self):
        return self._size

def prepare_battle():
    """Battle with several lines on each side.
    Just play around with army size, position...
    """
    battle = Battle()
    for i in range(10):
        for j in range(11):
            weakest = strategy(health=1)
            closest = strategy(distance=1)
            battle.units.append(Unit(0, np.array((i, j), float), closest))
            battle.units.append(Unit(1, np.array((30 - i, j), float), weakest))
    battle.units.append(Unit(0, np.array((10, 5), float), closest, 1000, 100, 100, 1.5, 1, False, False, True))
    battle.units.append(Unit(1, np.array((20, 5), float), closest, 1000, 100, 100, 1.5, 1, False, False, True))

    return battle


def make_simulation(battle: Battle, file_name: str):
    """Save the battle in a file."""
    state = 0
    # In order to erase the content of the file
    with open(file_name, 'w') as file:
        file.write("0 health=1 \n")
        file.write("1 distance=1 \n")
        file.close()
    while not battle.is_finished() and state<100:
        state += 1
        battle.update()
        battle.export_state(file_name)
