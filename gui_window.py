from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMenuBar, QMainWindow, QSlider
from PyQt5.QtWidgets import QMenu, QAction, QFileDialog, QLabel, QComboBox
from PyQt5.QtTest import QTest
from gui_buttons import ActionButtons
from gui_battlefield import Battlefield
import os


class MainMenu(QMenuBar):
    """
    The menubar for the mainwindow
    """
    load = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.file = self.addMenu("File")
        self.file.addAction("Load")
        self.file.triggered[QAction].connect(self.get_path)

    def get_path(self):
        """
        To open a filedialog in order to get the path to a new simulation
        """
        filename = QFileDialog.getOpenFileName(self, 'Open file',
                                               os.path.dirname(os.path.abspath(__file__)), "Game files (*.txt)")
        self.load.emit(filename[0])


class MainWindow(QWidget):
    """
    The main window of the program
    """

    def __init__(self, simulation):
        super().__init__()

        colormaps = ["health", "strength", "braveness"]
        layout = QVBoxLayout()
        self.message = QLabel("Welcome !")
        self.buttons = ActionButtons()
        self.slide = QSlider(Qt.Horizontal)
        self.battlefield = Battlefield(simulation)
        self.select = QComboBox()
        self.select.addItems(colormaps)

        self.slide.setMinimum(0)
        self.slide.setMaximum(self.battlefield.size)

        self.menu = MainMenu()
        self.play = False
        self.setWindowTitle("Battles")

        layout.addWidget(self.menu)
        layout.addWidget(self.select)
        layout.addWidget(self.battlefield)
        layout.addWidget(self.buttons)
        layout.addWidget(self.slide)
        layout.addWidget(self.message)

        self.setLayout(layout)

        self.menu.load.connect(self.battlefield.load_from_file)
        self.buttons.click.connect(self.update)
        self.buttons.pause.connect(self.play_pause)
        self.buttons.zoom_io.connect(self.battlefield.zoom)
        self.select.activated[str].connect(self.battlefield.change_colormap)
        self.slide.valueChanged.connect(self.valuechange)

        self.setGeometry(300, 300, self.battlefield.width()+30,
                         self.battlefield.height())
        self.show()

    def update(self, step_state: int):
        """
        To update the battlefield and the widgets
        """
        self.battlefield.update(step_state)
        self.message.setText(
            "step "+str(self.battlefield.state+1)+"/"+str(self.battlefield.size))
        self.slide.setValue(self.slide.value() + step_state)

    def valuechange(self):
        """
        To move in the simulation
        """
        self.battlefield.go_to_state(self.slide.value())
        self.message.setText(
            "step "+str(self.battlefield.state+1)+"/"+str(self.battlefield.size))

    def play_pause(self):
        """
        Change the status
        """
        self.play = not self.play
        while self.play:
            self.update(1)
            QTest.qWait(400)
