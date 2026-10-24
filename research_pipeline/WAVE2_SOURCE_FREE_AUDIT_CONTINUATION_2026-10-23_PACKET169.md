# Wave2 source-free audit continuation — packet 169 and constructible-set scope (October 23, 2026)

## Verified application

Packet `semantic-global-audit-missing-alias-169` was committed to the **independent Wave2** dependency-graph inbox and its exact receipt confirms `status=applied_in_independent_graph_only`, `mode=alias`, `human_certified=false`, SHA256 `e9e4923c87e4715760e42ed3aaa44e2e75b6179c36337810faa89d3407e9611e`. [Wave2 graph Action 40047415206](https://github.com/Zengez/mathDef/actions/runs/40047415206) and [isolated research tests 40047415193](https://github.com/Zengez/mathDef/actions/runs/40047415193) both completed SUCCESS.

| Measure | Before | Verified after |
|---|---:|---:|
| Meanings | 611 | **611** |
| Scanned independent formulation texts | 659/659 | **659/659** (639 screened, 20 provisional) |
| Raw missing candidate identities | 724 | **724** |
| Context-reviewed alias records | 287 | **292** |
| Candidate resolutions to existing meanings | 7 | **7** |
| Unresolved canonical candidate identities | 430 | **425** |
| Unresolved missing occurrence rows | 819 | **819** |
| Append-only effective amendment events | 765 | **765** |
| Unassigned / ambiguous occurrence rows | 0 / 0 | **0 / 0** |
| Open / closed formulation nodes | 651 / 8 | **651 / 8** |
| Consolidation gate | false | **false** |

Authoritative inventory SHA256 `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`, new unresolved fingerprint `88f331d798795a542c3f2eab5dcec0d5e75630e4a56329cadf4cab8e9e121cc7`. The 819 missing *occurrences* are unchanged: candidate identity aliases are not new independent meaning definitions.

## Reviewed source-context prerequisite aliases

All five decisions were reviewed against their full parent mathematical formulation texts; source-specific additional conditions are not merged. The immutable packet is the exact audit record.

1. `missing.e9f8615c8ccefe3f5110` → `missing.ab1dee70553ea0ff2c1c`: the commuting cone `P→X,P→Y` above a cospan `X→S←Y` is an instance of a generic compatible **cone** to an indexing diagram. Pullback universality and scheme-specific conditions remain **additional** parent constraints, not consequences of an arbitrary cone.
2. `missing.d6860fab14d78960a770` → `missing.ddc9befb080e8d7146db`: a filtered diagram's compatible maps `M_i→X` are a **cocone** to that diagram. A cocone is neither automatically a colimit nor proof that the diagram is essentially constant; the special hypotheses remain in the parents.
3. `missing.82c525cf52c351433b8a` → `missing.b05a1814a9da0d01922a`: local homomorphisms of local rings, whether used in a Noetherian Tor criterion or on stalks of morphisms of locally ringed spaces, share the condition `f^{-1}(m_S)=m_R`. The Noetherian, stalk and flatness hypotheses are not inherited by a generic local homomorphism.
4. `missing.d4d437b437b24a44b5cc` → `missing.b86257b3cce62907e97e`: `φ^{-1}({0_N})` is a **set-theoretic preimage** of a singleton under the underlying module map `φ`. Its additional submodule/kernel interpretation depends on `R`-linearity, as stated in the parent formulation. Generic inverse image does not require invertibility.
5. `missing.68e74334168781726bb9` → `missing.de1b7a5e3717e67b42a7`: reverse Hom maps `f↦f∘u_{ij}` induced by R-module transition morphisms are instances of ordinary categorical **precomposition**. Inverse-system coherence and Mittag-Leffler image stabilization remain separate source requirements.

No formulation content, source evidence, public production definition, or frozen Wave1 data was changed.

## New high-impact mathematical review lead: constructible subsets of a non-Noetherian affine spectrum

The screened independent source `form.c766a18ce285a2d8.constructible-subset-affine-spectrum` states:

> A subset C of Spec(R) is constructible if and only if it is a finite union of subsets D(f)∩V(g_1,…,g_m), with f and each g_i drawn from R.

This is **not equivalent to the unrestricted finite-union-of-locally-closed-subsets convention** for arbitrary non-Noetherian R. It describes a narrower finite-data/patch-constructible class unless additional conventions or hypotheses are in force.

**Source-free mathematical counterexample under the broad locally-closed convention.** Let `R=k[x_1,x_2,…]` be the polynomial ring in countably infinitely many independent variables over a field `k`, and `m=(x_1,x_2,…)`. Then `V(m)={m}` is closed and hence locally closed, therefore constructible under the finite-union-of-locally-closed-sets convention.

Suppose `{m}` were a finite union of `D(f_j)∩V(g_{j1},…,g_{jr_j})`. Some constituent must contain `m`, so for that constituent `f_j∉m` and every `g_{jt}∈m`. Choose `N` so all these finitely many polynomials use only `x_1,…,x_N`. The smaller prime ideal `p=(x_1,…,x_N)` then contains every `g_{jt}` while not containing `f_j` (because `f_j` has nonzero constant term). Thus `p∈D(f_j)∩V(g_{j1},…,g_{jr_j})` but `p≠m`, contradiction. No such representation exists.

**Disposition:** record **definition/convention/scope mismatch** and require manual comparison with the independent cited-source terminology during the later authorized source/citation phase. Do NOT declare the cited source incorrect or overwrite the screened source. This example distinguishes (a) constructible in the broad locally-closed sense and (b) patch/finite Boolean combination of principal-open conditions; they can coincide in a Noetherian setting but need not in an arbitrary ring. The separate screened `form.049afb81432d58ef.constructible-subset-noetherian` explicitly assumes a Noetherian space, where finite-type presentations are less problematic.

**Review limit:** An initial *textual* sweep inspected formulation statements containing `equivalently`, `if and only if`, `precisely when`, or `exactly when` for possible scope issues. This is not a claim that all such equivalences were mathematically certified. No external references or original mathDef production definitions were accessed.

## Additional guarded non-merges retained

Targeted source-context checking also preserved these distinctions; similarity scores or shared notation must never force a merge:

- A diagram cone versus a **universal** limit cone; a commuting cospan cone versus a **universal** pullback.
- A cocone versus a **universal** colimit; a filtered cocone versus an **essentially constant** ind-object.
- Precomposition as a generic Hom operation versus the whole Mittag-Leffler inverse-system condition.
- Set-theoretic preimage `φ^{-1}({0})` versus the **module kernel** as a submodule with its linear structure.
- A graded ring element's homogeneous **component** versus a graded module's homogeneous degree **subgroup** and versus the whole graded direct-sum decomposition.
- Categorical coimage `Coim(f)` versus its canonical map to `Im(f)`; even when the comparison is an isomorphism in an abelian category these are different structural references.
- A section `s:X→Y` satisfying `r∘s=id_X` versus its retraction `r:Y→X`—paired data with opposite directions, not interchangeable names.
- A direct sum `⊕_i M_i` versus the unrestricted module direct product `∏_i M_i`; finite-support and arbitrary-support families differ for infinite indexing sets.

Prior precise non-merges from packet 168 remain in `WAVE2_SOURCE_FREE_AUDIT_CONTINUATION_2026-10-23_PACKET168.md`.

## Remaining mathematical risk and next actions

Three effective `small-groupoid` links potentially impose unintended size restrictions: `form.74cd6dc48e0606fc.setoid-category` (ref0), `form.0bf601085c1029d4.two-one-category` (ref2), `form.5e4b8f6efeda6522.category-fibred-in-groupoids` (ref3). There is still **no approved size-unrestricted groupoid meaning/candidate** that preserves the invertibility prerequisite while avoiding the extra size condition; do not replace any with plain `category` or invent a reviewed meaning in this phase. The independently logged quasi-finite/local-fibre isolation and submersive/surjectivity counterexamples, and perfect-closure characteristic-zero variant, also remain open and untouched.

Next review: prioritize mathematically consequential false-target scope and source-definition consistency before further cosmetic aliasing; if additional review has sharply diminishing returns, prepare the explicit source-free consolidation readiness evaluation rather than alias identities simply to drive 425 toward zero. **Do not** seal/open the consolidation gate, conduct missing-definition external research, resume breadth Batch143, alter screened/provisional source mathematics, edit production or frozen Wave1, claim source/citation certification, or freeze.
