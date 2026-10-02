from simdata.devices import SimLiDAR


lidar = SimLiDAR("deutsches_museum_2d")

previous_scan, _ = lidar.read()

for i in range(10):
    current_scan, _ = lidar.read()

    print(
        f"{i}: "
        f"previous={previous_scan.timestamp:.6f} "
        f"current={current_scan.timestamp:.6f}"
    )

    previous_scan = current_scan
