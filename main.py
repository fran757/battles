#!/usr/bin/env python3.7

import numpy as np
from PyQt5.QtWidgets import QApplication
import json
import sys

from unit import Unit
from battle import Battle
from decide import strategy
from tools.timer import Clock
from gui_window import MainWindow
from simulate import prepare_battle, make_simulation, Simulation


if __name__ == "__main__":
    APP = QApplication([])
    if len(sys.argv) > 1 and sys.argv[1] == "-s":
        print("generating simulation...")
        make_simulation(prepare_battle(), "save.txt")
        print("done !")
    window = MainWindow(Simulation("save.txt"))
    APP.exec_()

    for name, (n, time) in Clock.report().items():
        print(f"{name} (x{n}): {time:.3f} s")

