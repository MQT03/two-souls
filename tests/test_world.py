
import unittest

from two_souls.world.character import Character
from two_souls.world.agent import Agent
from two_souls.world.position import Position
from two_souls.world.world import World
from two_souls.world.position import Position
from two_souls.world.resource_type import ResourceType
from two_souls.world.world_resource import WorldResource


class TestWorld(unittest.TestCase):

    def setUp(self):
        self.world = World()

        self.adam = Agent(
            Character("adam-001", "Adam", Position(10, 20))
        )

        self.lina = Agent(
            Character("lina-001", "Lina", Position(15, 25))
        )

    def test_add_agent(self):
        self.world.add_agent(self.adam)

        self.assertIs(
            self.world.get_agent("adam-001"),
            self.adam
        )

    def test_add_multiple_agents(self):
        self.world.add_agent(self.adam)
        self.world.add_agent(self.lina)

        self.assertIs(
            self.world.get_agent("adam-001"),
            self.adam
        )

        self.assertIs(
            self.world.get_agent("lina-001"),
            self.lina
        )

        self.assertEqual(self.world.agents, (self.adam, self.lina))

    def test_get_nonexistent_agent_returns_none(self):
        result = self.world.get_agent("unknown")

        self.assertIsNone(result)

    def test_duplicate_agent_id_raises_error(self):
        self.world.add_agent(self.adam)

        duplicate = Agent(
            Character("adam-001", "Adam Clone", Position(30, 40))
        )

        with self.assertRaises(ValueError):
            self.world.add_agent(duplicate)

    def test_character_compatibility_is_a_projection_of_agents(self):
        self.world.add_agent(self.adam)

        self.assertEqual(self.world.characters, (self.adam.character,))
        self.assertIs(
            self.world.get_character("adam-001"),
            self.adam.character,
        )

    def test_legacy_add_character_creates_an_agent(self):
        character = Character("legacy-1", "Legacy", Position(0, 0))

        self.world.add_character(character)

        self.assertIs(self.world.get_agent("legacy-1").character, character)

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
