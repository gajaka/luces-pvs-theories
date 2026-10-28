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
