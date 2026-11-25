from copy import deepcopy

from two_souls.intelligence.agent_mind import AgentMind
from two_souls.intelligence.personality import Personality
from two_souls.world.agent import Agent
from two_souls.world.agent_profile import AgentProfile
from two_souls.world.character import Character
from two_souls.world.inventory import Inventory
from two_souls.world.needs import Needs


class AgentFactory:
    """Creates independent Agent aggregates from initial-state profiles."""

    def create(self, profile: AgentProfile) -> Agent:
        if not isinstance(profile, AgentProfile):
            raise TypeError("Profile must be an AgentProfile.")

        character = Character(
            character_id=profile.agent_id,
            name=profile.name,
            position=deepcopy(profile.position),
            needs=deepcopy(profile.needs),
            inventory=self._copy_inventory(profile.inventory),
        )
        mind = AgentMind(
            personality=Personality.with_traits(deepcopy(profile.traits)),
            values=deepcopy(profile.values),
            motivations=deepcopy(profile.motivations),
            emotions=deepcopy(profile.emotions),
            preferences=deepcopy(profile.preferences),
            knowledge=deepcopy(profile.knowledge),
            beliefs=deepcopy(profile.beliefs),
            memories=deepcopy(profile.memories),
            skills=deepcopy(profile.skills),
        )
        return Agent(character=character, mind=mind)

    @staticmethod
    def _copy_inventory(inventory: Inventory) -> Inventory:
        if not isinstance(inventory, Inventory):
            raise TypeError("Profile inventory must be an Inventory.")
        copied = Inventory()
        for resource, quantity in inventory.resources.items():
            copied.add(resource, quantity)
        return copied
