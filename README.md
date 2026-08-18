# Proof-Preserving Graphs: Formal Certification, Self-Assessment, and Repair

**A formal mathematical framework for structural resilience, with applications to optimal transport verification and hardware root-of-trust.**

41 theories. 456 machine-checked theorems. All proved in PVS.

**Core is closed.** Four questions, each with a machine-checked answer: How far does certification reach? What stops it from going further? Can the failure be safely contained and repaired? Did repair provably advance certification?

---

## Mathematical Framework: Proof-Preserving Graphs

A proof-preserving graph is a graph where every edge satisfies a refinement relation AND both endpoints maintain their local invariants. The graph may evolve (add vertices, add edges) but can never violate these constraints.

Built on:
- NASA PVS Library `graphs@graphs` (Butler & Sjogren, 1998)
- NASA PVS Library `sets_aux@rr_rel` (Stosic — refinement relations)

| Theory | Theorems | Scope |
|--------|----------|-------|
| `proof_preserving_graphs.pvs` | 40 | Core framework: validity hierarchy, walks, paths, evolution, monotonicity, connectivity, separation, deterministic traversal, violation detection, certificate chains |
| `pp_graphs_extended.pvs` | 26 | Extensions: temporal evolution, weighted/OT connection, algebraic automorphisms, fault tolerance, categorical morphisms |
| `lowrisc_boot_verification.pvs` | 11 | Application: secure boot chain (layered DAG, failure isolation, lock-out) |
| `opentitan_boot_instance.pvs` | 9 | Concrete instantiation: OpenTitan ROM --> ROM_EXT --> BL0 --> Kernel |
| `lie_pp_connection.pvs` | 7 | Bridge: curvature-coherence inverse law, Lie generator <--> PP-graph |
| `pp_graph_repair.pvs` | 10 | Repair semantics: relational choice, isolation reversal, route bypass, convergence |
| `categorical_pp_graphs.pvs` | 7 | Categorical structure: morphisms, embeddings, quotients, refinement, simulation |
| `parametric_certification.pvs` | 35 | Parametric certification: master refinement, lattice operators, PPG bridge, threshold instance, completeness |
| `cert_quotient.pvs` | 35 | Quotient structure: cert_equiv, induced PartialOrder, meet closure, separating family |
| `cert_selection.pvs` | 25 | Hierarchical selection: pullback equiv, CertFamily, representative lenses |
| `cert_blocking.pvs` | 7 | Blocking certificates: diagnostic layer, canonical emptiness, stricter nonemptiness |
| `cert_quotient_bridge.pvs` | 4 | Bridge: spec graph projects to quotient PPG via surjective morphism |
| `directed_pp_graph.pvs` | 1 | Directed PPG definitions: structural foundation for parametric theories |

**Lean 4 port:** [ppg-lean](https://github.com/gajaka/ppg-lean) — 172 theorems, zero sorry, verified with Mathlib. Includes complementary slackness, self-assessment, and assessment bridge (parametric certification as instance of repair semantics).

### Key Results

**Structural Resilience:**
- Graph evolution forms a partial order (reflexive, transitive, antisymmetric)
- Invariant sets grow monotonically under transformation
- Paths persist once established

**Deterministic Traversal:**
- Inference function extraction without Axiom of Choice
- Uniqueness (one successor per vertex) gives definite description
- Constructive: computable traversal, not existential witness

**Fault Tolerance:**
- Byzantine vertices are isolated in pp-valid graphs
- Connected vertices are always honest

**Secure Boot (applied):**
- Boot chain is a DAG (layered acyclicity)
- Failure at level k blocks all levels > k
- No unsigned execution past verification

---

## Optimal Transport Certificates

25 theories formalizing Kantorovich duality and optimal transport structure, validated on real spectral data from a 4-node ESP32 mesh network.

| Theory | Theorems | Topic |
|--------|----------|-------|
| `kantorovich_duality.pvs` | 11 | Kantorovich dual formulation |
| `brenier_uniqueness.pvs` | 6 | Brenier map uniqueness |
| `cyclical_monotonicity.pvs` | 5 | Cyclical monotonicity characterization |
| `displacement_interpolation.pvs` | 9 | McCann displacement interpolation |
| `displacement_concavity.pvs` | 7 | Displacement concavity/convexity |
| `wasserstein_metric.pvs` | 10 | Wasserstein metric properties |
| `transport_structure.pvs` | 10 | Transport map structure |
| `transport_structure_v2.pvs` | 7 | Refined transport structure |
| `transport_stability.pvs` | 11 | Stability of transport maps |
| `stability_of_maps.pvs` | 5 | Map persistence under perturbation |
| `monge_kantorovich_equivalence.pvs` | 5 | Monge-Kantorovich equivalence |
| `lie_generator_structure.pvs` | 17 | Lie generator coherence (T10) |
| `fisher_boundary.pvs` | 5 | Fisher information boundary |
| `fisher_voronoi.pvs` | 5 | Fisher-Voronoi partition |
| `dual_observability.pvs` | 6 | Dual observability certificates |
| `hybrid_observability.pvs` | 3 | Hybrid observability |
| `tangent_bundle.pvs` | 9 | Tangent bundle structure |
| `velocity_asymmetry.pvs` | 8 | Dawn/dusk velocity asymmetry |
| `entropy_along_geodesic.pvs` | 8 | Entropy production along geodesics |
| `rank_orientation.pvs` | 3 | Rank and orientation preservation |
| `global_optimality.pvs` | 12 | Geodesic segmentation: local excess vs global optimality, interpolation, coexistence |
| `unbalanced_regime.pvs` | 12 | Unbalanced OT: source/sink dynamics, deviation functional, regime classification |
| `fisher_atlas.pvs` | 11 | Manifold atlas: charts, transition maps, Fisher metric, Fisher<-->Wasserstein bridge |
| `observability_geometry.pvs` | 8 | Paper 2: excitation-dependent observability, temporal chart stratification (Allen intervals) |
| `observability_refinement.pvs` | 12 | Paper 2: axiom refinement, SNR margin, quantitative robustness bound |

### Key Theorem (T10)

```pvs
thm_coherence_iff: THEOREM
  continuously_observed?(p) AND NOT shape_direction_reversal?(p)
    IFF coherent?(p)
```

Validated on 13 independent experiments.

---

## Z3/SMT2 Proofs

| File | Solver | Result |
|------|--------|--------|
| `fisher_boundary_strong.smt2` | Z3 (NRA) | UNSAT — theorem holds |
| `brenier_t3_surjective.smt2` | Z3 (QF_LIA, N=20) | UNSAT — theorem holds |

---

## Sterbenz Floating-Point Proof

`Sterbenz/` — Correctness proof of Sterbenz's lemma via frama-c → Jessie → PVS pipeline.

---

## Related Publications

1. "Empirical Information Geometry on an Embedded Adaptive Lighting System" — [DOI: 10.5281/zenodo.20094759](https://zenodo.org/records/20094759)
2. "Excitation-Dependent Observability Geometry on an Embedded Adaptive Lighting Manifold" — [DOI: 10.5281/zenodo.20389804](https://zenodo.org/records/20389804)
3. "Optimal Transport Geometry of Natural Spectral Regime Transitions" — [DOI: 10.5281/zenodo.21956336](https://zenodo.org/records/21956336)
4. (In preparation) "Parametric Proof-Preserving Certification for Runtime Transport Invariants"

## System

- Hardware: 4-node ESP32 mesh (ESP32-S3 + ESP32-C6), AS7341 spectral sensor, TSL2591 lux
- Runtime: <2W total, no cloud dependency, FreeRTOS, real-time 7s control loop
- Verification: PVS (Prototype Verification System), NASA Langley

## Availability

The core theory is closed. I am available for formal verification, runtime verification, or theorem proving positions (remote, B2B contract from Belgrade, Serbia). Contact: dragan.stosic@gmail.com

## Author

Dragan Stosic, MSc — [NASA PVS Libraries contributor](https://github.com/nasa/pvslib/blob/master/sets_aux/rr_rel.pvs)

## License

© 2026 Dragan Stosic. All rights reserved.
