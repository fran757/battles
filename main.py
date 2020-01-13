#!/usr/bin/env python3.7

"""Main, executable file for the project.
By default, open the GUI to visualize and play around with the simulation.
Options :
    -a : do not launch GUI
    -s : run the simulation
"""

import sys
from PyQt5.QtWidgets import QApplication

from tools.timer import clock_report
from tools.log import Logger
from gui_window import MainWindow
from simulate import prepare_battle, make_simulation


def main():
    """Parse user input and start the simulation or launch GUI accordingly."""
    Logger.init("logs.txt")

    app = QApplication([])
    if "-s" in sys.argv:
        print("generating simulation...")
        make_simulation(prepare_battle(), "save.txt")
        print("done !")
    if "-a" not in sys.argv:
        window = MainWindow("save.txt")
        sys.exit(app.exec_())

    clock_report()


if __name__ == "__main__":
    main()
