
from two_souls.simulation.system import SimulationSystem
from two_souls.world.character_state import CharacterState
from two_souls.world.world import World


class NeedsSystem(SimulationSystem):
    """Updates the physical needs of all characters."""

    HUNGER_RATE = 0.05
    THIRST_RATE = 0.08
    ENERGY_DRAIN_RATE = 0.05
    SLEEP_RECOVERY_RATE = 0.15

    def __init__(self, world: World) -> None:
        self._world = world

    def update(self, tick: int) -> None:
        for character in self._world.characters:
            needs = character.needs

            needs.hunger = min(
                100.0,
                needs.hunger + self.HUNGER_RATE
            )

            needs.thirst = min(
                100.0,
                needs.thirst + self.THIRST_RATE
            )

            if character.state == CharacterState.SLEEPING:
                needs.energy = min(
                    100.0,
                    needs.energy + self.SLEEP_RECOVERY_RATE
                )
            else:
                needs.energy = max(
                    0.0,
                    needs.energy - self.ENERGY_DRAIN_RATE
                )
