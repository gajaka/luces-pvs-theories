# Parametric Certification Theories

The design discussion and boot tables below include historical case-study
material. For current application contracts, measured bindings and limits, read
[LUCES model scope](LUCES_MODEL_SCOPE.md) and the
[theorem-scope record](THEOREM_SCOPE.md). The boot comparisons are observations
from separate runs, not a formal refinement proof of a firmware intervention.

## Proof-Preserving Graphs

A proof-preserving graph is a graph where every edge satisfies a refinement relation AND both endpoints maintain their local invariants. The graph may evolve (add vertices, add edges) but can never violate these constraints.

In a pp-valid graph, any endpoint of an admitted edge satisfies its invariant.
A failing vertex is isolated in that graph. Paths persist under the separately
defined monotone graph extensions with a fixed invariant; arbitrary state
changes need a preservation proof. Uniqueness gives deterministic traversal in
the corresponding relational model. These graph properties do not supply an
implementation that detects failures or repairs a physical system.

Built on NASA PVS Library: graphs@graphs (Butler and Sjogren, 1998) and sets_aux@rr_rel (Stosic, refinement relations).

The extended models state the time, cost and fault assumptions they use.
Isolation relative to a chosen invariant is not a Byzantine-consensus theorem.
The categorical interface defines morphisms, injective embeddings and
surjective quotients. A specification projection generally sends an edge to an
edge **or a collapsed vertex**. The actual categorical quotient results require
the stated noncollapse and descent conditions; see
`ppg_selection_quotient_graph` and `ppg_list_quotient_bridge`. The legacy
`cert_quotient_bridge` keeps its weaker projection predicate.

## The Certification Problem

You have a system producing data. You have certificates that check whether the data meets certain standards. The usual question is: does it pass or fail?

Wrong question. The right question is: how far does certification reach, and what stops it from going further?

## From Binary to Graded

Specifications form a partial order, where some are stricter than others. A certificate is monotone: if data passes at a strict level, it passes at all weaker levels. This is the master refinement property.

Monotonicity makes the certified levels an upper set. When a least certified level exists, that set is principal and its generator is the canonical level. The complete-lattice results require a nonempty certified set and closure under the stated infima; monotonicity alone does not supply a least level.

## The PPG Connection

The specification space is a graph: vertices are specification levels, edges connect comparable levels. The certified subgraph (only levels where certification holds) is pp-valid. Every edge satisfies the pp-edge predicate, with certification as the vertex invariant and refinement as the edge relation.

Master refinement gives certification at the weaker target level. The resulting
certified specification graph is pp-valid. Path persistence additionally uses
the chosen fixed-predicate graph extension; state repair uses its own target and
preservation obligations.

## Blocking as Diagnosis

At the canonical level, every certificate passes and the blocking set is empty. At any stricter level, at least one certificate fails and the blocking set is nonempty. Both directions proved. The pair (canonical level, blocking set) is the full certification state.

## Relaxation vs Repair

Two responses when certification fails at a desired level. Relaxation weakens the specification (move up in the order). Repair changes the data to meet the original bar. In PPG terms: relaxation follows an existing edge to a weaker vertex; repair reconnects an isolated vertex to the certified core. A system that only relaxes is degrading. A system that repairs is recovering.

## Quotient and Hierarchical Selection

Two specifications that certify exactly the same data are certification-equivalent. The quotient carries a well-defined partial order. Certification equivalence is the intersection of per-datum lens equivalences, which is the finest equivalence the family generates. Proved in Lean as an exact identity, not an analogy.

## Run the Example

The historical report compares five certification levels, S > A > B > C > D,
on embedded spectral logs. Its recorded classifications and counts describe
that run. The current numerical runner and its versioned observability screens
are documented separately in its
[README](https://github.com/gajaka/master-controler/blob/main/cert_runner/README.md).

Full results: [CERT_RUNNER_RESULTS.md](CERT_RUNNER_RESULTS.md)

## Theory Flow

```
refinement --> monotone certification --> canonical level --> blocking set
  --> dependency decomposition --> LLL feasibility --> relaxation/repair --> quotient
```

The full tracked family supplies a dependency graph through shared variable
support; passing certificates must remain in that graph because a repair can
invalidate them. A satisfied Local Lemma budget is a sufficient existence
criterion. An infeasible numerical budget, including a negative pairwise
discriminant, rules out that sufficient criterion; it does not prove that no
good assignment or repair exists. Moser–Tardos convergence uses the stated
event probabilities, dependency conditions and resampling law.

The repair path is three steps:

```
decomposition --> decision --> construction
```

Decomposition organizes dependencies, a numerical LLL check can certify a
sufficient budget, and a valid resampling construction gives its own
termination or expected-work conclusion. Existence of some good state alone
does not establish convergence of an arbitrary repair operator.

## Files

| File | Theorems |
|------|----------|
| [proof_preserving_graphs.pvs](../theories/ppg_core/proof_preserving_graphs.pvs) | 37 |
| [pp_graphs_extended.pvs](../theories/ppg_core/pp_graphs_extended.pvs) | 21 |
| [categorical_pp_graphs.pvs](../theories/ppg_core/categorical_pp_graphs.pvs) | 6 |
| [pp_graph_repair.pvs](../theories/ppg_core/pp_graph_repair.pvs) | 9 |
| [parametric_certification.pvs](../theories/certification/parametric_certification.pvs) | 28 |
| [cert_quotient.pvs](../theories/certification/cert_quotient.pvs) | 30 |
| [cert_selection.pvs](../theories/certification/cert_selection.pvs) | 21 |
| [cert_blocking.pvs](../theories/certification/cert_blocking.pvs) | 7 |
| [cert_quotient_bridge.pvs](../theories/certification/cert_quotient_bridge.pvs) | 4 |
| [directed_pp_graph.pvs](../theories/ppg_core/directed_pp_graph.pvs) | 0 |
| [ppg_self_assessment.pvs](../theories/certification/ppg_self_assessment.pvs) | 12 |
| [ppg_assessment_bridge.pvs](../theories/certification/ppg_assessment_bridge.pvs) | 7 |
| [ppg_probabilistic.pvs](../theories/moser_tardos/ppg_probabilistic.pvs) | 10 |
| [ppg_lll.pvs](../theories/local_lemmas/ppg_lll.pvs) | 30 |
| [ppg_mt.pvs](../theories/moser_tardos/ppg_mt.pvs) | 5 |
| [ppg_mt_process.pvs](../theories/moser_tardos/ppg_mt_process.pvs) | 5 |
| [ppg_mt_growing.pvs](../theories/moser_tardos/ppg_mt_growing.pvs) | 18 |
| [ppg_mt_witness.pvs](../theories/moser_tardos/ppg_mt_witness.pvs) | 6 |
| [ppg_mt_injectivity.pvs](../theories/moser_tardos/ppg_mt_injectivity.pvs) | 22 |
| [ppg_mt_convergence.pvs](../theories/moser_tardos/ppg_mt_convergence.pvs) | 8 |
| [ppg_mt_weight.pvs](../theories/moser_tardos/ppg_mt_weight.pvs) | 4 |

This table records the earlier certification and Moser–Tardos entry points. The generic Lean-to-PVS translation was completed on 2026-10-24: all 1,824 recorded source theorems and lemmas in 191 Lean modules have replayed PVS counterparts. Supporting PVS lemmas and TCCs are additional obligations. See the [repository README](../README.md#typechecking-and-proof-replay) for the complete proof scope, replay records and current commands.

## Self-Assessment Theory

A pp-valid graph excludes edges incident to a vertex failing the selected
invariant. This is a property of the mathematical graph at the evaluated
state. An implementation must still evaluate certificates and maintain that
graph. A fixed-predicate graph extension cannot change the invariant's meaning;
a repair changes data and needs separate restoration and preservation proofs.

This supplies formal admissibility and repair conditions. An implementation
must evaluate the conditions, update its graph and justify its repair operation;
the graph definition does not perform those actions by itself.

Three evolution modes are formally distinct:

```
PP evolution: G --> G', Spec fixed (graph grows, invariant unchanged)
Relaxation:   theta --> theta', State fixed (weaken the contract)
Repair:       s --> s', Spec fixed (restore the system to the bar)
```

Relaxation changes what is demanded. Repair changes the represented data. The
formal repair model fixes the specification as a parameter and uses a function
on states (`S --> V --> S`). This does not by itself enforce a fixed policy in
an external program.

A repair operator is valid (proof-preserving) if it satisfies two proof obligations: target restoration (the broken vertex becomes certified) and core preservation (no previously certified vertex loses its status). Monotone recovery is then a derived theorem, not a definitional truth.

The theory is proved in PVS (12 theorems, all proved): [ppg_self_assessment.pvs](../theories/certification/ppg_self_assessment.pvs)

The formal pipeline has five components:

```
Detect  --> violation                (vertex breaks invariant)
Contain --> failure_total_isolation  (no edges in either direction)
Assess  --> assessment_trichotomy   (certified / repairable / non-repairable)
Repair  --> valid_repair            (proof obligations: target restored + core preserved)
Recover --> repair_strict_growth    (Certified(s) ⊊ Certified(R(s,v)))
```

## Assessment Bridge (complete)

Parametric certification is an instance of the self-assessment repair model. The bridge ([ppg_assessment_bridge.pvs](../theories/certification/ppg_assessment_bridge.pvs), 7 theorems, all proved) sets S := D, V := Θ, Spec := fully_certified F, and applies the repair operator directly over the specification space.

The complete formal cycle:

```
canonical(d)              --> where you are
blocking(d, t)            --> what blocks you
failure_total_isolation   --> failure contained
valid_cert_repair(R,d,t)  --> proof obligations met
cert_repair_strict_growth --> CertifiedLevels(d) ⊊ CertifiedLevels(R(d,t))
repair_removes_blockers   --> blocking_set(R(d,t), t) = ∅
canonical_frontier_advances --> t_c_new ≤ t ≤ t_c_old
```

Key theorem (complete_repair_cycle): given a broken target and a valid repair operator, the repaired datum is certified at t, all previously certified levels are preserved, blocking set is empty, and new canonical is at most t.

The later dependency bridge derives the state-repair preservation contract
from locality, a write frame and checked component postconditions. The concrete
finite-read instance derives locality from syntax and checks the full family
before selecting a candidate.

## Historical boot comparison

The following recorded comparison used unchanged S/A/B/C/D thresholds and was
interpreted as a tau-recalibration case study. The quoted `FORMAL VERIFICATION`
and `ALL PROPERTIES VERIFIED` labels report comparisons of the extracted
certification sets. They do not prove that a firmware transformation caused
the change between the separate boot experiments or formally verify that code.
The actual generic theorem is conditional on its valid-repair premises.

```
PRE-FIX (state BEFORE repair)

  boot334:
    Canonical level: FAIL
    Certified levels: NONE
    Observables: rho=1.0000 monge=0.7609 gap=5.45e-16 coh=0.0000 sparsity=0.1900
    Blocking at S: {monge_min: 0.7609 vs 0.9, sparsity_max: 0.1900 vs 0.02, coherence_min: 0.0000 vs 0.85}
    Blocking at A: {coherence_min: 0.0000 vs 0.7, monge_min: 0.7609 vs 0.8, sparsity_max: 0.1900 vs 0.05}
    Blocking at B: {sparsity_max: 0.1900 vs 0.1, coherence_min: 0.0000 vs 0.5}
    Blocking at C: {coherence_min: 0.0000 vs 0.3}
    Blocking at D: {coherence_min: 0.0000 vs 0.1}

POST-FIX (state AFTER repair)

  boot347:
    Canonical level: C
    Certified levels: {C, D}
    Observables: rho=0.9970 monge=0.7619 gap=1.35e-16 coh=0.9982 sparsity=0.1900

  boot349:
    Canonical level: D
    Certified levels: {D}
    Observables: rho=1.0000 monge=0.7584 gap=2.12e-16 coh=0.2371 sparsity=0.1900

  boot330:
    Canonical level: C
    Certified levels: {C, D}
    Observables: rho=0.9970 monge=0.7688 gap=6.21e-16 coh=0.8740 sparsity=0.1900

  boot320:
    Canonical level: C
    Certified levels: {C, D}
    Observables: rho=0.9970 monge=0.7399 gap=2.53e-16 coh=0.9988 sparsity=0.1900

FORMAL VERIFICATION (complete_repair_cycle)

  Before (boot334): canonical=FAIL, certified=NONE
  After  (boot347): canonical=C, certified={C, D}

  [1] repair_strict_growth:
      CertifiedLevels(before) = {}
      CertifiedLevels(after)  = {C, D}
      Subset: True, Proper: True
      VERDICT: PASS (CertifiedLevels(before) ⊊ CertifiedLevels(after))

  [2] repair_removes_all_blockers (target=C):
      BlockingSet(before, C) = {coherence_min: 0.0000 vs 0.3}
      BlockingSet(after, C)  = {}
      VERDICT: PASS (blockers cleared at C)

  [3] canonical_frontier_advances:
      Canonical(before) = FAIL (index 5)
      Canonical(after)  = C (index 3)
      VERDICT: PASS (canonical frontier advanced: FAIL --> C)

  COMPLETE REPAIR CYCLE: ALL PROPERTIES VERIFIED

  The firmware tau recalibration (repair operator R) changed the
  system state while the specification remained fixed. The certified
  region strictly grew, all blockers at level C were removed, and
  the canonical frontier advanced from FAIL to C.

  Backed by: complete_repair_cycle (ppg_assessment_bridge.pvs)
```

PVS formalization complete: [ppg_self_assessment.pvs](../theories/certification/ppg_self_assessment.pvs) (12 theorems, all proved) + [ppg_assessment_bridge.pvs](../theories/certification/ppg_assessment_bridge.pvs) (7 theorems, all proved).

## Probabilistic Repair Convergence

The blocking dependency decomposition reveals that some certificate components are locally repairable while others are genuinely coupled (negative discriminant proves infeasibility of the General LLL condition for certain pairs). This raises the question: can we formally guarantee that a randomized repair operator converges to a good state?

The framework is the Lovász Local Lemma (Alon and Spencer, "The Probabilistic Method", 4th ed., Wiley 2016, Lemma 5.1.1): given bad events with bounded dependency and probabilities satisfying the General LLL condition, a configuration where no bad event occurs exists with positive probability. This existence result is now machine-checked (`ppg_lll.pvs`, 30 theorems), with the blocking decomposition and pair infeasibility formalized in `ppg_probabilistic.pvs` (10 theorems). The proof is division-free, so it never requires nonzero conditioning measure.

Under its stated dependency and probability hypotheses, the Moser–Tardos algorithm supplies randomized resampling. The Lean and PVS developments include the resampling process, witness construction and injectivity, the expected-work bound E[T_LOG] ≤ Σ x(α), and the reachability bridge to abstract repair. Their statements and entry points are indexed in the [repository README](../README.md#central-theorems); the [Lean development](https://github.com/gajaka/ppg-lean) gives the corresponding source results.

## Related

- Lean 4 port: [ppg-lean](https://github.com/gajaka/ppg-lean)
- Paper 3: [DOI 10.5281/zenodo.21956336](https://zenodo.org/records/21956336)
- Paper (in preparation): "Parameterized Proof-Preserving Certification"
