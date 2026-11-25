from two_souls.world.character import Character
from two_souls.world.resource_type import ResourceType
from two_souls.world.world import World


class ResourceGatheringService:
    """Coordinates gathering resources from the world into an inventory."""

    def __init__(self, world: World) -> None:
        self._world = world

    def gather(
        self,
        character: Character,
        resource_id: str,
        quantity: int
    ) -> bool:
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        resource = self._world.get_resource(resource_id)

        if resource is None:
            return False

        resource_type: ResourceType = resource.resource_type

        if not resource.gather(quantity):
            return False

        character.inventory.add(resource_type, quantity)

        return True