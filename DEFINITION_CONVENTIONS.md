# mathDef — mathematical definition conventions and interpretation notes

**Status:** standing editorial reference, established 2026-10-27.
**Audience:** everyone reviewing, consolidating, comparing, writing, or linking mathematical definitions in mathDef, including future ChatGPT/Codex work.
**Scope:** interpret the *mathematics* of already available definitions; this is **not** a list of new terminology candidates, a global axiom system, or a substitute for source verification.

> **Required reading before definition review.** Read this guide together with `AGENTS.md` and the current execution plan. Apply its checks to comparisons and deduplication throughout the corpus, even if a temporary project plan does not repeat them. Amend this document whenever a recurring scholarly convention is identified; do not rely on a conversation-specific memory.

## 1. Core observation: tacit boundary cases

Mathematical writing often *implicitly assumes* that a set, space, module, index family, object, or example is nonempty/nonzero/nontrivial. Authors may omit the degenerate case to streamline exposition, because the typical theorem needs a stronger hypothesis, or because of conventions in their field. This can make definitions **appear to disagree without introducing substantially different mathematical constructions**.

**Interpretive rule:** A difference involving the empty set, zero object, trivial group, degenerate interval, singleton, or empty indexing family should trigger a **boundary-case/convention check before we classify two definitions as distinct mathematical variants**. Conversely, **do not silently declare them equivalent**: explicit nonemptiness or identity requirements can change the extension of a definition, theorem hypotheses, or the behavior of constructions.

An author-specific restriction is not automatically a mistake, and the omitted-case convention is **not universal**. Distinguish an implicit working assumption from an explicit mathematical requirement using the actual logic of the statements and, where needed, source context.

The editorial goal is to retain meaningful mathematical perspectives, not manufacture duplicate formulations out of ordinary shorthand *or* erase substantive differences.

## 2. Practical decision procedure for every candidate pair

1. **Expand the mathematics.** Write each definition as a predicate with the same explicitly stated ambient category, quantifiers, variables, structures, and algebraic/topological assumptions. Identify differences in objects and operations before worrying about English prose.
2. **Test boundary objects.** Ask what each definition says about the empty set or space, singleton, zero vector/module/ring, trivial group, empty family, zero-dimensional case, and other relevant degeneracies. Determine whether a quantifier is vacuously true and whether the definitions intentionally exclude that object.
3. **Check what the author meant.** Distinguish (a) standard vacuous truth, (b) tacit 'nonempty/nonzero' standing assumptions, (c) a deliberate alternative convention, and (d) a substantive change in permitted mathematical structure. Verify the formulation's cited source before assigning (b) or (c) confidently.
4. **Compare on the meaningful common domain.** If both predicates agree for every nondegenerate object, identify the exact exception. Ask whether retaining separate full definition cards teaches a genuinely different construction, or whether one precise definition plus a **source-attributed convention note** would be clearer.
5. **Classify conservatively.**
   - **Clear duplicate:** only notation, trivial rewording or tacit shorthand differs; one well-written formulation with collected sources is adequate.
   - **Clear mathematical variant:** different defining objects, structural constructions, required hypotheses, genuinely useful characterizations or incompatible frameworks. Retain it.
   - **Boundary-convention difference:** the same core definition, but an author adds/excludes a degenerate case. **Do not automatically merge or automatically retain as a separate conceptual variant.** Record the exact difference, sources, and recommended treatment; if nontrivial, submit to the user's existing uncertain-case review process.
   - **Unclear:** retain pending explicit review; state the question in mathematical terms.
6. **Preserve traceability.** If formulations consolidate, retain independent mathematical source URLs in the term/meaning source registry, indicate the selected **primary source**, and record exceptional conventions in structured notes rather than discarding their evidence. Labels such as 'Original mathDef' or 'Wave 2' are provenance, not subject or context.
7. **Respect the active work phase.** In the 2026-10-27 deduplication effort, collect borderline cases for the user's review **before** any final full linking rebuild, as mandated by the temporary cleanup plan. This guide neither authorizes new candidate discovery nor overrides that review checkpoint.

## 3. Worked example: empty connected spaces

Consider the same topological object `X` under two formulations:

- **No nontrivial separation:** there do not exist two **nonempty**, disjoint, open subsets whose union is `X`. Under the ordinary logical reading, **the empty space is connected**, vacuously.
- **Nonempty and no nontrivial separation:** `X` is additionally required to be nonempty, so the empty space is **not** connected.

These agree on **every nonempty topological space**. Their sole difference is the empty boundary case. **This is a real convention choice, not evidence of two intrinsically different notions of connectedness on nonempty spaces.** It need not justify two independent, nearly identical displayed definition cards.

However, do **not** assert that every author includes the empty space, nor dismiss an explicit nonempty requirement as mere laziness. For example:

- Munkres' standard 'no separation' formulation treats the empty space as connected by vacuity: [Topology, section on connected spaces](https://math.mit.edu/~hrm/palestine/munkres-topology.pdf).
- [Mathlib's connectedness notes](https://imperialcollegelondon.github.io/FLT/docs/Mathlib/Topology/Connected/Basic.html) explicitly distinguish `IsConnected` (nonempty) and `IsPreconnected` (the separation property without nonemptiness).
- [nLab's connected-space discussion](https://ncatlab.org/nlab/show/Introduction%2Bto%2BTopology%2B--%2B1) adopts the nonempty reading in one treatment and explicitly recognizes the alternative as a convention.

**Deduplication guidance:** compare the *full* formulations and citations, then usually prefer one mathematically explicit core formulation plus a short, clearly attributed empty-space convention note if the definitions differ only here. If that would erase a distinction essential to the term's actual usage or related results, leave the case in the user's uncertainty queue. Do not globally rewrite all connectedness notions without source-specific adjudication.

The same check may be useful for **path-connected spaces**, but verify their own authors' conventions separately rather than extrapolating from connectedness.

## 4. Additional recurrent convention families (prompts, not blanket rules)

| Family | Boundary or hidden convention to check | Review warning |
|---|---|---|
| **Empty sets/spaces** | Nonempty assumed versus universal/vacuous definition; compactness, connectedness, path-connectedness, manifolds | Do not import an implicit nonempty requirement from a particular theorem into the basic definition of the concept. |
| **Zero/trivial algebraic objects** | Zero ring, zero module/vector space, trivial group, zero ideal | A meaningful nonzero/nontrivial qualification may change the actual class and should not be discarded without examination. |
| **Rings and their maps** | Ring with `1` versus possibly nonunital; whether homomorphisms preserve `1`; whether `0=1` is allowed | These are often *substantive* category/structure conventions, not simply omissions of a degenerate case. |
| **Domains/fields** | Integral domains conventionally require `1 != 0`; field axioms exclude the zero ring | Do not 'restore' a trivial case that violates an explicit axiom. |
| **Natural numbers and indexing** | `0 in N` versus `N = {1,2,...}`; indices beginning at `0` or `1`; empty sequences | An indexing shift is often presentational, but the underlying set convention may be significant. Preserve explicit assumptions. |
| **Empty operations/families** | Empty sum `= 0`, empty product `= 1` when identities exist; empty intersection depends on ambient universe | Do not infer undefined operations or an unspecified ambient universal set. |
| **Finite or degenerate geometry** | Singletons, point intervals, dimension zero, collapsed simplices, constant maps | Different authors' nondegeneracy hypotheses may be deliberate and mathematically useful. |
| **Ordering/completeness** | Empty joins/meets, extrema of empty sets, upper/lower bounds, vacuous universal predicates | Existence of extrema often needs completeness/bottom/top elements or an explicit nonempty hypothesis. |
| **Zero polynomial and degree** | `deg(0)` undefined versus `-infinity` and other conventions | Do not conflate genuinely different definitions of dependent operations. |
| **First/last term and size constraints** | 'Finite', 'positive', 'nontrivial', 'proper', 'nonempty', 'strict', 'unitary' | Adjectives can carry required mathematical data; check them rather than stripping as stylistic qualifiers. |

The examples are prompts for checking, **not a global policy** that all these cases are interchangeable. Disagreements can persist after the degenerate case is set aside, especially when assumptions involve different objects or constructions.

## 5. How to log a borderline case for user review

When the source record already contains multiple formulations, include **all existing formulations** for the term, not only the borderline pair. Suggested structure:

```text
Definition of: [complete existing term]

Subject: [mathematical branch]     Context: [if any]
Def A: [complete formulation]     Source: [URL]
Def B: [complete formulation]     Source: [URL]
Def C: [complete formulation]     Source: [URL]

Question: Are A and B separate useful meanings, or one statement with
          an explicit boundary-case convention note?
Boundary check: [e.g. identical for all nonempty X; disagree only on X = empty]
Clearly retained: [e.g. C, using a distinct defining construction]
Preliminary recommendation: [merge / retain / defer, with rationale]
Status: awaiting user decision
```

Do not turn an undecided boundary convention into a new candidate term, a forced link, or a silently deleted mathematical meaning. Once the user resolves it, record the decision and the selected primary/reference sources.

## 6. Editorial upkeep

This document is **permanent**, unlike task-specific temporary plans or old research queues. When similar interpretive conventions arise, update this guide with the specific logical issue and a reputable mathematical source, preferably including a counterexample or degenerate object. Keep it distinct from the formal mathematical Subject and Context registries that the cleanup is establishing. The guide is an **interpretation aid**, not a corpus of authoritative definitions.

In future chats, read this file **at the beginning of definition-review work**. This ensures its guidance is available even when the conversation that first identified the convention is not in context.
