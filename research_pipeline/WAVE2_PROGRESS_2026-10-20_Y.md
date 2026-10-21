# Independent mathDef Wave 2 — verified checkpoint Y (2026-10-20)

**Fast restart:** [generated RESUME_STATE.json](experiments/reconstruction-v2-independent/state/RESUME_STATE.json) and [mathDef adapter resume_plan.json](adapters/mathdef/resume_plan.json). This supersedes checkpoint X for current totals and next work without rewriting historical screen decisions.

## Batches 125–127: pointwise/uniform/local convergence; eigenvectors

Three independent GitHub Actions workflows were verified SUCCESS:

- **Batch 125 source-only** [run 39525344705](https://github.com/Zengez/mathDef/actions/runs/39525344705): four source headings and eight separately attributable direct source observations from ProofWiki [Pointwise Convergence](https://proofwiki.org/wiki/Definition:Pointwise_Convergence), [Uniform Convergence](https://proofwiki.org/wiki/Definition:Uniform_Convergence), [Locally Uniform Convergence](https://proofwiki.org/wiki/Definition:Locally_Uniform_Convergence), and [Eigenvector/Linear Operator](https://proofwiki.org/wiki/Definition:Eigenvector/Linear_Operator). One uniform-series source observation **explicitly HELD** because ProofWiki mistakenly defines partial sums using f_n(x) under sum over k instead of f_k(x). Mathematical texts require the running summand f_k(x), not n copies of f_n(x). Bad source line retained for transparency, not promoted. Source-only batch leaves older mathematical meanings and links alone.
- **Batch 126 mathematical screening** [run 39525525324](https://github.com/Zengez/mathDef/actions/runs/39525525324): six mathematically scoped meanings and seven individually source-screened safe formulations. Real pointwise convergence has the quantifier order forall x, forall epsilon, exists cutoff potentially depending on x; topological pointwise convergence is equivalently convergence in function-space product topology T^D. Metric-target uniform convergence requires one epsilon-dependent cutoff valid for ALL input points; real-valued uniform convergence is that metric specialization. Locally uniform convergence uses uniform convergence on a neighborhood of EACH source point. Eigenvectors of a field-linear endomorphism have two equivalent formulations: nonzero v with Av=λv, or nonzero v in ker(A−λI). The zero vector is **not** an eigenvector. Historic 611 individual review decisions and 825 links preserved.
- **Batch 127 individual prerequisites** [run 39525835162](https://github.com/Zengez/mathDef/actions/runs/39525835162): fifteen individually source-checked mathematical definition prerequisite links, covering each of seven new formulations. Targets are independently screened mappings, topological space, metric space, real number field, metric uniform convergence, field vector-space linear transformation and field-linear-map kernel, as appropriate. Every historic 825 relation and 611 unrelated formulation decision remains unchanged, no directed cycles. New candidate missing prerequisite targets explicitly **logged, not fabricated**: function-space product topology T^D and field-linear-operator eigenvalue meaning.

## Current committed independent reconstruction

| Registry | Count |
| --- | ---: |
| Approved independent external source collections | **14** |
| Independent attributed source headings | **469** |
| Individual source observations | **932**, including 3 separately quarantined source claims |
| Mathematically screened contextual meanings | **583** |
| Individually reviewed mathematical formulations | **618** |
| Source-specific reviewed direct prerequisite relations | **840** |
| Formulation dispositions | **612 linked / 6 justified no-supported-target / 0 pending** |
| Dependency graph cycles | **0** |
| Sealed Wave 2 stages | **0** |

Independent Wave1 frozen digest remains **7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801**. The original production mathDef definitions, citations and variants have **never been consulted or compared**. These checks represent independently screenable source research and computational validations, not expert human mathematical peer review.

### Three held source claims, all excluded from accepted meanings

1. ProofWiki directional derivative claims gradient dot direction with assumption merely that the gradient exists, insufficient for equality with line-direction difference quotient without stronger total differentiability (checkpoint U).
2. ProofWiki graph isomorphism page initially offers only a forward-edge-preserving bijection, insufficient for isomorphism without reflecting edges (checkpoint W).
3. ProofWiki uniform-convergence page's Infinite Series section mis-indexes partial sum as s_n(x)=sum_{k=1}^n f_n(x) instead of sum f_k(x) (this checkpoint Y).

### Detailed current batch provenance

Relative to research_pipeline/experiments/reconstruction-v2-independent:

- wave2/convergence_eigen_source_batch125_2026-10-20.jsonl
- wave2/conv125_quarantined_source_claims.jsonl
- state/wave2_conv125_source_intake.json
- wave2/conv126_individual_mathematical_reviews.jsonl
- state/wave2_conv126_meaning_screen.json
- wave2/conv127_individual_source_screened_links.jsonl
- wave2/conv127_missing_prerequisite_targets.jsonl
- state/wave2_conv127_link_review.json
- Prior 611/618-row historical review snapshots and exact source-specific intake files.

Prior source quality notes and access constraints remain: ProofWiki topological-boundary bad source variant previously excluded; uncited normed division-ring pair page; inaccessible eight Encyclopedia of Mathematics links and 27 PlanetMath original pages, first-pass original 192 priority entries not exhaustive.

## Suggested next bounded work: Batch 128

Broaden independent sourced mathematical definitions outside this wave's analysis/linear operator branch; selectively source and audit outstanding product-topology and eigenvalue prerequisites if direct evidence is available, then consider retroactive links to prior pointwise/eigenvector forms without altering their historic decisions. Possible orthogonal fresh sources: combinatorial graph invariants, probability or linear algebra canonical forms. **Do not chase new prerequisite chains without a bounded reason**.

Maintain reusable generic research engine subject-neutral (for future mathematical theorem, educational mathematics terminology and other topics), place mathematics-specific decisions in mathDef adapters. All five Wave 2 stages remain UNSEALED; never access/compare original production definitions before independent reconstruction freeze. End bounded 12–14-minute work intervals with verified source/math/link commits and compact checkpoint.
