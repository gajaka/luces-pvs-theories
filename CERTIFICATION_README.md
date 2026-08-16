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

190 theorems (PPG + certification). Full repo: 435 theorems, 39 theories.
Lean 4: 153 theorems, zero sorry.

## Related

- Lean 4 port: [ppg-lean](https://github.com/gajaka/ppg-lean)
- Paper 3: [DOI 10.5281/zenodo.21956336](https://zenodo.org/records/21956336)
- Paper (in preparation): "Parameterized Proof-Preserving Certification"
