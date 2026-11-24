
from dataclasses import dataclass, field

from two_souls.world.position import Position
from two_souls.world.needs import Needs
from two_souls.world.personality import Personality
from two_souls.world.character_state import CharacterState


@dataclass
class Character:
    """Represents an individual character in the world."""

    character_id: str
    name: str
    position: Position

    needs: Needs = field(default_factory=Needs)
    personality: Personality = field(default_factory=Personality)
    state: CharacterState = CharacterState.IDLE
