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
