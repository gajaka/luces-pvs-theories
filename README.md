# Proof-Preserving Graphs: Formal Certification, Self-Assessment, and Repair (PVS)

This PVS development studies graded certification, blocking and repair. It
contains the original PPG and LUCES application theories, together with the
ongoing translation of the generic [Lean 4 library](https://github.com/gajaka/ppg-lean).
The application theories describe transport, observability and secure-boot
models; the generic theory keeps the data, specifications and repair actions
abstract.

As of **2026-10-19**, the translation has independently replayed counterparts
for **1,204 of 1,824 Lean source theorems and lemmas**, with all recorded results
checked in **112 of 191 modules**. Supporting PVS lemmas and type-correctness
conditions are additional obligations and are excluded from those source-result counts.
The translation is still in progress.

## Typechecking and proof replay

The recorded translation checks use **PVS 8.1.2**,
[NASA's PVS libraries](https://github.com/nasa/pvslib) and the `proveit` batch
driver, version `8.1-20260706`. The libraries must be available through
`PVS_LIBRARY_PATH`; its entries are directories containing libraries such as
`measure_integration`, `sets_aux` and `graphs`.

```sh
export PVS_LIBRARY_PATH="/path/to/pvslib"
```

Each `.pvs` file contains specifications and theorem statements. Its `.prf`
companion contains saved proofs. Typechecking checks expressions and generates
type-correctness conditions (TCCs); replaying the proofs checks those conditions
and the theorem bodies. A successful typecheck alone does not establish the
theorems.

From the repository root, typecheck one file without running its proofs:

```sh
proveit --typecheck-only ppg_general_active_count.pvs
```

For a clean replay, use a separate checkout: PVS writes proof metadata and
compiled context files. The following command forces the saved proofs of one
file and its imported project theories, with oracles disabled and no ProofLite
script installation:

```sh
REPORT_DIR="../pvs-proof-reports"
mkdir -p "$REPORT_DIR"

proveit --clean --import-chain --no-scripts --no-purge \
  --disable-oracles --force --timeout 60 --log \
  --dir "$REPORT_DIR" --out active-count \
  ppg_general_active_count.pvs
```

To replay just one theorem from its saved proof:

```sh
proveit --no-scripts --no-purge --disable-oracles --force --log \
  --dir "$REPORT_DIR" --out active-count-equality \
  @ppg_general_active_count.expectedActiveCount_eq_tsum
```

The single-theorem command does not replay the import chain. Use the file-level
command when checking its dependencies as well.

For a batch over the root-level PVS files:

```sh
for file in ./*.pvs; do
  name="${file##*/}"
  proveit --no-scripts --no-purge --disable-oracles --force \
    --timeout 60 --log --dir "$REPORT_DIR" \
    --out "${name%.pvs}" "$file" || exit "$?"
done
```

This loop leaves `Sterbenz/` out of the batch. That older Frama-C/Jessie
development has separate floating-point library dependencies; see its
[README](Sterbenz/README.md).

Recorded translation checks on 2026-10-18 and 2026-10-19 include:

| Check | Result |
|-------|--------|
| General active-count integral and positive-drift budget | 318/318 project obligations complete across 32 theories, including all 87 new obligations. |
| Full resampling, complete dependency graphs and drift-region support | 2,216/2,216 project obligations complete, including 172 new obligations. |
| Native measure and integration support | 1,109 library proof bodies freshly forced over three disjoint rounds, with ordinary complete proof chains. The certificate includes general monotone convergence and the weighted-measure support. |
| General conditional expectation | 600/600 project obligations complete across 52 theories, including all 52 new obligations. |
| General drift, Moser–Tardos certificates and execution cost | 2,241/2,241 project obligations complete across 230 theories, including all 69 new obligations and 14 source results. |
| Generic repair, growing lists and meta refinement | 80/80 project obligations complete across 10 theories, including 13 new obligations and 30 source results. |
| Acyclic relation reversal | 24/24 project obligations complete across 1 theory, including 24 new obligations and 9 source results. |
| Witness DAGs and ancestor prefixes | 61/61 project obligations complete across 2 theories, including 37 new obligations and 15 source results. |
| Longest-path heights and independent layers | 183/183 project obligations complete across 14 theories, including 33 new obligations and 14 source results. |

These runs check saved proofs in isolated workspaces. Project dependencies use
the exact committed source and proof inputs. The separately checked native
library sources and proofs are hashed before and after reuse. A completed run
requires `proved - complete`, including the relevant TCCs and dependencies.
The table records those checks; it does not report a fresh successful replay of
every legacy application file or of `Sterbenz/`.

Some original application theories declare empirical or mathematical axioms.
Their results are conditional on those assumptions. For example,
[kantorovich_duality.pvs](kantorovich_duality.pvs) declares feasibility and
complementary-slackness assumptions, while
[lie_generator_structure.pvs](lie_generator_structure.pvs) states the
observability/coherence assumptions it uses. Their proof scope should be read
from the declarations in those files.

## Motivation

See the [motivation in the Lean README](https://github.com/gajaka/ppg-lean/blob/main/README.md#motivation)
for the LUCES system, the certification problem and the intended controller
workflow.

## Overview

A certificate is a predicate over data and a specification level. Ordered
levels express stronger and weaker contracts. If a certificate passes at a
stricter level, monotonicity makes it pass at every weaker level.

Smaller levels are stricter in the formal order. When a canonical level exists,
the certified region has the characterization `Cert(d, theta) iff theta_c <=
theta`. Monotonicity alone does not give that least certified level. The
complete-lattice construction also requires a nonempty certified set and closure
under infima of nonempty subsets.

At a target level, the blocking set contains the failed certificates. Shared
variables determine a dependency graph. Under predicate locality, a repair
confined to one component's footprint preserves the selected obligations in
other components. Any further admissibility constraints need their own
preservation argument.

A repair changes the state while keeping the target specification fixed. Its
obligations are to restore the target and preserve prior certification. The
framework distinguishes the existence of a repair path, almost-sure success of
a random procedure and a bound on its expected work.

The probabilistic development now includes the original Moser–Tardos
expected-work bound **E[T_LOG] <= sum x(a)**, followed by finite-expectation and
almost-sure termination results. The counting argument permits infinite paths;
termination is derived under the budget hypotheses. Here `x` is a resampling
budget. Classical Local Lemma parameters `q` give `x = q/(1-q)`.

Pegden's independent-subset criterion and strict Shearer positivity provide
further work bounds. Component-local bounds control the expected resampling
count of the selected component under their stated hypotheses. They do not
establish that a schedule eventually serves that component.

Finite rational models support checked potentials, exact expected hitting
counts, survival recurrences and geometric block bounds. Lumping and commuting
updates transfer these results when the transition laws and good-state tests
are preserved. Full resampling also has exact geometric probabilities and an
extended expected-work formula. These are bounds on model steps or resamplings;
a hardware execution-time claim needs an additional timing model.

### Application background

The LUCES theories describe transport structure, spectral observability and
certification of recorded measurements. The
[certificate-runner report](CERT_RUNNER_RESULTS.md) contains the concrete
results for the embedded lighting system. A log can satisfy structural checks
while failing a dynamical one: the `boot334` example records a spectral-direction
reversal while several transport checks still pass.

The boot theories describe a layered verification graph and the consequences of
a failed stage under the declared signature and refinement predicates. The
transport and boot models require a separate connection to the implementation
and physical measurements they describe.

## Files

The tables give entry points into the development. A source result often needs
several PVS files for its finite sums, measurable spaces, probability laws and
integration arguments. Each entry's imports lead to that support.

### Certification, structure and assessment

| Files | Scope |
|-------|-------|
| [proof_preserving_graphs.pvs](proof_preserving_graphs.pvs), [pp_graphs_extended.pvs](pp_graphs_extended.pvs) | Validity, paths, evolution, invariants and graph extensions. |
| [categorical_pp_graphs.pvs](categorical_pp_graphs.pvs), [directed_pp_graph.pvs](directed_pp_graph.pvs) | Morphisms, embeddings, quotients and directed graph structure. |
| [parametric_certification.pvs](parametric_certification.pvs) | Monotone certification, canonical levels, lattice operations and threshold instances. |
| [cert_quotient.pvs](cert_quotient.pvs), [cert_selection.pvs](cert_selection.pvs), [cert_quotient_bridge.pvs](cert_quotient_bridge.pvs) | Certification equivalence, quotient order and hierarchical selection. |
| [cert_blocking.pvs](cert_blocking.pvs), [ppg_self_assessment.pvs](ppg_self_assessment.pvs), [ppg_assessment_bridge.pvs](ppg_assessment_bridge.pvs) | Blocking diagnostics, failure containment and certification after repair. |
| [pp_graph_repair.pvs](pp_graph_repair.pvs), [ppg_repair_semantics.pvs](ppg_repair_semantics.pvs) | Repair relations, restoration and preservation obligations. |
| [ppg_refinement_meta.pvs](ppg_refinement_meta.pvs) | Configuration compatibility, upgrade chains and refinement preservation. |

### Dependency and probabilistic repair

| Files | Scope |
|-------|-------|
| [ppg_bdd.pvs](ppg_bdd.pvs), [ppg_bdd_locality.pvs](ppg_bdd_locality.pvs), [ppg_bdd_cost.pvs](ppg_bdd_cost.pvs) | Shared-variable components, repair non-interference and component costs. |
| [ppg_lll.pvs](ppg_lll.pvs), [ppg_lopsided_probability.pvs](ppg_lopsided_probability.pvs) | General and lopsided Local Lemma criteria. |
| [ppg_mt_random_process.pvs](ppg_mt_random_process.pvs), [ppg_mt_trajectory_measurable.pvs](ppg_mt_trajectory_measurable.pvs) | Product-table trajectories, local counters and measurability. |
| [ppg_mt_growing.pvs](ppg_mt_growing.pvs), [ppg_mt_injectivity.pvs](ppg_mt_injectivity.pvs), [ppg_rose_canonical_enum.pvs](ppg_rose_canonical_enum.pvs) | Witness construction, injective occurrence encodings and canonical trees. |
| [ppg_mt_check_probability.pvs](ppg_mt_check_probability.pvs), [ppg_mt_total_budget.pvs](ppg_mt_total_budget.pvs) | Witness probabilities, occurrence counts and the expected-work bound. |
| [ppg_mt_termination.pvs](ppg_mt_termination.pvs), [ppg_mt_budget_repair.pvs](ppg_mt_budget_repair.pvs) | Almost-sure termination and the repair reachability bridge. |
| [ppg_pegden_expectation.pvs](ppg_pegden_expectation.pvs), [ppg_pegden_termination.pvs](ppg_pegden_termination.pvs) | Independent-subset budgets, expected resamplings and termination. |
| [ppg_shearer_total_expectation.pvs](ppg_shearer_total_expectation.pvs), [ppg_shearer_component_integral.pvs](ppg_shearer_component_integral.pvs) | Strict Shearer expected-work bounds and component integrals. |

### HLS witness DAGs

| Files | Scope |
|-------|-------|
| [ppg_hls_reversal.pvs](ppg_hls_reversal.pvs) | Reversible arcs of arbitrary acyclic relations. |
| [ppg_hls_witness_dag.pvs](ppg_hls_witness_dag.pvs) | Finite witness DAGs, unique sinks, reversal and ancestor prefixes. |
| [ppg_hls_witness_layers.pvs](ppg_hls_witness_layers.pvs), [ppg_finite_nat_sup.pvs](ppg_finite_nat_sup.pvs), [ppg_nat_rank_well_founded.pvs](ppg_nat_rank_well_founded.pvs) | Constructed longest-path heights, independent layers and their successor relation. |

### Integrals, finite stochastic models and stopping bounds

| Files | Scope |
|-------|-------|
| [ppg_probability_measure.pvs](ppg_probability_measure.pvs), [ppg_probability_integral.pvs](ppg_probability_integral.pvs) | Probability laws and their native NASAlib real integrals. |
| [ppg_general_simple_integral.pvs](ppg_general_simple_integral.pvs), [ppg_general_code_order.pvs](ppg_general_code_order.pvs) | Nonnegative integrals from weighted measurable indicators, including infinite event masses. |
| [ppg_general_active_count.pvs](ppg_general_active_count.pvs), [ppg_additive_drift_budget.pvs](ppg_additive_drift_budget.pvs) | Arbitrary-measure count integrals and extended nonnegative budget bounds. |
| [ppg_conditional_existence.pvs](ppg_conditional_existence.pvs), [ppg_subsigma_restricted_integral.pvs](ppg_subsigma_restricted_integral.pvs) | Conditional expectation for integrable real functions under arbitrary finite native measures and sub-sigma algebras. |
| [ppg_additive_conditional_certificate.pvs](ppg_additive_conditional_certificate.pvs), [ppg_additive_certificate_expectation.pvs](ppg_additive_certificate_expectation.pvs) | Conditional potential certificates, integrated decrease, expected active count and almost-sure finiteness. |
| [ppg_mt_fixed_drift.pvs](ppg_mt_fixed_drift.pvs), [ppg_mt_random_init_drift.pvs](ppg_mt_random_init_drift.pvs), [ppg_mt_drift_expected_cost.pvs](ppg_mt_drift_expected_cost.pvs) | Drift bounds for the actual fixed-start and slot-zero MT processes, with bounded per-step costs. |
| [ppg_finite_conditional_value.pvs](ppg_finite_conditional_value.pvs), [ppg_finite_conditional_drift.pvs](ppg_finite_conditional_drift.pvs) | Finite-state conditional values and integrated drift. |
| [ppg_finite_potential_synthesis.pvs](ppg_finite_potential_synthesis.pvs), [ppg_finite_potential_accessible.pvs](ppg_finite_potential_accessible.pvs) | Rational first-step equations, checked potentials and positive-mass accessibility. |
| [ppg_exact_mt_fixed.pvs](ppg_exact_mt_fixed.pvs), [ppg_exact_mt_random.pvs](ppg_exact_mt_random.pvs) | Exact fixed-start and random-start MT expected work. |
| [ppg_resampling_table_tail.pvs](ppg_resampling_table_tail.pvs), [ppg_tail_mt_fixed.pvs](ppg_tail_mt_fixed.pvs), [ppg_tail_mt_random.pvs](ppg_tail_mt_random.pvs) | Exact stopping probabilities, checked geometric bounds and closed bad classes. |
| [ppg_finite_lumping_paths.pvs](ppg_finite_lumping_paths.pvs), [ppg_update_projection_stopping.pvs](ppg_update_projection_stopping.pvs) | Exact stopped-count reduction through lumping and commuting updates. |
| [ppg_full_resampling_probability.pvs](ppg_full_resampling_probability.pvs), [ppg_full_resampling_mean.pvs](ppg_full_resampling_mean.pvs) | Full-resampling geometric laws, expected work and positive good-state mass. |

### Feasibility and checked refutations

| Files | Scope |
|-------|-------|
| [ppg_certified_decision.pvs](ppg_certified_decision.pvs), [ppg_unsatisfiable_core.pvs](ppg_unsatisfiable_core.pvs) | Finite feasibility decisions and minimal infeasible cores. |
| [ppg_correction_duality.pvs](ppg_correction_duality.pvs) | Minimal-core and correction-set duality. |
| [ppg_farkas_certificate.pvs](ppg_farkas_certificate.pvs), [ppg_farkas_refutation.pvs](ppg_farkas_refutation.pvs) | Soundness of rational Farkas certificates and model-based reachability refutations. |
| [ppg_finite_abstraction_repair.pvs](ppg_finite_abstraction_repair.pvs), [ppg_find_good_path.pvs](ppg_find_good_path.pvs) | Repair traces and refutations through supplied executable exact finite abstractions. |

### Transport, observability and boot applications

| Files | Scope |
|-------|-------|
| [kantorovich_duality.pvs](kantorovich_duality.pvs), [brenier_uniqueness.pvs](brenier_uniqueness.pvs), [cyclical_monotonicity.pvs](cyclical_monotonicity.pvs) | Discrete transport optimality certificates and monotonicity under the stated assumptions. |
| [displacement_interpolation.pvs](displacement_interpolation.pvs), [wasserstein_metric.pvs](wasserstein_metric.pvs), [transport_stability.pvs](transport_stability.pvs) | Interpolation, metric properties and map stability. |
| [global_optimality.pvs](global_optimality.pvs), [unbalanced_regime.pvs](unbalanced_regime.pvs), [transport_ppg.pvs](transport_ppg.pvs) | Segmentation, source/sink regimes and the transport-to-PPG connection. |
| [fisher_atlas.pvs](fisher_atlas.pvs), [observability_geometry.pvs](observability_geometry.pvs), [observability_refinement.pvs](observability_refinement.pvs) | Charts, excitation-dependent observability and quantitative certificate refinements. |
| [lie_generator_structure.pvs](lie_generator_structure.pvs), [dual_observability.pvs](dual_observability.pvs), [tangent_bundle.pvs](tangent_bundle.pvs) | Generator coherence, dual observability and transport tangent structure. |
| [lowrisc_boot_verification.pvs](lowrisc_boot_verification.pvs), [opentitan_boot_instance.pvs](opentitan_boot_instance.pvs) | Layered boot graphs, failure blocking and the declared OpenTitan stage model. |

The standalone [SMT-LIB files](#related) and the
[Sterbenz development](Sterbenz/README.md) have separate proof scopes and tool
requirements.

## Central Theorems

The summaries below omit some type, measurability, locality and model parameters.
The linked PVS files give the complete statements and their assumptions.
Random initialization uses slot zero of the product resampling table; fixed-start
results specify the initial state separately.

### Certification, blocking and probabilistic repair

1. **Canonical certification.**
   [certified_iff_above_canonical](parametric_certification.pvs) characterizes
   certification by `theta_c <= theta` when `theta_c` is canonical. The
   complete-lattice theory proves existence under nonemptiness and infimum closure.

2. **Blocking at the frontier.**
   [canonical_blocking_empty](cert_blocking.pvs) gives an empty blocking set at
   a canonical level; `stricter_has_blocking` gives a failed certificate at a
   target outside that certified upper set.

3. **Component repair non-interference.**
   [repair_noninterference](ppg_bdd_locality.pvs) preserves an obligation in
   another dependency component when the predicates are local and the state
   change stays inside the selected component's footprint.

4. **Moser–Tardos expected work.**
   [randomInitETLog_le_sum](ppg_mt_total_budget.pvs) proves
   **E[T_LOG] <= sum x(a)** under the stated locality, event-probability and
   resampling-budget hypotheses. Finite expected work follows without a
   termination premise.

5. **Pegden and Shearer budgets.**
   [Pegden's expected-work theorem](ppg_pegden_expectation.pvs) replaces the
   product budget by independent-subset sums. The
   [Shearer expected-work theorem](ppg_shearer_total_expectation.pvs) bounds
   **E[T_LOG] by sum q_a/q_empty** under strict Shearer positivity and the
   stated event-probability upper bounds.

### General integrals and exact stochastic models

6. **Integral of the active count.**
   [expectedActiveCount_eq_tsum](ppg_general_active_count.pvs) proves
   **integral count = sum measure(active_n)** for any native measure and a
   countable family of measurable events. Both sides may be infinite; no
   finite-measure, sigma-finiteness or semifiniteness hypothesis is imposed.

7. **Local budget to expected work.**
   [expectedActiveCount_le_of_budget](ppg_general_active_count.pvs) gives
   **expected active count <= budget(0)/delta**, for positive finite `delta`,
   from `delta * measure(active_n) + budget(n+1) <= budget(n)`.
   Budgets may take the value infinity. Under a finite measure,
   [integrated_decrease](ppg_additive_conditional_certificate.pvs) derives
   this inequality from an integrable, adapted, almost-everywhere nonnegative
   potential and its local conditional decrease. The resulting bound is
   **ofReal(integral initial potential)/delta**. For the fixed-start MT
   process, [ETLog_le_of_drift](ppg_mt_fixed_drift.pvs) gives
   **E[T_LOG] <= potential(initial)/delta**. The
   [cost bound](ppg_mt_drift_expected_cost.pvs) multiplies this by a finite
   cap on each active step; the cost function need not be measurable.

8. **Full resampling.**
   [fullResampling_expected_work_eq](ppg_full_resampling_mean.pvs) identifies
   the random-start mean with the extended geometric mean **b/(1-b)**, where
   `b` is the original bad-state probability. At `b = 1` the mean is infinity.
   Positive good-state mass gives finite expected work and almost-sure success.

9. **Exact potential synthesis and expectation.**
   [synthesize_iff_accessible](ppg_finite_potential_accessible.pvs) characterizes
   successful checked synthesis by positive-mass accessibility of good states.
   [ETLog_eq_potential](ppg_exact_mt_fixed.pvs) then identifies the fixed-start
   expectation with the exact rational potential under its accessibility hypothesis.

10. **Exact tails and checked closed bad classes.**
    [TLog_timeout_eq_survival](ppg_tail_mt_fixed.pvs) gives
    **Pr[T_LOG > N] = survival(N,s0)**. Accepted survival rows yield the
    block estimate **Pr[T_LOG > kH] <= b^k**. An accepted closed bad class
    containing the start instead gives an infinite expectation for that kernel.

11. **Exact stopped-count reduction.**
    [hitCount_projection](ppg_update_projection_stopping.pvs) equates concrete
    and reduced stopped counts on the same input stream when updates commute
    with projection and the good-state tests agree. The concrete state space
    need not be finite.

### Feasibility and refutation

12. **Checked finite decisions.**
    [ppg_certified_decision.pvs](ppg_certified_decision.pvs) gives witnesses or
    refutations from exhaustive finite enumeration. The
    [exact-abstraction repair theory](ppg_finite_abstraction_repair.pvs) realizes
    the abstract steps as a concrete repair trace under its realization obligations.
    [Farkas refutations](ppg_farkas_refutation.pvs) check a supplied rational
    certificate under a sound linear model; completeness of certificate search
    is a separate question.

## Theory Layers

The organization follows the companion Lean development, with PVS-specific
support for finite folds, sigma algebras, probability laws and saved proof chains.

### Certification, structure and assessment

Ordered certificates and refinement relations determine the certified region.
Quotients and selection lenses organize equivalent specifications. Blocking,
self-assessment and repair describe failures and recovery while preserving the
chosen contract. The transport and boot theories provide application models.

### Dependency and probabilistic repair

Variable footprints determine dependency components and the locality guarantees
used in repair. Local Lemma criteria give sufficient existence conditions.
Resampling tables, witness trees, canonicalization and occurrence probabilities
then support expected-work and termination theorems for the declared process.
Pegden and Shearer bounds use their own budget hypotheses.

### Witness DAGs and layers

A witness DAG has separate finite node and arc sets over an arbitrary label
type. Validity records supported arcs, acyclicity and orientation of dependent
labels. Reversal preserves validity when the reversed relation is acyclic;
ancestor prefixes preserve validity and canonical occurrence indices.
Longest-path heights are defined by recursion on descendant cardinality. Each
height layer has distinct independent labels, and each positive layer belongs
to the successor family of the preceding layer.

### Integrals and exact stochastic models

The integration layer connects measurable functions to NASAlib's real integral
and to extended nonnegative sums. General active-count integrals retain infinite
event masses. Finite rational kernels add conditional transition laws, checked
potentials, exact means and survival bounds. Lumping preserves these quantities
under transition-mass and good-state compatibility conditions.

### Feasibility, refutation and remaining translations

Finite search and exact abstraction provide concrete repair witnesses or checked
refutations. Minimal cores and correction sets describe infeasible obligation
families. The companion Lean library also contains intersection-sensitive HLS
policy bounds and an infinite-model undecidability result; their PVS translations
remain to be completed.

## Related

- [ppg-lean](https://github.com/gajaka/ppg-lean): the generic Lean 4 development,
  its full module inventory, central theorems and kernel-verification record.
- [CERTIFICATION_README.md](CERTIFICATION_README.md): the earlier certification
  exposition and example workflow. Its historical counts and port-status notes
  predate the current translation.
- [CERT_RUNNER_RESULTS.md](CERT_RUNNER_RESULTS.md): recorded LUCES certificate
  results and the five-level certification example.
- [fisher_boundary_strong.smt2](fisher_boundary_strong.smt2) and
  [brenier_t3_surjective.smt2](brenier_t3_surjective.smt2): standalone Z3 encodings.
  Their unsatisfiability claims concern those encodings, including the finite
  domain used in the Brenier example.
- [Sterbenz/README.md](Sterbenz/README.md): floating-point subtraction through
  the Frama-C/Jessie/PVS pipeline.

## References and scope

The references identify the mathematical sources and the part represented in
the PVS files. Further references appear beside the relevant definitions and
proofs.

### Local Lemmas and Moser–Tardos

- Noga Alon and Joel H. Spencer, *The Probabilistic Method*, fourth edition,
  Wiley, 2016, Lemma 5.1.1 and Section 5.7. The
  [General Local Lemma](ppg_lll.pvs) and
  [expected resampling bound](ppg_mt_total_budget.pvs) use the declared event
  probabilities, dependencies and resampling budgets.
- Robin A. Moser and Gabor Tardos,
  [*A constructive proof of the general Lovász Local Lemma*](https://arxiv.org/abs/0903.0544v3),
  especially Section 2. The PVS development includes the table process,
  witness construction, injectivity and probability bounds used in the counting
  argument.
- David G. Harris,
  [*Lopsidependency in the Moser-Tardos framework: Beyond the Lopsided Lovász Local Lemma*](https://arxiv.org/abs/1610.02420v4),
  Section 1.2, recalls the Erdős–Spencer criterion used by the
  [lopsided theory](ppg_lopsided_probability.pvs).

### Stronger probabilistic bounds

- Wesley Pegden,
  [*An extension of the Moser-Tardos algorithmic local lemma*](https://arxiv.org/abs/1102.2853v2),
  Theorem 1.4. The [PVS expectation theory](ppg_pegden_expectation.pvs) uses the
  independent-subset budget over each closed neighborhood.
- Nicholas J. A. Harvey and Jan Vondrák,
  [*Short proofs for generalizations of the Lovász Local Lemma: Shearer's condition and cluster expansion*](https://arxiv.org/abs/1711.06797v1),
  Section 2, provides the strict Shearer presentation. The expected-work bound
  follows the Kolipaka–Szegedy argument presented in
  [Vondrák's 2018 Lecture 8](https://theory.stanford.edu/~jvondrak/MATH233A-2018/Math233-lec08.pdf).
  See [ppg_shearer_total_expectation.pvs](ppg_shearer_total_expectation.pvs).

- Kun He, Qian Li and Xiaoming Sun,
  [*Moser–Tardos Algorithm: Beyond Shearer’s Bound*](https://arxiv.org/abs/2111.06527v1),
  Definitions 2.1–2.4 and Facts 2.5–2.6. The
  [witness-DAG theory](ppg_hls_witness_dag.pvs) covers reversal and ancestor
  prefixes. The stable-set connection is discussed in Section 1.2.1, footnote 3.
- Nicholas J. A. Harvey and Jan Vondrák,
  [*An Algorithmic Proof of the Lovász Local Lemma via Resampling Oracles*](https://arxiv.org/abs/1504.02044v3),
  Definition 5.2 and Section 5.3.2. The
  [layer theory](ppg_hls_witness_layers.pvs) constructs independent layers
  and proves their closed-neighborhood successor condition. The later HLS
  counting and policy translations remain in progress.

### Integration, potentials and stopping bounds

- Patrick Billingsley, *Probability and Measure*, third edition, Wiley, 1995;
  Sterling K. Berberian, *Fundamentals of Real Analysis*, Springer, 1999.
  The [general integral](ppg_general_simple_integral.pvs) uses weighted measurable
  indicators, and the [count theorem](ppg_general_active_count.pvs) uses monotone
  convergence under a finite bound inside an arbitrary-measure argument.
- Johannes Lengler, [*Drift Analysis*](https://arxiv.org/abs/1712.00964v2),
  Theorem 1, gives the additive-drift background. The
  [conditional certificate](ppg_additive_conditional_certificate.pvs)
  integrates the local decrease; the
  [MT certificate](ppg_mt_conditional_certificate.pvs) applies it to the
  actual stopped potential under the original product-log law. The
  [execution-cost bound](ppg_mt_drift_expected_cost.pvs) combines the
  resulting expected count with a cap on each active-step charge.
- Michael Mitzenmacher and Eli Upfal,
  [*Probability and Computing*, second edition](https://doi.org/10.1017/9781316651124),
  Section 7.1.1 and Exercise 7.25; David A. Levin and Yuval Peres,
  [*Markov Chains and Mixing Times*, second edition](https://pages.uoregon.edu/dlevin/MARKOV/mcmt2e.pdf),
  Exercise 10.22 and the uniform-block argument in Lemma 1.13. These support
  the [exact MT expectations](ppg_exact_mt_fixed.pvs) and
  [stopping bounds](ppg_tail_mt_fixed.pvs).
- Levin and Peres, Section 2.3.1, Lemma 2.5 and equation (2.10), is the background
  for [finite lumping](ppg_finite_lumping_paths.pvs). The
  [commuting-update reduction](ppg_update_projection_stopping.pvs) also permits
  an infinite concrete state space.

### Application models and publications

Cédric Villani, *Optimal Transport: Old and New*, Springer, 2009, is a source
for the discrete transport certificate models. The application theories state
their finite domains, feasibility conditions and empirical assumptions explicitly.

The LUCES experimental background is described in:

- [*Empirical Information Geometry on an Embedded Adaptive Lighting System: Multi-Chart Manifold Transitions Under Signal Collapse*](https://zenodo.org/records/20094759) (2026).
- [*Excitation-Dependent Observability Geometry on an Embedded Adaptive Lighting Manifold*](https://zenodo.org/records/20389804) (2026).
- [*Optimal Transport Geometry of Natural Spectral Regime Transitions*](https://zenodo.org/records/21956336) (2026).

## Future work

General conditional expectation is proved. The additive-drift,
Moser–Tardos drift and execution-cost source modules are translated
and replayed. The witness-DAG reversal, ancestor-prefix and longest-path layer
modules are also replayed. The next proof work covers their stable and canonical
encodings and the policy bounds built on them, followed by the computability
limit for the encoded infinite repair family. Existing core translations also
need further source-by-source semantic review and replay accounting.

For the controller application, live measurements need a defined interpretation
in the formal state, and the running checker must evaluate the corresponding
predicates correctly. Control actions need proved restoration and preservation
properties. Native execution, timing and physical response require their own
evidence alongside the graph and stochastic process results.

The finite procedures use exhaustive search or supplied exact abstractions.
Finding useful abstractions, repair witnesses and checked potentials efficiently
remains practical work. Failure of a sufficient probabilistic criterion leaves
repairability unresolved unless a separate refutation is available.

## Author

Dragan Stosic, MSc — [NASA PVS Libraries contributor](https://github.com/nasa/pvslib/blob/master/sets_aux/rr_rel.pvs)

## License

© 2026 Dragan Stosic. All rights reserved.

This work (theories, proofs, and source) is made available for reading, academic study, and non-commercial research use, with attribution. Redistribution, modification, derivative works, or any commercial use require prior written permission. If you are interested in using this work, including in a commercial or product setting, please get in touch: dragan.stosic@gmail.com
