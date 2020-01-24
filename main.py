#!/usr/bin/env python3.7

"""Main, executable file for the project.
By default, open the GUI to visualize and play around with the simulation.
Options :
    -a : do not launch GUI
    -s : run the simulation
"""

import sys
import os.path
from PyQt5.QtWidgets import QApplication

from tools.timer import clock_report
from gui import MainWindow
from control import prepare_battle, make_battle


def main():
    """Parse user input and start the simulation or launch GUI accordingly."""
    save_file = "data/save.txt"

    if "-s" in sys.argv or not os.path.exists(save_file):
        try:
            print("generating simulation...")
            make_battle(prepare_battle(), save_file)
            print("done !")
        except KeyboardInterrupt:
            return  # would not be able to read battle file
        finally:
            clock_report()

    if "-a" not in sys.argv:
        app = QApplication([])
        window = MainWindow(save_file)
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
