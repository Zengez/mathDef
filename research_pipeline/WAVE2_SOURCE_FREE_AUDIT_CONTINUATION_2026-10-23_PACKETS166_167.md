# Wave2 source-free audit continuation — October 23, 2026, packets 166–167

**Status: exact independent-graph-only application verified; human certification is FALSE.** Both `semantic-global-audit-missing-alias-166` and `semantic-global-audit-missing-alias-167` have matching `applied_in_independent_graph_only` receipts. Eight reviewed mathematical **prerequisite** identities were appended, without adding mathematical meanings, changing original formulations or closing the source-free consolidation gate.

## Verified state and change

| Measure | Beginning (after packet 165) | Current (after packet 167) |
| --- | ---: | ---: |
| Meanings | 611 | **611** |
| Formulations scanned | 659/659 | **659/659** |
| Screened/provisional formulations | 639/20 | **639/20** |
| Raw candidate records | 724 | **724** |
| Cumulative contextual alias records | 271 | **279** |
| Candidate-to-existing meaning resolutions | 7 | **7** |
| Unresolved canonical candidate identities | 446 | **438** |
| Unresolved missing occurrence rows | 819 | **819** |
| Scan amendments | 765 | **765** |
| Ambiguous/unassigned occurrences | 0/0 | **0/0** |
| Graph open/closed | 651/8 | **651/8** |
| Consolidation gate | FALSE | **FALSE** |

Original inventory SHA256 stays `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`. New unresolved canonical fingerprint: `8e680a8bec257e29452c8bc0f6d690fa7d9cae95e057317dc873d01450a556da`. The 438 candidate identity classes are **not** independent confirmations of 438 absent standalone mathematical definitions.

## Decisions: packet 166 (five)

1. `missing.68baad0cbaf9575f0b7e` → `missing.08a2969d79ad1ddc1922`: in going-up/going-down, prime q of S lies over prime p of R precisely when the contracted prime under the specified ring homomorphism is p; the **existence of chain-compatible primes** remains a separate parent condition.
2. `missing.ff999343a9d3baed47b5` → `missing.2ca12da5425144816e3c`: the **open** neighborhood U containing x in local Krull dimension/local finiteness is the same object used in Hausdorff and pointwise-continuity sources. This does **not** identify ordinary not-necessarily-open neighborhoods with open ones.
3. `missing.2473a37ecddeac42985e` → `missing.fcb5ab865c6d9dbb3d79`: base category C of split fibred category is ordinary, size unrestricted. Splitness and Grothendieck construction are not inherited by generic categories.
4. `missing.5b9f93c9e8355c4bc4c0` → `missing.fcb5ab865c6d9dbb3d79`: ordinary ambient category for categorical fibre product; pullback existence and universal property remain with the fibre-product source.
5. `missing.7dc109f22452f0217a2a` → `missing.fcb5ab865c6d9dbb3d79`: underlying ordinary category I in filtered-category definition. Filteredness, nonemptiness and coequalizing parallel arrows are not assumed by every category.

## Decisions: packet 167 (three)

6. `missing.5d09c68ceead2919f965` → `missing.fcb5ab865c6d9dbb3d79`: the diagram index I and target C are ordinary categories; the distinction of their roles and universality of (co)limits remain parent-specific, with no artificial smallness of C.
7. `missing.8b7c553a4b15276100e5` → `missing.c5104821c3c70afa1f63`: `−⊗_R M` is an **ordinary covariant functor** on module categories. Its tensor action and exactness preservation/reflection requirements remain in flatness/faithful flatness parent texts.
8. `missing.e451d61d5424959081ca` → `missing.c5104821c3c70afa1f63`: `Hom_R(P,−)` is an ordinary covariant functor acting by postcomposition. Hom-specific construction and exactness are still source-specific and do not hold for arbitrary functors.

Reviewer rationales and source contexts are preserved in the immutable packets at `experiments/reconstruction-v2-independent/dependency_graph/inbox/`; matching exact receipts appear in `applied/`. The decisions **do not** collapse the definitions of a tensor functor, a Hom functor and an arbitrary functor or declare their special properties automatic. This reuse policy remains a potential area for later specialized-variant population review.

## New high-priority *review leads*: groupoid smallness in effective graph

The independent source meaning `meaning.wave2.foundation.small-groupoid` explicitly defines a groupoid as a **small category** with all arrows invertible. Three *effective amended* nodes currently reference this meaning without explicitly restricting their groupoids to be small:

- `form.74cd6dc48e0606fc.setoid-category`, reference index 0, phrase `groupoid C`.
- `form.0bf601085c1029d4.two-one-category`, reference index 2, phrase `groupoid`, for arbitrary hom-categories of a strict (2,1)-category.
- `form.5e4b8f6efeda6522.category-fibred-in-groupoids`, reference index 3, phrase `groupoids`, for fibred-in-groupoids structure without an explicit size bound.

These are **plausible false-target/scope restrictions** and warrant a future precisely anchored correction, but this round did **not** certify them as errors or change their dependency reference states. Unlike the previously reported category-size issue from outdated base nodes, this groupoid concern was detected by replaying the **current effective** append-only amendment ledger for 577 amended formulation nodes. The groupoid-valued presheaf source explicitly targets `Groupoids`, a category of small groupoids in this independent corpus, and was **not** flagged.

A new **read-only heuristic** in `research_pipeline/engine/dependency_global_audit.py` emits `groupoid_size_scope` for such cases, unless the source explicitly says `small groupoid`, `finite groupoid` or names the `Groupoids` target category. A direct independent replay of the 765-event effective amendment ledger with the same mathematical predicate detected precisely the three nodes above. **Remote Python syntax/CLI tests were not run** in this tool session, and this is a reviewer lead rather than mathematical certification. The project workflow documentation now explains the check. The correct future correction must preserve *both* groupoid invertibility and any size restrictions explicitly present; blindly aliasing to a generic category alone would lose a mathematical prerequisite. There is currently no reviewed, registered size-unrestricted groupoid candidate suitable for an automatic target swap.

## Additional 20/20 provisional formulation read-only source-text inspection

All **20 provisional formulations** in the independent inventory (Batches 139–142) were inspected for their stated domain, quantifiers, boundary cases and displayed mathematical conditions. The list spans: two integer congruence variants, matrix trace, two affine hull variants, three event-independence formulations, finite graph cycle, two connected-space variants, left and right group actions, metric outer measure, ordinary outer measure, bounded linear transformation, two equivalent operator norm statements, contraction map, and proper k-vertex coloring.

No new definite mathematical inconsistency was established from these standalone source statements in this pass. These contextual qualifications should remain explicit:
- A connected space may **include the empty space** under the separation/clopen convention of the provisional variants, contrasting with the nonempty connected-space source elsewhere in Wave2. Do not silently drop this scope difference.
- A contraction map here is **allowed to have different domain/codomain metric spaces**; Banach fixed-point consequences need a self-map and other additional conditions.
- A proper k-vertex coloring **need not use all k colors**; the no-surjectivity condition is deliberate.
- Matrix trace assumes n≥1 as stated, and the operator norm is defined for **bounded** linear maps on real/complex normed spaces.
- Metric outer measure uses the positive-distance additivity condition and extended values; the empty-set distance convention is explicitly specified.
- Left and right group actions use different composition orientations; they should remain separate contextual formulations.

This is a **source-free text-consistency pass**, not external source provenance checking, reference verification, a claim that the 20 statements are all mathematically certified, or full normalization of variants. The earlier three reported source issues—quasi-finite local fibre, surjectivity within the submersive-map equivalence, and characteristic-zero perfect closure convention—remain open and untouched.

## Resume contract

Use current live `dependency_graph/STATE.json`, `CHECKPOINT.json`, `INVENTORY.json`, `amendments.jsonl`, reviewer alias packets 166–167 and their exact receipts. Never infer effective dependencies only from original `nodes/*.json`. Prioritize mathematically valid size-unrestricted groupoid dependency handling, distinguish source-level equivalence issues from shared-prerequisite identities, and continue source-free candidate classification and varied-source checks. **Do not** open the consolidation gate, populate new definitions through external research, resume Batch143 breadth, modify the original mathDef production corpus or frozen Wave1, certify sources, or freeze Wave2.
