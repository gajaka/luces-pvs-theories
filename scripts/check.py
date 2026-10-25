#!/usr/bin/env python3
"""Typecheck or replay PVS theories in isolated, persistent worker sessions."""

import argparse
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import threading


ACTIVE_PROCESSES = set()
PROCESS_LOCK = threading.Lock()
STOP_REQUESTED = threading.Event()
EXCLUDED_DIRS = {".git", ".vscode", "pvsbin", "translation", "__pycache__", "node_modules", ".venv", "venv"}


def stop_workers():
    with PROCESS_LOCK:
        STOP_REQUESTED.set()
        processes = list(ACTIVE_PROCESSES)
    for process in processes:
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
    for process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()


def within(path, parent):
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def lisp_string(value):
    value = str(value)
    if any(char in value for char in "\x00\r\n"):
        raise ValueError("PVS paths must not contain newlines or NUL characters")
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def source_paths(root):
    for directory, children, names in os.walk(str(root), followlinks=False):
        children[:] = sorted(name for name in children if name not in EXCLUDED_DIRS and not name.startswith("."))
        for name in sorted(names):
            yield Path(directory) / name


def tracked_paths(root):
    try:
        top = subprocess.check_output(["git", "-C", str(root), "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL, text=True).strip()
        if Path(top).resolve() != root:
            return None
        paths = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"], stderr=subprocess.DEVNULL)
        return {root / os.fsdecode(path) for path in paths.split(b"\0") if path}
    except (OSError, subprocess.CalledProcessError):
        return None


def selected_files(root, args, tracked):
    files = sorted(path for base in (root / "theories", root / "applications") if base.is_dir()
                   for path in source_paths(base) if path.suffix == ".pvs" and path.is_file()
                   and (tracked is None or path in tracked))
    if args.all:
        selected = files
    elif args.file:
        requested = Path(args.file)
        requested = requested if requested.is_absolute() else root / requested
        requested = requested.resolve()
        if not within(requested, root) or requested.suffix != ".pvs" or not requested.is_file():
            raise ValueError("--file must name a PVS file inside the source tree")
        selected = [requested]
    else:
        group = Path(args.group)
        matches = []
        for base in (root / "theories", root / "applications"):
            if (base / group).is_dir():
                matches.append(base / group)
        if args.group == "Sterbenz" and (root / "Sterbenz").is_dir():
            matches.append(root / "Sterbenz")
        if (root / group).is_dir() and group.parts[0] in ("theories", "applications"):
            matches.append(root / group)
        matches = sorted(set(path.resolve() for path in matches))
        if len(matches) != 1:
            raise ValueError("--group must identify one directory under theories/ or applications/, or Sterbenz")
        selected = sorted(path for path in source_paths(matches[0]) if path.suffix == ".pvs" and path.is_file()
                          and (tracked is None or path in tracked))
    if not selected:
        raise ValueError("No PVS files match the selection")
    return [path.resolve().relative_to(root) for path in selected]


def copy_sources(source, destination, records, label, allowed=None):
    """Copy source/proof inputs, excluding generated caches and private ledgers."""
    for path in source_paths(source):
        if (allowed is not None and path not in allowed) or not path.is_file():
            continue
        if path.suffix not in (".pvs", ".prf", ".lisp") and path.name not in ("pvs-strategies", "pvs-attachments", ".pvslib", ".nasalib"):
            continue
        relative = path.relative_to(source)
        data = path.read_bytes()
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        records.append({"source": str(path), "copy": str(Path(label) / relative),
                        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})


def external_roots(pvs, source_root):
    paths = [Path(value).expanduser().resolve() for value in os.environ.get("PVS_LIBRARY_PATH", "").split(os.pathsep) if value]
    installed = Path(pvs).resolve().parent / "nasalib"
    if installed.is_dir() and installed not in paths:
        paths.append(installed)
    return list(dict.fromkeys(path for path in paths if path.is_dir() and not within(path, source_root)))


def run_worker(index, selected, snapshot, reports, args, pvs, driver, library_count):
    worker = reports / ("worker-%d" % index)
    worker.mkdir()
    tree = worker / "inputs"
    shutil.copytree(str(snapshot), str(tree))
    workspace = tree / "project"
    libraries = [tree / "libraries" / str(number) for number in range(library_count)]
    status_file = worker / "status.json"
    manifest = worker / "manifest.sexp"
    project_files = sorted(path for path in source_paths(workspace) if path.suffix == ".pvs" and path.is_file())
    manifest.write_text("(:root %s :mode %s :timeout %d :status-file %s :library-roots (%s) :project-files (%s) :files (%s))\n" % (
        lisp_string(str(workspace) + os.sep), lisp_string("typecheck" if args.typecheck else "proof"),
        args.timeout,
        lisp_string(status_file), " ".join(lisp_string(str(path.resolve()) + os.sep) for path in libraries),
        " ".join(lisp_string(path) for path in project_files),
        " ".join(lisp_string(workspace / name) for name in selected)), encoding="utf-8")
    env = os.environ.copy()
    local = [workspace / "theories", workspace / "applications", workspace]
    env["PVS_LIBRARY_PATH"] = os.pathsep.join(str(path) for path in local + libraries if path.is_dir())
    env["PPG_CHECK_MANIFEST"] = str(manifest)
    if args.heap_mib:
        env["PVS_SBCL_DYNAMIC_SPACE_SIZE"] = str(args.heap_mib)
    command = [pvs, "-raw", "-nobg", "-L", str(driver),
               "-E", "(pvs::ppg-check-run)"]
    (worker / "command.json").write_text(json.dumps({"argv": command, "PVS_LIBRARY_PATH": env["PVS_LIBRARY_PATH"],
                                                   "selected_files": [str(path) for path in selected],
                                                   "project_input_files": len(project_files)}, indent=2) + "\n")
    with (worker / "console.log").open("wb") as log:
        with PROCESS_LOCK:
            if STOP_REQUESTED.is_set():
                raise ValueError("Worker cancelled")
            process = subprocess.Popen(command, cwd=str(workspace), env=env, stdin=subprocess.DEVNULL,
                                       stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            ACTIVE_PROCESSES.add(process)
        try:
            returncode = process.wait(timeout=args.wall_timeout or None)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
            raise
        finally:
            with PROCESS_LOCK:
                ACTIVE_PROCESSES.discard(process)
    with (worker / "console.log").open(encoding="utf-8", errors="replace") as log:
        unexpected_debugger = any(line.lstrip().lower().startswith((
            "debugger invoked on a", "unhandled condition in --disable-debugger mode")) for line in log)
    result = {"worker": index, "process_exit": returncode, "selected_files": len(selected),
              "unexpected_lisp_debugger": unexpected_debugger, "passed": False}
    if status_file.is_file():
        status = json.loads(status_file.read_text(encoding="utf-8"))
        result["status"] = status
        result["passed"] = (returncode == 0 and not unexpected_debugger and status.get("complete") is True
                            and status.get("files") == len(selected) and status.get("incomplete") == 0
                            and status.get("mode") == ("typecheck" if args.typecheck else "proof"))
    (worker / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print("Worker %d: %s; log: %s" % (index, "PASS" if result["passed"] else "FAIL", worker / "console.log"), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--all", action="store_true", help="check theories/ and applications/; Sterbenz is separate")
    scope.add_argument("--group", metavar="NAME", help="check one package, for example hls, or Sterbenz")
    scope.add_argument("--file", metavar="PATH", help="check one source file and its loaded project dependencies")
    parser.add_argument("--typecheck", action="store_true", help="check types without replaying proofs")
    parser.add_argument("--jobs", type=int, choices=(1, 2), default=1, help="independent PVS sessions (default: 1)")
    parser.add_argument("--timeout", type=int, default=60, help="seconds per proof; 0 disables the proof timer")
    parser.add_argument("--wall-timeout", type=int, default=0, help="optional limit in seconds for each worker session")
    parser.add_argument("--heap-mib", type=int, help="set the PVS SBCL heap per worker; otherwise retain installation settings")
    parser.add_argument("--report-dir", type=Path, help="new output directory outside the source tree")
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1], help="source tree to snapshot")
    parser.add_argument("--pvs", default=os.environ.get("PVS", "pvs"), help="PVS launcher executable")
    parser.add_argument("--list", action="store_true", help="list selected files without starting PVS")
    args = parser.parse_args()
    if args.timeout < 0 or args.wall_timeout < 0 or (args.heap_mib is not None and args.heap_mib <= 0):
        parser.error("timeouts must be nonnegative and heap size must be positive")
    root = args.source_root.expanduser().resolve()
    try:
        tracked = tracked_paths(root)
        files = selected_files(root, args, tracked)
        if args.list:
            print("\n".join(str(path) for path in files))
            return 0
        pvs = shutil.which(args.pvs)
        if pvs is None:
            raise ValueError("PVS executable not found: " + args.pvs)
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
        state = Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state")))
        reports = (args.report_dir or state / "pvs-checks" / ("check-" + now)).expanduser().resolve()
        if within(reports, root):
            raise ValueError("--report-dir must be outside the source tree")
        reports.mkdir(parents=True, exist_ok=False)
        snapshot = reports / "snapshot"
        records = []
        if tracked is not None:
            tracked.update(root / name for name in files)
            tracked.update((root / name).with_suffix(".prf") for name in files)
        for name in ("theories", "applications", "Sterbenz"):
            if (root / name).is_dir():
                copy_sources(root / name, snapshot / "project" / name, records, "project/" + name, tracked)
        libraries = external_roots(pvs, root)
        # Keep the external library search order while isolating their caches.
        for index, library in enumerate(libraries):
            copy_sources(library, snapshot / "libraries" / str(index), records, "libraries/%d" % index)
        (reports / "inputs.json").write_text(json.dumps({"source_root": str(root),
            "external_libraries": [str(path) for path in libraries], "files": records}, indent=2) + "\n")
        workers = min(args.jobs, len(files))
        driver = Path(__file__).resolve().with_name("check-pvs.lisp")
        print("Checking %d files in %d persistent PVS session(s). Reports: %s" % (len(files), workers, reports), flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            try:
                futures = [pool.submit(run_worker, index + 1, files[index::workers], snapshot, reports,
                                       args, pvs, driver, len(libraries)) for index in range(workers)]
                results = [future.result() for future in futures]
            except BaseException:
                stop_workers()
                raise
        passed = all(item["passed"] for item in results)
        (reports / "result.json").write_text(json.dumps({"passed": passed, "mode": "typecheck" if args.typecheck else "proof",
            "selected_files": len(files), "workers": results,
            "counts_are_per_worker_and_dependency_overlap_is_not_deduplicated": workers > 1}, indent=2) + "\n")
        print("%s: %s" % ("PASS" if passed else "FAIL", reports / "result.json"), flush=True)
        return 0 if passed else 1
    except KeyboardInterrupt:
        print("check.py: interrupted; worker processes stopped", file=sys.stderr)
        return 130
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print("check.py: %s" % error, file=sys.stderr)
        return 1


def terminate(signum, frame):
    raise KeyboardInterrupt()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, terminate)
    sys.exit(main())
