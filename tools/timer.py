from functools import wraps
from time import time


records = ({}, [])
scope = []

def record(value):
    r = records
    for name in scope:
        try:
            r = r[0][name]
        except KeyError:
            r[0][name] = ({}, [])
            r = r[0][name]
    r[1].append(value)


def clock(fun):
    @wraps(fun)
    def timed(*args, **kwargs):
        before = time()
        scope.append(f"{fun.__qualname__}")
        value = fun(*args, **kwargs)
        now = time()
        record(now - before)
        scope.pop()
        return value
    return timed

def clock_report():
    def aux(tab, name, record):
        count, total = len(record[1]), sum(record[1])
        print(tab * "  " + f"{name:<{50-2*tab}} (x{count:<5}): {total:.3f} s")
        for name, rec in record[0].items():
            aux(tab + 1, name, rec)
    for name, rec in records[0].items():
        aux(0, name, rec)
