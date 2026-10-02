import math

from simdata.core.icp import icp
from simdata.core.lidar_geometry import scan_to_points
from simdata.devices import SimLiDAR


lidar = SimLiDAR("deutsches_museum_2d")

previous_scan, _ = lidar.read()

for i in range(10):
    current_scan, _ = lidar.read()

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
    )

    print(
        f"{i:02d} | "
        f"Δt={(current_scan.timestamp - previous_scan.timestamp) * 1000:.2f} ms | "
        f"Δx={dx:.4f} m | "
        f"Δy={dy:.4f} m | "
        f"Δθ={math.degrees(dtheta):.4f}°"
    )

    previous_scan = current_scan