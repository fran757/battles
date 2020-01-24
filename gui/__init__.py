from PyQt5.QtWidgets import QApplication
import sys

from .window import MainWindow


def main(save_file):
    app = QApplication([])
    window = MainWindow(save_file)
    sys.exit(app.exec_())
