"""Set up and run Simulation, read and write to file."""
import os, sys

from tools import clock_report

from .parse import read_battle
from .prepare import prepare_battle, make_battle


def main(save_file):
    """Launch simulation using battle setup from prepare.py and write to file.
    Upon interruption will clean up save file and report execution times.
    """
    try:
        print("generating simulation...")
        make_battle(prepare_battle(), save_file)
        print("done !")
    except KeyboardInterrupt:
        os.remove(save_file)
        sys.exit(0)
    except:
        os.remove(save_file)
        raise
    finally:
        clock_report()
