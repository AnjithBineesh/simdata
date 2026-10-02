import time
from collections.abc import Iterator
from typing import TypeVar

T = TypeVar("T")


class ReplayClock:
    def __init__(
        self,
        speed: float = 1.0,
        realtime: bool = True,
    ):
        if speed <= 0:
            raise ValueError("Replay speed must be greater than 0.")

        self.speed = speed
        self.realtime = realtime

    def timestamps(
        self,
        samples: Iterator[T],
    ) -> Iterator[tuple[T, float]]:

        first_timestamp = None
        replay_start = None

        for sample in samples:

            if first_timestamp is None:
                first_timestamp = sample.timestamp
                replay_start = time.monotonic()

            relative_time = (
                sample.timestamp - first_timestamp
            ) / self.speed

            if self.realtime:
                elapsed = time.monotonic() - replay_start
                wait_time = relative_time - elapsed

                if wait_time > 0:
                    time.sleep(wait_time)

            yield sample, relative_time