import unittest

from two_souls.world.character import Character
from two_souls.world.position import Position
from two_souls.world.resource_gathering_service import ResourceGatheringService
from two_souls.world.resource_type import ResourceType
from two_souls.world.world import World
from two_souls.world.world_resource import WorldResource


class TestResourceGatheringService(unittest.TestCase):

    def setUp(self):
        self.world = World()

        self.character = Character(
            "adam-001",
            "Adam",
            Position(10, 20)
        )

        self.resource = WorldResource(
            "tree-001",
            ResourceType.WOOD,
            Position(20, 30),
            10
        )

        self.world.add_resource(self.resource)

        self.service = ResourceGatheringService(self.world)

    def test_gather_resource_successfully(self):
        result = self.service.gather(
            self.character,
            "tree-001",
            3
        )

        self.assertTrue(result)

        self.assertEqual(self.resource.quantity, 7)

        self.assertEqual(
            self.character.inventory.quantity(ResourceType.WOOD),
            3
        )

    def test_gather_all_available_resources(self):
        result = self.service.gather(
            self.character,
            "tree-001",
            10
        )

        self.assertTrue(result)
        self.assertEqual(self.resource.quantity, 0)
        self.assertEqual(
            self.character.inventory.quantity(ResourceType.WOOD),
            10
        )

    def test_gather_nonexistent_resource(self):
        result = self.service.gather(
            self.character,
            "missing-resource",
            3
        )

        self.assertFalse(result)
        self.assertEqual(
            self.character.inventory.quantity(ResourceType.WOOD),
            0
        )

    def test_gather_more_than_available(self):
        result = self.service.gather(
            self.character,
            "tree-001",
            15
        )

        self.assertFalse(result)
        self.assertEqual(self.resource.quantity, 10)
        self.assertEqual(
            self.character.inventory.quantity(ResourceType.WOOD),
            0
        )

    def test_invalid_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            self.service.gather(
                self.character,
                "tree-001",
                0
            )

        with self.assertRaises(ValueError):
            self.service.gather(
                self.character,
                "tree-001",
                -1
            )

    def test_non_integer_quantity_is_rejected(self):
        with self.assertRaises(TypeError):
            self.service.gather(
                self.character,
                "tree-001",
                2.5
            )

    def test_gathered_resources_are_added_to_correct_inventory(self):
        lina = Character(
            "lina-001",
            "Lina",
            Position(12, 20)
        )

        self.service.gather(
            self.character,
            "tree-001",
            4
        )

        self.assertEqual(
            self.character.inventory.quantity(ResourceType.WOOD),
            4
        )

        self.assertEqual(
            lina.inventory.quantity(ResourceType.WOOD),
            0
        )


if __name__ == "__main__":
    unittest.main()