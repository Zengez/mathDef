# Wave2 source-free mathematical dependency audit — Round 180 (2026-10-24)

## Authoritative state and method

Started at verified Round179: 611 meanings, 659/659 complete formulation scans, 421 canonical unresolved prerequisite identities, 842 effective missing occurrences, 769 scan amendments, 300 aliases, 7 resolutions, 0 ambiguous/unassigned, no consolidation approval. Inventory SHA256 `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`; starting unresolved fingerprint `5ce283b1e53f511a472b9913440f36a3f40a827378823afddd33200c2af7a96a`.

Examined current **effective** post-amendment references, not stale original node snapshots; read complete original independent source formulations, surveyed the most reused populated meaning targets and highest-frequency unresolved prerequisites, and checked comparable topology, commutative-algebra and module-reference contexts. This pass did **not** use the original production mathDef corpus, external missing-definition research, frozen Wave1, breadth Batch143, or mathematical/citation certification.

## Applied mathematical object-type correction

Source: `form.097db25e2f156689.clopen-subset-of-spectrum` (clopen subsets of an affine spectrum; unchanged original source version `7d47c90a9aac6cfa2da71d348da436f571c8f1369b34e7a45ae326113bf59a3e`).

The phrase `simultaneously open and closed` in

> For a commutative ring R, a subset U of Spec(R) is simultaneously open and closed exactly when there is an idempotent e of R ... with U=D(e).

was linked to `meaning.wave2.foundation.topological-space`. That link was insufficiently typed: it refers to the axioms of the *ambient* space, while the occurrence asserts that the subset `U` itself has **both** openness and closedness. The full parent source already has independent links to `Spec(R)`, subset `U`, idempotent `e`, and distinguished open `D(e)`.

The pre-existing canonical candidate `missing.b599bdc9343a25050226` expresses precisely the **general** clopen-subset predicate and already had three incoming connectedness-definition contexts (including alternative empty-space conventions). A complete-node amendment changed **only** that one wrongly typed occurrence from `existing:topological-space` to `missing:generic-clopen-subset`, carrying an explicit `reviewed_existing_candidate_id`, the original source phrase and a detailed identity-review rationale. This was an **existing candidate reuse**, not creation of a new meaning or a forced synonym match.

- Source-reviewed amend packet: `dependency_graph/inbox/wave2-sourcefree-round180-clopen-spectrum-candidate-reuse.json`
- Applied receipt: `dependency_graph/applied/wave2-sourcefree-round180-clopen-spectrum-candidate-reuse.json`, SHA256 `09049e2a9c1f3d85309bee49d2127e88a8d9ebf50cb772a4a38bb17a6b258abc`, mode `amend`, status `applied_in_independent_graph_only`, `human_certified=false`
- [Git commit `9bc695f3b523`](https://github.com/Zengez/mathDef/commit/9bc695f3b5232bfab8f710448fe801e2e442b586)
- New canonical clopen candidate incoming contexts: **4** (the affine-spectrum example plus 3 general connectedness formulations); graph candidate total and alias count **unchanged**.

The amendment's exact receipt and the new `unresolved_occurrences.jsonl` reference were checked after graph processing. The new effective occurrence is `occ.982109ad4faf2e20b72d`.

## Reviewed, deliberately unchanged mathematical dependencies

1. **Finite generation of ring ideals vs. modules.** Reviewed the full statements of a finitely presented ring map, the Tor flatness test with finitely generated ideal `I`, and the pure-ideal intersection test with finitely generated ideal `J`. All three use the populated *finitely generated module* dependency, which may initially appear insufficiently typed. In a commutative ring, however, an ideal is an `R`-module, and generation by a finite list as an ideal is equivalent to generation by that list as an `R`-module. Their separately recorded ideal/ring hypotheses remain present. **No unsupported retargeting was made.**
2. **General set-theoretic preimages.** Audited all 15 effective uses of `missing.b86257b3cce62907e97e` (inverse image) across continuous/quasi-compact maps, scheme prime contraction, module kernels, measure pushforwards and random variables. Every occurrence invokes the same set-level preimage operation; ring, topology and measurable-set properties are extra parent conditions. Do **not** split by superficial algebraic/topological notation or mistake `f^{-1}[B]` for an inverse function requiring bijectivity.
3. **Quotient rings.** Examined all 16 incoming full source contexts of canonical `missing.50fc57153b93520a247a`: polynomial quotients, prime-ideal quotients, `I`-adic completions, formal smoothness/étaleness, Tor and fibre-local-ring quotients. All are compatible with the commutative-unital quotient-ring construction as the shared prerequisite; field/flatness/fibre/finite-presentation constraints remain source-specific. No new alias or meaning was needed.
4. **Residue fields.** Inspected 11 incoming source contexts of `missing.38969d113c4ee1db6e98` (local-ring residue fields), covering Henselianity, fibre criteria and regularity. The underlying `A/\mathfrak m` and `\kappa(p)` instances are correct; context-specific relative-fibre statements remain candidate source-quality reviews, not grounds to merge primes or base fields.

## Verified end-of-round graph

| Metric | Verified |
| --- | ---: |
| Independent meanings / scanned formulations | **611 / 659 of 659** |
| Raw missing-candidate IDs | **728** |
| Canonical unresolved candidates | **421** |
| Reviewed aliases / resolutions | **300 / 7** |
| Missing-reference occurrences | **843** |
| Append-only scan amendments / seed overrides | **770 / 19** |
| Ambiguous / unassigned | **0 / 0** |
| Structurally open / closed | **651 / 8** |
| Consolidation gate | **FALSE** |

Final unresolved fingerprint: `43bab18ecbb3d9789cf1fb6fc613e2a73b842a5de1d33a9023b7040e1693e2f4`. Original inventory SHA unchanged.

## Handoff

Continue with truly new source-level object, variance and size mismatches; prioritize existing links with high fan-in and preserve valid generic prerequisites. Do not rerun Round177 category/functor corrections, Round179 groupoid scope corrections, or Round180 clopen retargeting. Distinguish a valid broad prerequisite from a mis-typed object; avoid counting numerical canonical-candidate reduction as the goal. Source-free restrictions remain intact and the consolidation gate stays closed pending separate reviewed authorization. The earlier packet-code optimizations were used successfully at the level of exact receipt, but **this is not a claim of full repository CI success, citation verification or human mathematical certification**.
