from time import time


class Clock:
    """Record execution time of function.
    Instance registration by function name.
    Report average of each set of records.
    """
    _known = {}

    @classmethod
    def provide(cls, name):
        """Provide clock for named function.
        If not already registered, create one.
        """
        if name not in cls._known:
            cls._known[name] = cls()
        return cls._known[name]

    def __init__(self):
        self.records = []

    def record(self, value):
        """Append value to record."""
        self.records.append(value)

    @classmethod
    def report(cls):
        """Print mean of each record."""
        for name, value in cls._known.items():
            print(name, sum(value.records)/len(value.records))


def clock(fun):
    """Clock decorator : register 'fun' execution times.
    Closure preserves method identity.
    """
    def timed(*args, **kwargs):
        before = time()
        value = fun(*args, **kwargs)
        now = time()
        Clock.provide(fun.__qualname__).record(now - before)
        return value
    return timed
