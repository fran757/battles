from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtTest import QTest
from gui_buttons import ActionButtons
from gui_battlefield import Battlefield
from simulate import Simulation


class MainWindow(QWidget):
    """
    The main window of the program
    """
    def __init__(self, simulation):
        super().__init__()
        layout = QVBoxLayout()
        self.buttons = ActionButtons()
        self.battlefield = Battlefield(simulation)
        self.play = False
        self.setWindowTitle("Battles")

        layout.addWidget(self.battlefield)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

        self.buttons.click.connect(self.battlefield.update)
        self.buttons.pause.connect(self.play_pause)

        self.setGeometry(300, 300, self.battlefield.width()+30, self.battlefield.height())
        self.show()

    def play_pause(self):
        """
        Change the status
        """
        self.play = not self.play
        while self.play:
            self.battlefield.update(1)
            QTest.qWait(400)
