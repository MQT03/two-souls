
from dataclasses import dataclass


@dataclass
class Needs:
    """Represents a character's physical needs and condition."""

    hunger: float = 0.0
    thirst: float = 0.0
    energy: float = 100.0
    health: float = 100.0

    def __setattr__(self, name: str, value: float) -> None:
        if name in {"hunger", "thirst", "energy", "health"}:
            if not 0 <= value <= 100:
                raise ValueError(
                    f"{name} must be between 0 and 100."
                )

        super().__setattr__(name, value)
