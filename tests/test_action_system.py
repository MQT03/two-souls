import unittest

from two_souls.simulation.session import create_new_game
from two_souls.simulation.systems.action_system import ActionSystem
from two_souls.simulation.systems.decision_system import DecisionSystem
from two_souls.world.character_action import CharacterAction
from two_souls.world.character_decision import CharacterDecision
from two_souls.world.character_state import CharacterState
from two_souls.events.event_bus import EventBus
from two_souls.events.character_events import CharacterActionCompleted

class TestActionSystem(unittest.TestCase):

    def setUp(self):
        self.session = create_new_game()
        self.world = self.session.world

        self.adam = self.world.get_character("adam-001")
        self.event_bus = EventBus()
        self.action_system = ActionSystem(self.world, self.event_bus)

    def test_work_decision_starts_work_action(self):
        self.adam.decision = CharacterDecision.WORK

        self.action_system.update(1)

        self.assertEqual(
            self.adam.state,
            CharacterState.WORKING
        )

        self.assertIsNotNone(self.adam.current_action)

    def test_action_progresses_each_tick(self):
        self.adam.decision = CharacterDecision.WORK

        self.action_system.update(1)
        self.action_system.update(2)

        self.assertEqual(
            self.adam.current_action.elapsed_ticks,
            2
        )

    def test_action_completes_after_duration(self):
        action = CharacterAction(
            decision=CharacterDecision.WORK,
            duration_ticks=2
        )

        self.assertFalse(action.advance())
        self.assertTrue(action.advance())
        self.assertTrue(action.is_complete)

    def test_completed_action_returns_character_to_idle(self):
        self.adam.decision = CharacterDecision.SEEK_FOOD

        for tick in range(1, 31):
            self.action_system.update(tick)

        self.assertEqual(
            self.adam.state,
            CharacterState.IDLE
        )

        self.assertTrue(
            self.adam.current_action.is_complete
        )

    def test_changed_decision_replaces_current_action(self):
        self.adam.decision = CharacterDecision.WORK
        self.action_system.update(1)

        self.adam.decision = CharacterDecision.REST
        self.action_system.update(2)

        self.assertEqual(
            self.adam.current_action.decision,
            CharacterDecision.REST
        )

        self.assertEqual(
            self.adam.state,
            CharacterState.SLEEPING
        )

    def test_idle_decision_clears_current_action(self):
        self.adam.decision = CharacterDecision.WORK
        self.action_system.update(1)

        self.adam.decision = CharacterDecision.IDLE
        self.action_system.update(2)

        self.assertIsNone(self.adam.current_action)
        self.assertEqual(
            self.adam.state,
            CharacterState.IDLE
        )

    def test_decision_system_starts_action_through_engine(self):
        for _ in range(5):
            self.session.engine.advance_tick()

        self.assertEqual(
            self.adam.decision,
            CharacterDecision.WORK
        )

        self.assertEqual(
            self.adam.state,
            CharacterState.WORKING
        )

        self.assertIsNotNone(self.adam.current_action)

    def test_action_continues_when_decision_is_unchanged(self):
        for _ in range(5):
            self.session.engine.advance_tick()

        first_action = self.adam.current_action

        for _ in range(5):
            self.session.engine.advance_tick()

        self.assertIs(
            self.adam.current_action,
            first_action
        )

        self.assertEqual(
            self.adam.current_action.elapsed_ticks,
            6
        )

    def test_new_need_interrupts_active_action(self):
        for _ in range(5):
            self.session.engine.advance_tick()

        self.assertEqual(
            self.adam.state,
            CharacterState.WORKING
        )

        self.adam.needs.hunger = 80

        for _ in range(5):
            self.session.engine.advance_tick()

        self.assertEqual(
            self.adam.decision,
            CharacterDecision.SEEK_FOOD
        )

        self.assertEqual(
            self.adam.current_action.decision,
            CharacterDecision.SEEK_FOOD
        )

        self.assertEqual(
            self.adam.state,
            CharacterState.SEEKING_FOOD
        )
        
    def test_completed_action_does_not_restart_without_new_decision(self):
        self.adam.decision = CharacterDecision.SEEK_FOOD

        for tick in range(1, 31):
            self.action_system.update(tick)

        completed_action = self.adam.current_action

        self.action_system.update(31)

        self.assertIs(
            self.adam.current_action,
            completed_action
        )

        self.assertTrue(completed_action.is_complete)

        self.assertEqual(
            self.adam.state,
            CharacterState.IDLE
        )
        
    def test_completed_action_restarts_after_new_decision_evaluation(self):
        self.adam.decision = CharacterDecision.WORK

        self.adam.current_action = CharacterAction(
            decision=CharacterDecision.WORK,
            duration_ticks=1,
            decision_revision=0
        )

        self.adam.state = CharacterState.WORKING

        self.action_system.update(1)

        completed_action = self.adam.current_action

        self.assertTrue(completed_action.is_complete)

        decision_system = DecisionSystem(self.world)
        decision_system.update(5)

        self.action_system.update(6)

        self.assertEqual(
            self.adam.decision,
            CharacterDecision.WORK
        )

        self.assertIsNot(
            self.adam.current_action,
            completed_action
        )

        self.assertEqual(
            self.adam.current_action.decision_revision,
            1
        )

        self.assertEqual(
            self.adam.state,
            CharacterState.WORKING
        )
        
    def test_evaluations_during_action_do_not_restart_completed_action(self):
        self.adam.decision = CharacterDecision.WORK

        decision_system = DecisionSystem(self.world)

        decision_system.update(1)

        self.adam.current_action = CharacterAction(
            decision=CharacterDecision.WORK,
            duration_ticks=1,
            decision_revision=self.adam.decision_revision
        )

        decision_system.update(2)

        self.action_system.update(3)

        completed_action = self.adam.current_action

        self.assertTrue(completed_action.is_complete)

        self.action_system.update(4)

        self.assertIs(
            self.adam.current_action,
            completed_action
        )

        self.assertEqual(
            self.adam.state,
            CharacterState.IDLE
        )

        decision_system.update(5)
        self.action_system.update(6)

        self.assertIsNot(
            self.adam.current_action,
            completed_action
        )

        self.assertEqual(
            self.adam.state,
            CharacterState.WORKING
        )

    def test_action_completion_publishes_event(self):
        received_events = []

        self.event_bus.subscribe(
            CharacterActionCompleted,
            received_events.append
        )

        self.adam.decision = CharacterDecision.WORK
        self.adam.decision_revision = 1

        self.action_system.update(1)

        action = self.adam.current_action

        for tick in range(2, action.duration_ticks + 1):
            self.action_system.update(tick)

        self.assertEqual(len(received_events), 1)

        event = received_events[0]

        self.assertEqual(event.character_id, self.adam.character_id)
        self.assertEqual(event.decision, CharacterDecision.WORK)
        self.assertEqual(event.tick, action.duration_ticks)


    def test_action_completion_event_is_published_only_once(self):
        received_events = []

        self.event_bus.subscribe(
            CharacterActionCompleted,
            received_events.append
        )

        self.adam.decision = CharacterDecision.WORK
        self.adam.decision_revision = 1

        for tick in range(1, 150):
            self.action_system.update(tick)

        self.assertEqual(len(received_events), 1)


    def test_interrupted_action_does_not_publish_completion_event(self):
        received_events = []

        self.event_bus.subscribe(
            CharacterActionCompleted,
            received_events.append
        )

        self.adam.decision = CharacterDecision.WORK
        self.adam.decision_revision = 1

        self.action_system.update(1)
        self.action_system.update(2)

        self.adam.decision = CharacterDecision.REST
        self.adam.decision_revision += 1

        self.action_system.update(3)

        self.assertEqual(received_events, [])


    def test_event_contains_actual_completion_tick(self):
        received_events = []

        self.event_bus.subscribe(
            CharacterActionCompleted,
            received_events.append
        )

        self.adam.decision = CharacterDecision.SOCIALIZE
        self.adam.decision_revision = 1

        self.action_system.update(40)

        action = self.adam.current_action

        for tick in range(41, 40 + action.duration_ticks):
            self.action_system.update(tick)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(
            received_events[0].tick,
            40 + action.duration_ticks - 1
        )

if __name__ == "__main__":
    unittest.main()
