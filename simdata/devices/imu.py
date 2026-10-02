from collections.abc import Iterator

from simdata.core.replay import ReplayClock
from simdata.core.types import IMUSample
from simdata.datasets.imu_reader import RosbagIMUReader
from simdata.datasets.manager import DatasetManager


class SimIMU:
    def __init__(self, dataset: str, replay_speed: float = 1.0):
        manager = DatasetManager()
        bag_path = manager.get_builtin(dataset)

        self.reader = RosbagIMUReader(bag_path)
        self.clock = ReplayClock(
            speed=replay_speed,
            realtime=True,
        )

        self._samples: Iterator[
            tuple[IMUSample, float]
        ] = self.clock.timestamps(self.reader.read())

    def read(self) -> tuple[IMUSample, float]:
        try:
            return next(self._samples)
        except StopIteration:
            raise RuntimeError("IMU dataset has ended.")

    def reset(self):
        self._samples = self.clock.timestamps(
            self.reader.read()
        )
