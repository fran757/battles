from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen, QColor, QBrush
from simulate import Simulation


class Battlefield(QGraphicsView):
    """The graphical battlefield"""

    def __init__(self, simulation: Simulation):
        super().__init__()
        self.simulation = simulation
        self._state = 0
        self._size = self.simulation.size
        self.unit_size = 10
        self.scene = QGraphicsScene()
        self.grid_size = 50

        self.setGeometry(300, 300, self.grid_size*10, self.grid_size*10)
        self.setScene(self.scene)
        self.show()

    def load_from_file(self, path: str):
        """
        To load a simulation from a file
        """
        self.simulation = Simulation(path)
        self._state = 0

    def update(self, state_step: int):
        """Update the graphics and the grid between two steps."""
        if 0 <= self._state+state_step < self.simulation.size:
            self._state += state_step
            self.draw()

    @property
    def size(self):
        """
        Get the size of the simulation
        """
        return self._size

    @property
    def state(self):
        """
        Get the current state
        """
        return self._state

    def draw(self):
        """Draw the units."""
        self.scene.clear()
        # shuffle so that we also see blue units
        for unit in self.simulation.get_state(self._state):
            i, j = [unit[1], unit[2]]
            color = {0: QColor(150*(unit[3]/5)+105, 0, 0),
                     1: QColor(0, 0, 150*(unit[3]/5)+105)}
            self.scene.addRect(i*self.unit_size, j*self.unit_size,
                               self.unit_size, self.unit_size,
                               QPen(), QBrush(color[unit[0]]))
