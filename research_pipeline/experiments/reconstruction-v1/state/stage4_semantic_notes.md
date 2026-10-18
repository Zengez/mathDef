# Stage 4 semantic classification and consistency notes

Date: 2026-10-18. Workspace: independent `reconstruction-v1`. Read only the sealed research workspace and external scholarly sources; **no production mathDef definitions, variants, citation databases, or audits were consulted**.

## Scope and provenance

The Stage 3 observations registry contains 349 entries, including 31 independently authored candidate paraphrases covering 25 distinct terms. The other 318 entries are source locators: 291 Stacks index sections and 27 unverified PlanetMath leads. Stage 4 inspected the 31 substantive observations and their cited public Stacks Project sections, then generated **31 context-labeled mathematical meanings** with **32 formulations**. All 31 observations are represented by at least one formulation; the upstream `obs.*` IDs, exact section URLs, and source section labels remain attached. Each meaning has `human_verified:false`. No independent formal mathematical refereeing is implied.

The exhaustive 293-term **missing-evidence list** is in `stage4_review.json`. A locator, even if it resolves, cannot independently justify a mathematical definition. These terms remain unresolved and are **not** turned into unsupported meanings.

## Context distinctions retained

| Source section | Interpretive distinction | Treatment |
| --- | --- | --- |
| Stacks 9.10, `09GP` | Algebraic closure **of a given field** versus property of being **algebraically closed** | Two meanings in a shared source-term group; the latter also records the equivalent polynomial-root test |
| Stacks 5.5, `004O` | Open-set **basis** versus **subbasis** built using finite intersections | Two meanings; not equivalent objects |
| Stacks 4.12, `002B` | **Initial** objects (unique outgoing maps) versus **terminal/final** objects (unique incoming maps) | Two dual, non-interchangeable meanings |
| Stacks 5.12, `0059` | Quasi-compactness of a **space** versus of a **continuous map** | Two different object types and conditions |
| Stacks 10.37, `037B` | Integrally closed **domain** versus general **ring** with normal prime localizations | Two contexts; the domain case is a restriction of the general notion, not an unrelated homonym |
| Stacks 26.2, `01HA` | A **locally ringed space** versus a **morphism** of such spaces | Object and structure-preserving arrow distinguished |

Each grouping uses the source term's stable `term_group_id`, retaining the source record even when the displayed mathematical concept is more specific than the original chapter heading. No synonym merging has been performed without affirmative evidence.

## Checks completed

- Inspected the referenced public Stacks Project sections for the 25 source-backed term entries, including exact definitions and adjacent lemmas where the Stage 3 paraphrase relies on an equivalence.
- Verified field-theoretic distinctions such as finite degree, minimal polynomial, algebraic closure, splitting fields, purely inseparable extensions, linear disjointness, and Artin–Schreier constructions.
- Verified categorical variances (initial/terminal, exact/adjoint, pushout and monomorphism) and the fact that a quasi-compact map does **not** have the same defining object as a quasi-compact space.
- Preserved source-specific restrictions: zero copied passages, no PlanetMath automated access under unavailable robots policy, and no use of paid MathSciNet or disallowed OpenStax content.
- Ingestion/semantic integrity gate checks non-locator evidence only, all 31 authored observation IDs covered, globally unique formulation IDs, six split source term groups, stable term-group IDs, context/section metadata, and the presence of an alternative equivalent definition. The regression test also rejects locator-only evidence promotion.
- The Stage 4 automatic GitHub workflow passed its isolated tests, wrote only experiment record/checkpoint files, and sealed the stage with 31 meanings.

## Remaining limitations and Wave 2 follow-up

The bounded Wave 1 test is a **prototype**, not a complete reconstruction of the original mathematics corpus. Only 25/318 title records presently have mathematical definitions, and screened here means *editorial/source screening*, not certification by an independent mathematician. In particular, 293 title records must be revisited for additional source research during Wave 2.

One algebraically closed field formulation currently combines both the extension criterion and polynomial-root equivalence in one paragraph, while a second formulation gives the root criterion separately. Both are correct, but a later editorial revision could make the two alternatives cleaner and more parallel. Because Stage 4 is now sealed, do not edit the record in place; use the versioned revision mechanism in Wave 2.

## Handoff

**Stage 4 is complete and sealed. Next stage: Stage 5 — independently research and screen relevant concept dependencies/relations, recommended effort High.** Stage 5 should prioritize the 31 meanings and 32 forms with actual evidence. The 293 unsupported title leads must not receive imaginary relationship endpoints. Do not use the original production corpus until both complete independent waves are frozen.
