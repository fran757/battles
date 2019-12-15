from dataclasses import dataclass
from typing import Callable
import random
import numpy as np
from colorama import Fore, Style

from delay import delay


@dataclass
class Unit:
    """Basic unit structure.
    Combat attributes (annotations below).
    Elementary actions (move, attack) as delayed orders.
    """

    # todo : too many attributes ?

    side: int  # which side the unit is on (e.g. blue and red armies)
    coords: np.ndarray  # where the unit is (float)
    strategy: Callable = delay(lambda *args: None)  # decision taking
    _health: int = 5  # health remaining
    strength: int = 2  # how much damage inflicted through attacks
    reach: int = 1.5  # how far damage can be dealt
    speed: int = 1  # how far the unit can go at a time
    is_dead: bool = False
    has_centurion = True

    def real_strenght(self):
        """Returns real strenght of the unit"""
        if self.has_centurion:
            return self.strength*1.5
        return self.strength

    @delay
    def attack(self, target):
        """Inflict damage according to own strength."""
        if target.has_centurion:
            death_prob = self.real_strenght()/(target.health) # Probability that a centurion dies
            rand_value = random.random()
            if rand_value < death_prob:
                target.has_centurion = False
        target.health -= self.real_strenght()

    @delay
    def move(self, direction):
        """Move according to own speed."""
        self.coords += self.speed * direction

    @delay
    def flee(self, fleeing_prob):
        """Cowards flee from this unit."""
        rand_value = random.random()
        if rand_value < fleeing_prob:
            self._health *= 0.4  # 40% health loss

    def decide(self, others):
        """Take decision according to own strategy."""
        return self.strategy(self, others)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        """If health falls to 0, unit is dead."""
        self._health = max(value, 0)
        self.is_dead = self._health == 0

    def __str__(self):
        """Print health with color code for side."""
        color_code = [Fore.BLUE, Fore.RED]
        return color_code[self.side] + str(self.health) + Style.RESET_ALL
