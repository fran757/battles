from .timer import clock as _clock, clock_report
from .cache import cache as _cache, Cache
from .log import log as _log


def tools(cache=False, clock=False, log=None):
    def deco(fun):
        if clock:
            fun = _clock(fun)
        if log is not None:
            fun = _log(log)(fun)
        if cache:
            fun = _cache(fun)
        return fun
    return deco
