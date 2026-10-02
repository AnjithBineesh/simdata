import json
from pathlib import Path

from simdata.trajectory.lidar_trajectory import Pose2D


def save_trajectory(
    trajectory: list[Pose2D],
    path: str | Path,
):
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = [
        {
            "timestamp": pose.timestamp,
            "x": pose.x,
            "y": pose.y,
            "theta": pose.theta,
        }
        for pose in trajectory
    ]

    with path.open("w") as file:
        json.dump(
            data,
            file,
            indent=2,
        )


def load_trajectory(
    path: str | Path,
) -> list[Pose2D]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Trajectory file not found: {path}"
        )

    with path.open() as file:
        data = json.load(file)

    return [
        Pose2D(
            timestamp=item["timestamp"],
            x=item["x"],
            y=item["y"],
            theta=item["theta"],
        )
        for item in data
    ]