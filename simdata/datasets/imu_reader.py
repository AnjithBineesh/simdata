from collections.abc import Iterator
from pathlib import Path

from rosbags.highlevel import AnyReader

from simdata.core.types import IMUSample


class RosbagIMUReader:
    def __init__(self, bag_path: str | Path, topic: str = "imu"):
        self.bag_path = Path(bag_path)
        self.topic = topic

        if not self.bag_path.exists():
            raise FileNotFoundError(
                f"Bag file not found: {self.bag_path}"
            )

    def read(self) -> Iterator[IMUSample]:
        with AnyReader([self.bag_path]) as reader:
            for connection, timestamp, rawdata in reader.messages():
                if connection.topic != self.topic:
                    continue

                msg = reader.deserialize(
                    rawdata,
                    connection.msgtype,
                )

                yield IMUSample(
                    timestamp=timestamp / 1e9,
                    frame_id=msg.header.frame_id,

                    orientation_x=float(msg.orientation.x),
                    orientation_y=float(msg.orientation.y),
                    orientation_z=float(msg.orientation.z),
                    orientation_w=float(msg.orientation.w),

                    angular_velocity_x=float(
                        msg.angular_velocity.x
                    ),
                    angular_velocity_y=float(
                        msg.angular_velocity.y
                    ),
                    angular_velocity_z=float(
                        msg.angular_velocity.z
                    ),

                    linear_acceleration_x=float(
                        msg.linear_acceleration.x
                    ),
                    linear_acceleration_y=float(
                        msg.linear_acceleration.y
                    ),
                    linear_acceleration_z=float(
                        msg.linear_acceleration.z
                    ),
                )
