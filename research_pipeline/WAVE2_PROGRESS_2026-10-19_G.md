# Independent mathDef Wave 2 — verified checkpoint G (2026-10-19)

**Authoritative continuation state:** Verify latest `main` and all GitHub Actions results before resuming. This report supersedes earlier checkpoint counts while preserving their provenance and research history. Latest verified relationship result commit: `2058b4403e64e23`; latest authored change before report: `d0adceb7fcdc93a`.

## Verified committed independent research status

| Measure | Current |
|---|---:|
| Approved source registrations | 9 |
| Discovered source-term records | **354** (318 frozen Wave 1, 36 new Wave 2) |
| Source observations | **777** (749 frozen, 28 new) |
| Screened distinct contextual meanings | **453** (419 frozen, 34 new) |
| Individually dispositioned formulations | **465** (431 frozen, 34 new) |
| Screened definition links | **600** (445 frozen Wave 1, 155 new) |
| Reviewed formulations with at least one linked prerequisite | **457** |
| Formulations reviewed as no currently supported prerequisite | **7** |
| Source/context-held ambiguities | **1** |
| Formulations lacking any first review decision | **0** |
| Stages sealed | **0** |

**These are current investigated-source counts, not the size of mathematics.** The seven no-target formulations include four elementary set/assignment primitives deliberately left unlinked rather than inventing an inappropriate directed dependency. One arbitrary 2-category equivalence formulation remains held because only a *strict* 2-category source was independently reviewed.

Historical reviews for all 459 earlier formulations are preserved as `state/wave2_formulation_reviews_snapshot_459_before_foundations10.jsonl`; batch 10 source/meaning review evidence and 18 relations are separate. Seven original no-target dispositions were individually reassessed after new source-grounded meanings became available.

## Workflow execution — verified

- [Review four elementary primitives (39301240745)](https://github.com/Zengez/mathDef/actions/runs/39301240745) — **success**, all 459 reviewed cases dispositioned without inventing membership/set-theory prerequisites; 582 screened relationships retained.
- [Four-source intake (39301858602)](https://github.com/Zengez/mathDef/actions/runs/39301858602) — **success**, term records 350→354 and source observations 773→777 with original 350-term individual coverage snapshot.
- [Per-term source coverage (39301939814)](https://github.com/Zengez/mathDef/actions/runs/39301939814) — **success** after fixing outdated workflow cardinality guard that only allowed 336/339 terms.
- [Six contextual meaning screens (39302445333)](https://github.com/Zengez/mathDef/actions/runs/39302445333) — **success**, 447→453 screened meanings, 459→465 reviews. An earlier run 39302291558 failed because the new evidence was accidentally assigned an existing historical review filename; corrected to `foundation_meaning_review_batch_10.jsonl` before rerun.
- [Eighteen individual prerequisite links (39302995223)](https://github.com/Zengez/mathDef/actions/runs/39302995223) — **success**, 582→600 screened links, no cycles, 457 linked review entries, 7 no-target and one held ambiguity. All 445 frozen Wave 1 link records retained and all 465 reviews represented in the live ledger.

The standardized 192-priority benchmark generator is `research_pipeline/engine/wave2_priority_progress.py`, with report `state/wave2_priority_progress_current.json`. **The report most recently inspected was stale** (82 of 93 original gap tasks now linked, 11 still unlinked, based on 574 links). Workflow `.github/workflows/mathdef-wave2-priority-reconcile-after-links.yml` was updated to watch the successful 600-link screening workflow, but its new outcome must be checked before using any refreshed priority percentage. Do not confuse 192 original priority tasks with the separately collected 3,599 generic research leads.

## Source-specific mathematical findings

The six newly screened independent contextual meanings explicitly preserve:
- **Reduced ring:** no nonzero nilpotent elements in an associative ring, without imposing a unit or commutativity.
- **General ring homomorphism** versus **unital ring homomorphism**: operations preserved in both, but preservation of `1` is an extra axiom in the unital formulation. The precise independent reference was ProofWiki Definition:Ring Homomorphism.
- **Well-ordered set:** total ordering with a least element in every **nonempty** subset. ProofWiki source prose has the correct quantification while one display omits nonemptiness; the latter omission was not reproduced.
- **General subspace topology** on `A⊆X`, permitting empty `A` under the chosen general topology convention, versus a restricted nonempty-subspace usage.

The exact source research note is `wave2/source_notes_algebra_order_topology_2026-10-19.jsonl`, candidate intake `intake/foundations_batch_09_observations.jsonl`, meaning screens `wave2/foundation_meaning_review_batch_10.jsonl`, screened mathematical link batch `intake/wave2_curated_relations_batch_10.jsonl`, accepted report `state/wave2_link_review_batch_10.json` and source review coverage `state/wave2_term_coverage.json`. Previously corrected category-valued and groupoid-valued presheaf variance/strictness remain documented with their audited second-wave revisions.

## Original source and independence safeguards

Frozen corrected Wave 1: `research_pipeline/experiments/reconstruction-v1-recovery`, publication digest `7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801`. Every relevant workflow checks the frozen publication hash, relation identities, stage states, source locators and individual review provenance. **Do not read or consult the original production mathDef definitions, variants or citations and do not compare with production until the independent Wave 2 is completed and frozen.** No human mathematical peer review has been claimed; licensed source prose is independently paraphrased.

Remaining acquisition/access limitations: eight new Encyclopedia of Mathematics locators direct-rechecked with HTTP 502, 27 inherited blocked source investigations, and 59 inherited no-suitable-definition section outcomes. They remain under active research, not silently marked complete.

## Next work — High reasoning

1. Confirm the 600-link priority-reconciliation workflow completed and accurately refresh the 192-item original priority baseline metric.
2. Individually source and examine remaining gap concepts: Grothendieck site/covering family, generic indexed family equivalence, kernel/cokernel/exact sequences for the snake lemma, and the arbitrary weak 2-category/bicategory equivalence case. Preserve math distinctions; do not link because keywords match.
3. Research and retain separate formal variants for mappings (typed graph versus graph-only), set-theoretic primitives (membership not invented as defined), quotient versus subspace topology, and order-theoretic well-order versus ordinal.
4. Further source/intake batches must version prior source and review snapshots before rewriting derived digests; keep all Wave 2 stages unsealed and complete individually justified mathematical screens.
5. After truly extensive independent coverage, seal and freeze Wave 2. Only then run the first comparison with the original production mathDef corpus.

**No user action required.** No further stage may claim completion from a queued workflow alone; read its committed result and job logs.
