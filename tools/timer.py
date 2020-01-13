from functools import wraps
from time import time

from .tool import Tool


class Clock(metaclass=Tool):
    def __init__(self):
        self._records = []

    def record(self, value):
        """Append value to records."""
        self._records.append(value)

    @classmethod
    def report(cls):
        """Return mean of each record."""
        records = {}
        for name, instance in cls._known.items():
            record = instance._records
            records.update({name: (len(record), sum(record))})
        return records


def clock(fun):
    """Clock decorator : register 'fun' execution times.
    Closure preserves method identity.
    """

    @wraps(fun)
    def timed(*args, **kwargs):
        before = time()
        value = fun(*args, **kwargs)
        now = time()
        Clock[fun].record(now - before)
        return value

    return timed


def clock_report():
    """Provide timing records."""
    print("Clock report :")
    for name, (n, time) in Clock.report().items():
        print(f"{name} (x{n}): {time:.3f} s")
