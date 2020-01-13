from .timer import clock as _clock, clock_report
from .cache import cache as _cache
from .log import log as _log


def tools(cache = False, clock = True, log = None):
    def deco(fun):
        if log is not None:
            fun = _log(log)(fun)
        if cache:
            fun = _cache(fun)
        if clock:
            fun = _clock(fun)
        return fun
    return deco
