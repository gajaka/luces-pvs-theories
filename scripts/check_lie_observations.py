#!/usr/bin/env python3
"""Replay the finite C20/C21/C22 fixture and check its PVS source bindings."""

from __future__ import annotations

import argparse
import contextlib
from fractions import Fraction
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import sys


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=repository.parent / "master-controler")
    arguments = parser.parse_args()
    source_root = arguments.source_root.resolve()
    fixture = json.loads((repository / "applications/luces/data/lie_observations.json").read_text())
    for relative, expected in fixture["formal_sources_sha256"].items():
        require(digest(repository / relative) == expected, f"PVS source changed: {relative}")
    source = source_root / fixture["c20_source"]
    require(digest(source) == fixture["c20_source_sha256"], "C20 source hash changed")
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("measured_c20_source", source)
    require(spec is not None and spec.loader is not None, "Cannot load C20 source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    import numpy as np
    import pandas as pd

    pvs = (repository / "applications/luces/lie_generator_structure.pvs").read_text()
    field_sources = {
        "global_alignment": "mean_cos_full",
        "pair_alignment": "mean_cos",
        "shape_min_cosine": "min_cos_active",
        "speed_ratio": "speed_ratio",
    }
    for row in fixture["rows"]:
        dataset = source_root / "paper3/dataset" / row["dataset"]
        require(digest(dataset) == row["dataset_sha256"], f"Dataset changed: {dataset.name}")
        with contextlib.redirect_stdout(io.StringIO()):
            result = module.analyze_boot(str(dataset), row["name"])
        require(result is not None, f"No observation for {dataset.name}")
        actual = {field: float(result[key]) for field, key in field_sources.items()}
        # This additional curvature uses the SAME seven distributions as C20.
        # It is not the differently binned curvature of C_DEV/c20_vs_curvature.
        data = pd.read_csv(dataset)
        night = data[data.elevation < -3]
        transition = data[(data.elevation > -3) & (data.elevation < 8)]
        day = data[data.elevation > 8]
        width = len(transition) // 5
        points = [module.to_dist(night[module.SPEC_COLS].mean().values)]
        points += [
            module.to_dist(transition.iloc[i * width : (i + 1) * width][module.SPEC_COLS].mean().values)
            for i in range(5)
        ]
        points += [module.to_dist(day[module.SPEC_COLS].mean().values)]
        differences = np.diff(np.array(points), axis=0)
        norms = np.linalg.norm(differences, axis=1)
        unit = np.divide(
            differences, norms[:, None], out=np.zeros_like(differences), where=norms[:, None] > 1e-10
        )
        curvatures = [
            float(np.arccos(np.clip(np.dot(unit[i], unit[i + 1]), -1, 1)) / norms[i])
            if norms[i] > 1e-10 else 0.0
            for i in range(len(differences) - 1)
        ]
        actual["path_curvature"] = float(np.mean(curvatures))
        match = re.search(rf"\b{re.escape(row['name'])}: TransportPath =\s*\(#(.*?)#\)", pvs, re.S)
        require(match is not None, f"Missing PVS observation: {row['name']}")
        for field, expected in row["metrics"].items():
            rational = Fraction(expected["numerator"], expected["denominator"])
            require(rational == Fraction(expected["value"]), f"Invalid exact-float rational: {field}")
            require(abs(actual[field] - float(rational)) <= 1e-12, f"Replay differs: {row['name']}.{field}")
            literal = f"{expected['numerator']}/{expected['denominator']}"
            require(f"{field} := {literal}" in match.group(1), f"PVS value differs: {row['name']}.{field}")
        require("observability := unmeasured" in match.group(1), "Unmeasured C14 evidence was changed")
        for field in ("c20", "c21", "c22"):
            require(result[f"{field}_status"] == row[field], f"Classification differs: {row['name']}.{field}")
    # The operator counterexample is bound to its separate C_DEV fixture.
    operator_data = json.loads((repository / "applications/luces/data/luces_runner_deviation.json").read_text())
    operator_pvs = (repository / "applications/luces/lie_pp_connection.pvs").read_text()
    for row in operator_data["inputs"]:
        name = Path(row["path"]).name.split("_")[0]
        match = re.search(rf"\b{name}_operator: OperatorObservation =\s*\(#(.*?)#\)", operator_pvs, re.S)
        require(match is not None, f"Missing operator observation: {name}")
        for field, source_field in (("path_curvature", "curvature"), ("operator_alignment", "mean_operator_alignment")):
            exact = row["observed_features"][source_field]["exact"]
            literal = f"{exact['numerator']}/{exact['denominator']}"
            require(f"{field} := {literal}" in match.group(1), f"Operator metric differs: {name}.{field}")
    print(f"PASS: {len(fixture['rows'])} C20/C21/C22 observations, exact PVS values and separate C_DEV counterexample")


if __name__ == "__main__":
    main()
