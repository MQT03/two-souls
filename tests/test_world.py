
import unittest

from two_souls.world.character import Character
from two_souls.world.position import Position
from two_souls.world.world import World
from two_souls.world.position import Position
from two_souls.world.resource_type import ResourceType
from two_souls.world.world_resource import WorldResource


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

    def test_add_resource(self):
        world = World()

        resource = WorldResource(
            "tree-001",
            ResourceType.WOOD,
            Position(20, 30),
            10
        )

        world.add_resource(resource)

        self.assertIs(world.get_resource("tree-001"), resource)


    def test_get_nonexistent_resource_returns_none(self):
        world = World()

        self.assertIsNone(world.get_resource("missing"))


    def test_duplicate_resource_id_raises_error(self):
        world = World()

        resource = WorldResource(
            "tree-001",
            ResourceType.WOOD,
            Position(20, 30),
            10
        )

        world.add_resource(resource)

        with self.assertRaises(ValueError):
            world.add_resource(resource)


    def test_world_returns_resources_as_tuple(self):
        world = World()

        resource = WorldResource(
            "tree-001",
            ResourceType.WOOD,
            Position(20, 30),
            10
        )

        world.add_resource(resource)

        self.assertIsInstance(world.resources, tuple)

if __name__ == "__main__":
    unittest.main()
