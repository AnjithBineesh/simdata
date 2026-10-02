from dataclasses import dataclass, field
from pathlib import Path

from rosbags.highlevel import AnyReader

from simdata.core.synchronizer import TimedSample, TimestampSynchronizer
from simdata.datasets.manager import DatasetManager
from simdata.devices import SimIMU, SimLiDAR


@dataclass
class Scenario:
    name: str
    dataset: str
    sync_tolerance: float = 0.01

    lidar: SimLiDAR = field(init=False)
    imu: SimIMU = field(init=False)
    synchronizer: TimestampSynchronizer = field(init=False)
    _imu_buffer: list[TimedSample] = field(
        default_factory=list,
        init=False,
    )

    def __post_init__(self):
        self.lidar = SimLiDAR(self.dataset)
        self.imu = SimIMU(self.dataset)

        self.synchronizer = TimestampSynchronizer(
            tolerance=self.sync_tolerance
        )

    def streams(self) -> dict[str, str]:
        manager = DatasetManager()
        bag_path = manager.get_builtin(self.dataset)

        streams = {}

        with AnyReader([Path(bag_path)]) as reader:
            for connection in reader.connections:
                streams[connection.topic] = connection.msgtype

        return streams

    def _fill_imu_buffer(self, target_timestamp: float):
        while True:
            imu_sample, _ = self.imu.read()

            self._imu_buffer.append(
                TimedSample(
                    timestamp=imu_sample.timestamp,
                    data=imu_sample,
                )
            )

            if imu_sample.timestamp >= target_timestamp:
                break

    def read_synced(self):
        scan, _ = self.lidar.read()

        self._fill_imu_buffer(scan.timestamp)

        matched = self.synchronizer.nearest(
            scan.timestamp,
            self._imu_buffer,
        )

        if matched is None:
            return scan, None

        self._imu_buffer = [
            sample
            for sample in self._imu_buffer
            if sample.timestamp >= scan.timestamp
        ]

        return scan, matched.data