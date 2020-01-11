from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


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
