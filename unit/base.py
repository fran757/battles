from dataclasses import dataclass


@dataclass
class UnitBase:
    """Kind of unit."""
    strength: int = 4
    reach: int = 1.5
    speed: int = 1
    health: int = 5

    @property
    def is_dead(self):
        return self.health <= 0
