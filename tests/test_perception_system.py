import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import patch
from uuid import UUID

from two_souls.events.character_events import CharacterActionCompleted
from two_souls.events.event_bus import EventBus
from two_souls.intelligence.agent_mind import AgentMind
from two_souls.intelligence.observation import (
    Observation,
    ObservationType,
    PerceptionChannel,
)
from two_souls.simulation.session import create_new_game
from two_souls.simulation.systems.perception_system import PerceptionSystem
from two_souls.world.agent import Agent
from two_souls.world.character import Character
from two_souls.world.character_decision import CharacterDecision
from two_souls.world.position import Position
from two_souls.world.resource_type import ResourceType
from two_souls.world.world import World
from two_souls.world.world_resource import WorldResource


class TestObservation(unittest.TestCase):

    def test_observation_has_typed_fields_and_a_unique_default_id(self):
        with patch(
            "two_souls.intelligence.observation.uuid4",
            side_effect=(UUID(int=1), UUID(int=2)),
        ):
            first = Observation(
                observation_type=ObservationType.RESOURCE_PRESENT,
                channel=PerceptionChannel.SIGHT,
                description="A resource is nearby.",
                tick=4,
                subject_id="resource-1",
                position=Position(2, 3),
                metadata={"visible": True},
            )
            second = Observation(
                observation_type=ObservationType.RESOURCE_PRESENT,
                channel=PerceptionChannel.SIGHT,
                description="A resource is nearby.",
                tick=4,
            )

        self.assertNotEqual(first.observation_id, second.observation_id)
        self.assertEqual(first.subject_id, "resource-1")
        self.assertEqual(first.position, Position(2, 3))
        self.assertEqual(first.metadata["visible"], True)

    def test_observation_position_cannot_be_mutated_indirectly(self):
        position = Position(2, 3)
        observation = Observation(
            observation_type=ObservationType.RESOURCE_PRESENT,
            channel=PerceptionChannel.SIGHT,
            description="A resource may be visible.",
            tick=4,
            position=position,
        )

        with self.assertRaises(FrozenInstanceError):
            observation.position.x = 99
        self.assertEqual(position, Position(2, 3))

    def test_observation_validates_required_fields_and_ranges(self):
        arguments = {
            "observation_type": ObservationType.POTENTIAL_ACTIVITY,
            "channel": PerceptionChannel.HEARING,
            "description": "A distant sound was heard.",
            "tick": 2,
        }

        with self.assertRaises(ValueError):
            Observation(**{**arguments, "tick": -1})
        with self.assertRaises(ValueError):
            Observation(**{**arguments, "confidence": 1.1})
        with self.assertRaises(ValueError):
            Observation(**{**arguments, "description": " "})
        with self.assertRaises(TypeError):
            Observation(**{**arguments, "channel": "hearing"})

    def test_perception_channels_include_supported_senses(self):
        self.assertEqual(
            set(PerceptionChannel),
            {
                PerceptionChannel.SIGHT,
                PerceptionChannel.HEARING,
                PerceptionChannel.TOUCH,
                PerceptionChannel.SMELL,
            },
        )

    def test_agent_mind_receives_observations_without_world_access(self):
        mind = AgentMind()
        observation = Observation(
            observation_type=ObservationType.POTENTIAL_ACTIVITY,
            channel=PerceptionChannel.SIGHT,
            description="Someone completed an action.",
            tick=8,
        )

        self.assertTrue(mind.receive_observation(observation))
        self.assertEqual(mind.observations, (observation,))
        self.assertFalse(hasattr(mind, "world"))
        self.assertNotIn("world", AgentMind.__dataclass_fields__)
        with self.assertRaises(AttributeError):
            mind.observations.append(observation)
        with self.assertRaises(TypeError):
            mind.receive_observation("not an observation")

    def test_minds_reject_duplicate_observation_ids_independently(self):
        first = AgentMind()
        second = AgentMind()
        observation = Observation(
            observation_type=ObservationType.POTENTIAL_ACTIVITY,
            channel=PerceptionChannel.SIGHT,
            description="Someone completed an action.",
            tick=8,
            observation_id="observation-1",
        )

        self.assertTrue(first.receive_observation(observation))
        self.assertFalse(first.receive_observation(observation))
        self.assertTrue(second.receive_observation(observation))
        self.assertEqual(first.observations, (observation,))
        self.assertEqual(second.observations, (observation,))
        self.assertIsNot(first._observations, second._observations)


class TestPerceptionSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.source = Agent(
            Character("source", "Source", Position(0, 0))
        )
        self.near = Agent(
            Character("near", "Near", Position(3, 4))
        )
        self.far = Agent(
            Character("far", "Far", Position(5.1, 0))
        )
        self.world.add_agent(self.source)
        self.world.add_agent(self.near)
        self.world.add_agent(self.far)
        self.event_bus = EventBus()
        self.system = PerceptionSystem(
            self.world,
            self.event_bus,
            sight_range=5,
        )

    def test_sight_event_reaches_in_range_agent_only_with_event_tick(self):
        event = CharacterActionCompleted(
            character_id="source",
            decision=CharacterDecision.WORK,
            tick=17,
        )

        self.event_bus.publish(event)

        self.assertEqual(self.source.mind.observations, ())
        self.assertEqual(self.far.mind.observations, ())
        self.assertEqual(len(self.near.mind.observations), 1)

        observation = self.near.mind.observations[0]
        self.assertEqual(
            observation.observation_type,
            ObservationType.POTENTIAL_ACTIVITY,
        )
        self.assertEqual(observation.channel, PerceptionChannel.SIGHT)
        self.assertEqual(observation.source_id, "source")
        self.assertEqual(observation.tick, 17)
        self.assertEqual(observation.position, Position(0, 0))
        self.assertEqual(observation.metadata["simulated_activity"], "work")
        self.assertFalse(observation.metadata["visual_attention_confirmed"])
        self.assertEqual(observation.confidence, 0.5)
        self.assertIn("may have performed", observation.description)
        self.assertNotIn("completed", observation.description)

    def test_republishing_same_event_does_not_duplicate_observations(self):
        event = CharacterActionCompleted(
            character_id="source",
            decision=CharacterDecision.WORK,
            tick=17,
        )

        self.event_bus.publish(event)
        self.event_bus.publish(event)

        self.assertEqual(len(self.near.mind.observations), 1)

    def test_repeated_periodic_sight_does_not_repeat_unchanged_resource(self):
        resource = WorldResource(
            resource_id="wood-1",
            resource_type=ResourceType.WOOD,
            position=Position(3, 5),
            quantity=8,
        )
        self.world.add_resource(resource)

        self.system.update(10)
        self.system.update(20)
        self.system.update(30)

        self.assertEqual(len(self.near.mind.observations), 1)
        self.assertEqual(self.far.mind.observations, ())

        observation = self.near.mind.observations[0]
        self.assertEqual(
            observation.observation_type,
            ObservationType.RESOURCE_PRESENT,
        )
        self.assertEqual(observation.subject_id, "wood-1")
        self.assertEqual(observation.tick, 10)
        self.assertFalse(observation.metadata["visual_attention_confirmed"])
        self.assertEqual(observation.confidence, 0.5)

    def test_periodic_sight_ignores_depleted_resources(self):
        self.world.add_resource(
            WorldResource(
                resource_id="empty-wood",
                resource_type=ResourceType.WOOD,
                position=Position(3, 5),
                quantity=0,
            )
        )

        self.system.update(10)

        self.assertEqual(self.near.mind.observations, ())

    def test_reentering_range_creates_a_new_resource_observation(self):
        self.world.add_resource(
            WorldResource(
                resource_id="wood-1",
                resource_type=ResourceType.WOOD,
                position=Position(3, 5),
                quantity=8,
            )
        )

        self.system.update(10)
        first_observation = self.near.mind.observations[0]

        self.near.character.position = Position(20, 20)
        self.system.update(20)
        self.near.character.position = Position(3, 4)
        self.system.update(30)

        observations = self.near.mind.observations
        self.assertEqual(len(observations), 2)
        self.assertEqual(observations[1].tick, 30)
        self.assertNotEqual(
            observations[1].observation_id,
            first_observation.observation_id,
        )

    def test_resource_visibility_is_tracked_independently_per_agent(self):
        self.world.add_resource(
            WorldResource(
                resource_id="wood-1",
                resource_type=ResourceType.WOOD,
                position=Position(3, 5),
                quantity=8,
            )
        )

        self.system.update(10)
        self.assertEqual(len(self.near.mind.observations), 1)
        self.assertEqual(self.far.mind.observations, ())

        self.far.character.position = Position(3, 10)
        self.system.update(20)

        self.assertEqual(len(self.near.mind.observations), 1)
        self.assertEqual(len(self.far.mind.observations), 1)
        self.assertNotEqual(
            self.near.mind.observations[0].observation_id,
            self.far.mind.observations[0].observation_id,
        )

    def test_resource_state_change_creates_a_new_observation(self):
        resource = WorldResource(
            resource_id="wood-1",
            resource_type=ResourceType.WOOD,
            position=Position(3, 5),
            quantity=8,
        )
        self.world.add_resource(resource)

        self.system.update(10)
        resource.quantity = 7
        self.system.update(20)

        observations = self.near.mind.observations
        self.assertEqual(len(observations), 2)
        self.assertTrue(observations[1].metadata["state_changed"])

    def test_resource_position_change_creates_a_new_observation(self):
        resource = WorldResource(
            resource_id="wood-1",
            resource_type=ResourceType.WOOD,
            position=Position(3, 5),
            quantity=8,
        )
        self.world.add_resource(resource)

        self.system.update(10)
        resource.position = Position(4, 5)
        self.system.update(20)

        observations = self.near.mind.observations
        self.assertEqual(len(observations), 2)
        self.assertEqual(observations[1].position, Position(4, 5))
        self.assertTrue(observations[1].metadata["state_changed"])
        self.assertEqual(
            observations[1].description,
            "A nearby wood resource appears different from before.",
        )

    def test_session_registers_event_and_periodic_perception(self):
        session = create_new_game()
        session.world.add_resource(
            WorldResource(
                resource_id="food-1",
                resource_type=ResourceType.FOOD,
                position=Position(10, 21),
                quantity=2,
            )
        )

        for _ in range(10):
            session.engine.advance_tick()

        adam = session.world.get_agent("adam-001")
        lina = session.world.get_agent("lina-001")
        self.assertTrue(
            any(
                observation.subject_id == "food-1"
                and observation.tick == 10
                for observation in adam.mind.observations
            )
        )

        session.event_bus.publish(
            CharacterActionCompleted(
                character_id="adam-001",
                decision=CharacterDecision.WORK,
                tick=11,
            )
        )
        self.assertTrue(
            any(
                observation.source_id == "adam-001"
                and observation.tick == 11
                for observation in lina.mind.observations
            )
        )


if __name__ == "__main__":
    unittest.main()
