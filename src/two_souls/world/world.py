
from two_souls.world.character import Character
from two_souls.world.world_resource import WorldResource

class World:
    """Represents the game world and manages its characters."""

    def __init__(self) -> None:
        self._characters: dict[str, Character] = {}
        self._resources: dict[str, WorldResource] = {}

    def add_character(self, character: Character) -> None:
        character_id = character.character_id

        if character_id in self._characters:
            raise ValueError(
                f"Character with ID '{character_id}' already exists."
            )

        self._characters[character_id] = character

    def get_character(self, character_id: str) -> Character | None:
        return self._characters.get(character_id)
    @property
    def characters(self) -> tuple[Character, ...]:
        return tuple(self._characters.values())
    @property
    def resources(self) -> tuple[WorldResource, ...]:
        return tuple(self._resources.values())


    def add_resource(self, resource: WorldResource) -> None:
        resource_id = resource.resource_id

        if resource_id in self._resources:
            raise ValueError(
                f"Resource with ID '{resource_id}' already exists."
            )

        self._resources[resource_id] = resource


    def get_resource(self, resource_id: str) -> WorldResource | None:
        return self._resources.get(resource_id)