
from dataclasses import dataclass

from two_souls.simulation.engine import SimulationEngine
from two_souls.simulation.runner import SimulationRunner
from two_souls.simulation.systems.action_system import ActionSystem
from two_souls.simulation.systems.decision_system import DecisionSystem
from two_souls.simulation.systems.needs_system import NeedsSystem
from two_souls.world.character import Character
from two_souls.world.personality import Personality
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
        position=Position(10, 20),
        personality=Personality(
            sociability=35,
            kindness=60,
            curiosity=45,
            diligence=85
        )
    )

    lina = Character(
        character_id="lina-001",
        name="Lina",
        position=Position(12, 20),
        personality=Personality(
            sociability=85,
            kindness=80,
            curiosity=75,
            diligence=45
        )
    )

    world.add_character(adam)
    world.add_character(lina)

    engine = SimulationEngine()
    engine.add_system(NeedsSystem(world))
    engine.add_system(
    DecisionSystem(world),
    update_interval=5
    )
    engine.add_system(ActionSystem(world))
    runner = SimulationRunner(
        engine=engine,
        time_multiplier=1.0
    )

    return GameSession(
        world=world,
        engine=engine,
        runner=runner
    )
