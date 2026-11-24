
from two_souls.simulation.system import SimulationSystem


class SimulationEngine:
    """
    Coordinates the progression of the world simulation.
    """

    def __init__(self) -> None:
        self._tick_count = 0
        self._systems: list[tuple[SimulationSystem, int]] = []

    @property
    def tick_count(self) -> int:
        return self._tick_count

    def add_system(
        self,
        system: SimulationSystem,
        update_interval: int = 1
    ) -> None:
        if update_interval < 1:
            raise ValueError("Update interval must be at least 1.")

        self._systems.append((system, update_interval))

    def advance_tick(self) -> int:
        self._tick_count += 1

        for system, interval in self._systems:
            if self._tick_count % interval == 0:
                system.update(self._tick_count)

        return self._tick_count
