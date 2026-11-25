
# Two Souls — Software Architecture

## 1. Project Overview

Two Souls is an autonomous living world simulation where agents live, interact, make decisions, and develop relationships independently of the player.

The world continues to evolve even when the game is closed. Its state is updated based on elapsed real-world time when the game is reopened.

## 2. Architectural Principles

The project follows these principles:

- Separation of Concerns.
- Modular and maintainable architecture.
- Independence between simulation and game rendering.
- Independence between character intelligence and presentation.
- Event-driven communication between systems where appropriate.
- Persistent world state.
- Individual character knowledge and memory.
- Testability and future scalability.

## 3. Main Components

### 3.1 Presentation Layer

Responsible for displaying the world and handling player input.

Technology: Pygame (pygame-ce).

It does not own simulation rules or character decision-making logic.

### 3.2 Simulation Engine

Responsible for coordinating the simulation lifecycle.

Responsibilities include:

- Managing simulation updates.
- Advancing world time.
- Coordinating interactions between simulation systems.
- Processing elapsed time after reopening the game.

### 3.3 Intelligence System

Provides cognitive state for each Agent and, in later stages, autonomous decision-making.

The AgentMind is the owner of:

- Personality traits, values, and motivations.
- Emotions and preferences.
- Knowledge, beliefs, and memories.
- Learned skills and the current decision state.

Traits are typed data defined independently from their per-agent values. Traits can use boolean, integer, floating-point, or string values, with optional numeric bounds. A trait can influence future evaluation but does not directly cause an action. Beliefs represent an agent's confidence in a proposition and may be incorrect; motivations describe drives rather than fixed goals.

AgentMind contains state, not a reasoning engine. It does not receive the World object; future perception and knowledge systems will supply controlled observations.

The system must provide explainable decisions and must not depend on external AI services.

### 3.4 World Model

Represents the actual state of the simulated world.

It includes:

- Agents and their physical Characters.
- Locations and environment.
- Resources and inventory.
- Crops and farming activities.
- Relationships and world state.

#### Agent Core and Ownership

`World` stores and retrieves `Agent` aggregates. An Agent is the autonomous entity and owns exactly one Character and one AgentMind. Its identity is the Character's ID.

Character contains physical and bodily state: name, position, needs, inventory, activity state, and action progress. AgentMind contains cognitive state. Learned skills stay with the mind, while physical capabilities and equipment belong with the body when those models are introduced. This boundary keeps physical simulation and cognition distinct while allowing systems to coordinate through an Agent.

Agents can be created from an `AgentProfile` using `AgentFactory`. Profiles describe initial physical and cognitive state; they do not prescribe a profession, goals, or life path. The factory copies mutable profile state so newly created Agents do not share inventories, needs, traits, or mind collections.

For compatibility with older callers, `World.characters` is a read-only tuple projection of the Characters owned by its Agents. `add_character` and `get_character` are also compatibility adapters; they do not maintain a separate Character collection. New code should use `add_agent`, `get_agent`, and `agents`.

### 3.5 Persistence Layer

Responsible for saving and loading world data using SQLite.

It preserves the world state and supports simulation continuity across game sessions.

### 3.6 Event System

Provides a communication mechanism between independent systems.

Examples:

- CharacterAteFood.
- CropPlanted.
- CropHarvested.
- RelationshipChanged.
- CharacterSlept.

Events allow systems to react to changes without unnecessary direct dependencies.

## 4. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Game Framework | Pygame-ce |
| Database | SQLite |
| Version Control | Git |
| Repository Hosting | GitHub |
| Development Environment | Visual Studio Code |

## 5. Simulation Lifecycle

The simulation must support two operating scenarios:

### Active Session

When the game is running:

- The simulation advances.
- Agents evaluate their needs and cognitive state.
- Agents select decisions and their Characters perform physical actions.
- World events are generated.
- The presentation layer displays the updated world.

### Inactive Session

When the game is closed:

- The last world state and timestamp are saved.
- No rendering or continuous game loop is required.
- Upon reopening, elapsed real-world time is calculated.
- The simulation processes the elapsed time logically.
- The updated world state is saved.

## 6. Architectural Boundaries

- Presentation must not contain world simulation rules.
- Intelligence must not depend on Pygame.
- Persistence must be responsible for database operations.
- The Simulation Engine coordinates systems but should not contain every system's internal logic.
- World state must remain independent of rendering.

## 7. Future Development

The architecture should support future expansion, including:

- Additional characters.
- More locations and environments.
- Advanced memory and relationship systems.
- More complex decision-making.
- Additional world simulation systems.
- Optional local AI model integration.


## 8. Time and Simulation Model

Two Souls uses a Fixed Simulation Tick model.

### Time Concepts

- Real Time: Actual elapsed time on the user's device.
- Game Time: Time progression inside the simulated world.
- Simulation Tick: A fixed unit used to advance the simulation.

### Simulation Tick Configuration

- Each Simulation Tick represents one Game Minute.
- Game Time can advance faster than Real Time using a configurable time multiplier.
- Simulation updates are independent of rendering FPS.
- The simulation must support offline progression.

### System Update Strategy

Not every system needs to update on every Simulation Tick.

Systems may use scheduled updates or event-driven processing depending on their responsibilities and performance requirements.
