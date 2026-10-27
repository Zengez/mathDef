# The 22 cross-heading mathematical comparisons — resolved research pass

**Date:** October 27, 2026  
**Branch:** `work/dedup-subject-context-sources-20261027`  
**Scope:** Exactly the 22 pairs in the previously flagged `TEMP_CROSS_HEADING_SURFACE_REVIEW_2026-10-27.md`. This was one bounded research pass, not a new term-discovery or full research-corpus audit.

## Results

- **11 pairs grouped as related variants**, with their *mathematically distinct meanings and formulations preserved*. Grouping only retires a duplicate **search heading** and retains its name as an alias; it does **not** claim the two meanings are equivalent.
- **11 pairs retained as separate terms**, because they define different mathematical objects, impose an additional substantive property, or encode a substantively distinct notion.
- **0 pairs still need manual mathematical comparison** for the *deduplication/grouping decision*. The existing 44 earlier **within-heading** manual-review cases are outside this pass and still open.
- **0 meaning merges** and **0 formulation deletions** were made in this 22-case pass. The only content changes were the 11 reviewed *group-only heading migrations* and their existing retained-variant ledger updates.
- Validated by [stage-only GitHub Actions run 40567640298](https://github.com/Zengez/mathDef/actions/runs/40567640298): 1,986 headings, 2,068 meanings, 2,110 formulations, 2,662 preserved source identities, 1,014 original historic IDs reachable, no final linking or publication.

### Complete 22-pair decision table

| # | Existing headings compared | Disposition | Basis for decision |
|---:|---|---|---|
| 1 | minimal prime ideal / prime minimal over an ideal | Grouped, meanings retained | A minimal prime of R is precisely a prime minimal over I=(0). Relative minimality above a general ideal I is a parameterized extension; keep both predicates and searchable labels. |
| 2 | Algebraic closure of a field / Relative algebraic closure | Separate terms | The field of elements algebraic over k inside a specified K need not be algebraically closed; an algebraic closure must itself be algebraically closed. They are different constructions and data. |
| 3 | Analytic Hardy space on the disk / Hardy Hilbert space on the disk | Grouped, meanings retained | H^2(D) is the p=2 Hilbert-space specialization of analytic H^p(D), with useful coefficient inner product; preserve p-dependent and Hilbert-specific formulations separately. |
| 4 | Bergman space / Weighted Bergman space | Grouped, meanings retained | Weighted Bergman spaces add an explicit positive weight ω in the integrability condition; ω=1 recovers the ordinary unweighted Bergman space. Keep both settings and sources. |
| 5 | Bloch space on the disk / Little Bloch space | Separate terms | Little Bloch functions require a vanishing boundary-limit seminorm, a strictly stronger property than finite Bloch seminorm. The little space is a distinct closed subspace, not an alternative defining wording. |
| 6 | Cohen–Macaulay local ring / Cohen–Macaulay ring | Grouped, meanings retained | For a Noetherian ring the global Cohen–Macaulay condition tests all localizations at primes; the local formulation tests depth=dimension of one Noetherian local ring. Retain global/local scope as separate variants. |
| 7 | Cohen–Macaulay local module / global Cohen–Macaulay module | Grouped, meanings retained | Local module equality between depth and dimension of support contrasts with testing every prime localization of a finite global module; related as local and global formulations, not identical in declared input. |
| 8 | I-adic completion of a Noetherian ring / I-adic completion of a ring | Grouped, meanings retained | Both define lim_n R/I^n; Noetherianity is an additional scope restriction, not needed for the inverse-limit construction. Preserve specialized and general contexts without discarding any source. |
| 9 | Tor-based local criterion for module flatness / Tor-vanishing criterion for module flatness | Grouped, meanings retained | The general criterion uses Tor_1(M,R/I) for all finitely generated ideals I. The local criterion needs a local map of Noetherian local rings and finite S-module M, but needs only Tor_1^R(k,M)=0. Both test R-flatness under DIFFERENT hypotheses; preserve both theorems. |
| 10 | G-unramified at a target prime / unramified at a target prime | Grouped, meanings retained | In Stacks' definitions G-unramified requires finite presentation and Ω=0 after suitable localization; unramified requires finite type and Ω=0. The finiteness hypotheses must remain visible and are not generally equivalent. |
| 11 | Zariski topology on a scheme / Zariski topology on a spectrum | Grouped, meanings retained | On affine Spec R the Zariski topology has closed V(I) and basic open D(f); schemes carry a topology assembled from those affine charts. Keep the affine and global scheme cases as distinct input contexts. |
| 12 | box topology on a product of topological spaces / product topology of a family of topological spaces | Separate terms | Box basic opens allow arbitrary coordinate restrictions whereas product basic opens restrict only finitely many coordinates. On infinite products they can be genuinely different topologies. |
| 13 | Reproducing kernel of a Hilbert function space / Reproducing-kernel Hilbert space | Separate terms | The reproducing kernel is a function K:X×X→C, while an RKHS is a Hilbert space of functions with continuous evaluations. Despite correspondence they have DIFFERENT object types. |
| 14 | Categorical epimorphism / categorical epimorphism of rings | Grouped, meanings retained | Right-cancellability defines epimorphism in an arbitrary category; the commutative-ring specialization has the tensor multiplication criterion and need not be surjective on underlying sets. Retain categorical and ring-specific formulations. |
| 15 | Conditional independence of events / Independence of events | Separate terms | Conditional independence given C with P(C)>0 is computed under the conditional probability P(·\|C) and is not equivalent to unconditional independence under P. |
| 16 | formally unramified ring homomorphism / unramified ring homomorphism | Grouped, meanings retained | Formal unramifiedness is uniqueness of square-zero lifts (equivalently Ω=0); Stacks unramified additionally requires finite type. Finite type is a real extra requirement, so do not conflate meanings. |
| 17 | Lebesgue measure / Lebesgue–Stieltjes measure | Separate terms | The Lebesgue–Stieltjes measure on the real line is parametrized by monotone right-continuous F, with F(x)=x yielding 1D Lebesgue measure (after appropriate completion). General Stieltjes measures also include atomic/singular cases and are not synonymous with Lebesgue measure on R^n. |
| 18 | pure short exact sequence / Short exact sequence | Separate terms | Pure exactness is the additional property of surviving every tensor base change, not merely injective-exact-surjective. Ordinary short exact sequences need not be pure. |
| 19 | free abelian group / Free module | Separate terms | Free abelian groups are precisely free Z-modules, but the first is an abelian-group type and the second is an R-module construction with specified scalar ring. Preserve the distinct named algebraic structures rather than alias them. |
| 20 | Hausdorff second-countable topological space / Second-countable space | Separate terms | Hausdorff second-countability imposes a separate T2 axiom in addition to a countable basis. Second-countable spaces alone need not be Hausdorff. |
| 21 | Boolean isomorphism of measured actions / Spatial isomorphism of measured actions | Separate terms | A Boolean isomorphism permits a distinct conull agreement set X_g for each g; spatial isomorphism requires ONE invariant conull set with all g-equivariance. Distinct generally: Hoareau–Le Maître give Boolean-isomorphic but not spatially isomorphic examples for non-locally-compact Polish groups; some countable/local compact settings collapse the difference. |
| 22 | C-constrained map of chromatic metric pairs / Sigma-constrained map of chromatic metric pairs | Separate terms | The C-constrained condition quantifies over every sigma∈C, while sigma-constrained concerns one chosen sigma; arbitrary families impose an intersection of constraints. Different parameter data; no equality for unrestricted C. |

### Source provenance for this review

The external sources below support the specific comparisons where recorded; they do **not** automatically certify all historical formulations or change the existing source-verification labels in mathDef:

1. https://www.cambridge.org/core/books/abs/an-introduction-to-hankel-operators/hardy-spaces/46E184B3C5B607B8C870749EA056B2B3
2. https://stacks.math.columbia.edu/tag/02IN
3. https://stacks.math.columbia.edu/tag/00M9
4. https://stacks.math.columbia.edu/tag/00MK
5. https://public.websites.umich.edu/~mmustata/ReviewSheet6_2018.pdf
6. https://stacks.math.columbia.edu/tag/00UT
7. https://www.cambridge.org/core/books/abs/mathematical-pictures-at-a-data-science-exhibition/reproducing-kernel-hilbert-spaces/1751438EC21F68851E6B0E4A21D7380E
8. https://stacks.math.columbia.edu/tag/00UU
9. https://stacks.math.columbia.edu/tag/00US
10. https://www.math.ucdavis.edu/~hunter/measure_theory/measure_notes_ch2.pdf
11. https://teorth.github.io/pfr/docs/Mathlib/MeasureTheory/Measure/Lebesgue/Basic.html
12. https://arxiv.org/abs/2406.02401

**Important:** Some previously flagged cases (notably G-unramified / unramified, formal unramified / unramified, the two Tor flatness criteria, and the Hardy H² specialization) contain **materially different hypotheses**. They were grouped solely as *search variants*, never merged into one mathematical meaning. Boolean versus spatial isomorphisms remain **separate**, supported by explicit nonequivalence results for some Polish groups (and agreement under additional hypotheses such as countable discrete groups).

**Future work boundary:** The earlier 44 within-heading manual comparisons have not been researched or adjudicated by this pass. No global relinking, production publish, or unrelated mathematics investigation has been authorized.
