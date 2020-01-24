import os, sys

from tools import clock_report

from .parse import read_battle
from .prepare import prepare_battle, make_battle


def main(save_file):
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
