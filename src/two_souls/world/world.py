
from two_souls.world.character import Character


class World:
    """Represents the game world and manages its characters."""

    def __init__(self) -> None:
        self._characters: dict[str, Character] = {}

    def add_character(self, character: Character) -> None:
        character_id = character.character_id

        if character_id in self._characters:
            raise ValueError(
                f"Character with ID '{character_id}' already exists."
            )

        self._characters[character_id] = character

    def get_character(self, character_id: str) -> Character | None:
        return self._characters.get(character_id)
