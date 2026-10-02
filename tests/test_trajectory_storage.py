from simdata.trajectory.lidar_trajectory import (
    LiDARTrajectoryBuilder,
)
from simdata.trajectory.storage import (
    load_trajectory,
    save_trajectory,
)


builder = LiDARTrajectoryBuilder(
    dataset="deutsches_museum_2d"
)

trajectory = builder.build(
    max_scans=20
)

path = "trajectory_test.json"

save_trajectory(
    trajectory,
    path,
)

loaded = load_trajectory(path)

print(f"Original poses: {len(trajectory)}")
print(f"Loaded poses:   {len(loaded)}")

print(
    f"First pose: "
    f"x={loaded[0].x:.4f}, "
    f"y={loaded[0].y:.4f}, "
    f"theta={loaded[0].theta:.4f}"
)

print(
    f"Last pose: "
    f"x={loaded[-1].x:.4f}, "
    f"y={loaded[-1].y:.4f}, "
    f"theta={loaded[-1].theta:.4f}"
)