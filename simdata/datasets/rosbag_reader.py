from collections.abc import Iterator
from pathlib import Path

from rosbags.highlevel import AnyReader

from simdata.core.types import LidarScan


class RosbagLidarReader:

    def __init__(
        self,
        bag_path: str | Path,
        topic: str = "horizontal_laser_2d",
    ):
        self.bag_path = Path(bag_path)
        self.topic = topic

        if not self.bag_path.exists():
            raise FileNotFoundError(
                f"Bag file not found: {self.bag_path}"
            )

    def read(self) -> Iterator[LidarScan]:

        with AnyReader([self.bag_path]) as reader:

            for connection, timestamp, rawdata in reader.messages():

                if connection.topic != self.topic:
                    continue

                msg = reader.deserialize(
                    rawdata,
                    connection.msgtype,
                )

                ranges = []

                for echo in msg.ranges:

                    if len(echo.echoes) > 0:
                        ranges.append(float(echo.echoes[0]))
                    else:
                        ranges.append(float("inf"))

                yield LidarScan(
                    timestamp=timestamp / 1e9,
                    ranges=ranges,
                    angle_min=float(msg.angle_min),
                    angle_max=float(msg.angle_max),
                    angle_increment=float(msg.angle_increment),
                    range_min=float(msg.range_min),
                    range_max=float(msg.range_max),
                    frame_id=msg.header.frame_id,
                )