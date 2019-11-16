from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtTest import QTest
from battle import Battle
from unit import Unit
from decide import target_closest, target_weakest
import numpy as np


class MainWindow(QGraphicsView):
    """
    The main window of the gui
    """

    def __init__(self, battle: Battle):
        super().__init__()
        self.battle = battle
        self.scene = QGraphicsScene()
        self.army_size = 5
        self.grid_size = 20

        self.setGeometry(300, 300, self.grid_size*10, self.grid_size*10)
        self.setWindowTitle('Battles')
        self.setScene(self.scene)
        self.show()

        for _ in range(100):
            self.update()
            QTest.qWait(500)

    def update(self):
        self.battle.update()
        self.draw()

    def draw(self):
        self.scene.clear()
        color = {0: QColor(255, 0, 0), 1: QColor(0, 0, 255)}
        for unit in self.battle.units:
            i, j = unit.coords
            height, width = 10, 10
            self.scene.addRect(i*10, j*10, width, height, QPen(), QBrush(color[unit.side]))
