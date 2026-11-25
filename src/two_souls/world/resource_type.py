from enum import Enum


class ResourceType(str, Enum):
    """Represents the types of resources available in the world."""

    FOOD = "food"
    WATER = "water"
    WOOD = "wood"