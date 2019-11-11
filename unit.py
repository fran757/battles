from dataclasses import dataclass
from typing import Callable
import numpy as np

from colorama import Fore, Style

from delay import delay


@dataclass
class Unit:
    """Basic unit structure.
    Combat attributes (annotations below).
    Elementary actions (move, attack) as delayed orders.
    """

    side: int # which side the unit is on (e.g. blue and red armies)
    coords: np.ndarray # where the unit is (float)
    strategy: Callable = delay(lambda *args: None) # decision taking
    health: int = 5 # health remaining
    strength: int = 1 # how much damage inflicted through attacks
    reach: int = 1.5 # how far damage can be dealt
    speed: int = 1 # how far the unit can go at a time

    @delay
    def attack(self, target):
        """Inflict damage according to own strength."""
        target.health -= self.strength

    @delay
    def move(self, direction):
        """Move according to own speed."""
        self.coords += self.speed * direction

    def decide(self, others):
        """Take decision according to own strategy."""
        return self.strategy(self, others)

    def __str__(self):
        """Print health with color code for side."""
        color_code = [Fore.BLUE, Fore.RED]
        return color_code[self.side] + str(self.health) + Style.RESET_ALL
