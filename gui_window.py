from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import QTimer, QEventLoop, pyqtSignal
from PyQt5.QtTest import QTest
from battle import Battle
from unit import Unit
from decide import target_closest, target_weakest
import numpy as np
import random

class MainWindow(QGraphicsView):
    """
    The main window of the gui
    """

    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.battle = Battle()
        self.scene = QGraphicsScene()
        self.army_size = 5
        self.grid_size = 70
        random.seed()
        for side in range(2):
            for _ in range(self.army_size):
                coords = np.array(np.random.randint(0, self.grid_size-1, 2), float)
                strategy = [target_closest, target_weakest][side]
                self.battle.units.append(Unit(side, coords, strategy))

        self.setGeometry(300, 300, self.grid_size*10, self.grid_size*10)
        self.setWindowTitle('Battles')
        self.setScene(self.scene)
        self.show()

        for _ in range(5):
            self.update()
            QTest.qWait(500)

    def update(self):
        self.draw()
        self.battle.update()

    def draw(self):
        self.scene.clear()
        color = {0: QColor(255, 0, 0), 1: QColor(0, 0, 255)}
        for unit in self.battle.units:
            i, j = unit.coords
            height, width = 10, 10
            self.scene.addRect(i*10, j*10, width, height, QPen(), QBrush(color[unit.side]))
