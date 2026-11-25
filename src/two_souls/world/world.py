
from two_souls.intelligence.agent_mind import AgentMind
from two_souls.world.agent import Agent
from two_souls.world.character import Character
from two_souls.world.world_resource import WorldResource


class World:
    """Represents the world and manages its agents and resources."""

    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}
        self._resources: dict[str, WorldResource] = {}

    def add_agent(self, agent: Agent) -> None:
        if not isinstance(agent, Agent):
            raise TypeError("World can only manage Agent instances.")

        agent_id = agent.agent_id
        if agent_id in self._agents:
            raise ValueError(f"Agent with ID '{agent_id}' already exists.")

        self._agents[agent_id] = agent

    def get_agent(self, agent_id: str) -> Agent | None:
        return self._agents.get(agent_id)

    @property
    def agents(self) -> tuple[Agent, ...]:
        return tuple(self._agents.values())

    def add_character(self, character: Character) -> None:
        """Compatibility adapter that registers a Character inside an Agent."""
        self.add_agent(Agent(character=character, mind=AgentMind()))

    def get_character(self, character_id: str) -> Character | None:
        """Compatibility lookup returning the physical side of an Agent."""
        agent = self.get_agent(character_id)
        return agent.character if agent is not None else None

    @property
    def characters(self) -> tuple[Character, ...]:
        """Read-only legacy projection; Agents remain the source of truth."""
        return tuple(agent.character for agent in self._agents.values())

    @property
    def resources(self) -> tuple[WorldResource, ...]:
        return tuple(self._resources.values())

    def add_resource(self, resource: WorldResource) -> None:
        resource_id = resource.resource_id

        if resource_id in self._resources:
            raise ValueError(
                f"Resource with ID '{resource_id}' already exists."
            )

        self._resources[resource_id] = resource

    def get_resource(self, resource_id: str) -> WorldResource | None:
        return self._resources.get(resource_id)