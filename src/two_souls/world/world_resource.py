from dataclasses import dataclass

from two_souls.world.position import Position
from two_souls.world.resource_type import ResourceType


@dataclass
class WorldResource:
    """Represents a resource available in the game world."""

    resource_id: str
    resource_type: ResourceType
    position: Position
    quantity: int

    def __post_init__(self) -> None:
        if not self.resource_id.strip():
            raise ValueError("Resource ID cannot be empty.")

        if not isinstance(self.resource_type, ResourceType):
            raise TypeError("Invalid resource type.")

        if not isinstance(self.position, Position):
            raise TypeError("Position must be a Position instance.")

        self._validate_quantity(self.quantity)

    def gather(self, quantity: int) -> bool:
        """Gather resources if enough quantity is available."""

        self._validate_quantity(quantity)

        if self.quantity < quantity:
            return False

        self.quantity -= quantity
        return True

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")