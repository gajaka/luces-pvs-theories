# Theorem scope and local repair

The source-result count is a declaration inventory. It includes structural
laws, definition accessors and helper lemmas alongside the main arguments.
The historical whole-library checks in the README are dated separately from
later changes to individual theories.

## Repository and prover boundaries

The public Lean-to-PVS correspondence concerns the dated `ppg-lean` inventory.
The later `pp_walk_*`, `unit_spherical_angle`,
`tangent_bundle_finite_transport` and `tangent_bundle_optimality` developments
are maintained in PVS; a Lean port is outside the current scope.

[`tangent_bundle_optimality`](TANGENT_OPTIMALITY.md) certifies every normalized
feasible plan supported on `j-i` equal to zero or one, and applies that result
to two named plans. That module does not establish optimum attainment for
arbitrary marginals or the correctness of a general transport solver; results
from the separate Lean development are not claimed as PVS results.

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

At commit `a5d33fc`, `lie_pp_connection` has a fixed coordinate-map parameter and a
`CurvatureBoundPrewalk` subtype equating reported and computed curvature. Its
certification result also recovers the actual vertex invariants. The earlier
unconstrained `MeasuredPrewalk` and its graph-independent field-projection
theorem are replaced by this interface. In that revision, legacy float fixtures remain
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

## Endpoint-direction coherence and the curvature relation

The subsequent `pp_walk_coherence` extension defines endpoint coherence from
the same ordered coordinates as curvature. It is the clipped dot product of
the first and last normalized steps, with an explicit short-trace branch.
`lie_pp_connection` now uses `WalkMeasurements` with computed curvature and
endpoint alignment. `BoundWalkReport` requires equality with both computations;
`accept_report?` checks that equality for an untrusted report and applies the
combined PPG, activity, curvature and alignment conditions.

For three active samples, `three_sample_curvature_identity` proves that mean
curvature equals the inverse cosine of endpoint coherence divided by the first
step norm. At a fixed positive first step norm, this gives strict inverse
ordering. The precise corollary and its assumptions are stated below. This
relation does not establish a universal inverse ordering across arbitrary
traces. A computed counterexample
uses two paths of four normalized samples, equal endpoints, equal arc length
and the same increment multiset. Their endpoint coherences are zero and one,
while the latter has strictly larger curvature. The comparison uses calculated
fields, not arbitrary attached values.

The seven historical C20 observation results now live in the nonparametric
`lie_captured_observations` theory. Its raw `TransportPath` has no unverified
walk field. Neither the endpoint definition nor its counterexample is a claim
about C20 coupling-generator alignment. Coordinate calibration, binary64
agreement and the remaining application and Lean/PVS coverage gaps are
separate obligations.

### Fixed-scale three-sample corollary

Let `p` and `q` each have exactly three samples and active steps under the same
fixed coordinate map. Suppose their first step norms are equal to a common
`h > step_cutoff`. Write `C` for endpoint coherence and `kappa` for measured
curvature. The checked identity gives

```text
kappa(p) = acos(C(p)) / h
kappa(q) = acos(C(q)) / h
C(p) < C(q)  iff  kappa(p) > kappa(q)
```

The last equivalence follows from strict decrease of `acos` on `[-1,1]` and
division by positive `h`. NASAlib states that analytic fact as
`trig@acos.acos_strict_decreasing`. The corollary is now saved as
`three_sample_strict_inverse` in
[`pp_walk_coherence_order`](../applications/luces/pp_walk_coherence_order.pvs).
Equal second step norms are not needed. Without the common first norm, the
denominators can change the ordering.

Three samples are a sufficient condition here, not a necessary condition for
every individual comparison. The four-sample counterexample refutes a
universal extension; it does not say every longer trace violates inverse
ordering.

### Equal step lengths do not suffice

There is also an equal-step variant of the counterexample. Take orthogonal
increments `u = (-1/4,1/4,0,0)` and `v = (0,0,-1/4,1/4)`, each of norm
`h = sqrt(1/8) > step_cutoff`. Start at `S = (1/2,0,1/2,0)`. The two paths are
`S, S+u, S+2u, S+2u+v` and `S, S+u, S+u+v, S+2u+v`. Every coordinate is
nonnegative and each vector sums to one; pad the other six coordinates with
zero.

| Increments | Consecutive turning angles | Endpoint coherence | Mean curvature |
| --- | --- | --- | --- |
| `u,u,v` | `0, pi/2` | `0` | `pi/(4*h)` |
| `u,v,u` | `pi/2, pi/2` | `1` | `pi/(2*h)` |

The sample count, endpoints, first step, increment multiset and arc length
`3*h` agree, and all steps have the same length. Both coherence and curvature
still increase. This variant is an exact calculation from the current
definitions, not a saved PVS example; the replayed example above is unchanged.

### A sufficient condition for longer traces

A stronger geometric restriction gives a positive theorem beyond three
samples. In `pp_walk_coherence_order`, `shortest_arc_trace?` requires `N >= 3`
samples and every actual step to have the same active norm
`h`, and the unit directions to have the form
`q_j = cos(theta_j)*e1 + sin(theta_j)*e2` for one orthonormal pair `e1,e2`.
Require nondecreasing `theta_j` and total turn
`0 <= theta_(N-2) - theta_0 <= pi`. Thus the directions progress along one
shortest great-circle arc without reversing.

`circle_dot` derives the cosine of the angular difference from the frame's
inner products. `circle_angle` uses the principal interval `[0,pi]` to recover
the actual angle. `shortest_arc_prefix` then proves by induction that the
consecutive contributions telescope. The endpoint angle is computed from the
same actual unit directions. `shortest_arc_curvature_identity` concludes

```text
kappa = acos(C) / ((N-2)*h)
```

`shortest_arc_strict_inverse` proves strict inverse ordering for two such
traces when both `N` and `h` are fixed. The two traces may have different
orthonormal frames and angle sequences. Equal step lengths alone do not
supply the telescoping condition. The hypotheses constrain actual vectors
and step lengths; they do not assume a curvature identity or an inverse law.

The concrete `nonzero_four_sample_example` supplies a normalized PPG path with
increments `u,u,v`, where `u = (-1/4,1/4,0,0)` and
`v = (0,0,-1/4,1/4)`. Starting at `(1/2,0,1/2,0)` gives four nonnegative
mass-one spectra, with the remaining six coordinates zero. All steps have norm
`h = sqrt(1/8)`, the direction angles are `0,0,pi/2`, and the calculated metrics
are `C = 0` and `kappa = pi/(4*h) > 0`. The path satisfies the displayed arc
hypotheses and the explicit graph's `pp_path` conditions. This is a
nonstraight witness, not a calibration or physical-RR result.

The equal-step countercalculation in the preceding section is still not a
saved PVS counterexample: the new example formalizes its `u,u,v` path, not the
comparison with the reversing `u,v,u` path. The earlier unequal-step
counterexample remains fully checked in `pp_walk_coherence`.

### Applicability to the captured runner inputs

The separate [recorded applicability analysis](../reports/LUCES_WALK_ARC_APPLICABILITY_20261029.json)
checks the same seven producer distributions for boot320, boot334 and boot347.
All three fail two necessary conditions: exact rational embeddings of their
saved binary64 point coordinates give unequal squared step norms and delta
rank six. The longest/shortest step ratios are about 5.97, 4.47 and 7.25.
Thus the sufficient class of `shortest_arc_curvature_identity` is not
instantiated by any of those three represented traces.

Numerical uncentered unit-direction SVD diagnostics agree that the configured
plane criterion fails. The angular stage is consequently `NOT_APPLICABLE`;
projecting a nonplanar trace and checking its projected angles would not check
the actual PVS hypothesis. The script retains exact finite-data witnesses,
source and CSV hashes, extraction details, configured tolerances and separate
floating-point diagnostics. See [reproduction and interpretation](LIE_GENERATOR_README.md#applicability-to-the-captured-seven-sample-walks).

This is a finite represented-data investigation, not a PVS theorem or a
Python/binary64 refinement proof. Existing formal sources and saved proofs
were unchanged; their previous replay remains applicable. The result does
not classify other runner datasets or identify endpoint coherence with C20.

### Captured C20 data and Lean coverage

The three captured C20 rows are three datasets, not three-point walks. The
curvature replay in `scripts/check_lie_observations.py` uses seven distributions
per dataset: night, five transition bins and day. The endpoint-coherence
identity therefore neither explains their C20 ordering nor identifies it as
coincidence. C20 is a different metric, and the cause of the captured ordering
remains unestablished.

At Lean main `0d702bb`, `ppg-lean` has no project counterparts of
`pp_walk_geometry`, `pp_walk_coherence`, `pp_walk_coherence_order`,
`unit_spherical_angle`, `pp_walk_curvature_bound` or
`pp_walk_certificate_coherence`. Its rational LUCES snapshot and
certificate-repair modules do not define these geometric metrics. The geometry
extension is a PVS
development, outside the historical Lean-to-PVS correspondence inventory.

The completed [order-theorem replay](../reports/PVS_WALK_COHERENCE_ORDER_20261029.json)
selected the new entry point and checked all seven loaded Project modules:
**149 saved Project bodies and 911 required original Native bodies** passed
the unchanged ordinary checker. The new pair contributes 26 explicit claims
and seven TCCs. All incomplete, missing-script, derived, copied and Native
failure counters were zero. `trig@trig_inverses` supplies the additional
`acos_cos` dependency, whose required original proof chain was replayed too.
All 2,251 pre-existing tracked formal working files remained byte-identical;
the earlier geometry, coherence and C20 fixtures were not modified.

The earlier completed [coherence replay](../reports/PVS_WALK_COHERENCE_20261029.json)
checks the new coherence kernel and example, the computed-report interface and
the separated legacy theory. All **138 Project bodies and 761 required
original Native bodies** passed the unchanged ordinary public checker across
eight Project modules. There were no unfinished obligations, missing scripts,
copied or derived credits, Native failures or debugger entries. The original
geometry source/proof pair remained byte-identical to commit `a5d33fc`.

The current entry points can be replayed separately with the README's library
setup:

```sh
python3 scripts/check.py --file applications/luces/pp_walk_coherence.pvs \
  --jobs 1 --heap-mib 6144 --timeout 180

python3 scripts/check.py --file applications/luces/lie_pp_connection.pvs \
  --jobs 1 --heap-mib 6144 --timeout 180

python3 scripts/check.py --file applications/luces/lie_captured_observations.pvs \
  --jobs 1 --heap-mib 6144 --timeout 180

python3 scripts/check.py --file applications/luces/pp_walk_coherence_order.pvs \
  --jobs 1 --heap-mib 6144 --timeout 180
```

## Universal curvature lower bound for active walks

[`pp_walk_curvature_bound`](../applications/luces/pp_walk_curvature_bound.pvs)
proves a one-sided relation for every walk with `N >= 3` samples and active
steps in the existing ten-coordinate model. Let `m = N-2` and let `l_i` be
the norm of step `i`, starting at zero. Define

```text
Lmax = max(l_0, ..., l_(N-3))
kappa >= acos(C) / ((N-2) * Lmax)
```

Here `C` is the computed endpoint-direction coherence and `kappa` is the
existing measured mean curvature. The last observed step, at index `N-2`,
is excluded from `Lmax`: it supplies the final direction but is not a local
curvature denominator. All observed steps must exceed `step_cutoff`; this
also makes every normalized direction a unit vector and ensures `Lmax > 0`.
There is no equal-length, planar, monotone-turning or graph/RR hypothesis.

[`unit_spherical_angle`](../applications/luces/unit_spherical_angle.pvs)
derives the needed unit-sphere triangle inequality. For unit vectors `u,v,w`,
the residuals `u-(u dot v)*v` and `w-(w dot v)*v` have norms equal to the sines
of the adjacent angles. Cauchy--Schwarz bounds their inner product, giving
`cos(angle(u,v)+angle(v,w)) <= u dot w`. Cosine monotonicity gives the angle
inequality when the sum is at most `pi`; the principal angle's upper bound
handles the other case. The vector operations are explicitly instantiated at
dimension ten. The triangle inequality is proved, not supplied as a premise.

`endpoint_angle_le_turn_sum` applies it by induction along the actual unit
directions. `weighted_prefix_lower_bound` compares each nonnegative local
angle divided by `Lmax` with the same angle divided by its own step norm.
With `theta_i` denoting those local angles, the resulting chain is

```text
acos(C) <= sum(theta_i) <= Lmax * sum(theta_i/l_i) = (N-2)*Lmax*kappa
```

`universal_curvature_lower_bound` uses the computed finite maximum.
`universal_curvature_bound_with_upper` also permits any positive supplied
upper bound on the same denominator steps. Neither result assumes the
desired curvature inequality. Different walks can still have different
sample counts and length scales; no inverse ordering between arbitrary
walks follows.

The saved `tight_unequal_step_example` reuses the original normalized
`u,u,v` PPG path. Its first two step norms are `h = sqrt(1/8)`, while its final
step has norm `2*h`. It has `C=0` and
`kappa = pi/(4*h) = pi/sqrt(2)`, exactly the computed lower bound. Thus the
bound can be tight for unequal steps and the maximum excludes the last step
as specified. The earlier returning-direction examples retain positive
curvature with endpoint coherence one.

The separate [numerical check](../reports/LUCES_CURVATURE_BOUND_CHECK_20261029.json)
recomputes the saved seven-point traces, verifies their source/data bindings
and compares both curvature and endpoint coherence with the existing trace
report before evaluating the bound. It records lower bounds about 1.583846,
1.646142 and 6.220662 for boot320, boot334 and boot347, below the corresponding
curvatures 6.858686, 34.855611 and 19.061509. These are binary64 calculations,
not outward-rounded bounds for the exact transcendental expressions or a
Python/PVS refinement proof. The PVS theorem concerns exact real arithmetic;
C20 coupling coherence, calibration and physical RR remain separate.

The [completed bound-theorem replay](../reports/PVS_WALK_CURVATURE_BOUND_20261029.json)
selected `pp_walk_curvature_bound.pvs` and checked its eight loaded Project
modules: **152 saved Project bodies and 925 required original Native bodies**
all passed. The new kernel and bound comprise 27 explicit claims and nine
TCCs. All missing, incomplete, copied, derived and Native-failure counters
were zero, with unchanged public ownership, oracle and completion gates.
Actual input and runtime source/proof hashes matched the canonical files.
All 2,253 prior formal working files were preserved byte-for-byte. The
numerical tool's nine semantic tests and actual three-trace command passed
separately; those calculations are not PVS proof credit.

With the README's pinned library setup, the new loaded closure can be replayed:

```sh
python3 scripts/check.py --file applications/luces/pp_walk_curvature_bound.pvs \
  --jobs 1 --heap-mib 6144 --timeout 180
```

## Coherence derived from a curvature certificate

[`pp_walk_certificate_coherence`](../applications/luces/pp_walk_certificate_coherence.pvs)
uses an existing `geometry_certificate?`, including its actual path, sample
count, active steps and curvature upper bound `B`. Write

```text
S = (N-2)*curvature_lmax > 0
A = S*B
```

`certified_angle_budget` combines `kappa <= B` with the universal lower bound
to prove `acos(C) <= A`. `certified_coherence_small_budget` gives
`C >= cos(A)` when `A <= pi`. The total function `safe_coherence_floor` clips
the angle budget at `pi`, and `certified_coherence_global` proves

```text
C >= cos(min(pi,A))
```

for every valid geometry certificate. For `A >= pi` this yields only the range
bound `C >= -1`; using the uncut cosine outside the principal interval is
invalid. The function alone certifies nothing: a short or inactive raw walk
can have a zero budget by definition but cannot pass the geometry certificate.

The combined certificate requires the strict test `C > coherence_floor`.
`combined_from_safe_floor` discharges this obligation when
`coherence_floor < safe_coherence_floor`. Under this sufficient
guard, `combined_equiv_geometry_under_safe_floor` proves that combined
certification is equivalent to geometry certification. Failure of the guard
does not establish failure of coherence: the actual `C` may exceed the
coarse guarantee. No unconditional redundancy or necessity criterion is claimed.

For `f` in `[-1,1]`, `combined_from_strict_budget_threshold` states the useful
direct criterion

```text
geometry_certificate? AND B < acos(f)/S  IMPLIES  combined_certificate?(..., B, f)
```

This strict threshold automatically puts the angle budget below `pi`.
`certificate_budget_window` also gives `A <= pi IFF B <= pi/S` under the
geometry certificate. Equality at the coherence threshold yields only a
non-strict lower bound and cannot generally imply the strict combined test.

The saved interior example has a valid geometry certificate, `A=pi/2` and
`C=0`. Its combined certificate holds exactly when `coherence_floor < 0`;
choosing zero fails despite equality with the derived lower bound. A straight
prefix gives the second boundary case: `B=0`, `A=0`, `C=1`, and the strict
floor-one certificate still fails. Both examples are actual PPG paths from
the existing normalized construction.

These corollaries discharge a threshold on the computed endpoint coherence.
Equality of an untrusted reported field with that computed value remains a
separate obligation in `report_matches_walk?`. The existing report interface
and acceptance checks were not changed. Python/C execution, binary64 error
bounds, calibration and C20 coupling alignment are outside the corollary.

The [numerical budget illustration](../reports/LUCES_CERTIFICATE_COHERENCE_BUDGET_20261029.json)
uses recorded floating-point curvature as a hypothetical tight upper bound,
not as an exact-real geometry certificate. It gives safe cosine floors about
`-0.878126`, `-1` and `-1` for boot320, boot334 and boot347. None of these
budgets guarantees endpoint coherence above `0.7` or `0.85`, even though the
recorded boot320 coherence exceeds `0.7`. The report also separates the
angular-detour and denominator-weight factors in the earlier lower-bound gap.

The [ordinary corollary replay](../reports/PVS_CERTIFICATE_COHERENCE_20261029.json)
passed 168 saved Project bodies and 925 required original Native bodies across
ten loaded modules. This includes all 13 explicit new claims and three new
TCCs; no existing formal statement or proof file was changed. The checker,
ownership and completion gates were unchanged, and all failure and missing-script
counters were zero. This checks only the new module and its loaded closure.

With the README's pinned library setup, replay that closure with:

```sh
python3 scripts/check.py --file applications/luces/pp_walk_certificate_coherence.pvs \
  --jobs 1 --heap-mib 6144 --timeout 180
```

## Repair hazards and observable subalgebras

The theories under [`theories/repair/`](../theories/repair/) add structural
read/write hazards, semantic invalidation, checked state changes and rational
observable subalgebras. Their reference is the public Lean repair development
at revision `60151677e58704ce856c05a572904d681fd959f6`. The detailed
[contract and correspondence note](REPAIR_HAZARDS_OBSERVABLES.md) distinguishes
the PVS specializations from the broader Lean interfaces.

The action subtype requires both the write frame and read locality. Under
predicate locality, footprint-disjoint changes preserve certificate truth.
Scoped commits check the target and every potentially affected previously true
core obligation. Semantic scope instead contains certificates with an actual
invalidation witness in the specified allowed domain. Its finite classifier
needs `CompleteDomain` to conclude domain-wide absence of invalidation. The PVS
`HazardResult` is an ordinary record with separately proved contracts; it is
not Lean's proof-carrying result datatype.

The observation layer constructs rational function subalgebras, observational
equivalence classes and well-defined updates of their quotient. Stable
subalgebras stay closed under admitted repair pullbacks; their values may
change. Fixedness leaves the values unchanged. Equal retained observations
remain equal after a common admitted operation sequence, and decision tests
must separately factor through those observations. The least stable hull is
defined by intersection and characterized by finite future observations; its
existence does not imply a computable small summary.

Zero/one certificate indicators connect this algebra to semantic hazards.
Fixedness of an algebra containing the protected indicators prevents their
invalidation. Stability alone supplies equal decisions for observationally
equivalent initial states under a common future sequence, rather than constant
certificate truth throughout an execution.

For finite rational kernels, closure of the full projection algebra is
equivalent to equal aggregate transition masses on summary fibers, with
surjectivity for the constructed reduced model. The good-state predicate has
an independent factorization obligation. Together these conditions establish
the existing finite-lumping interface and transfer its stochasticity and
survival results under their stated premises. The examples distinguish this
full closure from checking expectation on algebra generators alone.

This PVS development specializes rational scalars and same-state endomorphism
pullbacks. Lean's scalar-polymorphic algebra and cross-state pullback interface
are more general. The 34 source results in `ObservableSchemes` remain Lean-only;
no PVS affine-scheme or structure-sheaf foundation is claimed. The historical
1,824-result translation ledger above is unchanged by this extension.

The [normal targeted replay completed on 2026-10-30](../reports/PVS_REPAIR_OBSERVABLES_20261030.json)
passed 450 Project bodies across 34 loaded modules for 11 repair source files.
The new theories contain 223 explicit claims and 19 TCCs, totaling 242 new
bodies; 208 bodies are unchanged Project dependencies. The source comparison
accounts for 144 specialized Lean counterparts and 79 additional PVS supporting
claims. No Native proof bodies were required. All unfinished, missing-script
and derived-only counters were zero, with proof oracles disabled and no new
source `AXIOM` declarations. This is the new repair closure, rather than a
whole-library proof replay or a replacement of the historical source inventory.

Replay the repair group with the repository's pinned library setup:

```sh
python3 scripts/check.py --group repair --jobs 1 --heap-mib 6144 --timeout 60
```
