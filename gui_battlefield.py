from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QLabel
from PyQt5.QtGui import QPen, QColor, QBrush, QPixmap, QMovie
from PyQt5.QtTest import QTest
from simulate import Simulation, GraphicUnit


class Battlefield(QGraphicsView):
    """The graphical battlefield"""

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
        self.background = QPixmap("fond.png")
        self.zoom_level = 1
        self.selected_unit = 0
        self.edit = False
        self.simu = False
        self.loading = QLabel()

        gif_load = QMovie("loading.gif")
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
        self.simulation = Simulation(path)
        self._state = 0
        self._size = self.simulation.size

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
        self.resetCachedContent()
        self.draw()

    def get_unit(self, index: int):
        """
        To get a specific unit specs
        """
        return self.simulation.get_state(self._state)[index]

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
        if(color in self.possible_colors):
            self.colormap = self.possible_colors[color]
            self.draw()

    def on_mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        sim = self.simulation.get_state(self.state)
        for i in range(len(sim)):
            if sim[i].is_here(pos.x(), pos.y(), self.unit_size, self.zoom_level):
                self.click.emit(i)
                self.selected_unit = i
                self.draw()

    def on_mouseMoveEvent(self, event):
        if(self.edit):
            self.draw()
            pos = self.mapToScene(event.pos())
            self.scene.addRect(pos.x(), pos.y(),
                               self.unit_size,
                               self.unit_size,
                               QPen(), QBrush(QColor(0, 255, 0, 125)))
            QTest.qWait(10)

    def on_mouseReleaseEvent(self, event):
        if(self.edit):
            pos = self.mapToScene(event.pos())
            new_x = (pos.x()/(self.zoom_level*self.unit_size))-10
            new_y = (pos.y()/(self.zoom_level*self.unit_size))-10
            self.simulation.get_state(self._state)[
                self.selected_unit].move(new_x, new_y)
            self.draw()
            if self.simu:
                self.instant_export()

    def change_mod(self):
        self.edit = not(self.edit)

    def change_simu(self):
        self.simu = not(self.simu)

    def gen_color(self, index, unit):
        """
        To generate a colormap
        """
        max_val = max([unit.specs()[index]
                       for unit in self.simulation.get_state(0)])
        return {0: QColor(150*(unit.specs()[index]/max_val)+105, 0, 0),
                1: QColor(0, 0, 150*(unit.specs()[index]/max_val)+105)}

    def draw(self):
        """Draw the units."""
        self.scene.clear()
        # self.scene.addRect(-100, -100, 500, 500, QPen(), QBrush(QColor(255, 255, 255)))
        self.scene.addPixmap(self.background.scaled(int(self.background.width()*(1+self.zoom_level)),
                                                    int(self.background.height()*(1+self.zoom_level))))
        # shuffle so that we also see blue units
        for unit in self.simulation.get_state(self._state):
            if not unit.health == 0:
                i, j = [unit.x+10, unit.y+10]
                color = self.gen_color(self.colormap, unit)
                unit.draw(self.scene, self.unit_size,
                          self.zoom_level, color[unit.side])
        self.simulation.get_state(self._state)[self.selected_unit].draw(
            self.scene, self.unit_size, self.zoom_level, QColor(0, 255, 0))

    def export(self, name):
        """To export the current state"""
        self.scene.addRect(-10,-10, int(self.background.width()*(1+self.zoom_level)), int(self.background.height()*(1+self.zoom_level)), QPen(), QBrush(QColor(255, 255, 255)))
        self.scene.addWidget(self.loading)
        QTest.qWait(200)
        self.simulation.export(self.state, name)
        QTest.qWait(200)
        self.draw()

    def instant_export(self):
        self.export("new.txt")
        self.load_from_file("new.txt")
