
import unittest

from two_souls.simulation.session import (
    GameSession,
    create_new_game
)


class TestGameSession(unittest.TestCase):

    def setUp(self):
        self.session = create_new_game()

    def test_creates_game_session(self):
        self.assertIsInstance(self.session, GameSession)

    def test_creates_adam_and_lina(self):
        adam = self.session.world.get_character("adam-001")
        lina = self.session.world.get_character("lina-001")

        self.assertIsNotNone(adam)
        self.assertIsNotNone(lina)

        self.assertEqual(adam.name, "Adam")
        self.assertEqual(lina.name, "Lina")

    def test_simulation_engine_starts_at_zero(self):
        self.assertEqual(self.session.engine.tick_count, 0)

    def test_simulation_updates_both_characters(self):
        adam = self.session.world.get_character("adam-001")
        lina = self.session.world.get_character("lina-001")

        self.session.engine.advance_tick()

        self.assertAlmostEqual(adam.needs.hunger, 0.05)
        self.assertAlmostEqual(lina.needs.hunger, 0.05)
        
    def test_runner_advances_session_engine(self):
        ticks = self.session.runner.update(1.0)

        self.assertEqual(ticks, 1)
        self.assertEqual(self.session.engine.tick_count, 1)


if __name__ == "__main__":
    unittest.main()
