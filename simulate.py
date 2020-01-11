from dataclasses import dataclass
from PyQt5.QtGui import QPen, QColor, QBrush
from battle import Battle
from unit import Unit
from decide import strategy
import numpy as np


@dataclass
class GraphicUnit:
    side: int
    x: float
    y: float
    health: int
    strength: int
    braveness: int
    is_centurion: bool
    reach: float
    speed: int
    is_dead: bool
    is_fleeing: bool

    def specs(self):
        return [self.health, self.strength, self.braveness]

    def is_here(self, clicked_x, clicked_y, unit_size, zoom_level):
        i, j = (self.x+10)*unit_size*zoom_level, (self.y+10)*unit_size*zoom_level
        if (i <= clicked_x <= i+unit_size) and (j <= clicked_y <= j+unit_size):
            return True
        else:
            return False

    def draw(self, scene, unit_size, zoom_level, color: QColor):
        i, j = self.x+10, self.y+10
        scene.addRect(i*unit_size*zoom_level,
                      j*unit_size*zoom_level,
                      unit_size,
                      unit_size,
                      QPen(), QBrush(color))

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


class Simulation:
    """
    A simple class to load a simulation from a file
    """

    def __init__(self, file_name):
        super().__init__()
        with open(file_name, 'r') as file:
            lines = [line.rstrip().split(' ') for line in file.readlines()]
            self.states = []
            self.strat = [[int(lines[0][0]), int(lines[0][1])], [int(lines[1][0]), int(lines[1][1])]]
            i = 2
            while i < len(lines):
                units = []
                size = int(lines[i][0])
                for j in range(1, size+1):
                    units.append(GraphicUnit(int(lines[i+j][0]),
                                             float(lines[i+j][1]),
                                             float(lines[i+j][2]),
                                             int(lines[i+j][3]),
                                             int(lines[i+j][4]),
                                             int(lines[i+j][5]),
                                             bool(int(lines[i+j][6])),
                                             float(lines[i+j][7]),
                                             int(lines[i+j][8]),
                                             bool(int(lines[i+j][9])),
                                             bool(int(lines[i+j][10]))))
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

    def export(self, state, name):
        """
        To regenerate a simulation file from a state in Simulation
        """
        print("Generating new simulation...")
        battle = Battle()
        graph_units = self.get_state(state)
        strats = [strategy(health=st[0], distance=st[1]) for st in self.strat]
        for gunit in graph_units:
            battle.units.append(Unit(gunit.side,
                                     np.array((gunit.x, gunit.y), float),
                                     strats[gunit.side],
                                     gunit.health, gunit.strength,
                                     gunit.braveness,
                                     gunit.reach, gunit.speed,
                                     gunit.is_dead, gunit.is_fleeing,
                                     gunit.is_centurion))
        make_simulation(battle, name)
        print("... Done !")



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
    battle.units.append(Unit(0, np.array((10, 5), float),
                        closest, 1000, 100, 100, 1.5, 1, False, False, True))
    battle.units.append(Unit(1, np.array((20, 5), float),
                        closest, 1000, 100, 100, 1.5, 1, False, False, True))

    return battle


def make_simulation(battle: Battle, file_name: str):
    """Save the battle in a file."""
    state = 0
    # In order to erase the content of the file
    with open(file_name, 'w') as file:
        file.write("1 0 \n") #arguments for strategy, health and distance, in the order of sides, to improve
        file.write("0 1 \n")
        file.close()
    while not battle.is_finished() and state < 200:
        state += 1
        battle.update()
        battle.export_state(file_name)
