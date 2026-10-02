from simdata.devices import SimOdom


odom = SimOdom(
    dataset="deutsches_museum_2d",
    replay_speed=1.0,
)

for _ in range(10):
    sample, replay_time = odom.read()

    print(
        f"t={sample.timestamp:.3f} | "
        f"x={sample.position_x:.4f} m | "
        f"y={sample.position_y:.4f} m | "
        f"vx={sample.linear_velocity_x:.4f} m/s | "
        f"vy={sample.linear_velocity_y:.4f} m/s | "
        f"wz={sample.angular_velocity_z:.4f} rad/s"
    )