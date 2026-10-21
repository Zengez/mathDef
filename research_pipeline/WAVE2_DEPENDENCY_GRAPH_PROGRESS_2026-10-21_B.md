# Independent Wave2 dependency graph — implementation continuation 2026-10-21

**Scope:** Follow-up to the first dependency-first pilot. Read the agreed TEMP_DEPENDENCY_FIRST_WAVE2_PLAN.md §8 before further implementation. All changes are isolated to the independent reconstruction infrastructure and graph. No original production mathDef content was read or compared, no independent Wave1 artifact was edited, and no screened or provisional mathematical content was promoted, modified or published.

## Implemented and committed

- **Replay-safe semantic scan amendments.** Original per-formulation node files are immutable after review. Append-only amendments.jsonl events capture complete replacement scans, exact prior-node digest, formulation version, rationale and reviewer. Replaying a stale/broken chain fails closed (unscanned/Open) rather than accepting incomplete adjacency. Original remains recoverable and untouched.
- **Reproducible graph batch intake.** Committed independent dependency_graph/inbox/*.json files explicitly specify mode ingest/amend/resolve, unique filename-aligned ID, and schema version. The graph Action synchronizes the inventory, applies batches, writes receipt-last SHA-bound applied/ records, then generates a small bounded set of lexical proposals. Unchanged batches replay without duplicate effects.
- **Safer contextual suggestions.** Cross-domain exact word matches are now flagged as ambiguous rather than automatically resolved. The mathDef proposal adapter's SHA digest is stored as a versioned invalidation fingerprint, allowing only unfinished, unreviewed lexical proposals to be refreshed following matching-rule changes.
- **Correct effective rooted trees.** On-demand traversal uses persisted resolved occurrences, including corrected scans and missing-meaning resolutions; it retains cycle-closing edges without expanding cycles indefinitely.
- **Population integration.** The independent population Action automatically resynchronizes the graph inventory when new provisional research is applied. The generic queue planner defers old unrelated-breadth proposals while the explicit graph checkpoint keeps unrelated breadth on hold.
- **Additional deterministic tests.** The test suite now covers scan amendment replay, stale/corrupt amendment chains, source-code-fingerprint provisional refresh, conservative cross-domain ambiguity, resolution-aware tree expansion, and partial inbox replay/receipt integrity.

## Actual observed pilot state

Most recently read committed STATE.json:

- 611 distinct contextual meanings; 659 formulations.
- 639 screened forms and 20 separately provisional forms from earlier research.
- 440 scan_incomplete lexical proposal snapshots; 219 not yet scanned.
- 0 complete semantic formulation scans, 0 Closed formulations; 659 Open.
- 891 prior seeded prerequisite relations; 356 lexical occurrence suggestions.
- 192 ambiguities; 5 existing deferred missing-meaning candidates; zero appended semantic scan corrections on real mathematical records.

These numbers count non-exhaustive machine *proposals*, NOT completed mathematical scans. A proposal can list zero matches without being complete. The increase in ambiguities partly reflects the deliberately conservative cross-domain matching rule and adapter refresh.

## Verification

At this checkpoint, dedicated graph Action 39661628196 succeeded, and isolated pipeline test runs 39661589464 and 39661356164 passed. More recent code/documentation commits may trigger another independent test run; check the latest run status before drawing a green conclusion for the final HEAD.

No new real provisional population package was admitted during this follow-up chunk, so the new production-to-graph synchronization path has been code-reviewed and fixture tested, but not yet demonstrated with a new independent research batch.

## Next priority

1. Verify current graph status, CI and saved adapter fingerprints.
2. Perform a representative *exhaustive* contextual semantic reference review on a bounded group of formulations and save each as a GitHub-committed version-bound inbox scan package. Inspect the real edges and missed references against original independent reconstruction **only**.
3. Test the Action auto-applied receipts against an actual reviewed graph scan batch, including clean-checkout recovery.
4. Implement reviewed missing-meaning synonym/alias merging and a versioned resolution-correction ledger without rewriting existing candidate IDs.
5. Work missing contextual meaning clusters via independent source-backed provisional package intake; scan newly added forms and propagate Open/Closed statuses incrementally.
6. Only after dependency stabilization reconsider unrelated breadth. Batch143 remains on hold.

The detailed operating procedure lives at research_pipeline/DEPENDENCY_FIRST_WORKFLOW.md; durable state is in reconstruction-v2-independent/dependency_graph/{INVENTORY.json,STATE.json,CHECKPOINT.json}. The latest resume_plan.json references these files.
