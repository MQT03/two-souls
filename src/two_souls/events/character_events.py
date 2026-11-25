from dataclasses import dataclass

from two_souls.world.character_decision import CharacterDecision


@dataclass(frozen=True)
class CharacterActionCompleted:
    """Represents the completion of a character action."""

    character_id: str
    decision: CharacterDecision
    tick: int