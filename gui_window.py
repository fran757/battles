from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtTest import QTest
from simulate import Simulation
from random import sample


class MainWindow(QGraphicsView):
    """The main window of the gui."""

    def __init__(self, simulation: Simulation):
        super().__init__()
        self.simulation = simulation
        self.state = 0
        self.unit_size = 10
        self.scene = QGraphicsScene()
        self.grid_size = 50

        self.setGeometry(300, 300, self.grid_size*10, self.grid_size*10)
        self.setWindowTitle('Battles')
        self.setScene(self.scene)
        self.show()

        while not self.state == self.simulation.size-1:
            self.update()
            QTest.qWait(100)

    def update(self):
        """Update the graphics and the grid between two steps."""
        self.state += 1
        self.draw()

    def draw(self):
        """Draw the units."""
        self.scene.clear()
        # shuffle so that we also see blue units
        for unit in self.simulation.get_state(self.state):
            i, j = [unit[1], unit[2]]
            color = {0: QColor(150*(unit[3]/5)+105, 0, 0),
                     1: QColor(0, 0, 150*(unit[3]/5)+105)}
            self.scene.addRect(i*self.unit_size, j*self.unit_size,
                               self.unit_size, self.unit_size,
                               QPen(), QBrush(color[unit[0]]))
