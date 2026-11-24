from two_souls.simulation.system import SimulationSystem
from two_souls.world.character_decision import CharacterDecision
from two_souls.world.world import World


class DecisionSystem(SimulationSystem):
    """Evaluates character needs and personality to select decisions."""

    NEED_THRESHOLD = 60.0
    ENERGY_THRESHOLD = 40.0

    def __init__(self, world: World) -> None:
        self._world = world

    def update(self, tick: int) -> None:
        for character in self._world.characters:
            character.decision = self._choose_decision(character)

    def _choose_decision(self, character):
        needs = character.needs
        personality = character.personality

        scores = {
            CharacterDecision.WORK:
                20.0 + personality.diligence * 0.6,

            CharacterDecision.SOCIALIZE:
                20.0 + personality.sociability * 0.6,

            CharacterDecision.EXPLORE:
                20.0 + personality.curiosity * 0.6,
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