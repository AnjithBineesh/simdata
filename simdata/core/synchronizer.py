from dataclasses import dataclass
from typing import Any


@dataclass
class TimedSample:
    timestamp: float
    data: Any


class TimestampSynchronizer:
    def __init__(self, tolerance: float = 0.01):
        if tolerance < 0:
            raise ValueError("Tolerance must be non-negative.")

        self.tolerance = tolerance

    def nearest(
        self,
        timestamp: float,
        samples: list[TimedSample],
    ) -> TimedSample | None:
        if not samples:
            return None

        nearest_sample = min(
            samples,
            key=lambda sample: abs(sample.timestamp - timestamp),
        )

        if abs(nearest_sample.timestamp - timestamp) > self.tolerance:
            return None

        return nearest_sample