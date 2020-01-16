from dataclasses import dataclass


@dataclass
class UnitBase:
    """Kind of unit."""
    strength: int
    reach: float
    speed: int
    _health: int

    @property
    def is_dead(self):
        return self.health <= 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(0, value)

