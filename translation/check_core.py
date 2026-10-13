#!/usr/bin/env python3
"""Replay the directed PPG, categorical, and refinement proofs in a fresh copy."""

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


CORE_FILES = (
    "directed_pp_graph",
    "ppg_refinement",
    "ppg_config",
    "categorical_pp_graphs",
    "categorical_pp_closure",
    "ppg_refinement_nasa",
    "directed_pp_examples",
    "directed_pp_empty",
)
STATUS = re.compile(
    r"^\s*(\S+?)\.{2,}(proved - complete|proved - incomplete|unfinished|untried)\s+\[",
    re.MULTILINE,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=60, help="Seconds per proof; 0 disables the limit")
    parser.add_argument("--output", type=Path, help="A new directory for the snapshot and reports")
    args = parser.parse_args()
    if args.timeout < 0:
        parser.error("--timeout must be nonnegative")
    proveit = shutil.which("proveit")
    if not proveit:
        parser.error("proveit is not on PATH; source ~/.zprofile first")

    root = Path(__file__).resolve().parent.parent
    if args.output:
        report = args.output.expanduser().resolve()
        report.mkdir(parents=True, exist_ok=False)
    else:
        report_root = Path.home() / ".local/state/pvs-checks"
        report_root.mkdir(parents=True, exist_ok=True)
        report = Path(tempfile.mkdtemp(prefix="core-replay-", dir=report_root))
    snapshot = report / "project"
    logs = report / "logs"
    snapshot.mkdir()
    logs.mkdir()
    hashes = {}
    for source in sorted(root.iterdir()):
        if source.is_file() and source.suffix in (".pvs", ".prf"):
            data = source.read_bytes()
            (snapshot / source.name).write_bytes(data)
            hashes[source.name] = hashlib.sha256(data).hexdigest()

    version = subprocess.run([proveit, "--version"], text=True, capture_output=True, check=True)
    manifest = {
        "source_directory": str(root),
        "proveit": str(Path(proveit).resolve()),
        "proveit_version": version.stdout.strip(),
        "pvs_library_path": os.environ.get("PVS_LIBRARY_PATH", ""),
        "source_sha256": hashes,
        "files": list(CORE_FILES),
        "oracles_disabled": True,
        "proof_timeout": args.timeout,
    }
    (report / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    results = []
    print(f"Reports: {report}", flush=True)
    for name in CORE_FILES:
        command = [
            proveit, "--no-scripts", "--no-purge", "--disable-oracles",
            "--force", "--timeout", str(args.timeout), "--log", "--dir", str(logs),
            name + ".pvs",
        ]
        with (logs / (name + ".console.log")).open("w") as console:
            process = subprocess.run(command, cwd=snapshot, stdout=console, stderr=subprocess.STDOUT)
        summary_path = logs / (name + ".summary")
        summary = summary_path.read_text(errors="replace") if summary_path.exists() else ""
        log_path = logs / (name + ".log")
        log = log_path.read_text(errors="replace") if log_path.exists() else ""
        statuses = STATUS.findall(summary)
        declarations = re.findall(
            r"^\s*(\w+)\s*:\s*(?:THEOREM|LEMMA)\b",
            (snapshot / (name + ".pvs")).read_text(), re.MULTILINE,
        )
        seen = {formula for formula, _ in statuses}
        missing = sorted(set(declarations) - seen)
        unfinished = [formula for formula, status in statuses if status != "proved - complete"]
        totals = re.search(r"Grand Totals:\s+(\d+) proofs,\s+(\d+) attempted,\s+(\d+) succeeded", summary)
        total_matches = bool(totals) and all(int(n) == len(statuses) for n in totals.groups())
        error = bool(re.search(r"(?im)^\s*(?:\*\*\*\s*)?Error\b", summary + "\n" + log))
        passed = (
            process.returncode == 0 and bool(statuses) and total_matches
            and not missing and not unfinished and not error
        )
        result = {
            "file": name + ".pvs", "passed": passed,
            "formulas": len(statuses), "returncode": process.returncode,
            "missing": missing, "unfinished": unfinished, "error_in_log": error,
            "summary": str(summary_path.relative_to(report)),
        }
        results.append(result)
        print(f"{'PASS' if passed else 'FAIL'} {name}: {len(statuses)} formulas", flush=True)
    (report / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    with (report / "results.tsv").open("w", newline="") as output:
        writer = csv.writer(output, delimiter="\t", lineterminator="\n")
        writer.writerow(("file", "passed", "formulas", "returncode", "summary"))
        for result in results:
            writer.writerow(result[key] for key in ("file", "passed", "formulas", "returncode", "summary"))
    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
