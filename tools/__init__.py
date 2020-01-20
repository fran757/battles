"""Provide one decorator enabling different tools for functions :
- clock will time a function and return the results when asked
- cache will map a functions's output to its input to avoid repeating tasks
- log will enable logging either on function call or on demand.

Provide a simple progress bar for longer processes."""

from .timer import clock as _clock, clock_report
from .cache import cache as _cache, Cache
from .log import log as _log
from .progress import Bar


def tools(cache=False, clock=False, log=None):
    """Unified decorator for all tools.
    If no function is given, take action immediately (useful for logging).
    """
    def deco(fun=None):
        if fun is None:
            return deco(lambda: None)()

        name = fun.__name__

        if clock:
            fun = _clock(fun)
        if log is not None:
            fun = _log(log)(fun)
        if cache:
            fun = _cache(fun)

        if not fun.__name__ == name:
            tools(log=f"Altered {name} with options {clock} {log} {cache}")()

        return fun
    return deco
