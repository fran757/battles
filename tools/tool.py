"""Tool data is stored in a generic dictionnary-like registery,
with one instance for every function (by function name).
Tool functionality is left to function decorators to preserve a method's
identity with closure.
"""
def _name(fun):
    """Name under which the function will be registered."""
    return f"{fun.__qualname__}"


class Tool(type):
    """Metaclass for function-specific tools.
    Functions get a registry by name, with dictionnary-like access."""

    def __new__(cls, name, bases, attrs):
        tool = super().__new__(cls, name, bases, attrs)
        tool._known = {}
        return tool

    def __getitem__(cls, fun):
        """Get registered instance for fun, create it if necessary."""
        name = _name(fun)

        if name not in cls._known:
            cls._known[name] = cls()
        return cls._known[name]

    def instances(cls):
        """Getter for registered instances."""
        for name, instance in cls._known.items():
            yield name, instance

    def reset(cls):
        for instance in cls._known.values():
            instance._records.clear()
