# Independent Wave2 source-free audit — Round 175 (October 23, 2026)

## Verified result: 18 exactly anchored historical seed-retarget previews; 2 deferred

This round addressed the twenty size-scope review leads identified in Round 174, **without editing the original screened or provisional formulations, seed relations, independent dependency graph, or original production mathDef**.

**Source-free provenance:** live independent `INVENTORY.json`, `STATE.json`, and canonical `missing_candidates.jsonl`. No external reference/source research and no human certification. The preflight uses only the current source inventory, original complete immutable seed records and their source version, the canonical missing-candidate registry with its registered incoming source IDs, and the existing alias list. Nothing was submitted to `dependency_graph/inbox/`.

### Final triage

- **16 justified preview redirects:** 16 old seed edges `→ meaning.wave2.foundation.small-category` instead propose `missing.fcb5ab865c6d9dbb3d79`, the already registered **category (size-unrestricted)** candidate. Example: a terminal object, a monoidal category, or a monomorphism exists meaningfully in locally small categories whose collection of objects is not a set. The old target imposes an unsupported size restriction.
- **2 justified preview redirects:** 2 old seed edges `→ meaning.wave2.foundation.category-functor` instead propose `missing.c5104821c3c70afa1f63`, already registered ordinary **functor F:C→D** without globally small domain/codomain. They concern the *left adjoint* and *covariant representable functor* formulations. Natural bijections and preservation of identity/composition remain source-specific conditions.
- **1 deferred for candidate-to-source provenance:** `rel.wave2.batch03.category-limit.to.small-category`. The underlying concept probably calls for an unrestricted category, but `form.8f7683667fac9d28.category-limit` is **not an incoming source** currently registered for `missing.fcb5ab865c6d9dbb3d79`. Do not silently reuse the candidate without an explicit full-source linkage and reviewer confirmation.
- **1 deferred for size-convention ambiguity:** `rel.wave2.batch06.setoid-category.to.small-groupoid`. The source says groupoid with trivial automorphism groups but does not specify an underlying set/universe. Equivalence-relation-on-a-set setoids are small, whereas an unrestricted thin groupoid can be large. Do not replace the existing target with generic category (which loses invertibility) or assert the conventional setoid size without further review.

The 18 reviewed seed relationships represent **18 of the 20 warnings**, not new mathematical definitions or a reduction of the 420 unresolved canonical missing identities. The category/functor candidates were already registered from the completed independent contextual scan; their query strings and contexts are preserved, not invented here.

### Portable, exact, version-pinned proposal manifest

[Read-only proposal manifest](review_proposals/WAVE2_SEED_SCOPE_ROUND175_READONLY.json)

**File:** `research_pipeline/review_proposals/WAVE2_SEED_SCOPE_ROUND175_READONLY.json`

Each proposed change contains:
- Original immutable `relation_id` and **complete original seed record** for exact-match validation (every field, not merely a display phrase).
- Original source formulation ID and `version_sha256` (protects against a changed mathematical formulation).
- Explicit old meaning target; proposed `state=missing` and one of the two **registered canonical** candidate IDs above.
- Separate mathematical rationale explaining why the narrow target overrestricts the parent.
- Inventory hash, seed-relations hash and unresolved graph fingerprint binding the entire proposal to the exact current corpus.
- Two explicit deferrals and their reasons, excluded from the executable preview changes.

**Authoritative anchor values:**
- Independent source inventory: `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`.
- Seed relation registry SHA256: `e39a19f0366494d8a1d19c6dbcede6e949c48f4104c857dd690c2c062b24698f`.
- Unresolved fingerprint: `f740c264e171ba568241e8925c32efd5e53d8f528f8976fd7e9f9308a7300554`.

### Safe reusable preview validator implemented

New `research_pipeline/engine/dependency_seed_retarget_preview.py` performs **read-only preflight** of historical-seed change proposals. It rejects:
1. Stale inventory, independent seed registry, or unresolved-graph fingerprint.
2. Unknown/duplicate seed IDs, altered source formulation IDs or versions, changed old target meaning, and changed original seed evidence.
3. Unresolved candidates that have been aliased, resolved to existing meanings, are unknown, or are not marked `unresearched`.
4. Candidate IDs without a registered incoming occurrence from the same mathematical formulation.
5. Undocumented or mathematically unreasoned changes (minimum substantive rationale).
6. Unsupported replacement types: only an existing, canonical **missing** candidate is permitted during this proposal phase.

The validator returns old target, proposed candidate and full source context; **it has no graph-write/apply mode or import path into the graph dispatcher**.

Run when the same snapshot is available:

```bash
python -m research_pipeline.engine.dependency_seed_retarget_preview \
  --workspace research_pipeline/experiments/reconstruction-v2-independent \
  --manifest research_pipeline/review_proposals/WAVE2_SEED_SCOPE_ROUND175_READONLY.json
```

Separate tests cover exact-match portable seed records; invalid/missing candidates; aliased/resolved identities; missing incoming source evidence; duplicate IDs; weak rationale; state/version staleness; and nonmutation of both graph snapshot and decision manifest.

**Crucial live regression test:** `test_live_round175_proposals_are_valid_at_original_snapshot` loaded the actual independent Wave2 graph, compared its seed and unresolved fingerprints to the manifest, and validated all **18** real proposed changes. The GitHub Actions log confirms this test ran and returned **ok**, rather than being skipped.

**Verified [research pipeline CI run #40052846242](https://github.com/Zengez/mathDef/actions/runs/40052846242): SUCCESS, 142 tests, including the live Round 175 manifest check.**

Code/test/proposal commits:
- `9ac2cdd247043b468ee563432bde87779c3acb9f` — new standalone immutable-seed preview validator.
- `b2b071ebb8df48339d8c9c8011ca9190752b3480` — synthetic regression coverage.
- `250da5f1e092ee07ed86a0fd4d481bcebd8bd70a` — accept complete original seed record as an exact portable version pin.
- `724833e143e38045abb3fa1b7522eca1fedb8415` — regression for record-based anchoring.
- `56142510940ea16a556b5831c2ab56886f0c377d` — 18-proposal manifest and explicit 2-case deferral.
- `a982d16a06000c29c0cf0148aeba5896076adfa6` — live full-graph regression verifying the manifest.

### Required future *application* contract (design only)

A proposal passing source-based preflight is **not** authority to apply it. To implement a safe seed-correction mechanism later:

1. Add a reviewed **append-only seed override ledger** with unique event ID, exact old seed digest, source formulation/version, and new missing/existing target plus mathematical review rationale. Historical source relation files and `INVENTORY.json` retain the original untouched seed data.
2. During graph replay, independently validate the event chain against its exact predecessor and the current source inventory. Reject duplicate or conflicting overrides; retain stale historical events for provenance without applying them to newer source versions.
3. Rebuild **all** relevant derived views from a *single effective seed resolver*: adjacency, occurrence and reverse indexes, blocker counts, unresolved fingerprints and state/checkpoint. The original seed link must be suppressed **only in the effective replayed graph**, not deleted from immutable history.
4. Ensure crash-replay atomicity, deterministic rebuild, no double-counting, explicit accepted receipt status, review evidence and no automatic setting of `human_certified` or `consolidation_gate_valid`. Test conflicting edits, partial write/replay, version changes, preserved original historical data, candidate alias state and complete fingerprint changes.
5. Do not apply this hypothetical mechanism until separately verified with isolated CI and mathematical sign-off; the present read-only preview is **not** a substitute for these requirements.

### Live quantitative checkpoint and phase constraints

**All effective graph counts UNCHANGED from Round 174:** 611 independent meanings, 659/659 scanned formulations (639 screened, 20 provisional), 724 raw missing candidate identities, 297 reviewed aliases, 7 candidate-to-existing resolutions, **420 unresolved canonical missing identities**, 819 missing occurrence rows, 765 amendment events, zero ambiguous/unassigned, 651 structurally open/8 closed, consolidation gate FALSE. Inventory/unresolved SHA fingerprints unchanged as above.

No external citation research, missing-definition population, Batch143 breadth expansion, source formulation revisions, Wave1/prod changes, consolidation, automatic graph promotion or human certification.

**Next round priority:** independently review the two deferred cases, then implement and test the append-only **seed override replay** in a separate controlled pass if the source-free phase and explicit review contract still authorize it. Do not submit the 18 proposals directly as legacy relation rewrites or pretend the preview mutated the graph.
