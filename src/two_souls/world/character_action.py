
from dataclasses import dataclass

from two_souls.world.character_decision import CharacterDecision


@dataclass
class CharacterAction:
    """Represents an activity being performed by a character."""

    decision: CharacterDecision
    duration_ticks: int
    elapsed_ticks: int = 0
    decision_revision: int = 0

    def __post_init__(self) -> None:
        if self.duration_ticks < 1:
            raise ValueError("Action duration must be at least 1.")

        if not 0 <= self.elapsed_ticks <= self.duration_ticks:
            raise ValueError("Invalid action progress.")

    @property
    def is_complete(self) -> bool:
        return self.elapsed_ticks >= self.duration_ticks

    @property
    def remaining_ticks(self) -> int:
        return self.duration_ticks - self.elapsed_ticks

    def advance(self) -> bool:
        """Advance the action by one simulation tick."""

        if not self.is_complete:
            self.elapsed_ticks += 1

        return self.is_complete
