from functools import wraps
from inspect import signature

from .tool import Tool


class Cache(metaclass=Tool):
    def __init__(self):
        self._records = {}

    def __setitem__(self, key, value):
        self._records[key] = value

    def __getitem__(self, arg):
        key = id(arg)
        if not key in self._records:
            raise KeyError
        return self._records[key]

    def __setitem__(self, arg, value):
        self._records[id(arg)] = value

    @classmethod
    def reset(cls):
        for instance in cls._known.values():
            instance.records = []


def cache(fun):
    @wraps(fun)
    def cached(*args):
        key = [a for n, a in zip(signature(fun).parameters, args) if n != "self"][0]
        try:
            return Cache[fun][key]
        except KeyError:
            value = fun(*args)
            Cache[fun][key] = value
            return value
    return cached

