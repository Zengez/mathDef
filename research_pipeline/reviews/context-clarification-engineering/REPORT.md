# Candidate-context review metadata — engineering handoff

Implemented on `codex/wave2-context-clarification`, based on engineering
`51696c08b1e5e8b7964ad4f1599e61acc9301ff9`; current main mathematical
checkpoint remains `a7ce2ba3cdd07e6d0b9809d4e39014fb8533228c`.
Evidence/policy input is pinned to `c1882af843cd0573356d780a28168f9ce1543a47`.
Git verifies that the evidence branch descends from the engineering branch.
GitHub API GETs for PRs #13/#14 returned Forbidden, so draft/open metadata
could not be independently refreshed; their branch heads and ancestry were
verified. Neither branch was merged or reset by this task.

## Result and architecture

The registry is derived from immutable observations, aliases and graph replay;
editing its context field would erase the distinction between observation and
interpretation. Instead, the new domain-neutral module validates a separate,
explicit **analysis metadata log**, using the design in `DESIGN.md`:

- A **proposal** retains the exact canonical query/context, full observed
  references, source wording/versions, every incoming occurrence and its alias
  path, and an independently authored proposed interpretation. Coverage must
  include the specialized representative parents as well as mismatched uses.
- Pins cover the complete inventory (all variants), nodes, state, registry,
  ordered alias/resolution/override/review ledgers, and **all workspace raw file
  bytes**, including original nodes, historical amendments and receipts.
- A **review** approves or rejects one exact proposal digest. It cannot replace
  that payload. Unique event IDs, previous-event hashes, trusted history
  checkpoints, exact prior-interpretation pins and pure append extension reject
  duplicates, changed history, truncation, reordering and conflicting approvals.
- Context roles are explicitly **component prerequisites**, with per-occurrence
  instantiation and retained parent conditions. Whole-parent identity, alias,
  resolution and new-dependency fields are rejected. No context text is parsed
  as a graph operation; adding a self-edge is therefore unsupported.
- Global focus/scan and consistency readers can opt in. They show parallel raw
  observed, recorded canonical, proposed and reviewed descriptions plus full
  provenance. They revalidate attached metadata before reporting it. All graph
  fields, leads, source evidence hashes and cycle results retain their original
  meanings. Other readers remain raw graph readers; no implicit log is loaded.
- Preflight uses a disposable **byte-identical copy**, verifies source inventory
  freshness, and checks both original/copy and review inputs afterward, including
  failure paths. Its receipt-shaped result is `mechanically_valid_not_applied`,
  never an applied graph receipt. Logs/checkpoints must stay outside the protected
  workspace. No submit/apply dispatcher or automatic ledger writer is added.

This is an operational capability for version-controlled reviewer metadata,
not a graph recontextualization applied here. `extend_log` returns a validated
extension preserving its entire prior prefix; a reviewer can commit that JSON
and its checkpoint through normal Git review. There is no implicit approval
from a research report or approval inferred from similar words.

## Policy preservation and limitations

The owner-approved typed component-prerequisite rule is accepted as policy;
this report does not reopen it. The qualification policy is also retained.
Basic qualification-ledger validation separates proposals from claimed applied
entries, requires application evidence for the latter, and does **not** verify
that those claimed edits actually happened. A proposal may reference an exact
unapplied qualification entry only when its source/occurrence/version/node pins
match. Metadata approval cannot apply a source qualification. The actual owner
ledger remains **one proposal, zero applied qualifications**, unchanged.

Mechanical schema checks cannot prove a statement written in prose. A dishonest
author could label a mathematically invalid claim a component; independent
mathematical review and protected Git approval remain necessary. Tests reject
**declared** whole-process equivalence/generalization, including a homogeneous
one-parent case, without claiming natural-language theorem proving. No unitality,
nonzero hypothesis, category size or indexing convention is inferred.

History checkpoints must come from a trusted reviewed revision. Replacing both
a log and its trusted checkpoint outside that review boundary is not prevented
by hashes, nor do author-name strings authenticate a person. Every log event
must match the current complete snapshot: a graph change fails replay closed.
This version provides no automatic stale-event migration or historical-log
revalidation/supersession across changing graphs. That future capability would
require a separately reviewed design preserving old events; never delete stale
events or relax pins to make the current log pass.

No mathematical correction is applied or newly authorized. The six rank-36/38
mismatches remain for separate mathematical transaction authorization. The
existing source-provider evidence on the evidence branch is preserved as
reported evidence, not recertified here; no external page was fetched. Its
10 convention checks / 3 significant remaining qualifications are not graph
resolutions or gate acceptance.

## Actual validation

- Baseline: **256 tests**, two expected skips, no failures (3.616 s).
- Final: **284 tests: 282 passed, two expected stale Round175/176 skips**,
  no failures/errors (5.669 s). Twenty-eight new tests include positive replay,
  rejection, prior interpretation updates/races, complete coverage, aliases and
  historical seed distinction, malicious/malformed JSON/events, stale source,
  variant/node/ledger pins, raw-byte drift, changed inputs/failure paths,
  reader revalidation, CLI integration and qualification status controls.
- Exhaustive readiness: **19/19 true**, no integrity failures; Pass 2 completion
  remains `not_determined`. Exhaustive consistency: **20 review leads**, zero
  integrity findings. Global: nine leads, one formulation-avoidable effective
  cycle, zero unavoidable components, zero integrity findings. These are review
  evidence, not mathematical certification.
- Structural provenance complete: 659 formulations, 611 meanings, 15 source
  records, 973 observations; no missing evidence/source/locator records. All
  formulations remain paraphrases with unspecified verification state.
- Reconciliation status unchanged: six applied receipt-verified transactions,
  two superseded historical reviews. No previously applied transaction resubmitted.
- Exact handoff CLI smoke: six mismatches plus two specialized occurrences,
  all **8/8** source/node anchors match. Five historical alias events preserved.
  Temporary test-only approvals exercise mechanics on a copied workspace; the
  log is deleted and never installed or committed. Global/consistency opt-in
  reports differ from raw reports **only by the parallel metadata field**.
  `SMOKE.json` retains compact evidence, not an active mathematical review log.
- Loaded pre-change code directly from engineering Git blobs and compared its
  default global scan, focus and exhaustive consistency output to current code:
  **exact JSON equality**. Existing effective graph results are unchanged.
- Python compilation and `git diff --check` passed. No production/frozen data,
  combined live previews, deployment, external subject research or workflow
  dispatch was used. Frontend tests were not repeated for this analysis-only change.

All **2,293** protected file paths and raw bytes match
`PROTECTED_FILE_HASHES.json`. Canonical file-map SHA256:
`b14aa5eced27ec6b82d6c723191fed3266e8115c06b428cd9be8bfcacaf61d17`.
Sources, graph nodes/indexes, missing registry, aliases, resolutions, receipts
and ledgers remain unchanged. Branch-to-base changes are only the three analysis
modules, one test module and this engineering report directory; the exact list
and output hashes are in `VALIDATION.json`. Frozen Wave 1 has no changed path
and its Git tree is unchanged; no frozen mathematical files were read.

Current state remains **611 meanings; 659/659 scans; 418 unresolved canonical
identities; 841 missing occurrences; 727 registry candidates; 300 active aliases
(301 historical alias events); nine resolutions; 775 amendments**. Inventory:
`34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113`;
unresolved fingerprint:
`7b69e2fdcb30a4536883df44308d386219b7621533886d65276b8992959f4773`.
Gate is **closed**; Pass 3 unauthorized.

## Reproduction

From repository root, using the explicit independent workspace:

```sh
W=research_pipeline/experiments/reconstruction-v2-independent
python -m unittest research_pipeline.tests.test_dependency_context_reviews -v
python -m unittest discover -s research_pipeline/tests -v
python -m compileall -q research_pipeline/engine research_pipeline/tests
python -m research_pipeline.engine.dependency_consolidation_readiness --workspace "$W" --exhaustive
python -m research_pipeline.engine.dependency_consistency_worklist --workspace "$W" --exhaustive
python -m research_pipeline.engine.dependency_provenance_audit --workspace "$W"
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" scan --limit 80 --candidate-limit 80 --include-cycle-edges
python -m research_pipeline.engine.dependency_reconciliation_status --workspace "$W" --queue research_pipeline/reviews/canonical-identity-2026-10-24/LIVE_RECONCILIATION_QUEUE.json
git diff --check
```

For a separately reviewer-authored log and trusted history checkpoint outside
the protected workspace (placeholder paths below, **not** live approved inputs):

```sh
python -m research_pipeline.engine.dependency_context_reviews \
  --workspace "$W" --log /tmp/review-log.json --checkpoint /tmp/trusted-history.json
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" \
  --context-review-log /tmp/review-log.json \
  --context-review-checkpoint /tmp/trusted-history.json focus --compact-sources
python -m research_pipeline.engine.dependency_consistency_worklist --workspace "$W" \
  --context-review-log /tmp/review-log.json \
  --context-review-checkpoint /tmp/trusted-history.json --exhaustive
```

The JSON envelope is exactly `{"schema_version":1,"events":[...]}`; each event
has `event_id`, `previous_event_sha256`, `kind` and `payload`. Generate factual
anchors with `candidate_basis(load_context_snapshot(workspace), canonical_id)`;
author the interpretation, every occurrence instantiation, hypotheses and
provenance separately. `history_checkpoint(events)` pins the trusted ordered
history; `extend_log` validates a pure append without writing anything.
`test_dependency_context_reviews.py` contains complete synthetic proposal/review
examples and the non-applying live-case regression. Mathematical review remains
required beyond those mechanical examples. `--qualification-ledger` optionally
supplies the exact proposed-qualification provenance; it cannot apply an entry.

Delivery status and resume instructions are in `CHECKPOINT.json`. After code
review, any actual adoption of the six mathematical clarifications still needs
separate authorization; do not begin repairs or another audit round automatically.

Branch pushed through validation checkpoint `457ef4ee4ce4f15f1435f965ae68b8508b188286` and this final delivery
commit. Draft PR creation via `gh pr create --draft` (GraphQL) and REST POST
with `draft: true` both returned **Forbidden**. No PR was created or merged.
[Open the comparison against the engineering base](https://github.com/Zengez/mathDef/compare/codex/wave2-engineering-integration...codex/wave2-context-clarification?expand=1).
