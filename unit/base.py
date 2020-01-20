from dataclasses import dataclass


@dataclass
class UnitBase:
    """Basic stats container, unit prototype."""
    strength: int
    reach: float
    speed: int
    _health: int  # todo: max/health separation (immutable base)
    braveness: int = 100
    time_fleeing: int = 0

    @property
    def is_dead(self):
        return self.health <= 0

    @property
    def is_fleeing(self):
        return self.braveness <= 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        """Unit health cannot be negative."""
        self._health = max(0, value)

    def reset_braveness(self):
        self.braveness = 100
        self.time_fleeing = 0

    def change_moral(self, value):
        self.braveness += value
