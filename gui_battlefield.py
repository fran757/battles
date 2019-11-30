from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen, QColor, QBrush
from simulate import Simulation


class Battlefield(QGraphicsView):
    """The graphical battlefield"""

    def __init__(self, simulation: Simulation):
        super().__init__()
        self.simulation = simulation
        self.state = 0
        self.unit_size = 10
        self.scene = QGraphicsScene()
        self.grid_size = 50

        self.setGeometry(300, 300, self.grid_size*10, self.grid_size*10)
        self.setScene(self.scene)
        self.show()

    def update(self, state_step: int):
        """Update the graphics and the grid between two steps."""
        if 0 <= self.state+state_step < self.simulation.size:
            self.draw()
            self.state += state_step

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
