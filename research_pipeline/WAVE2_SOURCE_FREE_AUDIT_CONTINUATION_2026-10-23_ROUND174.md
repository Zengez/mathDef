# Wave2 source-free audit — Round 174 (October 23, 2026)

## Result: historical seed relationships have an independent scope-audit blind spot

After Round 173 recovered the append-only effective graph, this round read the authoritative **inventory** (Git blob `eaed3c32b194e75d1538193cb286ca18c8f68575`) and full **effective occurrence index** (Git blob `f79d18ec495352f5484372e1faeb8a301562fe00`). The graph holds **4,489 effective occurrence records**, including **2,672 existing-target references**. These comprise both contextual scanner references and historical authoritative seed relations.

An important distinction is now established:

- There are **27 links** in the effective occurrence index to `meaning.wave2.foundation.small-category`.
- **21** of these are original seed relations; the other **six** were asserted by the contextual scanner.
- The six scanner links are grounded in explicitly **small** categories or **finite** indexing categories. They were not shown to be incorrect merely because the historical seed target is restrictive.
- The legacy seed target `meaning.wave2.foundation.category-functor` also explicitly describes functors between **small** categories, whereas the two source definitions feeding it do not specify smallness.
- Source-free review of all **891 seed relations** revealed **25 targeted seed edges** to these three restricted concepts (small category, small-category functor, small groupoid). **20 require size-convention review**; five explicitly establish a compatible scope.

**No mathematical meaning, source formulation, seed relation, alias, resolution or graph node was automatically rewritten.** These are actionable audit findings, **not 20 certified source errors**.

### Why source scope materially matters

Smallness is a property of the **size of the object/morphism collections**, not merely a property of being a category. A terminal object, a monoidal category or an adjunction can live in a non-small but locally small category.

For example, in the ordinary category `Set` of sets (under a standard class/universe convention), the singleton is a terminal object and Cartesian product makes `Set` monoidal, even though the category is not small in the unrestricted set-theoretic reading. Likewise, free-group construction is left adjoint to the forgetful functor between large categories of sets and groups. These are counterexamples to treating *small category* as an intrinsic prerequisite of those notions.

A **locally small** category (each Hom is a set) need not be **small** (the whole category has set-sized collections of objects and arrows). Existing source texts vary in which size convention they establish, and the graph should not silently import one stronger than needed.

### Exact review queue from the live 891-seed inventory

| Source formulation term | Historical target | Why flagged |
| --- | --- | --- |
| epimorphism | small category | Arbitrary ambient category |
| monomorphism | small category | Arbitrary ambient category |
| colimit of a diagram | small category | Diagram/ambient category not declared small |
| limit of a diagram | small category | Diagram/ambient category not declared small |
| connected category | small category | Connectivity does not impose smallness |
| discrete category | small category | Discreteness does not impose smallness |
| filtered category | small category | Filteredness does not impose smallness |
| final object | small category | Terminal objects can exist in large categories |
| initial object | small category | Initial objects can exist in large categories |
| monoidal category | small category | Monoidal structures need not be small |
| opposite category | small category | Opposite construction works at same general size |
| covariant set-valued representable functor | small category | Base category not declared small |
| multiplicative system of arrows | small category | Source does not establish smallness |
| cartesian arrow over base category | small category | Source `p:E→C` not declared small |
| pseudofunctor from category to strict 2-category | small category | Ordinary source category not necessarily small |
| strict 2-category | small category | Hom-categories need not be small without further assumptions |
| preadditive category | small category | Enrichment in abelian groups does not bound object-class size |
| left adjoint | functor between small categories | Adjunction need not be between small categories |
| covariant set-valued representable functor | functor between small categories | Representability need not constrain size |
| setoid category | small groupoid | An equivalence-relation-on-a-set presentation implies smallness, but this source does not explicitly declare the set/universe convention |

**20 seed records in total:** 17 `legacy_seed_category_size_scope`, two `legacy_seed_functor_size_scope`, and one `legacy_seed_groupoid_size_scope`. Each warning records its original immutable `relation_id`, source formulation ID, full original text, historical target, and a distinct legacy-seed occurrence identity. The new check is intentionally **review-level**, not a declaration that an unrestricted source is actually intended in all conventions.

The five other targeted seed relations are not flagged: their source explicitly states **small categories** or names the category `Groupoids` in the already-established typed convention. The finite-category exemption is independently regression-tested.

### Why fixing effective scan nodes alone cannot repair these references

The graph engine reconstructs effective adjacency from **both** source inventory seed relations **and** the versioned effective scan nodes. Even when a contextual scanner amends its complete node to use a missing **size-unrestricted** category candidate, the original historical seed relation can still contribute a separate edge to the restricted small-category meaning.

Thus an incorrect seed source target is not safely fixed by merely editing or replacing a scanned reference. Such edits would leave a misleading surviving historical edge. Any future direct correction needs a documented provenance-preserving, version-bound seed-target review mechanism or an explicitly approved source-relation change. **Do not mutate authoritative seed files or shadow them with untracked deletions in the current source-free consolidation phase.**

This distinction explains why earlier audits could report an apparent small-category violation even after several effective node corrections had already been applied.

## Code and tests committed

1. `research_pipeline/engine/dependency_global_audit.py` now independently inspects seed targets for category, groupoid and functor size restrictions. Explicit **small or finite categories**, explicit **small/finite groupoids**, and the exact named target `Groupoids` exempt the respective warnings. Every warning carries **origin=preexisting_seed_relation**, original immutable relation ID, and source-scoped rationale.
2. `research_pipeline/tests/test_dependency_global_audit.py` now tests generic categories (flag), explicitly small/finite categories (not flagged), unrestricted groupoids (flag), the named `Groupoids` convention and explicit small groupoids (not flagged), and unrestricted versus explicitly small functors. It also checks that warnings have **review** severity and retain exact historical relation identity.

Commits:
- `6fa688927275105bb1b57264c930e391b073c412` — audited historical seed relations.
- `52798eb9669c54ba1216d2f25863dc576a458f90` — finite-category size exemption.
- `f8b9a156381f532be50280f57b42bbdb2212e77b` — provenance and type-sensitive regression tests.

[Isolated research-pipeline tests #40051896667](https://github.com/Zengez/mathDef/actions/runs/40051896667): **SUCCESS**.

## State / boundaries

Graph remained exactly as verified in Packet 172 / Round 173: **611 meanings, 659/659 scanned (639 screened, 20 provisional), 724 original missing identities, 297 reviewed aliases, 7 candidate-to-existing resolutions, 420 unresolved canonical identities, 819 missing occurrence rows, 765 append-only amendment events, 0 ambiguous/unassigned, 651 structurally open and 8 closed. Consolidation gate FALSE.**

Inventory SHA256 `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492` and unresolved fingerprint `f740c264e171ba568241e8925c32efd5e53d8f528f8976fd7e9f9308a7300554` unchanged. The run performed no outside research, no citations verification, no mathematical meaning additions, no original screened/provisional formulation edits, no frozen Wave1 or production-site data edits, no breadth Batch143, no alias count reductions, no source/graph gate changes, and no human certification.

### Next handoff

The priority is no longer synonym count reduction: review these **20 historical size-scope leads**, separating true source convention, false legacy target and safe subsumption. Plan the provenance-preserving seed-relation correction mechanism **before** changing any seeds, while keeping original source snapshots intact. Continue occasional whole-formulation mathematical consistency review (rather than relying on automated warnings as proof). Once the substantive risks are exhausted, assess whether to authorize a new source-research phase rather than repeating source-free scans indefinitely.
