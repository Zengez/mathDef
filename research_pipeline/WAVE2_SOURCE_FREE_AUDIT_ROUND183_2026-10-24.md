# Independent Wave2 source-free audit — Round 183 (2026-10-24)

## Verified starting position

Continued from [Round182](WAVE2_SOURCE_FREE_AUDIT_ROUND182_2026-10-24.md) and the [current handoff](WAVE2_CURRENT_HANDOFF.md). Consulted original independent formulation records and source provenance, source-context reference nodes, and the effective graph/state; did **not** use production mathDef, frozen independent Wave1, external missing-definition research, Batch143 or unapproved population reconciliation.

Latest independently read `dependency_graph/STATE.json`: **611 meanings; 659/659 scans complete (639 screened, 20 provisional); 728 raw candidate records; 300 alias decisions; 7 candidate-to-meaning resolutions; 421 unresolved canonical candidates; 843 effective missing occurrences; 770 append-only scan amendments; 19 seed overrides; 0 ambiguous/unassigned; 651 open / 8 closed; consolidation gate FALSE**. Inventory `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`, unresolved fingerprint `43bab18ecbb3d9789cf1fb6fc613e2a73b842a5de1d33a9023b7040e1693e2f4`. These are structural workflow counts, not mathematical or citation certifications.

## New finding: topological ring/module source-convention mismatch (high-priority mathematical scope review)

Inspected all four related independent meanings, the original full text, indexed source metadata and explicit reference nodes for topological group, profinite group, topological ring and topological module.

1. `form.646e4dcbd9b6f1e1.topological-ring` (record cites Stacks Project Definition 5.30.7, tag `0B1Y`):

   > A topological ring is a ring R with a topology for which its addition R×R→R and multiplication R×R→R are continuous maps.

   Its effective existing reference for `ring R` is `meaning.wave2.foundation.associative-ring-identity-optional`, **explicitly** permitting rings without a multiplicative identity. It does **not** state that additive inversion x↦−x must be continuous or that (R,+) is a topological group.

2. `form.646e4dcbd9b6f1e1.topological-module` (same source section, Definition 5.30.10) requires continuous addition and scalar multiplication, but its existing `R-module M` reference points to `meaning.wave2.foundation.left-module-nonunital`, explicitly permitting an action without 1_R m=m. No continuity of m↦−m is stated.

3. `form.646e4dcbd9b6f1e1.topological-group` (Definition 5.30.1 in the same source collection) **does** require both multiplication and inversion continuity. The profinite-group formulation correctly depends on the full topological-group notion.

### Explicit mathematical counterexample under the currently linked nonunital convention

Let R be the additive group of integers `(ℤ,+)`, equipped with **zero multiplication** `a·b=0` for all a,b∈ℤ. This is an associative, commutative **nonunital** ring. Give its underlying set the **upper-set topology**: a subset `U⊆ℤ` is open if and only if `n∈U, m≥n ⇒ m∈U` (including ∅).

- Addition `+:R×R→R` is continuous: if `x+y∈U`, the neighborhoods `[x,∞)` and `[y,∞)` have pairwise sums in `[x+y,∞)⊆U`.
- Multiplication `R×R→R` is constant at 0, hence continuous.
- Additive inverse `x↦−x` is **not** continuous: the inverse image of the open set `[0,∞)` is `(−∞,0]`, not an open upper set.

This ring therefore satisfies the **literal reconstructed topological-ring formulation and its explicitly nonunital prerequisite**, but its additive group is **not** a topological group.

Now let M=ℤ carry the same upper-set topology and make it a left R-module by the **zero scalar action** `r·m=0` for all r,m. The module axioms hold over this zero-multiplication nonunital R. Addition on M is continuous, scalar multiplication is constant/continuous, and negation on M fails continuity. Thus the current **literal** topological-module formulation likewise permits a module whose additive group is not topological.

### Important qualification: unital hypotheses change the conclusion

For a **unital ring**, continuous multiplication implies that additive inversion is continuous by `-x=(-1_R)·x`: multiplication by the fixed element `−1_R` is continuous. Likewise for a **unital left module** over a unital topological ring, `-m=(-1_R)m` and continuity follows from scalar multiplication. The current source records are indexed to Stacks definitions, whose ambient ring/module conventions must be checked at source-citation reconciliation; the above is **not** a claim that the original Stacks statements are mathematically false in their actual convention.

The defect is therefore a **scope mismatch/under-specification within this reconstructed independent collection**: its texts and explicit prerequisite links adopt a nonunital interpretation for which omission of inversion continuity is mathematically consequential. An eventual reviewed repair should either:
- Explicitly restrict the corresponding ring and module meanings/references to **unital** ring/module contexts where negation continuity follows; or
- Retain general nonunital rings/modules but require that the additive groups are **topological groups**, in addition to continuous multiplication/scalar multiplication.

Do not silently switch either convention; the source-dependent choice and compatibility with other independent meanings must be justified and provenance-preserving.

## Relevance to graph links and action boundaries

This is **not** an excuse to retarget the current literal phrase `ring R` to an unital meaning without re-review: it would impose an unstated hypothesis. Nor is the existing topological-space/continuity/product-topology link intrinsically wrong. The issue is that the **mathematical content and intended prerequisite scopes do not jointly guarantee the customary topological algebra structure**.

The targeted existing reference records were compared:
- `form.646e4dcbd9b6f1e1.topological-ring` → nonunital `associative-ring-identity-optional`;
- `form.646e4dcbd9b6f1e1.topological-module` → `topological-ring` and nonunital left `module`;
- `form.646e4dcbd9b6f1e1.topological-group` → group with inversion-continuity condition;
- `form.646e4dcbd9b6f1e1.profinite-topological-group` → the ordinary topological group.

No dependency node was amended because all safe mathematical fixes require explicit **source convention and/or formulation** review, not an unsupported source-free link change. New meanings, outside source consultation and production edits remain prohibited in this phase.

## Other reviewed consistency sample

As a complementary source-free inspection, enumerated 106 of the 639 screened formulations containing phrases such as `equivalently`, `exactly when` or `if and only if`. Revisited selected hypotheses for the screened equivalence definitions of compactness (open covers vs closed-set FIP), connectedness (empty-space convention), pure ideals (quotient flatness vs ideal-intersection test), group setoids (invertibility and trivial automorphisms), categorical exactness, and natural/isomorphism definitions. This is a **screening/worklist inspection**, not a proof of all 106 equivalences; no second independently established error was promoted from this sample.

## End-of-round / next work

**Read-only mathematical issue discovered, no graph packet submitted, no ledger or source definition changed.** Log the topological ring/module nonunital-versus-inversion issue as a high-priority source/variant reconciliation lead, along with the existing submersive-map surjectivity biconditional and perfect-closure characteristic-zero variant caveat. The earlier quasi-finite distinction between **fibre local-ring dimension** and **local topological dimension** must continue to be protected.

Resume high-impact effective graph/type/variant review after reading live STATE. Investigate math source conventions only when the separate external source/citation and source-revision gates permit them. No consolidation gate, population promotion, human certification, frozen Wave1 changes or original-production edits are authorized.
