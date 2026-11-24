
import unittest

from two_souls.simulation.engine import SimulationEngine
from two_souls.simulation.system import SimulationSystem


class RecordingSystem(SimulationSystem):
    def __init__(self, name: str, records: list) -> None:
        self.name = name
        self.records = records

    def update(self, tick: int) -> None:
        self.records.append((self.name, tick))


class TestSimulationEngine(unittest.TestCase):

    def test_initial_tick_count_is_zero(self):
        engine = SimulationEngine()

        self.assertEqual(engine.tick_count, 0)

    def test_advance_tick_increments_counter(self):
        engine = SimulationEngine()

        engine.advance_tick()
        engine.advance_tick()

        self.assertEqual(engine.tick_count, 2)

    def test_systems_execute_in_registration_order(self):
        engine = SimulationEngine()
        records = []

        engine.add_system(RecordingSystem("First", records))
        engine.add_system(RecordingSystem("Second", records))

        engine.advance_tick()

        self.assertEqual(
            records,
            [("First", 1), ("Second", 1)]
        )

    def test_system_respects_update_interval(self):
        engine = SimulationEngine()
        records = []

        engine.add_system(
            RecordingSystem("Intelligence", records),
            update_interval=5
        )

        for _ in range(10):
            engine.advance_tick()

        self.assertEqual(
            records,
            [("Intelligence", 5), ("Intelligence", 10)]
        )

    def test_invalid_update_interval_raises_error(self):
        engine = SimulationEngine()
        records = []

        system = RecordingSystem("Test", records)

        for interval in [0, -1, -5]:
            with self.subTest(interval=interval):
                with self.assertRaises(ValueError):
                    engine.add_system(system, update_interval=interval)


if __name__ == "__main__":
    unittest.main()
