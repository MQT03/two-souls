
from dataclasses import dataclass


@dataclass
class Personality:
    """Represents a character's personality traits."""

    sociability: float = 50.0
    kindness: float = 50.0
    curiosity: float = 50.0
    diligence: float = 50.0

    def __setattr__(self, name: str, value: float) -> None:
        if name in {
            "sociability",
            "kindness",
            "curiosity",
            "diligence"
        }:
            if not 0 <= value <= 100:
                raise ValueError(
                    f"{name} must be between 0 and 100."
                )

        super().__setattr__(name, value)
