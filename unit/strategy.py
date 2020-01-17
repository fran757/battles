from dataclasses import dataclass


@dataclass
class Strategy:
    closer: float = 0
    weaker: float = 0
