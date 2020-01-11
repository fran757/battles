from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox
from simulate import GraphicUnit


class Button(QPushButton):
    """
    A custom and fancy button
    """

    def __init__(self, label, value=0):
        super().__init__()
        self.setFixedHeight(30)
        self.setFixedWidth(30)
        self.setText(label)
        self._value = value
        self.setStyleSheet("""
                QPushButton { height: 30; width: 30; qproperty-iconSize: 25px;}
                """)

    @property
    def value(self):
        """
        To get the value
        """
        return self._value


class ActionButtons(QWidget):
    """
    A group of action buttons
    """

    click = pyqtSignal(int)
    pause = pyqtSignal()
    zoom_io = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        self.playpause = Button("⏯")
        self.next = Button(">", 1)
        self.prev = Button("<", -1)
        self.zoom_in = Button("+", 1.1)
        self.zoom_out = Button("-", 0.9)

        self.playpause.clicked.connect(self.pause.emit)
        self.next.clicked.connect(self.get_order)
        self.prev.clicked.connect(self.get_order)
        self.zoom_in.clicked.connect(self.zoom)
        self.zoom_out.clicked.connect(self.zoom)

        layout.addWidget(self.prev)
        layout.addWidget(self.playpause)
        layout.addWidget(self.next)
        layout.addWidget(self.zoom_in)
        layout.addWidget(self.zoom_out)

        self.setLayout(layout)

    def get_order(self):
        """
        To emit a signal when one button is pushed
        """
        sender = self.sender()
        self.click.emit(sender.value)

    def zoom(self):
        """
        To emit a signal when the zoom button is pushed
        """
        sender = self.sender()
        self.zoom_io.emit(sender.value)


class InfoBox(QWidget):
    """
    To display infos on a unit
    """

    mod_checked = pyqtSignal()
    simu_checked = pyqtSignal()
    generate = pyqtSignal()

    def __init__(self, unit: GraphicUnit):
        super().__init__()
        self.unit = unit
        layout = QVBoxLayout()

        self.change_mod = QCheckBox("edit mode")
        self.change_simu = QCheckBox("auto generation")
        self.bgenerate = QPushButton()
        self.side = QLabel("side: "+str(self.unit.side))
        self.health = QLabel("health: "+str(self.unit.health))
        self.strength = QLabel("strength: "+str(self.unit.strength))
        self.braveness = QLabel("braveness: "+str(self.unit.braveness))
        self.centurion = QLabel("centurion: "+str(self.unit.is_centurion))


        self.bgenerate.setText("Generate !")

        layout.addWidget(self.change_mod)
        layout.addWidget(self.change_simu)
        layout.addWidget(self.bgenerate)
        layout.addWidget(self.side)
        layout.addWidget(self.health)
        layout.addWidget(self.strength)
        layout.addWidget(self.braveness)

        self.setLayout(layout)

        self.change_mod.stateChanged.connect(self.mod_box_checked)
        self.change_simu.stateChanged.connect(self.simu_box_checked)
        self.bgenerate.clicked.connect(self.start_generation)

    def start_generation(self):
        self.generate.emit()

    def mod_box_checked(self):
        self.mod_checked.emit()

    def simu_box_checked(self):
        self.simu_checked.emit()

    def change_unit(self, unit: GraphicUnit):
        self.unit = unit
        self.side.setText("side: "+str(self.unit.side))
        self.health.setText("health: "+str(self.unit.health))
        self.strength.setText("strength: "+str(self.unit.strength))
        self.braveness.setText("braveness: "+str(self.unit.braveness))
        self.centurion.setText("centurion: "+str(self.unit.is_centurion))
