
from dataclasses import dataclass

from two_souls.simulation.engine import SimulationEngine
from two_souls.simulation.runner import SimulationRunner
from two_souls.simulation.systems.needs_system import NeedsSystem
from two_souls.world.character import Character
from two_souls.world.position import Position
from two_souls.world.world import World


@dataclass
class GameSession:
    """Holds the main components of an active game session."""

    world: World
    engine: SimulationEngine
    runner: SimulationRunner


def create_new_game() -> GameSession:
    """Creates and initializes a new game session."""

    world = World()

    adam = Character(
        character_id="adam-001",
        name="Adam",
        position=Position(10, 20)
    )

    lina = Character(
        character_id="lina-001",
        name="Lina",
        position=Position(12, 20)
    )

    world.add_character(adam)
    world.add_character(lina)

    engine = SimulationEngine()
    engine.add_system(NeedsSystem(world))

    runner = SimulationRunner(
        engine=engine,
        time_multiplier=1.0
    )

    return GameSession(
        world=world,
        engine=engine,
        runner=runner
    )
