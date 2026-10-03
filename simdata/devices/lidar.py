from collections.abc import Iterator

from simdata.core.replay import ReplayClock
from simdata.core.types import LidarScan
from simdata.datasets.manager import DatasetManager
from simdata.datasets.rosbag_reader import RosbagLidarReader


class SimLiDAR:

    def __init__(
        self,
        dataset,
        replay_speed=1.0,
        realtime=True,
        clock: ReplayClock | None = None,
    ):
        manager = DatasetManager()

        bag_path = manager.get_builtin(dataset)

        self.reader = RosbagLidarReader(bag_path)

        # Use an externally supplied shared clock when available.
        if clock is not None:
            self.clock = clock
        else:
            self.clock = ReplayClock(
                speed=replay_speed,
                realtime=realtime,
            )

        self._scans: Iterator[
            tuple[LidarScan, float]
        ] = self.clock.timestamps(
            self.reader.read()
        )

    def read(self):
        try:
            return next(self._scans)

        except StopIteration:
            raise RuntimeError(
                "LiDAR dataset has ended."
            ) from None

    def reset(self):

        self.clock.reset()

        self._scans = self.clock.timestamps(
            self.reader.read()
        )