from dataclasses import dataclass

@dataclass
class Bar:
    """Knowing estimated computation time (can be any unitless arbitrary value),
    update a loading bar on each call given current remaining time.
    """
    total: int

    def advance(self, remaining):
        """Print simple loading bar, just knowing remaining 'time'."""
        ratio = 1 - remaining / self.total
        progress = round(50 * ratio)
        bar = "█" * progress + "-" * (50 - progress)
        print(f"\rProgress: |{bar}| {ratio * 100:.1f}% Complete", end="\r")
