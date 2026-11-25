import unittest

from two_souls.world.inventory import Inventory
from two_souls.world.resource_type import ResourceType


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()

    def test_inventory_starts_empty(self):
        self.assertEqual(
            self.inventory.quantity(ResourceType.FOOD),
            0
        )

    def test_add_resource(self):
        self.inventory.add(ResourceType.FOOD, 5)

        self.assertEqual(
            self.inventory.quantity(ResourceType.FOOD),
            5
        )

    def test_add_same_resource_multiple_times(self):
        self.inventory.add(ResourceType.FOOD, 5)
        self.inventory.add(ResourceType.FOOD, 3)

        self.assertEqual(
            self.inventory.quantity(ResourceType.FOOD),
            8
        )

    def test_different_resources_are_independent(self):
        self.inventory.add(ResourceType.FOOD, 5)
        self.inventory.add(ResourceType.WATER, 3)

        self.assertEqual(
            self.inventory.quantity(ResourceType.FOOD),
            5
        )

        self.assertEqual(
            self.inventory.quantity(ResourceType.WATER),
            3
        )

    def test_remove_resource(self):
        self.inventory.add(ResourceType.FOOD, 5)

        result = self.inventory.remove(ResourceType.FOOD, 2)

        self.assertTrue(result)
        self.assertEqual(
            self.inventory.quantity(ResourceType.FOOD),
            3
        )

    def test_remove_more_than_available(self):
        self.inventory.add(ResourceType.FOOD, 5)

        result = self.inventory.remove(ResourceType.FOOD, 10)

        self.assertFalse(result)
        self.assertEqual(
            self.inventory.quantity(ResourceType.FOOD),
            5
        )

    def test_remove_all_resource(self):
        self.inventory.add(ResourceType.FOOD, 5)
        self.inventory.remove(ResourceType.FOOD, 5)

        self.assertEqual(
            self.inventory.quantity(ResourceType.FOOD),
            0
        )

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.inventory.add(ResourceType.FOOD, 0)

        with self.assertRaises(ValueError):
            self.inventory.remove(ResourceType.FOOD, -1)

    def test_non_integer_quantity(self):
        with self.assertRaises(TypeError):
            self.inventory.add(ResourceType.FOOD, 2.5)

    def test_resources_property_returns_copy(self):
        self.inventory.add(ResourceType.FOOD, 5)

        resources = self.inventory.resources
        resources[ResourceType.FOOD] = 100

        self.assertEqual(
            self.inventory.quantity(ResourceType.FOOD),
            5
        )


if __name__ == "__main__":
    unittest.main()