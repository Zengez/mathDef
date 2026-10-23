# Wave2 source-free audit continuation — October 23, 2026, packets 158–161

**Status: VERIFIED APPLIED TO INDEPENDENT GRAPH ONLY.** Four source-context-reviewed alias packets 158–161 have exact `applied_in_independent_graph_only` receipts, each `human_certified=false`. They contain **19 additional reviewer-authored prerequisite alias judgments**, packet sizes **5 + 5 + 5 + 4**. This continuation did not edit source mathematical formulations, evidence, independent Wave1, original mathDef production, or the consolidation gate.

## Recovery and methodology correction: effective graph versus original nodes

The preceding [154–157 handoff](WAVE2_CONTEXTUAL_AUDIT_CONTINUATION_2026-10-23_PACKETS154_157.md) flagged several apparent links to the **small-category** and **small-to-small functor** meanings as a high-priority *possible* scope error. This round verified that the apparent incorrect edges were in **historical original scan snapshots**, not the current effective graph. The append-only `dependency_graph/amendments.jsonl` ledger already contains **up to three corrections per sampled formulation** replacing them with the correctly typed `missing.fcb5ab865c6d9dbb3d79` (unrestricted category) and `missing.c5104821c3c70afa1f63` (unrestricted ordinary functor), as appropriate.

Checked the original independent full-text formulations, the precise meanings of `meaning.wave2.foundation.small-category` and `meaning.wave2.foundation.category-functor`, and the **latest recorded amendment replacement snapshots** for:
- `form.56119d315cf02fdf.two-category-over-base`
- `form.fef4e69e96c25bfa.opposite-category`
- `form.fef4e69e96c25bfa.contravariant-functor`
- `form.ec5e3a0d13f85f3a.strict-two-category`
- `form.709d3d2f82950c5b.inductive-system`
- `form.709d3d2f82950c5b.inverse-system`
- `form.6775f8b2e6e1cceb.grothendieck-fibred-category`

**All seven sampled current effective nodes already preserve unrestricted category and functor typing in their relevant reference slots.** The earlier scope inconsistency warning about these particular effective links is **resolved / a stale-snapshot false positive**. Do **not** submit redundant false-target amendments. The reusable global auditor's `live_nodes` mechanism already replays amendments; future manual review must do the same, rather than relying on `dependency_graph/nodes/*.json` alone.

The full amendments ledger and original independent `INVENTORY.json` were read by **exact Git blob SHA** for this verification, because the normal file-content response does not expose their large full bodies. This method recovered the intact 765-event ledger and all 659 inventory entries; no repository records were rewritten.

## Exact graph comparison

| Metric | Verified start after packet 157 | Verified after packet 161 |
| --- | ---: | ---: |
| Mathematical meanings | 611 | 611 |
| Scanned formulations | 659 / 659 | 659 / 659 |
| Provisional formulations | 20 | 20 |
| Raw candidate identities | 724 | 724 |
| Reviewed missing-candidate alias events | 245 | **264** |
| Existing-meaning resolutions | 4 | 4 |
| Unresolved canonical candidate identities | 475 | **456** |
| Unresolved missing occurrence rows | 822 | 822 |
| Append-only mathematical scan amendments | 765 | 765 |
| Unassigned / ambiguous occurrences | 0 / 0 | 0 / 0 |
| Graph structural open / closed | 651 / 8 | 651 / 8 |
| Consolidation gate | FALSE | FALSE |

Original source-inventory SHA256 remains `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`. Latest unresolved canonical fingerprint is `20287c1e30bae866d0b2ed3d2aa186d36f92426bc2fd7a2de7ec2ee3faa59270`. The `456` figure denotes **unresolved candidate identity classes**, not a count of verified absent definitions. Source evidence remains structurally traceable but **not externally citation-certified**.

## Review and applied decisions

### Packet 158 — five aliases

- `missing.be21819dbf92c119e444` → `missing.0c99be984399f9134720`: multiplicative subset used in localization, specialized to all nonzero-divisors for total quotient ring.
- `missing.3bc9c793050ced5e186f` → `missing.f112efe448973069bae2`: finite indexed intersections, including the empty intersection, shared by topology/subbasis statements.
- `missing.a6b162089f9cb7a865be` → `missing.2d82e7722cfbce9eca14`: tensor products of commutative unital algebras, variables A/B/C versus R/S/R′.
- `missing.88078f7f55020544980e` → `missing.ad976486b1e3635e60d2`: K-algebra scalar extension A⊗_k K with the same multiplication.
- `missing.abbeccae2b7cf4128cfd` → `missing.fbd11071cfe5ca8ef6e2`: elementwise conjugation gNg⁻¹ of a subset, specialized to subgroup N; normality retains its own inclusion/equality clauses.

### Packet 159 — five aliases

- `missing.cfc33bf502fe3236bf86` → `missing.e43d4f1922e210cc373a`: finite iterated ideal multiplication specialized to prime-ideal factorization in a Dedekind domain.
- `missing.a7cbeca3e5f5d1ce1e33` → `missing.7413d0506040cdeb60af`: structure-sheaf stalk O_{X,x}, as filtered colimit; local-ring property stays parent-specific.
- `missing.e1eeea250fa81655407a` → `missing.77eacb7314c513d85c72`: isomorphism over base C with inverse over base, specialized to fibred categories.
- `missing.42f6560f7237a67371f0` → `missing.ef28497e9dc38c5b82e5`: finite strict chains of irreducible closed subsets; maximality/fixed endpoints remain specific to catenarity.
- `missing.830ec6095a60fa189021` → `missing.c5104821c3c70afa1f63`: p:E→C is an ordinary size-unrestricted functor before the fibration conditions.

### Packet 160 — five aliases

The underlying unrestricted ordinary functor F:C→D, with identity/composition preservation, was independently found within:
- `missing.7f7a9ea9ba237d4d230d` — diagram F:I→C;
- `missing.ba7c7234ba3861b43a27` — pair F:A→C, G:B→C;
- `missing.c02e1ce9fa43e5498d67` — oppositely oriented pair of functors used in an adjunction;
- `missing.78bf491fb0c8921f9fe5` — functor commuting with projections over C;
- `missing.2eeb694b49cd0cf12a88` — tensor bifunctor C×C→C, a functor from the product category.

Each aliases to `missing.c5104821c3c70afa1f63` as a **shared mathematical prerequisite**, with the different domain/category shapes, projection equations, adjunctions, monoidal coherence, and diagram-index assumptions preserved by the original source-level definitions. Neither categorical smallness nor pseudofunctor structure was silently introduced.

### Packet 161 — four aliases

- `missing.8935c9439ad08cf80a1b` → `missing.11276cd4f561922a8529`: transitivity property of binary relations in a preorder versus an equivalence relation.
- `missing.99ed82d968323ff940b1` → `missing.a8c70a2a13320680c54c`: natural transformation of presheaves, used as one or two arrows; representability/pullback-specific constraints remain parents.
- `missing.1572a58850a1f38252f4` → `missing.ca9ba1e0fc16e5162ef7`: ordinary associative unital rings, instantiated twice in a ring-homomorphism definition; the unital homomorphism equation does not follow from ring unitality.
- `missing.1bc737c9f2d261a2de5b` → `missing.2a57a4bcdc8b7937c52e`: the unit ideal (1)=R shared by localized-section compatibility and polynomial coprimality; the finite list of generating elements and Bézout combination are parent-specific.

## Separations and follow-up

Lexical near matches that remain **mathematically different** and must not be blindly aliased: left versus right group translations; radical ideals versus radical of an arbitrary ideal; Hermitian sesquilinear versus real symmetric bilinear forms; ascending versus descending chain conditions; module direct product versus finite-support direct sum; homology versus cohomology; finite versus countably infinite orthogonal polynomial support; natural isomorphisms versus monoidal coherent structure; open versus general neighborhoods. In particular, a graded module's homogeneous degree pieces are not necessarily R-submodules when the base ring is nontrivially graded: **do not** automatically alias its graded direct-sum decomposition with a direct sum of ordinary R-modules.

Three earlier source-level mathematical flags are still UNCHANGED: the quasi-finite local-fibre point equivalence, submersive map lacking explicit surjectivity in the alleged equivalence, and perfect closure characteristic-zero convention/variant coverage. Original source statements or citations have not been corrected under the source-free graph phase.

**Methodology risk to monitor:** An alias here represents an identical **underlying prerequisite**, not equivalence of all hypotheses or full parent definitions. At later missing-definition population time, ensure variants of specialized concepts are not lost simply because the prerequisite's identity aliases to a more generic construction. Preserve the original observed candidate, full context and source formulation in the audit ledger.

## Resume next

1. Read live graph `STATE.json`, `CHECKPOINT.json`, `INVENTORY.json`, `amendments.jsonl`, four packet receipts, and this report. Reconstruct *effective* references before flagging errors.
2. Continue high-impact contextual identity reviews and sample unrelated non-similar formulations for false targets and source-mathematics errors.
3. Prepare future source-level correction stage separately; **no unapproved original text rewrites or external citation certification**.
4. Keep consolidation gate FALSE, missing-definition external research OFF, breadth Batch143 ON HOLD, Wave1 frozen, and original production mathDef unmodified. Neither zero unassigned references nor these aliases is mathematical peer certification.

