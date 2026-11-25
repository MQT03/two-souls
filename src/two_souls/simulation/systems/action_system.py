
from two_souls.simulation.system import SimulationSystem
from two_souls.world.character_action import CharacterAction
from two_souls.world.agent import Agent
from two_souls.world.character_decision import CharacterDecision
from two_souls.world.character_state import CharacterState
from two_souls.world.world import World
from two_souls.events.event_bus import EventBus
from two_souls.events.character_events import CharacterActionCompleted

class ActionSystem(SimulationSystem):
    """Manages the execution of character activities."""

    ACTION_CONFIG = {
        CharacterDecision.REST: (
            CharacterState.SLEEPING, 60
        ),
        CharacterDecision.WORK: (
            CharacterState.WORKING, 120
        ),
        CharacterDecision.SOCIALIZE: (
            CharacterState.SOCIALIZING, 60
        ),
        CharacterDecision.EXPLORE: (
            CharacterState.EXPLORING, 90
        ),
        CharacterDecision.SEEK_FOOD: (
            CharacterState.SEEKING_FOOD, 30
        ),
        CharacterDecision.SEEK_WATER: (
            CharacterState.SEEKING_WATER, 30
        ),
    }

    def __init__(self, world: World, event_bus: EventBus) -> None:
        self._world = world
        self._event_bus = event_bus

    def update(self, tick: int) -> None:
        for agent in self._world.agents:
            self._update_agent(agent, tick)

    def _update_agent(self, agent: Agent, tick: int) -> None:
        character = agent.character
        mind = agent.mind
        decision = mind.decision
        action = character.current_action

        if decision == CharacterDecision.IDLE:
            character.current_action = None
            character.state = CharacterState.IDLE
            return

        should_start_action = (
            action is None
            or action.decision != decision
            or (
                action.is_complete
                and mind.decision_revision > action.decision_revision
            )
        )

        if should_start_action:
            state, duration = self.ACTION_CONFIG[decision]

            action = CharacterAction(
                decision=decision,
                duration_ticks=duration,
                decision_revision=mind.decision_revision
            )

            character.current_action = action
            character.state = state

        elif action.is_complete:
            character.state = CharacterState.IDLE
            return

        if action.advance():
            action.decision_revision = mind.decision_revision
            character.state = CharacterState.IDLE

            self._event_bus.publish(
                CharacterActionCompleted(
                    character_id=character.character_id,
                    decision=action.decision,
                    tick=tick
                )
            )