#!/usr/bin/env python3
"""Replay the implemented phase 3 theories and their imports in a fresh project snapshot."""

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


def snapshot_nasalib(report, environment):
    """Isolate library caches and record the exact definitions used by PVS."""
    candidates = [Path(p) for p in environment.get("PVS_LIBRARY_PATH", "").split(os.pathsep) if p]
    source = next((p for p in candidates if (p / "measure_integration/subset_algebra_def.pvs").is_file()), None)
    if source is None:
        raise RuntimeError("NASALib is not on PVS_LIBRARY_PATH; source ~/.zprofile first")
    destination = report / "nasalib"
    files, normalizations = {}, []
    for path in sorted(source.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in (".pvs", ".prf", ".lisp") and path.name != "pvs-strategies":
            continue
        relative = path.relative_to(source)
        original = data = path.read_bytes()
        # PVS 8.1 expects a symbol in this legacy proof-metadata field.
        # The proof commands and theorem statements are unchanged.
        if relative.as_posix() == "orders/non_empty_bounded_sets.prf":
            data, count = re.subn(rb'(?m)^([ \t]*)"shostak"([ \t]*)$', rb'\1SHOSTAK\2', data)
            if count:
                normalizations.append({"file": str(relative), "decision_procedure_fields": count})
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        files[str(relative)] = {
            "original_sha256": hashlib.sha256(original).hexdigest(),
            "snapshot_sha256": hashlib.sha256(data).hexdigest(),
        }
    manifest = {"source": str(source.resolve()), "files": files, "metadata_normalizations": normalizations}
    (report / "nasalib-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    environment["PVS_LIBRARY_PATH"] = str(destination)


NASA_SUPPORT = (
    ("measure_integration", "subset_algebra_def", "nasa_sigma_types",
     ("trivial_subset_algebra_TCC1", "sigma_algebra_TCC1")),
    ("reals", "sigma", "nasa_sum_definition",
     ("sigma_TCC1", "sigma_TCC2", "sigma_TCC3")),
    ("reals", "sigma_nat", "nasa_sum_naturals",
     ("IMP_sigma_TCC1", "int_is_T_high", "nat_is_T_low")),
    ("measure_integration", "generalized_measure_def", "nasa_measure_types",
     ("disjoint_indexed_measurable_TCC1", "disjoint_indexed_measurable_TCC2")),
)


def replay_nasa_formulas(proveit, report, environment, timeout, library, theory, label, names):
    """Replay an explicit set of external support obligations in the library copy."""
    expected = set(names)
    logs = report / "logs"
    command = [
        # The snapshot starts without caches. Retain earlier support statuses
        # when several selected theories share the same library context.
        proveit, "--no-clean", "--no-scripts", "--no-purge", "--disable-oracles",
        "--force", "--timeout", str(timeout), "--log", "--out", label,
        "--dir", str(logs),
        "@" + theory + "." + ":".join(names),
    ]
    with (logs / (label + ".console.log")).open("w") as console:
        process = subprocess.run(command, cwd=report / "nasalib" / library,
                                 env=environment, stdout=console, stderr=subprocess.STDOUT)
    summary_path, log_path = logs / (label + ".summary"), logs / (label + ".log")
    summary = summary_path.read_text(errors="replace") if summary_path.exists() else ""
    log = log_path.read_text(errors="replace") if log_path.exists() else ""
    formulas = dict(match.groups() for line in summary.splitlines() if (match := STATUS.match(line)))
    totals = re.search(r"Grand Totals:\s+(\d+) proofs,\s+(\d+) attempted,\s+(\d+) succeeded", summary)
    errors = bool(re.search(r"\bError:|(?im:^\s*(?:\*\*\*\s*)?Error\b)|unhandled condition", summary + "\n" + log))
    typechecked = theory + " typechecked in" in log
    passed = (process.returncode == 0 and typechecked and not errors and set(formulas) == expected
              and all(status == "proved - complete" for status in formulas.values())
              and bool(totals) and all(int(n) == len(expected) for n in totals.groups()))
    result = {"passed": passed, "returncode": process.returncode, "typechecked": typechecked,
              "error_in_log": errors, "formulas": formulas,
              "summary": "logs/" + label + ".summary", "library": library, "theory": theory,
              "scope": "explicitly selected support obligations"}
    print(f"{'PASS' if passed else 'FAIL'} NASALib {theory}: {len(formulas)} obligations", flush=True)
    return result


def replay_nasa_support(proveit, report, environment, timeout):
    batches, formulas = [], {}
    for library, theory, label, names in NASA_SUPPORT:
        result = replay_nasa_formulas(proveit, report, environment, timeout,
                                      library, theory, label, names)
        batches.append(result)
        formulas.update({library + "@" + theory + "." + name: status
                         for name, status in result["formulas"].items()})
    result = {"passed": all(batch["passed"] for batch in batches),
              "batches": batches, "formulas": formulas}
    (report / "nasalib-results.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


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
    all_names = (root / "translation/phase3-theories.txt").read_text().split()
    names = args.files or all_names
    if len(set(names)) != len(names) or any(name not in all_names for name in names):
        parser.error("--files must contain distinct names from phase3-theories.txt")
    if args.output:
        report = args.output.expanduser().resolve()
        report.mkdir(parents=True, exist_ok=False)
    else:
        report_root = Path.home() / ".local/state/pvs-checks"
        report_root.mkdir(parents=True, exist_ok=True)
        report = Path(tempfile.mkdtemp(prefix="phase3-replay-", dir=report_root))
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
    environment = os.environ.copy()
    snapshot_nasalib(report, environment)
    manifest = {
        "source_directory": str(root), "proveit": str(Path(proveit).resolve()),
        "proveit_version": version.stdout.strip(),
        "pvs_library_path": os.environ.get("PVS_LIBRARY_PATH", ""),
        "replay_pvs_library_path": environment["PVS_LIBRARY_PATH"],
        "nasalib_manifest": "nasalib-manifest.json",
        "source_sha256": hashes, "files": names,
        "all_listed_theories_checked": set(names) == set(all_names),
        "complete_phase3_scope": False,
        "oracles_disabled": True, "import_chain_replayed": True,
        "import_chain_scope": "project-local (proveit --import-chain)",
        "external_library_proofs_replayed": True,
        "external_library_scope": "10 selected support obligations; see nasalib-results.json",
        "proof_timeout": args.timeout,
    }
    (report / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    results, unique = [], {}
    print(f"Reports: {report}", flush=True)
    support = replay_nasa_support(proveit, report, environment, args.timeout)
    for name in names:
        command = [
            proveit, "--clean", "--import-chain", "--no-scripts", "--no-purge",
            "--disable-oracles", "--force", "--timeout", str(args.timeout),
            "--log", "--dir", str(logs), name + ".pvs",
        ]
        with (logs / (name + ".console.log")).open("w") as console:
            process = subprocess.run(command, cwd=snapshot, env=environment, stdout=console, stderr=subprocess.STDOUT)
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
    passed = support["passed"] and all(result["passed"] for result in results)
    totals = {
        "passed": passed, "complete_phase3_scope": False,
        "all_listed_theories_checked": manifest["all_listed_theories_checked"],
        "files": len(results), "unique_formulas": len(unique),
        "unique_complete": sum(status == "proved - complete" for status in unique.values()),
        "own_formulas": sum(result["own_formulas"] for result in results),
        "external_support_formulas": len(support["formulas"]),
        "external_support_complete": sum(status == "proved - complete" for status in support["formulas"].values()),
    }
    (report / "totals.json").write_text(json.dumps(totals, indent=2) + "\n")
    print(json.dumps(totals), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
