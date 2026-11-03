"""Simple depth-only warning logic; not a navigation or safety system."""
from dataclasses import dataclass
from statistics import median
from typing import Sequence

@dataclass(frozen=True)
class RegionResult:
    region: str
    distance_m: float | None
    valid_samples: int
    warning: bool


def analyze_depth(
    depth_mm: Sequence[Sequence[int]],
    threshold_m: float = 1.5,
    min_valid_samples: int = 4,
    min_distance_m: float = 0.35,
    max_distance_m: float = 5.0,
) -> list[RegionResult]:
    """Split a rectangular depth image into thirds, estimate each region's distance.

    depth_mm: 2D image of millimeter distances; 0/invalid readings ignored.
    Uses a 20th percentile of valid readings (robust versus a single noisy pixel).
    This is a *demonstration heuristic*, not a validated obstacle detector.
    """
    if not depth_mm or not depth_mm[0]:
        raise ValueError('Depth image cannot be empty')
    height, width = len(depth_mm), len(depth_mm[0])
    if any(len(row) != width for row in depth_mm):
        raise ValueError('Depth image must be rectangular')
    if width < 3:
        raise ValueError('Depth image must be at least 3 pixels wide')
    if threshold_m <= 0 or min_valid_samples < 1:
        raise ValueError('Invalid thresholds')

    # Center crop reduces the impact of image edges. Camera pitch / floor masking
    # will need to be added and calibrated once real hardware is available.
    y0, y1 = height // 4, max(height // 4 + 1, 3 * height // 4)
    regions = [('left', 0, width // 3),
               ('center', width // 3, 2 * width // 3),
               ('right', 2 * width // 3, width)]
    results = []
    for name, x0, x1 in regions:
        valid = sorted(value / 1000 for row in depth_mm[y0:y1]
                       for value in row[x0:x1]
                       if isinstance(value, (int, float)) and
                       min_distance_m * 1000 <= value <= max_distance_m * 1000)
        if len(valid) < min_valid_samples:
            results.append(RegionResult(name, None, len(valid), False))
            continue
        # Approximate 20th percentile. Smaller distances represent nearer surfaces.
        ix = int(0.20 * (len(valid) - 1))
        distance = valid[ix]
        results.append(RegionResult(name, round(distance, 2), len(valid), distance < threshold_m))
    return results


def describe(results: list[RegionResult]) -> str:
    warnings = [r for r in results if r.warning]
    if warnings:
        closest = min(warnings, key=lambda r: r.distance_m)
        return f'CAUTION: {closest.region} region ~{closest.distance_m:.2f} m'
    if any(r.distance_m is None for r in results):
        return 'UNKNOWN: insufficient valid depth data in one or more regions'
    return 'NO NEARBY DEPTH HAZARD IN MONITORED REGIONS (not a safety guarantee)'
