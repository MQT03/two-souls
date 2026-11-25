from dataclasses import dataclass, field
from enum import Enum
import math
from types import MappingProxyType
from typing import Mapping, TypeAlias
from uuid import uuid4

from two_souls.world.position import Position


class PerceptionChannel(str, Enum):
    SIGHT = "sight"
    HEARING = "hearing"
    TOUCH = "touch"
    SMELL = "smell"


class ObservationType(str, Enum):
    POTENTIAL_ACTIVITY = "potential_activity"
    RESOURCE_PRESENT = "resource_present"


ObservationMetadataValue: TypeAlias = str | int | float | bool | None


@dataclass(frozen=True)
class Observation:
    """A fallible, agent-specific perception of an event or entity."""

    observation_type: ObservationType
    channel: PerceptionChannel
    description: str
    tick: int
    observation_id: str = field(default_factory=lambda: str(uuid4()))
    source_id: str | None = None
    subject_id: str | None = None
    position: Position | None = None
    confidence: float = 1.0
    metadata: Mapping[str, ObservationMetadataValue] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        if not isinstance(self.observation_type, ObservationType):
            raise TypeError("Observation type must be an ObservationType.")
        if not isinstance(self.channel, PerceptionChannel):
            raise TypeError("Channel must be a PerceptionChannel.")
        if not isinstance(self.observation_id, str) or not self.observation_id.strip():
            raise ValueError("Observation ID cannot be empty.")
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("Observation description cannot be empty.")
        if (
            isinstance(self.tick, bool)
            or not isinstance(self.tick, int)
            or self.tick < 0
        ):
            raise ValueError("Observation tick must be a non-negative integer.")
        if (
            isinstance(self.confidence, bool)
            or not isinstance(self.confidence, (int, float))
            or not math.isfinite(self.confidence)
            or not 0.0 <= self.confidence <= 1.0
        ):
            raise ValueError("Observation confidence must be between 0 and 1.")
        if self.position is not None and not isinstance(self.position, Position):
            raise TypeError("Observation position must be a Position.")

        for identifier in (self.source_id, self.subject_id):
            if identifier is not None and (
                not isinstance(identifier, str) or not identifier.strip()
            ):
                raise ValueError("Observation identifiers cannot be empty.")

        if not isinstance(self.metadata, Mapping):
            raise TypeError("Observation metadata must be a mapping.")
        for key, value in self.metadata.items():
            if not isinstance(key, str):
                raise TypeError("Observation metadata keys must be strings.")
            if not isinstance(value, (str, int, float, bool, type(None))):
                raise TypeError("Observation metadata values must be scalar.")

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )
