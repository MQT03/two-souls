
import unittest

from two_souls.world.character import Character
from two_souls.world.position import Position
from two_souls.world.world import World


class TestWorld(unittest.TestCase):

    def setUp(self):
        self.world = World()

        self.adam = Character(
            "adam-001",
            "Adam",
            Position(10, 20)
        )

        self.lina = Character(
            "lina-001",
            "Lina",
            Position(15, 25)
        )

    def test_add_character(self):
        self.world.add_character(self.adam)

        self.assertIs(
            self.world.get_character("adam-001"),
            self.adam
        )

    def test_add_multiple_characters(self):
        self.world.add_character(self.adam)
        self.world.add_character(self.lina)

        self.assertIs(
            self.world.get_character("adam-001"),
            self.adam
        )

        self.assertIs(
            self.world.get_character("lina-001"),
            self.lina
        )

    def test_get_nonexistent_character_returns_none(self):
        result = self.world.get_character("unknown")

        self.assertIsNone(result)

    def test_duplicate_character_id_raises_error(self):
        self.world.add_character(self.adam)

        duplicate = Character(
            "adam-001",
            "Adam Clone",
            Position(30, 40)
        )

        with self.assertRaises(ValueError):
            self.world.add_character(duplicate)


if __name__ == "__main__":
    unittest.main()
