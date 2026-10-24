# Independent Wave2 audit efficiency assessment — October 24, 2026

## Scope and unchanged mathematics

Reviewed the preceding audit handoffs, Round 178 exact event/receipt chain, current live graph and the implementations of `dependency_graph`, `dependency_global_audit`, `dependency_review_preflight`, `dependency_review_submit`, existing optimization work and focused mathematical review tests. **This is an efficiency/code review, not an additional mathematical certification round.** No source definitions, existing independent graph events, production mathDef, frozen Wave1, experimental breadth Batch143, phase gates or candidate mathematical conclusions were changed.

Last *verified* numerical graph baseline from Round178: 611 meanings, 659/659 scanned formulations, 725 raw candidate records, 298 alias decisions, 7 candidate-to-meaning resolutions, 420 unresolved canonical candidates, 839 missing-reference occurrences, 766 scan amendments, 19 historical seed overrides, zero ambiguous/unassigned, 651 open/8 closed, consolidation gate FALSE. Read live STATE for any subsequent advances.

## Most costly repetition: reviewed candidate mismatch

Round178 established that an `amend` reference classified `missing` silently regenerated `missing_candidate_id` as `missing_key(phrase, context)`, even when the reviewer supplied an existing canonical missing candidate ID. The resulting extra raw candidate required a separate source-reviewed alias, a second committed packet, another graph Action and new fingerprint/checkpoint work. This is an *engine identity rule*, not proof that the original audit was wrong.

**Implemented optional, nonautomatic reuse** in `make_snapshot`, `amend`, the offline reviewed-manifest builder and preflight. An amended missing reference may now include:

```json
{
  "phrase": "closed subset in the ambient space",
  "state": "missing",
  "context": "Full original mathematical context, including the ambient topology",
  "reviewed_existing_candidate_id": "missing.EXACT_ACTIVE_CANONICAL_ID",
  "candidate_identity_review_rationale": "A full source-context justification (at least forty characters) showing that this occurrence denotes precisely the already-registered mathematical prerequisite."
}
```

The **reviewer**, not the engine, supplies the identity and justification. The target must be a presently registered, unresolved canonical candidate in the independent `missing_candidates.jsonl` index. Incorrect IDs and insufficient rationales are rejected before the amendment ledger is written. References that omit `reviewed_existing_candidate_id` still use deterministic `phrase + context` hashing; there is **no automatic synonym-merging**. A reused reference retains its own original phrase, context and reviewed identity rationale as part of the effective node for audit traceability. `review_preflight` now reports the *actual* candidate ID, whether explicit reuse was requested, and whether a new candidate identity would be generated.

A dedicated `test_candidate_reuse.py` exercises explicit reuse, unchanged default behavior, unknown IDs, insufficient rationales and a whole-workspace preflight/amendment case. **Tests have been committed, but this connector could not independently retrieve the current main-branch GitHub Actions run conclusion or run the entire repo's suite in a local checkout; do not report passing CI or measured speedups until verified.**

### What this improves

In the precise Round178 pattern, a correctly pre-reviewed target can be used **within the same single amendment packet**. This removes the needless new raw identity and the second alias event/commit/graph rebuild *for that pattern*. It does **not** replace mathematical context review and must not be used to force context-sensitive variants together. Previous source/alias data are not rewritten.

## Other priority improvements, mostly operational

1. **Audit once per substantive risk, not by quota.** Many of the 420 canonical candidates are genuinely distinct missing prerequisites. Prioritize wrongly typed existing links, unjustified smallness assumptions, object/variance mismatches, high fan-in candidates, and source statements with verified counterexamples over indefinite low-frequency lexical alias hunts.
2. **One compact effective-graph worklist per session.** Use `dependency_global_audit focus` (which joins current effective amendments and full original parents) rather than repeatedly downloading the million-byte inventory and megabyte amendment ledger through the connector. For a candidate with many incoming sources, opt into `--max-formulations 1000` before claiming all contexts checked. Some GitHub file endpoints return no inline content for large blobs; when connector-only, retrieve the pinned blob after obtaining its SHA, not repeatedly asking the same file endpoint.
3. **Prepare related reviewed decisions together.** `dependency_review_submit` already accepts multiple disjoint packets in one commit. Group same-mode decisions to let `apply_inbox` rebuild once; separate GitHub pushes do **not** benefit from that optimization. Keep bounded complete-node amendments and source/version/occurrence preflight.
4. **Persist nonmerges and reviewed false-positive warnings.** The existing `dependency_audit_acceleration` exact-effective-node reviewer ledger supports suppressing *only* accepted, source/version/occurrence-pinned heuristics. Use it consistently for justified nonmerges and scope conclusions. Never suppress integrity alerts, material changes or an unresolved issue merely because it is old.
5. **Stop multiplying status documents.** Use `WAVE2_CURRENT_HANDOFF.md` + authoritative `STATE.json` for session start, exact immutable receipts as mathematical graph history, and one detailed report only for substantive new mathematical decisions. Do not rewrite giant `WORK_CHECKPOINT.md` on every packet. The existing CI and Pages path filters already avoid many unnecessary runs for internal/docs-only changes.
6. **Measure before deeper engine refactoring.** Existing optimized complete-scan `propose` and same-mode inbox batching are already in place. Further graph caching/mixed-mode batching would carry larger invalidation and crash-replay risks; prefer recording wall-clock baseline and measured Actions run cost before redesigning core event processing.

## Resume contract

Start with the short handoff, then current live graph state. Use source-complete effective-node context and prioritize substantive mathematics. If correcting an existing-target link into an already-registered missing prerequisite, use the explicit reviewed reuse option and preflight it. Preserve original source formulations, append-only provenance, zero premature external research, and separate mathematical/citation/human certification. Do not open consolidation gate or freeze based on these efficiency changes.


## Additional implemented improvement: amortized multi-packet preflight (October 24)

The previous `review_packet_collection` invoked `review_preflight` once per package. Every invocation independently loaded the complete inventory and candidate registry, replayed **all** effective-node amendment history (currently 766 events over 659 formulations), and reloaded the append-only amendment ID ledger. Thus checking `k` independent packets cost approximately `k` effective-graph replays even though all packets used the **same unchanged graph** and repeated formulation IDs were already forbidden.

**Implemented:** `dependency_review_preflight.prepare_review_context()` prepares the inventory, effective version-pinned nodes, registered and reusable candidate IDs, and known amendment IDs in a single read-only snapshot. `review_packet_collection` lazily prepares it only for a packet that survives initial independent-package checks and passes it to subsequent `review_preflight` calls. Each packet creates a separate shallow dictionary of effective nodes before simulating amendments; validation of one packet cannot contaminate another. Ordinary standalone preflight remains supported, with fresh authoritative loading by default. No new mutable cache, filesystem cache, relaxed review contract, automatic alias, or graph write is introduced.

**Regression test:** `research_pipeline/tests/test_review_preflight_cache.py` creates two distinct version-anchored amendment packets and asserts that `live_nodes` is invoked exactly once for the batch, that both receive valid read-only mechanical validation, and that the live graph files and event ledgers remain unchanged. It also tests default standalone preflight independently.

**Expected operation-count benefit:** for a single same-state review of `k` disjoint packets, full effective-node replays fall from `k` to **one**. For example, 5 reviewed packets avoid 4 redundant full graph replays (**80% reduction in this suboperation**); this is not a measured 80% wall-clock improvement. The end-to-end action still performs mandatory separate graph processing when approved amendments are actually applied.

**Verification boundary:** Code and tests are committed. This connector session still does not expose successful current Actions conclusions or a runnable repository checkout, so neither the new batch regression nor the full suite is claimed to have passed. Verify via the automatic `Research pipeline isolated tests` workflow before treating the optimization as production-proven.

### New operational default

For a batch of independently source-reviewed corrections: construct complete version-pinned packets off-line, use the existing `review_packet_collection` validation with one shared in-memory context, stage them **once** after approval, commit together, and confirm the unique receipts and authoritative `STATE.json` after processing. Repeating ad hoc one-packet GitHub commits defeats the already implemented same-mode graph-rebuild coalescing.
