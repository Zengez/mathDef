# mathDef independent reconstruction — Wave 2 checkpoint E (2026-10-19)

**Authoritative state as verified by repository data immediately before this report.** Always recheck GitHub main and Actions before assuming this checkpoint is latest. This supersedes status/counts in `research_pipeline/WAVE2_PROGRESS_2026-10-19_D.md` while retaining the earlier mathematical and source audit history.

## Persisted screened research status

| Component | Latest verified committed count |
| --- | ---: |
| Approved independent source registrations | 9 |
| Independent source term/heading records | **343** (318 frozen Wave 1 + 25 added Wave 2) |
| Individual source observations | **766** (749 frozen Wave 1 + 17 new) |
| Independently screened contextual meanings | **435** (419 frozen + 16 new) |
| Individually covered formulation reviews | **447** (431 frozen + 16 new) |
| Existing screened prerequisite relationships | **545** (445 frozen + 100 new) |
| Current review dispositions | **419 linked, 22 no-supported-target, 2 held ambiguity, 4 pending link review** |
| Source research held without screening | 8 inaccessible EoM locators, plus 27 inherited access blocks and 59 inherited no-suitable-definition cases |
| Stages sealed | **0** |

The four newly screened Stacks meanings are (1) a nonzero commutative unital **field**, (2) ordinary **covariant functor**, (3) small **groupoid**, and (4) **pseudofunctor into a strict 2-category**. Their source identity and exact conventions were checked against Stacks tags **09FD**, **001B**, **0018**, and **003N** respectively. The pseudofunctor meaning retains invertible unit/composition comparison 2-morphisms and all coherence equations; do not treat it as an ordinary strict functor.

The updated four-meaning screening report is committed as `state/wave2_new_foundations_batch_06_screened.json`. Its commit is `10bd29c1a2493a`. A prior attempt of the screen workflow failed because the intake pseudofunctor source key was `pseudo-functor-strict-2category` while the meaning key was `pseudofunctor-to-strict-2category`; the fix `f48452a37f5b` explicitly maps the IDs **without weakening evidence checks**. The corrected run [39283736766](https://github.com/Zengez/mathDef/actions/runs/39283736766) generated the committed output. The web/API may lag in marking the job terminal; verify the final conclusion separately.

## Fixed original research backlog — a useful denominator

The untouched independent Wave 2 prioritized research queue has **192** cases, of which **93** are original missing-foundation/ambiguity relation cases. At the **545-link** checkpoint:

- **72/93 (77.4%)** now have at least one source-screened mathematical prerequisite relationship.
- **21/93** still have no such relationship: 19 missing-foundation cases, 2 held cases.
- Remaining **99** original source/variant/collection tasks: 27 blocked source investigations, 59 previously unproductive sections, 4 cross-source variants, 9 source collection resurveys.
- Thus **120/192** original priority tasks are **not demonstrated complete** by this conservative relation-based benchmark. A linked source formulation may still have other missing prerequisites.
- The separate **3,599** generic discovery leads do not represent 3,599 known definitions.

Per-original-task append-only overlay saved at `state/wave2_priority_reconciliation_2026-10-19.jsonl`, summary at `state/wave2_priority_reconciliation_2026-10-19.json`. Reproducible engine `research_pipeline/engine/wave2_priority_progress.py`, triggered by `.github/workflows/mathdef-wave2-priority-reconcile-after-links.yml` only after a successfully screened relationship batch. It will not automatically mark source research tasks complete or alter the immutable original priority queue.

## Pending workflows — do not count output before success

1. **New 18-link relationship batch** sourced from Stacks foundational meanings and historically held cases: `intake/wave2_curated_relations_batch_06.jsonl`. The guarded code supports batch 06, checks exact source anchors and catalog digests, asserts no cycles, and requires the audited 443-review historical snapshot. Trigger: `.github/workflows/mathdef-wave2-links-batch6-on-meaning-review.yml` after a successful 4-meaning workflow. Latest detected queued run: [39283843058](https://github.com/Zengez/mathDef/actions/runs/39283843058). **No `state/wave2_link_review_batch_06.json` committed yet**; current screened link count remains **545**, not 563. If it passes, expect 563 screened links, 435 meanings, 447 reviews and four previous pending source formulations linked.
2. **Four source observations from ProofWiki**: monoid, general/internal binary operation, typed/graph binary relation, binary Cartesian product, with mathematically distinct contexts. Source evidence at `wave2/direct_source_research_foundational_algebra_sets_batch_2026-10-19.jsonl`; reviewed source-intake module `research_pipeline/engine/wave2_foundations_batch6_settheory.py`; workflow `.github/workflows/mathdef-wave2-source-intake-after-batch6.yml` depends on successful 18-link screen. If verified: 347 source term records, 770 source observations, 563 links. Do not mistake four observations for already screened meanings.
3. **Six explicitly context-specific elementary meaning proposals**: monoid; general binary operation; internally closed binary operation; typed binary relation; graph-only binary relation; binary Cartesian product. Proposals at `wave2/foundational_meaning_proposals_batch_07.jsonl`. Guarded mathematical review script `research_pipeline/engine/wave2_screen_elementary_foundations.py` (source-key and syntax checks implemented), dependent workflow `.github/workflows/mathdef-wave2-screen-elementary-after-source-intake.yml`. If this passes, expect **441** meanings and **453** formulation reviews (6 newly `needs_review`), with 563 preserved links. The 447 previously reviewed formulations are snapshotted exactly before digest rebasing.
4. **Next 11 source-exact elementary prerequisite relationships**, currently only prepared under `intake/wave2_curated_relations_batch_07.jsonl`. Examples: group → monoid, ring → internal binary operation, preorder → graph-based binary relation, both relation variants → Cartesian product. They require the six new meanings to pass screening first. Guarded by `research_pipeline/engine/wave2_apply_links.py` and `.github/workflows/mathdef-wave2-screen-elementary-links-batch7.yml`. If the chain succeeds, expect 574 links with 441 meanings, 453 reviews and 1 unlinked Cartesian-product formulation requiring a separate source-specific no-target review. **Do not report 574 as completed before the exact workflow passes.**

All pending source and mathematical screening jobs share `mathdef-independent-wave2-writes` concurrency group and have individual source-link and historical-ledger checks. Read failed job logs before retrying. A prior source screen was aborted by Python syntax error and that was repaired; standard isolated CI now globally compiles Python modules before its 52 tests.

## Additional independently verified source research (not yet ingested)

- `wave2/direct_source_research_ordered_pairs_subsets_and_mapping_variants_2026-10-19.jsonl`: individually reviewed ProofWiki pages for ordered pairs, proper/non-strict subsets, and several **mapping/function** formulations (element assignment, typed graph, bare graph under fixed ambient domain/codomain). Notes preserve that bare relation graph need not uniquely specify a codomain and alternative set-theoretic pair encodings are not literally the same set.
- `wave2/direct_source_research_foundational_algebra_sets_batch_2026-10-19.jsonl`: four earlier ProofWiki source investigations for monoids, binary operations, binary relations and Cartesian products.
- Eight inaccessible Encyclopedia of Mathematics source locators were directly retried and documented with HTTP 502; do not bypass access limits or relabel a Stacks definition as Encyclopedia evidence.

## Nonnegotiable independent-reconstruction constraints

**Frozen Wave 1** at `research_pipeline/experiments/reconstruction-v1-recovery` has publication digest `7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801`. It is immutable. The 2026-10-19 correction of two inherited Stacks presheaf mathematical errors occurred solely in the **editable independent Wave 2**, with explicit candidate-to-screened revision events and source evidence; review history and all earlier links preserved.

Never consult the original live production mathDef definitions/variants/citations for this research, and do not compare against production until Wave 2 has been independently completed and **frozen**. Never auto-approve mathematical links by matching words. Respect source access and licensing. **High thinking** recommended for source/context and definition review. All Wave 2 stages remain **UNSEALED**.

**First next task:** inspect latest main, active four-meaning job and batch-06 link workflow logs/report, then continue from the last *verified* commit. If linked batch06 fails, identify and fix its concrete error before running dependent source/meaning batches.
