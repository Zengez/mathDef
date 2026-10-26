# Standing rule: opportunistic completion at any stage of research

**Date:** 2026-10-26  
**Status:** **owner-approved general workflow rule**, effective for subsequent mathDef review, research, preparation, integration, quality assurance and audit work. The runtime automation / supporting engine changes are not yet implemented. Approval of this method is **not** a mathematical-content approval, a Pass 2 gate transition, source certification, permission to alter protected records, or publication approval.  
**Applies to:** every stage of mathDef, not only dependency discovery: candidate collection, dependency and context classification, source research, formulation drafting, cross-definition consolidation, variant work, technical integration, QA, citation and renderer audits, release notes and later bounded patch/audit waves. It also provides a reusable default for analogous mathematical theorem catalogs, educational resources, and other structured reconstruction projects.

## Problem and objective

The dependency-first process should remain the default because identifying existing items and consolidating obvious duplicates before conducting substantial research saves time. An inefficiency appears whenever a step, **at any stage**, already requires nearly the work needed to produce a useful output that a later stage would otherwise recreate. A deep dependency distinction leading almost to a definition is one prominent example, but the rule is not confined to it. Earlier reviews sometimes determined the domain, quantifiers, axioms, essential hypotheses, counterexamples and relevant sources, but produced only an unresolved-candidate annotation. A later population pass then repeats the expensive work.

**Standing principle: capitalize on near-completed work wherever it occurs.** Whenever work in one step has already established most of a useful end product, and completing it now would require only a bounded, low incremental cost, **finish the eligible output then**, instead of forcing the same reasoning to be reconstructed in a later step. Save it as a **provisional, lineage-tracked artifact** if it still needs later review; save it at the appropriate approved final status only if all normal requirements have already been satisfied. Do not lower the quality bar to call something finished. Use that provisional output as an additional, lower-trust reference for future classification.

This is a conditional subroutine, **not** replacement of dependency-first screening with a full research pass on every lexical candidate. Do not generate a definition merely to have one, do not require source research for obvious aliases, and do not keep researching indefinitely to satisfy the trigger.

## Across-the-workflow application examples

The checkpoint applies wherever the work becomes close to another **valid end product**, not only when definitions are missing:

- **Source intake:** If checking a citation already establishes all hypotheses and the correct source-specific version, save a reusable source-backed formulation/review result, not just a short locator comment.
- **Dependency classification:** If resolving a difficult false-target/meaning issue effectively constructs a rigorous definition, finish a provisional version when allowed, and link its original candidate and occurrences.
- **Consolidation and variants:** If the review establishes a complete alternative formulation or a rigorous non-equivalence argument, preserve that as an independently reusable variant or adjudication artifact.
- **Mathematical audit:** If investigating a flaw gives a fully justified narrow correction and a counterexample, complete the exact version-anchored proposed patch and test rationale; do not merely flag "needs fix." Apply it only when the source-revision procedure permits.
- **Software/integration work:** If a one-off diagnostic nearly produces a general, validated reusable script, finish the reusable unit and tests when the incremental effort is low and changes are authorized. Otherwise preserve a tested proposal.
- **Publication/release preparation:** If validating a release diff supplies enough evidence for release notes, an exact manifest or a rollback checklist, finish those artifacts while the evidence is assembled.

The rule applies to **final outputs too**, not just provisional definitions. If all normal acceptance conditions are already satisfied, publish/save the result into the appropriate authorized stage; *provisional* is only needed for remaining mathematical, citation, source, technical or editorial review obligations.

## Preserve efficiency and scope

Use the nearest useful deliverable and smallest reasonable incremental step. Do not broaden a bounded audit into indefinite new research, convert every incidental insight into a new task, or divert effort from the current goal just to "complete" something. A strong reason to finish is likely **reuse or avoidance of duplicated analysis**. If the remaining work is substantial, save a precise handoff, source evidence, and a named next action instead.

This applies as an ongoing human/assistant working rule immediately, independent of whether a future automated trigger has been implemented. The rule does not override the explicitly gated independent-reconstruction workflow, the prohibition on consulting production mathematical content before freeze, version guards, source checks, or deployment approval.

## Decision rule: "suitably close"

During **any** research, review, checking, integration or documentation step that becomes mathematically, technically or empirically deep, apply this short checkpoint:

1. **Has substantial output-relevant work already been done?** Examples: the full mathematical object and context, conditions, necessary counterexamples and credible source; a nearly complete source audit with exact anchors; a reusable integration transformation with tests; a release note whose changeset is already verified. This excludes routine lexical grouping, obvious links and mere conjecture.
2. **Can a bounded artifact now be produced?** For a mathematical definition, can we accurately state its *type/object*, *hypotheses and quantifiers*, *defining condition or construction*, *distinguishing context* and *traceable source/locator*? At least four of these five components should normally be substantively established and the remainder achievable by a small targeted check. For other work, use the corresponding output-specific acceptance criteria (e.g., source locator and quotation accuracy, testable code plus inputs, an exact change manifest). The heuristic is **not** certification and does not supersede mandatory checks.
3. **Is finishing now cheaper than restarting later?** A useful operational indicator is that a source-backed provisional formulation can be completed with one brief, bounded source/wording check, whereas delaying would require rereading multiple sources or repeating substantive mathematical analysis. A rough remaining-effort estimate no more than ~20–30% of the work already invested may help but is **never a mandatory stopwatch or a scientific threshold**. Compare marginal cost and expected reuse, not sunk cost.
4. **Is the required action allowed in the current phase and appropriately sourced?** Complete the deliverable **to the furthest authorized boundary**. If the phase forbids external research or content population, **do not fetch sources or write protected meaning records**. Instead finish an allowed artifact (mathematical rationale, review-ready draft, fixture or *ready-for-provisional-completion* lead) preserving the reasoning, and perform restricted actions when their approved phase begins. Similarly, drafting production-ready material does not authorize merging or deploying it.
5. **Is the object supportable?** If definition correctness, source authority, contextual identity, rights, or required evidence remains materially disputed, **defer or quarantine** rather than fabricate certainty or mechanically convert a disputed context into a definition.

If the opportunity is clear: finish the meaningful, eligible output immediately—such as a provisional definition, full source/equivalence adjudication, reviewed conversion design, tested patch proposal or changelog draft—and document exactly what still requires review or authorization.

**Decision options:** existing accepted output, justified link/merge, new provisional output, completed reviewed output when fully eligible, ready-to-complete lead for a blocked phase, or explicit deferred item with its reason. The aim is not to force every lead into a definition.

## Separate provisional outputs from accepted results

A provisional item is **substantive reusable content** but neither a production definition nor a certified independent reconstruction meaning. Its status must remain visible every time it appears in a comparison or search.

Suggested lifecycle:

```
observed dependency / candidate
  ├─ existing accepted meaning: reviewed link
  ├─ obvious equivalent candidate: justified merge/alias
  ├─ insufficient knowledge: missing / deferred candidate
  └─ deep review, output nearly complete and research permitted:
       provisional meaning/formulation + evidence + lineage
          ├─ used as comparison anchor (provisional only)
          ├─ merged as a reviewed synonym/variant
          ├─ mathematically/source-screened → eligible independent result
          └─ corrected, held or rejected (retaining history)
```

**Accepted** and **provisional** collections should be queried in one comparison workflow but remain separate indexes/tiers. For example, return possible matches in this order:

1. **Accepted meanings within the currently authorized comparison corpus.**
2. **Provisional source-backed meanings**, clearly marked as such.
3. **Open candidate contexts, earlier negative-match judgments and unresolved leads.**

In mathDef's independent Wave 2 experiment, the authorized collection before freeze is the **independent screened corpus**, **not the original production mathDef site**, plus appropriately contained independent provisional outputs. The original production corpus becomes an authorized comparison input **only after the independent release-candidate freeze** under the separately reviewed publish-first plan. For normal post-publication updates, accepted/published meanings may be used immediately.

A provisional anchor is useful for candidate discovery, but **a similarity to a provisional anchor is only a suggestion**. Before any canonical candidate IDs are merged or a graph edge is declared resolved, check the actual mathematical equivalence, domains, hypotheses and context, independent of whether that anchor has already been used for another provisional candidate. **No transitive union-by-similarity**: A resembling B and B resembling C does not show A and C are equivalent; even recorded equivalence needs explicit reviewed justification and eventual version guards.

## What to preserve with each opportunistic provisional output

Use existing source-intake and independent provisional-population schemas when they fit; do not implement a second, incompatible shadow definition catalog. A reusable record or view should provide:

| Field / concept | Why |
| --- | --- |
| `provisional_id` / stable contextual meaning ID | Remains addressable when other candidates cluster around it |
| `origin_candidate_ids` and **exact original occurrences** | Documents that the content came from the *currently reviewed missing-dependency set*, not independent breadth research |
| `origin_batch_id`, graph/input fingerprint and version | Keeps the originating bounded research/audit wave explicit; preserves provenance if later merged |
| Term label, mathematical domain, object/type, distinct context | Disambiguates homonyms and specialization |
| Preliminary formulation(s), hypotheses, exceptions | Gives a substantive comparison object; no placeholder definition |
| Source IDs, exact locators, rights, paraphrase policy | Allows later source-screening without repeating discovery |
| `review_status`, uncertainty/known omissions, mathematical notes | Prevents interpreting a draft as a certified fact |
| Linked/possible related meaning IDs, **relation kind** and rationale | Distinguishes equivalent, alternative formulation, specialization, prerequisite and merely similar |
| Incoming known occurrence IDs; newly discovered missing prerequisites | Reuse immediate links and record future candidates without expanding the current bounded batch |
| Content version / immutable amendment history | Supports later source/correction audit and avoids silent overwrite |
| Promotion/rejection disposition and successor ID | Never lose candidate ancestry when merging into a preexisting meaning |

For mathDef, the existing `research_pipeline/POPULATION_WORKFLOW.md` already separates `populate`, `reconcile` and `certify` and stores source-backed provisional content under the independent population workspace. Prefer adapting those records and the existing candidate registry rather than designing a new unguarded file format.

## Clustering without premature canonicalization

- Compare each new candidate against accepted independent meanings **and** already stored provisional meanings, including their contexts and hypotheses.
- If an accepted meaning is an exact contextual match, record a proposed existing-meaning link and preserve the provisional research evidence as a supporting variant/source, not a duplicated searchable heading.
- If a provisional meaning matches, **attach a reasoned proposed equivalence/variant relationship to that provisional cluster**. Do not destroy the second candidate's source-specific hypothesis or assume that the cluster is automatically a certified meaning.
- If one meaning generalizes another, preserve **both types/contexts**; a generic category is not the same mathematical object declaration as a *small* category, and a general functor is not equivalent to a functor defined only between small categories.
- Distinguish explicitly different conventions, e.g. nonempty versus empty-inclusive connectedness, or unital versus nonunital structures. Prefer contextual variants to indiscriminate synonym merges.
- Retain source and rationale even if two formulations ultimately merge. A later audit may separate them again.
- Review clusters globally at a bounded checkpoint, at least before release-candidate freeze. Re-run targeted matches when a provisional anchor is corrected or rejected.

## Nonrecursive and economical by default

Opportunistic completion is about **reusing deep work already performed**, not recursively researching everything named in the newly drafted statement. Record new references as linked only when already supported; otherwise register them as future-batch candidates. Do not pull second-generation prerequisites into the mandatory first publication batch.

A provisional statement must meet a **basic correctness floor**: no known falsehood, clear scope and core hypotheses, a credible traceable source if presenting source-backed content, and no invented link. Comprehensive literature searching, full cross-context variant discovery, recursive linking, formal peer review and final source/renderer certification may remain for bounded later audit waves.

**Stop condition:** after the short bounded completion opportunity is exhausted, stop. An unresolved source contradiction, disputed theorem or domain ambiguity should become an explicit review task; do not do a second full research pass "while here" merely because much time has already been spent.

## Example: category theory

Suppose a dependency points to an ordinary, potentially large category, but the independent existing definition describes a **small** category. Basic context review can establish immediately that a naive link is wrong. If a source-free phase prohibits new source research, record the generic-category candidate and the scoped nonmerge; stop.

In a research-enabled phase, if verifying the distinction requires reading the full category axioms in a reliable source, the provisional output is almost finished. Write an independently paraphrased general category definition under a provisional meaning ID, with source locator, preserve the existing small-category meaning, and compare subsequent category candidates against **both**. Audit the new provisional content and formalize its link relationships before publication.

## Reusable quality and efficiency measures

The purpose is to reduce repeated work, **not** maximize provisional-item counts:

- Share of deep candidate reviews that yield immediately reusable evidence or a provisional statement.
- Later research tasks that can reuse a source, hypotheses and prepared content without reopening the full case.
- Number of false-positive automatic merges / reviewer-reversed clusters.
- Provisional outputs successfully screened, merged, corrected, held or rejected.
- Time saved by reused research compared with time spent on unnecessary draft creation (sample batches suffice; no false precision).

Pilot with a handful of already researched candidates once the research phase is authorized. Compare effort and correctness with an equivalent ordinary dependency-only batch. Only add any automatic trigger if it is reliable; the initial trigger can be a reviewer decision.

## Current Wave 2 safety boundary

As of 2026-10-26 the current independent Wave 2 has completed all 659 initial scans and has 418 unresolved canonical candidates, but the Pass 2 `consolidate_occurrences` gate remains closed. Historical detailed mathematical reviews **can** be tagged as ready-to-complete leads, but this policy alone **does not authorize researching sources, writing provisional meaning records into the protected workspace, opening the gate, altering approved aliases, comparing the original production definitions, freezing a release or publishing the website**.

Once the separately reviewed gate opens, opportunistic completion can be used throughout the bounded first-generation research pass and later audit waves. The associated proposal for the first publishable release and subsequent bounded patches is `research_pipeline/WAVE2_RELEASE_FIRST_AUDIT_WAVES_PROPOSAL_2026-10-26.md` (draft PR #16).

**Next implementation stage (deferred):** integrate a lightweight phase-aware "ready to complete" marker in existing candidate review metadata and a query combining accepted and provisional comparison results (with trust tiers); add tests for lineage, phase gating, stable IDs, no auto-equivalence, idempotent retry and no production corpus leakage. No change to live mathematical content is implied by this design document.
