import unittest

from two_souls.intelligence.agent_mind import (
    AgentMind,
    Belief,
    Emotion,
    KnowledgeItem,
    Memory,
    Motivation,
    Preference,
    Skill,
    Value,
)
from two_souls.intelligence.personality import (
    Personality,
    TraitDefinition,
    TraitInstance,
)
from two_souls.world.agent import Agent
from two_souls.world.agent_factory import AgentFactory
from two_souls.world.agent_profile import AgentProfile
from two_souls.world.character import Character
from two_souls.world.inventory import Inventory
from two_souls.world.needs import Needs
from two_souls.world.position import Position
from two_souls.world.resource_type import ResourceType


class TestAgentModel(unittest.TestCase):

    def test_agent_owns_one_character_and_one_mind(self):
        character = Character("agent-1", "Ari", Position(1, 2))
        agent = Agent(character)

        self.assertIs(agent.character, character)
        self.assertIsInstance(agent.mind, AgentMind)
        self.assertEqual(agent.agent_id, character.character_id)

    def test_mind_has_independent_typed_default_components(self):
        first = AgentMind()
        second = AgentMind()

        self.assertIsInstance(first.personality, Personality)
        self.assertIn("diligence", first.personality.traits)
        self.assertEqual(first.values, {})
        self.assertEqual(first.motivations, {})
        self.assertEqual(first.emotions, {})
        self.assertEqual(first.preferences, {})
        self.assertEqual(first.knowledge, {})
        self.assertEqual(first.beliefs, {})
        self.assertEqual(first.memories, [])
        self.assertEqual(first.skills, {})
        self.assertIsNot(first.values, second.values)
        self.assertIsNot(first.memories, second.memories)
        self.assertIsNot(first.personality, second.personality)
        self.assertIsNot(first.personality.traits, second.personality.traits)

    def test_mind_distinguishes_cognitive_state_types(self):
        mind = AgentMind(
            values={"honesty": Value("honesty", 0.9)},
            motivations={"recognition": Motivation("recognition", 0.6)},
            emotions={"fear": Emotion("fear", 0.7)},
            preferences={"tea": Preference("tea", 0.8)},
            knowledge={"river": KnowledgeItem("river", "Flows east")},
            beliefs={"weather": Belief("Rain is coming", 0.3)},
            memories=[Memory("Saw clouds", 12)],
            skills={"farming": Skill("farming", 0.4)},
        )

        self.assertNotEqual(
            mind.motivations["recognition"].name,
            mind.beliefs["weather"].proposition,
        )
        self.assertEqual(mind.beliefs["weather"].confidence, 0.3)
        self.assertEqual(mind.memories[0].tick, 12)

    def test_personality_accepts_data_defined_typed_traits(self):
        trait = TraitInstance(
            TraitDefinition("prefers_solitude", bool),
            True,
        )
        color_trait = TraitInstance(
            TraitDefinition("favorite_color", str),
            "blue",
        )
        birth_order_trait = TraitInstance(
            TraitDefinition("birth_order", int, minimum=1),
            2,
        )
        personality = Personality.with_traits({"prefers_solitude": trait})
        personality.traits["favorite_color"] = color_trait
        personality.traits["birth_order"] = birth_order_trait

        self.assertIs(
            personality.get_trait("prefers_solitude").value,
            True,
        )
        self.assertEqual(
            personality.get_trait("favorite_color").value,
            "blue",
        )
        self.assertEqual(personality.numeric_value("birth_order"), 2.0)

        with self.assertRaises(TypeError):
            TraitInstance(TraitDefinition("prefers_solitude", bool), 1)
        with self.assertRaises(TypeError):
            TraitDefinition("bounded_label", str, minimum=1)
        with self.assertRaises(ValueError):
            TraitInstance(
                TraitDefinition("magnitude", float),
                float("nan"),
            )
        with self.assertRaises(TypeError):
            personality.numeric_value("favorite_color")

    def test_agent_factory_builds_agent_from_profile(self):
        inventory = Inventory()
        inventory.add(ResourceType.FOOD, 3)
        profile = AgentProfile(
            agent_id="agent-2",
            name="Rin",
            position=Position(4, 5),
            needs=Needs(hunger=25),
            inventory=inventory,
            traits={
                "diligence": TraitInstance(
                    TraitDefinition(
                        "diligence",
                        float,
                        minimum=0.0,
                        maximum=100.0,
                    ),
                    80.0,
                )
            },
            values={"care": Value("care", 0.9)},
            motivations={"recognition": Motivation("recognition", 0.6)},
            emotions={"fear": Emotion("fear", 0.7)},
            preferences={"tea": Preference("tea", 0.8)},
            knowledge={"river": KnowledgeItem("river", "Flows east")},
            beliefs={"home": Belief("This is home", 0.4)},
            memories=[Memory("Arrived", 1)],
            skills={"gardening": Skill("gardening", 0.3)},
        )

        agent = AgentFactory().create(profile)

        self.assertEqual(agent.agent_id, "agent-2")
        self.assertEqual(agent.character.name, "Rin")
        self.assertEqual(agent.character.position, Position(4, 5))
        self.assertEqual(agent.character.needs.hunger, 25)
        self.assertEqual(
            agent.character.inventory.quantity(ResourceType.FOOD),
            3,
        )
        self.assertEqual(
            agent.mind.personality.get_trait("diligence").value,
            80.0,
        )
        self.assertEqual(agent.mind.values["care"].importance, 0.9)
        self.assertEqual(
            agent.mind.motivations["recognition"].strength,
            0.6,
        )
        self.assertEqual(agent.mind.emotions["fear"].intensity, 0.7)
        self.assertEqual(agent.mind.preferences["tea"].preference, 0.8)
        self.assertEqual(agent.mind.knowledge["river"].content, "Flows east")
        self.assertEqual(
            agent.mind.beliefs["home"].proposition,
            "This is home",
        )
        self.assertEqual(agent.mind.memories[0].content, "Arrived")
        self.assertEqual(agent.mind.skills["gardening"].level, 0.3)

    def test_factory_and_agents_do_not_share_mutable_state(self):
        profile = AgentProfile("agent-3", "Sol", Position(0, 0))
        factory = AgentFactory()
        first = factory.create(profile)
        second = factory.create(profile)

        first.character.needs.hunger = 60
        first.character.inventory.add(ResourceType.WOOD, 2)
        first.mind.values["curiosity"] = Value("curiosity", 0.8)
        first.mind.motivations["explore"] = Motivation("explore", 0.7)
        first.mind.emotions["fear"] = Emotion("fear", 0.4)
        first.mind.preferences["tea"] = Preference("tea", 0.6)
        first.mind.knowledge["forest"] = KnowledgeItem(
            "forest",
            "North of the village",
        )
        first.mind.beliefs["forest"] = Belief("The forest is safe", 0.2)
        first.mind.memories.append(Memory("Found a path"))
        first.mind.skills["tracking"] = Skill("tracking", 0.5)
        first.mind.personality.traits["diligence"] = TraitInstance(
            TraitDefinition("diligence", float, minimum=0, maximum=100),
            90.0,
        )

        self.assertEqual(second.character.needs.hunger, 0)
        self.assertEqual(
            second.character.inventory.quantity(ResourceType.WOOD),
            0,
        )
        self.assertEqual(second.mind.values, {})
        self.assertEqual(second.mind.motivations, {})
        self.assertEqual(second.mind.emotions, {})
        self.assertEqual(second.mind.preferences, {})
        self.assertEqual(second.mind.knowledge, {})
        self.assertEqual(second.mind.beliefs, {})
        self.assertEqual(second.mind.memories, [])
        self.assertEqual(second.mind.skills, {})
        self.assertEqual(
            second.mind.personality.get_trait("diligence").value,
            50.0,
        )

        profile.needs.hunger = 15
        profile.inventory.add(ResourceType.FOOD, 1)
        profile.values["generosity"] = Value("generosity", 0.4)
        profile.memories.append(Memory("Profile memory"))

        self.assertEqual(first.character.needs.hunger, 60)
        self.assertEqual(first.character.inventory.quantity(ResourceType.FOOD), 0)
        self.assertEqual(
            first.mind.values,
            {"curiosity": Value("curiosity", 0.8)},
        )
        self.assertEqual(first.mind.memories, [Memory("Found a path")])


if __name__ == "__main__":
    unittest.main()
