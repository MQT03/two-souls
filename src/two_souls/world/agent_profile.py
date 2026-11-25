from dataclasses import dataclass, field

from two_souls.intelligence.agent_mind import (
    Belief,
    Emotion,
    KnowledgeItem,
    Memory,
    Motivation,
    Preference,
    Skill,
    Value,
)
from two_souls.intelligence.personality import TraitInstance
from two_souls.world.inventory import Inventory
from two_souls.world.needs import Needs
from two_souls.world.position import Position


@dataclass
class AgentProfile:
    """Initial physical and cognitive state used to create an Agent."""

    agent_id: str
    name: str
    position: Position
    needs: Needs = field(default_factory=Needs)
    inventory: Inventory = field(default_factory=Inventory)
    traits: dict[str, TraitInstance] = field(default_factory=dict)
    values: dict[str, Value] = field(default_factory=dict)
    motivations: dict[str, Motivation] = field(default_factory=dict)
    emotions: dict[str, Emotion] = field(default_factory=dict)
    preferences: dict[str, Preference] = field(default_factory=dict)
    knowledge: dict[str, KnowledgeItem] = field(default_factory=dict)
    beliefs: dict[str, Belief] = field(default_factory=dict)
    memories: list[Memory] = field(default_factory=list)
    skills: dict[str, Skill] = field(default_factory=dict)
