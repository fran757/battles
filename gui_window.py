from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtTest import QTest
from battle import Battle

from random import sample

class MainWindow(QGraphicsView):
    """The main window of the gui."""

    def __init__(self, battle: Battle):
        super().__init__()
        self.battle = battle
        self.unit_size = 10
        self.scene = QGraphicsScene()
        self.grid_size = 20

        self.setGeometry(300, 300, self.grid_size*10, self.grid_size*10)
        self.setWindowTitle('Battles')
        self.setScene(self.scene)
        self.show()

        while not self.battle.is_finished():
            self.update()
            QTest.qWait(1)

    def update(self):
        """Update the graphics and the grid between two steps."""
        self.battle.update()
        self.draw()

    def draw(self):
        """Draw the units."""
        self.scene.clear()
        # shuffle so that we also see blue units
        for unit in sample(self.battle.units, len(self.battle.units)):
            i, j = map(int, map(round, unit.coords))
            color = {0: QColor(150*(unit.health/5)+105, 0, 0),
                     1: QColor(0, 0, 150*(unit.health/5)+105)}
            self.scene.addRect(i*self.unit_size, j*self.unit_size,
                               self.unit_size, self.unit_size,
                               QPen(), QBrush(color[unit.side]))
