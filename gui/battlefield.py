from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QLabel
from PyQt5.QtGui import QPen, QColor, QBrush, QPixmap, QMovie
from PyQt5.QtTest import QTest
import numpy as np

from simulation import Simulation, read_battle, make_battle


class Battlefield(QGraphicsView):
    """The graphical battlefield."""

    click = pyqtSignal(int)
    start = pyqtSignal()
    stop = pyqtSignal()

    def __init__(self, path: str):
        super().__init__()

        self.load_from_file(path)
        self.possible_colors = {"health": 0, "strength": 1, "braveness": 2}
        self.unit_size = 10
        self.scene = QGraphicsScene()
        self.grid_size = 50
        self.colormap = 0
        self.background = QPixmap("gui/fond.png")
        self.zoom_level = 1
        self.selected_unit = 0
        self.edit = False
        self.simu = False
        self.loading = QLabel()

        self.wait = False

        gif_load = QMovie("gui/loading.gif")
        self.loading.setMovie(gif_load)
        gif_load.start()

        self.mousePressEvent = self.on_mousePressEvent
        self.mouseMoveEvent = self.on_mouseMoveEvent
        self.mouseReleaseEvent = self.on_mouseReleaseEvent

        self.setGeometry(300, 300, self.grid_size*10, self.grid_size*10)
        self.setScene(self.scene)
        self.show()
        self.draw()

    def load_from_file(self, path: str):
        self.simulation = Simulation(read_battle(path))
        self._state = 0
        self._size = self.simulation.size

    def update(self, state_step: int):
        """Update the graphics and the grid between two steps."""
        if 0 <= self._state + state_step < self.simulation.size:
            self._state += state_step
            self.draw()

    def go_to_state(self, state):
        """Move animation to given state."""
        if 0 <= state < self.simulation.size:
            self._state = int(state)
            self.draw()

    def zoom(self, precision: float):
        """Zoom in on the picture."""
        self.zoom_level *= precision
        self.resetCachedContent()
        self.draw()

    def get_unit(self, index: int):
        """Access specific unit."""
        return self.simulation.state(self._state)[index]

    @property
    def size(self):
        """Get the size of the simulation."""
        return self._size

    @property
    def state(self):
        """Get the current state."""
        return self._state

    def change_colormap(self, color: str):
        """Change the colormap."""
        if color in self.possible_colors:
            self.colormap = self.possible_colors[color]
            self.draw()

    def unit_position(self, unit):
        """Get screen position of unit."""
        return (unit.coords + 10) * self.unit_size * self.zoom_level

    def on_mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        click = np.array((pos.x(), pos.y()))
        for i, unit in enumerate(self.simulation.state(self.state)):
            unit_pos = self.unit_position(unit)
            if np.all(unit_pos <= click) and np.all(click <= unit_pos + self.unit_size):
                self.click.emit(i)
                self.selected_unit = i
                self.draw()
                break
        else:  # no unit found under pointer
            pos = event.pos()
            self.centerOn(pos.x(), pos.y())

    def on_mouseMoveEvent(self, event):
        if self.edit:
            self.draw()
            pos = self.mapToScene(event.pos())
            self.scene.addRect(pos.x(), pos.y(),
                               self.unit_size,
                               self.unit_size,
                               QPen(), QBrush(QColor(0, 255, 0, 125)))
            QTest.qWait(10)

    def on_mouseReleaseEvent(self, event):
        if self.edit:
            pos = self.mapToScene(event.pos())
            new_x = (pos.x()/(self.zoom_level*self.unit_size))-10
            new_y = (pos.y()/(self.zoom_level*self.unit_size))-10
            self.simulation.state(self.state)[self.selected_unit].coords = np.array([new_x, new_y])
            self.draw()
            if self.simu:
                self.instant_export()

    def change_mod(self):
        self.edit = not(self.edit)

    def change_simu(self):
        self.simu = not(self.simu)

    def gen_color(self, index, unit):
        """Generate a colormap for unit."""
        def specs(unit):
            return [unit.health, unit.strength, unit.braveness]
        max_val = max([specs(unit)[index] for unit in self.simulation.state(0)])
        shade = 150 * (specs(unit)[index] / max_val) + 105
        color = [0, 0, 0]
        color[2 * unit.side] = shade
        return QColor(*color)

    def draw_unit(self, unit, pen, brush):
        position = self.unit_position(unit)
        self.scene.addRect(*position, *[self.unit_size] * 2, pen, brush)

    def draw_image(self, image):
        def shape(dim):
            return int(dim * (1 + self.zoom_level))
        self.scene.addPixmap(image.scaled(*map(shape, (image.width(), image.height()))))

    def draw(self):
        """Draw the units and background."""
        self.scene.clear()
        self.draw_image(self.background)

        # shuffle so that we also see blue units
        state = self.simulation.state(self.state)
        for unit in state:
            if not unit.is_dead:
                color = self.gen_color(self.colormap, unit)
                self.draw_unit(unit, QPen(), QBrush(color))
        self.draw_unit(state[self.selected_unit], QPen(), QBrush(QColor(0, 255, 0)))


    def export(self, name):
        """To export the current state"""
        if not(self.wait):
            self.wait = True
            self.scene.addRect(-10,-10, int(self.background.width()*(1+self.zoom_level)), int(self.background.height()*(1+self.zoom_level)), QPen(), QBrush(QColor(255, 255, 255)))
            self.scene.addWidget(self.loading)
            QTest.qWait(200)
            make_battle(self.simulation.state(self.state), name)
            QTest.qWait(200)
            self.draw()
            self.wait = False

    def instant_export(self):
        if not(self.wait):
            self.export("new.txt")
            self.load_from_file("new.txt")
