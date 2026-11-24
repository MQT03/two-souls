
import unittest

from two_souls.simulation.engine import SimulationEngine
from two_souls.simulation.systems.needs_system import NeedsSystem
from two_souls.world.character import Character
from two_souls.world.character_state import CharacterState
from two_souls.world.position import Position
from two_souls.world.world import World


class TestNeedsSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()

        self.adam = Character(
            "adam-001",
            "Adam",
            Position(10, 20)
        )

        self.world.add_character(self.adam)

        self.engine = SimulationEngine()
        self.engine.add_system(NeedsSystem(self.world))

    def test_hunger_and_thirst_increase(self):
        self.engine.advance_tick()

        self.assertAlmostEqual(self.adam.needs.hunger, 0.05)
        self.assertAlmostEqual(self.adam.needs.thirst, 0.08)

    def test_energy_decreases_while_awake(self):
        self.engine.advance_tick()

        self.assertAlmostEqual(self.adam.needs.energy, 99.95)

    def test_energy_recovers_while_sleeping(self):
        self.adam.state = CharacterState.SLEEPING
        self.adam.needs.energy = 50.0

        self.engine.advance_tick()

        self.assertAlmostEqual(self.adam.needs.energy, 50.15)

    def test_needs_respect_maximum_and_minimum_values(self):
        self.adam.needs.hunger = 99.99
        self.adam.needs.thirst = 99.99
        self.adam.needs.energy = 0.01

        self.engine.advance_tick()

        self.assertEqual(self.adam.needs.hunger, 100.0)
        self.assertEqual(self.adam.needs.thirst, 100.0)
        self.assertEqual(self.adam.needs.energy, 0.0)

    def test_health_is_not_changed(self):
        self.adam.needs.health = 75.0

        self.engine.advance_tick()

        self.assertEqual(self.adam.needs.health, 75.0)


if __name__ == "__main__":
    unittest.main()
