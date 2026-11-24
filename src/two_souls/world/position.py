
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """Represents an object's position in the game world."""

    x: float
    y: float
