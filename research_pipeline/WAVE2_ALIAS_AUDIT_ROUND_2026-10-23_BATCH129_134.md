# Independent Wave2 — contextual alias and false-friend audit, 2026-10-23, packets 129–134

**Status: VERIFIED AND APPLIED.** All six packets 129–134 have exact receipts `applied_in_independent_graph_only`, `human_certified=false`. Graph [Actions 40021399375](https://github.com/Zengez/mathDef/actions/runs/40021399375) and isolated [Actions 40021399377](https://github.com/Zengez/mathDef/actions/runs/40021399377) both SUCCESS. This source-free audit is NOT external citation verification, peer-refereeing, promotion or consolidation-gate approval.

## Work performed

Baseline verified from live graph: 611 meanings, 659/659 formulations scanned, zero ambiguous/unassigned; 724 raw candidate identities, 126 reviewed aliases and 598 unresolved canonical identities. Read the original independently inventoried mathematical formulation text and candidate context for **30** new shared-prerequisite identity decisions; specifically confirmed that the two original parent definitions were *not* being identified as equivalent when their stronger hypotheses differ. Submitted 6 packets of at most five aliases in one atomic change. Application and CI **succeeded**. Live graph records **156** cumulative aliases and **568** unresolved canonical identities, with 724 raw candidate records, 826 provisional missing occurrences, 659/659 complete formulations, 0 unassigned/ambiguous, and source inventory unchanged. Subsequent targeted amendment packet 135 changed reference targets, not alias counts.

### Mathematical focus

- Category theory: fibre categories, Hom-collections with local-smallness caveats, parallel arrows, diagrams with explicit index size, Yoneda-instance natural transformations, relative diagonals (not set diagonal).
- Commutative algebra: m-primary ideals under Noetherian local hypotheses, general quotient-ring operation specialized to polynomial presentations, formal R-algebra lifts with separate uniqueness/existence clauses, minimal prime ideals, Zariski closed sets and principal opens.
- Modules and homological algebra: arbitrary module sums/products and free modules, special countability restrictions, isomorphism classes under restricted parent objects.
- Probability/measure, topology, graphs and arithmetic: measurable mappings, event-index families, extended nonnegative real codomain, open neighborhood, simple-graph and multigraph unordered edge, rational ordering, arbitrary intersections, standard-open covers.

### Explicit reviewed non-merges

1. **Radical ideal** (property I=√I) vs **radical of I** (operation I↦√I).
2. **Diagonal subset** of X×X vs **relative diagonal morphism** X→X×_S X; the latter is a typed scheme morphism.
3. **Discrete-weight** moments/orthogonality vs **interval-integral** moments/orthogonality, absent a separately reviewed common measure construction.
4. **R-linear** versus **S-linear** maps under restriction of scalars (the converse implication fails in general).
5. A **closed map** versus a **closed subset**, and an **open neighborhood** versus an arbitrary neighborhood that may not be open.
6. A **span** versus a **cospan**, and **opposite-direction functors** versus functors with a common codomain.
7. **Finite-variable polynomial quotient** versus a **general ring quotient** remain different full parent constructions even though their quotient-operation prerequisite may be aliased.
8. **Pairwise** versus **mutual** independence, **finite locally free** versus **locally free**, **smooth** versus **unramified**, and **separated** versus **quasi-separated** remain mathematically distinct parent conditions despite shared prerequisites.

## Commit verification protocol

- Confirm inbox receipts `dependency_graph/applied/semantic-global-audit-missing-alias-129.json` through `134.json` all have status `applied_in_independent_graph_only` and human_certified false.
- Require independent graph GitHub Action and isolated pipeline tests both SUCCESS, then inspect updated live STATE and CHECKPOINT and source inventory sha.
- Acyclicity and zero unassigned are structural safeguards, not mathematical certification.
- Do NOT start missing-definition research, Batch143 breadth, original mathDef comparison, Wave1 changes, freeze, or stage promotion. Consolidation gate must remain FALSE.

## Observations about efficiency

30 contextual candidate merges can be safely reviewed using a single retrieved candidate registry plus original inventoried source-text cache; packet construction is a deterministic mechanical operation afterward. Re-reviewing individual effective formulation snapshots is unnecessary for identity-only alias decisions. Notation and object-type conflict checks remain essential, and false friends should be recorded to avoid wasted repeat reviews. Verification through a single multi-packet submission amortizes GitHub write and CI overhead without weakening source-context review.

## Final verified graph and handoff

The subsequent [affine-fibre audit](WAVE2_AFFINE_FIBRE_AUDIT_2026-10-23.md) detected and corrected two whole-fibre/local-ring type errors, so the live amendment count is **765** (prior 763). Graph/test Actions for these corrections also SUCCESS: [40021923064](https://github.com/Zengez/mathDef/actions/runs/40021923064) and [40021923072](https://github.com/Zengez/mathDef/actions/runs/40021923072). The one source-level quasi-finiteness equivalence error remains explicitly flagged but not source-modified. The consolidation gate remains FALSE and unresolved fingerprint is `4ccfbccefa0faa5e440cce938b434909a9b5c2af0a0cd73dd99b60de556b8779`.
