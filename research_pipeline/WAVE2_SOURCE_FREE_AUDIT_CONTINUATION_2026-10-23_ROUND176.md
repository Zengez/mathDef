# Independent Wave2 source-free audit — Round 176 (October 23, 2026)

## Outcome: tested append-only historical-seed replay, and repaired an actual two-hop alias integrity defect

**No historical seed override was submitted or applied.** This round implemented and independently tested the ability to preserve immutable original seed relations while applying approved, exact/version-anchored overrides to the *effective* graph. During review of the two deferred Round175 links, we found and corrected a wider problem: older alias events could form multi-hop chains, but the old effective-graph replay did not follow them to the final canonical identity.

### A. Source mathematical review of the two deferrals

1. **Limit of a diagram** `form.8f7683667fac9d28.category-limit`: the definition concerns a diagram `F:I→C` with an ambient category `C`; there is no global small-category assumption. The historical seed `rel.wave2.batch03.category-limit.to.small-category` imposing `meaning.wave2.foundation.small-category` is over-restrictive. Unlike what Round175's stale *derived registry* suggested, the effective node **does** contain a registered size-unrestricted prerequisite:
   - Observed phrase “categories I and C” has candidate `missing.74e6fe8f36dca77abf73`.
   - Historical alias `alias.global-audit.20261023.003` points this to `missing.5d09c68ceead2919f965`.
   - Later alias `alias.global-audit.20261023.199` points the intermediate to final `missing.fcb5ab865c6d9dbb3d79`, the general unrestricted-category candidate.
   - The **source is legitimate**; failure to show incoming membership was a canonical-alias replay bug, not missing mathematical provenance.

2. **Setoid category** `form.74cd6dc48e0606fc.setoid-category`: the full source defines a groupoid with trivial object automorphism groups. Over an actual set of objects, this is a small thin groupoid; a large thin groupoid over a proper class is also possible in a class/universe setting. **Smallness is not stated.** Retain a context/size-convention review, and do not replace a groupoid with an arbitrary category because that would drop invertibility. The effective source already correctly treats “identity automorphism” as a defining condition and separately records the automorphism-group prerequisite. No new link was issued.

Thus **19 of the original 20 historical seed size warnings** now have *read-only, exact* correction proposals: **17** unrestricted-category prerequisites and **2** unrestricted-functor prerequisites; **one setoid/groupoid scope convention remains deferred**.

### B. Genuine replay defect: 21 multi-hop historical alias chains

The independent canonical alias registry currently contains **297 applied alias events**. Inspecting the raw append-only event pairs found **21 source-to-target paths of length two** (e.g. `A→B→C`). The old `alias_map` prohibited a chain when the target was already an alias in the event order, but did not reject or flatten the **later canonicalization of a previously used target**. The derived occurrence registry therefore sometimes kept `A` under intermediate `B` instead of final canonical `C`. This hid legitimate source occurrences from final canonical candidates.

**Correction:** `research_pipeline/engine/dependency_graph.py` now builds the direct historical mapping and walks each path to a final canonical identity, detects cycles, and returns the flattened **effective** alias map. **Every original alias event and raw occurrence remains unchanged**. This is a derived-index reconstruction, not retroactive rewriting of mathematical sources or decisions.

The independent graph workflow automatically rebuilt its derived files after the code commit: [graph Action **40053389115**, SUCCESS](https://github.com/Zengez/mathDef/actions/runs/40053389115). The final general-category candidate now records the limit-diagram formulation among its incoming sources, with **43 occurrences from 42 distinct formulations** (previous derived output falsely reported 42 from 41).

The ledger's original direct aliases remain present for audit. The note from Round172 claiming existing chained aliases were impossible under the historic ledger must be **superseded**: they were indeed present and previously mishandled. New decision packets should target the **ultimate** canonical ID; no direct old alias events should be deleted.

### C. Tested provenance-preserving historical seed overrides (mechanism only)

New module: `research_pipeline/engine/dependency_seed_overrides.py`.

- A seed override event pins the **original complete seed digest**, source **formulation version**, original meaning target, proposed canonical missing-candidate identity, original relation ID, reviewer and substantive rationale.
- Rejects invalid/duplicate IDs, conflicting active overrides, a candidate not mathematically observed in the same source, candidates already aliased/resolved, source/seed staleness, and actual alias cycles.
- **Canonical-source validation now follows reviewed alias chains**, so the repaired limit-diagram provenance passes without inventing a source occurrence.
- Preserves the exact original historical **seed occurrence ID** and original target ID in effective occurrence metadata, while substituting only its effective `missing` reference.
- `rebuild` then recalculates adjacency, edges, reverse indexes, missing candidate registry, blockers, unresolved fingerprint, structural open/closed status and checkpoint. The original `INVENTORY.json` and screened relation files are never rewritten by the override.
- `apply_inbox` and the graph CLI now support `mode="seed_override"`, with same-mode packet batching, append-only event ledger, conflict checks before writing and individual receipts with `human_certified=false`. This reuses the independent graph's existing Git-transaction workflow, without automatic gate opening or external research.
- An event tied to a previous source version is retained in history but becomes **inactive** if its source version changes.
- The read-only global audit recognizes effective overrides, so superseded legacy small-category warnings no longer masquerade as live dependency edges.

**Deliberately not done this round:** no `seed_overrides.jsonl` exists in the live independent graph; no new `inbox/seed_override` packet was submitted, so **zero live historical seed link targets have been changed**. These changes implement a guarded application *capability*, not mathematical certification or authorization to bypass review.

Code changes are committed under `research_pipeline/engine/dependency_seed_overrides.py`, `research_pipeline/engine/dependency_graph.py`, and `research_pipeline/engine/dependency_global_audit.py`. Tests under `research_pipeline/tests/test_dependency_seed_overrides.py` exercise end-to-end derived occurrence replacement, deterministic reapplication, original-seed immutability, candidate merging, blocker/fingerprint changes, stale source/seed rejection, rejected alias or unobserved candidate, grouped atomic conflicts, and live historical canonical paths.

### D. Rebased 19-record read-only proposal validated against live graph

The Round175 18-record manifest was correctly invalidated by the rebuilt unresolved fingerprint. **Do not submit stale Round175 proposals.**

New immutable review artifact: [`review_proposals/WAVE2_SEED_SCOPE_ROUND176_READONLY.json`](review_proposals/WAVE2_SEED_SCOPE_ROUND176_READONLY.json).

- **19** complete, source-version-anchored, context-reviewed previews: 17 `→ missing.fcb5ab865c6d9dbb3d79` plus 2 `→ missing.c5104821c3c70afa1f63`.
- Original inventory hash: `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`.
- Historical seed relation registry SHA256: `e39a19f0366494d8a1d19c6dbcede6e949c48f4104c857dd690c2c062b24698f`.
- **Current canonical unresolved fingerprint:** `ed093f80ade539884a779309483eefe54fd34d1030e673a36abc35372fa88125`.
- Exactly one explicit deferral remains, `rel.wave2.batch06.setoid-category.to.small-groupoid`, pending size conventions.

[CI **40053541995** — research pipeline tests SUCCESS](https://github.com/Zengez/mathDef/actions/runs/40053541995): **151 tests**, with one intentional skip for the stale Round175 snapshot. The *new* test `test_live_round176_alias_repaired_proposals_match_sources` ran and returned **ok**. Direct real-graph tests also verified both category and functor two-hop alias paths and that the final candidate's provenance is correctly observed.

### E. Current authoritative checkpoint and caution

The independent live graph's derived state (after automatic rebuilding for canonical alias replay) is:

| Metric | Verified Round176 |
| --- | ---: |
| Original mathematical meanings | 611 |
| Formulations scanned | 659/659 (639 screened, 20 provisional) |
| Raw missing candidate records | 724 |
| Applied reviewed alias events | 297 |
| Candidate-to-existing resolutions | 7 |
| Unresolved final canonical identities | 420 |
| Missing occurrence rows | 819 |
| Original amendment events | 765 |
| Historical seed override events **applied** | **0** |
| Unassigned / ambiguous | 0 / 0 |
| Open / closed | 651 / 8 |
| Consolidation gate | **FALSE** |

The effective unresolved fingerprint changed from `f740c264e171ba568241e8925c32efd5e53d8f528f8976fd7e9f9308a7300554` to `ed093f80ade539884a779309483eefe54fd34d1030e673a36abc35372fa88125` **because canonical candidate attribution has changed**, not because source definitions or number of missing occurrence rows changed.

`scan_occurrences` now correctly reports **3598** rather than 3599: the earlier aggregation mistakenly counted a historical seed occurrence with a candidate-resolution suffix as a new scan occurrence. It is a bookkeeping reclassification, not a deleted reference.

No original production mathDef corpus, frozen Wave1 content, independent Wave2 source definitions, external citations, Batch143, terms, human certification or phase gates were changed.

### Next safe step

The next autonomous round can prepare an **offline inbox-formatted packet** from the new 19-record manifest, run the seed-override preflight against the **current** graph and test unchanged original inventory/seed records. Only then decide whether to submit the explicitly reviewed overrides through the existing independent graph dispatcher. Keep the final setoid size-convention case out of the packet until context is established. Never equate passing CI with mathematical source certification.
