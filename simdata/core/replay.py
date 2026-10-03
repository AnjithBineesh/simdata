import time
from collections.abc import Iterator
from typing import TypeVar


T = TypeVar("T")


class ReplayClock:
    """
    Shared replay clock for timestamped SimData streams.

    A single ReplayClock instance can be shared by multiple
    devices so that they use the same wall-clock replay epoch.
    """

    def __init__(
        self,
        speed: float = 1.0,
        realtime: bool = True,
        origin_timestamp: float | None = None,
    ):
        if speed <= 0:
            raise ValueError(
                "Replay speed must be greater than 0."
            )

        self.speed = speed
        self.realtime = realtime
        self.origin_timestamp = origin_timestamp

        # Shared wall-clock start.
        self._replay_start: float | None = None

    def reset(self) -> None:
        """
        Reset the replay clock.
        """

        self._replay_start = None

    def set_origin(self, timestamp: float) -> None:
        """
        Set the common dataset timestamp used as replay time zero.
        """

        self.origin_timestamp = timestamp

    def start(self) -> None:
        """
        Start the shared replay timeline.

        The same ReplayClock instance can be shared by multiple
        virtual devices.
        """

        if self._replay_start is None:
            self._replay_start = time.monotonic()

    def replay_time(self, timestamp: float) -> float:
        """
        Convert a dataset timestamp into replay time.
        """

        if self.origin_timestamp is None:
            raise RuntimeError(
                "ReplayClock origin_timestamp has not been set."
            )

        return (
            timestamp - self.origin_timestamp
        ) / self.speed

    def timestamps(
        self,
        samples: Iterator[T],
    ) -> Iterator[tuple[T, float]]:
        """
        Replay timestamped samples according to the shared clock.

        If no origin timestamp was supplied, the timestamp of the
        first sample becomes the replay origin automatically.
        """

        for sample in samples:

            # For standalone devices, automatically use the first
            # sample as the replay origin.
            if self.origin_timestamp is None:
                self.origin_timestamp = sample.timestamp

            # Start the shared wall-clock timeline.
            self.start()

            # Convert dataset timestamp into replay time.
            relative_time = self.replay_time(
                sample.timestamp
            )

            if self.realtime:

                if self._replay_start is None:
                    raise RuntimeError(
                        "Replay clock has not been started."
                    )

                elapsed = (
                    time.monotonic()
                    - self._replay_start
                )

                wait_time = (
                    relative_time - elapsed
                )

                if wait_time > 0:
                    time.sleep(wait_time)

            yield sample, relative_time