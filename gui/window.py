from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMenuBar
from PyQt5.QtWidgets import QAction, QFileDialog, QLabel, QComboBox, QSlider
from PyQt5.QtTest import QTest

from .buttons import ActionButtons, InfoBox
from .battlefield import Battlefield
import os


class MainMenu(QMenuBar):
    """
    The menubar for the mainwindow
    """
    loading = pyqtSignal(str)
    saving = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.file = self.addMenu("File")
        self.loadAction = QAction("Load")
        self.saveAction = QAction("Generate new from now")

        self.file.addAction(self.loadAction)
        self.file.addAction(self.saveAction)

        self.loadAction.triggered.connect(self.load)
        self.saveAction.triggered.connect(self.save)

    @staticmethod
    def path():
        return os.path.dirname(os.path.abspath(__file__))

    def load(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', self.path(), "Game files (*.txt)")
        self.loading.emit(name[0])

    def save(self):
        name = QFileDialog.getSaveFileName(self, 'Save file', self.path(), "Game files (*.txt)")
        self.saving.emit(name[0])


class MainWindow(QWidget):
    """
    The main window of the program
    """

    def __init__(self, path: str):
        super().__init__()

        colormaps = ["health", "strength", "braveness"]
        layout = QVBoxLayout()
        self.selected_unit = 0
        self.message = QLabel("Welcome !")
        self.buttons = ActionButtons()
        self.slide = QSlider(Qt.Horizontal)
        self.battlefield = Battlefield(path)
        self.info = InfoBox(self.battlefield.get_unit(0))
        self.select = QComboBox()
        self.select.addItems(colormaps)

        self.slide.setMinimum(0)
        self.slide.setMaximum(self.battlefield.size)

        self.menu = MainMenu()
        self.play = False
        self.setWindowTitle("Battles")

        layout.addWidget(self.menu)
        layout.addWidget(self.select)

        second_layout = QHBoxLayout()
        second_layout.addWidget(self.battlefield)
        second_layout.addWidget(self.info)

        layout.addLayout(second_layout)
        layout.addWidget(self.buttons)
        layout.addWidget(self.slide)
        layout.addWidget(self.message)

        self.setLayout(layout)

        self.menu.loading.connect(self.load_from_file)
        self.menu.saving.connect(self.battlefield.export)
        self.buttons.click.connect(self.update)
        self.buttons.pause.connect(self.play_pause)
        self.buttons.zoom_io.connect(self.battlefield.zoom)
        self.select.activated[str].connect(self.battlefield.change_colormap)
        self.slide.valueChanged.connect(self.valuechange)
        self.battlefield.click.connect(self.change_selected_unit)
        self.info.mod_checked.connect(self.battlefield.change_mod)
        self.info.simu_checked.connect(self.battlefield.change_simu)
        self.info.generate.connect(self.instant_export)
        self.info.save_specs.connect(self.change_specs)

        self.setGeometry(300, 300, self.battlefield.width()+150,
                         self.battlefield.height())
        self.show()

    def change_selected_unit(self, unit_index: int):
        self.selected_unit = unit_index
        self.info.change_unit(self.battlefield.get_unit(self.selected_unit))

    def change_specs(self, new_specs):
        unit = self.battlefield.get_unit(self.selected_unit)
        for key, value in zip(("health", "strength", "braveness"), new_specs):
            setattr(unit, key, value)

    def instant_export(self):
        self.battlefield.instant_export()
        self.slide.setMaximum(self.battlefield.size)

    def load_from_file(self, path: str):
        self.battlefield.load_from_file(path)
        self.slide.setMaximum(self.battlefield.size)

    def update(self, step_state: int):
        """
        To update the battlefield and the widgets
        """
        stop = self.battlefield.update(step_state)
        self.message.setText(
            "step "+str(self.battlefield.state+1)+"/"+str(self.battlefield.size))
        self.slide.setValue(self.slide.value() + step_state)
        self.info.change_unit(self.battlefield.get_unit(self.selected_unit))
        return stop

    def valuechange(self):
        """
        To move in the simulation
        """
        self.battlefield.go_to_state(self.slide.value())
        self.info.change_unit(self.battlefield.get_unit(self.selected_unit))
        self.message.setText(
            "step "+str(self.battlefield.state+1)+"/"+str(self.battlefield.size))

    def play_pause(self):
        """
        Change the status
        """
        self.play = not self.play
        while self.play:
            self.play = self.update(1)
            QTest.qWait(400)
