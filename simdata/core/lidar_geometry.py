import math
from collections.abc import Sequence


def scan_to_points(
    ranges: Sequence[float],
    angle_min: float,
    angle_increment: float,
    range_min: float,
    range_max: float,
) -> list[tuple[float, float]]:
    points = []

    for index, distance in enumerate(ranges):
        if not math.isfinite(distance):
            continue

        if distance < range_min or distance > range_max:
            continue

        angle = angle_min + index * angle_increment

        x = distance * math.cos(angle)
        y = distance * math.sin(angle)

        points.append((x, y))

    return points
