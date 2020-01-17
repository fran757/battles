from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QCheckBox, QLineEdit


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
        self.setStyleSheet("QPushButton { height: 30; width: 30; qproperty-iconSize: 25px;}")

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
    save_specs = pyqtSignal(list)

    def __init__(self, unit):
        super().__init__()
        self.unit = unit
        layout = QVBoxLayout()

        self.change_mod = QCheckBox("edit mode")
        self.change_simu = QCheckBox("auto generation")
        self.bgenerate = QPushButton()
        self.bsave_specs = QPushButton()

        self.side = QLabel("side: "+str(self.unit.side))

        self.health = QLabel("health: ")
        self.health_edit = QLineEdit(str(self.unit.health))
        self.strength = QLabel("strength: ")
        self.strength_edit = QLineEdit(str(self.unit.strength))
        self.braveness = QLabel("braveness: ")
        self.braveness_edit = QLineEdit(str(self.unit.braveness))

        specs = [(self.health, self.health_edit),
                 (self.strength, self.strength_edit),
                 (self.braveness, self.braveness_edit)]

        second_layout = QGridLayout()
        for i in range(1, len(specs)+1):
            second_layout.addWidget(specs[i-1][0], i, 1)
            second_layout.addWidget(specs[i-1][1], i, 2)


        self.centurion = QLabel("centurion: "+str(self.unit.is_centurion))

        self.bgenerate.setText("Generate !")
        self.bsave_specs.setText("Save new specs !")

        layout.addWidget(self.change_mod)
        layout.addWidget(self.change_simu)
        layout.addWidget(self.side)
        layout.addLayout(second_layout)
        layout.addWidget(self.centurion)
        layout.addWidget(self.bsave_specs)
        layout.addWidget(self.bgenerate)

        self.setLayout(layout)

        self.change_mod.stateChanged.connect(self.mod_box_checked)
        self.change_simu.stateChanged.connect(self.simu_box_checked)
        self.bgenerate.clicked.connect(self.start_generation)
        self.bsave_specs.clicked.connect(self.save)

    def start_generation(self):
        self.generate.emit()

    def save(self):
        self.save_specs.emit([int(self.health_edit.text()),
                              int(self.strength_edit.text()),
                              int(self.braveness_edit.text())])

    def mod_box_checked(self):
        self.mod_checked.emit()

    def simu_box_checked(self):
        self.simu_checked.emit()

    def change_unit(self, unit):
        self.unit = unit
        self.side.setText("side: "+str(self.unit.side))
        self.health_edit.setText(str(self.unit.health))
        self.strength_edit.setText(str(self.unit.strength))
        self.braveness_edit.setText(str(self.unit.braveness))
        self.centurion.setText("centurion: "+str(self.unit.is_centurion))
