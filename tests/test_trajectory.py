import math

from simdata.trajectory.lidar_trajectory import LiDARTrajectoryBuilder


builder = LiDARTrajectoryBuilder(
    dataset="deutsches_museum_2d"
)

trajectory = builder.build(max_scans=20)

for pose in trajectory:
    print(
        f"t={pose.timestamp:.3f} | "
        f"x={pose.x:.4f} m | "
        f"y={pose.y:.4f} m | "
        f"theta={math.degrees(pose.theta):.4f}°"
    )