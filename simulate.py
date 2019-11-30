from battle import Battle
from unit import Unit
from decide import strategy
import numpy as np


def prepare_battle():
    """Battle with several lines on each side.
    Just play around with army size, position..."""
    battle = Battle()
    for i in range(5):
        for j in range(10):
            weakest = strategy(health=1)
            closest = strategy(distance=1)
            battle.units.append(Unit(0, np.array((i, j), float), closest))
            battle.units.append(Unit(1, np.array((19 - i, j), float), weakest))
    return battle


def make_simulation(init_battle: Battle, file_name: str):
    """
    To save the battle in a file
    """

    # In order to erase the content of the file
    with open(file_name, 'w') as file:
        file.close()
    while not init_battle.is_finished():
        init_battle.update()
        init_battle.export_state(file_name)
