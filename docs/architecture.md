
# Two Souls — Software Architecture

## 1. Project Overview

Two Souls is an autonomous living world simulation where characters live, interact, make decisions, and develop relationships independently of the player.

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

Responsible for autonomous character decision-making.

Initial approach:

- Rule-based decision-making.
- Utility-based decision-making.
- Goals and priorities.
- Needs evaluation.
- Memory-based decisions.
- Personality modifiers.

The system must provide explainable decisions and must not depend on external AI services.

### 3.4 World Model

Represents the actual state of the simulated world.

It includes:

- Characters.
- Locations and environment.
- Resources and inventory.
- Crops and farming activities.
- Relationships and world state.

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
- Characters evaluate their needs and goals.
- Characters make decisions and perform actions.
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
