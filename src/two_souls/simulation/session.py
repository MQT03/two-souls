
from dataclasses import dataclass

from two_souls.events.event_bus import EventBus
from two_souls.simulation.engine import SimulationEngine
from two_souls.simulation.runner import SimulationRunner
from two_souls.simulation.systems.action_system import ActionSystem
from two_souls.simulation.systems.decision_system import DecisionSystem
from two_souls.simulation.systems.needs_system import NeedsSystem
from two_souls.simulation.systems.perception_system import PerceptionSystem
from two_souls.intelligence.agent_mind import Motivation, Value
from two_souls.intelligence.personality import (
    TraitDefinition,
    TraitInstance,
)
from two_souls.world.agent_factory import AgentFactory
from two_souls.world.agent_profile import AgentProfile
from two_souls.world.position import Position
from two_souls.world.world import World


@dataclass
class GameSession:
    """Holds the main components of an active game session."""

    world: World
    engine: SimulationEngine
    runner: SimulationRunner
    event_bus: EventBus


def create_new_game() -> GameSession:
    """Creates and initializes a new game session."""

    world = World()
    event_bus = EventBus()
    agent_factory = AgentFactory()

    adam = agent_factory.create(AgentProfile(
        agent_id="adam-001",
        name="Adam",
        position=Position(10, 20),
        traits={
            name: TraitInstance(
                TraitDefinition(name, float, minimum=0.0, maximum=100.0),
                value,
            )
            for name, value in {
                "sociability": 35.0,
                "kindness": 60.0,
                "curiosity": 45.0,
                "diligence": 85.0,
            }.items()
        },
        values={"diligence": Value("diligence", 0.8)},
        motivations={"contribution": Motivation("contribution", 0.7)},
    ))

    lina = agent_factory.create(AgentProfile(
        agent_id="lina-001",
        name="Lina",
        position=Position(12, 20),
        traits={
            name: TraitInstance(
                TraitDefinition(name, float, minimum=0.0, maximum=100.0),
                value,
            )
            for name, value in {
                "sociability": 85.0,
                "kindness": 80.0,
                "curiosity": 75.0,
                "diligence": 45.0,
            }.items()
        },
        values={"kindness": Value("kindness", 0.8)},
        motivations={"belonging": Motivation("belonging", 0.7)},
    ))

    world.add_agent(adam)
    world.add_agent(lina)

    engine = SimulationEngine()
    perception_system = PerceptionSystem(world, event_bus)

    engine.add_system(NeedsSystem(world))
    engine.add_system(
        DecisionSystem(world),
        update_interval=5
    )
    engine.add_system(ActionSystem(world, event_bus))
    engine.add_system(
        perception_system,
        update_interval=PerceptionSystem.PERIODIC_INTERVAL,
    )

    runner = SimulationRunner(
        engine=engine,
        time_multiplier=1.0
    )

    return GameSession(
        world=world,
        engine=engine,
        runner=runner,
        event_bus=event_bus
    )
