# Wave2 mathematical dependency audit — efficiency review (October 23, 2026)

## Scope and baseline

Reviewed the source-free audit workflow, the last several packets (154–167), the live append-only graph, the global auditor, the candidate similarity scorer, the full graph rebuild/inbox dispatcher, context worklist, and existing regression test structure. This is a **process and code efficiency pass**, not a new mathematical-citation certification round and not a license to change source definitions.

At the start and end of these efficiency edits, the last verified mathematical graph state is **611 meanings**, **659/659 formulations scanned**, **724 original candidate identities**, **279 source-context alias records**, **seven version-bound candidate-to-existing-meaning resolutions**, **438 unresolved canonical candidate identity classes**, and **819 unresolved missing occurrences**. The consolidation gate remains FALSE. Source inventory SHA256: `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`; latest fingerprint `8e680a8bec257e29452c8bc0f6d690fa7d9cae95e057317dc873d01450a556da`. All original mathematical sources, Wave1, the production mathDef database and external missing-definition research remain untouched.

## Findings from the recent work

1. **Full-graph reconstruction per packet.** The `apply_inbox` driver already batched consecutive `amend` packages, but until this change it separately invoked `alias_candidates()` or `resolve()` for each pending alias or resolution packet. Each call validates a ledger and invokes `rebuild()`, replaying all live nodes/append-only amendments and rewriting derived graph indexes. In packets 158–161, four successive alias packets required four potential rebuilds when dispatched as separate invocations; if delivered in a single run they now need **one**. Packets 162–165 contained two alias packets and two resolution packets; ordering across mode boundaries controls possible grouping, so one common rebuild for all modes would be incorrect.
2. **Large repeated reads in review sessions.** The unoptimized GitHub-driven review often fetched the roughly 724-row candidate registry, the 659-formulation inventory, and the full 765-event amendment ledger, then reconstructed targeted source contexts manually. The previous global audit already had an all-effective snapshot and notation-aware suggestions, but lacked a **small ranked candidate-and-parent-source output**. Several reviews also initially inspected immutable *base* node snapshots, producing a stale-node false-positive alert that later had to be retracted.
3. **Selection governed too often by lexical resemblance.** The notation-aware pair scorer is a useful lead producer, but identical words do not imply the same mathematical object/type, and the still-unresolved candidate population is **not** a target of zero. Repeated local alias improvements of five to ten events per round have diminishing returns. Highest-impact scope errors (e.g. groupoid smallness) should come before cosmetic synonyms.
4. **Excessive per-round handoffs.** Rewriting multiple historical documents, a very large `WORK_CHECKPOINT.md`, the numeric resume plan and older reports after every small batch generates more remote calls and write conflicts than warranted. Live `STATE.json` is already the authoritative numeric checkpoint; immutable batch receipts give exact replay provenance.

## Implemented code changes

### A. Batch aliases and candidate resolutions, not just amendments

Changed `research_pipeline/engine/dependency_graph.py::apply_inbox` to collect **contiguous same-mode** `amend`, `alias`, or `resolve` packages, then validate the combined ledger decisions and call the corresponding writer once. Existing append-only event IDs, exact per-packet SHA receipts, chronological mode-boundary ordering, human-certification flags and replay safety are preserved. A malformed/conflicting event prevents any new ledger/receipts for that same-mode group. Each returned dispatcher result now includes `batched_rebuilds` (mode, packet count, event count), making grouping *observable* without inferring elapsed time or opening source-free phase gates.

**Important operational limitation:** this saves graph rebuilds only if multiple reviewed packets enter the **same dispatch invocation**. A new GitHub commit/Action for each individual packet still forces one rebuild per Action. Batch fully reviewed aliases in one checked packet, or submit multiple reviewed same-mode packets in one atomic Git push where supported. Do not increase batch size at the expense of individual mathematical scrutiny or review-rationale specificity.

### B. Add compact recurrence-prioritized contextual worklist

Changed `research_pipeline/engine/dependency_global_audit.py` to include a pure read-only `candidate_review_bundle()` and `focus` CLI. Each invocation loads the **effective append-only** graph once, filters out already aliased or resolved candidates, sorts remaining candidates by actual source recurrence/number of upstream formulations, and returns small source-specific review bundles. Each bundle includes the full original formulation, original context, current complete effective references, current node hash, source version, candidate ID, recurrence count and explicit source-truncation count. It never guesses alias equivalence.

Commands (from repository checkout):

```bash
W=research_pipeline/experiments/reconstruction-v2-independent
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" focus --limit 8 --max-formulations 3
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" focus --contains "sheaf" --limit 12
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" focus --candidate-id missing.fcb5ab865c6d9dbb3d79 --max-formulations 1000
```

The last command deliberately opts into a large, complete context review of one high-recurrence identity. Source counts and hashes are exposed precisely so future reviewers do not claim to have checked omitted contexts.

### C. Add regression coverage

`research_pipeline/tests/test_dependency_graph.py` now includes new tests for two same-mode alias packets requiring one rebuild, preserving separate receipts and idempotent replay; conflicting alias group rejection without partial receipts; two same-mode resolution packets requiring one rebuild; conflicting resolutions without partial receipts; mixed-mode alias-to-resolution ordering; and reported `batched_rebuilds` metadata.

`research_pipeline/tests/test_dependency_global_audit.py` now tests the new focus queue's recurrence priority, source-truncation disclosure, immutable graph behavior, effective source/reference information, named-candidate selection, rejection of aliased or unknown IDs, normalized text filters and fingerprint output.

**Verification boundary:** Code and tests are committed, and source files were re-fetched to verify the changes. The GitHub connector's commit-status endpoint did not expose running/passing Actions in this session, and the remote checkout is not accessible for executing Python test suites. Therefore **do not claim successful CI or measured wall-time performance** until a normal repository checkout/Actions run completes these tests.

## Estimated reductions (operation counts, not measurements)

- Four *contiguous* alias packets dispatched **together**: four complete graph rebuilds before, **one** after (**75% fewer full rebuilds**).
- Two *contiguous* resolution packets dispatched **together**: two before, **one** after (**50% fewer**).
- A single packet per GitHub push: **no graph-rebuild savings** from dispatch batching; reducing the number of commits/dispatches is therefore an equally important process change.
- The compact focus queue avoids manually composing repeated large source/ledger responses when run from a checkout; the exact token and elapsed-time savings depend on use and have **not** been benchmarked.

## Recommended review cadence and next decision

Start each session with **one live STATE check**, the compact last handoff, and a targeted `focus` query; do not reload full registries for every candidate. Review related parent formulations in **topical groups**; submit a single math-reviewed alias packet containing several well-supported decisions where possible, then check one Action run, receipts and live STATE. Finish by updating **one** compact latest-status report, and the resume plan only when the actual operational instructions changed.

Do not attempt to reduce all 438 unresolved classes through synonym merging. Prioritize groupoid-category smallness, other false-target/scope errors, and the pre-existing quasi-finite/submersive/perfect-closure source issues before further low-impact lexical merges. After high-impact review and reasonable global spot-checks, explicitly report whether remaining candidates should enter the **separately authorized missing-definition population phase** under the established consolidation-gate protocol. The gate is **not** opened by this efficiency update.
