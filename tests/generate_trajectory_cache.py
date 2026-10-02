from pathlib import Path

from simdata.trajectory.lidar_trajectory import LiDARTrajectoryBuilder
from simdata.trajectory.storage import save_trajectory


DATASET = "deutsches_museum_2d"

CACHE_PATH = (
    Path("simdata")
    / "trajectory"
    / "cache"
    / f"{DATASET}.json"
)


def show_progress(count):
    if count % 100 == 0:
        print(f"Processed {count} scan transitions")


def main():
    print("Generating trajectory...")
    print(f"Dataset: {DATASET}")
    print()

    builder = LiDARTrajectoryBuilder(
        dataset=DATASET,
        progress_callback=show_progress,
    )

    trajectory = builder.build()

    print()
    print(f"Trajectory generated: {len(trajectory)} poses")

    save_trajectory(
        trajectory,
        CACHE_PATH,
    )

    print(f"Saved to: {CACHE_PATH}")


if __name__ == "__main__":
    main()
