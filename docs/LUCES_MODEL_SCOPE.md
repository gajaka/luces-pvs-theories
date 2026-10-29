# LUCES models and measured certificate inputs

The LUCES theories distinguish mathematical models, computed observations and
physical claims. The current sources contain no hand-written `AXIOM`
declarations. This revision replaces the earlier axiomatic claims with explicit
finite constructions, consequences of stated model laws and counterexamples
where the old implication was too strong. It does not prove every claim made in
the older case-study reports.

## Transport and geometry

| Theories | Established scope |
| --- | --- |
| `monge_kantorovich_equivalence` | Ten-bin normalized marginals, actual row/column constraints, compatible maps and induced couplings. Optimization ranges over feasible plans. A nonzero uniform diagonal plan witnesses the conditions; the zero plan is rejected. The support-size result is a bound, not a proof of extremality. |
| `kantorovich_duality`, `cyclical_monotonicity` | Finite-sum weak duality and zero gap from checked prices, marginal feasibility and support complementary slackness. The cycle consequences cover two and three cycles; the quadratic two-cycle inequality rules out crossed support pairs. No general dual-optimum existence or all-cycle converse is asserted. |
| `brenier_uniqueness` | A finite one-dimensional quadratic argmin comparison implies monotonicity. This is not the continuous Brenier existence or uniqueness theorem. |
| `transport_structure`, `transport_structure_v2` | Explicit normalized identity/reversal couplings and costs give optimal sparse witnesses. A dense, 100-entry optimum for zero cost disproves universal optimal-implies-sparse and near-Monge claims. A sparse optimum may also exist for that cost. |
| `transport_stability` | Exact rank correlations for permutations of twenty distinct ranks. The correlation of identity with one adjacent swap is `664/665`; identity with reversal has correlation `-1`. There is no tie-corrected Spearman implementation or physical learnability theorem. |
| `stability_of_maps` | An implemented finite argmin is unchanged when a checked objective gap exceeds twice a uniform objective perturbation bound. Deriving that bound from measured distribution changes remains separate. |
| `wasserstein_metric`, `displacement_interpolation`, `entropy_along_geodesic` | Consequences of explicit metric, constant-speed interpolation and convex-energy laws. A real-line construction proves the laws for distance `abs(x-y)`, affine interpolation and squared energy. This does not construct Wasserstein measures or identify the energy with Shannon entropy. |
| `global_optimality` | Additive costs for two segments of the same oriented path give a weighted excess identity. Zero full gap excludes positive segment extras. A constructed example has 23% local excess and 4.6% global excess. These are path-length costs, not an identification with a squared Kantorovich objective. |
| `tangent_bundle` | A finite pushforward defines map representability. Endpoint and discrepancy laws are explicit model conditions, with consistency and nonrepresentability witnesses. No Wasserstein tangent bundle or general differentiability theorem is constructed. |

The Shannon functional in `displacement_concavity` is actually
`-sum p log p`, with `0 log 0 = 0`. A two-channel midpoint has positive Shannon
excess even when every source observation has zero lamp contribution. This
refutes the former universal pure-path entropy bound and the proposed inference
from positive excess to a hybrid source. The displacement-convex entropy energy
in the cited optimal-transport literature has the opposite sign and additional
geometric hypotheses.

## Charts and observability

| Theories | Established scope |
| --- | --- |
| `fisher_atlas` | An explicit chart/metric law package and a four-candidate nearest-centroid selector with deterministic tie handling. A five-state model satisfies every law and includes a four-way tie. No Fisher-Rao metric, smooth atlas or topology equivalence is constructed. |
| `fisher_boundary` | A positive diagonal quadratic form with unequal weights can move a two-center boundary. Both the general comparison and a concrete weighted example are supplied. No estimated sensor Fisher matrix is identified with those weights. |
| `fisher_voronoi` | Cell separation and boundary equations under the atlas laws. Four real centers at `0,2,4,6` show why the outer cells need not share a boundary; a segment can cross the three adjacent boundaries at `1,3,5`. |
| `observability_geometry`, `observability_refinement` | Controlled-response data and a positive cutoff define sensitivity and an attained finite margin. Opposing channel preferences give a nonzero minor. A proportional response table shows why one large response ratio does not establish rank. The witnesses are synthetic, not reconstructed boot experiments. |
| `hybrid_observability` | Arithmetic comparisons of entered conditioning values and a counterexample to a universal intermediate-conditioning claim. The entered values alone do not verify their measurement provenance. |
| `dual_observability` | Versioned `overlap-v1` numerical checks use elevation, lux, spectral mass and geometry as separate observations. An elevation interval alone cannot imply positive lux or bounded geometry. All 27 boot320 and 48 boot347 overlap rows are included in the numerical binding. |

The runner's restored `proxy-v1` OBS/MRG diagnostics use ordinary signal
variation and a noise proxy. They are not controlled-excitation measurements and
do not instantiate the sensitivity experiment model by themselves. The
historical OBS/DATL/MRG implementation was unavailable; these new versioned
metrics do not recover its definitions or validate its old classifications.

## Generator screens and deviation scores

`lie_generator_structure` uses measured numeric fields for C20 global
alignment, C21 pair alignment/speed and C22 minimum active shape alignment.
The boolean screens use those same fields and the thresholds in
`paper3/scripts/lie_group_transport_v2.py`. Passing a C21 screen is not a proof
of a representation `exp(tX)`. A realizable rational direction example shows
that a reversal can coexist with C20 coherence; another example separates
absence of reversal from sufficient global alignment. Coherence supplies no
missing observability evidence.

`pp_walk_geometry` computes angular curvature from the ordered vertices of a
prewalk and a fixed ten-coordinate observation map. It normalizes successive
differences, clips their dot product to `[-1,1]`, applies `acos`, divides by the
current step length and averages the interior terms. The small-step branches
are explicit. This is an exact-real formula, not a squared-difference proxy or
a proof of NumPy's floating-point evaluation.

`pp_walk_coherence` computes endpoint-direction coherence from the same walk
and coordinate map: the clipped dot product of its first and last normalized
steps. This is a different observable from C20 coupling alignment. For three
active samples, the curvature equals `acos(endpoint_coherence)/first_step_norm`.
At a common positive first step norm this implies strict inverse ordering.
That corollary does not require equal second step norms. It is a mathematical
consequence of the checked identity, saved as `three_sample_strict_inverse`
in `pp_walk_coherence_order`.

`lie_pp_connection` accepts a report only when both its curvature and endpoint
alignment equal those computations. `BoundWalkReport` encodes this equality;
`accept_report?` additionally checks `pp_path`, at least three samples, active
steps, the curvature bound and the endpoint-alignment floor. A raw zero from
inactive steps is insufficient. The coordinate map remains a fixed theory
input; its relation to sensor calibration is still an external obligation.

Graph extension preserves an already certified path with the same ordered
vertices and coordinate map. It does not certify every newly available path.
A construction with four normalized vertices supplies two paths of three
samples each, one straight and one with a right angle. Both respect the graph's
vertex and RR conditions,
but only the straight path satisfies a zero-curvature certificate.

The computed coherence does not obey a universal inverse ordering with mean
curvature. Two normalized paths with four samples, equal endpoints, equal arc
length and the same increment multiset give curvature `pi/sqrt(2)` with endpoint
alignment zero versus curvature `3*pi/(2*sqrt(2))` with alignment one. The order
of the interior directions matters.
This does not exclude inverse ordering for particular longer traces. Even
equal step lengths are insufficient for a universal law; the
[scope discussion](THEOREM_SCOPE.md#equal-step-lengths-do-not-suffice) gives an
exact equal-step countercalculation. The separate `pp_walk_coherence_order`
module proves a sufficient condition for longer traces: equal active step
lengths and actual unit directions moving monotonically along one shortest
great-circle arc of total angle at most `pi`. It derives
`kappa = acos(C)/((N-2)*h)` and strict inverse ordering at fixed `N,h`.
A normalized four-sample PPG path with nonzero curvature satisfies these
hypotheses. The formalized example covers the `u,u,v` path; the comparison
against `u,v,u` in the equal-step countercalculation is not yet a PVS result.
The [order-theorem replay](../reports/PVS_WALK_COHERENCE_ORDER_20261029.json)
passed 149 Project and 911 required original Native proof bodies across the
new entry point's dependency closure. All pre-existing formal files are
unchanged; this does not broaden the physical or floating-point scope.

`lie_captured_observations` retains the older C20 values as raw `TransportPath`
observations, with no unverified walk field. They depend on edge and endpoint
transport couplings. The inverse-order test over three captured rows remains
finite evidence; the computed endpoint counterexample does not establish a
claim about C20. A separate boot320/347 operator-alignment example shows why
those metrics also cannot be substituted for one another.
Each of the three captured rows is a dataset replayed with seven distributions.
The three-sample endpoint identity does not explain that C20 ordering or
establish coincidence. The new PVS walk-geometry and coherence modules have no
Lean counterparts at Lean main `0d702bb`.

The [current coherence receipt](../reports/PVS_WALK_COHERENCE_20261029.json)
records a completed ordinary replay of all three affected entry points and
their dependencies: 138 Project and 761 required original Native proof bodies,
with no unfinished obligations. All three raw C20 fixture rows also passed the
numerical recheck after their source was relocated.

The earlier [geometry replay receipt](../reports/PVS_WALK_GEOMETRY_20261029.json)
binds the curvature-only revision's sources and scripts. Its entry points passed the
ordinary checker with 90 Project and 757 required original Native bodies;
these counts include supporting lemmas and TCCs.

Keep these quantities distinct:

- **C20:** coupling-displacement alignment, pass threshold `0.7`.
- **C_GEN:** signed spectral-flow alignment used by the runner and local repair
  family, with its own threshold `0`.
- **DEV `op_align` / `op_neg`:** comparisons of flattened `T-I`
  operators and the presence of a negative alignment.
- **DEV `norm_residual`:** a residual between already normalized
  distributions, not physical source or sink strength.

`luces_runner_deviation` preserves the operational weights `(0.01,1,2,5)` and
cutoffs `1,3`. Measured feature enclosures and explicit float-score error bounds
imply `UNBALANCED` for boot320 (`3.9144200653044043`) and boot347
(`4.220548513515491`). `unbalanced_regime` is a separate calibrated numerical
model; its generic calibration hypotheses are not silently imposed on the
operational runner. Three-window velocity examples in `velocity_asymmetry`
establish orderings of the stated profiles, not physical time irreversibility.

## Finite certificate repair and data provenance

[`luces_local_certificate_repair.pvs`](../applications/luces/luces_local_certificate_repair.pvs)
evaluates atoms and conjunctions from the actual shared local-plan contract.
Its read sets come from that syntax. The family has eight positions, including
a repeated Monge predicate. The
[`indexed dependency bridge`](../theories/certification/ppg_indexed_certification_dependency.pvs)
retains those positions, their footprints and plan entries. It also proves the
image relation to the older predicate-valued blocking set; it does not identify
graphs that have different duplicate semantics.

The measured bank contains five mixtures of independent and optimal couplings
for the first populated boot320 elevation-bin pair. The 3/4 mixture passes
Monge but fails the full family. Search accepts only a candidate satisfying all
checks and the write frame, which protects GEN and dataset identity. In this
bank it selects the optimal coupling. This proves acceptance and preservation
for the represented snapshots; it neither synthesizes a repair for every bank
nor changes firmware.

The [`data README`](../applications/luces/data/README.md) gives commands for
recomputing CSV features, checking exact float ratios and source hashes, and
comparing the generated PVS literal blocks. The companion Lean development
additionally checks its included JSON through a pure parser in the kernel.
Neither boundary verifies the optimal-transport solver, arbitrary Python
execution, sensor physics or a physical intervention.

## Reading proof results

Use the public checker to replay the selected source and its dependency
closure. A successful typecheck is not a replay; a law package is not an
implementation; a finite data recheck is not a universal numerical theorem.
Counts include supporting lemmas and TCCs, and different runs can share
dependencies. The historical whole-library record in the repository README is
dated separately from these later revisions. See also the
[NASAlib metadata compatibility bundle](../library-proof-fixes/README.md) and
[theorem-scope record](THEOREM_SCOPE.md).

The scoped checks completed on 2026-10-28 and 2026-10-29 include:

| Selected entry points | Project bodies | Required Native bodies |
| --- | ---: | ---: |
| Fourteen remaining transport, geometry and observability source files | 156 | 40 |
| Lie-generator and measured-path connection | 43 | 0 |
| Finite cyclical-monotonicity closure | 44 | 38 |
| Finite transport-structure closure | 44 | 34 |
| Exact rank-stability example | 19 | 13 |
| Indexed certification-dependency bridge | 139 | 3 |
| Measured finite certificate repair | 163 | 3 |
| Measured DEV bridge | 27 | 0 |
| Logarithmic Shannon counterexample (`displacement_concavity`), 2026-10-29 | 17 | 761 |

Each listed public replay completed with zero unfinished bodies. Counts
overlap and are not totals of distinct theorems. The Shannon row is a completed
normal public replay of the current source and saved scripts. Together with
the eight reused source-matched normal passes, it closes all 27 semantic
source changes; the three separate proof-only repairs also have a completed
normal dependency closure. The
[incremental verification receipt](../reports/PVS_INCREMENTAL_REPLAY_20261029.json)
records the source hashes and scope guards. No new whole-library proof pass
is claimed.

References motivating the models include C. Villani, *Optimal Transport: Old
and New* (2009); V. M. Panaretos and Y. Zemel, *An Invitation to Statistics in
Wasserstein Space* (2020); S. Amari and H. Nagaoka, *Methods of Information
Geometry* (2000); B. C. Hall, *Lie Groups, Lie Algebras, and Representations*
(2015); and R. J. McCann, “A Convexity Principle for Interacting Gases” (1997).
These references do not substitute for the explicit assumptions in each
formal theory.
