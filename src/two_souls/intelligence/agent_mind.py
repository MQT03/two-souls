from dataclasses import dataclass, field

from two_souls.intelligence.observation import Observation
from two_souls.intelligence.personality import Personality
from two_souls.world.character_decision import CharacterDecision


@dataclass
class Value:
    name: str
    importance: float = 0.5


@dataclass
class Motivation:
    name: str
    strength: float = 0.5


@dataclass
class Emotion:
    name: str
    intensity: float = 0.0


@dataclass
class Preference:
    subject: str
    preference: float


@dataclass
class KnowledgeItem:
    topic: str
    content: str


@dataclass
class Belief:
    proposition: str
    confidence: float = 0.5


@dataclass
class Memory:
    content: str
    tick: int | None = None


@dataclass
class Skill:
    name: str
    level: float = 0.0


@dataclass
class AgentMind:
    """Cognitive state for one agent; it has no reference to the World."""

    personality: Personality = field(default_factory=Personality)
    values: dict[str, Value] = field(default_factory=dict)
    motivations: dict[str, Motivation] = field(default_factory=dict)
    emotions: dict[str, Emotion] = field(default_factory=dict)
    preferences: dict[str, Preference] = field(default_factory=dict)
    knowledge: dict[str, KnowledgeItem] = field(default_factory=dict)
    beliefs: dict[str, Belief] = field(default_factory=dict)
    memories: list[Memory] = field(default_factory=list)
    skills: dict[str, Skill] = field(default_factory=dict)
    decision: CharacterDecision = CharacterDecision.IDLE
    decision_revision: int = 0
    _observations: list[Observation] = field(
        default_factory=list,
        init=False,
        repr=False,
    )
    _observation_ids: set[str] = field(
        default_factory=set,
        init=False,
        repr=False,
    )

    @property
    def observations(self) -> tuple[Observation, ...]:
        return tuple(self._observations)

    def receive_observation(self, observation: Observation) -> bool:
        if not isinstance(observation, Observation):
            raise TypeError("AgentMind can only receive Observation instances.")
        if observation.observation_id in self._observation_ids:
            return False

        self._observation_ids.add(observation.observation_id)
        self._observations.append(observation)
        return True
