#!/usr/bin/env python3.7

import numpy as np
from PyQt5.QtWidgets import QApplication
import json
import sys

from unit import Unit
from battle import Battle
from decide import strategy
from tools.timer import clock_report
from tools.log import Logger
from gui_window import MainWindow
from simulate import prepare_battle, make_simulation, Simulation


if __name__ == "__main__":
    Logger.init("logs.txt")

    APP = QApplication([])
    if "-s" in sys.argv:
        print("generating simulation...")
        make_simulation(prepare_battle(), "save.txt")
        print("done !")
    if not "-a" in sys.argv:
        window = MainWindow("save.txt")
        sys.exit(APP.exec_())

    clock_report()
