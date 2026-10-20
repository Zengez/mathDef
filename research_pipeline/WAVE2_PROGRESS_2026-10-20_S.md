# Independent mathDef Wave 2 — verified checkpoint S (2026-10-20)

**Restart authorities:** [RESUME_STATE.json](experiments/reconstruction-v2-independent/state/RESUME_STATE.json) and [resume_plan.json](adapters/mathdef/resume_plan.json). This supersedes checkpoint R counts and next actions, while preserving earlier historical evidence and individual review ledgers.

## Batches 106–108 — topology, linear algebra and calculus

All three independently researched sequential workflows successfully completed and committed their screened results to GitHub:

- **Batch 106, source only:** [GitHub workflow 39507831430 — successful](https://github.com/Zengez/mathDef/actions/runs/39507831430). Four new individually sourced headings from exact external ProofWiki pages: topological closure, topological boundary, kernel of a linear transformation, and derivative of a real function on an open interval. **Seven** individual paraphrased source observations; no mathematical meanings/links promoted until their respective later screens. Checked existing interior and point-derivative meanings for collisions. Independently detected an apparent mathematical error on the ProofWiki boundary page: a proposed formula restricting the boundary to points in A excludes boundary points outside A. **Rejected that third formulation** explicitly, instead of copying it to the data. The closure source also provides a closure-via-boundary formula; excluded from this batch to avoid spurious circular closure ↔ boundary prerequisites.
- **Batch 107, mathematical screening:** [GitHub workflow 39508076150 — successful](https://github.com/Zengez/mathDef/actions/runs/39508076150). Five mathematical contexts with seven independently source-backed formulations. The intersection of all closed supersets and the least closed containing set are equivalent presentations of *one* topological closure meaning. Closure-minus-interior and intersection of closure with closure of the complement are equivalent presentations of *one* topological boundary meaning, relative to specified ambient X. Kernels of R-linear maps between modules and K-linear maps between field-vector spaces are related but different scope-specific meanings. The derivative function f′:I→ℝ on a fully differentiable open interval is distinct from the previously screened number f′(a) at an interior point. Snapshotted/preserved all 573 historical review decisions and 765 graph links.
- **Batch 108, prerequisite screening:** [GitHub workflow 39508374483 — successful](https://github.com/Zengez/mathDef/actions/runs/39508374483). Nine exact source→mathematical-meaning links: two closure formulations → topological space; first boundary formulation → closure and previously screened interior; second boundary formulation → closure; module kernel → independently screened left R-module; field-vector kernel → vector-space structure and general module kernel; derivative function → previously screened pointwise real derivative. No source-defined closure variant links to boundary, so the graph remains acyclic. Earlier 765 relations and all 573 unrelated reviewed formulations retained without rewriting history. Seven new formulations all received individual dependency dispositions.

### Latest verified committed independent research counts

| Registry | Count |
| --- | ---: |
| Approved independent sources | **14** |
| Attributed independent term/heading records | **445** |
| Individual external source observations | **891** |
| Mathematically screened contextual meanings | **552** |
| Individually dispositioned formulations | **580** |
| Individually source-screened prerequisite links | **774** |
| Formulation dispositions | **574 linked; 6 independently justified no-supported-target; 0 pending** |
| Directed dependency cycles | **0** |
| Sealed Wave 2 stages | **0** |

The frozen independent Wave 1 digest remains **7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801**. Production mathDef definitions, variants and existing citation files were **not** consulted or compared with reconstructed data. These are independently source-reviewed and programmatically tested records, not human-refereed mathematical results.

New detailed evidence records in research_pipeline/experiments/reconstruction-v2-independent:
- wave2/cross_branch_source_variants_batch106_2026-10-20.jsonl
- wave2/foundation_source_discovery_batch_106.jsonl
- state/wave2_cross106_source_intake.json
- wave2/cross107_individual_mathematical_reviews.jsonl
- state/wave2_cross107_meaning_screen.json
- wave2/cross108_individually_screened_links.jsonl
- state/wave2_cross108_link_review.json
- Historical formulation-review snapshots before Batches107 and 108, and original intake records under intake/.

### Caveats requiring future attention

1. The third "closure and exterior" definition of topological boundary in the reviewed source is not mathematically sound as written; it remains explicitly excluded. A later independent citation audit should flag the offending source section, not silently normalize it.
2. Topological closure and boundary depend on the chosen ambient topological space, and closure of the empty subset remains empty with no nonempty-space hypothesis.
3. Field-vector kernels are a specialization of module kernels but neither should be equated with an arbitrary mapping fiber, or with the previously separately screened category-theoretic universal-property kernel.
4. A derivative at a single interior point does not assert that the whole function is differentiable on an interval.
5. Previous bibliographic caveat remains: standalone ProofWiki normed-division-ring pair page lacks its own bibliography, although mathematical components were separately source-checked.
6. Eight Encyclopedia of Mathematics source locators inaccessible, 27 original PlanetMath source pages blocked, and original 192 priority terms have only first-pass evidence, not exhaustive definition coverage.

## Next suggested bounded independently sourced wave (High thinking)

**Batch 109:** continue source-rich independent cross-domain breadth (e.g. set-theoretic or topological closure context contrasts, elementary linear transformations/image and rank with source-specific scope, multivariable calculus derivatives with precise open-set assumptions). Do a collision audit first. Another valid priority is a read-only targeted inconsistency audit for newly sourced topology definitions (especially erroneous closure/exterior alternative), followed by a separate bounded correction batch if required. Avoid repeating completed Batches 94–108.

The reusable research **engine** must remain domain-neutral; mathematical subject decisions belong to research_pipeline/adapters/mathdef. Work in approximately **12–14-minute bounded sessions**, update the compact checkpoint and commit before timeouts. All five independent Wave 2 stages remain **UNSEALED** and the original production corpus remains outside this experiment until an independent freeze.
