from dataclasses import dataclass
from collections.abc import Sequence


@dataclass
class LidarScan:
    timestamp: float
    ranges: Sequence[float]
    angle_min: float
    angle_max: float
    angle_increment: float
    range_min: float
    range_max: float
    frame_id: str


@dataclass
class IMUSample:
    timestamp: float
    frame_id: str

    orientation_x: float
    orientation_y: float
    orientation_z: float
    orientation_w: float

    angular_velocity_x: float
    angular_velocity_y: float
    angular_velocity_z: float

    linear_acceleration_x: float
    linear_acceleration_y: float
    linear_acceleration_z: float


@dataclass
class OdomSample:
    timestamp: float
    frame_id: str
    child_frame_id: str

    position_x: float
    position_y: float
    position_z: float

    orientation_x: float
    orientation_y: float
    orientation_z: float
    orientation_w: float

    linear_velocity_x: float
    linear_velocity_y: float
    linear_velocity_z: float

    angular_velocity_x: float
    angular_velocity_y: float
    angular_velocity_z: float

@dataclass
class Pose2D:
    timestamp: float
    x: float
    y: float
    theta: float