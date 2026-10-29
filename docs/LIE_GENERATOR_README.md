# Lie-generator numerical screens

The current PVS models are
[lie_generator_structure.pvs](../applications/luces/lie_generator_structure.pvs)
and the legacy data checks in
[lie_captured_observations.pvs](../applications/luces/lie_captured_observations.pvs).
The computed path interface is
[lie_pp_connection.pvs](../applications/luces/lie_pp_connection.pvs), with
computed path geometry in
[pp_walk_geometry.pvs](../applications/luces/pp_walk_geometry.pvs) and
[pp_walk_coherence.pvs](../applications/luces/pp_walk_coherence.pvs).
They evaluate measured C20/C21/C22 observations and include explicit
counterexamples to the former universal coherence implications. They do not
prove a Lie exponential representation or infer physical observability from
coherence. See [LUCES model scope](LUCES_MODEL_SCOPE.md).

## Displacement observation

The producer `paper3/scripts/lie_group_transport_v2.py` in `master-controler`
forms a displacement field from a Kantorovich coupling:

```text
v(i) = sum_j P(i,j) * (j-i) / sum_j P(i,j)
```

Its comparisons of segment fields, the full field and active shape directions
are different observables. They are also distinct from the runner's C_GEN
signed-flow comparison and DEV's flattened `T-I` alignment.

| Screen | Actual numeric condition |
| --- | --- |
| C20 | Global mean alignment > 0.7; STRONG when > 0.85. |
| C21 | Pair mean alignment > 0.85 and speed ratio < 5. This is a screen, not an `exp(tX)` theorem. |
| C22 | Minimum active shape-direction cosine >= 0 passes; > 0.85 is STRONG in the producer. Negative values mark reversal. |

The strict boundaries matter: a global alignment of exactly 0.7 does not pass
C20. The formal predicates read the same numeric fields as these comparisons.

## Bound, recomputed observations

The versioned [fixture](../applications/luces/data/lie_observations.json) records
exact binary-float ratios and hashes for boot320, boot334 and boot347. The
[recheck script](../scripts/check_lie_observations.py) reruns the actual producer,
checks the CSV/source hashes and compares those values with the PVS literals.
From this repository, using Python with NumPy, pandas, SciPy and POT:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_lie_observations.py \
  --source-root ../master-controler
```

For these three rows, C20 is respectively STRONG, FAIL and PASS. Boot320 and
boot347 pass C22; boot334 reverses. All three fail C21. The C20 producer does
not measure C14 observability, so its formal observations explicitly retain
`unmeasured` evidence.

The fixture also records an additional curvature computed from the same seven
windows as C20. That curvature is not the differently binned DEV curvature.
The PVS inverse-order check applies only to the finite captured C20 table.
A separate bound DEV example has both higher curvature and higher operator
alignment, disproving any universal inverse law for that different metric.

## Mathematical counterexamples and limits

Two unit directions `(119,120)/169` and `(119,-120)/169` each align with `(1,0)`
by more than 0.7, while their mutual cosine is negative. Thus reversal alone
cannot force failure of the C20 global-alignment predicate. A second observation
has no reversal but insufficient global alignment. A coherent observation can
also lack measured observability evidence. The older proposed equivalence
`coherent IFF observed AND NOT reversal` is therefore not a current theorem.

Hall, *Lie Groups, Lie Algebras, and Representations* (2015), gives mathematical
background on one-parameter subgroups. It does not justify turning the numeric
C21 thresholds into that theorem; no such formal bridge is supplied here.

## Historical extended table

The following rounded table is retained from the earlier report. Only the
three rows named above have been rerun by the versioned binding in this
revision. The other entries and their historical labels are not a fresh
replay or a universal theorem. A rounded speed of 5.0 can still exceed the
strict C21 cutoff, as it does for boot320.

| Boot | Type | Cloud | cos_pair | cos_full | speed | Dir | C20 | C21 | C22 |
|---|---|---|---|---|---|---|---|---|---|
| Boot293 | dawn | CLOUDY | 0.514 | 0.746 | 17.1x | ROT | PASS | FAIL | PASS |
| Boot301 | dawn | CLEAR | 0.332 | 0.635 | 32.9x | ROT | FAIL | FAIL | FAIL |
| Boot305 | dawn | CLEAR | 0.409 | 0.552 | 54.3x | ROT | FAIL | FAIL | FAIL |
| Boot312 | dawn | CLOUDY | 0.168 | 0.525 | 5.0x | ROT | FAIL | FAIL | FAIL |
| Boot314 | dawn | MIXED 45% | -0.041 | 0.264 | 20.5x | ROT | FAIL | FAIL | FAIL |
| Boot320 | dawn | CLOUDY 97% | 0.940 | 0.918 | 5.0x | STABLE | STRONG | FAIL | STRONG |
| Boot330 | dawn | MIXED 62% | 0.493 | 0.705 | 10.0x | ROT | PASS | FAIL | PASS |
| Boot334 | dawn | CLOUDY 94% | 0.194 | 0.502 | 7.6x | ROT | FAIL | FAIL | FAIL |
| Boot347 | dawn | CLOUDY 100% | 0.456 | 0.711 | 6.3x | ROT | PASS | FAIL | STRONG |
| Boot349 | dawn | CLEAR 2% | 0.804 | 0.892 | 14.2x | STABLE | STRONG | FAIL | PASS |
| Boot303 | dusk | CLEAR | -0.098 | 0.193 | 19.6x | ROT | FAIL | FAIL | FAIL |
| Boot298 | dusk | CLOUDY | -0.117 | 0.188 | 17.0x | ROT | FAIL | FAIL | FAIL |
| Boot322 | dusk | CLOUDY | -0.153 | -0.066 | 64.2x | ROT | FAIL | FAIL | FAIL |

The table illustrates why C20 and C22 grades differ: boot347 has mean global
alignment about 0.711 but minimum active shape alignment about 0.903. Neither
a rounded table nor a matching finite classification establishes a universal
physical implication.

## Geometry computed from a PPG path

The coordinate map assigns ten real coordinates to each vertex. It is a fixed
input, shared by the original and extended graph. For consecutive samples,
the extractor computes the exact-real expression

```text
delta_i = x_(i+1) - x_i
r_i     = norm(delta_i)
u_i     = delta_i / r_i if r_i > epsilon, otherwise zero
kappa_i = acos(clip(dot(u_i, u_(i+1)), -1, 1)) / r_i
          if r_i > epsilon, otherwise zero
kappa   = mean of the n-2 interior terms
epsilon = 1 / 10^10
```

The raw function is total on short traces, but a curvature certificate requires
at least three samples and every successive step to exceed the cutoff. This
admission condition is stronger than merely checking the raw numerical score.
If the current step is active and the following step
is inactive, the formula uses `acos(0)/r_i`; it does not silently discard that
turn. The rational epsilon and exact-real operations define the mathematical
model. Equality with NumPy's binary64 result, including its rounded threshold,
requires a separate numerical refinement proof.

`BoundWalkReport` rules out independent reported curvature or endpoint
alignment: both must equal the calculations for its walk. `accept_report?` requires
the ordered walk to be a `pp_path` satisfying the chosen vertex invariant and
RR relation, the curvature bound and the alignment floor. A graph extension
preserves that same certified path. Replacing
its middle vertex can change the measured geometry.

The concrete example uses four normalized samples, shown in their first four
coordinates; the other six coordinates are zero:

| Sample | Coordinates |
| --- | --- |
| Start | `(1/2, 0, 1/2, 0)` |
| Straight middle | `(1/4, 1/4, 1/4, 1/4)` |
| Bent middle | `(0, 1/2, 1/2, 0)` |
| End | `(0, 1/2, 0, 1/2)` |

```text
Start ---- Straight middle ---- End     curvature = 0
   \
    +----- Bent middle ---------+       curvature > 0
```

Both paths satisfy the graph's normalization and forward-rank conditions.
The extension keeps the old path and adds the bent alternative. A separate
zero-curvature certificate accepts the old path and rejects the new one.
Thus preservation of old paths and admission of new paths are distinct checks.

The endpoint-direction comparison below is bound by the same construction.
C20 also needs the consecutive
coupling displacement fields and a full endpoint coupling. The historical
three-boot fixture stores rounded observations, not a formal extraction of
those couplings or an equality between its float curvature and this real
formula. It remains an attached observation, not a certified geometric trace.

The earlier [geometry replay](../reports/PVS_WALK_GEOMETRY_20261029.json) passed
the curvature-only revision with 90 Project and 757 required Native proof bodies.
The ordinary source, proof ownership and completion gates were unchanged.
Its source hashes describe that dated revision.

## Coherence computed from the same walk

Endpoint-direction coherence is the clipped cosine between the first and last
normalized steps. Its inputs are the same ordered vertices and fixed coordinate
map used by the curvature calculation. There is no freely supplied alignment
field in an accepted report. This definition does not identify endpoint
alignment with C20's average coupling-generator alignment.

For a three-sample active trace, the definitions give the exact relation

```text
mean_curvature = acos(endpoint_coherence) / first_step_norm
```

For two such traces with the same positive first step norm, greater endpoint
coherence is equivalent to strictly smaller curvature, since `acos` is
strictly decreasing on `[-1,1]`. Equal lengths for the second steps are not
required. This order equivalence is a mathematical corollary of the checked
identity, not a separately saved PVS theorem.

A longer trace can turn and later recover its initial direction. The concrete
counterexample uses five normalized samples, with the other six coordinates zero:

| Vertex | Coordinates |
| --- | --- |
| S | `(1/2, 0, 1/2, 0)` |
| A | `(1/4, 1/4, 1/2, 0)` |
| B | `(0, 1/2, 1/2, 0)` |
| C | `(1/4, 1/4, 0, 1/2)` |
| E | `(0, 1/2, 0, 1/2)` |

```text
S --> A --> B --> E     curvature = pi/sqrt(2),       endpoint cosine = 0
       \
        +-> C --> E     curvature = 3*pi/(2*sqrt(2)), endpoint cosine = 1
```

Both paths have four samples, the same endpoints, the same first step and arc
length `sqrt(2)`. Their increment multiset is the same: two copies of
`u = (-1/4,1/4,0,0)` and one `v = (0,0,-1/2,1/2)`. The order is `u,u,v` versus
`u,v,u`. Thus more mean curvature can coexist with more endpoint coherence,
even with these other quantities fixed. The common graph uses explicit edges
and the universal RR relation for a shared context, rather than an invented
ranking assumption. These are constructed mathematical witnesses, not boot-log
measurements or a derived physical transition relation.

This refutes universal inverse ordering; some longer traces can still obey
that ordering. Equal step lengths alone do not restore it: orthogonal
equal-length increments in the orders `u,u,v` and `u,v,u` give coherence
`0` versus `1` and curvature `pi/(4*h)` versus `pi/(2*h)`. This equal-step
variant is an exact calculation, not the replayed PVS example. See the
[precise conditions and longer-trace candidate](THEOREM_SCOPE.md#fixed-scale-three-sample-corollary).

The three captured C20 rows are three datasets, each replayed with seven
distributions, not three-sample traces. These endpoint-metric results do not
explain the captured C20 ordering or show that it is coincidental. The new
walk geometry and coherence modules currently have no Lean counterparts.

The [completed coherence replay](../reports/PVS_WALK_COHERENCE_20261029.json)
passed all three entry points, with 138 Project and 761 required original
Native proof bodies. The public source-ownership and completion gates were
unchanged. The three-row numerical fixture command also passed with unchanged
measurements and updated source routing.

## Author

Dragan Stosic, 2026
