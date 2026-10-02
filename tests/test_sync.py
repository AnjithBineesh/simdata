from simdata.core.synchronizer import TimedSample, TimestampSynchronizer
from simdata.devices import SimIMU, SimLiDAR


lidar = SimLiDAR("deutsches_museum_2d")
imu = SimIMU("deutsches_museum_2d")

synchronizer = TimestampSynchronizer(tolerance=0.01)

imu_samples = []

for _ in range(100):
    sample, _ = imu.read()
    imu_samples.append(
        TimedSample(
            timestamp=sample.timestamp,
            data=sample,
        )
    )

for _ in range(5):
    scan, _ = lidar.read()

    matched = synchronizer.nearest(
        scan.timestamp,
        imu_samples,
    )

    if matched is None:
        print("No IMU match")
    else:
        difference = abs(
            scan.timestamp - matched.timestamp
        )

        print(
            f"LiDAR: {scan.timestamp:.6f} | "
            f"IMU: {matched.timestamp:.6f} | "
            f"Difference: {difference * 1000:.3f} ms"
        )
