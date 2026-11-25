import unittest

from two_souls.simulation.session import create_new_game
from two_souls.world.character_decision import CharacterDecision
from two_souls.world.character_state import CharacterState
from two_souls.simulation.systems.decision_system import DecisionSystem

class TestDecisionSystem(unittest.TestCase):

    def setUp(self):
        self.session = create_new_game()

        self.adam = self.session.world.get_agent("adam-001")
        self.lina = self.session.world.get_agent("lina-001")

    def advance_decisions(self):
        for _ in range(5):
            self.session.engine.advance_tick()

    def test_adam_prefers_work(self):
        self.advance_decisions()

        self.assertEqual(
            self.adam.mind.decision,
            CharacterDecision.WORK
        )

    def test_lina_prefers_socializing(self):
        self.advance_decisions()

        self.assertEqual(
            self.lina.mind.decision,
            CharacterDecision.SOCIALIZE
        )

    def test_hunger_overrides_personality_preference(self):
        self.adam.character.needs.hunger = 80

        self.advance_decisions()

        self.assertEqual(
            self.adam.mind.decision,
            CharacterDecision.SEEK_FOOD
        )

    def test_thirst_overrides_personality_preference(self):
        self.lina.character.needs.thirst = 80

        self.advance_decisions()

        self.assertEqual(
            self.lina.mind.decision,
            CharacterDecision.SEEK_WATER
        )

    def test_low_energy_prioritizes_rest(self):
        self.adam.character.needs.energy = 20

        self.advance_decisions()

        self.assertEqual(
            self.adam.mind.decision,
            CharacterDecision.REST
        )

    def test_decision_does_not_change_current_state(self):
        decision_system = DecisionSystem(self.session.world)

        decision_system.update(5)

        self.assertEqual(
            self.adam.mind.decision,
            CharacterDecision.WORK
        )

        self.assertEqual(
            self.adam.character.state,
            CharacterState.IDLE
        )


if __name__ == "__main__":
    unittest.main()