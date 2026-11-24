
from enum import Enum


class CharacterState(str, Enum):
    """Represents a character's current activity."""

    IDLE = "idle"
    SLEEPING = "sleeping"
    EATING = "eating"
    WORKING = "working"
    SOCIALIZING = "socializing"
    EXPLORING = "exploring"
    SEEKING_FOOD = "seeking_food"
    SEEKING_WATER = "seeking_water"