from simdata.devices import SimLiDAR


lidar = SimLiDAR(
    dataset="deutsches_museum_2d",
    replay_speed=1.0,
)


while True:

    try:

        scan, replay_time = lidar.read()

        print(
            f"time={replay_time:.6f}s "
            f"beams={len(scan.ranges)} "
            f"first_range={scan.ranges[0]:.3f}m"
        )

    except RuntimeError:

        print("Dataset replay finished.")

        break