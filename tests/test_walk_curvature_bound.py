"""Curvature-bound equality cases, exclusions and geometric transformations."""

import math
from pathlib import Path
import runpy
import tempfile
import unittest

import numpy as np


REPOSITORY = Path(__file__).resolve().parents[1]
TOOL = runpy.run_path(str(REPOSITORY / "scripts/check_walk_curvature_bound.py"))
analyze_points = TOOL["analyze_points"]


def walk(steps):
    steps = np.asarray(steps, dtype=float)
    return np.vstack((np.zeros(steps.shape[1]), np.cumsum(steps, axis=0)))


class WalkCurvatureBoundTests(unittest.TestCase):
    def test_three_samples_exclude_a_long_final_step_and_are_tight(self):
        report = analyze_points(walk([[1, 0], [0, 100]]))
        self.assertEqual(report["status"], "NUMERICAL_CHECK_PASSED")
        self.assertEqual(report["denominator_step_indices"], [0])
        self.assertEqual(report["excluded_last_step_index"], 1)
        self.assertEqual(report["excluded_last_step_norm"], 100)
        self.assertEqual(report["maximum_denominator_step_norm"], 1)
        self.assertAlmostEqual(report["mean_curvature"], math.pi / 2)
        self.assertEqual(report["mean_curvature"], report["lower_bound"])

    def test_same_direction_then_quarter_turn_is_a_sharp_four_sample_case(self):
        for h in (0.25, 1.0, 2.0):
            with self.subTest(h=h):
                report = analyze_points(walk([[h, 0], [h, 0], [0, h]]))
                self.assertEqual(report["status"], "NUMERICAL_CHECK_PASSED")
                self.assertAlmostEqual(report["lower_bound"], math.pi / (4 * h))
                self.assertEqual(report["mean_curvature"], report["lower_bound"])

    def test_recovering_endpoint_coherence_does_not_force_zero_curvature(self):
        report = analyze_points(walk([[1, 0], [0, 1], [1, 0]]))
        self.assertEqual(report["endpoint_coherence"], 1)
        self.assertEqual(report["lower_bound"], 0)
        self.assertAlmostEqual(report["mean_curvature"], math.pi / 2)
        self.assertGreater(report["curvature_minus_bound"], 0)
        self.assertIsNone(report["curvature_over_bound"])

    def test_unequal_nonplanar_steps_do_not_need_the_arc_hypotheses(self):
        report = analyze_points(walk([[1, 0, 0], [0, 2, 0], [0, 0, 3]]))
        self.assertEqual(report["status"], "NUMERICAL_CHECK_PASSED")
        self.assertEqual(report["maximum_denominator_step_norm"], 2)
        self.assertEqual(report["excluded_last_step_norm"], 3)
        self.assertAlmostEqual(report["mean_curvature"], 3 * math.pi / 8)
        self.assertAlmostEqual(report["lower_bound"], math.pi / 8)

    def test_inactive_and_short_traces_are_not_positive_certificates(self):
        for points in (np.zeros((4, 2)), walk([[1, 0], [0, 0], [0, 1]]),
                       [[0, 0], [1, 0]], [[0, 0]]):
            with self.subTest(points=np.asarray(points).tolist()):
                report = analyze_points(points)
                self.assertEqual(report["status"], "NOT_APPLICABLE")
                self.assertNotIn("lower_bound", report)

    def test_cutoff_is_strict(self):
        at_cutoff = analyze_points([[0, 0], [1e-10, 0], [1e-10, 1]])
        self.assertEqual(at_cutoff["status"], "NOT_APPLICABLE")
        self.assertEqual(at_cutoff["inactive_step_indices"], [0])

    def test_rigid_rotation_and_scaling_preserve_the_expected_values(self):
        points = walk([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
        rotation, _ = np.linalg.qr(np.random.default_rng(31).normal(size=(3, 3)))
        original = analyze_points(points)
        rotated = analyze_points(points @ rotation)
        for field in ("endpoint_coherence", "mean_curvature", "lower_bound"):
            self.assertAlmostEqual(original[field], rotated[field], places=12)
        for scale in (0.25, 4.0):
            scaled = analyze_points(scale * points)
            self.assertAlmostEqual(scaled["endpoint_coherence"], original["endpoint_coherence"])
            self.assertAlmostEqual(scaled["mean_curvature"], original["mean_curvature"] / scale)
            self.assertAlmostEqual(scaled["lower_bound"], original["lower_bound"] / scale)

    def test_nonfinite_and_overflowing_inputs_are_rejected(self):
        for points in ([[0, 0], [math.nan, 1], [1, 1]],
                       [[0, 0], [math.inf, 1], [1, 1]],
                       [[-1e308, 0], [1e308, 0], [0, 1]]):
            with self.subTest(points=points):
                with self.assertRaises(ValueError):
                    analyze_points(points)

    def test_a_changed_frozen_report_is_rejected_before_reading_other_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            changed = root / "changed.json"
            changed.write_text("{}\n")
            with self.assertRaisesRegex(ValueError, "Frozen trace report hash changed"):
                TOOL["load_bound_trace_report"](root / "pvs", root / "runner", changed)


if __name__ == "__main__":
    unittest.main()
