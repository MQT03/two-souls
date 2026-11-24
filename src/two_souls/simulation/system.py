
from abc import ABC, abstractmethod


class SimulationSystem(ABC):
    """Base class for all world simulation systems."""

    @abstractmethod
    def update(self, tick: int) -> None:
        """Update the system for the given simulation tick."""
        pass
