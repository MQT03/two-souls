
import unittest

from two_souls.events.event_bus import EventBus
from two_souls.events.character_events import CharacterActionCompleted
from two_souls.world.character_decision import CharacterDecision


class TestEventBus(unittest.TestCase):

    def setUp(self):
        self.event_bus = EventBus()

        self.event = CharacterActionCompleted(
            character_id="adam-001",
            decision=CharacterDecision.WORK,
            tick=100
        )

    def test_subscriber_receives_published_event(self):
        received_events = []

        self.event_bus.subscribe(
            CharacterActionCompleted,
            received_events.append
        )

        self.event_bus.publish(self.event)

        self.assertEqual(received_events, [self.event])

    def test_multiple_subscribers_receive_same_event(self):
        first_received = []
        second_received = []

        self.event_bus.subscribe(
            CharacterActionCompleted,
            first_received.append
        )

        self.event_bus.subscribe(
            CharacterActionCompleted,
            second_received.append
        )

        self.event_bus.publish(self.event)

        self.assertEqual(first_received, [self.event])
        self.assertEqual(second_received, [self.event])

    def test_subscriber_does_not_receive_different_event_type(self):
        received_events = []

        self.event_bus.subscribe(
            str,
            received_events.append
        )

        self.event_bus.publish(self.event)

        self.assertEqual(received_events, [])

    def test_publishing_without_subscribers_does_not_raise_error(self):
        self.event_bus.publish(self.event)


if __name__ == "__main__":
    unittest.main()
