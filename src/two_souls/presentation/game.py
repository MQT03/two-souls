
import time

import pygame

from two_souls.simulation.session import GameSession


class Game:
    """Handles the presentation and main game loop."""

    def __init__(
        self,
        session: GameSession,
        width: int = 960,
        height: int = 640,
        target_fps: int = 60
    ) -> None:
        self._session = session
        self._width = width
        self._height = height
        self._target_fps = target_fps

    def run(self) -> None:
        pygame.init()

        screen = pygame.display.set_mode(
            (self._width, self._height)
        )

        pygame.display.set_caption("Two Souls")

        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 28)

        running = True
        previous_time = time.monotonic()

        try:
            while running:
                # Limit rendering FPS.
                clock.tick(self._target_fps)

                # Calculate elapsed real time.
                current_time = time.monotonic()
                elapsed_time = current_time - previous_time
                previous_time = current_time

                # Handle user input and window events.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                if not running:
                    break

                # Advance the simulation independently of FPS.
                self._session.runner.update(elapsed_time)

                # Render the current world state.
                self._render(screen, font)

                pygame.display.flip()

        finally:
            pygame.quit()

    def _render(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font
    ) -> None:
        screen.fill((35, 40, 45))

        tick_text = font.render(
            f"Simulation Tick: {self._session.engine.tick_count}",
            True,
            (255, 255, 255)
        )

        screen.blit(tick_text, (30, 30))

        y_position = 100

        for character in self._session.world.characters:
            character_text = (
                f"{character.name} | "
                f"State: {character.state.value} | "
                f"Hunger: {character.needs.hunger:.1f} | "
                f"Thirst: {character.needs.thirst:.1f} | "
                f"Energy: {character.needs.energy:.1f}"
            )

            text_surface = font.render(
                character_text,
                True,
                (220, 220, 220)
            )

            screen.blit(text_surface, (30, y_position))
            y_position += 45
