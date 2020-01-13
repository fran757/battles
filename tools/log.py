from functools import wraps
from inspect import signature

from .tool import Tool


class Logger(metaclass=Tool):
    file_name = "log.txt"

    @classmethod
    def init(cls, file_name):
        cls.file_name = file_name
        with open(file_name, "w"):
            pass

    @classmethod
    def log(cls, message):
        if cls.file_name is None:
            print(message)
        else:
            with open(cls.file_name, "a") as log_file:
                log_file.write(message + "\n")


def log(message):
    def wrapper(fun):
        @wraps(fun)
        def wrapped(*args, **kwargs):
            formats = {n: v for n, v in zip(signature(fun).parameters, args)}
            formats.update(kwargs)
            output = fun(*args, **kwargs)
            formats.update(output = output)
            Logger.log(message.format(**formats))
            return output
        return wrapped
    return wrapper
