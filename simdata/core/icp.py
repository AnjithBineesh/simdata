import math
from collections.abc import Sequence

import numpy as np
from scipy.spatial import cKDTree


Point2D = tuple[float, float]


def transform_points(
    points: Sequence[Point2D],
    dx: float,
    dy: float,
    dtheta: float,
) -> list[Point2D]:
    cos_theta = math.cos(dtheta)
    sin_theta = math.sin(dtheta)

    return [
        (
            cos_theta * x - sin_theta * y + dx,
            sin_theta * x + cos_theta * y + dy,
        )
        for x, y in points
    ]


def nearest_points(
    source: Sequence[Point2D],
    target: Sequence[Point2D],
    max_distance: float,
) -> list[tuple[Point2D, Point2D]]:
    if not source or not target:
        return []

    source_array = np.asarray(
        source,
        dtype=float,
    )

    target_array = np.asarray(
        target,
        dtype=float,
    )

    tree = cKDTree(target_array)

    distances, indices = tree.query(
        source_array,
        distance_upper_bound=max_distance,
    )

    pairs = []

    for source_point, distance, index in zip(
        source,
        distances,
        indices,
        strict=True,
    ):
        if math.isfinite(distance):
            pairs.append(
                (
                    source_point,
                    tuple(target_array[index]),
                )
            )

    return pairs


def estimate_transform(
    pairs: Sequence[tuple[Point2D, Point2D]],
) -> tuple[float, float, float]:
    if not pairs:
        return 0.0, 0.0, 0.0

    source_x = sum(
        pair[0][0] for pair in pairs
    ) / len(pairs)

    source_y = sum(
        pair[0][1] for pair in pairs
    ) / len(pairs)

    target_x = sum(
        pair[1][0] for pair in pairs
    ) / len(pairs)

    target_y = sum(
        pair[1][1] for pair in pairs
    ) / len(pairs)

    source_centered = [
        (
            source[0] - source_x,
            source[1] - source_y,
        )
        for source, _ in pairs
    ]

    target_centered = [
        (
            target[0] - target_x,
            target[1] - target_y,
        )
        for _, target in pairs
    ]

    cross = sum(
        source[0] * target[1]
        - source[1] * target[0]
        for source, target in zip(
            source_centered,
            target_centered,
            strict=True,
        )
    )

    dot = sum(
        source[0] * target[0]
        + source[1] * target[1]
        for source, target in zip(
            source_centered,
            target_centered,
            strict=True,
        )
    )

    rotation = math.atan2(
        cross,
        dot,
    )

    cos_theta = math.cos(rotation)
    sin_theta = math.sin(rotation)

    translation_x = (
        target_x
        - (
            cos_theta * source_x
            - sin_theta * source_y
        )
    )

    translation_y = (
        target_y
        - (
            sin_theta * source_x
            + cos_theta * source_y
        )
    )

    return (
        translation_x,
        translation_y,
        rotation,
    )


def icp(
    source: Sequence[Point2D],
    target: Sequence[Point2D],
    max_iterations: int = 20,
    max_distance: float = 0.5,
    tolerance: float = 1e-5,
) -> tuple[float, float, float]:
    current = list(source)

    total_dx = 0.0
    total_dy = 0.0
    total_dtheta = 0.0

    for _ in range(max_iterations):
        pairs = nearest_points(
            current,
            target,
            max_distance,
        )

        if len(pairs) < 3:
            break

        dx, dy, dtheta = estimate_transform(
            pairs
        )

        current = transform_points(
            current,
            dx,
            dy,
            dtheta,
        )

        cos_theta = math.cos(dtheta)
        sin_theta = math.sin(dtheta)

        previous_dx = total_dx
        previous_dy = total_dy

        total_dx = (
            cos_theta * previous_dx
            - sin_theta * previous_dy
            + dx
        )

        total_dy = (
            sin_theta * previous_dx
            + cos_theta * previous_dy
            + dy
        )

        total_dtheta += dtheta

        if (
            abs(dx) < tolerance
            and abs(dy) < tolerance
            and abs(dtheta) < tolerance
        ):
            break

    return (
        total_dx,
        total_dy,
        total_dtheta,
    )