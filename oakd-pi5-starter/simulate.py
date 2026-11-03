"""Run on any Python 3.10+ computer; no camera or pip packages required."""
from src.obstacle_logic import analyze_depth, describe

if __name__ == '__main__':
    # 6 x 9 example depth map, in millimeters. Left ~2.6m,
    # center ~0.9m, right ~3.0m. Zero indicates invalid reading.
    depth = [[2600]*3 + [900]*3 + [3000]*3 for _ in range(6)]
    depth[2][4] = 0
    for result in analyze_depth(depth, min_valid_samples=3):
        print(result)
    print(describe(analyze_depth(depth, min_valid_samples=3)))
