import numpy as np

from unit import Unit
from battle import Battle
from decide import target_closest, target_weakest
from gui_window import MainWindow
from PyQt5.QtWidgets import QApplication

def prepare_battle():
    """Battle with several lines on each side.
    Just play around with army size, position..."""
    battle = Battle()
    for i in range(5):
        for j in range(10):
            battle.units.append(Unit(0, np.array((i, j), float), target_closest))
            battle.units.append(Unit(1, np.array((19 - i, j), float), target_weakest))
    return battle


def play_battle(battle):
    """Run a few iterations, then display battlefield and army health."""
    for _ in range(10):
        battle.update()
    print(battle)
    for side in range(2):
        print(sum([unit.health for unit in battle.units if unit.side == side]))


if __name__ == "__main__":
    # play_battle(prepare_battle())
    APP = QApplication([])
    window = MainWindow()
    APP.exec_()
