# Wave 2 Pass 2 — focused mathematical convention adjudication and draft consolidation rationale

**Status: REVIEW PROPOSAL ONLY, source-free, 2026-10-24.** This document makes no source-record, dependency, candidate-identity, ledger, or graph edits; it is **not** an adopted review-ledger disposition, an approval of mathematical source content, a consolidation event, or authorization for Pass 3. The reviewer must separately accept or modify the proposed conventions and record the necessary dispositions before deciding whether to submit a gate package.

## Scope and current immutable anchors

Only the independent Wave 2 dataset at `research_pipeline/experiments/reconstruction-v2-independent/` and permitted Wave 2 audit/engine documents were used. No production mathDef mathematical corpus, frozen Wave 1 data, or external mathematical sources were consulted.

- Current source inventory SHA256: `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`.
- Current unresolved-pool fingerprint: `61246db4cb0897ac3bfdb43f8a8e6be361e2f05bf905367bfbda0b388a541113`.
- Live checkpoint: 611 contextual meanings; 659/659 semantic formulation scans complete; 0 unassigned, ambiguous, or deferred occurrences; 728 raw missing identities, comprising **421 unresolved canonical / 300 alias / 7 resolved**; 844 missing occurrences; 770 scan amendments; 20 historical seed overrides.
- Consolidation gate: **FALSE**; current phase `consolidate_occurrences`; **no `CONSOLIDATION.json`**.
- The read-only readiness review reports **19/19 mechanical checks passing**. This certifies neither correct mathematical definitions nor complete independent contextual review.
- Reviewed lead-by-lead evidence, formulations, and hashes: `WAVE2_CODEX_CONTEXTUAL_CONSOLIDATION_REVIEW.md` (20 cases, PR #7). Source-free engineering evidence: `WAVE2_CODEX_CONSOLIDATION_READINESS.md` (PR #6).

All hashes are checkpoint-specific. If the graph, source inventory, related variants, candidate mapping, or reviewed evidence changes, repeat the readiness assessment and reassess any affected decision before citing these values.

## Decision A — compactness and the finite intersection property (FIP)

**Source formulation:** `form.wave2.broad67.compact-closed-fip`, current formulation version SHA256 `e6a0aa44634543ff92c50272643e6d7a42152bc50827bbbd925d745849f036bb`, effective node SHA256 `101ea433c98c87cacaaa5ed473300ed2484699fa8134b14fc57185df57c6f8d8`.

The current **stored independent source formulation** reads:

> Equivalently, X is compact if every family of closed subsets of X that has the finite intersection property has nonempty total intersection.

The unresolved canonical FIP prerequisite `missing.ded806b239b007c8af8c` has recorded context:

> General set theory/topology: family (F_i) of subsets of X with ⋂_{i∈E}F_i nonempty for every nonempty finite E of indices; specify the empty-family convention separately.

This is not a populated, externally source-verified FIP definition; it is an exact contextual missing-prerequisite record. The separately unresolved closed-subset predicate is `missing.c4ed408b10943e9c0f8e`. The pre-existing compactness seed `rel.wave2.broad68.02` targets `meaning.wave2.foundation.topological-space`, correctly supplying the ambient space; it must **not** be automatically deleted or conflated with the closed-subset predicate.

### Counterexample to the unqualified combination

Take `X = ∅` with its unique topology. It is compact by the finite-open-subcover definition: any open cover, including the empty cover, has a finite subcover. Take the **empty indexed family** of closed subsets. It satisfies `⋂_{i∈E}F_i ≠ ∅` for every **nonempty finite** set of indices `E` vacuously, since there is no such `E`. Yet the full intersection is `⋂_{i∈∅}F_i = X = ∅`. Therefore the displayed closed-set compactness criterion fails if this candidate's nonempty-finite-index convention is used without a separate family-nonemptiness qualification. This is a real logical countermodel, not an inference from lexical matching.

### Recommended convention (preferred, NOT applied)

**Retain** the recorded FIP candidate's nonempty-finite-index convention. **Qualify the compactness criterion to nonempty indexed families** of closed subsets:

> A topological space X is compact if and only if every **nonempty family of closed subsets of X** with the finite intersection property has nonempty intersection.

This proposal preserves the currently intended FIP candidate identity and does not assume `X ≠ ∅` or impose any Hausdorff hypothesis. It removes only the empty-family edge case. It is a **proposed mathematical rewording**, not a newly verified quotation from the stored source.

### Proof of the repaired equivalence for arbitrary X

(**Compact ⇒ criterion.**) Let `(F_i)_{i∈I}` be a **nonempty** indexed family of closed subsets satisfying FIP for all nonempty finite `E ⊆ I`. If its total intersection were empty, the opens `X\F_i` would cover X. Compactness gives a finite subcover. For nonempty X, any finite subcover must have at least one member, contradicting FIP. For empty X, no nonempty family can satisfy this version of FIP, since every singleton `{i}` has `F_i=∅`. Thus the implication holds for empty X as well.

(**Criterion ⇒ compact.**) If X were noncompact, there would exist an open cover `(U_i)_{i∈I}` with no finite subcover. It must be a nonempty indexed cover; otherwise X would be empty and compact. Then `F_i=X\U_i` is a nonempty indexed family of closed sets. Every nonempty finite intersection is nonempty (as the corresponding finite open subfamily does not cover X), but `⋂_{i∈I}F_i=∅`, contradiction. Hence X is compact.

**Alternative, not selected:** Change the FIP convention to quantify over *all* finite index subsets including `E=∅`, with empty finite intersection equal to X; this excludes the vacuous empty-family-on-empty-space counterexample without changing the compactness source wording. However it alters the FIP candidate's current intended convention and can change other contexts. A third alternative is a nonempty-X-only theorem variant, which is unnecessarily restrictive. The above nonempty-family repair is the least disruptive proposal **for the current snapshot**.

**Pass 2 disposition proposed:** Treat the candidate identity `missing.ded806b239b007c8af8c` as distinct and legitimate, but mark the current compactness/FIP source equivalence as requiring the explicit nonempty-family qualification in a **separately authorized source/variant revision**. An explicit documented quarantine pending that revision is defensible for contextual identity consolidation; blanket certification of the present theorem is not. No graph packet or source edit is included in this report.

## Decision B — module and ring unitality scope (proposed deferral policy)

The source-free dossier identifies **seven** open general-versus-unital module convention cases (#2, #4–#9), **two** related commutative ring/ideal cases (#12–#13), and one distinguishable free-resolution case (#3).

### Mathematical non-equivalence must be retained

- A general left module does **not** automatically satisfy `1·m=m` merely because its coefficient ring has an identity. On `R=F₂, M=C₂`, the all-zero scalar action satisfies the general axioms but is nonunital. The existing `meaning.wave2.foundation.left-module-nonunital` and `meaning.wave2.module94.unital-left-module` are distinct legitimate contexts; **never alias** them.
- A nonzero commutative ring with a unique maximal proper ideal need not be unital if ring identities are optional. The additive group `C₂` with zero multiplication is such a nonunital rng. The general two-sided ideal target and the commutative-unital maximal-ideal target are distinct mathematical prerequisites.
- For the free-resolution case #3, where the stored free-module construction is over a unital ring and the augmentation is surjective, unitality of M follows: if `ε:F₀→M` is surjective, `m=ε(x)`, so `1m=ε(1x)=ε(x)=m`. This case has a stronger internal justification than a generic source label.

### Recommended policy (NOT adopted as a source convention)

**Preserve** all currently separate general and specialized target identities and their provenance; no blanket unlinking or merging is justified. Record the nine open cases as a **single shared source-convention family** with separate exact formulation IDs and evidence hashes retained in `WAVE2_CODEX_CONTEXTUAL_CONSOLIDATION_REVIEW.md`.

**Do not assert an unital convention globally from a Stacks-attributed paraphrase or locator alone.** Ordinary mathematical usage may favor unital modules/rings, but that is not sufficient evidence that the current stored text or every source variant establishes the narrower scope.

For subsequent source/variant reconciliation, either (a) obtain source-specific evidence that a unital convention is intended and express it in the relevant formulation/context, or (b) retain the broad formulation and separately classify/prune any unjustified **specialized** target after exact contextual review. General prerequisites can remain valid alongside justified specialized prerequisites. Re-run the version-bound graph audit for any actual edited formulation or target choice.

**Pass 2 disposition proposed:** Document these as unresolved, specifically scoped **source/variant convention deferrals**, not nine automatically mistaken identity merges or automatic gate blockers. Their actual dispositions must be accepted before an unconditional global consolidation claim.

## Decision C — other source/variant issues

These have proposed later-source-reconciliation status, **not** silently accepted repairs:

- **Topological ring/module:** `form.646e4dcbd9b6f1e1.topological-ring` and `form.646e4dcbd9b6f1e1.topological-module` require an explicit unital domain or additive-topological-group/continuous-negation condition to support conventional definitions. In the unital scope, multiplication by `−1` makes negation continuous; without that scope, continuity of addition and multiplication alone is not enough. Preserve both potential variants and independently verify intended sources later.
- **Submersive map:** `form.83a528850cdf6a59.submersive-continuous-map` contains an unqualified “equivalently” phrase. The biconditional `U⊆Y` open iff `f^{-1}(U)` open does not, by itself, imply surjectivity: a nonsurjective injection of a one-point discrete space into a two-point discrete space is a counterexample. Keep the already separate surjectivity and quotient-topology dependencies; consider wording clarification later.
- **Four provisional population source issues:** `issue.wave2.pop140.pairwise-proofwiki-quantifier`, `issue.wave2.pop141.eom-outer-measure-convention`, `issue.wave2.pop142.bounded-quantifier`, and `issue.wave2.pop142.operator-norm-codomain`. Existing independent drafts distinguish `i≠j`, power-set versus broader outer-measure domains, one global boundedness constant, and the target-space norm. Retain source-issue records pending source-backed comparison in a separately authorized phase.
- The other flagged seed/scan differences are reported in the 20-lead dossier as valid general/specialized or construction/property dependencies **for those specific reviewed occurrences**, not as certifications of every source or candidate. No mathematical graph changes are proposed from those comparisons.

## Draft global contextual consolidation rationale — NOT YET CERTIFIED OR SUBMITTED

The following is a **proposed review narrative** rather than a ready-to-submit `consolidate` payload:

> At the independently sourced Wave 2 inventory SHA256 `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492` and unresolved pool fingerprint `61246db4cb0897ac3bfdb43f8a8e6be361e2f05bf905367bfbda0b388a541113`, all 659 stored formulations have complete, version-valid semantic scan dispositions, with no unassigned, ambiguous, or deferred reference states. Effective occurrence and candidate registries consistently replay 300 reviewed alias events, seven version-bound candidate resolutions and 20 historical seed overrides. The 421 unresolved canonical candidates represent classified contextual missing prerequisites, not 421 unclassified references or a mandate to reduce their count to zero. All 20 current high-priority consistency diagnostics received bounded contextual examination; many were justified as distinct general/specialized or construction/property dependencies, while the compactness/FIP empty-family convention and nine shared module/ring-convention readings remain precisely documented for explicit adjudication or later source/variant reconciliation. The six remaining documented source/wording groups (topological algebra, submersive map and four provisional source issues) are not falsely treated as independently verified. This evidence can support a **reviewed source-free identity-consolidation decision** without certifying the complete mathematical correctness, missing-term completeness, source attributions or all external citations. Any pending unresolved contextual ambiguity that might actually change a candidate identity must be adjudicated or explicitly excluded from the assertion before signing.

**Why the gate is still not approved:** The executable gate checks mechanical completeness and demands a substantive *reviewed* rationale, but 19/19 checks, 300 recorded alias events and 20 reviewed detector leads do not, by themselves, prove that all 421 canonical identity classes received exhaustive human contextual assessment. The proposed FIP and unitality dispositions are not source-record changes, accepted review-ledger entries or a signed global exception list. A reviewer still must decide whether the documented scope and acknowledged residual risks suffice for the Pass 2 identity-consolidation claim. This draft should **not** be copied as though that decision has been made.

## Concrete next checkpoint

1. **Mathematical choice:** accept/modify the nonempty-family FIP repair as a scoped mathematical proposal, and decide whether to quarantine the source formulation for subsequent revision or authorize a separate exact, version-bound source change.
2. **Conventions:** adopt a named, reviewed source/variant **deferral policy** for the seven module and two ring/ideal cases, with the free-resolution case recognized separately.
3. **Coverage decision:** review the remaining canonical missing-candidate contexts using existing ranked/exhaustive bundles as needed; log what is actually inspected. Decide what coverage supports a truthful global Pass 2 consolidation rationale, rather than asserting blanket review without evidence.
4. **Only by separate authorization:** if the review standards are met, re-run the latest read-only readiness assessment, confirm the exact current hashes, and prepare a reviewed consolidation packet. Do **not** create `CONSOLIDATION.json`, open the gate, begin Pass 3 research or change live dataset files as part of this document.

This is a durable read-only mathematical proposal. All identity, scope and gate choices remain subject to human/chat review and later version-valid implementation.