# Wave2 source-free audit continuation — packet 170 and contextual identity-split review (October 23, 2026)

## Applied packet and exact verification

**Packet**: `semantic-global-audit-missing-alias-170`, commit `8981e6b28a8aa40c8fbb4f768e8ea52e20b9e32b`. The independent graph dispatcher emitted exact receipt `status=applied_in_independent_graph_only`, `mode=alias`, `human_certified=false`, SHA256 `e9e3853ebecf9ad8fbb7ed03b8536b1f27f8098f7feb97c17a7cb3fb62204b51`. [Graph CI run 40049966896](https://github.com/Zengez/mathDef/actions/runs/40049966896) and [isolated research-pipeline tests 40049966906](https://github.com/Zengez/mathDef/actions/runs/40049966906) both passed.

| Metric | Packet 169 | Verified packet 170 |
|---|---:|---:|
| Existing meanings | 611 | **611** |
| Scanned formulations | 659/659 | **659/659** (639 screened + 20 provisional) |
| Raw stored missing candidate IDs | 724 | **724** |
| Accepted prerequisite alias records | 292 | **294** |
| Candidate-to-existing-meaning resolutions | 7 | **7** |
| Outstanding canonical missing identities | 425 | **423** |
| Unresolved missing occurrence rows | 819 | **819** |
| Effective amendment events | 765 | **765** |
| Unassigned / ambiguous occurrences | 0 / 0 | **0 / 0** |
| Graph structurally open / closed | 651 / 8 | **651 / 8** |
| Consolidation gate | false | **false** |

The graph retains source inventory SHA256 `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492` and new unresolved fingerprint `aeb62c80b7cf0f95c9d944309bc4888acd97daa2c58e148bf2ffdb13b06642a7`. Missing **identity** count is not the number of missing definitions or unresolved occurrences. The 819 rows remain non-certified.

### Source-context alias decisions

1. `missing.0b84d58d6738b7667a3d` (“isomorphic to” as locally ringed spaces) → `missing.15bb96cb26d587868bbe` (invertible **categorical** morphism). Sources: `form.4c7d59ba7058613b.affine-scheme`, `form.bdc3e54fd4523fad.scheme-local-affine`, and generic category-isomorphism use in `form.e3f74861fea6f59a.category-localization`, `form.wave2.foundation.small-groupoid`, and `form.wave2.foundation15.abelian-category`. In the category of locally ringed spaces the specified isomorphism is exactly a morphism admitting an inverse *as a locally ringed-space morphism*, not merely a bijective set map or a homeomorphism. Ambient morphism type and the scheme-specific structure remain specified in the full parent sources.
2. `missing.2940257ef7ae0b2135c7` (weighted integral polynomial orthogonality) → `missing.2e90e090541bb3b84623` (orthogonality with respect to a nonnegative measure). Sources: `form.wave2.analysis.orthogonal-polynomials-interval` and `form.wave2.analysis.orthogonal-polynomials-measure`. The weight `w(x)dx` defines a nonnegative measure `μ_w`, and `∫p_np_m w dx=∫p_np_m dμ_w`; both prerequisites are precisely the vanishing of mixed integrals for distinct indices. The measure-based abstraction does **not** claim that every measure has a density, nor erase source-specific moment, support or positivity assumptions.

## High-priority, source-proven context collision — **do NOT alias further**

Shared candidate `missing.fbe845b2e6ab78c9890f` is named **“intersection of all closed supersets of A”** and its explanatory context specifies a family of topologically *closed* sets containing A, equating the intersection with topological closure `cl_X(A)`. Its registry lists **three** incoming formulations, but those parents quantify over different families:

1. **Topological closure** `form.wave2.cross107.topological-closure.1`: intersection of all **topologically closed** supersets of `A`. The candidate's current wording fits this occurrence.
2. **Convex hull** `form.wave2.cross133.convex-hull-real.2`: intersection of all **convex** supersets of `U`. This is not an intersection of all *topologically closed* supersets of U.
3. **Affine hull** `form.wave2.pop140.affine-hull-intersection`: intersection of all **affine-closed (stable under finite affine combinations)** supersets of `S`. The property `affine-closed` does **not** simply mean closed in a topology.

**Concrete counterexample:** in `ℝ` with its usual topology, take `A={0,1}`. The intersection of all topologically closed supersets of `A` is `{0,1}`; the intersection of all convex supersets is `[0,1]`; the intersection of all affine-closed supersets is `ℝ`. A displayed prerequisite with the label “intersection of all closed supersets” therefore teaches a mathematically incorrect construction if used to explain either convex hull or affine hull.

**Recommended scoped repair, not yet applied:** use the effective-node **version-anchored** amendment path to split the two affected non-topological occurrences from the topological closure candidate, or deliberately replace all three by a truly general set-theoretic **intersection over a parameterized family** prerequisite while retaining the different family-defining predicates as context-specific links. Review exact effective occurrence IDs, complete current node snapshots, immutable candidate registrations, and preflight before any submitted `amend` packet. Reuse the proper `--candidate-id`/`focus` worklist and `dependency_global_audit prepare`; do not edit base node JSON, amend historic source descriptions, mutate the registry ad hoc, or merge these three hull/closure operations themselves. **The current shared identity is not proof that the three hull/closure notions are equivalent.**

This finding also establishes a general audit rule: a candidate can correctly represent a generic operation (arbitrary intersection) while its *label* and *context* make an invalid special assertion. Check **candidate explanations against every incoming source context**, not only parent-pair semantic similarity.

## Groupoid-size review: three previously flagged uses are not equally severe

Existing definition `form.wave2.foundation.small-groupoid`: `G` is explicitly a **small category** and all arrows invertible. Therefore an effective target to this meaning asserts a size restriction in addition to groupoid invertibility.

- `form.74cd6dc48e0606fc.setoid-category`: “A setoid is a groupoid C in which every object has only its identity automorphism”. If `setoid` is understood as an equivalence relation on an underlying **set**, smallness can be implicit and the target may be justified; if source-category conventions allow proper-class objects, smallness is unjustified. **Conditional** scope lead, not a verified error.
- `form.0bf601085c1029d4.two-one-category`: each **hom-category** is a groupoid because all 2-arrows invert under vertical composition. Whether those hom-categories are small depends on strict 2-category size conventions; the statement itself does not impose it. **Scope remains unproved.**
- `form.5e4b8f6efeda6522.category-fibred-in-groupoids`: source lifting and unique-lift conditions imply fibres are groupoids without directly requiring their object collections to be sets. Stronger **size-caveat review lead**, but still needs the ambient universe convention checked.
- Explicit functors into `Groupoids` (e.g. `form.f0d993a60533fc99.groupoid-valued-presheaf`) use a category of small groupoids under common conventions and should **not** be blindly flagged along with the previous three.

There is no approved unrestricted-groupoid target retaining both category axioms and arrow invertibility without asserting smallness. Replacing an arbitrary groupoid with an arbitrary **category** would incorrectly lose the defining invertibility condition. All three current effective references remain untouched.

## Further formulation/variant consistency checks (read-only)

Enumerated **42 contextual meanings having multiple formulations** (90 formulation texts total) in the independent 611-meaning population and inspected their displayed mathematical statements. Most inspected pairs express legitimate equivalent definitions; this was a **targeted review**, not a claim of proof/citation certification for all ninety statements.

- **Connectedness**: `form.ab260940ea9c523d.connected-topological-space` explicitly begins “A **nonempty** topological space X...”, while independent versions `form.wave2.variant71.connected.01/.02/.03` and `form.wave2.pop141.connected-no-separation/.connected-clopen` do not require nonemptiness. The empty space satisfies the no-separation/clopen/no-surjection criteria vacuously. These formulations need **explicit convention alignment and variant labeling**, not an assertion that the cited nonempty-scoped source is incorrect.
- **Quasi-finiteness/local fibre dimension**: previous notes supplied `Spec(k[t])` at generic prime `(0)` as a counterexample if “local fibre has dimension zero” means the **Krull dimension of the fibre local ring** `k(t)`, which is indeed zero although the point is not isolated. But another possible meaning of local topological dimension is **infimum of dimensions of open neighbourhoods** of the fibre point, which for that generic point is one. The earlier counterexample is rigorous only for the *local-ring dimension* interpretation. The phrase in `form.3718becace9c852d.quasifinite-at-prime` must be disambiguated against `form.3fcd082413a6b2eb.relative-dimension-at-prime`; do not misclassify the narrower topological-dimension interpretation as disproved.
- **Submersive map** `form.83a528850cdf6a59.submersive-continuous-map`: its converse “`U⊆Y` open iff `f^{-1}(U)` open” requires the **surjectivity assumption** carried forward from the first clause. Without that assumption the inclusion of a one-point discrete space into a two-point discrete space satisfies the open-preimage equivalence but is not a surjection.
- **Constructible affine subsets**: retain the non-Noetherian constructibility **convention** counterexample and exact scope detailed in packet 169, without overwriting the screened formulation.
- **Perfect closure**: `form.f77b42c1adb38c56.perfect-closure` is explicitly characteristic `p>0`; a context-zero convention/variant is outstanding and not an error in that scoped source.

## Work boundaries and next steps

No external citation/source lookup, no original production mathDef access, no frozen Wave1 edits, no screened/provisional population edits, no new meaning/variant addition, no breadth Batch143, no mathematical/human certification, and no consolidation gate opening/freeze took place.

**Next focus:** fix the source-proven `missing.fbe845...` contextual cross-contamination via complete **effective** per-node snapshots and version-anchored amendment preflight, **if safely obtainable**; otherwise leave a reproducible blocker. Continue scope-sensitive review of high-fan-in prerequisites and the three groupoid references. Stop synonym-count chasing and preserve all prior justified non-merges. The live `dependency_graph/STATE.json`, `CHECKPOINT.json`, immutable packet receipt and this report are the continuation authority.
