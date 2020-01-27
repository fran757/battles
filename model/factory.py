"""Army-oriented Unit factory, using generic stats stored in json file."""

from dataclasses import dataclass, field as dfield
from typing import List
import json

from tools import tools

from .unit import Unit, UnitBase, UnitField, Strategy
from .army import Army

@dataclass
class Factory:
    """Interface to build units for an army.
    Army side is provided at instanciation.
    Each call providing unit type and position will use loaded stats
    to add a new unit to the underlying army.
    """
    side: int
    units: List[Unit] = dfield(default_factory=list)

    _registery = {}

    @classmethod
    @tools(log="registered {name}")
    def register(cls, name, prototype):
        """Register prototype for given unit type name."""
        cls._registery[name] = prototype

    @property
    def army(self):
        """Provide army built from created units."""
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
    """Load unit type stats from json file."""
    with open(file_name) as file:
        data = json.load(file)
    for name, attrs in data.items():
        Factory.register(name, UnitBase(*attrs))
