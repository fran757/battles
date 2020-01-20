from dataclasses import dataclass

@dataclass
class Bar:
    total: int

    def advance(self, remaining):
        """stackoverflow.com/questions/3173320/text-progress-bar-in-the-console"""
        ratio = 1 - remaining / self.total
        progress = int(50 * ratio)
        bar = "█" * progress + "-" * (50 - progress)
        print(f"\rProgress: |{bar}| {ratio * 100:.1f}% Complete", end="\r")


