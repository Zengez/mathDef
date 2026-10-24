# Wave2 independent source-free dependency audit — Round 184 (2026-10-24)

## Scope, provenance, and starting checkpoint

Continued from the current handoff / Round183. Audited the **effective** current `dependency_graph/edges.jsonl` (not stale base formulation snapshots), all screened and provisional independent meaning records as needed, the append-only historical seed ledger, a broad sample of contextual candidate aliases, and current CI validation. No external research for missing definitions, production mathDef source, Wave1 modifications, Batch143 expansion, new meaning population, unreviewed aliases, citation certification or consolidation gate action.

Starting STATE: 611 meanings; 659/659 scanned formulations (639 screened / 20 provisional); 728 raw missing candidates; 421 unresolved canonical classes; 300 explicit alias decisions; 7 resolutions; 843 effective missing occurrences; 770 scan amendments; 19 seed overrides; zero ambiguous and unassigned; gate FALSE.

## Corrected residual **effective** small-groupoid seed — verified applied

### Source-specific mathematical review

Independent source `form.74cd6dc48e0606fc.setoid-category` states:

> A setoid is a groupoid C in which every object has only its identity automorphism; equivalently, between two objects there is at most one arrow, and its existence is an equivalence relation.

A **groupoid** has invertible arrows; requiring smallness is an additional restriction on collections of objects/arrows. Nothing in this setoid statement assumes a small groupoid, and the earlier Round179 mathematical review explicitly removed the unsupported size requirement from its **scan** reference.

The graph-wide review detected that an **independent historical seed** survived: `rel.wave2.batch06.setoid-category.to.small-groupoid` remained an effective `preexisting_relation` edge to `meaning.wave2.foundation.small-groupoid`. A corrected scan alone does not remove this seed. Preserving a historically false target would therefore defeat the previous correction even when the full scan was mathematically correct.

Applied source-version-anchored historical seed override `seedoverride.wave2.review184.001`, using the existing canonical source-reviewed prerequisite `missing.1ebe938ec77d5606093e` for an ordinary **size-unrestricted groupoid**. Original source wording, original seed relation ID, target provenance, alternative proper `Groupoids` source convention and all frozen materials are unchanged.

- Inbox packet: `dependency_graph/inbox/wave2-sourcefree-round184-setoid-seed-size-override.json`.
- Exact receipt: `dependency_graph/applied/wave2-sourcefree-round184-setoid-seed-size-override.json`, SHA256 `afe9b2d060cf70c3f9110c54427feaf62c204328f2aabe1426c34d9dc3b31051`, status `applied_in_independent_graph_only`, `human_certified=false`.
- [Packet commit](https://github.com/Zengez/mathDef/commit/87be929bc65cd74cdfe220920e968949aaef0bc5), [dependency graph Action succeeded](https://github.com/Zengez/mathDef/actions/runs/40098074079).
- **Afterward:** effective `edges.jsonl` has **no** setoid→small-groupoid edge; its remaining setoid existing-edge dependency is the equivalence relation. The original historical seed remains immutable behind the override, and the canonical groupoid missing occurrences account for both the formerly corrected scan and overridden seed.

Only one unintended small-groupoid seed remained; the existing literal `F:C^op→Groupoids` target category in `form.f0d993a60533fc99.groupoid-valued-presheaf` intentionally invokes **small** groupoids and is preserved. The current small-category effective edges were reviewed against source declarations (finite index category, explicitly small source category, site, and small groupoid); no additional unsupported small-category seed was established.

## Repaired failing validation without dropping rigor

The initial packet triggered a successful graph rebuild but exposed **two already-latent CI problems**:

1. `test_dependency_seed_overrides.py` had hard-coded **420** canonical missing classes and exactly **19** historical seed events, despite Round179 having raised the class count to 421 and Round184 properly adding a twentieth event. The replay regression now verifies invariant counts against its **current baseline**, checks the original 19 relation IDs within the expanded historical ledger, restricts its source-relation assertions to the Round177 cohort, and compares unrelated groupoid-scope flags before/after the idempotent replay. Thus it remains a meaningful check as the reviewed graph evolves. [Test correction](https://github.com/Zengez/mathDef/commit/caefe5c238af4038bfca88e53f2d648184d54088).
2. Once those tests passed, the **strict global audit** surfaced `stale_missing_identity` on Round180's legitimate explicitly reviewed reuse of existing clopen prerequisite `missing.b599bdc9343a25050226`. The original phrase/context intentionally does not rehash to that previously registered canonical candidate, and the reviewed amendment carries `reviewed_existing_candidate_id` and substantive `candidate_identity_review_rationale` evidence. The global scanner now exempts **only** such explicitly tagged, reasoned reuse; it continues to reject unregistered IDs, accidental phrase/context mismatches, mismatched reuse markers and inadequate review rationale. Additional regression tests exercise all of those cases. The validated reviewer is recorded in the amendment event, not necessarily in each effective reference. [Code correction](https://github.com/Zengez/mathDef/commit/82cd896c03428921a855abdf4e2a2bda0ecf9cbd), [regression coverage](https://github.com/Zengez/mathDef/commit/776c92bbbf4445560169056301a4c1fba1920a2d).

CI now prints concrete integrity flags before still enforcing the strict failure condition: [diagnostic change](https://github.com/Zengez/mathDef/commit/45f554ec31b938b8bccdda96f51ea588353c4543). After these fixes, [latest Research pipeline isolated tests **SUCCEEDED**](https://github.com/Zengez/mathDef/actions/runs/40098617697), including **160 Python tests** (159 existing + one new), read-only global audit checks, and following workflow steps. This is operational validation, **not** mathematical/citation certification.

## Additional distinct graph integrity observation — candidate-resolution variant cycle

Independent cross-check of all 2,647 **effective** existing dependency edges finds exactly **one two-meaning loop** when **candidate-resolved edges** are included:

- `form.wave2.analysis98.metric-space.compatible` (alternative metric-space/topology presentation) → `meaning.wave2.directional113.open-metric`, origin `scan:candidate_resolution`.
- `form.wave2.directional113.open-metric` → `meaning.wave2.analysis98.metric-space` (normal direct dependency).

This is **not** necessarily mathematically foundational circularity: the **other** formulation `form.wave2.analysis98.metric-space` defines a metric directly by distance axioms, without needing an open ball, so a definition-expansion system can break the variant-level cycle by choosing the foundational metric formulation first. Both original edges are contextually warranted and were not altered.

**Next technical audit lead:** the global scanner's `cycle_components` currently does **not** include `scan:candidate_resolution` edges in its adjacency, while the authoritative derived `edges.jsonl` does. Therefore its reported zero cycles is true for its *restricted adjacency*, not for the whole effective meaning-level graph. Review how to expose both (i) full effective meaning-level SCCs including resolved-candidate links and (ii) genuine unavoidable / formulation-choice dependency cycles, without treating this benign alternative-formulation loop as an automatic graph error or making CI falsely fail. Maintain existing path-based expansion loop guards.

### Reviewed aliases/nonmerges

Sampled historical 300 context-reviewed candidate aliases for conceptual conflation, including comma categories `(j↓H)` versus `(H↓j)` (distinct directional **instances** of an ordinary comma-category construction), ordinary surjectivity under topology/module/ring maps, natural isomorphism of covariant versus contravariant functors (the abstract natural-isomorphism prerequisite is generic), and set intersection for convex/closed/affine supersets (the underlying intersection operation is common; the parent family predicate remains distinct). Found no new independently justified alias split requiring a correction in this sample; do not interpret these as proof that the parent mathematical structures are interchangeable.

## Authoritative end-of-round state

- **611** independent meanings, **659/659** scanned, including **639 screened / 20 provisional**.
- **728** raw missing candidate records, **421** unresolved canonical identity classes, **300** explicit aliases, **7** resolutions; **844** effective missing occurrences (one extra reviewed seed provenance).
- **770** complete scan amendments; **20** historical seed overrides.
- **0** ambiguous / unassigned; **651** structurally open / **8** closed; consolidation gate **FALSE**.
- Inventory SHA256 unchanged `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`; unresolved fingerprint `61246db4cb0897ac3bfdb43f8a8e6be361e2f05bf905367bfbda0b388a541113`.

No new source content, independent population reconciliation, missing-definition external research, human review certificate or citation certificate. Round183's topological ring/module inversion-continuity scope finding remains an unresolved source-convention issue.

**Next:** Round185 should check full effective graph SCC reporting including candidate resolutions; prioritize new high-impact mathematical target mismatches and protect the contextual split between generic and small structures. Preserve original mathematical records and closed consolidation gate.
