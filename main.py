import numpy as np
from PyQt5.QtWidgets import QApplication
import json

from unit import Unit
from battle import Battle
from decide import strategy
from tools.timer import Clock
from gui_window import MainWindow
from simulate import prepare_battle, make_simulation


if __name__ == "__main__":
    APP = QApplication([])
    make_simulation(prepare_battle(), "yolo.txt")
    # window = MainWindow(prepare_battle())
    Clock.report()
