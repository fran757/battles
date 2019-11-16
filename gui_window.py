from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtTest import QTest
from battle import Battle


class MainWindow(QGraphicsView):
    """
    The main window of the gui
    """

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

        for _ in range(100):
            self.update()
            QTest.qWait(500)

    def update(self):
        self.battle.update()
        self.draw()

    def draw(self):
        self.scene.clear()
        for unit in self.battle.units:
            i, j = map(int, map(round, unit.coords))
            color = {0: QColor(255*(unit.health/5), 0, 0), 
                     1: QColor(0, 0, 255*(unit.health/5))}
            self.scene.addRect(i*self.unit_size, j*self.unit_size,
                               self.unit_size, self.unit_size,
                               QPen(), QBrush(color[unit.side]))
