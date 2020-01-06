"""Logging utility through a simple decorator.
Provide formatted message to log.
Initialize Logger with file name.
"""

from dataclasses import dataclass
from inspect import signature


@dataclass
class _Logger:
    """Log messages to file of given name.
    If no name is provided, will print to stdout.
    """
    file_name: str = None

    def log(self, message):
        """Print message to registered stream."""
        if self.file_name is None:
            print(message)
        else:
            with open(self.file_name, "a") as log_file:
                log_file.write(message + "\n")


class Logger:
    """Singleton wrapper for _Logger."""
    #todo: some kind of metaclass

    instance = None
    file_name = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = _Logger(cls.file_name)
        return cls.instance

    @classmethod
    def init(cls, file_name):
        """Register output file name."""
        cls.file_name = file_name
        with open(file_name, "w"):
            pass


def log(message):
    """Give message formatting as decorator argument.
    Will log through Logger.
    >>> @log("double {bar} is {output}")
    ... def foo(bar):
    ...     return 2*bar
    >>> foo(2)
    double 2 is 4
    4
    """
    def wrapper(fun):
        formats = {}
        def wrapped(*args, **kwargs):
            for name, value in zip(signature(fun).parameters, args):
                formats[name] = value
            formats.update(kwargs)
            output = fun(*args, **kwargs)
            formats.update(output=output)
            Logger().log(message.format(**formats))
            return output
        return wrapped
    return wrapper

if __name__ == "__main__":
    import doctest
    doctest.testmod()
