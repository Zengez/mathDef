# Proposal: opportunistic provisional completion during dependency research

**Date:** 2026-10-26  
**Status:** proposed reusable workflow improvement; design documentation only. Not implemented in the engine, not a mathematical result, not a Pass 2 gate transition, and not publication approval.  
**Applies to:** mathematical definitions in mathDef; intended to generalize to mathematical theorem catalogs, educational resources, and other structured research/reconstruction projects.

## Problem and objective

The dependency-first process should remain the default because identifying existing items and consolidating obvious duplicates before conducting substantial research saves time. An inefficiency appears, however, when determining whether a dependency is genuinely absent **already requires nearly the research that would be needed to produce a definition**. Earlier reviews sometimes determined the domain, quantifiers, axioms, essential hypotheses, counterexamples and relevant sources, but produced only an unresolved-candidate annotation. A later population pass then repeats the expensive work.

**Principle: amortize deep reasoning at the point of use.** When the expected marginal effort to finish an **adequately supported preliminary content item** is small compared with the future cost of reconstructing the context and findings, finish it now and persist it as a **provisional, lineage-tracked output**. Use that provisional output as an additional, lower-trust reference for future classification.

This is a conditional subroutine, **not** replacement of dependency-first screening with a full research pass on every lexical candidate. Do not generate a definition merely to have one, do not require source research for obvious aliases, and do not keep researching indefinitely to satisfy the trigger.

## Decision rule: "suitably close"

During a dependency/identity decision that becomes mathematically or empirically deep, apply this short checkpoint:

1. **Has substantial output-relevant work already been done?** Examples: the full mathematical object and context, conditions, necessary counterexamples, and/or credible source have already been examined. This excludes routine lexical grouping, obvious links, and mere conjecture.
2. **Can a bounded artifact now be produced?** For mathDef, can we accurately state its *type/object*, *hypotheses and quantifiers*, *defining condition or construction*, *distinguishing context* and *traceable source/locator*? At least four of these five components should normally be substantively established and the remainder achievable by a small targeted check. This **heuristic is not a mathematical certificate**.
3. **Is finishing now cheaper than restarting later?** A useful operational indicator is that a source-backed provisional formulation can be completed with one brief, bounded source/wording check, whereas delaying would require rereading multiple sources or repeating substantive mathematical analysis. A rough remaining-effort estimate no more than ~20–30% of the work already invested may help but is **never a mandatory stopwatch or a scientific threshold**. Compare marginal cost and expected reuse, not sunk cost.
4. **Is the research phase permitted and appropriately sourced?** If the current phase forbids external research/content population, **do not fetch sources or write to protected meaning records**. Instead record a compact *ready-for-provisional-completion* lead pointing to the existing already-available reasoning, and perform the completion when the approved research phase begins.
5. **Is the object supportable?** If definition correctness, source authority, contextual identity, rights, or required evidence remains materially disputed, **defer or quarantine** rather than fabricate certainty or mechanically convert a disputed context into a definition.

If the opportunity is clear: complete a provisional output immediately, including a self-contained mathematical statement and the essential qualification; document exactly what is unverified.

**Decision options:** ordinary existing match; obvious new-candidate record; complete provisional output; ready-to-complete lead for a blocked research phase; unresolved/deferred with mathematical reason.

## Separate "provisional output" from "accepted result"

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
