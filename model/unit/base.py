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
        """Unit is considered dead when its health falls to 0."""
        return self.health <= 0

    @property
    def is_fleeing(self):
        """Unit starts fleeing once its braveness falls to 0."""
        return self.braveness <= 0

    @property
    def health(self):
        """Property wrapper for unit health."""
        return self._health

    @health.setter
    def health(self, value):
        """Unit health cannot be negative."""
        self._health = max(0, value)

    def reset_braveness(self):
        """Set braveness back to normal, unit stops fleeing."""
        self.braveness = 100
        self.time_fleeing = 0

    def change_moral(self, value):
        """Add given value (can be negative) to unit braveness."""
        self.braveness = min(self.braveness + value, 100)
