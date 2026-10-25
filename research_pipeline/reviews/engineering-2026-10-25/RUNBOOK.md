# Engineering runbook and compatibility notes

This supplements the existing dependency-first execution contract; it does not
replace its mathematical approval, phase or source policies. No command below
submits a packet or opens the consolidation gate.

## Plan a bounded contextual review

```bash
python -m research_pipeline.engine.dependency_global_audit \
  --workspace research_pipeline/experiments/reconstruction-v2-independent \
  focus --limit 420 --max-formulations 1000 \
  --parent-budget 100 --compact-sources > /tmp/review-focus.json
```

Priority remains the existing occurrence/parent-count/ID order. The budget
counts **all** incoming parent visits for selected identities, even when
`--max-formulations` truncates emitted source evidence. It is not a difficulty
score. Selection stops at the first item that would exceed the remaining
budget; it does not silently skip difficult high-priority candidates. An
oversized first candidate is returned with an explicit over-budget flag.
Explicit `--candidate-id` requests cannot be combined with a truncating budget.
A zero candidate limit returns an empty result.

Without either new option, schema-v1 output is unchanged. Compact schema v2
places complete source contexts in `source_contexts[formulation_id]`. Candidate
rows retain their exact `matching_source_references`, occurrence IDs and the
source ID. Reconstruct a legacy source row by combining its shared source
context with that candidate-specific match list. Unknown sources remain visible
integrity warnings. Effective live reference positions and historical seed
provenance retain their separate views. No bundle marks a review COMPLETE;
the legacy `reviewed_candidate_count` is a returned-item count, not adjudication.

The current 421/421 completed audit is historical, while the active graph has
420 canonical candidates after approved transactions. Use the existing
receipt-backed reconciliation status command to relate these snapshots. Do not
run the historical coverage validator as though it targeted the changed graph,
or rewrite the completed audit ledger to make that check pass.

## Export explicitly reviewed proposals

Use only source/version-bound requests already reviewed by a person/assistant.
The example path is a placeholder for such a committed request, not a staged
mathematical correction supplied by this engineering task.

```bash
python -m research_pipeline.engine.dependency_review_export \
  --repo-root "$PWD" \
  --workspace research_pipeline/experiments/reconstruction-v2-independent \
  --manifest research_pipeline/reviews/approved-review/manifest.json \
  --output-dir /tmp/unique-reviewed-preflight
```

An alias-only request uses `--alias-packet` instead; both may be supplied.
Reviewed JSON inputs must resolve inside `research_pipeline/reviews`, with no
absolute paths, `..`, or symlink escape. The output must be a NEW directory
outside the checkout. The workflow fixes the workspace to the independent
Wave 2 directory; the generic CLI can target another explicit workspace only
when that workspace is separately authorized. The runner rejects workspace
symlinks, rather than hashing content outside its declared scope.

Artifacts contain generated complete-node amendment packets (at most five
formulations each), exact reviewed inputs, canonical packet digests and byte
hashes, current inventory/fingerprint and checkout commit, and whole-workspace
before/after byte fingerprints. Current source/formulation/meaning/seed data is recollected read-only and compared with the stored inventory before exporting; an already-stale inventory fails without any automatic rebuild. The optional `--commit` is checked against
actual Git HEAD. Local input hashes remain necessary: HEAD alone does not prove
an uncommitted local request belongs to that commit. CI also checks a clean
working tree. No artifact is copied into an inbox, committed, pushed or applied.

`mechanically_preflighted_not_applied` means at least one valid new proposal.
`already_applied_no_new_proposals` identifies receipt-backed historical input,
not a fresh ready-to-submit action. The report lists these packet IDs separately.
Receipt acceptance requires matching packet ID, mode, digest and applied status.
A stale/invalid request or input/workspace change fails the export and removes
half-generated artifacts. `failed_not_applied` report.json is diagnostic only.
Never reuse a prior output directory to bypass a failure.

The workflow `.github/workflows/reviewed-dependency-preflight.yml` is manual,
contents-read-only, has no persisted checkout credentials, uses environment
variables for input values and exports evidence for 14 days. It has no push
trigger and no graph/submission permission. Until a workflow is on the default
branch, workflow_dispatch may not be available. Local CLI tests and YAML
parsing are not a claim of a remotely executed Actions dispatch. After separate
review/merge, dispatch a bounded approved input and inspect artifact status,
packet hashes, unchanged-workspace proof and receipts before any separately
authorized operational action.

Offline multi-packet export reuses one prepared preflight context after its
initial effective snapshot. Each packet retains a separate simulated node map.
Standalone preflight remains fresh. Existing full-node hashes, exact occurrence
IDs, candidate reuse checks and explicit mathematical rationale are unchanged.
The older preparer additionally rejects any output under dependency_graph,
including symlinked aliases of that path.

## Bulk registry and intake behavior

`Workspace.ingest`, `seal` and `publication` reuse parsed registries within one
synchronous operation. They run the same public validator, including subclass
or adapter overrides. Relation endpoints use one formulation-ID index per
operation. Target registry mappings advance after each append, and checkpoints
still follow flush/fsync. Failure or return discards the cache; a later call
reloads files and detects changed IDs, malformed JSON, duplicate IDs, source
approval changes and broken evidence/relations. Checkpoint interruption after a
flush is covered by a retry test that retains the exact persisted prefix.

This is a bounded parsing optimization under the existing single-writer model,
not a persistent cache or new concurrent-writer protocol. Do not retain its
private context across sessions or semantic updates. Stage freezes, source
rights and evidence policies have not been relaxed.

Batch intake shares that bounded registry view and one robots-policy cache
within a single invocation. Each page still checks its source eligibility,
URLs and excerpt rights. A later invocation reloads policy; changed approval
cannot be hidden by a cache. No external source retrieval was performed here.

## Reproduce measurements and verification

```bash
python -m unittest discover -s research_pipeline/tests -v
python -m research_pipeline.benchmarks.registry_throughput --size 300 --repeats 3
python -m research_pipeline.engine.dependency_consolidation_readiness \
  --workspace research_pipeline/experiments/reconstruction-v2-independent --exhaustive
```

To reproduce a before comparison, save **software only** from the integrated
base, never an excluded historical dataset:

```bash
git show e978ae4d:research_pipeline/engine/core.py > /tmp/prior_core.py
python -m research_pipeline.benchmarks.registry_throughput --core-file /tmp/prior_core.py
git show e978ae4d:research_pipeline/engine/dependency_global_audit.py > /tmp/prior_audit.py
python -m research_pipeline.benchmarks.preflight_export --baseline-file /tmp/prior_audit.py
```

Benchmarks construct disposable synthetic registries/graphs, including an
800-event amendment history, and compare exact publication/packet digests.
They do not measure academic research quality, remote CI time or all dataset
sizes. Filesystem load, fsync and CPU affect timings; operation counts and
equality checks are the more portable evidence.
