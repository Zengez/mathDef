# Wave2 Pass2 source-free dependency consolidation — Chunk14 (2026-10-22)

## Verified independent Wave2 checkpoint

Continued from verified Chunk13 under `research_pipeline/DEPENDENCY_FIRST_WORKFLOW.md`. **All 611 original contextual meanings and 659 original source formulations remain unchanged.** All 659 source scans complete, all 659 structurally Open; none Closed. Phase `consolidate_occurrences`, consolidation gate false, breadth expansion on hold. No external mathematical source research, new meanings, production mathDef/frozen Wave1 comparison, freeze, promotion or human mathematical certification.

| Graph metric | Chunk13 start | Chunk14 verified finish |
|---|---:|---:|
| Unassigned occurrences | 512 | **462** |
| Ambiguous occurrences | 0 | **0** |
| Missing occurrences | 482 | **526** |
| Raw missing candidate records | 431 | **475** |
| Reviewed aliases | 78 | **78** |
| Canonical candidate previews | 353 | **397** |
| Append-only full-node amendments | 345 | **370** |
| Completed source formulation scans | 659 | **659** |

**50 formerly unassigned references classified across 25 full source formulations** in five five-formulation batches. Classification breakdown: **43** provisionally missing typed dependencies, **6** justified source-local defining predicates, **1** direct link to existing meaning. Additionally, **one prior incorrect existing small-category link** in a split-fibred-category formulation corrected to a general-category typed missing prerequisite, adding **44 raw provisional missing records** overall. No automatic alias merges.

- Source inventory SHA: `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`
- Live unresolved fingerprint: `dc1f2623fe3710b01b1a4f9af5ff703df7eea916b245552e003df9e8b6264415`
- `CHECKPOINT.state_sha256`: `5508ead726abfa5589540e07f621fe64cd03a642f1370bdd31b4855ee93a6dcd`

## Five applied review packets — both CI checks green

| Complete `mode:amend` packet suffix | Formulations | Formerly unassigned | New missing incl. correction | Source-local | Existing | Scope correction | Independent graph CI | Isolated tests |
|---|---:|---:|---:|---:|---:|---:|---|---|
| `homological-modules-032` | 5 | 10 | 8 | 1 | 1 | 0 | [39874966863](https://github.com/Zengez/mathDef/actions/runs/39874966863) SUCCESS | [39874966763](https://github.com/Zengez/mathDef/actions/runs/39874966763) SUCCESS |
| `module-exactness-product-033` | 5 | 10 | 8 | 2 | 0 | 0 | [39875120418](https://github.com/Zengez/mathDef/actions/runs/39875120418) SUCCESS | [39875120272](https://github.com/Zengez/mathDef/actions/runs/39875120272) SUCCESS |
| `locally-ringed-sheaves-034` | 5 | 10 | 10 | 0 | 0 | 0 | [39875395849](https://github.com/Zengez/mathDef/actions/runs/39875395849) SUCCESS | [39875395931](https://github.com/Zengez/mathDef/actions/runs/39875395931) SUCCESS |
| `scheme-fibres-points-035` | 5 | 10 | 7 | 3 | 0 | 0 | [39875664362](https://github.com/Zengez/mathDef/actions/runs/39875664362) SUCCESS | [39875664411](https://github.com/Zengez/mathDef/actions/runs/39875664411) SUCCESS |
| `fibred-dual-higher-category-036` | 5 | 10 | 11 incl. correction | 0 | 0 | 1 | [39875912308](https://github.com/Zengez/mathDef/actions/runs/39875912308) SUCCESS | [39875912232](https://github.com/Zengez/mathDef/actions/runs/39875912232) SUCCESS |
| **Total** | **25** | **50** | **44 incl. 1 correction** | **6** | **1** | **1** | **ALL SUCCESS** | **ALL SUCCESS** |

All five corresponding `dependency_graph/applied/semantic-pass2-*.json` receipts were fetched and verified with `status=applied_in_independent_graph_only`, `human_certified=false`. Submitted packets preserve the entire prior mathematical reference adjacency. The hash precondition is the canonical SHA256 digest of the **whole effective node** after applying the final historical amendment for that formulation, not the stored references-only `snapshot_sha256`. Canonical snapshot checks and source `version_sha256` passed.

## Reviewed mathematical contexts

1. **Free resolutions:** independently distinguish free R-modules (arbitrary rank) from augmented chain complexes and exactness. Existing free-resolution meaning directly reused in a second Tor reference rather than spawning another missing prerequisite.
2. **Ext and Tor:** cochain complex Hom_R(F_•,N) and cohomology H^i(C^•) versus chain-complex homology H_i(C_•), with different co/contravariance, kernels and images.
3. **Projective module:** arbitrary free direct-summand characterization and the covariant Hom functor are reusable structures. The universal lifting requirement for projectivity itself is defining, not an extra missing prerequisite.
4. **Mittag-Leffler module:** arbitrary products ∏_i Q_i (not finite-support direct sums) and natural map M⊗∏Q_i→∏(M⊗Q_i). No automatic claim of surjectivity.
5. **Flat versus faithfully flat:** tensoring is a reusable functor, but preserving exactness is the defining flatness criterion; reflecting exactness is the defining additional faithful flatness criterion, not a synonym.
6. **Transfinite module dévissage:** split successor inclusions and directed unions at limit ordinals; ordinal-indexed continuity is not ordinary topological continuity.
7. **Finite module presentation:** finite-rank free R^m,R^n and finite generators for kernel relations, distinct from arbitrary free resolutions or polynomial relations of algebra presentations.
8. **Schemes and locally ringed spaces:** sheaf of rings, sheaf stalks, canonical structure sheaf on Spec(R), locally ringed-space isomorphism, direct-image f_*O and inverse-image f^{-1}O sheaves, sheaf isomorphism, and local stalk homomorphisms. Distinguish the direction O_Y→f_*O_X of a scheme morphism from f^{-1}O_Y→O_X on the domain.
9. **Scheme fibre products:** compatible cones and tensor products of commutative A-algebras versus universal property. Universal mediation clauses belong to the very scheme fibre product being defined.
10. **Gluing and functor of points:** overlap isomorphisms, cocycle equality as the defining gluing condition, Hom_Sch(T,X) and contravariant precomposition; chart-restricted Zariski topology characterization is source-local.
11. **Left monoidal duals:** evaluation/coevaluation and two snake/zigzag triangle identities; preserve distinction from Mac Lane's monoidal triangle coherence axiom.
12. **Fibred/groupoid structures:** category-valued and groupoid-valued Grothendieck construction, isomorphism over base (rather than only abstract equivalence), 1-morphisms over a base and natural 2-morphisms projecting to identities, and invertibly 2-commutative dotted-arrow fillers.
13. **Category-size correction:** the split fibred category's base C had been linked to a strictly **small** category definition even though source does not impose size; now corrected to provisional general size-unrestricted category requirement.

## Additional review debt and consistency priorities

From the Chunk13 accelerated audit ledger: **142 provisional source-local dispositions** and **306 raw new missing candidate identities** across Chunks7–13. Chunk14 adds **6** source-local dispositions and **44** raw missing records (including one existing-link correction), producing a working cumulative review ledger of **148 source-local dispositions and 350 raw new missing candidate records across Chunks7–14**. These counts are **not 350 vetted distinct mathematical concepts**, and all may be revised during the required contextual equivalence and source-citation audit.

New priorities:
- Free module R^(I) vs finite-rank free R^n vs free-resolution chain complexes; avoid conflating direct sum with direct product for infinite indexed families.
- Ordinary module Hom object versus covariant/contravariant Hom functors; Tor-chain homology versus Ext-cochain cohomology; 'lifting criterion' is not a circular projective prerequisite.
- Flatness preservation versus faithful-flatness reflection are different predicates; compare duplicate typed tensor functor candidates.
- Sheaf-of-rings generality, canonical structure sheaf on Spec(R), sheaf of groups vs rings, and sheaf morphism image directions; stalkwise sheaf isomorphism requirements versus isomorphism of locally ringed spaces.
- Hom_Sch(T,X) may need smallness/local-smallness assumptions distinct from a small category of schemes; no unsupported source-category smallness.
- Monoidal snake triangle versus monoidal associator/unitor triangle coherence and (2,1)-categorical invertible 2-cells.
- Strict isomorphism of fibred categories over C vs categorical equivalence over base and strict functor vs pseudofunctor; reconcile the one corrected general category C scope.
- Retain all earlier warnings about empty-space FIP convention, graded ring scopes, spectral V(I)/D(f) recursion, residue characteristic p=0, Cauchy-real operations/well-definedness, and source citation rigor.

## Mechanical resume contract

Read this Chunk14 and `research_pipeline/DEPENDENCY_FIRST_WORKFLOW.md`, then the LIVE `research_pipeline/experiments/reconstruction-v2-independent/dependency_graph/{STATE.json,CHECKPOINT.json,INVENTORY.json,unresolved_occurrences.jsonl,missing_candidates.jsonl,candidate_aliases.jsonl,amendments.jsonl}`. The live graph supersedes this dated checkpoint.

Continue **source-free full-formulation contextual review of 462 unassigned references** in packages of five or fewer formulations, retaining full source versions and all previous classified references. SHA precondition: `expected_node_sha256=digest(effective_full_node)`; validate `digest(effective.references)==effective.snapshot_sha256`. If `fetch_file` returns no text for large `amendments.jsonl`, use its current Git blob SHA with `mcp__GitHub__fetch` on `https://api.github.com/repos/Zengez/mathDef/git/blobs/<sha>` to read complete historical events. Verify applied receipt plus graph/test CI before counting work.

Do not perform new missing-definition/source research, edit original meanings/source records, compare production mathDef/frozen Wave1, add unrelated breadth, mark the consolidation gate true, certify or freeze Wave2 until all unassigned occurrences have been consolidated and the comprehensive cross-definition mathematical/contextual alias audit has been completed.
