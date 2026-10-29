#!/usr/bin/env python3
"""Check necessary arc conditions on the three captured seven-sample walks.

Exact checks concern the real embedding of the saved binary64 coordinates.
Numerical compatibility is a diagnostic, not a PVS membership certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path
import subprocess
import sys


DEFAULT_LENGTH_RTOL = 1e-6
DEFAULT_PLANE_RTOL = 1e-8
DEFAULT_ANGLE_ATOL = 1e-6
EXACT_STEP_CUTOFF = Fraction(1, 10**10)
MACHINE_FLOOR_FACTOR = 64


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational(value: Fraction) -> dict:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def determinant3(matrix: list[list[Fraction]]) -> Fraction:
    a, b, c = matrix
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def exact_rank(matrix: list[list[Fraction]]) -> tuple[int, dict | None]:
    """Gaussian elimination also selects an independently checked 3x3 minor."""
    work = [row[:] for row in matrix]
    origins = list(range(len(work)))
    pivot_rows, pivot_columns = [], []
    rank = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(rank, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        origins[rank], origins[pivot] = origins[pivot], origins[rank]
        pivot_rows.append(origins[rank])
        pivot_columns.append(column)
        scale = work[rank][column]
        work[rank] = [x / scale for x in work[rank]]
        for i in range(rank + 1, len(work)):
            scale = work[i][column]
            if scale:
                work[i] = [x - scale * y for x, y in zip(work[i], work[rank])]
        rank += 1
        if rank == len(work):
            break
    minor = None
    if rank >= 3:
        rows, columns = pivot_rows[:3], pivot_columns[:3]
        selected = [[matrix[i][j] for j in columns] for i in rows]
        value = determinant3(selected)
        if not value:
            raise ArithmeticError("Elimination failed to produce its independent minor")
        minor = {"delta_rows": rows, "coordinate_columns": columns,
                 "entries": [[rational(x) for x in row] for row in selected],
                 "determinant": rational(value)}
    return rank, minor


def angular_diagnostic(unit, basis, angle_atol: float, machine_floor: float) -> dict:
    """Keep signed turns and explicitly choose the ambiguous antipodal lift."""
    import numpy as np

    xy = unit @ basis.T
    projected_norms = np.linalg.norm(xy, axis=1)
    degenerate = (~np.isfinite(projected_norms)) | (projected_norms <= machine_floor)
    if np.any(degenerate):
        return {"status": "NOT_APPLICABLE", "reason": "DEGENERATE_PLANE_PROJECTION",
                "projected_zero_or_nonfinite_indices": np.flatnonzero(degenerate).tolist(),
                "scope": "A loose plane tolerance cannot justify angles for a vanishing projected direction"}
    xy /= projected_norms[:, None]
    dots = np.clip(np.sum(xy[:-1] * xy[1:], axis=1), -1.0, 1.0)
    cross = xy[:-1, 0] * xy[1:, 1] - xy[:-1, 1] * xy[1:, 0]
    signed = np.arctan2(cross, dots)
    antipodal = (np.abs(cross) <= machine_floor) & (dots < 0)
    candidates = []
    for orientation in (1, -1):
        increments = orientation * signed
        # At a true antipode either semicircle has the same endpoints. Choosing
        # +pi here tests existence; a second flip still consumes another pi.
        increments = np.where(antipodal, math.pi, increments)
        lifted = np.concatenate(([0.0], np.cumsum(increments)))
        negative = float(np.sum(np.maximum(-increments, 0)))
        positive = float(np.sum(np.maximum(increments, 0)))
        backtrack = float(np.max(np.maximum.accumulate(lifted) - lifted))
        compatible = negative <= angle_atol + machine_floor and positive <= math.pi + angle_atol + machine_floor
        candidates.append({
            "orientation": orientation,
            "signed_increments_radians": increments.tolist(),
            "lifted_angles_from_first_radians": lifted.tolist(),
            "total_negative_variation_radians": negative,
            "total_positive_variation_radians": positive,
            "maximum_backtracking_radians": backtrack,
            "net_turn_radians": float(lifted[-1]),
            "observed_angle_span_radians": float(np.max(lifted) - np.min(lifted)),
            "tolerance_compatible": bool(compatible),
        })
    compatible = any(x["tolerance_compatible"] for x in candidates)
    return {
        "status": "TOLERANCE_COMPATIBLE_ONLY" if compatible else "TOLERANCE_REJECTED",
        "basis_scope": "Best uncentered two-dimensional unit-direction plane; numerical diagnostic only",
        "principal_signed_increments_radians": signed.tolist(),
        "antipodal_pair_indices": np.flatnonzero(antipodal).tolist(),
        "antipodal_orientation_nonunique": bool(np.any(antipodal)),
        "candidates": candidates,
    }


def analyze_points(points, *, length_rtol: float = DEFAULT_LENGTH_RTOL,
                   plane_rtol: float = DEFAULT_PLANE_RTOL,
                   angle_atol: float = DEFAULT_ANGLE_ATOL) -> dict:
    import numpy as np

    for name, value in (("length_rtol", length_rtol), ("plane_rtol", plane_rtol), ("angle_atol", angle_atol)):
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be finite and nonnegative")
    samples = np.asarray(points, dtype=np.float64)
    if samples.ndim != 2 or samples.shape[0] < 2 or samples.shape[1] < 2:
        raise ValueError("Expected at least two points with at least two coordinates each")
    if not np.isfinite(samples).all():
        raise ValueError("Coordinates must be finite binary64 values")

    represented = [[Fraction.from_float(float(x)) for x in row] for row in samples]
    # Subtract after embedding points. Embedding np.diff instead would give a
    # different real model when floating-point subtraction rounded its result.
    exact_deltas = [[b - a for a, b in zip(first, second)]
                    for first, second in zip(represented, represented[1:])]
    squares = [sum(x * x for x in row) for row in exact_deltas]
    rank, minor = exact_rank(exact_deltas)
    unequal = next((i for i, value in enumerate(squares[1:], 1) if value != squares[0]), None)
    exact_inactive = [i for i, value in enumerate(squares) if value <= EXACT_STEP_CUTOFF**2]
    reasons = []
    if len(samples) < 3:
        reasons.append("FEWER_THAN_THREE_SAMPLES")
    if exact_inactive:
        reasons.append("INACTIVE_EXACT_REPRESENTED_STEP")
    if unequal is not None:
        reasons.append("UNEQUAL_EXACT_REPRESENTED_SQUARED_STEP_LENGTHS")
    if rank > 2:
        reasons.append("EXACT_REPRESENTED_DELTA_RANK_EXCEEDS_TWO")

    deltas = np.diff(samples, axis=0)
    norms = np.linalg.norm(deltas, axis=1)
    if not np.isfinite(norms).all():
        raise ValueError("Floating-point differences or norms overflowed")
    active = norms > float(EXACT_STEP_CUTOFF)
    unit = np.divide(deltas, norms[:, None], out=np.zeros_like(deltas), where=active[:, None])
    machine_floor = MACHINE_FLOOR_FACTOR * np.finfo(np.float64).eps * max(samples.shape)
    mean_h = float(np.mean(norms))
    relative_spread = float((np.max(norms) - np.min(norms)) / mean_h) if mean_h else None
    ratio = float(np.max(norms) / np.min(norms)) if np.min(norms) else None
    length_compatible = relative_spread is not None and relative_spread <= length_rtol + machine_floor

    singular_values = np.linalg.svd(unit, compute_uv=False)
    denominator = float(np.sum(singular_values**2))
    rank2_energy = float(np.sum(singular_values[2:]**2) / denominator) if denominator else None
    rank2_relative = math.sqrt(rank2_energy) if rank2_energy is not None else None
    _, _, vectors = np.linalg.svd(unit, full_matrices=False)
    basis = vectors[:2]
    residuals = np.linalg.norm(unit - (unit @ basis.T) @ basis, axis=1)
    maximum_residual = float(np.max(residuals))
    plane_compatible = bool(np.all(active) and maximum_residual <= plane_rtol + machine_floor)
    angles = {"status": "NOT_APPLICABLE", "reason": "Inactive steps or failed uncentered plane criterion"}
    if plane_compatible and len(samples) >= 3:
        angles = angular_diagnostic(unit, basis, angle_atol, machine_floor)

    pair_cosines = np.array([np.clip(np.dot(first, second), -1, 1)
                             for first, second in zip(unit, unit[1:])])
    local_angles = np.arccos(pair_cosines)
    contributions = np.divide(local_angles, norms[:-1], out=np.zeros_like(local_angles), where=active[:-1])
    curvature = float(np.mean(contributions)) if len(contributions) else 0.0
    coherence = float(np.clip(np.dot(unit[0], unit[-1]), -1, 1))
    endpoint_angle = float(np.arccos(coherence))
    total_turn = float(np.sum(local_angles))
    comparison = endpoint_angle / ((len(samples) - 2) * mean_h) if len(samples) >= 3 and mean_h else None
    compatible = (len(samples) >= 3 and bool(np.all(active)) and bool(length_compatible)
                  and plane_compatible and angles["status"] == "TOLERANCE_COMPATIBLE_ONLY")
    mass = [sum(row) for row in represented]
    return {
        "sample_count": len(samples), "coordinate_count": samples.shape[1],
        "thresholds": {
            "length_relative_spread": length_rtol, "unit_plane_max_residual": plane_rtol,
            "total_backtracking_and_arc_angle_radians": angle_atol,
            "machine_floor": machine_floor,
            "machine_floor_formula": "64 * binary64_epsilon * max(sample_count, coordinate_count)",
            "exact_step_cutoff": rational(EXACT_STEP_CUTOFF),
            "configured_are_defaults": (length_rtol == DEFAULT_LENGTH_RTOL and plane_rtol == DEFAULT_PLANE_RTOL
                                        and angle_atol == DEFAULT_ANGLE_ATOL),
            "selection": "Defaults declared before captured-data evaluation; the values above expose any caller overrides",
        },
        "point_coordinates": {
            "binary64_hex": [[float(x).hex() for x in row] for row in samples],
            "exact_binary64_real_embedding": [[rational(x) for x in row] for row in represented],
            "exact_mass_sums": [rational(x) for x in mass],
            "mass_scope": "Informative only: unit mass is not a shortest_arc_trace? hypothesis",
        },
        "exact_necessary_conditions": {
            "status": "REPRESENTED_MODEL_REJECTED" if reasons else "NOT_REFUTED_BY_NECESSARY_CHECKS_ONLY",
            "rejection_reasons": reasons,
            "delta_squared_norms": [rational(x) for x in squares],
            "all_squared_norms_equal": unequal is None,
            "unequal_norm_witness": None if unequal is None else {"step_indices": [0, unequal], "squared_norms": [rational(squares[0]), rational(squares[unequal])]},
            "inactive_step_indices": exact_inactive,
            "delta_rank": rank, "nonzero_three_by_three_minor": minor,
            "scope": "Exact rational arithmetic on embedded frozen binary64 point coordinates; not physical data or a Python/PVS refinement proof",
        },
        "numerical_diagnostics": {
            "status": "TOLERANCE_COMPATIBLE_ONLY" if compatible else "TOLERANCE_REJECTED",
            "step_lengths": norms.tolist(), "mean_step_length": mean_h,
            "max_min_step_length_ratio": ratio, "relative_step_length_spread": relative_spread,
            "equal_length_tolerance_compatible": bool(length_compatible),
            "inactive_step_indices": np.flatnonzero(~active).tolist(),
            "uncentered_unit_plane": {
                "singular_values": singular_values.tolist(),
                "rank2_relative_frobenius_residual": rank2_relative,
                "rank2_relative_tail_energy": rank2_energy,
                "maximum_unit_direction_residual": maximum_residual,
                "criterion": "maximum unit-direction distance to best uncentered rank-two plane <= plane tolerance + machine floor",
                "tolerance_compatible": plane_compatible,
            },
            "monotone_shortest_arc": angles,
            "metrics": {
                "endpoint_coherence": coherence, "mean_curvature": curvature,
                "local_turn_angles_radians": local_angles.tolist(),
                "total_local_turn_radians": total_turn, "endpoint_angle_radians": endpoint_angle,
                "angular_excess_radians": total_turn - endpoint_angle,
                "acos_endpoint_over_count_times_mean_h": comparison,
                "mean_h_comparison_difference": curvature - comparison if comparison is not None else None,
                "mean_h_comparison_ratio": curvature / comparison if comparison else None,
                "mean_h_comparison_scope": "Diagnostic substitution of mean h; not the theorem formula unless its hypotheses hold",
                "inactive_scope": "Raw cutoff-branch values remain defined; inactive samples cannot certify a shortest arc",
            },
            "scope": "Floating-point tolerance diagnostic only; no exact membership or PVS theorem instantiation is certified",
        },
    }


def load_bound_inputs(repository: Path, source_root: Path) -> tuple[dict, object, dict]:
    fixture_path = repository / "applications/luces/data/lie_observations.json"
    receipt_path = repository / "reports/PVS_WALK_COHERENCE_ORDER_20261029.json"
    fixture = json.loads(fixture_path.read_text())
    receipt = json.loads(receipt_path.read_text())
    if receipt.get("passed") is not True:
        raise ValueError("The arc theorem receipt is not a passing verification receipt")
    bindings = []
    formal = dict(fixture["formal_sources_sha256"])
    for entry in receipt["actual_project_source_and_proof_closure"]:
        old = formal.setdefault(entry["path"], entry["sha256"])
        if old != entry["sha256"]:
            raise ValueError("Conflicting formal input bindings")
    for relative, expected in sorted(formal.items()):
        if digest(repository / relative) != expected:
            raise ValueError(f"Formal input changed: {relative}")
        bindings.append({"root": "pvs_repository", "path": relative, "sha256": expected})
    source = source_root / fixture["c20_source"]
    if digest(source) != fixture["c20_source_sha256"]:
        raise ValueError("Captured producer source hash changed")
    bindings.append({"root": "runner_repository", "path": fixture["c20_source"], "sha256": digest(source)})
    for row in fixture["rows"]:
        relative = "paper3/dataset/" + row["dataset"]
        if digest(source_root / relative) != row["dataset_sha256"]:
            raise ValueError(f"Captured dataset changed: {relative}")
        bindings.append({"root": "runner_repository", "path": relative, "sha256": row["dataset_sha256"]})
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("captured_arc_producer", source)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load captured producer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return fixture, module, {
        "fixture_sha256": digest(fixture_path), "order_verification_receipt_sha256": digest(receipt_path),
        "bound_inputs": bindings,
    }


def extract_points(dataset: Path, producer) -> tuple[list, dict]:
    import numpy as np
    import pandas as pd

    data = pd.read_csv(dataset)
    missing = [x for x in ["elevation", *producer.SPEC_COLS] if x not in data.columns]
    if missing:
        raise ValueError(f"Missing dataset columns: {missing}")
    if len(producer.SPEC_COLS) != 10:
        raise ValueError("The bound producer no longer supplies ten spectral coordinates")
    night = data[data.elevation < -3]
    transition = data[(data.elevation > -3) & (data.elevation < 8)]
    day = data[data.elevation > 8]
    width = len(transition) // 5
    groups = [night] + [transition.iloc[i * width:(i + 1) * width] for i in range(5)] + [day]
    if any(group.empty for group in groups):
        raise ValueError("At least one captured sampling group is empty")
    points, details = [], []
    for name, group in zip(["night", *[f"transition_{i}" for i in range(5)], "day"], groups):
        means = group[producer.SPEC_COLS].mean().values
        if not np.isfinite(means).all():
            raise ValueError(f"Nonfinite spectral mean in group {name}")
        points.append(producer.to_dist(means))
        indices = [int(x) for x in group.index]
        details.append({"name": name, "rows": len(group), "first_original_row": indices[0],
                        "last_original_row": indices[-1],
                        "original_row_positions_sha256": hashlib.sha256(json.dumps(indices, separators=(",", ":")).encode()).hexdigest(),
                        "mean_channels_clipped_by_producer": int(np.sum(means < 1e-8))})
    columns = data[producer.SPEC_COLS].to_numpy(dtype=float)
    return points, {
        "spectral_columns": list(producer.SPEC_COLS), "source_rows": len(data),
        "night_rows": len(night), "transition_rows": len(transition), "day_rows": len(day),
        "transition_bin_width": width,
        "unused_transition_row_positions": [int(x) for x in transition.iloc[5 * width:].index],
        "boundary_rows_at_minus3_or_8": int(((data.elevation == -3) | (data.elevation == 8)).sum()),
        "nonfinite_elevation_rows": int(np.sum(~np.isfinite(data.elevation.to_numpy(dtype=float)))),
        "nonfinite_spectral_values": int(np.sum(~np.isfinite(columns))),
        "day_contains_original_row_zero": bool(0 in day.index),
        "groups": details,
        "sampling_scope": "Original CSV row order; night elevation<-3, five positional transition bins -3<elevation<8, day elevation>8; no sorting, remainder repair or data cleaning",
    }


def revision(root: Path) -> str | None:
    try:
        return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    repository = Path(__file__).resolve().parents[1]
    parser.add_argument("--source-root", type=Path, default=repository.parent / "master-controler")
    parser.add_argument("--output", type=Path, help="write JSON here; otherwise use standard output")
    parser.add_argument("--length-rtol", type=float, default=DEFAULT_LENGTH_RTOL)
    parser.add_argument("--plane-rtol", type=float, default=DEFAULT_PLANE_RTOL)
    parser.add_argument("--angle-atol", type=float, default=DEFAULT_ANGLE_ATOL)
    arguments = parser.parse_args()
    source_root = arguments.source_root.resolve()
    fixture, producer, bindings = load_bound_inputs(repository, source_root)
    rows = []
    for captured in fixture["rows"]:
        points, extraction = extract_points(source_root / "paper3/dataset" / captured["dataset"], producer)
        analysis = analyze_points(points, length_rtol=arguments.length_rtol,
                                  plane_rtol=arguments.plane_rtol, angle_atol=arguments.angle_atol)
        expected = captured["metrics"]["path_curvature"]["value"]
        computed = analysis["numerical_diagnostics"]["metrics"]["mean_curvature"]
        if abs(computed - expected) > 1e-12:
            raise ValueError(f"Captured curvature replay differs for {captured['name']}")
        rows.append({"name": captured["name"], "dataset": captured["dataset"],
                     "extraction": extraction, "analysis": analysis})
    import numpy as np
    import pandas as pd
    report = {
        "schema": 1, "scope": "Captured seven-sample walks: exact represented-model obstructions and separate numerical arc diagnostics; no PVS, binary64 refinement, C20 equivalence or physical calibration proof",
        "producer_revision": revision(source_root), "pvs_revision": revision(repository),
        "tool_sha256": digest(Path(__file__)),
        "environment": {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__},
        "input_bindings": bindings, "rows": rows,
    }
    rendered = json.dumps(report, indent=2, allow_nan=False) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered)
        print(f"Recorded {len(rows)} bound walks in {arguments.output}")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
