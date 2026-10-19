# Independent mathDef Wave 2 — verified continuation checkpoint (2026-10-19)

## Authoritative verified status

GitHub main at source-intake checkpoint: `767f5567979cb4266c0c82255823689f0f43b09b`. Confirm later commits before continuing. Preserve frozen Wave 1 at `research_pipeline/experiments/reconstruction-v1-recovery` with publication digest `7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801`. Do **not** inspect production mathDef definitions/citations or compare against production while Wave 2 is unsealed.

Current independent Wave 2: `research_pipeline/experiments/reconstruction-v2-independent`.

| Measure | Verified current |
| --- | ---: |
| Approved source registrations | 9 |
| Independent source heading/term records | 339 (318 Wave 1 + 21 Wave 2) |
| Source observation records | 762 (749 Wave 1 + 13 Wave 2) |
| Independently screened contextual meanings | 428 (419 Wave 1 + 9 Wave 2) |
| Individually reviewed formulations | 440 (431 Wave 1 + 9 Wave 2) |
| Screened mathematical relationships | 529 (445 Wave 1 + 84 Wave 2) |
| Formulation reviews: linked | 411 |
| Formulation reviews: no supported target | 27 |
| Formulation reviews: held mathematical context ambiguity | 2 |
| Formulation reviews without an initial disposition | 0 |
| Newly added source observations without screened meaning | 3 |
| Unverified original Encyclopedia of Mathematics locators | 8 |
| Inherited access-blocked source investigations | 27 |
| Inherited no-suitable-definition outcomes | 59 |

All five Wave 2 stages remain **UNSEALED**; none of these counts is peer review. The 3 newest foundations (unit of unital ring, nonzero commutative integral domain, and maximal ideal of commutative unital ring) are direct-source *paraphrase observations only*, not screened meanings or links. Their exact sources and notes are in `wave2/foundation_source_discovery_batch_04.jsonl`.

The Wave 2 source coverage ledger now contains all **339** terms; its prior **336**-term snapshot remains at `state/wave2_term_coverage_snapshot_336.jsonl`. The covered direct-read Wave 2 terms increased from ten to thirteen; eight EoM source locators remain unverified.

## Verified workflow checkpoints

1. First 24 source-grounded links: [GitHub Actions 39271383457](https://github.com/Zengez/mathDef/actions/runs/39271383457) **success**.
2. Second 12 links: [39271973045](https://github.com/Zengez/mathDef/actions/runs/39271973045) **success**.
3. Three individually reviewed new foundations marked no-supported-target: [39272301911](https://github.com/Zengez/mathDef/actions/runs/39272301911) **success**.
4. Third 24 links: [39273250596](https://github.com/Zengez/mathDef/actions/runs/39273250596) **success**.
5. Fourth 24 links: [39273971915](https://github.com/Zengez/mathDef/actions/runs/39273971915) **success**.
6. Three new direct-source observation candidates and 339-term source coverage: [39275061111](https://github.com/Zengez/mathDef/actions/runs/39275061111) **success**.

Batch-specific reviewed relationship records are under `intake/wave2_curated_relations_batch_01.jsonl` through `batch_04.jsonl`; before/after disposition decisions and immutable historical override evidence are in `state/wave2_formulation_reviews.jsonl` and `events/wave2_link_disposition_overrides_batch{01,02,03,04}.jsonl`. Current link report: `state/wave2_link_review_batch_04.json`. All original Wave 1 relationship records and source-review history remain unchanged; no cycles in the derived link graph.

## Access-control and mathematical source findings

- A fresh direct web attempt at each of **8** EoM foundation URLs yielded **HTTP 502**. Logged individually in `wave2/eom_direct_access_recheck_2026-10-19.jsonl`. Do not bypass the source or transform an alternate ProofWiki/Stacks definition into fake EoM verification.
- Directly opened [Stacks 4.36, tag 02XU](https://stacks.math.columbia.edu/tag/02XU) and [Stacks 4.37, tag 0048](https://stacks.math.columbia.edu/tag/0048). Both explicitly describe **functors from C^op** (equivalently contravariant functors *on C*) with strict pullback composition; they are **not themselves citations for general pseudofunctors with nontrivial coherence data**.
- An inherited independent category-valued-presheaf formulation says *contravariant functor C^op→Cat*, incorrectly applying contravariance twice. Separately, the inherited groupoid-valued-presheaf formulation cites strict Stacks 4.37 while stating *pseudofunctor*. Do **not** silently overwrite frozen inherited content; these need explicit Stage 4 second-wave revision and refreshed 440-plus-formulation relation-review digests. Source-specific mathematical audit: `wave2/context_ambiguity_source_review_2026-10-19.jsonl`.
- Stacks [4.29, tag 003G](https://stacks.math.columbia.edu/tag/003G) explicitly works with strict 2-categories. The broader weak 2-category equivalence context remains unresolved.
- New terms for future variant screening: `obs.wave2.proofwiki.unit-of-ring`, `obs.wave2.stacks.integral-domain`, and `obs.wave2.proofwiki.maximal-ideal-of-ring`. Their source conventions differ from the general nonunital ring meaning and must be kept explicit.

## Safe next tasks — High thinking for meaning/relationship reviews

1. **Candidate meanings and mathematical cross-source reviews:** independently formulate context-precise meanings for unit, integral domain, and maximal ideal using the direct observations and the corroborating Stacks/ProofWiki locations. Keep these as candidates until individually screened. Do not conflate the zero ring, optional unity, noncommutative maximal left/right ideals, or properness.
2. **Extend the meaning/relation review ledger for growth:** currently `wave2_apply_links.py` and the Stage 5 review-seed script enforce the old 428 meanings/440 formulations; new screened meanings must be appended **without rewriting or losing any of the 440 prior reviewed decisions or 529 links**, and the common meaning-catalog digest must be refreshed with a historical snapshot. Add regression tests for idempotence, immutable inherited Wave 1, no cycles, stage-seal barriers and old decision preservation.
3. **Variance and strictness audit:** for the 2 presheaf formulations above, propose an explicit second-wave audited revision with source-correct strict versions and (where independently verified) separate pseudofunctor context variants. Changing inherited formulation text returns review state to candidate and requires downstream re-screening; never silently patch the frozen baseline.
4. **Address remaining 27 no-target + 2 held cases:** prioritize units, integral domains, maximal ideals, functors and groupoids, fields, general set operations, and coherent pseudofunctors. No keyword-only links.
5. Continue the 3,599 generic and 192 prioritized source/context/gap research tasks individually; those numbers are queued leads, **not** 3,791 definitions. Maintain source-specific dispositions and broad coverage accounting.
6. Only after source and contextual review coverage are substantially complete, rigorously seal and freeze Wave 2; *then* independently compare to production mathDef.

Do not treat any successful CI job as independent peer verification of mathematics, or infer that 440/440 reviewed formulations means all possible definitions have been found.
