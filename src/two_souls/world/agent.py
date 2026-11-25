from dataclasses import dataclass, field

from two_souls.intelligence.agent_mind import AgentMind
from two_souls.world.character import Character


@dataclass
class Agent:
    """Aggregate root joining one physical Character with one AgentMind."""

    character: Character
    mind: AgentMind = field(default_factory=AgentMind)

    def __post_init__(self) -> None:
        if not isinstance(self.character, Character):
            raise TypeError("Agent must own a Character.")
        if not isinstance(self.mind, AgentMind):
            raise TypeError("Agent must own an AgentMind.")

    @property
    def agent_id(self) -> str:
        return self.character.character_id
