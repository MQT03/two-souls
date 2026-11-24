
import math

from two_souls.simulation.engine import SimulationEngine


class SimulationRunner:
    """Converts elapsed real time into simulation ticks."""

    def __init__(
        self,
        engine: SimulationEngine,
        time_multiplier: float = 1.0
    ) -> None:
        if (
            isinstance(time_multiplier, bool)
            or not math.isfinite(time_multiplier)
            or time_multiplier <= 0
        ):
            raise ValueError("Time multiplier must be a positive number.")

        self._engine = engine
        self._time_multiplier = time_multiplier
        self._accumulator = 0.0

    @property
    def time_multiplier(self) -> float:
        return self._time_multiplier

    def update(self, elapsed_real_seconds: float) -> int:
        """Process elapsed real time and return the number of ticks."""

        if (
            isinstance(elapsed_real_seconds, bool)
            or not math.isfinite(elapsed_real_seconds)
            or elapsed_real_seconds < 0
        ):
            raise ValueError("Elapsed time must be a non-negative number.")

        self._accumulator += (
            elapsed_real_seconds * self._time_multiplier
        )

        ticks_to_run = math.floor(self._accumulator + 1e-9)
        ticks_to_run = max(0, ticks_to_run)

        self._accumulator = max(
            0.0,
            self._accumulator - ticks_to_run
        )

        for _ in range(ticks_to_run):
            self._engine.advance_tick()

        return ticks_to_run
