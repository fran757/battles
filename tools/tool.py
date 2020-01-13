def _name(fun):
    """Name under which the function will be recorder."""
    return f"{fun.__module__} / {fun.__qualname__}"


class Tool(type):
    def __new__(cls, name, bases, attrs):
        tool = super().__new__(cls, name, bases, attrs)
        tool._known = {}
        return tool

    def __getitem__(cls, fun):
        name = _name(fun)
        if name not in cls._known:
            cls._known[name] = cls()
        return cls._known[name]