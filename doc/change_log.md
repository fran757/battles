# Unit separated in three component classes :
- UnitBase, with stats defining unit type (strength, reach, speed, health)
- Strategy, holding decision-taking parameters
- UnitField, with in-situ stats (side, coords, braveness, centurion, fleeing)

The three component are then assembled in Unit, which takes one prototype
of each component (copying their fields as attributes).
Unit also implements decision taking, with logic methods (focus, flee, moral_update)
and action methods (move, attack, ...)
Any modification to Unit is to be delayed, which is done by returning a call to
a @delay decorated method. This can also be done on the fly like so :
"return delay(self.change)(args)" where "self.change" is any Unit method taking
"args" as arguments.


# Simulation overhaul :
- Simulation class holding successive states of a battle (each state being an unit list).
Different accessors (properties) to provide information about the simulation
are implemented (size, unit, volume, is_finished, and to each their docstring).
An update method keeps the battle going one step at a time until either side tumbles.

- prepare_battle generates the initial state of the battle that is to be simulated
(instanciate prototypes, then successively arrange each side in a similar fashion).

- read_battle parses a battle file and stores them in a state list,
ready for a Simulation instanciation.

- make_battle runs a Simulation instanciated with provided initial state,
and writes it to a file.

These three methods should probably be separated from simulation.py.
