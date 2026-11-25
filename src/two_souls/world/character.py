from dataclasses import dataclass, field

from two_souls.world.character_action import CharacterAction
from two_souls.world.character_state import CharacterState
from two_souls.world.needs import Needs
from two_souls.world.position import Position
from two_souls.world.inventory import Inventory

@dataclass
class Character:
    """Represents an individual character in the world."""

    character_id: str
    name: str
    position: Position

    needs: Needs = field(default_factory=Needs)
    state: CharacterState = CharacterState.IDLE
    current_action: CharacterAction | None = None
    inventory: Inventory = field(default_factory=Inventory)
