#!/usr/bin/env python3.7

"""Main, executable file for the project.
By default, open the GUI to visualize and play around with the simulation.
Options :
    -a : do not launch GUI
    -s : run the simulation
"""

import os
import sys

import tools, model, control, gui


def init():
    os.makedirs("data", exist_ok=True)
    tools.Logger.init("data/log.txt")
    model.load("model/base.json")


def main():
    """Parse user input and start the simulation or launch GUI accordingly."""
    init()
    save_file = "data/save.txt"

    if "-s" in sys.argv or not os.path.exists(save_file):
        control.main(save_file)

    if "-a" not in sys.argv:
        gui.main(save_file)


if __name__ == "__main__":
    main()
