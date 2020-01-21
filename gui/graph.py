from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsView, QGraphicsScene, QVBoxLayout
from PyQt5.QtGui import QPen, QColor
import numpy as np
import matplotlib.pyplot as plt

class Graph(QGraphicsView):
    """
    To plot in red and blue two lists
    """
    def __init__(self, title, R, B):
        super().__init__()

        self.R = R
        self.B = B
        self.title = title

        self.width = 100
        self.height = 50

        self.current_state = 0
        self.setSceneRect(0, 0, self.width, self.height)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        self.step = self.height/max(max(R), max(B))
        self.state_step = self.width/len(R)

        self.mousePressEvent = self.on_mousePressEvent

        self.setMinimumWidth(self.width+2)
        self.setMaximumWidth(self.width+2)
        self.setMinimumHeight(self.height)
        self.setMaximumHeight(self.height+2)

    def draw_curves(self):
        self.scene.addRect(0, 0, self.width, self.height,
                           QPen(QColor(255, 255, 255)), QColor(255, 255, 255))
        self.scene.addLine(self.current_state*self.state_step, 0,
                           self.current_state*self.state_step, self.height,
                           QPen())

        for i in range(1,len(self.R)):

            self.scene.addLine((i-1)*self.state_step,
                               self.height-(self.R[i-1]*self.step),
                               i*self.state_step,
                               self.height-(self.R[i]*self.step),
                               QPen(QColor(255, 0, 0)))
            self.scene.addLine((i-1)*self.state_step,
                               self.height-(self.B[i-1]*self.step),
                               i*self.state_step,
                               self.height-(self.B[i]*self.step),
                               QPen(QColor(0, 0, 255)))

    def change_state(self, state):
        self.current_state = state
        self.draw_curves()

    def load_data(self, RED, BLUE):
        self.R = RED
        self.B = BLUE
        self.step = self.height/max(max(RED), max(BLUE))
        self.state_step = self.width/len(RED)
        self.draw_curves()

    def on_mousePressEvent(self, event):
        plt.ion()
        plt.title(self.title+" over time")
        plt.xlabel("step of the simulation")
        plt.ylabel("average "+self.title)
        plt.plot(self.R,'r')
        plt.plot(self.B,'b')
        plt.show()

class GraphWidget(QWidget):
    """
    The graphs on the side of the window
    """
    def __init__(self, HEALTH, STRENGTH, BRAVE):
        super().__init__()

        layout = QVBoxLayout()

        self.health = Graph("health", *HEALTH)
        self.strength = Graph("strength", *STRENGTH)
        self.brave = Graph("braveness", *BRAVE)

        layout.addWidget(QLabel("health: "))
        layout.addWidget(self.health)
        layout.addWidget(QLabel("strength: "))
        layout.addWidget(self.strength)
        layout.addWidget(QLabel("braveness: "))
        layout.addWidget(self.brave)

        self.setLayout(layout)
        self.draw()

    def load_data(self, HEALTH, STRENGTH, BRAVE):
        self.health.load_data(*HEALTH)
        self.strength.load_data(*STRENGTH)
        self.brave.load_data(*BRAVE)

    def change_state(self, state):
        self.health.change_state(state)
        self.strength.change_state(state)
        self.brave.change_state(state)
        self.draw()

    def draw(self):
        self.health.draw_curves()
        self.strength.draw_curves()
        self.brave.draw_curves()
