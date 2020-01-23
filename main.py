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
from gui import MainWindow
from simulation import prepare_battle, make_battle


def main():
    """Parse user input and start the simulation or launch GUI accordingly."""

    if "-s" in sys.argv:
        try:
            print("generating simulation...")
            make_battle(prepare_battle(), "save.txt")
            print("done !")
        except KeyboardInterrupt:
            return  # would not be able to read battle file
        finally:
            clock_report()

    if "-a" not in sys.argv:
        app = QApplication([])
        window = MainWindow("save.txt")
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
