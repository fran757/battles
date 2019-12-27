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
        self.colormap = "health"

        self.zoom_level = 1

        self.setGeometry(300, 300, self.grid_size*10, self.grid_size*10)
        self.setScene(self.scene)
        self.show()
        self.draw()

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

    def go_to_state(self, state):
        """
        Going to the state
        """
        if 0 <= state < self.simulation.size:
            self._state = int(state)
            self.draw()

    def zoom(self, precision: float):
        """
        To zoom in on the picture
        """
        self.zoom_level *= precision
        self.draw()

    def move(self, x_axis: int, y_axis: int):
        """
        To move the camera on the scene
        """
        self.camera[0] += x_axis
        self.camera[1] += y_axis

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

    def change_colormap(self, color: str):
        """
        To change the colormap
        """
        self.colormap = color
        self.draw()

    def gen_color(self, index, unit):
        """
        To generate a colormap
        """
        max_val = max([unit[index] for unit in self.simulation.get_state(self._state)])
        return {0: QColor(150*(unit[index]/max_val)+105, 0, 0),
                1: QColor(0, 0, 150*(unit[index]/max_val)+105)}

    def draw(self):
        """Draw the units."""
        self.scene.clear()
        # shuffle so that we also see blue units
        for unit in self.simulation.get_state(self._state):
            i, j = [unit[1], unit[2]]

            if self.colormap == "health":
                color = self.gen_color(3, unit)
            elif self.colormap == "strength":
                color = self.gen_color(4, unit)

            self.scene.addRect(i*self.unit_size*self.zoom_level,
                               j*self.unit_size*self.zoom_level,
                               self.unit_size*self.zoom_level,
                               self.unit_size*self.zoom_level,
                               QPen(), QBrush(color[unit[0]]))
