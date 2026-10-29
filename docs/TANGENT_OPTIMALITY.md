# Optimality certificates for the three-bin tangent examples

[`tangent_bundle_optimality`](../applications/luces/tangent_bundle_optimality.pvs)
connects the existing three-bin transport model to the established ten-bin
Kantorovich certificate theory. It adds a separate source/proof pair and
leaves the existing models unchanged.

The bridge uses the existing `thm_primal_optimal` and
[`thm_certificate_gap_zero`](../applications/luces/kantorovich_duality.pvs).
It does not introduce a second proof of
weak duality. Optimality concerns the actual selected pure and split plans,
and arbitrary plans meeting the stated certificate conditions.

## Why padding needs a proof

The three-bin model accepts nonnegative mass vectors with arbitrary equal
total mass. The ten-bin feasible set requires both marginals to have total
mass one. The bridge therefore uses the explicit condition `mass(mu)=1` for
each small marginal. Both concrete examples satisfy it.

Masses and plans are extended by zero outside indices `0,1,2`:

```text
pad_mass(mu)(i) = mu(i)          if i < 3
                  0             otherwise

pad_plan(pi)(i,j) = pi(i,j)     if i < 3 and j < 3
                    0           otherwise
```

The bridge relates finite sums, row and column marginals, normalization and
objectives. The objective identity works for an arbitrary nonnegative cost on the ten-bin
grid: the padded plan's objective equals the nine-term objective on its
three-by-three block.

To transfer quadratic optimality back, every feasible three-bin competitor
with the same prescribed marginals is padded and compared using the ten-bin
optimum. Objective preservation then gives
the required comparison for every original competitor. This establishes
optimality, rather than merely observing that one plan satisfies a few
constraints. The transfer does not require identifying all arbitrary ten-bin
plans with three-bin plans.

## One certificate for forward-adjacent support

For integer bin indices, use the quadratic cost and common prices

```text
c(i,j) = (i-j)^2
psi(i) = i
phi(j) = j.
```

This is squared displacement of the bin indices. It is not identified with a
measured wavelength distance or an empirical C20 transport-cost matrix.

Their dual slack is

```text
c(i,j) - (phi(j)-psi(i)) = (j-i)*(j-i-1) >= 0.
```

The nonnegativity uses the integer grid: `j-i <= 0` or `j-i >= 1`. Equality
holds exactly when `j=i` or `j=i+1`. Consequently, any feasible normalized
plan supported on those pairs meets complementary slackness and the
existing optimality certificate. The support condition is sufficient;
the new theory does not characterize every optimal plan.

This particular linear-price certificate does not cover positive mass with
displacement two or a backward displacement, nor does it certify every
monotone plan. Such plans require another optimality argument. Both named
examples pass because their supports lie in the stated forward-adjacent
class. The general padding bridge is separate from this restricted certificate.

The quadratic cost and prices are defined on all ten bins. Dual feasibility
must hold on all 100 pairs, including places where a padded plan has no mass.
The same prices are not asserted to work for arbitrary real-valued locations.

## The two existing examples

The certified plans are the outputs of the existing `finite_coupler` on the
two existing pairs; new unrelated plans are not substituted.

| Example | Source | Target | Positive plan entries | Quadratic cost | Dual value |
| --- | --- | --- | --- | --- | --- |
| Pure | `(1/2,1/2,0)` | `(0,1/2,1/2)` | `pi(0,1)=pi(1,2)=1/2` | `1` | `1` |
| Split | `(1,0,0)` | `(1/2,1/2,0)` | `pi(0,0)=pi(0,1)=1/2` | `1/2` | `1/2` |

Both plans have zero primal-dual gap. The split plan still admits no
deterministic transport map: no map can send one atom of mass one to two
different targets with mass one half each. Optimality and deterministic
representability are separate properties.

## Two different gaps

The earlier tangent model uses affine mass interpolation and an L1
discrepancy. These definitions are unchanged:

| Example | Primal-dual gap | Existing affine L1 gap at time t |
| --- | --- | --- |
| Pure | `0` | `0` |
| Split | `0` | `t` |

At the midpoint the split example's affine L1 gap is one half despite zero
optimization gap. These are different quantities; the affine L1 gap is not
an optimality error. Certifying the endpoint coupling does not turn affine
mixing on the fixed grid into McCann displacement interpolation.

## The default coupler is not a general optimizer

For `source=target=(1/2,1/2,0)`, the existing default product coupling has
four entries of one quarter and quadratic cost one half. The diagonal plan
with entries `pi(0,0)=pi(1,1)=1/2` has the same marginals and cost zero.
The new counterexample excludes a universal optimality claim for
`finite_coupler`; its definition and the selected-map contract remain
unchanged.

Optimality is established for the two named input pairs. This does not assert
that these are the only input pairs on which the unchanged coupler is optimal.

The development supplies certificate transfer and certified examples. It
does not implement an optimal-transport solver or establish continuous
Brenier geometry, C20 extraction, numerical solver correctness, binary64
error bounds or agreement with Python/C execution. This module is maintained
in PVS; a Lean port is outside the current scope, as recorded in the
[repository and prover boundaries](THEOREM_SCOPE.md#repository-and-prover-boundaries).

Reference: Cédric Villani, *Optimal Transport: Old and New*, Springer, 2009,
Chapter 5. The continuous theory is background, not a claimed consequence
of these finite certificates.

## Verification

The [ordinary replay receipt](../reports/PVS_TANGENT_OPTIMALITY_20261029.json)
records a successful targeted check on 2026-10-29: 143 saved Project bodies
across six loaded modules, including all 38 new bodies (33 explicit claims
and five TCCs), plus 38 required original Native library bodies. All failure,
missing-script and incomplete counters were zero. This is a check of the new
entry point and its loaded dependencies, not a whole-library replay.

All 2,302 preexisting tracked working files remained byte-for-byte unchanged,
including 2,261 formal source and proof files. The new development consists
of a separate source/proof pair, this document and its verification receipt.

With the README's PVS and library setup, replay the entry point:

```sh
python3 scripts/check.py --file applications/luces/tangent_bundle_optimality.pvs \
  --jobs 1 --heap-mib 6144 --timeout 180
```

The checker's explicit `--file` selection includes the new source and its
companion `.prf` in the isolated snapshot without requiring Git staging.
