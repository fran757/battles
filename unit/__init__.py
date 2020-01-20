from dataclasses import dataclass

from .base import UnitBase
from .field import UnitField
from .strategy import Strategy
from .unit import Unit

from tools import tools


@dataclass
class Factory:
    side: int

    _registery = {}

    @classmethod
    def register(cls, name, prototype):
        cls._registery[name] = prototype

    def __call__(self, name, coords, strategy, is_centurion = False):
        try:
            base = self._registery[name]
        except KeyError:
            tools(log=f"Unregistered name: {name}")()
            base = UnitBase(0, 0, 0, 0)
        field = UnitField(self.side, coords, is_centurion)
        strat = Strategy(*strategy)
        return Unit(base, field, strat)

Factory.register("infantry", UnitBase(4, 1.5, 1, 5))
Factory.register("archer", UnitBase(8, 10., 1, 3))
Factory.register("crossbow", UnitBase(100, 10., 1, 3, True))
Factory.register("centurion", UnitBase(100, 1.5, 1, 1000, True))
Factory.register("special", UnitBase(10, 1.5, 100, 200))
