from two_souls.simulation.system import SimulationSystem
from two_souls.world.character_decision import CharacterDecision
from two_souls.world.agent import Agent
from two_souls.world.world import World


class DecisionSystem(SimulationSystem):
    """Evaluates physical needs and AgentMind personality to select decisions."""

    NEED_THRESHOLD = 60.0
    ENERGY_THRESHOLD = 40.0

    def __init__(self, world: World) -> None:
        self._world = world

    def update(self, tick: int) -> None:
        for agent in self._world.agents:
            agent.mind.decision = self._choose_decision(agent)
            agent.mind.decision_revision += 1

    def _choose_decision(self, agent: Agent) -> CharacterDecision:
        character = agent.character
        needs = character.needs
        personality = agent.mind.personality

        scores = {
            CharacterDecision.WORK:
                20.0 + personality.numeric_value("diligence") * 0.6,

            CharacterDecision.SOCIALIZE:
                20.0 + personality.numeric_value("sociability") * 0.6,

            CharacterDecision.EXPLORE:
                20.0 + personality.numeric_value("curiosity") * 0.6,
        }

        if needs.energy <= self.ENERGY_THRESHOLD:
            scores[CharacterDecision.REST] = (
                85.0 + (self.ENERGY_THRESHOLD - needs.energy) * 0.375
            )

        if needs.hunger >= self.NEED_THRESHOLD:
            scores[CharacterDecision.SEEK_FOOD] = (
                85.0 + (needs.hunger - self.NEED_THRESHOLD) * 0.375
            )

        if needs.thirst >= self.NEED_THRESHOLD:
            scores[CharacterDecision.SEEK_WATER] = (
                85.0 + (needs.thirst - self.NEED_THRESHOLD) * 0.375
            )

        return max(scores, key=scores.get)