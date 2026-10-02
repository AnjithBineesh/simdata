import math
from dataclasses import dataclass
from collections.abc import Callable

from simdata.core.icp import icp
from simdata.core.lidar_geometry import scan_to_points
from simdata.devices.lidar import SimLiDAR


@dataclass
class Pose2D:
    timestamp: float
    x: float
    y: float
    theta: float


class LiDARTrajectoryBuilder:
    def __init__(
        self,
        dataset,
        max_iterations=20,
        max_distance=0.5,
        tolerance=1e-5,
        progress_callback: Callable[[int], None] | None = None,
    ):
        self.lidar = SimLiDAR(
            dataset,
            realtime=False,
        )

        self.max_iterations = max_iterations
        self.max_distance = max_distance
        self.tolerance = tolerance
        self.progress_callback = progress_callback

    def build(self, max_scans=None):
        trajectory = []

        previous_scan, _ = self.lidar.read()

        x = 0.0
        y = 0.0
        theta = 0.0

        trajectory.append(
            Pose2D(
                timestamp=previous_scan.timestamp,
                x=x,
                y=y,
                theta=theta,
            )
        )

        scan_count = 0

        while max_scans is None or scan_count < max_scans:
            try:
                current_scan, _ = self.lidar.read()
            except RuntimeError:
                break

            previous_points = scan_to_points(
                previous_scan.ranges,
                previous_scan.angle_min,
                previous_scan.angle_increment,
                previous_scan.range_min,
                previous_scan.range_max,
            )

            current_points = scan_to_points(
                current_scan.ranges,
                current_scan.angle_min,
                current_scan.angle_increment,
                current_scan.range_min,
                current_scan.range_max,
            )

            dx, dy, dtheta = icp(
                source=current_points,
                target=previous_points,
                max_iterations=self.max_iterations,
                max_distance=self.max_distance,
                tolerance=self.tolerance,
            )

            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            global_dx = cos_theta * dx - sin_theta * dy
            global_dy = sin_theta * dx + cos_theta * dy

            x += global_dx
            y += global_dy
            theta += dtheta

            trajectory.append(
                Pose2D(
                    timestamp=current_scan.timestamp,
                    x=x,
                    y=y,
                    theta=theta,
                )
            )

            previous_scan = current_scan
            scan_count += 1

            if self.progress_callback is not None:
                self.progress_callback(scan_count)

        return trajectory