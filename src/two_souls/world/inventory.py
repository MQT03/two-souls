from two_souls.world.resource_type import ResourceType


class Inventory:
    """Manages the resources owned by a character."""

    def __init__(self) -> None:
        self._resources: dict[ResourceType, int] = {}

    @property
    def resources(self) -> dict[ResourceType, int]:
        return self._resources.copy()

    def quantity(self, resource: ResourceType) -> int:
        self._validate_resource(resource)
        return self._resources.get(resource, 0)

    def add(self, resource: ResourceType, quantity: int) -> None:
        self._validate_resource(resource)
        self._validate_quantity(quantity)

        current_quantity = self.quantity(resource)
        self._resources[resource] = current_quantity + quantity

    def remove(self, resource: ResourceType, quantity: int) -> bool:
        self._validate_resource(resource)
        self._validate_quantity(quantity)

        current_quantity = self.quantity(resource)

        if current_quantity < quantity:
            return False

        remaining_quantity = current_quantity - quantity

        if remaining_quantity == 0:
            del self._resources[resource]
        else:
            self._resources[resource] = remaining_quantity

        return True

    @staticmethod
    def _validate_resource(resource: ResourceType) -> None:
        if not isinstance(resource, ResourceType):
            raise TypeError("Resource must be a ResourceType.")

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")