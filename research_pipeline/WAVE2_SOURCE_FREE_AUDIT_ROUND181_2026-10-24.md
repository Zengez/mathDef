# Independent Wave2 source-free dependency audit — Round 181 (2026-10-24)

## Starting state, evidence and scope

Resumed after verified Round180, using the current **effective** `dependency_graph/edges.jsonl` and `STATE.json`, original independent `records/meanings.jsonl` formulation texts, selected node occurrence records and the compact `WAVE2_CURRENT_HANDOFF.md`. Source-free and independent-only: no original production mathDef, frozen Wave1, external missing-definition research, breadth Batch143, human/citation certification, original source-text edits, or consolidation approval.

Before this read-only review the graph contained 611 meanings; 659/659 complete scans (639 screened, 20 provisional); 728 raw missing candidates, 300 reviewer alias events, 7 candidate-to-existing resolutions, 421 unresolved canonical identities, 843 effective missing occurrences, 770 scan amendment events, 19 seed overrides, 0 ambiguous/unassigned, and 651 open/8 closed. Inventory SHA256 `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`; unresolved fingerprint `43bab18ecbb3d9789cf1fb6fc613e2a73b842a5de1d33a9023b7040e1693e2f4`; gate FALSE.

## Mathematical source-context checks

### 1. Functor variance and size discipline — no change justified

Read the complete independent meanings for the **general** contravariant functor `meaning.fef4e69e96c25bfa.contravariant-functor` and the **small-category-restricted** covariant functor `meaning.wave2.foundation.category-functor`. The latter's text explicitly begins “between small categories”; the former is defined as `F:C^op→D` without that size hypothesis.

The effective graph has **seven scan links** to the general contravariant functor (ten edges counting historical seeds) in:
- `form.23afebc5bde9e408.functor-of-points`
- `form.56d9781f393fa7d7.representable-functor-on-schemes`
- `form.a570f5bed277bd8b.presheaf-fibre-product`
- `form.a570f5bed277bd8b.representable-presheaf-morphism`
- `form.f7206eb9332b9389.category-valued-presheaf`
- `form.f7206eb9332b9389.split-fibred-category`
- `form.fef4e69e96c25bfa.representable-presheaf`

The source variance is correct: arrows reverse under precomposition, while split-fibred-category uses a strict contravariant category-valued functor, not an ordinary covariant one. The latest **effective** edges have **zero** references to `meaning.wave2.foundation.category-functor`; do not infer a live false target from an old node's pre-amendment references. The effective graph also has **six scan references** to `meaning.wave2.foundation.small-category`, in finite (hence small) diagram shapes and explicitly small foundation/category structures. A sampled original node for category-valued presheaf still displays stale small-category/functor references, whereas its current effective edges do not. **Always use effective graph state for conclusions.**

No erroneous variance or smallness retargeting was established; no packet submitted.

### 2. Strict-subset target specificity — four source links retained

The current scan edges targeting `meaning.wave2.foundation.subset-proper` occur in exactly four distinct source formulations: finite strictly increasing prime chains, chains of irreducible closed subsets with strict inclusions, proper maximal ideals, and proper prime ideals. Every original source explicitly calls for a **strict/proper** inclusion. Weakening these edges to general subsets would lose information; the four references were retained without changes.

### 3. Natural-number conventions — two meanings deliberately separate

The effective scan graph has **16** targets for the *positive* integer convention `meaning.wave2.set63.natural-positive-convention` and **24** for the *zero-including* convention `meaning.wave2.set63.natural-including-zero`.

Screened examples where positive indexing is warranted: field size `p^n` with `n>0`, primitive `n`-th roots of unity, tagged Riemann sums `i=1,…,n`, a sigma-algebra's `n≥1` countable union index, and positive-indexed rational sequences. Screened examples where zero must remain allowed: Bell number `B_0=1`, Stirling boundary values, the zeroth falling factorial `x^{\underline{0}}=1`, polynomial degrees including constant nonzero polynomials, nonnegative gradings, zero-indexed martingales and exponential generating functions.

**Coverage limit:** Several recent provisional formulations (notably `form.wave2.pop139`–`pop142`) have no text in the historical screened `records/meanings.jsonl`; their source texts live in the separate population overlay and were **not** independently read in this round. Therefore this is a targeted convention check, **not a complete audit/certification of all 40 edges**, and it does not license blanket retargeting. Nothing read justifies merging the two integer conventions.

### 4. Multi-formulation consistency samples — no change

Compared original independent mathematical texts for selected source variants:
- Noetherian module: finite generation of submodules, ascending-chain condition and maximal-element condition.
- Noetherian ring: finite generation of ideals, ascending-chain condition, maximal-element condition and module over itself.
- Normal subgroup: left/right cosets, conjugation equality and conjugation inclusion for **all** elements (including inverses).
- Convex subset and convex hull: binary convex combinations, finite positive convex combinations, least convex superset and intersection of all convex supersets, including the empty-set convention.
- Connected space (empty-space-allowed meaning): no nontrivial separation, no nontrivial clopen, and no continuous surjection onto the discrete two-point space.
- Discrete martingale: consecutive-time conditional expectation vs. arbitrary later-time conditional expectation, with integrability and adaptedness present.

The tested pairs/families agree under their stated hypotheses and conventions. This is a contextual sample, not a claim of full mathematical peer review or external citation verification. No aliases or amendments were warranted.

## Open mathematical quality follow-ups (unchanged)

The independent source formulation for a submersive continuous map still has the known logical caveat: `U⊆Y is open ⇔ f^{-1}(U) is open` does **not alone** ensure surjectivity (e.g. the empty-domain map into a nonempty indiscrete target). Its source sentence separately asserts surjectivity; do not rewrite the original source in this source-free phase. The perfect-closure characteristic-zero convention remains a later variant/quality issue; prior quasi-finite/local-dimension work carefully distinguishes fibre local-ring dimension from local topological dimension. No conclusion beyond earlier reports is asserted.

## End-of-round checkpoint and handoff

**Read-only round: no graph packets, no changed definition source, no numerical graph movement.** Re-read live `STATE.json` before the next packet rather than guessing from this report. Last verified graph: 611 meanings; 659/659 scans; 728 raw candidates; 421 unresolved canonical candidates; 300 aliases; 7 resolutions; 843 effective missing occurrences; 770 amendments; 19 seed overrides; zero ambiguous/unassigned; gate FALSE. Fingerprint `43bab18ecbb3d9789cf1fb6fc613e2a73b842a5de1d33a9023b7040e1693e2f4`.

Next reviews should find genuinely new high-impact object/scope/variance mismatches using the **effective** graph; avoid repeating the already-corrected Round177–180 category/groupoid/clopen changes. For provisional forms, read the population overlay, not just `records/meanings.jsonl`. Preserve source-free scope and evaluate diminishing returns before any **separately reviewed** consolidation decision. No human/citation certification or freeze was granted.
