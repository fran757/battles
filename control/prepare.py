import numpy as np

from model import Factory
from tools import tools, Bar
from .parse import write_battle
from .simulation import Simulation


@tools(clock=True)
def prepare_battle():
    """Generate initial state of a custom battle.
    Here we have on each side :
    - 10 rows of 11 infantrymen, led by a centurion
    - 1 row of 11 archers led by a crossbow, covering from behind.
    """
    strategies = [(1., 0.), (1., 1.)]  # each side has one uniform strategy

    def array(fun):
        return lambda *a: np.array(fun(*a), float)
    positions = map(array, [lambda i, j: (i, j), lambda i, j: (30 - i, j)])

    armies = []
    for side, (position, strategy) in enumerate(zip(positions, strategies)):
        factory = Factory(side)
        for i, j in np.indices((2, 11)).reshape((2, -1)).T:
            factory("archer", position(-5+i, j), strategy)
        for i, j in np.indices((10, 11)).reshape((2, -1)).T:
            factory("infantry", position(i, j), strategy)
        factory("centurion", position(10, 5), strategy, True)
        factory("crossbow", position(-4, 5), strategy, True)
        armies.append(factory.army)
    return armies


@tools(clock=True)
def make_battle(init, file_name: str):
    """Generate battle from initial state and write it to file.
    Will display a progress bar indicating health of losing army.
    """
    write_battle(init, file_name, "w")
    simulation = Simulation([init])
    bar = Bar(min(simulation.volume))
    for state in iter(simulation.update, None):
        bar.advance(min(simulation.volume))
        write_battle(state, file_name, "a")
    print()
