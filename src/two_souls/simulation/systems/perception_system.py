import math
from uuid import NAMESPACE_URL, uuid5

from two_souls.events.character_events import CharacterActionCompleted
from two_souls.events.event_bus import EventBus
from two_souls.intelligence.observation import (
    Observation,
    ObservationType,
    PerceptionChannel,
)
from two_souls.simulation.system import SimulationSystem
from two_souls.world.agent import Agent
from two_souls.world.position import Position
from two_souls.world.world import World


class PerceptionSystem(SimulationSystem):
    """Delivers limited world observations to individual AgentMinds."""

    PERIODIC_INTERVAL = 10
    DEFAULT_SIGHT_RANGE = 10.0

    def __init__(
        self,
        world: World,
        event_bus: EventBus,
        sight_range: float = DEFAULT_SIGHT_RANGE,
    ) -> None:
        if (
            isinstance(sight_range, bool)
            or not isinstance(sight_range, (int, float))
            or not math.isfinite(sight_range)
            or sight_range < 0
        ):
            raise ValueError("Sight range must be a non-negative number.")

        self._world = world
        self._sight_range = float(sight_range)
        self._visible_resources: dict[
            str,
            dict[str, tuple[str, int, float, float]],
        ] = {}
        event_bus.subscribe(
            CharacterActionCompleted,
            self._observe_completed_action,
        )

    def update(self, tick: int) -> None:
        if tick % self.PERIODIC_INTERVAL != 0:
            return

        for observer in self._world.agents:
            previous_visible = self._visible_resources.get(
                observer.agent_id,
                {},
            )
            current_visible: dict[str, tuple[str, int, float, float]] = {}

            for resource in self._world.resources:
                if resource.quantity <= 0:
                    continue
                if not self._can_see(observer, resource.position):
                    continue

                resource_state = (
                    resource.resource_type.value,
                    resource.quantity,
                    resource.position.x,
                    resource.position.y,
                )
                previous_state = previous_visible.get(resource.resource_id)
                current_visible[resource.resource_id] = resource_state
                if previous_state == resource_state:
                    continue

                state_changed = previous_state is not None
                description = (
                    f"A {resource.resource_type.value} resource may be "
                    "visible nearby."
                )
                if state_changed:
                    description = (
                        f"A nearby {resource.resource_type.value} resource "
                        "appears different from before."
                    )

                observer.mind.receive_observation(
                    Observation(
                        observation_type=ObservationType.RESOURCE_PRESENT,
                        channel=PerceptionChannel.SIGHT,
                        description=description,
                        tick=tick,
                        observation_id=self._observation_id(
                            "resource",
                            observer.agent_id,
                            resource.resource_id,
                            tick,
                            resource_state,
                        ),
                        subject_id=resource.resource_id,
                        position=resource.position,
                        confidence=0.5,
                        metadata={
                            "resource_type": resource.resource_type.value,
                            "state_changed": state_changed,
                            "visual_attention_confirmed": False,
                        },
                    )
                )

            self._visible_resources[observer.agent_id] = current_visible

    def _observe_completed_action(
        self,
        event: CharacterActionCompleted,
    ) -> None:
        source = self._world.get_agent(event.character_id)
        if source is None:
            return

        position = source.character.position
        for observer in self._world.agents:
            if observer is source or not self._can_see(observer, position):
                continue

            observer.mind.receive_observation(
                Observation(
                    observation_type=ObservationType.POTENTIAL_ACTIVITY,
                    channel=PerceptionChannel.SIGHT,
                    description=(
                        "A nearby agent may have performed an activity "
                        "associated with "
                        f"{event.decision.value.replace('_', ' ')}; actual "
                        "visual attention is not modeled."
                    ),
                    tick=event.tick,
                    observation_id=self._observation_id(
                        "action",
                        observer.agent_id,
                        event.character_id,
                        event.decision.value,
                        event.tick,
                    ),
                    source_id=event.character_id,
                    position=position,
                    confidence=0.5,
                    metadata={
                        "simulated_activity": event.decision.value,
                        "visual_attention_confirmed": False,
                    },
                )
            )

    def _can_see(self, observer: Agent, position: Position) -> bool:
        distance = math.hypot(
            observer.character.position.x - position.x,
            observer.character.position.y - position.y,
        )
        return distance <= self._sight_range

    @staticmethod
    def _observation_id(*parts: object) -> str:
        return str(uuid5(NAMESPACE_URL, repr(("two-souls", *parts))))
