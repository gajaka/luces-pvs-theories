# Parametric Certification Theories

## Proof-Preserving Graphs

A proof-preserving graph is a graph where every edge satisfies a refinement relation AND both endpoints maintain their local invariants. The graph may evolve (add vertices, add edges) but can never violate these constraints.

Consequences: if a vertex is connected to the certified core, it holds its invariant. If it does not hold its invariant, it is isolated, and no edge from the good part reaches it. Paths persist once established. Evolution is monotone. Deterministic traversal (computing the next vertex without the Axiom of Choice) follows from uniqueness along pp-valid edges. Repair reconnects isolated vertices via relational choice on finite candidate sets.

Built on NASA PVS Library: graphs@graphs (Butler and Sjogren, 1998) and sets_aux@rr_rel (Stosic, refinement relations).

The core theory extends in two directions. First, pp_graphs_extended adds time, weight, and fault tolerance. Temporal PP-graphs index the graph by discrete time: invariant sets grow monotonically, paths persist once established, and eventually the system reaches a fixpoint. Weighted PP-graphs connect to optimal transport by assigning costs to edges, with cyclical monotonicity preventing crossing. Byzantine fault tolerance follows from pp-validity: any vertex that violates its invariant is automatically isolated from the honest core, and connected vertices are always honest. Second, categorical_pp_graphs lifts refinement from the element level (rr_rel on vertices) to the graph level. A PP-morphism preserves vertices and pp-edge structure. An embedding is an injective morphism. A quotient is a surjective morphism. A concrete graph refines an abstract graph via a quotient morphism, and simulation (abstraction-concretization round-trip) implies refinement. This is the structural backbone that lets the certification framework project the specification graph onto its quotient via a surjective pp-morphism (cert_quotient_bridge).

## The Certification Problem

You have a system producing data. You have certificates that check whether the data meets certain standards. The usual question is: does it pass or fail?

Wrong question. The right question is: how far does certification reach, and what stops it from going further?

## From Binary to Graded

Specifications form a partial order, where some are stricter than others. A certificate is monotone: if data passes at a strict level, it passes at all weaker levels. This is the master refinement property.

Once you have monotonicity, the set of all levels a datum satisfies is a principal upper set with a unique generator. That generator is the canonical level, the tightest specification the data currently meets.

## The PPG Connection

The specification space is a graph: vertices are specification levels, edges connect comparable levels. The certified subgraph (only levels where certification holds) is pp-valid. Every edge satisfies the pp-edge predicate, with certification as the vertex invariant and refinement as the edge relation.

One line from master refinement: certified at the source implies certified at the target. So the entire PPG machinery applies to the specification space. Connected vertices are all certified. Uncertified levels are isolated. Evolution is monotone. Paths persist. No additional axioms needed. It falls out of the master theorem.

## Blocking as Diagnosis

At the canonical level, every certificate passes and the blocking set is empty. At any stricter level, at least one certificate fails and the blocking set is nonempty. Both directions proved. The pair (canonical level, blocking set) is the full certification state.

## Relaxation vs Repair

Two responses when certification fails at a desired level. Relaxation weakens the specification (move up in the order). Repair changes the data to meet the original bar. In PPG terms: relaxation follows an existing edge to a weaker vertex; repair reconnects an isolated vertex to the certified core. A system that only relaxes is degrading. A system that repairs is recovering.

## Quotient and Hierarchical Selection

Two specifications that certify exactly the same data are certification-equivalent. The quotient carries a well-defined partial order. Certification equivalence is the intersection of per-datum lens equivalences, which is the finest equivalence the family generates. Proved in Lean as an exact identity, not an analogy.

## Run the Example

27 certificates on an embedded spectral sensing system (4-node ESP32 mesh, AS7341 sensor, 10 channels). Five levels: S > A > B > C > D. The engine finds canonical level C for most logs (structure sound, Monge concentration too weak for B). boot334 fails at all levels because generator coherence is negative (spectral flow reverses mid-transition). C_CS (structural) passes everywhere. C_GEN (dynamical) fails only on boot334. Independent axes, no threshold tuning.

Full results: [CERT_RUNNER_RESULTS.md](https://github.com/gajaka/luces-pvs-theories/blob/main/CERT_RUNNER_RESULTS.md)

## Theory Flow

```
refinement --> monotone certification --> canonical level --> blocking set --> PP-graph --> relaxation/repair --> quotient
```

## Files

| File | Theorems |
|------|----------|
| [proof_preserving_graphs.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/proof_preserving_graphs.pvs) | 40 |
| [pp_graphs_extended.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/pp_graphs_extended.pvs) | 26 |
| [categorical_pp_graphs.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/categorical_pp_graphs.pvs) | 7 |
| [pp_graph_repair.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/pp_graph_repair.pvs) | 10 |
| [parametric_certification.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/parametric_certification.pvs) | 35 |
| [cert_quotient.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/cert_quotient.pvs) | 35 |
| [cert_selection.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/cert_selection.pvs) | 25 |
| [cert_blocking.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/cert_blocking.pvs) | 7 |
| [cert_quotient_bridge.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/cert_quotient_bridge.pvs) | 4 |
| [directed_pp_graph.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/directed_pp_graph.pvs) | 1 |
| [ppg_self_assessment.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/ppg_self_assessment.pvs) | 12 |
| [ppg_assessment_bridge.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/ppg_assessment_bridge.pvs) | 8 |

210 theorems (PPG + certification + self-assessment + bridge). Full repo: 456 theorems, 41 theories.
Lean 4: 172 theorems, zero sorry.

## Self-Assessment Theory

A proof-preserving graph does not promise that failures will not occur. It promises something stronger: a failure cannot remain structurally connected to the certified graph. The violating vertex is automatically isolated, no edge reaches it in either direction, and no evolution of the graph can silently reclassify it as certified without restoring its invariant.

This gives a formal notion of self-assessment without anthropomorphism. The graph carries its own admissibility conditions. It can detect when a component no longer belongs to the certified core, isolate that component without invalidating the rest, and admit it again after repair.

Three evolution modes are formally distinct:

```
PP evolution: G --> G', Spec fixed (graph grows, invariant unchanged)
Relaxation:   theta --> theta', State fixed (weaken the contract)
Repair:       s --> s', Spec fixed (restore the system to the bar)
```

Relaxation changes what is demanded. Repair changes what the system does. The type system enforces this separation: repair is a function on states (S --> V --> S) with no access to the specification as a mutable object.

A repair operator is valid (proof-preserving) if it satisfies two proof obligations: target restoration (the broken vertex becomes certified) and core preservation (no previously certified vertex loses its status). Monotone recovery is then a derived theorem, not a definitional truth.

The theory is proved in PVS (12 theorems, all proved): [ppg_self_assessment.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/ppg_self_assessment.pvs)

The formal pipeline has five components:

```
Detect  --> violation                (vertex breaks invariant)
Contain --> failure_total_isolation  (no edges in either direction)
Assess  --> assessment_trichotomy   (certified / repairable / non-repairable)
Repair  --> valid_repair            (proof obligations: target restored + core preserved)
Recover --> repair_strict_growth    (Certified(s) ⊊ Certified(R(s,v)))
```

## Assessment Bridge (complete)

Parametric certification is an instance of the self-assessment repair model. The bridge ([ppg_assessment_bridge.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/ppg_assessment_bridge.pvs), 8 theorems, all proved) sets S := D, V := Θ, Spec := fully_certified F, and applies the repair operator directly over the specification space.

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

Planned cleanup: make valid_cert_repair definitionally equal to valid_repair applied to certSpec F (type-level identity, not just semantic equivalence).

## Empirical Verification (complete_repair_cycle on real data)

Repair operator: firmware tau recalibration. Specification: fixed (S/A/B/C/D thresholds unchanged).

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

PVS formalization complete: [ppg_self_assessment.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/ppg_self_assessment.pvs) (12 theorems, all proved) + [ppg_assessment_bridge.pvs](https://github.com/gajaka/luces-pvs-theories/blob/main/ppg_assessment_bridge.pvs) (8 theorems, all proved).

## Open Problem: Probabilistic Repair Convergence

The blocking dependency decomposition reveals that some certificate components are locally repairable while others are genuinely coupled (negative discriminant proves infeasibility of the General LLL condition for certain pairs). This raises the question: can we formally guarantee that a randomized repair operator converges to a good state?

The natural framework is the Lovász Local Lemma (Alon and Spencer, "The Probabilistic Method", 4th ed., Wiley 2016, Lemma 5.1.1): given bad events with bounded dependency and probabilities satisfying the General LLL condition, a configuration where no bad event occurs exists with positive probability. The algorithmic version (Moser-Tardos, 2010) gives a constructive randomized repair procedure with expected polynomial convergence.

This is active ongoing work.

## Related

- Lean 4 port: [ppg-lean](https://github.com/gajaka/ppg-lean)
- Paper 3: [DOI 10.5281/zenodo.21956336](https://zenodo.org/records/21956336)
- Paper (in preparation): "Parameterized Proof-Preserving Certification"
