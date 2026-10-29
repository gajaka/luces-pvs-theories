# Proof-Preserving Graphs: Formal Certification, Self-Assessment, and Repair (PVS)

This PVS development studies graded certification, blocking and repair. It
contains the original PPG and LUCES application theories, together with the
translation of the generic [Lean 4 library](https://github.com/gajaka/ppg-lean).
The application theories describe transport, observability and secure-boot
models; the generic theory keeps the data, specifications and repair actions
abstract.

As of **2026-10-24**, the translation has independently replayed
counterparts for **1,824 of 1,824 Lean source theorems and lemmas**, with all recorded
results checked in **191 of 191 modules**. Supporting PVS lemmas and
type-correctness conditions are additional obligations and are excluded from
those source-result counts.

The 2026-10-28 theorem-scope cleanup removes the translated `THEOREM TRUE`
placeholder and replaces four weak repair statements with before/after
properties of an explicit local value update. A new restoration theorem keeps
the total Lean source declaration count at 1,824. The order-preservation helper
is now named `linear_cert_le_of_le` in both quotient developments. See the
[theorem-scope note](docs/THEOREM_SCOPE.md) for the fixed-specification model and
the targeted proof checks. The dated full-library results above remain the
historical translation record.

Further structural corrections on **2026-10-28** add a bridge from actual
certificate families to dependency components and the state-repair contract,
connect meta refinement to the core RR definition, and establish categorical
quotients under explicit noncollapse and descent conditions. An operational MT
bridge follows the supplied directed edges under a primitive-step contract.
These are scoped extensions of the historical translation, with their own proof
replay. The application
corrections replace the finite transport reconstruction assumption, derive
regime tests from calibrated arithmetic and use a directed boot policy. See the
[scope and verification details](docs/THEOREM_SCOPE.md#structural-and-application-corrections).

The subsequent finite-read integration retains repeated certificate positions
and derives read locality from checker syntax. Its measured LUCES instance
searches a fixed bank of candidate coupling snapshots while preserving the
signed GEN observation and dataset identity. The associated Lean inventory is
now **1,876 results in 198 modules**; this is a Lean declaration count, not a new
whole-library PVS replay count. The revised LUCES theories use explicit finite
models, checked model laws and measured numerical inputs in place of the
earlier hand-written axioms. Read the [LUCES model scope](docs/LUCES_MODEL_SCOPE.md)
for the established claims and the remaining implementation and physical
boundaries.

The finite-read integration receipt, completed on **2026-10-29**, covers
**28 changed `.pvs` files and 30 changed `.prf` files**: 27 semantic source
changes, one equivalent PVS-generated ADT rendering and three additional
proof-only repairs. Ten completed normal replay reports cover all 30
proof-bearing source roots and their loaded Project and required Native
dependencies. Eight existing passes were reused after checking their actual
loaded source/proof hashes against the publication. The two new passes replayed
**723 Project + 956 Native bodies** for the proof repairs and
**17 Project + 761 Native bodies** for the Shannon example, with no unfinished
bodies or missing scripts. These counts overlap. See the
[incremental verification receipt](reports/PVS_INCREMENTAL_REPLAY_20261029.json).

The same record includes successful typechecking of all 1,121 selected files.
The later whole-library
proof replay was stopped when the requested scope changed to modified and
affected theories; it is not reported as a new whole-library proof pass.
The source dependency and qualified-reference checks found no additional
unchanged consumers of the 27 semantic changes. The generated ADT change only
expands the binder `(x,y:T)` to `(x:T,y:T)` and removes three blank lines;
its parent datatype is unchanged.

A subsequent [walk-geometry extension](docs/THEOREM_SCOPE.md#curvature-extracted-from-certified-walks)
computes angular curvature from ordered vertex coordinates. Its certificate
requires `pp_path`, active steps and enough samples; the Lie interface
binds the reported curvature to that calculation. A graph extension preserves
the same certified path, while a concrete newly admitted bent path fails its
zero-curvature certificate. This does not certify C20 transport couplings or
floating-point agreement with the recorded boot observations.

That revision's completed [targeted replay](reports/PVS_WALK_GEOMETRY_20261029.json) covers
both entry points and their dependencies: **90 Project bodies and 757 required
Native originals**, all proved by the ordinary public checker on 2026-10-29.
These are proof-body counts including supporting lemmas and TCCs, not an
addition to the historical Lean translation count.

A later endpoint-coherence extension computes both reported fields from the
same ordered walk. The report checker verifies that equality as well as the
PPG and numerical certificate conditions. A three-sample curvature identity
and a computed four-sample counterexample describe the relation between these
two quantities. Endpoint-direction coherence is distinct from C20; captured
C20 data and its finite checks now have their own legacy observation theory.
See the [coherence scope](docs/THEOREM_SCOPE.md#endpoint-direction-coherence-and-the-curvature-relation).

The [endpoint-coherence replay](reports/PVS_WALK_COHERENCE_20261029.json)
passed all three entry points and their loaded dependencies on 2026-10-29:
**138 Project bodies and 761 required original Native bodies**, with no
unfinished obligations or Native failures. Supporting lemmas and TCCs are
included; these counts are not a new Lean translation inventory.

## Directory layout

The generic theories are grouped by subject. A theory keeps its original name,
and its saved `.prf` file stays beside its `.pvs` source. Imports between groups
name the corresponding PVS library explicitly.

| Directory | Contents |
|-----------|----------|
| [theories/foundations/](theories/foundations/) | Finite sets, lists, sums, products, order, encodings and rational linear algebra. |
| [theories/ppg_core/](theories/ppg_core/) | Proof-preserving graphs, morphisms, dependency components, refinement and repair relations. |
| [theories/certification/](theories/certification/) | Certificate families, ordered levels, quotients, selection, blocking and self-assessment. |
| [theories/measure_probability/](theories/measure_probability/) | Measurable spaces, extended nonnegative values, probability laws, products, integrals and conditional expectations. |
| [theories/witness_trees/](theories/witness_trees/) | Ordered witness trees, addresses, canonical encodings and weights. |
| [theories/moser_tardos/](theories/moser_tardos/) | Resampling processes, trajectories, witness probabilities, expected work and termination. |
| [theories/local_lemmas/](theories/local_lemmas/) | General, lopsided and variable Local Lemmas; Pegden and Shearer bounds. |
| [theories/hls/](theories/hls/) | HLS witness DAGs, stable encodings, coin laws, scheduling policies and repair bounds. |
| [theories/finite_models/](theories/finite_models/) | Exact stochastic updates, finite-state kernels, drift certificates, stopping, lumping and model reduction. |
| [theories/decision/](theories/decision/) | Feasibility checks, finite abstractions, unsatisfiable cores, Farkas certificates and refutations. |
| [theories/computability/](theories/computability/) | Primitive and partial recursion, program encodings, enumeration and undecidability. |
| [applications/luces/](applications/luces/) | Transport, Fisher geometry, observability and Lie-generator models. |
| [applications/boot/](applications/boot/) | The lowRISC and OpenTitan boot models. |

[Sterbenz/](Sterbenz/) retains its own floating-point development and library
requirements. Standalone SMT-LIB examples are in [smt/](smt/), supporting reports
in [docs/](docs/), and verification commands in [scripts/](scripts/).

## Typechecking and proof replay

The recorded translation checks use **PVS 8.1.2**,
[NASA's PVS libraries](https://github.com/nasa/pvslib) and the `proveit` batch
driver, version `8.1-20260706`. The libraries must be available through
`PVS_LIBRARY_PATH`; its entries are directories containing libraries such as
`measure_integration`, `sets_aux` and `graphs`. From the repository root, include
the project library directories as well when using interactive PVS or `proveit`:

```sh
export PVS_LIBRARY_PATH="$PWD/theories:$PWD/applications:/path/to/pvs/nasalib:/path/to/pvs/lib"
```

The bundled `lib` directory supplies required original proof inputs such as
`finite_sets`; it is distinct from NASAlib. Before replaying the logarithm and
entropy dependencies with PVS 8.1.2, check the versioned
[NASAlib proof-metadata compatibility bundle](library-proof-fixes/README.md):

```sh
python3 scripts/apply_library_proof_fixes.py \
  --nasalib-root /path/to/pvs/nasalib --check
```

If the check identifies supported original files, apply the documented changes
with `--apply` while no PVS session uses that library, then repeat `--check`.
Unknown source or proof versions are rejected. The bundle covers 130 exact
decision-procedure metadata slots in 44 files, preserving verified originals
and all theorem statements, proof programs and dependency lists. Applying it
is setup, not proof replay.

PVS loads the project startup file [theories/.pvs.lisp](theories/.pvs.lisp)
from that library path. It uses the standard setting that prevents recursive
binary-cache serialization across the project libraries.

The recorded full-replay V2 input snapshot is pinned to the official
[`nasa/pvslib` commit `f3bb2b36240ff3413136b2a46e431c47350fe108`](https://github.com/nasa/pvslib/commit/f3bb2b36240ff3413136b2a46e431c47350fe108),
plus the earlier single-slot `integral_split_scaf` metadata fix. An audit of all
2,502 tracked `.pvs` and 2,242 tracked `.prf` files found no other differences
from that commit. A later slot-aware audit identified the other 43 files in
the expanded compatibility bundle. Its 44-file sandbox validation establishes
metadata, source and proof-program preservation; it does not replay their
Native proofs. The frozen V2 inputs still contain only the earlier integral
fix. Results for a dependency closure using further metadata fixes must be
reported separately. These input copies do not contain the private
proof-program repairs used in the older historical checks below. See the
[library setup instructions](library-proof-fixes/README.md).

Each `.pvs` file contains specifications and theorem statements. Its `.prf`
companion contains saved proofs. Typechecking checks expressions and generates
type-correctness conditions (TCCs); replaying the proofs checks those conditions
and the theorem bodies. A successful typecheck alone does not establish the
theorems.

From the repository root, typecheck one file without replaying its proofs:

```sh
python3 scripts/check.py --typecheck \
  --file theories/measure_probability/ppg_general_active_count.pvs
```

Replay the saved proofs of that file and its imported project theories:

```sh
python3 scripts/check.py \
  --file theories/measure_probability/ppg_general_active_count.pvs
```

Select one subject group or the whole generic and application development:

```sh
python3 scripts/check.py --group hls
python3 scripts/check.py --all --timeout 180
```

The runner uses Python 3.9 or later and the installed PVS executable. It sets
up the project library paths, copies sources and saved proofs into a separate
workspace, and writes logs and a machine-readable report outside the repository.
`--report-dir` selects a new report directory. Proof replay runs the project
proofs and the library obligations they use, with oracles disabled and without
installing ProofLite scripts. Project and library calls have separate counts.
A successful run requires complete proof chains, including imported obligations
and relevant TCCs.

The default is one PVS worker. `--jobs 2` uses two independent workspaces;
`--timeout` sets the time limit for each proof; the full-run example allows
180 seconds. `--heap-mib` sets each worker's Lisp heap. To inspect the selected
files without starting PVS, use `--all --list` or `--group hls --list`.

`--all` selects `theories/` and `applications/`. It leaves [Sterbenz/](Sterbenz/)
out because that development has separate floating-point library requirements.
Select it explicitly with `--group Sterbenz` after configuring those libraries;
see its [README](Sterbenz/README.md). The SMT-LIB examples in [smt/](smt/) use
separate tools.

To replay just one named theorem with `proveit`, use a separate checkout and
run from its theory's directory. Configure `PVS_LIBRARY_PATH` from that
checkout's root as above, then run:

```sh
REPORT_DIR="$(mktemp -d)"
cd theories/measure_probability
proveit --no-scripts --no-purge --disable-oracles --force --log \
  --dir "$REPORT_DIR" --out active-count-equality \
  @ppg_general_active_count.expectedActiveCount_eq_tsum
```

The single-theorem command does not replay its imported proof bodies.

The directory reorganization was verified on **2026-10-25**. All **1,116 selected
source files typecheck**, and **12,853 distinct proof bodies reached QED**:
**11,159 project bodies and 1,694 Native library bodies**, including TCCs.
The proofs ran in one PVS process with a 24,000 MiB Lisp heap. A full project
pass was followed by targeted replay of 37 repaired proof programs across
29 `.prf` files and additional rounds of required original Native bodies.
Final checks passed for ordinary proof status, mapped originals, proof chains
and dependency closure, with oracles disabled. Part of the final dependency
audit used a separately tested hash-based traversal; proof programs and stored
results were unchanged. The public runner was checked separately on isolated
fixtures. The separate `Sterbenz/` development is outside
this run.

Historical translation checks on 2026-10-18 through 2026-10-24 include:

| Check | Result |
|-------|--------|
| General active-count integral and positive-drift budget | 318/318 project obligations complete across 32 theories, including all 87 new obligations. |
| Full resampling, complete dependency graphs and drift-region support | 2,216/2,216 project obligations complete, including 172 new obligations. |
| Native measure and integration support | 1,109 library proof bodies freshly forced over three disjoint rounds, with ordinary complete proof chains. The certificate includes general monotone convergence and the weighted-measure support. |
| Augmented HLS sample space and expectation transport | 960/960 project obligations complete, including all 177 new obligations and five source results; 1,204 Native obligations freshly replayed in the same cold PVS process, including 453 additional original-library bodies. |
| General conditional expectation | 600/600 project obligations complete across 52 theories, including all 52 new obligations. |
| General drift, Moser–Tardos certificates and execution cost | 2,241/2,241 project obligations complete across 230 theories, including all 69 new obligations and 14 source results. |
| Generic repair, growing lists and meta refinement | 80/80 project obligations complete across 10 theories, including 13 new obligations and 30 source results. |
| Acyclic relation reversal | 24/24 project obligations complete across 1 theory, including 24 new obligations and 9 source results. |
| Witness DAGs and ancestor prefixes | 61/61 project obligations complete across 2 theories, including 37 new obligations and 15 source results. |
| Longest-path heights and independent layers | 183/183 project obligations complete across 14 theories, including 33 new obligations and 14 source results. |
| Pointwise complementary slackness | 5/5 new obligations complete, covering 5 source results. |
| Certification equivalence and selection | 42/42 project obligations complete, including 7 new obligations and 4 source results. |
| Stable-sequence encodings and products | 429/429 project obligations complete across 42 theories, including 32 new obligations and 14 source results. |
| General self-assessment | 47/47 project obligations complete across 3 theories, including 12 new obligations and 12 source results. |
| Canonical witness-DAG reconstruction | 437/437 project obligations complete across 38 theories, including 24 new obligations and 9 source results. |
| Countable labels and finite witness DAGs | 108/108 project obligations complete across 8 theories, including 8 new supporting obligations; no additional source-theorem credit. |
| Finite-list certificates, lattice instances and blocking | 63/63 project obligations complete across 7 theories, including 37 new obligations and 31 source results. |
| Certification as self-assessment | 75/75 project obligations complete across 7 theories, including 9 new obligations and 8 source results. |
| Specification quotients and graph projection | 88/88 project obligations complete across 8 theories, including 45 new obligations and 31 source results. |
| Canonical proper witness-DAG weight budget | 564/564 project obligations complete across 57 proof-bearing theories from 58 source files, including 14 new obligations and 7 source results. |
| Representative selection and finite-list lenses | 75/75 project obligations complete across 6 theories, including 37 new obligations and 23 source results. |
| General numerical feasibility and dependent-domain resampling | 36/36 project obligations complete across 5 theories, including 12 new obligations and 9 source results. |
| Ordered witness DAGs and reversal | 105/105 project obligations complete across 6 theories, including 29 new obligations and 7 source results. |
| General Local Lemma | 407/407 project obligations complete across 39 theories, including 48 new obligations and 30 source results; 412 Native library obligations freshly replayed in the same cold PVS process. |
| Constructed topological node order | 191/191 project obligations complete across 15 theories, including 8 new obligations and 7 source results. |
| Computability limit for infinite repair models | 935/935 project obligations complete across 50 proof-bearing theories, including 144 new obligations and all 14 source results. The run includes 66 TCCs and uses no Native library proof bodies. |
| General double-sampling and Moser–Tardos intersection | 897/897 project obligations complete across 77 theories, including all 13 source results; 683 Native library obligations freshly replayed in the same cold PVS process. Measurable double, joint and forward events, product-measure identities and intersection bounds. |
| Final HLS probability, expectation and repair translation | **5,489/5,489 saved proof bodies complete (1,228 Native and 4,261 project)**. Proofs ran in one PVS process with a 24,000 MiB heap. The initial group replayed 4,656 bodies (1,228 Native and 3,428 project); later groups checked further supporting dependencies, each with its own records from before its proofs. The current comparison covers 593 theory headers. These checks include 869 new obligations across 74 theories and the remaining 97 source results. **Current proof chains, dependency closure, source declarations and physical origins checked**. |

These recorded runs precede the directory reorganization. They checked saved
proofs in isolated workspaces, with project declarations and saved proof programs
matching the versions committed at the time. The separately checked native
library sources and proofs were hashed before and after reuse. A completed run
requires `proved - complete`, including the relevant TCCs and dependencies.
The Local Lemma run starts from a source-only private library copy and freshly
checks 412 selected Native obligations. The larger 1,109-obligation support
certificate is recorded separately.
The augmented-space run replays 751 of those original library bodies and 453
additional bodies from the unchanged library sources and saved proofs. Both
product-law projections and transport of the existing extended expected work
are checked in that run.

The historical HLS and directory-reorganization checks used a local NASAlib copy with
proof-script repairs for `series.convergent_abs`,
`absconv_series_aux.nonneg_series_inj_conv` and `measure_space.simple_def3`.
The directory check also uses focused proof programs for five obligations in
`real_lebesgue_scaf`: `lebesgue_outer_measure_singleton`,
`lebesgue_outer_measure_le_length`, `lebesgue_outer_measure_TCC1`,
`outer_measurable_open_semi_infinite` and `lebesgue_measure_TCC1`, together
with `lebesgue_def.lambda_closed_ball`. Library statements and source files
were unchanged. Those historical proof-program repairs are separate from the
published [metadata compatibility fix](library-proof-fixes/README.md); that fix
does not install the older repairs. The runner records the hashes of the
external sources and proofs it actually copies in `inputs.json`; a check of
another library copy uses that copy's proof programs.

The table reports the earlier translation checks. The reorganization check
above separately covers the selected legacy applications as well as the generic
theories; it excludes `Sterbenz/`.

The generic theories, boot models and current `applications/luces/` sources
contain no hand-written `AXIOM` declarations. Healthy self-repair requires an explicit reflexivity hypothesis.
The weighted model states the cost laws as hypotheses and defines path cost
as the sum of consecutive edge costs.

The `_adt.pvs` files generated from `ppg_wtree` and `ppg_partrec_code`
contain PVS's datatype axioms for constructors, selectors, induction and
well-founded recursion. These belong to the datatype representation; they do
not assume the Local Lemma, Moser--Tardos or convergence results.

Removing the earlier LUCES axioms involved changing the models and their claims.
For example, finite Kantorovich results check normalized marginal feasibility,
dual feasibility and complementary slackness; they do not assume that arbitrary
empirical prices satisfy those checks. The Lie-generator models evaluate the
same numeric fields as their boolean screens and include counterexamples to
the former universal implications. Other theories explicitly require metric,
geodesic, chart or experiment laws. A theorem under a checked law package is
conditional on that package; absence of `AXIOM` declarations does not establish
an end-to-end theorem about a physical controller. See
[LUCES model scope](docs/LUCES_MODEL_SCOPE.md).

The revised `tangent_bundle`, `transport_ppg` and `unbalanced_regime` files
contain no hand-written axioms. Their contracts use explicit function laws,
measured certificate inputs or calibrated numerical inequalities. The finite
tangent contract includes a concrete consistency witness and a counterexample
to universal finite reconstruction; it does not construct a Wasserstein tangent
bundle. The directed boot instance takes signature, hash and policy checks as
inputs and proves reachability properties of that policy, without claiming to
verify cryptographic implementations or actual OpenTitan firmware.

The separate `Sterbenz/` development also contains axiomatic models generated
by Jessie/Why3. A successful proof replay establishes the theorems under the
axioms and hypotheses in scope; it does not prove the axioms themselves.

The hand-written-axiom cleanup was checked on **2026-10-26** across six
changed or importing source files: **139 project proof bodies and 13 required
NASAlib proof bodies** passed from a cold source/proof copy, with complete
dependency chains and oracles disabled. The checker replays required original
library proofs before inspecting their dependency records. This refreshes
anonymous imported judgement references that some older saved proofs cannot
resolve when first loaded. Library statements and proof programs are unchanged.

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
other components. The full-family bridge includes already passing certificates
in its component footprints. Checked component updates instantiate the actual
state-repair contract, and a checked finite plan covering the initial blockers
establishes full certification. Locality, frames and component post-checks
remain explicit obligations.

A repair changes the state while keeping the target specification fixed. Its
obligations are to restore the target and preserve prior certification. The
framework distinguishes the existence of a repair path, almost-sure success of
a random procedure and a bound on its expected work.

The probabilistic development now includes the original Moser–Tardos
expected-work bound **E[T_LOG] <= sum x(a)** for product-table random
initialization, followed by finite-expectation and
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
[certificate-runner report](docs/CERT_RUNNER_RESULTS.md) contains the concrete
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
| [proof_preserving_graphs.pvs](theories/ppg_core/proof_preserving_graphs.pvs), [pp_graphs_extended.pvs](theories/ppg_core/pp_graphs_extended.pvs) | Validity, paths, evolution, invariants and graph extensions. |
| [categorical_pp_graphs.pvs](theories/ppg_core/categorical_pp_graphs.pvs), [directed_pp_graph.pvs](theories/ppg_core/directed_pp_graph.pvs) | Morphisms, embeddings, quotients and directed graph structure. |
| [ppg_parametric_core.pvs](theories/certification/ppg_parametric_core.pvs), [ppg_certificate_lattice.pvs](theories/certification/ppg_certificate_lattice.pvs), [ppg_certificate_complete.pvs](theories/certification/ppg_certificate_complete.pvs), [ppg_threshold_certificates.pvs](theories/certification/ppg_threshold_certificates.pvs) | Actual finite lists of monotone certificates over arbitrary data and level types; canonical levels, lattices and real thresholds. |
| [ppg_list_quotient.pvs](theories/certification/ppg_list_quotient.pvs), [ppg_list_quotient_lattice.pvs](theories/certification/ppg_list_quotient_lattice.pvs), [ppg_list_quotient_linear.pvs](theories/certification/ppg_list_quotient_linear.pvs), [ppg_list_quotient_bridge.pvs](theories/certification/ppg_list_quotient_bridge.pvs) | Full certification classes, quotient order and meet; edge-or-collapse generally, with a categorical quotient on certified subgraphs under noncollapse. |
| [ppg_generic_selection.pvs](theories/certification/ppg_generic_selection.pvs), [ppg_selection_lenses.pvs](theories/certification/ppg_selection_lenses.pvs), [ppg_selection_quotient_graph.pvs](theories/certification/ppg_selection_quotient_graph.pvs) | Morphism-pair families, finite lenses, descended invariant/RR and categorical projection under explicit noncollapse and descent hypotheses. |
| [ppg_list_blocking.pvs](theories/certification/ppg_list_blocking.pvs), [ppg_generic_self_assessment.pvs](theories/certification/ppg_generic_self_assessment.pvs), [ppg_list_assessment_bridge.pvs](theories/certification/ppg_list_assessment_bridge.pvs) | Failed certificates, general repair obligations and the complete assess, repair and recertify cycle. |
| [parametric_certification.pvs](theories/certification/parametric_certification.pvs) | Earlier predicate-family certification presentation and its lattice and threshold instances. |
| [cert_quotient.pvs](theories/certification/cert_quotient.pvs), [cert_selection.pvs](theories/certification/cert_selection.pvs), [cert_quotient_bridge.pvs](theories/certification/cert_quotient_bridge.pvs) | Certification equivalence, quotient order and hierarchical selection. |
| [cert_blocking.pvs](theories/certification/cert_blocking.pvs), [ppg_self_assessment.pvs](theories/certification/ppg_self_assessment.pvs), [ppg_assessment_bridge.pvs](theories/certification/ppg_assessment_bridge.pvs) | Blocking diagnostics, failure containment and certification after repair. |
| [pp_graph_repair.pvs](theories/ppg_core/pp_graph_repair.pvs), [ppg_repair_semantics.pvs](theories/ppg_core/ppg_repair_semantics.pvs) | Repair relations, restoration and preservation obligations. |
| [ppg_refinement_meta.pvs](theories/ppg_core/ppg_refinement_meta.pvs) | Core RR correspondence, compatibility from underlying relation inclusion and correctness transport under supplied compatibility. |
| [ppg_complementary_slackness.pvs](theories/certification/ppg_complementary_slackness.pvs) | Pointwise pair inequalities and Monge-map certificates over arbitrary index types, under their explicit hypotheses. |

### Dependency and probabilistic repair

| Files | Scope |
|-------|-------|
| [ppg_bdd.pvs](theories/ppg_core/ppg_bdd.pvs), [ppg_bdd_locality.pvs](theories/ppg_core/ppg_bdd_locality.pvs), [ppg_bdd_cost.pvs](theories/ppg_core/ppg_bdd_cost.pvs) | Shared-variable components, repair non-interference and component costs. |
| [ppg_certification_dependency.pvs](theories/certification/ppg_certification_dependency.pvs) | Actual certificate-family blockers, full-family protection, the state-repair contract and checked finite repair plans. |
| [ppg_generic_probabilistic.pvs](theories/local_lemmas/ppg_generic_probabilistic.pvs), [ppg_dependent_resampling.pvs](theories/moser_tardos/ppg_dependent_resampling.pvs) | Numerical LLL budget feasibility and discriminant-based budget infeasibility; resampling identities for per-variable domains. No semantic irreparability follows from budget failure. |
| [ppg_lll_event_splits.pvs](theories/local_lemmas/ppg_lll_event_splits.pvs), [ppg_lll_pass_measurable.pvs](theories/local_lemmas/ppg_lll_pass_measurable.pvs), [ppg_lll_source_probability.pvs](theories/local_lemmas/ppg_lll_source_probability.pvs), [ppg_lopsided_probability.pvs](theories/local_lemmas/ppg_lopsided_probability.pvs) | Current general and lopsided Local Lemma criteria, event splits, measurable avoidance and the denominator telescope under its strict-subset induction hypothesis. |
| [ppg_mt_random_process.pvs](theories/moser_tardos/ppg_mt_random_process.pvs), [ppg_mt_trajectory_measurable.pvs](theories/moser_tardos/ppg_mt_trajectory_measurable.pvs) | Product-table trajectories, local counters and measurability. |
| [ppg_mt_growing.pvs](theories/moser_tardos/ppg_mt_growing.pvs), [ppg_mt_injectivity.pvs](theories/moser_tardos/ppg_mt_injectivity.pvs), [ppg_rose_canonical_enum.pvs](theories/witness_trees/ppg_rose_canonical_enum.pvs) | Witness construction, injective occurrence encodings and canonical trees. |
| [ppg_mt_check_probability.pvs](theories/moser_tardos/ppg_mt_check_probability.pvs), [ppg_mt_total_budget.pvs](theories/moser_tardos/ppg_mt_total_budget.pvs) | Witness probabilities, occurrence counts and the expected-work bound. |
| [ppg_mt_termination.pvs](theories/moser_tardos/ppg_mt_termination.pvs), [ppg_mt_budget_repair.pvs](theories/moser_tardos/ppg_mt_budget_repair.pvs) | Almost-sure termination and the repair reachability bridge. |
| [ppg_mt_topology_bridge.pvs](theories/moser_tardos/ppg_mt_topology_bridge.pvs) | Actual finite directed recovery paths under primitive-step compatibility; intermediate states may violate the target. |
| [ppg_pegden_expectation.pvs](theories/local_lemmas/ppg_pegden_expectation.pvs), [ppg_pegden_termination.pvs](theories/local_lemmas/ppg_pegden_termination.pvs) | Independent-subset budgets, expected resamplings and termination. |
| [ppg_shearer_total_expectation.pvs](theories/local_lemmas/ppg_shearer_total_expectation.pvs), [ppg_shearer_component_integral.pvs](theories/local_lemmas/ppg_shearer_component_integral.pvs) | Strict Shearer expected-work bounds and component integrals. |
| [ppg_general_double_sample.pvs](theories/measure_probability/ppg_general_double_sample.pvs), [ppg_general_forward_event.pvs](theories/measure_probability/ppg_general_forward_event.pvs), [ppg_intersection_events.pvs](theories/measure_probability/ppg_intersection_events.pvs), [ppg_native_double_measurable.pvs](theories/measure_probability/ppg_native_double_measurable.pvs), [ppg_native_intersection_measurable.pvs](theories/measure_probability/ppg_native_intersection_measurable.pvs), [ppg_probability_double_sample.pvs](theories/measure_probability/ppg_probability_double_sample.pvs), [ppg_probability_intersection.pvs](theories/measure_probability/ppg_probability_intersection.pvs) | General double-sample and intersection events, their measurability and measure identities, and probability bounds. |

### HLS witness DAGs

| Files | Scope |
|-------|-------|
| [ppg_hls_fair_orientation.pvs](theories/hls/ppg_hls_fair_orientation.pvs), [ppg_hls_augmented_space.pvs](theories/hls/ppg_hls_augmented_space.pvs), [ppg_hls_augmented_expectation.pvs](theories/hls/ppg_hls_augmented_expectation.pvs) | Tagged data and fair orientation coordinates, measurable projections, both full product-law pushforwards, and preservation of the existing random-start expected work, including infinity. |
| [ppg_hls_reversal.pvs](theories/hls/ppg_hls_reversal.pvs) | Reversible arcs of arbitrary acyclic relations. |
| [ppg_hls_ordered_dag.pvs](theories/hls/ppg_hls_ordered_dag.pvs), [ppg_hls_ordered_reversal.pvs](theories/hls/ppg_hls_ordered_reversal.pvs) | Witness orders, orientation and reversal under their local order hypotheses. |
| [ppg_hls_topological_order.pvs](theories/hls/ppg_hls_topological_order.pvs) | A constructed strict total node order for finite label universes, with longest-path height and an intrinsic label numbering. |
| [ppg_hls_witness_dag.pvs](theories/hls/ppg_hls_witness_dag.pvs) | Finite witness DAGs, unique sinks, reversal and ancestor prefixes. |
| [ppg_hls_witness_layers.pvs](theories/hls/ppg_hls_witness_layers.pvs), [ppg_finite_nat_sup.pvs](theories/foundations/ppg_finite_nat_sup.pvs), [ppg_nat_rank_well_founded.pvs](theories/foundations/ppg_nat_rank_well_founded.pvs) | Constructed longest-path heights, independent layers and their successor relation. |
| [ppg_hls_stable_encoding.pvs](theories/hls/ppg_hls_stable_encoding.pvs), [ppg_hls_encoding_product.pvs](theories/hls/ppg_hls_encoding_product.pvs), [ppg_hls_encoding_weight.pvs](theories/hls/ppg_hls_encoding_weight.pvs) | Stable layer sequences, finite products in arbitrary commutative monoids, and equality of real node and sequence weights. |
| [ppg_hls_canonical_encoding.pvs](theories/hls/ppg_hls_canonical_encoding.pvs) | Recovery of canonical node indices, nodes and arcs from the stable encoding. |
| [ppg_finite_set_nat_code.pvs](theories/foundations/ppg_finite_set_nat_code.pvs), [ppg_hls_dag_countable.pvs](theories/hls/ppg_hls_dag_countable.pvs) | Injective natural-number codes for finite sets and witness DAGs when the label type has such a code. |
| [ppg_hls_proper_family.pvs](theories/hls/ppg_hls_proper_family.pvs), [ppg_hls_witness_budget.pvs](theories/hls/ppg_hls_witness_budget.pvs), [ppg_nonneg_injective_bound.pvs](theories/measure_probability/ppg_nonneg_injective_bound.pvs) | Weight-preserving injection of canonical proper DAGs into stable sequences and unrestricted Shearer weight budgets. |
| [ppg_hls_coin_query_law.pvs](theories/hls/ppg_hls_coin_query_law.pvs), [ppg_hls_coin_saving.pvs](theories/hls/ppg_hls_coin_saving.pvs), [ppg_hls_relative_coins.pvs](theories/hls/ppg_hls_relative_coins.pvs) | Exact queried coin laws, pair savings and relative orientations. |
| [ppg_hls_process_footprint.pvs](theories/hls/ppg_hls_process_footprint.pvs), [ppg_hls_block_intersection_sets.pvs](theories/hls/ppg_hls_block_intersection_sets.pvs), [ppg_hls_block_intersection_results.pvs](theories/hls/ppg_hls_block_intersection_results.pvs) | Footprint decomposition, joined states, raw intersection-event identities and their probability bounds. |
| [ppg_hls_pair_block_queries.pvs](theories/hls/ppg_hls_pair_block_queries.pvs), [ppg_hls_pair_probability.pvs](theories/hls/ppg_hls_pair_probability.pvs) | Disjoint table queries, four-block product laws and intersection savings. |
| [ppg_hls_augmented_pair_saving.pvs](theories/hls/ppg_hls_augmented_pair_saving.pvs), [ppg_hls_augmented_dependence.pvs](theories/hls/ppg_hls_augmented_dependence.pvs), [ppg_hls_unit_probability.pvs](theories/hls/ppg_hls_unit_probability.pvs) | Augmented pair events, coordinate dependence, independent units and their exact probabilities. |
| [ppg_hls_refined_probability.pvs](theories/hls/ppg_hls_refined_probability.pvs), [ppg_hls_root_union_measure.pvs](theories/hls/ppg_hls_root_union_measure.pvs), [ppg_hls_root_family_weight.pvs](theories/hls/ppg_hls_root_family_weight.pvs) | Selected-pair discounts, refined DAG weights, rooted-family occurrence bounds and unrestricted weight sums. |
| [ppg_hls_policy_count_bound.pvs](theories/hls/ppg_hls_policy_count_bound.pvs), [ppg_hls_policy_expectation.pvs](theories/hls/ppg_hls_policy_expectation.pvs), [ppg_hls_expectation.pvs](theories/hls/ppg_hls_expectation.pvs) | Policy counts, extended expected work, finite-budget bounds and almost-sure termination. |
| [ppg_hls_history_expectation.pvs](theories/hls/ppg_hls_history_expectation.pvs), [ppg_hls_randomized_expectation.pvs](theories/hls/ppg_hls_randomized_expectation.pvs) | History-dependent schedules and product-law integration for randomized policies. |
| [ppg_hls_repair_bridge.pvs](theories/hls/ppg_hls_repair_bridge.pvs), [ppg_hls_decision_bridge.pvs](theories/hls/ppg_hls_decision_bridge.pvs), [ppg_hls_finite_decision_bridge.pvs](theories/hls/ppg_hls_finite_decision_bridge.pvs) | Good-state existence, repair reachability and the declared finite feasibility/refutation interfaces. |

### Integrals, finite stochastic models and stopping bounds

| Files | Scope |
|-------|-------|
| [ppg_probability_measure.pvs](theories/measure_probability/ppg_probability_measure.pvs), [ppg_probability_integral.pvs](theories/measure_probability/ppg_probability_integral.pvs) | Probability laws and their native NASAlib real integrals. |
| [ppg_general_simple_integral.pvs](theories/measure_probability/ppg_general_simple_integral.pvs), [ppg_general_code_order.pvs](theories/measure_probability/ppg_general_code_order.pvs) | Nonnegative integrals from weighted measurable indicators, including infinite event masses. |
| [ppg_general_active_count.pvs](theories/measure_probability/ppg_general_active_count.pvs), [ppg_additive_drift_budget.pvs](theories/measure_probability/ppg_additive_drift_budget.pvs) | Arbitrary-measure count integrals and extended nonnegative budget bounds. |
| [ppg_conditional_existence.pvs](theories/measure_probability/ppg_conditional_existence.pvs), [ppg_subsigma_restricted_integral.pvs](theories/measure_probability/ppg_subsigma_restricted_integral.pvs) | Conditional expectation for integrable real functions under arbitrary finite native measures and sub-sigma algebras. |
| [ppg_additive_conditional_certificate.pvs](theories/measure_probability/ppg_additive_conditional_certificate.pvs), [ppg_additive_certificate_expectation.pvs](theories/measure_probability/ppg_additive_certificate_expectation.pvs) | Conditional potential certificates, integrated decrease, expected active count and almost-sure finiteness. |
| [ppg_mt_fixed_drift.pvs](theories/moser_tardos/ppg_mt_fixed_drift.pvs), [ppg_mt_random_init_drift.pvs](theories/moser_tardos/ppg_mt_random_init_drift.pvs), [ppg_mt_drift_expected_cost.pvs](theories/moser_tardos/ppg_mt_drift_expected_cost.pvs) | Drift bounds for the actual fixed-start and slot-zero MT processes, with bounded per-step costs. |
| [ppg_finite_conditional_value.pvs](theories/finite_models/ppg_finite_conditional_value.pvs), [ppg_finite_conditional_drift.pvs](theories/finite_models/ppg_finite_conditional_drift.pvs) | Finite-state conditional values and integrated drift. |
| [ppg_finite_potential_synthesis.pvs](theories/finite_models/ppg_finite_potential_synthesis.pvs), [ppg_finite_potential_accessible.pvs](theories/finite_models/ppg_finite_potential_accessible.pvs) | Rational first-step equations, checked potentials and positive-mass accessibility. |
| [ppg_exact_mt_fixed.pvs](theories/finite_models/ppg_exact_mt_fixed.pvs), [ppg_exact_mt_random.pvs](theories/finite_models/ppg_exact_mt_random.pvs) | Exact fixed-start and random-start MT expected work. |
| [ppg_resampling_table_tail.pvs](theories/finite_models/ppg_resampling_table_tail.pvs), [ppg_tail_mt_fixed.pvs](theories/finite_models/ppg_tail_mt_fixed.pvs), [ppg_tail_mt_random.pvs](theories/finite_models/ppg_tail_mt_random.pvs) | Exact stopping probabilities, checked geometric bounds and closed bad classes. |
| [ppg_finite_lumping_paths.pvs](theories/finite_models/ppg_finite_lumping_paths.pvs), [ppg_update_projection_stopping.pvs](theories/finite_models/ppg_update_projection_stopping.pvs) | Exact stopped-count reduction through lumping and commuting updates. |
| [ppg_full_resampling_probability.pvs](theories/finite_models/ppg_full_resampling_probability.pvs), [ppg_full_resampling_mean.pvs](theories/finite_models/ppg_full_resampling_mean.pvs) | Full-resampling geometric laws, expected work and positive good-state mass. |

### Feasibility and checked refutations

| Files | Scope |
|-------|-------|
| [ppg_certified_decision.pvs](theories/decision/ppg_certified_decision.pvs), [ppg_unsatisfiable_core.pvs](theories/decision/ppg_unsatisfiable_core.pvs) | Finite feasibility decisions and minimal infeasible cores. |
| [ppg_correction_duality.pvs](theories/decision/ppg_correction_duality.pvs) | Minimal-core and correction-set duality. |
| [ppg_farkas_certificate.pvs](theories/decision/ppg_farkas_certificate.pvs), [ppg_farkas_refutation.pvs](theories/decision/ppg_farkas_refutation.pvs) | Soundness of rational Farkas certificates and model-based reachability refutations. |
| [ppg_finite_abstraction_repair.pvs](theories/decision/ppg_finite_abstraction_repair.pvs), [ppg_find_good_path.pvs](theories/decision/ppg_find_good_path.pvs) | Repair traces and refutations through supplied executable exact finite abstractions. |
| [ppg_repair_budget_counterfamily.pvs](theories/computability/ppg_repair_budget_counterfamily.pvs), [ppg_repair_certificate_enumeration.pvs](theories/computability/ppg_repair_certificate_enumeration.pvs), [ppg_repair_undecidability.pvs](theories/computability/ppg_repair_undecidability.pvs) | An encoded infinite repair family: repairability is recursively enumerable and undecidable; infeasibility is not recursively enumerable. No total repairability or impossibility decider, or complete computable refutation checker, exists for this family. |

### Transport, observability and boot applications

| Files | Scope |
|-------|-------|
| [kantorovich_duality.pvs](applications/luces/kantorovich_duality.pvs), [brenier_uniqueness.pvs](applications/luces/brenier_uniqueness.pvs), [cyclical_monotonicity.pvs](applications/luces/cyclical_monotonicity.pvs) | Discrete transport optimality certificates and monotonicity under the stated assumptions. |
| [displacement_interpolation.pvs](applications/luces/displacement_interpolation.pvs), [wasserstein_metric.pvs](applications/luces/wasserstein_metric.pvs), [transport_stability.pvs](applications/luces/transport_stability.pvs) | Interpolation, metric properties and map stability. |
| [global_optimality.pvs](applications/luces/global_optimality.pvs), [unbalanced_regime.pvs](applications/luces/unbalanced_regime.pvs), [transport_ppg.pvs](applications/luces/transport_ppg.pvs) | Segmentation under its existing assumptions; calibrated regime arithmetic; snapshot repair preserving a fixed certificate family. |
| [fisher_atlas.pvs](applications/luces/fisher_atlas.pvs), [observability_geometry.pvs](applications/luces/observability_geometry.pvs), [observability_refinement.pvs](applications/luces/observability_refinement.pvs) | Charts, excitation-dependent observability and quantitative certificate refinements. |
| [lie_generator_structure.pvs](applications/luces/lie_generator_structure.pvs), [dual_observability.pvs](applications/luces/dual_observability.pvs), [tangent_bundle.pvs](applications/luces/tangent_bundle.pvs) | Conditional generator/observability models; explicit finite representability and interpolation contracts with concrete witnesses. |
| [lowrisc_boot_verification.pvs](applications/boot/lowrisc_boot_verification.pvs), [opentitan_boot_instance.pvs](applications/boot/opentitan_boot_instance.pvs) | Legacy undirected-interface limitation; a directed four-stage policy with successful and blocked paths. |

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
   [certified_iff_above_canonical](theories/certification/ppg_parametric_core.pvs) characterizes
   certification by `theta_c <= theta` when `theta_c` is canonical. The
   complete-lattice theory proves existence under nonemptiness and infimum closure.

2. **Blocking at the frontier.**
   [canonical_blocking_empty](theories/certification/ppg_list_blocking.pvs) gives an empty blocking set at
   a canonical level; `stricter_has_blocking` gives a failed certificate at a
   target outside that certified upper set.

3. **Component repair non-interference.**
   [repair_noninterference](theories/ppg_core/ppg_bdd_locality.pvs) preserves an obligation in
   another dependency component when the predicates are local and the state
   change stays inside the selected component's footprint.

4. **Moser–Tardos expected work.**
   [randomInitETLog_le_sum](theories/moser_tardos/ppg_mt_total_budget.pvs) proves
   **E[T_LOG] <= sum x(a)** for product-table random initialization, under the
   stated locality, event-probability and resampling-budget hypotheses. Finite
   expected work follows without a termination premise.

5. **Pegden and Shearer budgets.**
   [Pegden's expected-work theorem](theories/local_lemmas/ppg_pegden_expectation.pvs) replaces the
   product budget by independent-subset sums. The
   [Shearer expected-work theorem](theories/local_lemmas/ppg_shearer_total_expectation.pvs) bounds
   **E[T_LOG] by sum q_a/q_empty** for random initialization, under strict Shearer
   positivity and the stated event-probability upper bounds.

### General integrals and exact stochastic models

6. **Integral of the active count.**
   [expectedActiveCount_eq_tsum](theories/measure_probability/ppg_general_active_count.pvs) proves
   **integral count = sum measure(active_n)** for any native measure and a
   countable family of measurable events. Both sides may be infinite; no
   finite-measure, sigma-finiteness or semifiniteness hypothesis is imposed.

7. **Local budget to expected work.**
   [expectedActiveCount_le_of_budget](theories/measure_probability/ppg_general_active_count.pvs) gives
   **expected active count <= budget(0)/delta**, for positive finite `delta`,
   from `delta * measure(active_n) + budget(n+1) <= budget(n)`.
   Budgets may take the value infinity. Under a finite measure,
   [integrated_decrease](theories/measure_probability/ppg_additive_conditional_certificate.pvs) derives
   this inequality from an integrable, adapted, almost-everywhere nonnegative
   potential and its local conditional decrease. The resulting bound is
   **ofReal(integral initial potential)/delta**. For the fixed-start MT
   process, [ETLog_le_of_drift](theories/moser_tardos/ppg_mt_fixed_drift.pvs) gives
   **E[T_LOG] <= potential(initial)/delta**. The
   [cost bound](theories/moser_tardos/ppg_mt_drift_expected_cost.pvs) multiplies this by a finite
   cap on each active step; the cost function need not be measurable.

8. **Full resampling.**
   [fullResampling_expected_work_eq](theories/finite_models/ppg_full_resampling_mean.pvs) identifies
   the random-start mean with the extended geometric mean **b/(1-b)**, where
   `b` is the original bad-state probability. At `b = 1` the mean is infinity.
   Positive good-state mass gives finite expected work and almost-sure success.

9. **Exact potential synthesis and expectation.**
   [synthesize_iff_accessible](theories/finite_models/ppg_finite_potential_accessible.pvs) characterizes
   successful checked synthesis by positive-mass accessibility of good states.
   [ETLog_eq_potential](theories/finite_models/ppg_exact_mt_fixed.pvs) then identifies the fixed-start
   expectation with the exact rational potential under its accessibility hypothesis.

10. **Exact tails and checked closed bad classes.**
    [TLog_timeout_eq_survival](theories/finite_models/ppg_tail_mt_fixed.pvs) gives
    **Pr[T_LOG > N] = survival(N,s0)**. Accepted survival rows yield the
    block estimate **Pr[T_LOG > kH] <= b^k**. An accepted closed bad class
    containing the start instead gives an infinite expectation for that kernel.

11. **Exact stopped-count reduction.**
    [hitCount_projection](theories/finite_models/ppg_update_projection_stopping.pvs) equates concrete
    and reduced stopped counts on the same input stream when updates commute
    with projection and the good-state tests agree. The concrete state space
    need not be finite.

### Feasibility and refutation

12. **Checked finite decisions.**
    [ppg_certified_decision.pvs](theories/decision/ppg_certified_decision.pvs) gives witnesses or
    refutations from exhaustive finite enumeration. The
    [exact-abstraction repair theory](theories/decision/ppg_finite_abstraction_repair.pvs) realizes
    the abstract steps as a concrete repair trace under its realization obligations.
    [Farkas refutations](theories/decision/ppg_farkas_refutation.pvs) check a supplied rational
    certificate under a sound linear model; completeness of certificate search
    is a separate question.

### Canonical witness DAGs

13. **Encoding determines a canonical DAG.**
    [eq_of_stableEncoding_eq](theories/hls/ppg_hls_canonical_encoding.pvs) proves equality
    of valid canonical witness DAGs with the same stable encoding. Node indices,
    node sets and arc sets are recovered from the layers.

14. **Weighted proper DAG budget.**
    [tsum_weight_le_stableBudget](theories/hls/ppg_hls_witness_budget.pvs) bounds the
    unrestricted sum of canonical proper witness-DAG weights by the singleton
    Shearer budget. The [inverse-slack bound](theories/hls/ppg_hls_witness_budget.pvs) gives
    `1/epsilon` under the stated positive multiplicative slack. Countability,
    runtime and occurrence-probability assumptions are not needed.

### HLS expectation and repair

15. **Intersection-sensitive expected work.**
    [randomInitETLog_le_sum_stableBudget](theories/hls/ppg_hls_expectation.pvs) bounds
    random-start resampling work under the stated probability, matching,
    overlap and stable-budget hypotheses. The
    [policy](theories/hls/ppg_hls_policy_expectation.pvs),
    [history](theories/hls/ppg_hls_history_expectation.pvs) and
    [randomized-policy](theories/hls/ppg_hls_randomized_expectation.pvs) results retain
    their own measurability and probability-law assumptions. Expectations
    remain extended nonnegative values until a finite-budget bound is applied.

16. **HLS certificates and repair reachability.**
    [good_repair_reachable](theories/hls/ppg_hls_repair_bridge.pvs) derives a path to a
    good state from the original HLS hypotheses. The
    [decision bridge](theories/hls/ppg_hls_decision_bridge.pvs) combines this with
    existential probability/overlap certificates and declared feasibility
    and refutation conditions. The [finite bridge](theories/hls/ppg_hls_finite_decision_bridge.pvs)
    retains its finite model and enumeration hypotheses.

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
The stable encoding preserves finite node products, and canonical occurrence
indices can be reconstructed from it. Proper canonical DAGs therefore inject
into the proper stable sequences without changing their clipped real weights.
Suprema over finite subfamilies give the unordered sum bounds, including for
uncountable label types. A separate coding theorem proves DAG countability
when the label type is countable.

### Integrals and exact stochastic models

The integration layer connects measurable functions to NASAlib's real integral
and to extended nonnegative sums. General active-count integrals retain infinite
event masses. Finite rational kernels add conditional transition laws, checked
potentials, exact means and survival bounds. Lumping preserves these quantities
under transition-mass and good-state compatibility conditions.

### Feasibility and refutation

Finite search and exact abstraction provide concrete repair witnesses or checked
refutations. Minimal cores and correction sets describe infeasible obligation
families. For an encoded infinite repair family, the translation now proves
that repairability is recursively enumerable and undecidable, while
infeasibility is not recursively enumerable. The reduction uses a constructed
partial-recursive evaluator and bounded computations; computability and the
halting obstruction are proved in PVS. This result concerns the encoded family
and does not prevent decisions for the finite models above.
The HLS expectation and repair bridges add good-state witnesses and modeled
repair paths under their stated overlap and probability hypotheses.

## Related

- [ppg-lean](https://github.com/gajaka/ppg-lean): the generic Lean 4 development,
  its full module inventory, central theorems and kernel-verification record.
- [CERTIFICATION_README.md](docs/CERTIFICATION_README.md): the certification
  exposition, example workflow and earlier theorem entry points.
- [CERT_RUNNER_RESULTS.md](docs/CERT_RUNNER_RESULTS.md): recorded LUCES certificate
  results and the five-level certification example.
- [LIE_GENERATOR_README.md](docs/LIE_GENERATOR_README.md): Lie-generator analysis,
  coherence certificates and the recorded transport examples.
- [fisher_boundary_strong.smt2](smt/fisher_boundary_strong.smt2) and
  [brenier_t3_surjective.smt2](smt/brenier_t3_surjective.smt2): standalone Z3 encodings.
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
  [General Local Lemma](theories/local_lemmas/ppg_lll_source_probability.pvs) and
  [expected resampling bound](theories/moser_tardos/ppg_mt_total_budget.pvs) use the declared event
  probabilities, dependencies and resampling budgets.
- Robin A. Moser and Gabor Tardos,
  [*A constructive proof of the general Lovász Local Lemma*](https://arxiv.org/abs/0903.0544v3),
  especially Section 2. The PVS development includes the table process,
  witness construction, injectivity and probability bounds used in the counting
  argument.
- David G. Harris,
  [*Lopsidependency in the Moser-Tardos framework: Beyond the Lopsided Lovász Local Lemma*](https://arxiv.org/abs/1610.02420v4),
  Section 1.2, recalls the Erdős–Spencer criterion used by the
  [lopsided theory](theories/local_lemmas/ppg_lopsided_probability.pvs).

### Stronger probabilistic bounds

- Wesley Pegden,
  [*An extension of the Moser-Tardos algorithmic local lemma*](https://arxiv.org/abs/1102.2853v2),
  Theorem 1.4. The [PVS expectation theory](theories/local_lemmas/ppg_pegden_expectation.pvs) uses the
  independent-subset budget over each closed neighborhood.
- Nicholas J. A. Harvey and Jan Vondrák,
  [*Short proofs for generalizations of the Lovász Local Lemma: Shearer's condition and cluster expansion*](https://arxiv.org/abs/1711.06797v1),
  Section 2, provides the strict Shearer presentation. The expected-work bound
  follows the Kolipaka–Szegedy argument presented in
  [Vondrák's 2018 Lecture 8](https://theory.stanford.edu/~jvondrak/MATH233A-2018/Math233-lec08.pdf).
  See [ppg_shearer_total_expectation.pvs](theories/local_lemmas/ppg_shearer_total_expectation.pvs).

- Kun He, Qian Li and Xiaoming Sun,
  [*Moser–Tardos Algorithm: Beyond Shearer’s Bound*](https://arxiv.org/abs/2111.06527v1),
  Definitions 2.1–2.4 and Facts 2.5–2.6. The
  [witness-DAG theory](theories/hls/ppg_hls_witness_dag.pvs) covers reversal and ancestor
  prefixes. The stable-set connection is discussed in Section 1.2.1, footnote 3.
- Nicholas J. A. Harvey and Jan Vondrák,
  [*An Algorithmic Proof of the Lovász Local Lemma via Resampling Oracles*](https://arxiv.org/abs/1504.02044v3),
  Definition 5.2 and Section 5.3.2. The
  [layer theory](theories/hls/ppg_hls_witness_layers.pvs) constructs independent layers
  and proves their closed-neighborhood successor condition. The
  [canonical encoding](theories/hls/ppg_hls_canonical_encoding.pvs) recovers the DAG, and the
  [weight budget](theories/hls/ppg_hls_witness_budget.pvs) bounds its canonical proper family.
  The [occurrence bound](theories/hls/ppg_hls_policy_count_bound.pvs) and
  [policy expectation](theories/hls/ppg_hls_policy_expectation.pvs) use these witness
  families together with the actual resampling process.

### Order and certification

- B. A. Davey and H. A. Priestley, *Introduction to Lattices and Order*, second
  edition, Cambridge University Press, 2002. The
  [certificate lattice](theories/certification/ppg_certificate_lattice.pvs),
  [quotient order](theories/certification/ppg_list_quotient.pvs) and
  [selection lenses](theories/certification/ppg_selection_lenses.pvs) use the corresponding order,
  equivalence-class and dual-order constructions. Meet on certification
  classes requires the stated certificate closure condition.

### Integration, potentials and stopping bounds

- Patrick Billingsley, *Probability and Measure*, third edition, Wiley, 1995;
  Sterling K. Berberian, *Fundamentals of Real Analysis*, Springer, 1999.
  The [general integral](theories/measure_probability/ppg_general_simple_integral.pvs) uses weighted measurable
  indicators, and the [count theorem](theories/measure_probability/ppg_general_active_count.pvs) uses monotone
  convergence under a finite bound inside an arbitrary-measure argument.
- Johannes Lengler, [*Drift Analysis*](https://arxiv.org/abs/1712.00964v2),
  Theorem 1, gives the additive-drift background. The
  [conditional certificate](theories/measure_probability/ppg_additive_conditional_certificate.pvs)
  integrates the local decrease; the
  [MT certificate](theories/moser_tardos/ppg_mt_conditional_certificate.pvs) applies it to the
  actual stopped potential under the original product-log law. The
  [execution-cost bound](theories/moser_tardos/ppg_mt_drift_expected_cost.pvs) combines the
  resulting expected count with a cap on each active-step charge.
- Michael Mitzenmacher and Eli Upfal,
  [*Probability and Computing*, second edition](https://doi.org/10.1017/9781316651124),
  Section 7.1.1 and Exercise 7.25; David A. Levin and Yuval Peres,
  [*Markov Chains and Mixing Times*, second edition](https://pages.uoregon.edu/dlevin/MARKOV/mcmt2e.pdf),
  Exercise 10.22 and the uniform-block argument in Lemma 1.13. These support
  the [exact MT expectations](theories/finite_models/ppg_exact_mt_fixed.pvs) and
  [stopping bounds](theories/finite_models/ppg_tail_mt_fixed.pvs).
- Levin and Peres, Section 2.3.1, Lemma 2.5 and equation (2.10), is the background
  for [finite lumping](theories/finite_models/ppg_finite_lumping_paths.pvs). The
  [commuting-update reduction](theories/finite_models/ppg_update_projection_stopping.pvs) also permits
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

The recorded Lean-to-PVS translation covers the full 191-module inventory and
all 1,824 source theorems and lemmas. The final HLS layer includes coin and
footprint constructions, intersection-sensitive probability, refined DAG
weights, policy and randomized expectations, and repair/decision bridges.
Supporting PVS lemmas and TCCs are counted separately. The theorem statements
retain their declared carrier, measurability, locality and model hypotheses.

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
