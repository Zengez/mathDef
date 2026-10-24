# Codex engineering report: effective and formulation-choice cycles

Base: `5e5edb441096b4588c87b4ea0046edb734fd03b2` (matched fetched main).
Branch: `codex/wave2-dependency-cycle-audit`.

## Problem and changes

The global auditor's legacy adjacency includes direct scanned existing targets
and unoverridden existing seeds, but omits resolved missing candidates. A zero
in that restricted graph does not establish effective acyclicity.

Files changed:

- `research_pipeline/engine/dependency_cycle_analysis.py`: pure read-only
  effective-reference reconstruction and formulation-choice cycle analysis.
- `research_pipeline/engine/dependency_global_audit.py`: load full resolution
  rows and attach the new analysis, counts and explicit graph scope labels.
- `research_pipeline/tests/test_dependency_cycle_analysis.py`: seven synthetic
  regressions, including disposable-workspace resolution/amendment replay.
- `research_pipeline/WAVE2_CODEX_CYCLE_AUDIT.md`: this report.

`cycle_analysis` analyzes the union of ALL effective existing-meaning edges.
It uses authoritative amendment replay, existing alias and seed validators,
version-valid resolution rows, deferred seeds, and historical seed overrides;
it never modifies or rebuilds the live graph. Edge diagnostics preserve
occurrence, relation, candidate/alias and override provenance where applicable,
plus original source and effective-node version anchors. Component diagnostics
include every stored alternative, its full source, dependencies and unresolved
references. Output is deterministic and independent of subject-specific terms.

For compatibility with the existing protected CI configuration, old
`summary.cycle_components`, `graph_cycle_components` and legacy edge counts
retain their restricted semantics. Explicit scope fields and
`graph_cycle_includes_candidate_resolutions=false` label that limitation.
Consumers needing full cycle coverage must use `summary.effective_cycle_components`,
`summary.effective_existing_dependency_edges` and `cycle_analysis.components`.
Normal `scan` output is now deliberately compact: it retains all cyclic-component
`internal_edges` and their provenance, plus `cycle_analysis.edge_count`,
but omits the complete `cycle_analysis.edges` array. For all individual effective
edges, use `scan --include-cycle-edges`; `scan --snapshot-output /tmp/...`
also writes the complete edge list to the explicitly requested exhaustive
snapshot (while ordinary stdout stays compact). Programmatically, use
`analyze_snapshot(snapshot, include_cycle_edges=True)` or
`analyze_cycles(snapshot, include_all_edges=True)`. The flag
`cycle_analysis.all_effective_edges_included` identifies the response form.
New summary counts distinguish avoidable, unavoidable and undetermined SCCs.
No integrity check was removed or suppressed; cycles are structural diagnostics,
not automatic integrity failures or instructions to remove links.

## Algorithm and exact scope

Inside each union SCC, repeatedly remove a meaning when at least one complete,
version-valid formulation has no dependencies remaining in the component.
Keep ALL scan and historical seed dependencies of each chosen formulation.
The deterministic removal order and selected formulation IDs witness an
acyclic selection. Edges outside the SCC cannot return to it in the union graph.

If a nonempty core remains and all stored alternatives are complete and
version-valid, every possible formulation selection leaves each core meaning
with at least one dependency within that finite core. Hence a cycle is
unavoidable **under the stored formulation model**, even when no particular
edge or cycle is shared by every selection. Diagnostics expose the remaining
core and each alternative's core dependencies. Missing/incomplete/stale scans
prevent that conclusion and produce an undetermined result instead.

This is a monotone fixed-point procedure, not an exponential enumeration of
choices. A small exhaustive-selection regression independently checks the
answer for all 64 two-meaning dependency configurations.

The model permits one stored formulation per meaning. It does not establish
that alternatives are mathematically valid or interchangeable in every context.
Missing, unassigned, ambiguous and deferred prerequisites are reported but are
outside the existing-meaning projection. No result certifies complete expansion,
mathematical harmlessness, definitions, citations or research-phase completion.

## Observed example and review questions

Read-only validation of the committed independent Wave 2 snapshot reconstructed
exactly the same multiset of **2,647** effective edges as `edges.jsonl`.
There is one effective cyclic SCC:

- `form.wave2.analysis98.metric-space.compatible` →
  `meaning.wave2.directional113.open-metric`, occurrence
  `occ.eefb964814f9dc363bc9`, via `scan:candidate_resolution` of
  `missing.a332f3bfaf4665bee83b`.
- `form.wave2.directional113.open-metric` →
  `meaning.wave2.analysis98.metric-space`, both a scanned occurrence and
  historical seed `rel.wave2.directional114.01`.

Choosing `form.wave2.analysis98.metric-space` (distance axioms), followed by
`form.wave2.directional113.open-metric`, avoids this SCC structurally. Both
legitimate existing links remain untouched. The legacy count remains zero;
the full effective count is one; formulation-avoidable count one; unavoidable
and undetermined counts zero. Human review must still assess the intended
meaning/context and use of the topology presentation versus the distance-axiom
presentation. This tooling does not decide that question automatically.

Synthetic contrast: A can choose either a formulation requiring B or one
requiring C; B and C each require A. Every selection cycles despite the lack of
a single obligatory outgoing edge from A. The algorithm correctly reports an
unavoidable core `{A,B,C}`. A missing scan of an alternative instead yields an
undetermined result, not a false primitive escape.

## Post-Codex ChatGPT follow-up: concise diagnostics (2026-10-24)

A subsequent efficiency review found that including all 2,647 current effective
edges in every global audit JSON response was unnecessary. The routine result
now reports the full edge count but includes only the edges inside cyclic
strongly connected components; callers can explicitly request every edge.
This is **presentation-only**: the algorithm still processes every effective
edge, cycle classifications are unchanged, and historical CI fields remain.
Added tests for compact, expanded, and exhaustive-snapshot results.

## Validation and boundaries

- **63 tests passed:** `python -m unittest
  research_pipeline.tests.test_dependency_cycle_analysis
  research_pipeline.tests.test_dependency_global_audit
  research_pipeline.tests.test_dependency_graph
  research_pipeline.tests.test_dependency_review_preflight
  research_pipeline.tests.test_candidate_reuse
  research_pipeline.tests.test_review_preflight_cache`.
- **8 seed-override tests passed**, selected from
  `research_pipeline.tests.test_dependency_seed_overrides.SeedOverrideReplayTests`.
  `test_live_round177_packet_full_copy_replay_and_invariants` was not run:
  it reads a mathematical proposal outside the authorized independent dataset.
- Read-only current-instance validation: no integrity flags; edge multiset
  equality; SHA256 equality before/after for all **1,413 live graph files**.
- `git diff --check` and final changed-path inspection passed.
- Broad production/site/frozen-Wave1 suites and workflow dispatches were not run.

Inputs were project instructions/handoff/workflow/Round184 report, relevant
engine/test software, Git metadata, and the authorized independent Wave 2 graph.
No production or frozen-Wave1 mathematical data were used. No source, live
state, graph records, aliases, ledgers, gate, website or deployment files changed;
no new mathematical research, audit round, graph proposals or corrections were
performed. Starting live state remained 611 meanings, 659 complete scans,
770 amendments, 20 seed overrides, consolidation gate false.

GitHub API read returned Forbidden; PR creation is unavailable through the
current API route. Deliver the feature branch and commit for review. No merge
or main-branch commit is authorized or performed.
