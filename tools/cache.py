from functools import wraps
from inspect import signature

from .tool import Tool


class Cache(metaclass=Tool):
    """Container mapping a function's output to its input to arguments,
    avoiding repeating fastidious calculations.
    Will reset records on command (when results are assumed to have changed).
    """
    def __init__(self):
        self._records = {}

    def __getitem__(self, arg):
        key = id(arg)
        if key not in self._records:
            raise KeyError
        return self._records[key]

    def __setitem__(self, arg, value):
        self._records[id(arg)] = value

    @classmethod
    def reset(cls):
        for _, instance in cls.instances():
            instance.records = []


def cache(fun):
    """On each call to fun, try to get computed value from args,
    otherwise compute and update records.
    """
    @wraps(fun)
    def cached(*args):
        param = signature(fun).parameters
        key = [a for n, a in zip(param, args) if n != "self"][0]
        try:
            return Cache[fun][key]
        except KeyError:
            value = fun(*args)
            Cache[fun][key] = value
            return value
    return cached
