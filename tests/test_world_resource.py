import unittest

from two_souls.world.position import Position
from two_souls.world.resource_type import ResourceType
from two_souls.world.world_resource import WorldResource


class TestWorldResource(unittest.TestCase):

    def setUp(self):
        self.resource = WorldResource(
            resource_id="tree-001",
            resource_type=ResourceType.WOOD,
            position=Position(20, 30),
            quantity=10
        )

    def test_resource_has_initial_values(self):
        self.assertEqual(self.resource.resource_id, "tree-001")
        self.assertEqual(self.resource.resource_type, ResourceType.WOOD)
        self.assertEqual(self.resource.quantity, 10)

    def test_gather_resource(self):
        result = self.resource.gather(3)

        self.assertTrue(result)
        self.assertEqual(self.resource.quantity, 7)

    def test_gather_all_resources(self):
        result = self.resource.gather(10)

        self.assertTrue(result)
        self.assertEqual(self.resource.quantity, 0)

    def test_gather_more_than_available(self):
        result = self.resource.gather(15)

        self.assertFalse(result)
        self.assertEqual(self.resource.quantity, 10)

    def test_gather_from_empty_resource(self):
        self.resource.gather(10)

        result = self.resource.gather(1)

        self.assertFalse(result)
        self.assertEqual(self.resource.quantity, 0)

    def test_negative_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            WorldResource(
                "tree-002",
                ResourceType.WOOD,
                Position(20, 30),
                -1
            )

    def test_non_integer_quantity_is_rejected(self):
        with self.assertRaises(TypeError):
            self.resource.gather(2.5)

    def test_zero_quantity_is_allowed(self):
        resource = WorldResource(
            "tree-003",
            ResourceType.WOOD,
            Position(20, 30),
            0
        )

        self.assertEqual(resource.quantity, 0)

    def test_empty_resource_id_is_rejected(self):
        with self.assertRaises(ValueError):
            WorldResource(
                " ",
                ResourceType.WOOD,
                Position(20, 30),
                10
            )


if __name__ == "__main__":
    unittest.main()