
import unittest

from two_souls.simulation.engine import SimulationEngine
from two_souls.simulation.runner import SimulationRunner


class TestSimulationRunner(unittest.TestCase):

    def setUp(self):
        self.engine = SimulationEngine()
        self.runner = SimulationRunner(self.engine)

    def test_no_tick_before_one_game_minute(self):
        ticks = self.runner.update(0.5)

        self.assertEqual(ticks, 0)
        self.assertEqual(self.engine.tick_count, 0)

    def test_advances_one_tick_after_one_second(self):
        ticks = self.runner.update(1.0)

        self.assertEqual(ticks, 1)
        self.assertEqual(self.engine.tick_count, 1)

    def test_time_multiplier_controls_simulation_speed(self):
        runner = SimulationRunner(
            self.engine,
            time_multiplier=5.0
        )

        ticks = runner.update(1.0)

        self.assertEqual(ticks, 5)
        self.assertEqual(self.engine.tick_count, 5)

    def test_fractional_time_is_preserved(self):
        self.runner.update(0.5)
        self.runner.update(0.5)

        self.assertEqual(self.engine.tick_count, 1)

    def test_multiple_ticks_can_run_in_one_update(self):
        ticks = self.runner.update(3.0)

        self.assertEqual(ticks, 3)
        self.assertEqual(self.engine.tick_count, 3)

    def test_invalid_elapsed_time_is_rejected(self):
        invalid_values = [-1, float("nan"), float("inf"), True]

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.runner.update(value)

    def test_invalid_time_multiplier_is_rejected(self):
        invalid_values = [
            0,
            -1,
            float("nan"),
            float("inf"),
            True
        ]

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    SimulationRunner(self.engine, value)


if __name__ == "__main__":
    unittest.main()
