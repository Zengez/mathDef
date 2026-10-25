# Wave 2 Pass 2 — source-free unitality adjudication and scoped convention deferrals

**Review date:** 2026-10-24 (America/New_York).  
**Review authority:** mathematical reasoning in ChatGPT, based on already recorded independent Wave 2 source formulations, the exhaustive 20-lead contextual review, the Pass 2 convention proposal, and the current graph. **Not** an independent external-source verification, an expert human refereeing certificate, a graph review-ledger event, or authorization for Pass 3.

**Disposition:** Adopt the *review policy* below as the working Pass 2 classification for these exact findings. The nine unresolved source-convention readings remain open for later source-specific checking. No graph reference is automatically reclassified as a graph `deferred` occurrence; the documentation-level **source/variant deferral** is deliberately distinct from the graph's reference-state enumeration. No mathematical source or graph record is edited by this review.

## Current scope and digest contract

After the authorized FIP source correction merged in PR #9:

- Active independent Wave 2 inventory `34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113`.
- Active unresolved-occurrence fingerprint `eb9beb4199a99b1dc3fc18b57daa1f1d4cc9c66051caa558acb7a48396242cee`.
- 611 meanings; 659/659 complete formulation scans; 421 unresolved canonical missing candidate identities; 300 reviewed aliases; seven resolved candidate identities; 844 missing occurrences; 770 historical scan amendments; zero ambiguous or unassigned reference states; global consolidation gate FALSE.

The individual nine non-FIP formulations were not changed by PR #9, but any future assessment must check their **current** version and effective-node hashes, not assume an old report hash remains valid indefinitely. The historical detailed case records and source/version/occurrence evidence are in `WAVE2_CODEX_CONTEXTUAL_CONSOLIDATION_REVIEW.md` §3, #2–9 and #12–13. The FIP issue #1 is **resolved**, not to be reported as an active blocker.

## Mathematical policy approved for continued Chat review

1. **Structure identity is not source convention.** Keep `meaning.wave2.foundation.left-module-nonunital` distinct from `meaning.wave2.module94.unital-left-module`; keep the identity-optional associative ring meaning distinct from the commutative-unital ring notion; and keep generic two-sided ideals distinct from maximal proper ideals of commutative unital rings. Do not form aliases between general and strictly stronger specialized meanings.
2. **An ordinary-source label is insufficient to infer an axiom.** Even if a cited author conventionally works with unital rings/modules, source attributions to a text or existing editor matching notes are not external proof of its ambient conventions. A ring with identity does not force all modules over that ring to be unital.
3. **Do not prematurely delete general links.** A valid general/foundational dependency may coexist with a valid specialized dependency under a **confirmed** specialized context. Duplicate navigation/expansion is a separate UI concern, not automatically a mathematical error.
4. **Do not certify unsupported specialized links.** The currently stored bare formulations sometimes also permit a nonunital reading. Until a source-specific convention is established, treat their *source scope* as unsettled; never report these conditional specialized links as unconditionally verified against the literal broad wording.
5. **Source/variant deferral is documented by finding.** Each pending question remains an exact source-formulation review obligation; it does not merge missing candidate identities, alter an effective graph state to `deferred`, or satisfy every canonical missing candidate's contextual identity review. Actual source edits require a new, narrowly authorized, version-safe migration and review.

## Separating models and case decisions

**General-module counterexample.** Let `R=F₂` and let `M=C₂` (additive group of order 2). Define `r·m=0` for all `r,m`. This is a left R-module under the identity-optional action axioms (associative scalar action and two distributive laws); it does not satisfy `1·m=m` for nonzero `m`. It has precisely the submodules 0 and M. The identity additive endomorphism of M is R-linear and its scalar action in Hom is zero. Consequently mere R-linearity, simplicity, a strict submodule chain, and annihilator constructions do **not** recover the unit axiom.

**Nonunital commutative-ring counterexample.** Take the additive group `C₂` with identically zero multiplication. It is nonzero and has two (two-sided) ideals, 0 and R; hence 0 is a unique maximal proper ideal, but R has no multiplicative identity. Thus “commutative,” “maximal ideal,” and “unique maximal ideal” do not imply a unital ring.

| Historical lead | Formulation ID | Mathematical disposition at current text | Remaining source decision |
| --- | --- | --- | --- |
| #2 Internal Hom | `form.3a0545450d7a5285.internal-hom-module` | General/unital module targets are **distinct**. Under unital M,N, the Hom action is unital; zero-action modules show the bare formula does not force this. Retain current references pending source validation. | Does the intended module convention include `1m=m` for M,N? |
| #4 Relative R-derivation | `form.7ca4fb934b2f076c.r-derivation` | With zero-action nonunital coefficient M, the zero derivation still satisfies the stated equation; unital ring maps do not force unital modules. | Explicit coefficient-module convention |
| #5 Finite-order differential operator | `form.a81a0fbec29f2186.finite-order-differential-operator` | Zero-action modules admit nonzero additive S-linear maps of order 0; the existing resolved R-linear map meaning is independently legitimate under scalar restriction. Preserve the distinction between order-zero S-linearity and positive-order R-linearity. | Explicit S-module convention |
| #6 Module composition length | `form.a95feee56dc057ee.module-composition-length` | Submodule-chain length makes mathematical sense without `1m=m`. For the zero-action C₂ example the length is 1. Do not replace chain length by number of generators or an unstated composition series. | Ambient module convention |
| #7 Simple module | `form.a95feee56dc057ee.simple-module` | A nonzero zero-action C₂ module is simple by the displayed proper-submodule condition but is not unital. Nonzero requirement remains essential. | Ambient module convention |
| #8 Annihilator of a module | `form.a9ca2e716ceffd36.annihilator-module` | For a general left module, Ann(M) is a two-sided ideal by associativity of scalar action; the annihilator may be all R. Do not silently require a proper ideal. | Ambient module convention |
| #9 M-regular sequence | `form.f17ea18ebee0660f.module-regular-sequence` | Special nuance: **if R has a unit and the sequence is nonempty**, injectivity of its first element forces `m=1m` for every m. But `r=0` is not excluded in the stored text, and a nonunital ring such as 2ℤ acting on ℤ admits the regular one-element sequence (2) with final quotient ℤ/2ℤ ≠ 0. | Ring identity, positivity/emptiness of sequence length, convention for regularity |
| #12 Jacobson radical | `form.90b0d1ecfa394230.jacobson-radical-ring` | Generic two-sided ideals are prerequisites to maximal ideals; the source's bare “commutative ring” and identity-optional ring link do not logically ensure that the specialized **commutative-unital** maximal ideal target is universal. This is not a reason to merge the target meanings. | Explicit ring identity convention; possible rng variant remains distinct |
| #13 Local ring | `form.4f7edb6d32334f67.local-ring-unique-maximal` | The nonzero zero-product C₂ rng has a unique maximal proper ideal without a unit. Source wording “nonzero commutative ring with exactly one maximal ideal” does not alone imply unitality. The ordinary equivalent “nonunits form an ideal” needs separate unital-context attention. | Unital local ring convention and equivalence scope |

**Separate justified case #3** — `form.788671763be693df.free-module-resolution`. Its recorded free modules are free over a unital R; exactness of the augmented complex makes ε:F₀→M surjective, and ε is R-linear. For any m=ε(x), `1·m=ε(1·x)=ε(x)=m`. Therefore unitality of M follows under this recorded construction, independent of a general unstated convention. Both general and unital links can remain. No module-source deferral is needed **for that edge under that exact free-module convention**; the candidate `missing.7462fa5f90275b34779a` still requires future substantive source-supported population.

**Special case #9 proof detail.** If R has identity 1 and r≥1, injectivity of multiplication by f₁ on M gives `f₁(m−1m)=f₁m−(f₁1)m=0`, so `m=1m`. An empty sequence (`r=0`), if allowed, imposes no first-element injectivity and its nonzero final quotient only means M ≠ 0; do not use the same inference there. For nonunital R this proof has no 1_R. The 2ℤ/ℤ example separates the scopes.

## Neighboring unresolved source/variant issues (outside the nine)

- `form.646e4dcbd9b6f1e1.topological-ring` and `form.646e4dcbd9b6f1e1.topological-module`: continuity of addition and multiplication alone does not ensure additive inverse continuity in general identity-optional topology; a correct ordinary topological ring/module formulation may need additive topological-group structure, or explicitly justified unital hypotheses. Preserve the two alternatives for future source verification.
- `form.83a528850cdf6a59.submersive-continuous-map`: the preimage-open biconditional **does not itself imply surjectivity**, while the first clause separately states surjectivity. Later source edit should say “equivalently, f is surjective **and** ...”, provided checked against the intended source. Keep the surjectivity and quotient-topology missing candidate identities distinct.
- Four recorded provisional issues remain source/variant checks: `issue.wave2.pop140.pairwise-proofwiki-quantifier`, `issue.wave2.pop141.eom-outer-measure-convention`, `issue.wave2.pop142.bounded-quantifier`, `issue.wave2.pop142.operator-norm-codomain`. The current drafts already distinguish relevant predicates; source authority and variant questions are not resolved by this mathematical reading.

## Scope of completed review, and what this document does NOT establish

This document supplies explicit Chat mathematical dispositions for exactly nine shared convention cases and the distinguishing free-resolution argument. It **does not** claim nine new machine-recorded identities, external verified source conventions, 421 reviewed missing candidates, a new alias, a completed graph audit, or final Pass 2 consolidation approval. The purpose is to prevent the next audit from reopening the same mathematical equivalence question when the unresolved issue is actually citation/domain scope.

**Decision threshold before any consolidation gate:** (a) ensure current form/node hashes remain version-valid, (b) record the actual coverage of the canonical candidate identity audit, (c) classify still-open source/variant concerns as bounded exceptions with a future reconciliation plan, (d) recompute the complete readiness report with current hashes, and (e) submit any global consolidation rationale only when its claimed review coverage has really occurred.

Next handoff: `research_pipeline/WAVE2_CODEX_CANONICAL_IDENTITY_AUDIT_TASK_2026-10-24.md`. That task is intentionally bounded and source-free. All data and gate restrictions remain in force.
