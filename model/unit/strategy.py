"""Unit component determining unit strategy."""
from dataclasses import dataclass


@dataclass
class Strategy:
    """Parameters for enemy selection."""
    closer: float = 0.
    weaker: float = 0.
    stronger: float = 0.
