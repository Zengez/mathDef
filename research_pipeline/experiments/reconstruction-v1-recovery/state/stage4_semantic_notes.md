# Corrected Wave 1 Stage 4 — context grouping notes

Date: 2026-10-18. Workspace: `research_pipeline/experiments/reconstruction-v1-recovery`.

**Source isolation:** The original production mathDef definition corpus, its variants, and its citations remain unseen. Source materials are the independent Stacks Project source sections, used for mathematical editorial screening and independently written paraphrases. The historical premature `reconstruction-v1` checkpoints were not reused to generate the corrected meaning registry.

## Completion counts and scope

- Stage 2 independently sealed term/source headings: **318**.
- Fetched Stacks source sections examined: **291**. PlanetMath source access-policy blocks: **27**.
- Fetched headings with authored mathematical content: **232**; headings without a suitable standalone definition: **59**.
- Independently authored mathematical formulations: **431**, referenced through Stage 3's sealed `obs.*` evidence IDs.
- Corrected Stage 4 context-labelled meaning candidates: **419**, representing all 431 formulations and all 232 supported headings. **86** unsupported or access-blocked headings explicitly remain held.
- **12** source-explicit within-heading equivalent-definition pairs were grouped under one meaning. Other different-object/context formulations under a shared source heading were kept separate.
- Stage 3 observation seal SHA-256: `3734e6183fa76ebf7bb186b45c0d82a4f1d87a53397aa73de4fd358bf1cd0c8d`.
- Stage 4 meaning seal SHA-256: `25c62402079c814c6bfe8d3fc391039df9a6c6fa6d8806d3fe6c1ed18b260ea6`.

**Interpretation:** 419 is the number of **context-labelled meaning records**, not an independently verified count of 419 globally distinct mathematical concepts. One concept may be expressed in several Stacks chapters, and some still-ungrouped within-chapter formulations may prove equivalent under closer editorial review. In particular, this first-wave grouping retains one candidate meaning per independently reviewed context and merges only the twelve manually enumerated obvious same-concept equivalences. It does not infer synonyms from lexical resemblance alone.

## Technical controls

- The builder `research_pipeline/engine/stage4_recovery_build.py` accepts **only** source-checked independently authored Stage 3 paraphrases, verifies the stage seals and complete term dispositions, and generates stable meaning and formulation IDs retaining every source observation ID.
- Mathematical context, exact section references and term-group identity are retained; `human_verified:false` remains explicit. Screening is an editorial source check, **not** independent formal refereeing.
- `stage4_recovery_finalize.py` rejects missing supported terms, unclassified authored observations, duplicate formulation IDs and locator-only formulations.
- GitHub Actions workflow `.github/workflows/mathdef-stage4-rebuild.yml` passed its regression suite, batch ingestion, comprehensive candidate coverage audit, and Stage 4 seal (run `39178163315`).
- The 318-term review outcomes are recorded in `state/stage3_term_reviews.jsonl`. They must not be overwritten to pretend an inaccessible source has been examined.

## Subsequent work

Stage 5 should use exact meaning and formulation identifiers and locate mathematically justified dependencies between **supported** concepts; it must not invent full definitions for blocked/no-suitable entries. A later Wave 2 pass should investigate (1) equivalent meanings across different source headings, (2) additional equivalences within headings, (3) potentially inconsistent hypotheses or definitions, (4) expansion of source collections and sources where the source article is a theorem section, (5) ambiguous context matches and synonyms. Freeze both independent reconstruction waves before comparison with the original mathDef production corpus.
