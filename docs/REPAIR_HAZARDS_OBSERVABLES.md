# Repair hazards and observable subalgebras

The repair theories distinguish an operation that may invalidate a certificate
from a footprint overlap that merely requires rechecking. The observation layer
tracks the information needed to evaluate certificates after later operations.

The reference development is the public Lean [repair directory](https://github.com/gajaka/ppg-lean/tree/60151677e58704ce856c05a572904d681fd959f6/PPGraph/Repair).
The PVS counterpart uses rational-valued observables and finite rational kernels.
The Lean deterministic algebra is polymorphic over a commutative semiring; the
rational PVS instance does not claim that additional scalar generality.

## Theory organization

| Theories | Purpose |
| --- | --- |
| [`ppg_repair_hazards`, `ppg_repair_footprint_tightness`](../theories/repair/ppg_repair_hazards.pvs) | Proved action frames and read locality, RAW/WAR/WAW tests, commutation, footprint scopes and checked commits; tightness over local Boolean interpretations. |
| [`ppg_repair_semantic_hazards`, `ppg_repair_semantic_footprints`](../theories/repair/ppg_repair_semantic_hazards.pvs) | Invalidation witnesses, exact domain-relative scope, complete finite classification and comparison with footprint scope. |
| [`ppg_repair_hazard_examples`](../theories/repair/ppg_repair_hazard_examples.pvs) | Independent writes, detected conflicts, accepted scoped repair and rejection of protected-certificate damage. |
| [`ppg_repair_semantic_hazard_examples`](../theories/repair/ppg_repair_semantic_hazard_examples.pvs) | Structural alarms refined by semantic preservation, cancellation and exact finite classification, including an incomplete sample that misses a hazard. |
| [`ppg_repair_observable_algebra`](../theories/repair/ppg_repair_observable_algebra.pvs) | Rational function subalgebras, `Stable`, `Fixed`, observational equivalence, adjoin and the least stable hull. |
| [`ppg_repair_observable_projection`](../theories/repair/ppg_repair_observable_projection.pvs), [`ppg_repair_observable_quotient`](../theories/repair/ppg_repair_observable_quotient.pvs) | Full algebras of summary functions and well-defined updates of complete observational equivalence classes. |
| [`ppg_repair_observable_kernel`](../theories/repair/ppg_repair_observable_kernel.pvs) | Finite rational expectation, fiber-local transition laws and exact lumping compatibility. |
| [`ppg_repair_observable_footprints`](../theories/repair/ppg_repair_observable_footprints.pvs) | Local observation algebras, fixedness from disjoint writes and stability from backward read envelopes. |
| [`ppg_repair_observable_certificates`](../theories/repair/ppg_repair_observable_certificates.pvs) | Boolean certificate indicators, fixedness preventing invalidation and decisions after common operation sequences. |
| [`ppg_repair_observable_examples`](../theories/repair/ppg_repair_observable_examples.pvs) | Stable-but-not-fixed observation, a nonstable summary, and failure of stochastic generator-only checking. |

## Contracts

An action has an actual write frame and read-locality condition. RAW, WAR and
WAW are relations between declared footprints. They support commutation and
recheck-scope results only together with the stated semantic conditions.
The action subtype requires those conditions. Certificate locality is a
separate premise about the predicates being protected.

The full repair contract requires the target predicates to hold after the
change and every previously true protected predicate to remain true. Scoped
checking uses all affected core predicates, including those that were already
passing. A rejected checked change returns the original state. These statements
describe atomic model-state operations; they do not model concurrent hardware
instruction interleavings.

For a fixed predicate family, operation and allowed-state domain, semantic
invalidation means that a certificate holds before the operation and fails
afterward. Exact scope uses this actual invalidation predicate. A finite search
is complete for the allowed domain only when its enumeration covers that domain.
A sample without coverage cannot certify the absence of a hazard.
`HazardResult` is a PVS record carrying a flag and a counterexample list.
Theorems establish its witness and preservation contracts under domain coverage.
The Lean result datatype carries proofs in its constructors; the two interfaces
therefore encode their guarantees differently.

A rational observable algebra contains every constant function and is closed
under pointwise addition and multiplication. Stability means closure under the
pullbacks of all admitted operations. Fixedness requires equality of observable
values for a particular operation. Equal retained observations must remain equal
after any common admitted finite operation sequence; decision tests separately
need to factor through those observations.

The PVS type `Algebra` is a set of rational-valued functions. `Subalgebra?`
states the closure laws explicitly, and the constructed algebras satisfy those
laws by theorem. Quotient states are complete `ObsEq` classes, not arbitrary
subsets of an equivalence class. Representatives define the quotient maps;
stability and membership prove independence from that choice.

The stable hull is an intersection construction over all stable subalgebras
containing the chosen generators. It has a mathematical leastness property.
This definition does not supply an algorithm for finding a small hull.

Zero/one indicators embed Boolean certificate predicates into this algebra.
Fixedness of the protected indicators prevents semantic invalidation. Stability
instead retains the information needed to compare certificate decisions after
the same admitted sequence from observationally equivalent initial states.
It does not require certificate truth to stay constant along that sequence.

For stochastic models, expectation is linear but is not generally
multiplicative. Closure of the full projection algebra requires equal aggregate
transition masses on each summary fiber. The good-state predicate has an
independent factorization condition. Their connection to the existing
`ppg_finite_lumping` interface transfers its probability results.
The examples show why checking expectation on algebra generators alone is
insufficient: the generator's expected value can agree on two states while the
expected value of its square distinguishes them.

## Scope boundaries

The function-algebra and finite-kernel development is separate from the Lean
`ObservableSchemes` module, which uses Mathlib affine schemes and structure
sheaves. A projection or a family of evaluation functions does not establish a
PVS port of that algebraic-geometric foundation. No such equivalence is claimed
by the rational observable interface.

The source correspondence accounts for 144 specialized Lean claims from the
seven function-algebra, kernel and hazard modules. The PVS sources contain 223
explicit claims: these 144 counterparts and 79 supporting claims, including
the certificate-indicator bridge. These counts describe correspondence and
proof organization, rather than 223 independent new mathematical results.

The PVS pullback interface concerns endomorphisms of one state type. Lean also
provides pullbacks between different state types and composition through three
types. Those extra type-polymorphic interfaces and the 34 `ObservableSchemes`
source results remain outside this PVS specialization. Correspondence should
therefore be read with these scalar and state-type restrictions, rather than
as an assertion that every Lean repair declaration has the same PVS type.

The development concerns specified state transformers and checkers. It does not
prove arbitrary C or Python implementations, a learning algorithm, reliable
external evidence, or physical actuation. MT/LLL applicability still requires
its own independence and probability hypotheses.

## References

- Dragan Stosic, *Proof-Preserving Graphs*, public Lean repair modules, revision
  `60151677e58704ce856c05a572904d681fd959f6`.
- University of Edinburgh, [HASE DLX scoreboard model](https://www.icsa.inf.ed.ac.uk/research/groups/hase/models/dlx-scb/index.html),
  for the architectural RAW/WAR/WAW terminology.
- David A. Levin and Yuval Peres, *Markov Chains and Mixing Times*, second
  edition, American Mathematical Society, 2017, Section 2.3.1, Lemma 2.5 and
  equation (2.10), for the finite lumpability criterion.

## Verification

Replay the group with the pinned library setup documented in the repository
README:

```sh
python3 scripts/check.py --group repair --jobs 1 --heap-mib 6144 --timeout 60
```

The [verification record](../reports/PVS_REPAIR_OBSERVABLES_20261030.json)
identifies the exact entry points, loaded dependency closure and source/proof
hashes of the normal replay completed on 2026-10-30. It passed 450 Project proof
bodies across 34 loaded modules, starting from the 11 repair source files.
The new theories contribute 242 bodies: 223 explicit claims and 19 TCCs. The
other 208 bodies belong to unchanged Project dependencies. No Native proof
bodies were required; unfinished, missing-script and derived-only counters
were zero, and proof oracles were disabled. The new source files contain no
`AXIOM` declarations.

Project proof-body counts include supporting lemmas and TCCs. They are separate
from Lean source-result counts and do not replace the historical 1,824-result
PVS translation ledger with a new whole-library replay claim.
