from enum import Enum


class CharacterDecision(str, Enum):
    """Represents a character's intended next activity."""

    IDLE = "idle"
    REST = "rest"
    SEEK_FOOD = "seek_food"
    SEEK_WATER = "seek_water"
    WORK = "work"
    SOCIALIZE = "socialize"
    EXPLORE = "explore"