# Theorem scope and local repair

The source-result count is a declaration inventory. It includes structural
laws, definition accessors and helper lemmas alongside the main arguments.
The historical whole-library checks in the README are dated separately from
later changes to individual theories.

## Changes on 2026-10-28

- Removed `linear_strict_not_equiv_aux: THEOREM TRUE` from
  `theories/certification/ppg_list_quotient_linear.pvs` and its saved proof file.
  The actual `equiv_convex` result remains proved.
- Renamed the one-way order-preservation result to `linear_cert_le_of_le` in
  both `ppg_list_quotient_linear.pvs` and `cert_quotient.pvs`, with matching
  proof names. No converse is claimed for an arbitrary certificate family.
- Replaced four weak statements in `theories/ppg_core/ppg_repair_semantics.pvs`
  with properties of an explicit local value update, and added
  `repair_restores`.

These changes match the corresponding
[Lean theorem-scope cleanup](https://github.com/gajaka/ppg-lean/blob/main/docs/THEOREM_SCOPE.md).
One placeholder was removed and one restoration theorem was added, leaving
the total number of explicit Lean source results unchanged at 1,824.

## Fixed specification and changed data

Initially, each abstract slot stores its own `State` value. `repair_choice`
selects a healthy reachable value when a repair candidate exists; otherwise
it selects the original value. The data update is explicit:

```text
repair_state(G, v)(w) = IF w = v THEN repair_choice(G, v) ELSE w ENDIF
```

The repaired graph view evaluates the original ``G`invariant_holds`` predicate
on those updated data. Its edge and reachability relations are unchanged.

| Result | Proven property |
| --- | --- |
| `repair_restores` | An available repair restores its target slot. |
| `repair_locality` | Every other slot retains its exact value and health. |
| `healthy_self_stable` | A healthy target leaves selection and the graph view unchanged. |
| `repair_no_cascade` | Every previously healthy slot remains healthy. |
| `active_independent_of_isolated` | Edges away from the target retain their activity. |

The predicate on stored values stays fixed. The proof uses the specified
local-copy operation and an explicit candidate-existence assumption. A concrete
C implementation, shared state or physical operation needs a separate
refinement argument; this theory does not provide a repair-search algorithm.

## Interpretation of the helper results

Projection lemmas and structural identity/composition laws remain part of the
library. Graph-extension results hold under their fixed-predicate model.
State-repair results require target restoration and core preservation as
separate obligations on the chosen operator.

Numerical LLL budget infeasibility rules out a sufficient certification
criterion. It does not by itself establish that no satisfying state or repair
exists. Pointwise complementary-slackness results should be read with their
stated entry-level assumptions, rather than as an aggregate strong-duality
theorem.

## Verification scope

The changed repair theory and both quotient files are checked with the public
`scripts/check.py` runner in isolated copies. Proof replay checks their project
dependencies and the required original external proof bodies, with oracles
disabled. A clean publication candidate excludes unrelated local proof edits.
The scoped runs establish the changed results; they do not constitute a new
replay of the entire library or of the separate `Sterbenz` development.

The clean publication candidate passed all three targeted runs on 2026-10-28:

| Selected file | Replayed Project bodies | Required Native bodies |
| --- | ---: | ---: |
| `theories/ppg_core/ppg_repair_semantics.pvs` | 10 | 0 |
| `theories/certification/ppg_list_quotient_linear.pvs` | 69 | 0 |
| `theories/certification/cert_quotient.pvs` | 91 | 26 |

Each run completed with zero unfinished bodies. Dependency counts can overlap
between runs. The original quotient check needs both the installed `nasalib`
and `lib` roots on `PVS_LIBRARY_PATH`, so the isolated runner can copy the
required original `finite_sets` proof inputs. No installed library or runner
was changed for these checks.

## Structural and application corrections

The later 2026-10-28 changes address the structural gaps separately from the
first placeholder cleanup. That stage recorded 1,842 Lean results in 192
modules. This does not relabel the dated full PVS translation ledger as a replay
of every later extension.

| Area | Established connection and assumptions |
| --- | --- |
| Certification and dependency | `ppg_certification_dependency` uses the actual finite family predicates. Full-family footprints include passing certificates; locality, a frame outside the changed component and a full component post-check imply preservation, strict blocker reduction and the `valid_repair` contract. A finite checked plan covering initial blockers certifies the original family at the fixed level. |
| Meta refinement | `ppg_refinement_meta` identifies its induced relation with the core RR and constructs compatibility from base-relation inclusion with unchanged abstraction/concretization. The original accessors remain elementary structural laws. |
| Selection and quotient | The generic selection graph descends the invariant and RR to equivalence classes, then proves the shared categorical morphism and quotient predicates. Noncollapse and descent are explicit hypotheses. The specification bridge retains edge-or-collapse in general and gives a categorical quotient on certified subgraphs under noncollapse. |
| Operational MT repair | `ppg_mt_topology_bridge` connects the actual constant-log trajectory to finite directed reachability when each primitive resampling is an admitted edge. Its intermediate states need not satisfy the target, so the recovery path is not a certified PPG walk. |

The earlier `ppg_certification_dependency` uses predicate-valued vertices and
merges repeated identical predicates through `listSet`. The later
`ppg_indexed_certification_dependency` uses bounded list positions, matching
Lean's indexed family, and retains separate footprints and plan entries for
repeated predicates. It proves the exact image relation between failing
positions and the older blocking set; it does not claim the two graphs are
isomorphic. The generic indexed bridge still requires predicate locality and
checked repair premises. The concrete finite-read LUCES instance derives
locality from its checker syntax and obtains the component post-check from its
search result; see the next section. The state-repair bridge derives its preservation obligation; the
unchanged graph-extension helpers in `SelfAssessment` still follow from their
fixed-predicate definitions.

The general MT witness-budget expectation theorem uses product-table random
initialization. A constant-log existence proof for an arbitrary start does not
establish a probability or the same expected-work bound for that start. The
separate fixed-start finite-potential results retain their explicit hypotheses.
A component-preservation statement requires the chosen log to stay within that
component. Numerical LLL budget infeasibility excludes a sufficient criterion;
it is not semantic impossibility of repair. Both numerical presentations now use
`lll_budget_feasible`, `lll_budget_infeasible` and
`lll_budget_feasible_or_infeasible` (with `?` on the earlier presentation's
boolean predicate names). The dichotomy is classical excluded middle, without
a decision procedure. The original abstract
`mtRepairGraph` keeps reachability independent of its supplied edges; the new
operational graph supplies the explicit edge connection.

### Application contracts

- `tangent_bundle` defines the actual finite pushforward and restricts endpoint
  reconstruction to representable pairs. Its law package is an explicit
  hypothesis, with a fully defined one-atom witness, a positive discrepancy
  example and a regression proving that the removed universal reconstruction
  condition conflicts with finite log collisions. It does not prove general
  Brenier differentiability or construct a Wasserstein tangent bundle.
- `transport_ppg` uses snapshots with a fixed provenance epoch, measured
  certificate fields and an actual record update. A valid candidate restores
  its target and preserves all already certified edges, hence any fixed
  protected family. Same-epoch RR is proved an equivalence. A concrete repair
  witnesses a PPG edge; recursive regime paths distinguish surviving prefixes
  from unreachable destinations after a cycle edge fails. Raw transport data
  extraction and a Spearman implementation remain separate obligations.
- `unbalanced_regime` replaces its twenty-five global axioms with an explicit
  numerical observation record, weighted deviation and a checked calibration
  predicate. Classification inequalities and nonvacuous calibrated examples
  are derived arithmetically. The reversal/coherence implication requires an
  explicit observation-consistency test; it is not an empirical physical law.
- `opentitan_boot_instance` uses the shared directed graph with four concrete
  stages and signature/hash/policy input checks. It proves graph validity, an
  actual successful walk and loss of later-stage reachability on signature
  failure. A new theorem in `lowrisc_boot_verification` proves that the legacy
  undirected strict-layer predicate forces an empty edge set. That interface
  is retained as legacy material, with its limitation documented.

These revised application theories contain no hand-written `AXIOM`
declarations. The later finite-model revisions described in
[LUCES model scope](LUCES_MODEL_SCOPE.md) also replace the remaining LUCES axioms.
Explicit model laws, checked observations and implementation boundaries still
matter; no unconditional geometric, physical, cryptographic or firmware
correctness result follows from an axiom count.

### Checks of the clean publication candidate

The corrected theories are checked with the unchanged public `scripts/check.py`
runner, using isolated cold source/proof copies, oracles disabled, a 6,144 MiB
heap and one worker per selected file. The candidate excludes unrelated local
proof alternatives and private translation artifacts. Counts below include
imported dependencies and TCCs; runs can overlap and must not be added as a count
of distinct source theorems. All twelve selected runs passed with zero
unfinished bodies and complete dependency chains on 2026-10-28.

| Selected file | Project proof bodies | Required Native bodies |
| --- | ---: | ---: |
| `theories/ppg_core/ppg_refinement_meta.pvs` | 15 | 0 |
| `theories/certification/ppg_selection_quotient_graph.pvs` | 61 | 0 |
| `theories/certification/ppg_list_quotient_bridge.pvs` | 82 | 0 |
| `theories/certification/ppg_certification_dependency.pvs` | 133 | 0 |
| `theories/moser_tardos/ppg_mt_topology_bridge.pvs` | 103 | 0 |
| `theories/moser_tardos/ppg_probabilistic.pvs` | 11 | 23 |
| `theories/local_lemmas/ppg_generic_probabilistic.pvs` | 27 | 0 |
| `applications/luces/tangent_bundle.pvs` | 18 | 0 |
| `applications/luces/transport_ppg.pvs` | 42 | 0 |
| `applications/luces/unbalanced_regime.pvs` | 15 | 0 |
| `applications/boot/opentitan_boot_instance.pvs` | 41 | 0 |
| `applications/boot/lowrisc_boot_verification.pvs` | 59 | 14 |

For example, with the installed NASAlib and bundled `lib` directories on
`PVS_LIBRARY_PATH`:

```sh
python3 scripts/check.py \
  --file theories/certification/ppg_certification_dependency.pvs \
  --jobs 1 --heap-mib 6144 --timeout 60 --wall-timeout 1200
```

The shared categorical theory is replayed through the quotient checks. Edits in
`cert_selection.pvs` and `cert_quotient_bridge.pvs` only clarify the scope of their
existing weaker projection predicates. These scoped checks do not replace the
dated full-library replay record.

## Finite reads, repeated positions and measured repair

The next integration adds the position-keyed dependency bridge and the concrete
`applications/luces/luces_local_certificate_repair.pvs` instance. Its atoms read
one field; a conjunction's read set is the structural union. An induction on
that syntax proves locality. The eight-position family includes the conjunction
of the four local-plan comparisons, a repeated Monge comparison, signed GEN
and the exact dataset key. Repetition is retained at separate positions.

Search checks every tracked certificate and the fixed write frame before
returning a candidate. Its soundness and finite-bank completeness theorems
derive the indexed component-repair and `valid_repair` obligations from that
result. The measured bank contains five actual coupling mixtures. Its selected
snapshot restores the entire family and leaves GEN and dataset identity
unchanged. This is finite selection over supplied candidates, not a guarantee
that an arbitrary bank has a repair or that the selected snapshot has been
applied to hardware.

The PVS source/proof closure of the indexed bridge passed **139 project and
3 required Native bodies** across 13 modules. The concrete repair closure
passed **163 project and 3 required Native bodies** across 14 modules. These
2026-10-28 runs used the public checker and completed with no unfinished bodies;
the closures overlap. The Python exporter separately recomputes the measured
matrices, comparisons and hashes. It is not a verified parser or solver.

The Lean companion additionally parses the included ASCII JSON byte lists with
a pure finite parser and proves the source-to-contract and source-to-row
bindings in the kernel. Its build and axiom audit are recorded by the Lean
repository. This stronger Lean input binding does not change the PVS exporter's
proof boundary or verify NumPy, POT, firmware or sensor physics.

The latest Lean inventory is **1,876 explicit source results in 198 modules**.
This describes the companion Lean library, not a replacement for the historical
PVS translation ledger or a claim that every later PVS extension was replayed
in one whole-library run.

## Completed incremental verification

The [incremental receipt](../reports/PVS_INCREMENTAL_REPLAY_20261029.json),
completed on **2026-10-29**, binds each changed source and proof file to the
publication. Its 28 changed sources comprise 27 semantic changes and one
equivalent generated ADT rendering. Its 30 changed proof files also include
the three proof-only repairs `density_history_version`, `point_native_mean`
and `native_integral_sequence_eq`. Their unchanged statements now replay in
the ordinary public closure: **723 Project bodies and 956 required Native
originals**, with zero unfinished bodies, missing scripts, derived or mapped
credit, or Native failures. The separate Shannon closure passed **17 Project
bodies and 761 required Native originals**. Eight source-matched earlier
normal passes supply the remaining changed-source coverage. The report
preserves per-run counts and source identities; overlapping dependency bodies
are not summed as distinct theorems. All 30 required proof-bearing roots are
covered. This is incremental verification, not a replacement for the dated
historical full-library replay.

## External proof-file metadata

The published [NASAlib compatibility bundle](../library-proof-fixes/README.md)
replaces 130 quoted decision-procedure metadata values in 44 pinned proof files.
It checks exact byte offsets and proof-record identities, unchanged adjacent
`.pvs` hashes and fingerprints of all proof programs. A 44-file external
sandbox test verifies the original backups, all expected after-hashes and an
idempotent second application. An ordinary Lisp reader checks the resulting
metadata fields are symbols; no PVS prover is loaded by that reader check.

This validation is distinct from proof replay. The recorded full V2 input copy
uses the pinned upstream library with only the earlier single integral-metadata
fix. The additional 43-file compatibility set has not been substituted into
that frozen input copy. Any proof result using a later library input must retain
its own input hashes and required-Native replay record. Metadata compatibility
alone adds no theorem or proof-body credit.

## Curvature extracted from certified walks

The subsequent `pp_walk_geometry` development computes angular curvature from
the ordered coordinates of a `directed_pp_graph.Prewalk`. The coordinate map
is an explicit input. Norms, normalized differences, clipping, inverse cosine,
small-step branches and the finite average are mathematical functions, rather
than independently supplied scalar observations.

Locality is proved for each contribution's three-vertex window. Equality of
observed traces implies equality of the computed curvature. A geometric
certificate checks `pp_path`, a minimum of three samples, active successive
steps and the curvature bound. Inactive samples cannot earn a certificate from
a totalized zero score. Its preservation under `pp_transform` uses preservation of the same
walk in an extended graph; it does not allow changes to the coordinate map or
certify every new path in that graph.

`lie_pp_connection` has a fixed coordinate-map parameter and a
`CurvatureBoundPrewalk` subtype equating reported and computed curvature. Its
certification result also recovers the actual vertex invariants. The earlier
unconstrained `MeasuredPrewalk` and its graph-independent field-projection
theorem are replaced by this interface. Legacy float fixtures remain
`AttachedObservation`; their other numeric fields are not silently certified.

Concrete normalized samples provide both a straight and an orthogonally bent
three-sample path. The graph extension admits both, while the zero-curvature
certificate admits only the straight path. Missing graph edges and a forged
zero report for the bent path are rejected. These witnesses check the actual
graph and geometric definitions rather than assuming the desired curvature.

This application extension is separate from the historical Lean translation
ledger. It formalizes an exact-real angular estimator, not NumPy binary64
execution, calibration correctness, POT couplings, C20 coherence or a physical
Lie generator. The prior finite-read integration receipt remains a dated
record for its own source hashes; it is not evidence for this later extension.

The completed [walk-geometry replay](../reports/PVS_WALK_GEOMETRY_20261029.json)
checks both changed entry points and five Project modules. All **90 Project
bodies and 757 required original Native bodies** passed the unchanged normal
checker, with no unfinished bodies, missing scripts, copied or derived credit,
or Native failures. The numerical fixture recheck also passed for all three
recorded boot logs; those observations were not promoted to exact-real traces.

With the library setup described in the repository README, the entry points
can also be replayed separately:

```sh
python3 scripts/check.py --file applications/luces/pp_walk_geometry.pvs \
  --jobs 1 --heap-mib 6144 --timeout 180

python3 scripts/check.py --file applications/luces/lie_pp_connection.pvs \
  --jobs 1 --heap-mib 6144 --timeout 180
```
