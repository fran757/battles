from dataclasses import dataclass


@dataclass
class Strategy:
    closer: int = 0
    weaker: int = 0
