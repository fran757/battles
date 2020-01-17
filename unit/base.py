from dataclasses import dataclass


@dataclass
class UnitBase:
    """Basic stats container, unit prototype."""
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
        """Unit health cannot be negative."""
        self._health = max(0, value)
