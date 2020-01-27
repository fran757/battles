"""Utility to log message on command or on function calls."""
from functools import wraps
from inspect import signature

from .tool import Tool


class Logger(metaclass=Tool):
    """Simple container with file writing functionality.
    Stores a generic message for a function, formatted with arguments and
    output before logging to file.
    """
    file_name = None


    @classmethod
    def init(cls, file_name):
        """Indicate name of file to log to."""
        cls.file_name = file_name
        with open(file_name, "w"):
            pass

    @classmethod
    def log(cls, message):
        """Write a (formatted) message to registered file."""
        if cls.file_name is None:
            print(message)
        else:
            with open(cls.file_name, "a") as log_file:
                log_file.write(message + "\n")


def log(message):
    """Register custom message for function, format it on every call."""
    def wrapper(fun):
        @wraps(fun)
        def wrapped(*args, **kwargs):
            formats = dict(zip(signature(fun).parameters, args))
            formats.update(kwargs)
            output = fun(*args, **kwargs)
            formats.update(output=output)
            Logger.log(message.format(**formats))
            return output
        return wrapped
    return wrapper
