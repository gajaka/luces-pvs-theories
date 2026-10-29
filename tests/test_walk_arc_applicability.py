"""Known arc families, genuine obstructions and floating-point model boundaries."""

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import runpy
import tempfile
import unittest

import numpy as np


REPOSITORY = Path(__file__).resolve().parents[1]
TOOL = runpy.run_path(str(REPOSITORY / "scripts/check_walk_arc_applicability.py"))
analyze_points = TOOL["analyze_points"]


def walk(steps):
    steps = np.asarray(steps, dtype=float)
    return np.vstack((np.zeros(steps.shape[1]), np.cumsum(steps, axis=0)))


def unpack(value):
    return Fraction(int(value["numerator"]), int(value["denominator"]))


class WalkArcApplicabilityTests(unittest.TestCase):
    def test_nonzero_shortest_arc_family(self):
        for h in (0.25, 1.0, 2.0):
            with self.subTest(h=h):
                report = analyze_points(walk([[h, 0], [h, 0], [0, h], [0, h]]))
                exact = report["exact_necessary_conditions"]
                numerical = report["numerical_diagnostics"]
                self.assertEqual(exact["status"], "NOT_REFUTED_BY_NECESSARY_CHECKS_ONLY")
                self.assertEqual(numerical["status"], "TOLERANCE_COMPATIBLE_ONLY")
                self.assertAlmostEqual(numerical["metrics"]["mean_curvature"], math.pi / (6 * h))
                self.assertAlmostEqual(numerical["metrics"]["mean_curvature"], numerical["metrics"]["acos_endpoint_over_count_times_mean_h"])

    def test_equal_steps_with_reversal_are_rejected(self):
        numerical = analyze_points(walk([[1, 0], [0, 1], [1, 0]]))["numerical_diagnostics"]
        self.assertTrue(numerical["equal_length_tolerance_compatible"])
        self.assertTrue(numerical["uncentered_unit_plane"]["tolerance_compatible"])
        self.assertEqual(numerical["monotone_shortest_arc"]["status"], "TOLERANCE_REJECTED")
        self.assertAlmostEqual(numerical["metrics"]["endpoint_coherence"], 1)
        self.assertAlmostEqual(numerical["metrics"]["angular_excess_radians"], math.pi)

    def test_nonplanar_steps_have_an_exact_minor(self):
        report = analyze_points(walk(np.eye(3)))
        exact = report["exact_necessary_conditions"]
        self.assertEqual(exact["delta_rank"], 3)
        self.assertNotEqual(unpack(exact["nonzero_three_by_three_minor"]["determinant"]), 0)
        self.assertIn("EXACT_REPRESENTED_DELTA_RANK_EXCEEDS_TWO", exact["rejection_reasons"])
        self.assertEqual(report["numerical_diagnostics"]["monotone_shortest_arc"]["status"], "NOT_APPLICABLE")
        self.assertAlmostEqual(report["numerical_diagnostics"]["metrics"]["total_local_turn_radians"], math.pi)

    def test_loose_plane_override_cannot_normalize_a_zero_projection(self):
        report = analyze_points(walk(np.eye(3)), plane_rtol=2)
        self.assertFalse(report["thresholds"]["configured_are_defaults"])
        arc = report["numerical_diagnostics"]["monotone_shortest_arc"]
        self.assertEqual(arc["status"], "NOT_APPLICABLE")
        self.assertEqual(arc["reason"], "DEGENERATE_PLANE_PROJECTION")
        json.dumps(report, allow_nan=False)

    def test_unequal_lengths_are_separate_from_arc_order(self):
        report = analyze_points(walk([[1, 0], [0, 2], [0, 2]]))
        self.assertFalse(report["exact_necessary_conditions"]["all_squared_norms_equal"])
        self.assertFalse(report["numerical_diagnostics"]["equal_length_tolerance_compatible"])
        self.assertEqual(report["numerical_diagnostics"]["monotone_shortest_arc"]["status"], "TOLERANCE_COMPATIBLE_ONLY")
        self.assertEqual(report["numerical_diagnostics"]["status"], "TOLERANCE_REJECTED")

    def test_constant_and_partly_inactive_walks_are_not_straight_passes(self):
        for points in (np.zeros((4, 2)), walk([[1, 0], [0, 0], [0, 1]])):
            with self.subTest(points=points.tolist()):
                report = analyze_points(points)
                self.assertTrue(report["exact_necessary_conditions"]["inactive_step_indices"])
                self.assertEqual(report["numerical_diagnostics"]["status"], "TOLERANCE_REJECTED")
                self.assertEqual(report["numerical_diagnostics"]["monotone_shortest_arc"]["status"], "NOT_APPLICABLE")

    def test_single_antipodal_flip_is_valid_but_return_is_not(self):
        forward = analyze_points(walk([[1, 0], [1, 0], [-1, 0], [-1, 0]]))["numerical_diagnostics"]
        back = analyze_points(walk([[1, 0], [-1, 0], [1, 0]]))["numerical_diagnostics"]
        self.assertEqual(forward["status"], "TOLERANCE_COMPATIBLE_ONLY")
        self.assertTrue(forward["monotone_shortest_arc"]["antipodal_orientation_nonunique"])
        self.assertEqual(back["status"], "TOLERANCE_REJECTED")
        self.assertTrue(all(x["total_positive_variation_radians"] > math.pi
                            for x in back["monotone_shortest_arc"]["candidates"]))

    def test_angle_branch_cut_does_not_create_a_reversal(self):
        theta = np.deg2rad([170, 179, 181])
        report = analyze_points(walk(np.column_stack((np.cos(theta), np.sin(theta)))))
        self.assertEqual(report["numerical_diagnostics"]["status"], "TOLERANCE_COMPATIBLE_ONLY")

    def test_cumulative_small_backtracking_is_not_hidden(self):
        atol = 1e-6
        theta = np.array([0.0, 0.1, 0.1 - 0.6 * atol, 0.1 - 1.2 * atol])
        report = analyze_points(walk(np.column_stack((np.cos(theta), np.sin(theta)))), angle_atol=atol)
        arc = report["numerical_diagnostics"]["monotone_shortest_arc"]
        self.assertEqual(arc["status"], "TOLERANCE_REJECTED")
        self.assertTrue(all(x["total_negative_variation_radians"] > atol for x in arc["candidates"]))

    def test_more_than_half_circle_is_rejected(self):
        theta = np.deg2rad([0, 100, 200])
        report = analyze_points(walk(np.column_stack((np.cos(theta), np.sin(theta)))))
        self.assertEqual(report["numerical_diagnostics"]["monotone_shortest_arc"]["status"], "TOLERANCE_REJECTED")

    def test_numerical_verdict_is_rigid_rotation_invariant(self):
        rotation, _ = np.linalg.qr(np.random.default_rng(7).normal(size=(4, 4)))
        families = ([[1, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0]],
                    [[1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0]],
                    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
        for steps in families:
            points = walk(steps)
            original = analyze_points(points)["numerical_diagnostics"]
            rotated = analyze_points(points @ rotation)["numerical_diagnostics"]
            self.assertEqual(original["status"], rotated["status"])
            self.assertEqual(original["monotone_shortest_arc"]["status"], rotated["monotone_shortest_arc"]["status"])
            self.assertAlmostEqual(original["metrics"]["mean_curvature"], rotated["metrics"]["mean_curvature"], places=6)
            # Rounding a rotation changes the exact binary64 embedding. Its
            # exact rational rank/equality verdict is deliberately not equated.

    def test_exact_model_embeds_points_before_subtraction(self):
        tiny = 2.0**-54
        report = analyze_points([[1.0, 0.0], [tiny, 0.0], [-1.0, 0.0]])
        exact = report["exact_necessary_conditions"]
        self.assertEqual(unpack(exact["delta_squared_norms"][0]), (Fraction(1) - Fraction(1, 2**54))**2)
        self.assertFalse(exact["all_squared_norms_equal"])
        self.assertEqual(report["numerical_diagnostics"]["step_lengths"], [1.0, 1.0])
        self.assertIn("UNEQUAL_EXACT_REPRESENTED_SQUARED_STEP_LENGTHS", exact["rejection_reasons"])

    def test_nonfinite_inputs_and_invalid_tolerances_fail(self):
        with self.assertRaises(ValueError):
            analyze_points([[0, 0], [math.nan, 1], [1, 1]])
        with self.assertRaises(ValueError):
            analyze_points([[0, 0], [1, 0], [2, 0]], angle_atol=-1)

    def test_source_binding_failure_precedes_producer_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository, runner = root / "pvs", root / "runner"
            (repository / "applications/luces/data").mkdir(parents=True)
            (repository / "reports").mkdir()
            runner.mkdir()
            (runner / "producer.py").write_text("raise RuntimeError('must not execute')\n")
            fixture = {"formal_sources_sha256": {}, "c20_source": "producer.py",
                       "c20_source_sha256": hashlib.sha256(b"a different producer").hexdigest(), "rows": []}
            (repository / "applications/luces/data/lie_observations.json").write_text(json.dumps(fixture))
            (repository / "reports/PVS_WALK_COHERENCE_ORDER_20261029.json").write_text(json.dumps(
                {"passed": True, "actual_project_source_and_proof_closure": []}))
            with self.assertRaisesRegex(ValueError, "producer source hash changed"):
                TOOL["load_bound_inputs"](repository, runner)


if __name__ == "__main__":
    unittest.main()
