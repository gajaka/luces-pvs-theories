# NASAlib saved-proof metadata compatibility

The supported base is the official
[`nasa/pvslib` revision `f3bb2b36240ff3413136b2a46e431c47350fe108`](https://github.com/nasa/pvslib/commit/f3bb2b36240ff3413136b2a46e431c47350fe108).
For a fresh checkout, choose a new directory and pin that revision:

```bash
git clone https://github.com/nasa/pvslib.git /path/to/nasalib
git -C /path/to/nasalib checkout f3bb2b36240ff3413136b2a46e431c47350fe108
```

PVS 8.1.2 expects a symbol in each saved proof's decision-procedure metadata
slot. Some upstream records contain the string `"shostak"`. That can prevent
an entire `.prf` file from loading, even when its proof programs are present.
The compatibility change replaces that metadata value with the symbol
`SHOSTAK`. It changes no theorem statement, tactic, proof program or dependency
list, and does not make an unfinished proof succeed.

## Recorded scope

The 2026-10-29 audit inspected the 4,933 external-library input records of the
full-replay snapshot, including all 2,309 `.prf` files. It recognized 51,971
modern or legacy proof records, with no parser errors or unclassified record
shapes. The two orphan-export files use a separate format without this metadata
slot. Tactic strings and proof descriptions were excluded from the metadata
scan. There were no string-valued decision-procedure candidates in the bundled
PVS `lib` input.

The snapshot already contained the earlier one-slot
`analysis/integral_split_scaf.prf` fix. The audit found 129 additional slots in
43 NASAlib proof files. The versioned [manifest](manifest.json) therefore covers
**44 files and 130 metadata slots**, including that original fix. Each file has
one exact upstream before/after hash, its unchanged `.pvs` hash and a fingerprint
of every proof program. Each hunk identifies its original byte offset, theory,
formula, proof variant and program hash.

The observed loader error in `orders/non_empty_bounded_sets.prf` concerns four
judgement proofs: the nonempty and boundedness conditions for both above- and
below-bounded sets. Its [readable patch](non_empty_bounded_sets.patch) shows all
four metadata edits. The earlier
[integral patch](integral_split_scaf.patch) remains available. The complete
multi-file patch specification is the offset manifest; it avoids republishing
large proof files just to change a few metadata bytes.

This is a compatibility inventory, not a claim that every affected file belongs
to every project's required dependency closure. The public proof checker must
still replay the actual required proof bodies. The older historical PPG runs
used separate locally repaired proof programs; this metadata bundle does not
install those older program changes.

## Check and apply

From the PVS repository, check the selected installation:

```bash
python3 scripts/apply_library_proof_fixes.py \
  --nasalib-root /path/to/nasalib --check
```

Checking is the default and writes nothing. Exit code 0 means every known fix
is already present; 1 means one or more exact supported originals need fixing;
2 reports an unknown file/source version, a malformed manifest or another error.
Apply the supported changes explicitly while no PVS session is using that
library:

```bash
python3 scripts/apply_library_proof_fixes.py \
  --nasalib-root /path/to/nasalib --apply
```

The tool validates every target before the first write. It checks the pinned
source hashes, parses the actual metadata slots, checks all record identities
and verifies preservation of every recorded proof-program hash.
Only the specified quoted metadata values can change. An identically spelled
string inside a tactic cannot be patched. Offset hunks are applied from the
end of each file so earlier offsets retain their original meaning.

Each changed file is replaced atomically after saving and verifying its
original bytes beside it as `.prf.ppg-original-<before-sha256>.bak`. Existing
backups are retained and checked. A fixed file is left untouched, including its
mtime. Unknown input versions, modified source statements, unexpected backups,
symlinked targets and escaping paths are rejected. The schema-1 single-context
manifest format remains supported with the same metadata-slot guard.

Applying these edits is setup, not proof replay. Run the repository's unchanged
public checker afterward. The temporary-library regression tests require only
Python's standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s tests -p test_library_proof_fixes.py -v
```

The tests cover multiple slots, preservation of a tactic containing the same
string, original backups, permissions, idempotence, changed source/proof
rejection, record/program identity, path/offset tampering, prevalidation of the
whole batch and the legacy manifest format.
