
import unittest

from two_souls.world.character import Character
from two_souls.world.position import Position
from two_souls.world.needs import Needs
from two_souls.world.personality import Personality
from two_souls.world.character_state import CharacterState


class TestCharacterModel(unittest.TestCase):

    def test_character_has_default_components(self):
        character = Character(
            "adam-001",
            "Adam",
            Position(10, 20)
        )

        self.assertIsInstance(character.needs, Needs)
        self.assertIsInstance(character.personality, Personality)
        self.assertEqual(character.state, CharacterState.IDLE)

    def test_characters_have_independent_needs(self):
        adam = Character("adam-001", "Adam", Position(10, 20))
        lina = Character("lina-001", "Lina", Position(15, 25))

        adam.needs.hunger = 80

        self.assertEqual(adam.needs.hunger, 80)
        self.assertEqual(lina.needs.hunger, 0)

    def test_characters_have_independent_personalities(self):
        adam = Character("adam-001", "Adam", Position(10, 20))
        lina = Character("lina-001", "Lina", Position(15, 25))

        adam.personality.sociability = 90

        self.assertEqual(adam.personality.sociability, 90)
        self.assertEqual(lina.personality.sociability, 50)

    def test_needs_reject_invalid_values(self):
        with self.assertRaises(ValueError):
            Needs(hunger=120)

    def test_personality_rejects_invalid_values(self):
        with self.assertRaises(ValueError):
            Personality(kindness=-10)

    def test_character_state_can_change(self):
        character = Character(
            "adam-001",
            "Adam",
            Position(10, 20)
        )

        character.state = CharacterState.SLEEPING

        self.assertEqual(character.state, CharacterState.SLEEPING)

    def test_needs_reject_invalid_updates(self):
        needs = Needs()

        with self.assertRaises(ValueError):
            needs.hunger = 150


    def test_personality_rejects_invalid_updates(self):
        personality = Personality()

        with self.assertRaises(ValueError):
            personality.kindness = -10
if __name__ == "__main__":
    unittest.main()
