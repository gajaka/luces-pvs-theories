#!/usr/bin/env python3
"""Replay the phase 2 theories and their imports in a fresh project snapshot."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


STATUS = re.compile(
    r"^\s*(\S+?)\.{2,}(proved - complete|proved - incomplete|unfinished|untried)\s+\["
)
DECLARATION = re.compile(r"^\s*(\w+)\s*:\s*(?:THEOREM|LEMMA)\b", re.MULTILINE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=60, help="Seconds per proof; 0 disables the limit")
    parser.add_argument("--output", type=Path, help="A new directory for the snapshot and reports")
    parser.add_argument("--files", nargs="+", help="Replay only these theory names, including their imports")
    args = parser.parse_args()
    if args.timeout < 0:
        parser.error("--timeout must be nonnegative")
    proveit = shutil.which("proveit")
    if not proveit:
        parser.error("proveit is not on PATH; source ~/.zprofile first")
    root = Path(__file__).resolve().parent.parent
    all_names = (root / "translation/phase2-theories.txt").read_text().split()
    names = args.files or all_names
    if len(set(names)) != len(names) or any(name not in all_names for name in names):
        parser.error("--files must contain distinct names from phase2-theories.txt")
    if args.output:
        report = args.output.expanduser().resolve()
        report.mkdir(parents=True, exist_ok=False)
    else:
        report_root = Path.home() / ".local/state/pvs-checks"
        report_root.mkdir(parents=True, exist_ok=True)
        report = Path(tempfile.mkdtemp(prefix="phase2-replay-", dir=report_root))
    snapshot, logs = report / "project", report / "logs"
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
        "source_directory": str(root), "proveit": str(Path(proveit).resolve()),
        "proveit_version": version.stdout.strip(),
        "pvs_library_path": os.environ.get("PVS_LIBRARY_PATH", ""),
        "source_sha256": hashes, "files": names,
        "complete_phase2_scope": set(names) == set(all_names),
        "oracles_disabled": True, "import_chain_replayed": True,
        "proof_timeout": args.timeout,
    }
    (report / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    results, unique = [], {}
    print(f"Reports: {report}", flush=True)
    for name in names:
        command = [
            proveit, "--clean", "--import-chain", "--no-scripts", "--no-purge",
            "--disable-oracles", "--force", "--timeout", str(args.timeout),
            "--log", "--dir", str(logs), name + ".pvs",
        ]
        with (logs / (name + ".console.log")).open("w") as console:
            process = subprocess.run(command, cwd=snapshot, stdout=console, stderr=subprocess.STDOUT)
        summary_path = logs / (name + ".summary")
        summary = summary_path.read_text(errors="replace") if summary_path.exists() else ""
        log_path = logs / (name + ".log")
        log = log_path.read_text(errors="replace") if log_path.exists() else ""
        theory, formulas, seen_theories = None, [], set()
        for line in summary.splitlines():
            heading = re.search(r"Proof summary for theory (\w+)", line)
            if heading:
                theory = heading.group(1)
                seen_theories.add(theory)
            match = STATUS.match(line)
            if match and theory:
                formula, status = match.groups()
                formulas.append({"theory": theory, "formula": formula, "status": status})
        missing = []
        seen = {(entry["theory"], entry["formula"]) for entry in formulas}
        for imported in seen_theories:
            source = snapshot / (imported + ".pvs")
            if source.exists():
                missing.extend(
                    imported + "." + declaration
                    for declaration in DECLARATION.findall(source.read_text())
                    if (imported, declaration) not in seen
                )
        unfinished = [
            entry["theory"] + "." + entry["formula"]
            for entry in formulas if entry["status"] != "proved - complete"
        ]
        totals = re.search(r"Grand Totals:\s+(\d+) proofs,\s+(\d+) attempted,\s+(\d+) succeeded", summary)
        counts_match = bool(totals) and all(int(n) == len(formulas) for n in totals.groups())
        errors = bool(re.search(r"\bError:|(?im:^\s*(?:\*\*\*\s*)?Error\b)|unhandled condition", summary + "\n" + log))
        typechecked = bool(re.search(r"\b" + re.escape(name) + r" typechecked in\b", log))
        passed = process.returncode == 0 and name in seen_theories and counts_match and typechecked and not (missing or unfinished or errors)
        result = {
            "file": name + ".pvs", "passed": passed, "typechecked": typechecked,
            "returncode": process.returncode, "formulas_with_imports": len(formulas),
            "own_formulas": sum(entry["theory"] == name for entry in formulas),
            "missing": missing, "unfinished": unfinished, "error_in_log": errors,
            "summary": str(summary_path.relative_to(report)), "formulas": formulas,
        }
        results.append(result)
        for entry in formulas:
            key = entry["theory"] + "." + entry["formula"]
            unique[key] = entry["status"]
        (report / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        print(f"{'PASS' if passed else 'FAIL'} {name}: {result['own_formulas']} own, {len(formulas)} with imports", flush=True)
    passed = all(result["passed"] for result in results)
    totals = {
        "passed": passed, "complete_phase2_scope": manifest["complete_phase2_scope"],
        "files": len(results), "unique_formulas": len(unique),
        "unique_complete": sum(status == "proved - complete" for status in unique.values()),
        "own_formulas": sum(result["own_formulas"] for result in results),
    }
    (report / "totals.json").write_text(json.dumps(totals, indent=2) + "\n")
    print(json.dumps(totals), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
