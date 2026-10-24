# Independent Wave2 source-free audit — packet 168 and scope counterexamples (2026-10-23)

**Verification:** Eight reviewer-authored prerequisite identity decisions committed in `semantic-global-audit-missing-alias-168`, independently applied with exact receipt (`status=applied_in_independent_graph_only`, `human_certified=false`). Both [dependency graph action 40043325640](https://github.com/Zengez/mathDef/actions/runs/40043325640) and [isolated research tests 40043325752](https://github.com/Zengez/mathDef/actions/runs/40043325752) completed SUCCESS. This is an audit of the *independent* Wave2 graph, not mathematical/citation certification.

## Verified live graph after application

| Metric | After 167 | After 168 |
|---|---:|---:|
| Independent meanings | 611 | **611** |
| Complete formulation scans | 659/659 | **659/659** |
| Raw missing candidates | 724 | **724** |
| Reviewed alias records | 279 | **287** |
| Version-bound resolved-to-existing records | 7 | **7** |
| Unresolved canonical candidate identities | 438 | **430** |
| Unresolved missing occurrence rows | 819 | **819** |
| Effective amendment ledger events | 765 | **765** |
| Unassigned / ambiguous occurrences | 0 / 0 | **0 / 0** |
| Open / closed formulation nodes | 651 / 8 | **651 / 8** |
| Consolidation gate | false | **false** |

Original source inventory SHA256: `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`. Unresolved candidate fingerprint: `9b1fee506b827111b238d86e7598d4b2063ca92325d603336c122016efef38c7`. Exact packet receipt SHA256: `595ca2941787583821be726e7f092dc83633d7fd83b7944e757b460d47f2da4`. Four of the inspected original parent formulations are provisional; **no** screened/provisional source text was changed.

## Eight version-independent prerequisite identity decisions

The full, mathematically contextualized reasons and immutable identifiers are stored in the inbox packet and exact applied receipt. All incoming parent formulations and existing/specialized dependencies were reviewed, including relevant provisional source texts; this is *not* an automatic lexical decision.

1. `missing.137c56b4f420dfc55ef9` -> `missing.a60aa43eed2b99b5d184`: zero object as endpoint of short exact sequences = a category's zero object (initial and terminal); sequence exactness is not inherited by a zero object.
2. `missing.37b0713211a5069fde53` -> `missing.de1b7a5e3717e67b42a7`: representable-presheaf Hom contravariance and scheme functor-of-points contravariance use the *same precomposition operation*, though the corresponding categories and presheaf conditions remain distinct.
3. `missing.72d70ff235732c7f0318` -> `missing.afee26ad5b8d0d34952a`: both proper vertex k-coloring parent statements explicitly have the same codomain palette `{1,…,k}`, k>=1; no surjectivity was added.
4. `missing.165ffe7c25768d23c1ab` -> `missing.cf55f62008d08ce2df84`: isomorphism of schemes over `Spec(A)` and over `Spec(R)` share the same *over-the-base* isomorphism prerequisite; fibre-product and closed-immersion constructions stay separate.
5. `missing.162c8a146060e41fc577` -> `missing.63acc9193a56ae7003b9`: two affine-hull formulations use the same finite affine-combination operation with real coefficients summing to 1. Neither imposes convex-combination positivity; `aff(∅)=∅` is preserved in the provisional parent formulation.
6. `missing.327c59bce72768b1faac` -> `missing.65d334caa51c845ea335`: the martingale and adapted-process source use a real-time `(F_t)_{t>=0}` increasing filtration, distinct from an `(F_n)` indexed by nonnegative integers.
7. `missing.a3e41c65d6b3f8114fb7` -> `missing.fa5932b42daa1a3e0307`: a root of a polynomial over `K` is the extension-field root condition `f(α)=0` with extension `K/K`, distinct from a root of unity or radical extension.
8. `missing.85d3921d2aa075f7883a` -> `missing.c84405a9f915b0897178`: two missing-candidate descriptions within *the same* provisional matrix-trace formulation denote the same `n×n` square matrix over field `K`, with `n>=1`.

These reduce *identity classes* from 438 to 430. The 819 unresolved occurrence rows remain, because aliases consolidate candidate identities; they do not supply the still-absent independent definition meanings.

## High-impact mathematical/source-text issues — precise read-only audit

### Quasi-finite at a prime: isolated vs dimension-zero local fibre

Current independent screened text for `form.3718becace9c852d.quasifinite-at-prime` states that the point `q` is isolated in the fibre `Spec(S⊗_R κ(p))`, **equivalently** the local fibre has dimension zero. This equivalence is too broad as written.

Counterexample: take a field `k`, `R=k`, `S=k[t]`, `p=(0)` in `Spec(k)`, and `q=(0)` the generic point of `Spec(k[t])`. The fibre is `Spec(k[t])`; its local ring at `q` is `k(t)`, a field, hence of Krull dimension zero. But `q` is not an isolated point of the fibre: the singleton generic point is not open. The finite-type map `k→k[t]` is not quasi-finite at this point. A future mathematical-source revision must determine the precise equivalent criterion using the cited Stacks context rather than silently removing the isolation condition or modifying the immutable screened text during this audit.

### Submersive map: quotient-topology condition alone does not force surjectivity

Current independent screened text for `form.83a528850cdf6a59.submersive-continuous-map` correctly includes **surjectivity** in its first characterization but then writes an `equivalently` clause consisting only of `U⊆Y` open iff `f^{-1}(U)` open in `X`. That condition, alone, does not imply surjectivity.

Counterexample: take discrete spaces `X={a}` and `Y={a,b}` with inclusion `f:X→Y`. Every subset of `Y` is open; the preimage of every subset is open in `X`, so the biconditional holds for every `U⊆Y`. Yet `f` is not surjective, hence is not submersive under the first characterization. Future corrected wording should keep surjectivity explicitly in *both* equivalent formulations or retain it as a standing hypothesis.

### Perfect closure in characteristic zero

`form.f77b42c1adb38c56.perfect-closure` defines perfect closure for positive-characteristic fields, a **valid scoped variant**, not a false statement. A complete cross-context meaning should also explain the characteristic-zero convention `k^{perf}=k`, since all characteristic-zero fields are perfect (consistent with `form.f77b42c1adb38c56.perfect-field`). Leave screened source wording and provenance unchanged pending the separately approved variant workflow.

### Three effective groupoid size assumptions remain unresolved

`meaning.wave2.foundation.small-groupoid` defines a **small category** with every arrow invertible. Current effective source references map the following phrases to this *small* meaning despite no explicit size restriction in their full parent formulations:

- `form.74cd6dc48e0606fc.setoid-category` (reference 0, `groupoid C`).
- `form.0bf601085c1029d4.two-one-category` (reference 2, `groupoid` in hom-categories).
- `form.5e4b8f6efeda6522.category-fibred-in-groupoids` (reference 3, `groupoids`).

These are scope review leads, not a proven mismatch under every permissible set-theoretic universe convention. An unrestricted-groupoid prerequisite must retain categorical structure **and invertibility**, without adding smallness; replacing the reference with ordinary category alone would be mathematically unsafe. No reviewed unrestricted-groupoid missing-candidate identity currently exists in the 724-entry registry. This round makes no reference-target or source change here. Never make assertions from immutable base node snapshots without replaying the current effective amendment ledger.

## Review disposition and next steps

The source-free phase has no outstanding *classification* backlog; its remaining 430 unresolved identities are not a mandate to create 430 aliases. The high-impact checks above now have explicit counterexamples (where applicable), mathematical scope distinctions, and relevant formulation IDs. Future work should first identify a safe size-unrestricted groupoid concept within the authorized source-free review protocol; audit genuinely mistargeted dependencies, then do stratified source/variant review and prepare a **separate gate decision**. Any correction of historical source formulations, new meaning population, external source verification, or source-free consolidation requires its separate workflow and authorization.

**Boundaries unchanged:** no external missing-definition research, no Batch143 breadth intake, no production mathDef edits, no frozen Wave1 edits, no human or citation certification, no consolidation-gate opening and no freeze.
