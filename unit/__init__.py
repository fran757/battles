from dataclasses import dataclass, field as dfield
from typing import List

from .base import UnitBase
from .field import UnitField
from .strategy import Strategy
from .unit import Unit
from .centurion import Centurion

from tools import tools

@dataclass
class Factory:
    side: int
    units: "List" = dfield(default_factory=list)

    _registery = {}

    @classmethod
    @tools(log="registered {name}")
    def register(cls, name, prototype):
        cls._registery[name] = prototype

    @property
    def centurion(self):
        return Centurion(self.units)

    def __call__(self, name, coords, strategy, is_centurion = False):
        try:
            base = self._registery[name]
        except KeyError:
            tools(log=f"Unregistered name: {name}")()
            base = UnitBase(0, 0, 0, 0)
        field = UnitField(self.side, coords, is_centurion)
        strat = Strategy(*strategy)
        self.units.append(Unit(base, field, strat))
        return self.units[-1]


Factory.register("infantry", UnitBase(4, 1.5, 1, 5))
Factory.register("archer", UnitBase(8, 10., 1, 3))
Factory.register("crossbow", UnitBase(100, 10., 1, 30))
Factory.register("centurion", UnitBase(100, 1.5, 1, 100))
Factory.register("special", UnitBase(10, 1.5, 100, 200))
