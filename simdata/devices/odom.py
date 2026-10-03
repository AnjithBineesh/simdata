import math
from collections.abc import Iterator
from pathlib import Path

from simdata.core.replay import ReplayClock
from simdata.core.types import OdomSample
from simdata.trajectory.storage import load_trajectory


class SimOdom:

    def __init__(
        self,
        dataset,
        replay_speed=1.0,
        clock: ReplayClock | None = None,
    ):
        self.dataset = dataset

        self.cache_path = (
            Path(__file__).parent.parent
            / "trajectory"
            / "cache"
            / f"{dataset}.json"
        )

        self.trajectory = load_trajectory(
            self.cache_path
        )

        # If a shared clock is supplied, use it.
        # Otherwise create an independent clock.
        if clock is not None:

            self.clock = clock
            self._owns_clock = False

        else:

            self.clock = ReplayClock(
                speed=replay_speed,
                realtime=True,
                origin_timestamp=self.trajectory[0].timestamp,
            )

            self._owns_clock = True

        self._samples: Iterator[
            tuple[OdomSample, float]
        ] | None = None

        self._create_stream()

    def _trajectory_to_samples(self):

        previous = None

        for pose in self.trajectory:

            if previous is None:

                vx = 0.0
                vy = 0.0
                wz = 0.0

            else:

                dt = (
                    pose.timestamp
                    - previous.timestamp
                )

                if dt <= 0:

                    vx = 0.0
                    vy = 0.0
                    wz = 0.0

                else:

                    vx = (
                        pose.x - previous.x
                    ) / dt

                    vy = (
                        pose.y - previous.y
                    ) / dt

                    wz = (
                        pose.theta
                        - previous.theta
                    ) / dt

            half_theta = pose.theta / 2.0

            yield OdomSample(
                timestamp=pose.timestamp,

                frame_id="odom",
                child_frame_id="base_link",

                position_x=pose.x,
                position_y=pose.y,
                position_z=0.0,

                orientation_x=0.0,
                orientation_y=0.0,
                orientation_z=math.sin(half_theta),
                orientation_w=math.cos(half_theta),

                linear_velocity_x=vx,
                linear_velocity_y=vy,
                linear_velocity_z=0.0,

                angular_velocity_x=0.0,
                angular_velocity_y=0.0,
                angular_velocity_z=wz,
            )

            previous = pose

    def _create_stream(self):

        samples = self._trajectory_to_samples()

        self._samples = self.clock.timestamps(
            iter(samples)
        )

    def read(self):

        if self._samples is None:

            raise RuntimeError(
                "Odometry stream is not initialized."
            )

        try:

            return next(self._samples)

        except StopIteration:

            raise RuntimeError(
                "Odometry dataset has ended."
            ) from None

    def reset(self):

        # Only reset the clock if this device owns it.
        #
        # If the clock is shared with another device,
        # resetting it here would disturb the other stream.

        if self._owns_clock:

            self.clock.reset()

        self._create_stream()