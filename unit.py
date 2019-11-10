from dataclasses import dataclass
from typing import Callable
import numpy as np

from colorama import Fore, Style

from delay import delay


@dataclass
class Unit:
    """Basic unit structure.
    Combat attributes and elementary actions (move, attack).
    """

    side: int
    coords: np.ndarray
    strategy: Callable = delay(lambda *args: None)
    health: int = 5
    strength: int = 1
    reach: int = 1.5
    speed: int = 1

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
