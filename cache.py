def named(cls):
    """Each instance of this class has a unique name.
    This allows it to be registered in cache.
    """

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)  # todo: handle bases
        obj.__init__(*args, **kwargs)
        obj._name = cls._counter
        cls._counter += 1
        return obj

    cls._counter = 0
    cls.__new__ = __new__
    return cls


class Cache:
    """Map function return to arguments.
    Save time on function execution.
    """

    _known = {}

    def __init__(self, fun):
        self.wrapped = fun
        self.records = {}

    def __call__(self, value):
        # todo: type consistency (+ include type in name ?)
        name = value._name
        if name not in self.records:
            self.records[name] = self.wrapped(value)
        return self.records[name]

    @classmethod
    def reset(cls):
        """Reset caches (when function return is assumed to have changed)."""
        for instance in cls._known.values():
            instance.records = {}


def cache(fun):
    """Provide cache for function."""
    name = fun.__name__
    if name not in Cache._known:
        Cache._known[name] = Cache(fun)
    return Cache._known[name]
