# Three-bin transport with a computed concentration certificate

The separate theory
[`tangent_bundle_finite_transport`](../applications/luces/tangent_bundle_finite_transport.pvs)
instantiates the existing `tangent_bundle[3]` interface. Existing theories are
unchanged. The construction exercises both a deterministic transport and an
actual split of one source atom, using couplings with the stated marginals.

The interpolation is affine mixing of mass vectors on a fixed grid. Neither
the function named `exp_map` by the inherited interface nor its `kantorovich`
field denotes a constructed Wasserstein exponential or McCann displacement
interpolation. The older interface does not force affine interpolation;
this model chooses it explicitly.

## What is computed

A distribution is a nonnegative mass vector on three indices. It need not
have total mass one. The two examples below are normalized. A coupling is a
nonnegative three-by-three matrix, and `feasible?` checks all three row sums
and all three column sums against the source and target.

For a coupling `pi`, define

```text
total(pi) = sum_i sum_j pi(i,j)
maxima(pi) = sum_i max_j pi(i,j)
fraction(pi) = 0                         if total(pi) = 0
               maxima(pi) / total(pi)    otherwise
```

The theory calls this quantity `concentration_fraction`. Its range `[0,1]`
comes from the actual row maxima and total mass. A maximum is attained at a
computed index; the greatest index wins ties, including entirely zero rows.

The `mongeMass` statistic in the separate Lean development is the unnormalized
sum of row maxima. With a matching plan representation, the values agree for
unit total mass; positive nonunit mass requires dividing that sum by the total
mass. This compares definitions without claiming a proved Lean/PVS
correspondence or identical argmax tie rules.

`unit_fraction_extracts_compatible_map` states that feasibility and fraction
one imply

```text
pushforward(source, row_argmax(pi)) = target.
```

The proof goes through row concentration: each row sum equals its maximum,
so all mass outside the chosen column is zero. This derives compatibility
from the matrix and marginal constraints. It does not assume compatibility
or infer compatibility for an arbitrary previously selected map.

The zero matrix has fraction zero. Thus zero rows can be harmless, while a
zero matrix cannot supply a fraction-one certificate.
For positive total mass, `positive_fraction_iff_concentrated` states the
equivalence: fraction one if and only if every row sum equals its row maximum.
The positive-mass hypothesis matters because zero rows are concentrated even
when the whole matrix is zero and its fraction is defined to be zero.

A fraction below one describes splitting in the selected coupling. It does
not exclude a different deterministic coupling with the same marginals.
The split example below proves that stronger impossibility separately.

## A model covering every balanced pair

`finite_coupler` supplies a feasible coupling whenever the two total masses
are equal. It uses the deterministic plan below for the designated pure pair.
For other balanced pairs of positive mass `M`, it uses

```text
pi(i,j) = source(i) * target(j) / M.
```

Balanced zero-mass vectors have the zero coupling. For unequal total masses
the total function also returns zero, and no marginal-feasibility claim is
made for that branch. `coupler_balanced_coverage` states the exact domain.
No optimality of the selected couplings is asserted.

The selected map is `(1,2,2)` for the pure pair and is otherwise constant at
the target's greatest maximizing index. These maps are nondecreasing on the
three indices. The constant default avoids treating an empty source row's
arbitrary argmax as an order constraint.

For a vector produced by `log_map`, `recover_map` reconstructs its encoded
finite map. The inherited `exp_map` is implemented as

```text
affine_mix(source, pushforward(source, recovered_map), t).
```

The reference `kantorovich` field is `affine_mix(source,target,t)`, and the
discrepancy is the sum of the three absolute coordinate differences. The
theorem `finite_model_admissible` addresses the complete inherited law package,
including its fraction-one branch. This is not a one-atom model or an
identically zero concentration function.

## Deterministic transport

```text
source = (1/2, 1/2, 0)
target = (0, 1/2, 1/2)
map    = (1, 2, 2)

coupling = [ 0   1/2   0   ]
           [ 0    0   1/2  ]
           [ 0    0    0   ]
```

The plan has the correct row and column sums, fraction one, and a
nondecreasing compatible map. `pure_transport_certificate` records these
conditions. `pure_zero_gap_all_times` gives gap zero for every `t` in `[0,1]`,
so the pure branch of the inherited contract is actually used.

## Splitting one atom

```text
source = (1, 0, 0)
target = (1/2, 1/2, 0)

coupling = [ 1/2   1/2   0 ]
           [  0     0    0 ]
           [  0     0    0 ]
```

This plan is also feasible, but its fraction is one half.
`split_no_deterministic_map` excludes every deterministic map, not merely the
model's chosen map: a map sends the entire source atom to one index.

The model chooses index one. Its two interpolations are therefore

```text
exp_map      = (1-t,   t,   0)
reference    = (1-t/2, t/2, 0)
L1 gap       = t.
```

`split_gap_at_every_time` states that identity. At the midpoint the gap is
one half, as recorded by `split_positive_midpoint_gap`. Both examples have
equal source and target total mass one; the positive gap does not arise
from comparing zero mass with unit mass.

## Scope

The results concern finite marginal feasibility, concentration, deterministic
representability and the explicitly chosen affine model. They do not prove
optimal transport cost, a Brenier existence or uniqueness theorem, a genuine
Wasserstein tangent bundle, a physical source detector, or agreement with
Python, C or binary64 execution.

Background: Victor M. Panaretos and Yoav Zemel, *An Invitation to Statistics in
Wasserstein Space*, Springer, 2020, Sections 1.5 and 2.3; Cédric Villani,
*Optimal Transport: Old and New*, Springer, 2009, Chapter 5. These references
provide context; the continuous theorems are not claims of this finite model.

## Verification

The [ordinary replay receipt](../reports/PVS_TANGENT_FINITE_TRANSPORT_20261029.json)
records a successful targeted check on 2026-10-29: 67 saved Project bodies
across three loaded modules, including all 49 new bodies (44 explicit claims
and five TCCs) and 18 unchanged bodies from the existing tangent interface and
its witness. This closure required no Native library bodies; the PVS prelude
remains part of the proof assistant's trusted setup. No whole-library replay
or new Lean port is claimed.

All 2,298 preexisting tracked working files remained byte-for-byte unchanged,
including the 2,259 existing formal source and proof files. The new development
adds this document, the new source/proof pair and its verification receipt.

With PVS configured as described in the repository README, replay the closure:

```sh
python3 scripts/check.py --file applications/luces/tangent_bundle_finite_transport.pvs \
  --jobs 1 --heap-mib 6144 --timeout 180
```
