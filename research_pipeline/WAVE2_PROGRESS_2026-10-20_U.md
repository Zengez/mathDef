# Independent mathDef Wave 2 — verified checkpoint U (2026-10-20)

**Fast-resume authorities:** [RESUME_STATE.json](experiments/reconstruction-v2-independent/state/RESUME_STATE.json) and [resume_plan.json](adapters/mathdef/resume_plan.json). Supersedes checkpoint T current counts, not historical evidence or individual mathematical dispositions.

## Batches 112–114 — directional derivative source audit; metric and topological contexts

- **Batch 112 source-only:** [successful workflow 39511138013](https://github.com/Zengez/mathDef/actions/runs/39511138013). Four ProofWiki source pages: Definition:Open_Ball; Definition:Closed_Ball; Definition:Homeomorphism/Topological_Spaces; Definition:Directional_Derivative. Four source headings and eight individual observations. Two each for open balls (metric / normed vector), closed balls (metric / normed vector), homeomorphisms (continuous bijection with continuous inverse / equivalent open-set criterion), and directional derivatives (differentiable line-restriction / gradient-dot formula). Exactly one observation is explicitly **HELD** rather than mathematically promoted: gradient-dot-direction with the source's inadequate "gradient exists" assumption. The source equivalence page repeats that unsupported equivalence.
- **Batch 113 mathematical screening:** [successful workflow 39511346184](https://github.com/Zengez/mathDef/actions/runs/39511346184). Six contextual meanings and seven mathematical formulations accepted; homeomorphism's two equivalent definitions remain one topological meaning, while metric and normed-vector open/closed ball contexts remain separate. Only the line-restriction directional derivative under **total differentiability** is admitted; gradient-existence alone stays in the held source observation. All previous 587 reviewed formulation decisions and 784 direct links preserved.
- **Batch 114 dependency screening:** [successful workflow 39511602204](https://github.com/Zengez/mathDef/actions/runs/39511602204). Ten source-specific links for seven new forms: open/closed metric ball to metric space; open/closed normed-vector ball to normed vector space; first homeomorphism form to topological space and topological continuity; second form to topology and mapping; directional derivative to mapping and ordered real number system. All original 784 links and 587 unrelated reviews preserved; dependency graph acyclic.

## Important mathematical caveats discovered

ProofWiki Definition:Directional_Derivative Definition 1 gives gradient dotted with a unit direction assuming merely that gradient exists, but Definition 2 requires differentiability of the underlying real-valued function. Assuming "gradient exists" means all partial derivatives at the point exist, the stated equivalence is generally **false**. Counterexample: define f(x,y)=xy/(x²+y²) away from the origin and f(0,0)=0. Both partial derivatives at the origin vanish, yet for u=(1,1)/sqrt(2), f(tu)=1/2 for every t≠0 and the directional difference quotient fails to converge finitely. Thus the source gradient-only presentation is **quarantined as evidence**, not promoted as a mathematical meaning. Total/Fréchet differentiability is a sufficient stronger hypothesis; source-specific conditions must be stated.

A closed metric ball defined by non-strict inequality d(x,a)≤r need not equal the topological closure of the corresponding open metric ball defined by d(x,a)<r. In a discrete metric space with at least two points and radius 1, the open ball around a is {a} with closure {a}, while the closed metric ball is the entire space. No false equivalence was admitted.

Other preserved caveats: ProofWiki's Boundary (Topology) erroneous closure-and-exterior formulation excluded in Batch106; its normed-division-ring pair definition lacks its own bibliography; 8 Encyclopedia of Mathematics source locators inaccessible, 27 PlanetMath original pages blocked, original 192 first-pass priority tasks not exhaustive coverage.

## Verified committed independent totals

| Registry | Total |
| --- | ---: |
| Approved independent source collections | **14** |
| Independently attributed headings | **453** |
| Individual source observations | **906**, of which 1 quarantined |
| Screened contextual mathematical meanings | **564** |
| Individually reviewed mathematical formulations | **594** |
| Individually source-screened prerequisite relationships | **794** |
| Formulation decisions | **588 linked / 6 justified no-supported-target / 0 pending** |
| Directed dependency cycles | **0** |
| Sealed Wave 2 stages | **0** |

Frozen independent Wave 1 publication digest: 7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801. Production mathDef mathematical content and original variants never consulted/compared. Research-screened is not human peer-verified.

### Detailed evidence paths

All relative to research_pipeline/experiments/reconstruction-v2-independent:
- wave2/directional_metric_topology_source_audit_batch112_2026-10-20.jsonl
- wave2/directional112_quarantined_source_claims.jsonl
- state/wave2_directional112_source_intake.json
- wave2/directional113_individual_mathematical_reviews.jsonl
- state/wave2_directional113_meaning_screen.json
- wave2/directional114_individual_source_screened_links.jsonl
- state/wave2_directional114_link_review.json
- Associated intake files and pre-batch 587 and 594 formulation-review ledger snapshots.

## Next bounded research — Batch 115 (High reasoning)

Broaden **independent source-backed discovery outside recently worked metric/topological/multivariable branches**. Possible topics: group actions and orbit stabilizer, combinatorial partitions, measure-theoretic pushforwards, or linear operators under explicit domain hypotheses. Collision-check current meanings and exact direct source access first. Opportunistically seek external rigorous support for total differentiability as a condition behind the directional derivative gradient formula, but do not release the held source claim merely because the gradient formula resembles the familiar textbook one.

Keep the generic research engine subject-neutral for future mathematics theorem and math-education projects; all domain policy in mathDef adapters. All five independent Wave 2 stages remain UNSEALED until independent freeze; comparison with production mathDef corpus prohibited. Stop each research session after roughly 12–14 active minutes, commit, verify checkpoint, and hand off cleanly.
