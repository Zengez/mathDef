# Independent mathDef Wave 2 — verified checkpoint AA (2026-10-20)

**Fast restart:** [portable RESUME_STATE.json](experiments/reconstruction-v2-independent/state/RESUME_STATE.json) and [mathDef adapter resume_plan.json](adapters/mathdef/resume_plan.json). Supersedes checkpoint Z only for current counts and next action; earlier source, mathematical, formulation and prerequisite decisions remain historically preserved.

## Batches 132–134: Bell numbers, Stirling numbers, convex hulls, and vertex degree

All three independently gated GitHub Actions workflows passed portable engine/adapter regressions, independent frozen Wave1 digest check, complete individual formulation review-preservation, direct prerequisite checking and definition-dependency cycle checks:

- **Batch132 source-only intake** [GitHub Actions success 39527991209](https://github.com/Zengez/mathDef/actions/runs/39527991209): Four directly inspected mathematical [ProofWiki](https://proofwiki.org/) definition pages: [Bell Number](https://proofwiki.org/wiki/Definition:Bell_Number), [Stirling Numbers of the Second Kind](https://proofwiki.org/wiki/Definition:Stirling_Numbers_of_the_Second_Kind), [Convex Hull](https://proofwiki.org/wiki/Definition:Convex_Hull), and [Degree of Vertex](https://proofwiki.org/wiki/Definition:Degree_of_Vertex). Added **four independent source headings and eight individually cited source observations**. Separate sourced equivalent representations: one Bell count, two Stirling criteria, three convex hull constructions, two simple-graph vertex-degree descriptions. No mathematical meanings or links changed during source intake.
- **Batch133 mathematical screening** [GitHub Actions success 39528163558](https://github.com/Zengez/mathDef/actions/runs/39528163558): **Four independently source-scoped mathematical meanings, eight individual formulations**, with equivalently correct formulations under the same meaning:
  - Bell number B_n counts unindexed partitions of an n-element set into nonempty blocks; importantly **B_0=1** because the empty set has exactly one partition (the empty collection).
  - Stirling numbers of the second kind S(n,k): Kronecker-delta boundary plus the recurrence S(n,k)=S(n−1,k−1)+kS(n−1,k) for positive n,k, equivalent to the coefficient identity x^n=Σ_{k=0}^n S(n,k)x^{underline k}. The combinatorial theorem identifying S(n,k) with number of partitions into exactly k blocks was independently reviewed as corroboration but not silently invented as a third source observation.
  - Convex hull of U⊆V in a real vector space: all finite positive-weight convex combinations; intersection of all convex supersets; unique least convex superset. **All three equivalent**, including conv(∅)=∅. Not automatically equal to a **closed** convex hull or affine hull.
  - Vertex degree in a **simple loopless undirected graph**: cardinality of incident edges equals cardinality of adjacent vertices in that context. **Not a general multigraph equivalence** (parallel edges and loops defeat it).
  - All **624** earlier formulation review decisions and **855** links preserved except expected meaning-catalog digest update.
- **Batch134 individual dependency screening** [GitHub Actions success 39528416620](https://github.com/Zengez/mathDef/actions/runs/39528416620): **Fourteen individually source/target screened prerequisite links**, covering all eight new forms: Bell→partition and nonnegative natural-number meaning; both Stirling descriptions→natural numbers including zero; each of three convex-hull descriptions→vector space and subset (six links); both simple-graph vertex-degree descriptions→simple undirected graph and cardinality (four links). All historical **855** reviewed links and **624** unrelated form review decisions intact, with zero dependency cycles and no pending individual review.

### Verified independent Wave 2 counts

| Registry | Total |
| --- | ---: |
| Approved external source collections | **14** |
| Attributed independent source headings | **477** |
| Individual source observations | **946**, including 3 historic held questionable source claims |
| Mathematically screened contextual meanings | **591** |
| Individually reviewed source-specific mathematical formulations | **632** |
| Independently screened direct prerequisite relationships | **869** |
| Formulation review decisions | **626 linked / 6 individually justified no-supported-target / 0 pending** |
| Directed dependency cycles | **0** |
| Sealed independent Wave 2 stages | **0** |

The independent frozen Wave1 publication digest remains **7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801**. No production mathDef definitions, original citations, variants or mathematical entries have been consulted or compared. This represents mathematical source-screening and automated test validation, **not independent expert peer review**.

### Mathematical source cautions and coverage gaps

1. **ProofWiki Degree of Vertex** gives edge-incidence count and neighbor count as an equation in general undirected-graph context but also discusses loop multigraphs, where these are not equal. Both source forms were admitted **ONLY in simple loopless graph context**. The broad multigraph source generalization remains documented as problematic; neither arbitrary multigraph definition nor a false equivalence was admitted.
2. **Stirling polynomial identity** uses falling-factorial polynomials, which still need a standalone independently screened prerequisite target; its recursion uses the **Kronecker delta**, also not yet independently screened. Those are source research gaps, not fabricated mathematical links.
3. **Convex hull's intersection and least-superset formulations** presuppose the mathematical notion **convex subset**. Existing independently screened general subset and vector-space meanings support some prerequisites but not this exact convexity predicate, logged as a separate missing target.
4. Historic THREE quarantined questionable observations remain **source-only, not mathematical meanings**: insufficient gradient-only directional derivative; forward-only graph-isomorphism condition; uniform-series partial-sum f_n rather than f_k typo. The older apparent ProofWiki topological-boundary source error was also excluded during its own earlier research.
5. Other preexisting access and validation caveats persist: eight inaccessible Encyclopedia of Mathematics source locators, 27 restricted original PlanetMath pages, uncited normed-division-ring pair source, and nonexhaustive first-pass coverage for original 192 research priorities.

### Files generated

Relative to research_pipeline/experiments/reconstruction-v2-independent:
- wave2/combinatorics_convex_graph_source_batch132_2026-10-20.jsonl
- wave2/foundation_source_discovery_batch_132.jsonl
- state/wave2_cross132_source_intake.json
- wave2/cross133_individual_mathematical_reviews.jsonl
- state/wave2_cross133_meaning_screen.json
- wave2/cross134_individual_source_screened_links.jsonl
- wave2/cross134_missing_prerequisite_targets.jsonl
- state/wave2_cross134_link_review.json
- Associated separate intake files and 624-/632-row historical individual review ledger snapshots.

### Next bounded mathematical work: Batch135

Prefer independent breadth, not unbounded recursion: source-rich mathematical definitions in **discrete probability, affine geometry, or graph theory beyond vertex degree**, while opportunistically recovering one or more clearly documented missing targets (convex set, falling factorial, Kronecker delta) if directly sourced and mathematically justified. Collision-check existing independent meanings first. Do not confuse source evidence with approved mathematical variants; all source-specific formulations and dependency links require separate review.

Keep the reusable research engine topic-neutral for future theorem and educational-definition projects. Mathematics-specific conventions stay in research_pipeline/adapters/mathdef. Keep all five Wave2 stages UNSEALED, frozen independent Wave1 unmodified and production-original content uninspected. Follow bounded ~12–14-minute work sessions with a verified commit and compact portable checkpoint.
