# Measured certificate inputs

These artifacts bind finite numerical observations to the adjacent PVS
literals. They record data and producer hashes and are rechecked by the
commands below. The [model-scope note](../../../docs/LUCES_MODEL_SCOPE.md)
distinguishes these computations from conditional model laws and physical
claims.

`luces_runner_deviation.json` records actual evaluations of
`master-controler/paper3/dataset/boot320_merged_dawn.csv` and
`boot347_dawn.csv`. It includes the CSV and producer SHA-256 hashes, exact
binary-float ratios, measured feature enclosures and the checked difference
between each returned float score and the real expression with weights
`1/100, 1, 2, 5`. The cutoffs remain `1` and `3`.

The adjacent `../luces_runner_deviation.pvs` proves classification and its
robustness under the recorded bounds. No source/sink strengths are inferred:
the measured mass term is a residual between normalized distributions.
Operator alignment is distinct from the signed spectral flow measured by
the separate `C_GEN` certificate.

To regenerate or check the artifact, use a Python environment containing
NumPy, pandas, SciPy and POT from the `master-controler` repository root:

```bash
python3 -m cert_runner.deviation_binding
python3 -m cert_runner.deviation_binding \
  --check ../luces-pvs-theories/applications/luces/data/luces_runner_deviation.json
```

The check recomputes from both CSVs and rejects changed data, producer or
formal source hashes. It is a finite reproducibility check. PVS checks the
stated real-arithmetic implications; Python execution, floating-point
arithmetic in general, the optimal-transport solver and the sensor physics
remain outside that proof.

`boot320_plan_candidates.json` is a separate finite repair-bank artifact. Its
five actual independent/optimal coupling mixtures use the first populated
boot320 elevation-bin pair. It records every matrix and measured feature,
the shared local-certificate contract hash, an unchanged positive signed GEN
observation and the exact CSV dataset key. The complete certificate family
rejects the first four candidates; the finite search selects the optimal one.
The identical artifact in `master-controler/cert_runner/contracts/` can be
rechecked there with:

```bash
python3 -m cert_runner.local_plan_binding \
  --check cert_runner/contracts/boot320_plan_candidates.json
```

This is a proposal over measured feature snapshots. It does not verify the
transport solver or execute a physical repair.

The [local certificate instance](../luces_local_certificate_repair.pvs) evaluates
the actual atom/conjunction fragment, derives locality from computed read sets,
and retains all eight list positions. It proves finite search soundness and
completeness for the supplied bank and obtains the indexed repair contract from
the returned checked result. Its actual bank selects the optimal coupling and
preserves GEN and the dataset key. The recheck also compares the generated
literal block with the current checker expressions and measured float ratios,
byte for byte. The generator itself is not a formally verified JSON parser.

`dual_observability.json` binds all 27 boot320 and 48 boot347 rows in the
strict -4 to -2 degree overlap window. It records each row's exact float
ratios for elevation, lux, spectral sum and `geo_kappa`, and checks all rows
against outward rational enclosures. The
[dual-chart model](../dual_observability.pvs) proves that these numerical
enclosures imply the versioned `overlap-v1` checks. Its two literal witness
rows come from the CSVs; separate concrete counterexamples show why elevation
alone does not imply positive lux and why spectral signal alone does not
bound geometry. No physical observability theorem is inferred from the
window or from signal variance.

From `master-controler`, recheck every observed row and the generated PVS
literal block with:

```bash
python3 -m cert_runner.observability_binding \
  --check ../luces-pvs-theories/applications/luces/data/dual_observability.json
```

`lie_observations.json` binds three rows from the actual C20/C21/C22 producer:
boot320, boot334 and boot347. It records exact float ratios, dataset and source
hashes and the corresponding PVS observations. The additional path curvature
uses the same seven windows as C20; it is different from the DEV binning and
its operator metric. Observability remains `unmeasured` because this producer
does not check C14. Recompute from this repository with the same scientific
Python dependencies:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_lie_observations.py \
  --source-root ../master-controler
```

The recheck also binds the separate DEV operator-alignment counterexample.
Neither a finite table's inverse ordering nor a passed C21 screen proves a
universal curvature law or a Lie exponential representation.
