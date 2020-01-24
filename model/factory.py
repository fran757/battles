from dataclasses import dataclass, field as dfield
from typing import List
import json

from tools import tools

from .unit import Unit, UnitBase, UnitField, Strategy
from .army import Army

@dataclass
class Factory:
    side: int
    units: List[Unit] = dfield(default_factory=list)

    _registery = {}

    @classmethod
    @tools(log="registered {name}")
    def register(cls, name, prototype):
        cls._registery[name] = prototype

    @property
    def army(self):
        return Army(self.units)

    def __call__(self, name, coords, strategy, is_centurion=False):
        try:
            base = self._registery[name]
        except KeyError:
            tools(log=f"Unregistered name: {name}")()
            base = UnitBase(0, 0, 0, 0)
        field = UnitField(self.side, coords, is_centurion)
        strat = Strategy(*strategy)
        self.units.append(Unit(base, field, strat))
        return self.units[-1]


def load(file_name):
    with open(file_name) as file:
        data = json.load(file)
    for name, attrs in data.items():
        Factory.register(name, UnitBase(*attrs))
