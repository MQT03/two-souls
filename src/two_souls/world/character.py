
from dataclasses import dataclass

from two_souls.world.position import Position


@dataclass
class Character:
    """Represents an individual character in the world."""

    character_id: str
    name: str
    position: Position
