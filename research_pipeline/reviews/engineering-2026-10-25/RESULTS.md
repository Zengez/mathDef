# Engineering audit results — independent reconstruction

Implemented and tested on a dedicated branch built from current main plus the
already integrated PR #11 engineering commit. PR #10 was inspected, not merged
or reset. The approved shifted-operator alias and filtration amendment on main
remain intact. This report is an engineering conclusion, not mathematical
certification, candidate reconciliation or a phase-transition rationale.

The [architecture map](ARCHITECTURE.md) covers initialization through recovery,
Wave 1 freeze, independent Wave 2 population, dependency replay, review,
reconciliation, validation and both independent UI paths. Its static inventory
covers 182 baseline software modules: 93 engine, 85 adapter, 2 UI and 2 evaluation.
There are 132 Wave 2-specific modules across engine/adapters and 178 stage/Wave 2/
research workflow files in the inspected naming families; 175 contain literal
`git push`. These are inventory counts, not a claim that every workflow has
identical semantics or that all 132 tools should be consolidated/deleted.

## Implemented improvements

1. **Bulk registry validation:** scoped parsed-registry and formulation-endpoint
   reuse in ingest, seal and publication; checkpoint reads no longer reload the
   same stage twice. Public validation overrides and all original predicates
   remain. Nothing persists across operations. Crash/retry, stale-input,
   duplicate/collision, source/evidence and publication tests pass.
2. **Intake:** batch pages share registry parsing and one robots-policy cache;
   later invocations reload changed approval. Acquisition remains rights-aware,
   bounded and opt-in. No real academic source was fetched.
3. **Offline preflight:** generated disjoint packets share the existing prepared
   context rather than replaying all amendments for each packet. The preparer
   refuses output inside the graph, including symlink escapes. Standalone
   preflight remains independently fresh and packets retain isolated simulation.
4. **Reusable artifact execution:** a tested CLI replaces the PR #10 workflow's
   embedded runner. The thin manual workflow fixes the independent workspace,
   exposes no write credentials and exports exact inputs, generated packets,
   digests, checkout identity and unchanged-byte proof, plus a read-only comparison of current records against the stored inventory. Stale source inventories, reviewed inputs, path
   escapes, reusing old output and concurrent input/workspace changes fail.
5. **Receipt reliability:** preflight now requires receipt ID and applied status
   in addition to mode/digest. Incomplete, mismatched or nonobject receipts fail
   closed. Export reports distinguish already-applied historical evidence from
   new proposals, reducing accidental replay ambiguity.
6. **Review throughput:** opt-in schema-v2 focus output stores a complete source
   once and preserves each candidate's own occurrence matches. Parent-visit
   budgets respect the existing priority order, count full source scope despite
   display truncation, and flag an oversized first item rather than hiding it.
   Default schema-v1 output is unchanged on the entire current candidate set.
7. **CI clarity and cost:** isolated CI watches the new workflow and excludes
   engineering measurement/checkpoint JSON that is not executable/test input.
   The live reconciliation queue remains included. CI retains integrity checks
   and validates effective-cycle edge coverage/report consistency; it no longer
   treats every structural cycle in the legacy projection as an automatic
   mathematical error. Both effective and legacy scopes are labeled.

## Measurements actually executed

Three repeats per version, same host; source fixture and exact output digests
held fixed. See [MEASUREMENTS.json](MEASUREMENTS.json) and runnable benchmarks.

| Workload | Before | After | Observed consequence |
|---|---:|---:|---|
| Five-stage registry ingest/seal/publication; 300 rows per non-source stage | 1.624740 s median; 3, 678 registry reads| 0.044441s; 27 reads|36.6× local speedup; publication SHA identical|
| Export 20 formulation changes in4 packets; 80 synthetic nodes and 800 historical amendments | 0.087796s; 5 graph replays| 0.033343s; 2 replays|2.63× local speedup; every packet digest identical|
| Entire live focus bundle, 420 canonical candidates |5, 448, 694 UTF-8 JSON bytes|3, 214, 620 bytes|41.0% smaller with exact context re-expansion|

The current focus workload still contains 813 candidate/parent visits over 468
sources. Deduplication removes repeated payloads and hashing, not the need for
345 repeated candidate-specific contextual assessments. No mathematical truth
or semantic-equivalence result is cached. Source count and visit budgets are
not estimates of mathematical difficulty or a promise of proportional human
review savings. The live focus measurement reads authorized Wave 2 only.

## Actual verification

- Full Python suite: **246 tests, zero failures/errors, two expected skips**.
  The two historical Round 175/176 proposals are intentionally stale against
  the current graph; they are not coerced into current valid transactions.
  Baseline was 218 tests with the same two skips. The added freshness, recovery, artifact, budget and receipt cases give 28 new tests.
- Read-only global scan, exhaustive consistency and exhaustive readiness all
  exited0. Readiness: **19/19 mechanical checks passed**. Nine global and 20
  consistency review leads remain. Existing metric/open-ball cycle remains
  formulation-avoidable in the effective existing-meaning projection; this is
  not a mathematical correctness verdict or permission to remove links.
- Receipt status: both separately approved transactions remain receipt-verified;
  outstanding Ext/Hom and local-basis questions remain mathematical reviews.
- The live Wave 2-only adapter and portable UI built to `/tmp`:559 term groups,
  595 screened meanings, 639 formulations, 887 displayed relations. This is a
  screened display subset, not an assertion all 611 graph meanings were published.
- Both synthetic stage UIs passed system-Chromium browser checks: independent
  term/text search, two contexts, citations, inline/nested dependency expansion
  to the correct context, focus/split, feedback dialog and mobile overflow.
  External requests were blocked. The bundled Playwright browser was missing
  and its CDN download was forbidden; the existing `/usr/bin/chromium` provided
  the successful final smoke. No browser dependency was added to the repository.
- Existing JavaScript syntax checks and the feedback unit test passed. Both
  modified workflow YAML files parsed. New CLI success/failure paths ran in
  subprocess tests. No claim that the manual workflow was remotely dispatched.
- All 2, 285 authorized live-workspace file hashes and the effective snapshot
  remain unchanged. Frozen Wave 1 is unchanged by Git tree identity and changed-
  path checks; its actual mathematical records were not inspected or regenerated.
  Synthetic freeze/recovery/publication tests passed. Production content and
  deployment configuration were neither read for data nor changed.

Machine-readable final scope, tests and changed paths are in VALIDATION.json.
The newly added reports do not alter AGENTS.md, current handoff, execution
contract, resume plan, mathematical audit history or authoritative graph data.

## Domain-neutral answers and remaining work

| Requested question | Evidence and assessment |
|---|---|
| Generic source/meaning/formulation model? | Already usable for contextual text and multiple formulations. Unknown metadata is accepted, but framework/units/operational-definition semantics are not validated. A typed optional review contract remains future work. |
| Reusable acquisition/discovery interfaces? | Manifest/parser/source-policy separation exists; one-run parsing/policy reuse is now implemented. Source-specific dispatch/priority belongs in adapters, not an indiscriminate crawler. |
| Common contextual extraction with subject rules? | Occurrence/version identity and graph replay are reusable. Math notation and category/module heuristics remain in current engine modules; moving them requires baseline rule-output fixtures first. |
| Equivalence versus specialization/competing meanings? | The current alias model must stay exact. Component prerequisites and alternative conventions need explicit reviewer roles, not a similarity merge or global ontology invented here. |
| Reuse the renderer? | Yes, the supplied catalog/branding contract and unrelated synthetic fixtures demonstrate it. Optional notation and domain terminology can vary; no UI features were removed. |
| Larger-scale efficient review? | Registry reads, graph replay and repeated source payloads now have measured reductions. Semantic judgment remains per context. Full graph materialization and repeated JS search normalization remain scaling candidates. |
| Reproducible empty start? | Mechanical init/ingest/seal/fork/recovery APIs and synthetic tests exist. Scholarly source approvals, research and editorial decisions are necessary external inputs, not deterministically regenerable facts. |
| Fewer scripts for a new discipline? | New shared preflight runner removes inline/transient execution probes. Consolidate orchestration interfaces gradually; preserve numbered historical tools and different freeze/provisional/review requirements. |
| Transparent contributor maintenance? | Stable IDs, source evidence, append-only decisions, exact packet artifacts and receipt-backed status provide the foundation. Better indexed documentation and adapter-policy contracts remain useful; mechanical success never labels scholarship verified. |

Immediate follow-up after normal code review: integrate this branch with the
separate PR #11 decision without cherry-picking duplicate code; let isolated CI
run on the final integrated tree; dispatch the manual workflow on a bounded
approved request once available on the default branch. Review artifacts and
statuses before any separately authorized submission. Do not merge PR #10's
historical graph snapshot over main.

Later architectural projects: extract math heuristics behind an optional domain
policy; unify repetitive workflow orchestration without changing receipts or
permissions; profile incremental graph materialization with dependency-aware
invalidation; evaluate a retrieval cache with source/version/rights/expiry
keys; precompute normalized frontend search fields; define optional typed review
roles; and specify process-level locking if concurrent writers become a real
requirement. Scoped caching assumes the existing exclusive writer and is not
that locking protocol. These projects need separate design/regression evidence,
not a sweeping rewrite or another domain's academic-source collection now.

The authorized engineering phases have produced reviewable code, measurements,
regressions and operational documentation. No mathematical transaction, source
research, population expansion, consolidation packet or gate transition follows
from this work.

GitHub handoff: branch pushed successfully. Draft PR creation was attempted with
`gh pr create --draft`, but the GraphQL API returned **Forbidden**. No new PR
URL was returned and nothing was merged. Use the [branch comparison](https://github.com/Zengez/mathDef/compare/main...codex/independent-pipeline-engineering-audit?expand=1)
for review or manual draft PR creation.
