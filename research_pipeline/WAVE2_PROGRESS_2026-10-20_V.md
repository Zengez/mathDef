# Independent mathDef Wave 2 — checkpoint V (2026-10-20)

**Fast resume:** [adapter resume plan](adapters/mathdef/resume_plan.json), [generated research status](experiments/reconstruction-v2-independent/state/RESUME_STATE.json). This checkpoint supersedes U for current totals/next actions, not prior archival research and citations.

## Completed Batches 115–117: cross-field orbit, stabilizer, measure and partitions

All three workflows succeeded on GitHub Actions, with regression tests, independent Wave1 digest checks, exact source/target locators, prior-review preservation and cycle detection:

- **Batch 115 source intake** [run 39512532131](https://github.com/Zengez/mathDef/actions/runs/39512532131): **4 source headings + 6 individually attributed observations** from directly read, approved ProofWiki definitions: [Orbit (Group Theory)](https://proofwiki.org/wiki/Definition:Orbit_(Group_Theory)), [Stabilizer](https://proofwiki.org/wiki/Definition:Stabilizer), [Pushforward Measure](https://proofwiki.org/wiki/Definition:Pushforward_Measure), [Set Partition](https://proofwiki.org/wiki/Definition:Set_Partition). These are independent of original production mathDef. Source distinctions documented: orbit as reached-set vs equivalence class; stabilizer as elements of the acting group fixing a point; pushforward uses inverse images under an appropriately measurable mapping; set partition permits empty base set with empty family, distinguishes indexed partitioning.
- **Batch 116 mathematical screening** [run 39512766067](https://github.com/Zengez/mathDef/actions/runs/39512766067): **4 contextual meanings with 6 source-specific formulations**. Each of orbit and set partition has **two mathematically equivalent formulations under one meaning**, not duplicate meanings. Stabilizer has one left-action-dependent meaning; nonnegative pushforward measure has one source-scoped measurable-space meaning. All **594 historical formulation decisions** and **794 historical links** remain intact (except catalog digest updates required for the new meanings); all 6 new formulations separately marked pending individual link review.
- **Batch 117 individual prerequisite screening** [run 39513052095](https://github.com/Zengez/mathDef/actions/runs/39513052095): **9 mathematically source-grounded direct links** across all 6 new formulations. Orbit reached-set -> left group action; orbit equivalence-class -> left group action and independently screened equivalence relation; stabilizer -> left group action; pushforward -> nonnegative measure, measurable space and typed mapping; both partition variants -> set-theoretic subset. Historical **794 links and 594 unrelated individual review dispositions preserved**, no cycles. All six newly screened formulations received completed individual review dispositions.

### Latest independently committed inventory

| Registry | Count |
| --- | ---: |
| Approved external source collections | **14** |
| Attributed independent source-term headings | **457** |
| Individual source observations | **912** |
| Screened mathematical contextual meanings | **568** |
| Individually dispositioned source formulations | **600** |
| Source-screened mathematical prerequisites | **803** |
| Formulation review decisions | **594 linked; 6 justified no-supported-target; 0 pending** |
| Detected dependency cycles | **0** |
| Sealed independent Wave 2 stages | **0** |

Frozen independently reconstructed Wave 1 publication digest remains `7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801`. No production mathDef definitions, variants, citations or original mathematical entries consulted or compared. Records are source-reviewed and regression-tested but not externally human peer-verified.

## Precision and provenance notes

- **Orbit** depends on a specified **left** G-action, without implying finiteness or transitivity; reached-set and action-relation equivalence-class forms give the same object.
- **Stabilizer** is a subset (indeed a subgroup as a separate theorem) of the acting **group G**, not the acted-on set. It depends on the action and selected point.
- **Pushforward** is on the *target* measurable space and obeys `(f_*μ)(B)=μ(f⁻¹(B))`; mere mapping is not enough: measurability is required. No probability normalization imposed.
- **Set partition** has pairwise disjoint, nonempty blocks covering S, equivalently each s∈S lies in exactly one block. For S=∅ the empty collection qualifies. Indexed families with additional index data are not silently identified with unindexed partitions.
- Previous explicitly **held source claim** from ProofWiki Definition:Directional_Derivative (gradient dot direction under merely gradient exists) remains **quarantined**, not promoted to approved mathematical meanings or relations. The earlier counterexample and stronger differentiability hypothesis remain in checkpoint U.
- Prior apparent ProofWiki topological-boundary/exterior source error remains explicitly excluded; closed metric ball is not presumed to equal closure of corresponding open ball; earlier uncited normed-division-ring bibliography caveat persists.
- Eight inaccessible Encyclopedia of Mathematics pages and 27 restricted PlanetMath original pages remain unresolved; first-pass evidence for 192 original source-priority terms is **not exhaustive** independent corpus coverage.

## Detailed Batch115–117 evidence

All relative to `research_pipeline/experiments/reconstruction-v2-independent/`:
- `wave2/group_action_measure_partition_source_batch115_2026-10-20.jsonl`
- `wave2/foundation_source_discovery_batch_115.jsonl`
- `state/wave2_group115_source_intake.json`
- `wave2/group116_individual_mathematical_reviews.jsonl`
- `state/wave2_group116_meaning_screen.json`
- `wave2/group117_individually_source_screened_links.jsonl`
- `state/wave2_group117_link_review.json`
- Historical 594 and 600 pre-screen individual review snapshots and source-specific intake files.

## Next bounded research: Batch 118 (High mathematical reasoning)

Choose 3–5 **new, accessible, independent source-rich mathematical contexts** outside the just-reviewed orbit/stabilizer/pushforward/partition branch. Candidate: quotient groups versus quotient sets under equivalence, measurable pushforward *probability* specializations or conditional distributions under explicit assumptions, combinatorial generating functions or graph isomorphism, and geometric affine transformations. First collision-check existing independent meanings and exact source locators. Preserve multiple correct variants under their appropriate contexts, mathematical equivalences within one meaning, and held unsafe source claims as unpromoted evidence.

Keep the **generic engine topic-neutral** and math-specific conventions in `research_pipeline/adapters/mathdef`. Never compare original production corpus until the independent reconstruction Wave 2 is sealed/frozen. All five Wave 2 stages remain UNSEALED. Work in ~12–14-minute bounded sessions, commit a coherent batch and checkpoint before timeout.
