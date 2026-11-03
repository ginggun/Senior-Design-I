import unittest
from src.obstacle_logic import analyze_depth, describe


class TestObstacleLogic(unittest.TestCase):
    def test_center_warning(self):
        frame = [[2500]*3 + [800]*3 + [3000]*3 for _ in range(6)]
        results = analyze_depth(frame, min_valid_samples=3)
        self.assertEqual([r.region for r in results if r.warning], ['center'])
        self.assertIn('center', describe(results))

    def test_invalid_is_unknown_not_safe(self):
        frame = [[0]*9 for _ in range(6)]
        self.assertIn('UNKNOWN', describe(analyze_depth(frame, min_valid_samples=3)))

    def test_invalid_shape(self):
        with self.assertRaises(ValueError):
            analyze_depth([[1000, 1000], [1000]])


if __name__ == '__main__':
    unittest.main()
