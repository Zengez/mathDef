# Phase 2 consolidation decision — substantive review proposal (NOT APPLIED)

**Date:** 2026-10-26  
**Status:** REVIEW-READY RECOMMENDATION, not an approved `consolidate` event or authorization to begin Pass 3.  
**Repository/branch:** `Zengez/mathDef`, `review/wave2-phase2-remaining-source-issues-2026-10-26` (draft PR #17).  
**Boundary:** independent `research_pipeline/experiments/reconstruction-v2-independent/` only. No production definitions, frozen Wave 1 or external research into missing definitions used. This record adds no candidate identity, mathematical source revision, alias, review override, graph transaction, or gate.

## 1. Decision proposed

**Recommend a *scoped* completion of source-free occurrence classification, followed by a separately authorized and fingerprint-guarded Pass 2 `consolidate` event.** The 418 unresolved canonical identities are a typed research *queue*, not 418 established new meanings, not certification of mathematical correctness, and not a requirement to continue low-yield synonym sweeps. The 841 occurrence records remain traceable to their respective parent formulations. Do not merge them with narrower meanings merely to lower the missing count.

This recommendation **does not approve** the source claims, publication eligibility, release holds, or future graph mutations enumerated below. Individual source defects may be isolated to their formulations and resolved by the source-revision process before release; the gate, if separately approved, states *classification readiness* only.

The proposal is conditional on a final authorization review of this rationale and the exact current graph state, including the source/alias history and 40-case contextual evidence. It does not claim an independent mathematical review of each of the 418 candidates or that the existing 19 mechanical checks prove such a review. If the responsible reviewer interprets the execution contract's "review every group and its originating formulation" as still unmet for any specific group, document those concrete exceptions and defer the gate; do not mechanically waive that requirement.

## 2. Exact pinned, independently checked baseline

| Evidence | Current value |
| --- | --- |
| Initial contextual meanings | 611 |
| Formulations | 659 (639 screened, 20 provisional) |
| Full initial source-free scans | 659/659 |
| Unassigned / ambiguous occurrences | 0 / 0 |
| Raw missing candidate records | 727 |
| Canonical missing candidates | 418 |
| Effective missing-reference occurrences | 841 |
| Scan amendments | 775 |
| `STATE.summary.phase` | `consolidate_occurrences` |
| `STATE.summary.consolidation_gate_valid` | `false` |
| `inventory_sha256` | `34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113` |
| `unresolved_fingerprint` | `7b69e2fdcb30a4536883df44308d386219b7621533886d65276b8992959f4773` |
| Independent meanings Git blob | `c9cf5b6365fd4349ea1f5409285a82b10d0edb1b` |
| Source observations Git blob | `27b356a11e1855865cb4fba070ce0786c39a2623` |

These were checked against the live branch's `STATE.json` and existing review's exact source/inventory evidence on 2026-10-26. The previous independent engineering round reports **19/19 mechanical readiness checks**, but these were **not rerun** during this document-only review. The approved granularity policy (draft PR #14) permits **typed component prerequisites**; it does not imply equality of general and specialized whole meanings.

## 3. Meaning-level and dependency dispositions

1. **Size/context repairs previously applied:** do not repeat the generic-category/functor corrections, the three generic-groupoid links, the setoid historical seed override, or the general limit/colimit category-size corrections. Their effective amendments/aliases/override were checked in `READINESS_TRIAGE.md`. The deliberately small `Groupoids`-valued presheaf remains distinct. Historic warning reports are not current live defects.
2. **High-frequency identities:** `missing.fcb5ab865c6d9dbb3d79` (generic category, 60 occurrences) and `missing.c5104821c3c70afa1f63` (generic functor, 39) must not be merged with the small-category / small-category-functor meanings. Quotient ring (16), set preimage (15), polynomial algebra (14), residue field (11), unital commutative ring (11), free module (11), and quotient module (10) likewise have no safe matching existing *whole* meaning in the reviewed independent corpus. See `HIGH_IMPACT_EXISTING_MATCH_REVIEW.md`: nine candidates represent **187** incoming occurrences. These negative-match judgments support deliberate first-generation research, not automatic admission.
3. **Other candidate identities:** retain current canonical IDs and their aliases pending individual bounded research/disposition. The 418-candidate `FIRST_GENERATION_QUEUE_PREVIEW.json` remains unapproved and must be revalidated, not treated as a certified frozen list. New dependencies found while writing first-generation definitions go into a distinct later-wave queue.
4. **Typed component cases:** preserve prerequisite-versus-whole-construction distinctions under `APPROVED_DEPENDENCY_GRANULARITY_POLICY.md`. The 40 historical cases partition into 13 original-provider convention checks, six candidate wording/type clarifications, 20 component reviews and one already corrected edge. Existing exact-effective reviews cover 73 occurrences / 72 parent visits in 26 case ranks, with 6 remaining context-representation mismatches; review is recorded, not source certified.
5. **Specific deferred graph-side questions:** the 3 rank-36 generic integrability occurrences and 3 rank-38 generic clopen occurrences need a guarded candidate-context overlay/adjudication (draft PR #15), not a forced alias split or a generic-to-specialized semantic substitution. Rank 298's zero-divisor reference may be explanatory/non-definitional; hold its optional reclassification pending an exact approved occurrence review. **Never** resolve rank 172, 223 or 245 generic-construction candidates back to their own specialized owning meanings, which would introduce circular self-prerequisites. These are bounded classification/representation questions, **not evidence requiring another global synonym sweep**.

### Explicit compactness/FIP determination — not a new defect

An earlier contextual report quoted the compactness/FIP equivalence without its leading family qualification and warned that on the **empty space** the **empty** closed-set family vacuously has the finite-intersection property if only **nonempty finite** index sets are tested. Under that *unqualified* statement, the compactness equivalence is indeed false. However the **current authoritative formulation** was inspected directly in `records/meanings.jsonl` (blob `c9cf5b6365fd4349ea1f5409285a82b10d0edb1b`):

> `form.wave2.broad67.compact-closed-fip`: “Equivalently, X is compact if every **nonempty family** of closed subsets of X that has the finite intersection property has nonempty total intersection.”

Its current formulation version from `STATE.json` is `844fa46b00ce7ef7960240f19be908bf46ae0985f5f45de1195b8137d61ed213`. The FIP reference is `missing.ded806b239b007c8af8c` (recorded nonempty-finite-subfamily interpretation; one parent occurrence), while the closed-subset predicate is the distinct `missing.c4ed408b10943e9c0f8e`. The nonempty-family qualification removes the empty-family counterexample even for `X=∅`: any nonempty family of closed subsets of the empty space contains `∅` and fails nonempty finite intersection. For nonempty `X` the familiar complement/open-cover proof works. **Do not resubmit an FIP text edit or treat the old bare quote as a current blocker.**

When subsequently defining FIP as an independent missing meaning, record the *scope convention* explicitly. The alternative all-finite-subfamilies-including-the-empty-index definition would also make the unrestricted compactness equivalence correct; do not silently conflate the two conventions, and do not alter the authoritative current formulation to chase an obsolete finding. The owner previously approved addressing the FIP convention; the now-verified source text means any new action must be chosen against the actual effective version, not the older report.

## 4. Source-mathematics issues: quarantine from publication, not merge candidates

The six **unapplied**, version-pinned proposals are already fully written in `SOURCE_CORRECTION_OPTIONS.json`, including exact formulation ID, source observation ID, old/suggested wording, original version SHA, counterexample or boundary argument, locator and preflight needs. The original meaning/formulation and paraphrase observation must be revised consistently; graph scans and incoming dependencies require version revalidation. **None has been applied.**

| Scope | Pass 2 decision | Release eligibility |
| --- | --- | --- |
| `form.3718becace9c852d.quasifinite-at-prime` | Keep already-fixed scheme-fibre dependency. Local fibre dimension zero at generic `(0)∈Spec(k[t])` does **not** imply an isolated point. Closedness in the finite-type fibre is needed for the displayed equivalence. | Correct wording with source verification **or hold this formulation**. |
| `form.83a528850cdf6a59.submersive-continuous-map` | An open-preimage biconditional without surjectivity does **not** imply quotient/submersive map; singleton→discrete two-point inclusion is a counterexample. Existing surjectivity/topology links remain legitimate. | Correct equivalence with explicit surjectivity **or hold**. |
| `form.646e4dcbd9b6f1e1.topological-ring` | In permitted nonunital scope, continuity of addition and multiplication does not imply continuous negation (ordered Alexandrov topology on integers, zero multiplication). | Require topological additive group or separate sourced unital variant **or hold**. |
| `form.646e4dcbd9b6f1e1.topological-module` | Under potentially nonunital action, continuous addition/action does not imply continuous negation (zero action example). | Require topological additive group or sourced, explicitly unital module-action variant **or hold**. |
| `form.f77b42c1adb38c56.perfect-closure` | Positive-characteristic root construction is valid *in its stated scope*; general geometric variants need clear `k^perf=k` in characteristic zero. | Distinct convention/variant integration; do **not** falsely label the positive-characteristic definition wrong. |
| `form.41e3aea7f356bae3.rank-of-map-finite-free` | Give existing zero-map clause precedence: rank `0` for `φ=0`, then nonzero exterior-power maximum; avoids excluding zero ring, where `∧⁰φ` is zero. | Editorial clarification and source review before integration; no global `R≠0` rule. |

Additional **provider-specific** bounded source checks remain open: historical rank **133** (shared unit in included subrings), **166** (Stieltjes one-sided normalization/endpoint and atom conventions), and **175** (zero-ring rank). The other ten historical provider convention questions have selective provider evidence in `PRIMARY_SOURCE_STATUS.json` on draft PR #14; no archival source snapshot or full record is automatically certified by that evidence. Other specifically documented source caveats, e.g. rank 23's geometric regularity paraphrase, also remain release-level review obligations.

Four independent **provisional population source issues** remain unscreened/unpromoted, not automatically publication-eligible:

- `issue.wave2.pop140.pairwise-proofwiki-quantifier` (`form.wave2.pop140.pairwise-independent`): retain distinct-index and pairwise-vs-mutual distinctions.
- `issue.wave2.pop141.eom-outer-measure-convention` (`form.wave2.pop141.outer-measure-full`): countable subadditivity alone does not imply monotonicity; source-domain convention needs checking.
- `issue.wave2.pop142.bounded-quantifier` (`form.wave2.pop142.bounded-linear`): global linear-operator bound cannot be replaced by an individual-point quantifier.
- `issue.wave2.pop142.operator-norm-codomain`: numerator must use the codomain norm; preserve the correct stored alternatives.

Exact source evidence/versions and countermodels for these issues remain in `SOURCE_DEFERRALS.md` on draft PR #14. **Do not publish/promote an affected formulation without independent reconciliation, and do not change protected source or graph data under this document.**

## 5. Gate review, transaction boundary and staged first-generation research

**Reviewer proposition:** known high-impact wrong-target/type/size issues appear bounded, previously corrected, or explicitly deferred. No presently identified outstanding issue demonstrates that *another global missing-identity synonym sweep* is necessary prior to a scoped Pass 2 classification decision. This is a reasoned exit recommendation—not a claim no undiscovered errors exist.

**Required before an actual transition:**

1. Obtain a separate explicit owner/reviewer approval of this mathematical consolidation rationale, including the bounded source/provisional exceptions and limits of manual review. Recheck draft PRs #13–#17 and any concurrent graph changes without merging them implicitly.
2. Re-read live `INVENTORY.json.source_inventory_sha256`, `STATE.json.summary.unresolved_fingerprint`, `CHECKPOINT.json`, effective alias/seed/scan history, and complete classification counts. If either pin changes, **re-review and regenerate** the gate packet and queue; old hashes cannot be carried forward.
3. Review `CONSOLIDATION_GATE_PACKET_DRAFT.json` as an **offline artifact only**. Only after separate gate authorization submit an exact, version-matching `consolidate` package through the existing reviewed inbox workflow. Require successful preflight, exact applied receipt, and independent graph `STATE.summary.consolidation_gate_valid=true` and phase `research_missing_dependencies`.
4. Only then permit source-backed first-generation research against the independently maintained accepted/provisional corpus, taking the **bounded 418 candidate preview** as starting scope (subject to revalidation), preserving every canonical ID, originating occurrence and source/version fingerprint, mathematical identity reasoning, and all explicit holds. Provisional researched outputs may serve as *lower-trust comparison anchors*, never auto-establish identity.
5. The existing workflow describes recursive later dependency research by default, while owner-approved draft PR #16 changes the **publication milestone** to a bounded *nonrecursive* first-generation pass. Implement or explicitly approve the revised staging/stop rule without bypassing event/receipt or content-version safeguards. Record second-generation discoveries separately. Do not touch original production definitions until the independent bounded release-candidate freeze; production reconciliation and deployment each need their own review.

**Validation in this round:** live metadata, selected actual independent mathematical record, and relevant PR reviews were read through the connected GitHub API; prior source/version checks are cited in `REVIEW_VALIDATION.json`. **No complete Python test suite, replay of all 19 readiness checks, source-provider refetch, release preview or GitHub Action was executed in this writing session.** No live independent source, graph ledger, original production, frozen Wave 1, site, gate or Pages changes.

**Resume from here:** finalize the reviewed gate decision, not another synonym sweep. If the owner authorizes submission, regenerate/verify exact hashes before applying; thereafter run the bounded first-generation research milestone under explicit nonrecursive safeguards, carrying the above per-formulation release holds forward.
