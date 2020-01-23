from functools import wraps
from time import time

from .tool import Tool


class Clock(metaclass=Tool):
    """Register duration of every function call,
    provide results when asked for a report.
    """
    def __init__(self):
        self._records = []

    def record(self, value):
        """Append value to records."""
        self._records.append(value)

    @classmethod
    def report(cls):
        """Return total time taken by function, and number of calls."""
        records = {}
        for name, instance in cls.instances():
            record = instance._records
            records.update({name: (len(record), sum(record))})
        return records


def clock(fun):
    """Register fun's execution times."""
    # clock = Clock[fun]
    @wraps(fun)
    def timed(*args, **kwargs):
        before = time()
        value = fun(*args, **kwargs)
        now = time()
        Clock[fun].record(now - before)
        return value

    return timed


def clock_report():
    """Provide all timing records."""
    print("Clock report :")
    for name, (count, total) in Clock.report().items():
        print(f"{name:<50} (x{count:<5}): {total:.3f} s")

