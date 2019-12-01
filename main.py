import numpy as np
from PyQt5.QtWidgets import QApplication
import json

from unit import Unit
from battle import Battle
from decide import strategy
from tools.timer import Clock
from gui_window import MainWindow
from simulate import prepare_battle, make_simulation, Simulation


if __name__ == "__main__":
    APP = QApplication([])
    # Uncomment to generate a new simulation file
    # print("generating simulation...")
    # make_simulation(prepare_battle(), "save.txt")
    # print("done !")
    window = MainWindow(Simulation("save.txt"))
    APP.exec_()
    Clock.report()
