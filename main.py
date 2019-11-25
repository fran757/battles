import numpy as np
from PyQt5.QtWidgets import QApplication

from unit import Unit
from battle import Battle
from decide import strategy
from gui_window import MainWindow


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


if __name__ == "__main__":
    APP = QApplication([])
    window = MainWindow(prepare_battle())
    APP.exec_()
