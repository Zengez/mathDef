# Wave 2 engineering integration — 2026-10-25

Software from draft PRs #11 and #12 is integrated on
`codex/wave2-engineering-integration`, based on verified current `main`
`a7ce2ba3cdd07e6d0b9809d4e39014fb8533228c` (fetched again after validation).
No mathematical transaction was proposed or applied. Pass 2's consolidation
gate remains **closed**; Pass 3 is not authorized.

## Integration and preservation

Cherry-picked PR #11 `e978ae4d` and PR #12's seven subsequent commits through
`0767fb1e`, in order, without merge conflicts. Their software changes were
checked against current main before import; no older experimental snapshot
was included. PR #10 was not merged, and its immutable review ledger was not
rewritten or imported over current main. The original engineering reports in
`reviews/engineering-2026-10-25/` remain historical evidence; this report and
the current receipt status supersede their operational counts and pending
review descriptions.

The integrated implementation retains the domain-neutral engine/mathDef
adapter boundary: operation-scoped registry reuse and bulk validation,
amortized intake parsing, replay reuse during preflight, exact live-occurrence
review anchors, compact context bundles and visit budgets, guarded offline
artifact export, and fail-closed receipt verification. No adapter, mathematical
record, production viewer, deployment configuration, or dependency was changed.
The read-only status CI step and optional export workflow are imported as
engineering configuration; neither applies packets or opens a phase gate.

This integration additionally supports receipt-backed existing-meaning
resolutions and explicit supersession of historical review anchors. Supersession
requires the verified amendment packet to name the **exact formulation and
predecessor node hash**, plus a changed live node with the old occurrence
disposition no longer present. Missing receipts, wrong predecessors, unchanged
effects and invalid case links fail closed. Historical anchors and questions
remain unchanged. Resolution diagnostics compare the current registry, immutable
resolution ledger and target version covering **all** meaning variants.
A historical receipt remains historical evidence if a later variant changes;
the separate current-version diagnostic then becomes false.

## Current reconciliation

All six inbox packet canonical digests agree with their immutable applied
receipts (mode, ID, hash and applied status). Full packet IDs, target versions,
and current-effect diagnostics are in `RECONCILIATION_STATUS.json`.

| Transaction | Canonical packet SHA256 |
| --- | --- |
| Shifted-operator alias | `b3574ca780c053c6df1392a414df7eb86e5be1dab124dbf25f6fafe606883c11` |
| Real-time filtration amendment | `1517ea4b426f4dcf0fdec00dfc385b9d84fe125768c21b955526537c7cfa215f` |
| Ext/Hom and local-connectedness amendment | `125fac4067b5a72d774ab3d09cae9df723d2bd2916c4430e0a2af3fd7d2a299f` |
| Order-zero S-linearity resolution | `d519a0c911253565dc1ea138f7cc36b107dc7767a6f91f4e9b4a508b10eaf2d9` |
| m-primary reanchoring amendment | `8c9ba8c6e6b67c397c08c6950c5a0b998106ea892643b87a4e052bf80d677da4` |
| m-primary existing-meaning resolution | `a6e41ea7f038971cdb00fa40487da2054820f864b3ddf963658f7e435e258eef` |

The two old Ext/Hom and local-basis anchors are
`superseded_by_verified_transaction`, not pending reanchoring actions. The
queue has six verified transactions, two retained superseded reviews, and zero
active reviews **in this queue only**. This does not settle all mathematical
questions. Both resolution packets' current registry, ledger and complete
target-version checks pass.

The m-primary regression preserves alias event
`alias.global-audit.20261023.051`: observed candidate
`missing.2a4c23153be5ee32b75f` is now inactive, while canonical candidate
`missing.b963edbe734f35266d3a` resolves to
`meaning.b9defeff446a0526.ideal-of-definition-local-ring`.
In `form.22c049b8eee93897.system-of-parameters`, live occurrence
`occ.8421cc652ec8506b0ca9` uses the explicitly reviewed canonical candidate;
its effective edge records candidate resolution. Recomputing the lexical key
still yields the historical observed ID and must not override that decision.
The raw original occurrence `occ.0040f1ed3e2891509ae9` was unassigned; it is
not interchangeable with the live occurrence or a historical seed reference.
The defining formulation's m-primary phrase remains external, without a
resolved self-edge. Tests retain duplicate historical-alias ID rejection.

## Executed validation

- Full Python discovery: baseline **207**, imported **246**, final **256**
  tests; final **254 passed, two expected skips**, zero failures/errors
  (3.388 s). Skips are deliberately stale Round 175/176 proposal fixtures.
- Exhaustive readiness: **19/19** mechanical checks true, no integrity failures.
  Pass 2 completion remains `not_determined`.
- Exhaustive consistency: **20 review leads**, zero integrity findings.
- Global/cycle audit: nine leads, zero integrity findings; legacy projection
  has zero cycles, complete effective graph has one metric/open-ball component,
  avoidable under stored formulation choices; zero unavoidable components.
  All candidate-resolved dependencies and historical seed overrides are included.
- Provenance: 659 formulation evidence links, 15 source records, 973 observations,
  no absent evidence/source/locator records. All 659 formulations are paraphrases
  with unspecified verification state. External citations were not verified.
- Actual Wave 2 draft: 559 groups, 595 screened meanings, 639 formulations,
  887 relations. Provisional records remain excluded from that publication view.
- Chromium: both synthetic stage previews pass search, contextual meanings,
  source links, inline/nested expansion, feedback, focus/split, mobile overflow
  and runtime-error checks; external requests blocked. Feedback Node test passes.
  Source/generated JavaScript syntax, Python compilation and workflow YAML parse
  pass. The two read-only audit/status CI shell steps pass locally verbatim.
- Guarded export CLI on a disposable byte-identical live-workspace copy returns
  `already_applied_no_new_proposals` for the shifted-operator packet, with no
  new proposals, identical before/after bytes and fresh source inventory.
  No apply, rebuild or submission was executed on that copy or the live workspace.

Synthetic measurements (three repeats; `MEASUREMENTS.json`): 300-row registry
median 1.692 s before / 0.039 s after, identical publication digest. Amendment-
heavy export median 0.091 s / 0.034 s, five / two graph replays, identical packet
digests. Export comparison uses PR #11 before replay optimization; an initial
main-baseline attempt failed closed because main expects the older
`reference_index` manifest format. No guard was relaxed. Timings do not measure
mathematical review effort or promise production speedups.

All **2,293** live workspace file paths and raw byte hashes equal the pre-import
manifest `PROTECTED_FILE_HASHES.json`, including sources, graph, receipts,
ledgers, aliases, missing registry and state. Canonical file-map SHA256:
`b14aa5eced27ec6b82d6c723191fed3266e8115c06b428cd9be8bfcacaf61d17`.
Frozen Wave 1's Git tree is unchanged:
`00d52a5fbb31827f80bf7683ae8347e6d652e569`; no frozen records were read.
Branch-to-base path checks and `git diff --check` pass. `VALIDATION.json`
contains the exact complete changed-file list and mechanical results.

Live counts remain 611 meanings, 659/659 scans, 418 unresolved canonical
identities, 841 missing occurrences, 727 registry candidates, 300 active aliases
(301 retained historical alias events), nine existing-meaning resolutions and
775 amendment events. Inventory SHA256:
`34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113`;
unresolved SHA256:
`7b69e2fdcb30a4536883df44308d386219b7621533886d65276b8992959f4773`.

## Reproduction and limits

From the repository root, using only the authorized Wave 2 workspace:

```sh
W=research_pipeline/experiments/reconstruction-v2-independent
python -m unittest discover -s research_pipeline/tests -v
python -m research_pipeline.engine.dependency_consolidation_readiness --workspace "$W" --exhaustive
python -m research_pipeline.engine.dependency_consistency_worklist --workspace "$W" --exhaustive
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" scan --limit 80 --candidate-limit 80 --include-cycle-edges
python -m research_pipeline.engine.dependency_provenance_audit --workspace "$W"
python -m research_pipeline.engine.dependency_reconciliation_status --workspace "$W" --queue research_pipeline/reviews/canonical-identity-2026-10-24/LIVE_RECONCILIATION_QUEUE.json
python -m compileall -q research_pipeline/engine research_pipeline/tests research_pipeline/benchmarks
node --test research_pipeline/tests/test_reference_ui_feedback.cjs
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/usr/bin/chromium node research_pipeline/tests/test_reference_ui_browser.cjs
git diff --check
```

The live draft was built with `adapters.mathdef.preview.build(workspace,
draft=True, output=Path('/tmp/integration-live-wave2-preview'))`, then
`ui.renderer.render` on its catalog and adapter branding; generated `app.js`
and `preview.js` passed `node --check`. The export smoke used
`python -m research_pipeline.engine.dependency_review_export --repo-root COPY_ROOT
--workspace research_pipeline/experiments/reconstruction-v2-independent
--alias-packet research_pipeline/reviews/readonly-integration-fixture/alias.chat-postcoverage.20261025.shifted-operator.json
--output-dir FRESH_OUTSIDE_CHECKOUT`, after copying only the authorized workspace
and that existing packet into a disposable tree. Temporary inputs were removed.

The combined live `preview_site` and live `resume_checkpoint` commands were not
run: they read frozen Wave 1, prohibited by `AGENTS.md`. Synthetic tests cover
their portable behavior. No remote workflow dispatch was performed; the new
optional workflow remains proposed for review, not exercised on GitHub here.
No production/frozen mathematical data, external subject sources or research
phase actions were used. Source reconciliation, formulation conventions,
mathematical judgments and any gate decision remain explicitly deferred.

Delivery status is recorded durably in `CHECKPOINT.json`. Review this unmerged
branch; PRs #11/#12 should not subsequently be merged as duplicate implementations.

The branch was pushed successfully through validation commit `8036662b` and
this final delivery checkpoint. Draft PR creation was attempted using both
`gh pr create --draft` (GraphQL) and `gh api --method POST repos/Zengez/mathDef/pulls`
(REST with `draft: true`); both returned **Forbidden**. No PR was created or merged.
[Review the pushed branch](https://github.com/Zengez/mathDef/tree/codex/wave2-engineering-integration)
or [open its comparison](https://github.com/Zengez/mathDef/compare/main...codex/wave2-engineering-integration?expand=1).
