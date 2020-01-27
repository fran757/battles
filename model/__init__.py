"""Composant pattern-based unit with army-building factory.
Simulation container for successive battle states.
"""
from .army import Army
from .unit import Unit, UnitBase, UnitField, Strategy
from .factory import Factory, load
from .simulation import Simulation
