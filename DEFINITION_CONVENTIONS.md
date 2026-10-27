# mathDef — mathematical definition conventions and interpretation notes

**Status:** standing editorial reference, established 2026-10-27.
**Audience:** everyone reviewing, consolidating, comparing, writing, or linking mathematical definitions in mathDef, including future ChatGPT/Codex work.
**Scope:** distinguish mathDef's adopted definition from the language and assumptions of each cited source, especially when using a source to define another concept. This is **not** a new term-candidate list or a substitute for source verification. Source-convention metadata is specified here; its implementation belongs to the ongoing source-registry cleanup.

> **Required reading before definition review.** Read this guide together with `AGENTS.md` and the current execution plan. Apply its checks to comparisons and deduplication throughout the corpus, even if a temporary project plan does not repeat them. Amend this document whenever a recurring scholarly convention is identified; do not rely on a conversation-specific memory.

## 1. Core observation: tacit boundary cases

Mathematical writing often *implicitly assumes* that a set, space, module, index family, object, or example is nonempty/nonzero/nontrivial. Authors may omit the degenerate case to streamline exposition, because the typical theorem needs a stronger hypothesis, or because of conventions in their field. This can make definitions **appear to disagree without introducing substantially different mathematical constructions**.

**Interpretive rule:** A difference involving the empty set, zero object, trivial group, degenerate interval, singleton, or empty indexing family should trigger a **boundary-case/convention check before we classify two definitions as distinct mathematical variants**. Conversely, **do not silently declare them equivalent**: explicit nonemptiness or identity requirements can change the extension of a definition, theorem hypotheses, or the behavior of constructions.

An author-specific restriction is not automatically a mistake, and the omitted-case convention is **not universal**. Distinguish an implicit working assumption from an explicit mathematical requirement using the actual logic of the statements and, where needed, source context.

The editorial goal is to retain meaningful mathematical perspectives, not manufacture duplicate formulations out of ordinary shorthand *or* erase substantive differences.

## 1A. Adopt an explicit mathDef meaning; keep source assumptions separate

**Two different layers must not be conflated:**

1. **Canonical mathDef meaning:** the mathematically precise predicate/structure mathDef elects to state for a term, with explicit assumptions and boundary cases. When a property is naturally defined by a universal condition that also makes sense on an empty or trivial object, **prefer the broad formulation, including that object**, unless the mathematics itself or a well-supported editorial choice calls for a restriction. Avoid silently importing an author's convenient nonempty/nonzero standing assumption into the base definition.
2. **Source-specific convention:** a qualification a particular book, paper, chapter, section, or formal library imposes on its own use of the term. Such a convention can be perfectly legitimate *within that source* while differing from mathDef's preferred general wording. Record the difference as a source convention, **not automatically as a second core mathematical definition**. **A restriction generally requires affirmative evidence to override mathDef's broad reading**: authors routinely announce restrictive standing assumptions, but may have no reason to explicitly declare that they are *not* adopting a restriction. The absence of an explicit rejection must therefore not force an unnecessary second definition.

This is an **editorial default, not an assertion that there is one universally accepted definition**. Some objects require a nonzero or nonempty condition by their actual axioms; some fields have genuinely competing conventions, and some restrictions determine substantively different structures. Investigate those instead of indiscriminately broadening definitions. Preserve mathematically useful alternate constructions even if they are logically equivalent.

**Place short convention notes after the pertinent canonical definition** (once the user-facing UI is implemented), not inside the defining predicate itself. A note explains common restricted usage without falsely changing what mathDef defines. The full per-source evidence belongs in the term's future **Sources** view, not as repeated inline citations. Until that UI exists, persist the canonical note and source-convention records as metadata.

**Definitions borrowed from a source with a verified narrower convention require an explicit translation.** When adapting a definition that uses a source-defined word, make the inherited restriction visible *in mathDef's actual statement*, e.g., say **"nonempty connected subspace"** instead of simply **"connected subspace"** when the source establishes nonemptiness and mathDef's unqualified term permits the empty subspace. Do this only when the restriction is genuinely required, is not already logically implied, and preserves the source's intended mathematical meaning. Record that the source uses a narrower convention and what wording mathDef made explicit. **If review was inconclusive, default to mathDef's current broad interpretation instead of inventing the narrower source restriction**; keep the inconclusive status and revise later if new evidence establishes it.

Do not present an adapted paraphrase as a verbatim quotation. If the translation changes the mathematical claim rather than merely surfacing an implicit condition, pause for mathematical/source review instead of silently editing.


## 2. Practical decision procedure for every candidate pair

1. **Expand the mathematics.** Write each definition as a predicate with the same explicitly stated ambient category, quantifiers, variables, structures, and algebraic/topological assumptions. Identify differences in objects and operations before worrying about English prose.
2. **Test boundary objects.** Ask what each definition says about the empty set or space, singleton, zero vector/module/ring, trivial group, empty family, zero-dimensional case, and other relevant degeneracies. Determine whether a quantifier is vacuously true and whether the definitions intentionally exclude that object.
3. **Check what the author meant.** Distinguish (a) standard vacuous truth, (b) tacit 'nonempty/nonzero' standing assumptions, (c) a deliberate alternative convention, and (d) a substantive change in permitted mathematical structure. Verify the formulation's cited source before assigning (b) or (c) confidently.
4. **Compare on the meaningful common domain.** If both predicates agree for every nondegenerate object, identify the exact exception. Prefer the naturally broad canonical predicate when logically valid; describe a narrower *source-specific* convention in a **note below the definition** rather than unnecessarily displaying two versions of the same predicate.
5. **Classify conservatively.**
   - **Clear duplicate:** only notation, trivial rewording or tacit shorthand differs; one well-written formulation with collected sources is adequate.
   - **Clear mathematical variant:** different defining objects, structural constructions, required hypotheses, genuinely useful characterizations or incompatible frameworks. Retain it.
   - **Boundary-convention difference:** the same core definition, but an author adds/excludes a degenerate case. **Default to one mathematically precise canonical formulation (often the broader predicate) plus a convention note and per-source convention record**, provided this preserves mathematical correctness. **Do not automatically merge or automatically retain** if genuine usage or constructions differ; record uncertainty and submit important borderline cases to the user's existing review process.
   - **Unclear:** retain pending explicit review; state the question in mathematical terms.
6. **Preserve traceability.** If formulations consolidate, retain independent mathematical source URLs in the term/meaning source registry, indicate the selected **primary source**, and record any source-specific convention **with its scope, evidence, verification state, and explicit wording adjustments** rather than discarding that evidence. Labels such as 'Original mathDef' or 'Wave 2' are provenance, not subject or context.
7. **Respect the active work phase.** In the 2026-10-27 deduplication effort, collect borderline cases for the user's review **before** any final full linking rebuild, as mandated by the temporary cleanup plan. This guide neither authorizes new candidate discovery nor overrides that review checkpoint.

## 3. Worked example: connected spaces, components and scope translation

Let `NoSeparation(X)` mean that `X` cannot be written as the disjoint union of two nonempty open subsets. This predicate is well-defined on every topological space, and **`NoSeparation(∅)` is true** because no such pair of subsets exists.

### 3.1 Canonical mathDef definition

**Connected space.** A topological space is connected if it admits no separation into two disjoint nonempty open subsets whose union is the whole space. **Under this definition the empty space is connected.**

**Suggested note displayed *beneath* that definition (not part of the predicate):**

> **Note (convention).** Some authors adopt a standing convention that a connected space must be nonempty. Under that convention, the empty space is excluded; unless stated otherwise, mathDef uses the no-separation condition, which includes it.

This makes the adopted mathematics explicit without creating a second near-identical definition card merely for a common author's convention. Use a source-attributed wording in the eventual source detail where a particular author makes the nonempty assumption.

This is a meaningful choice **within mathDef**, not a claim that all mathematical literature agrees. As an example of a source using the other choice, mathlib deliberately distinguishes **`IsPreconnected(X)`** (no nontrivial separation) from **`IsConnected(X)`** (nonempty *and* `IsPreconnected(X)`). See its source-level discussion: [Mathlib.Topology.Connected.Basic](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Topology/Connected/Basic.html). That source is evidence for **its own** convention; it does not set mathDef's default.

### 3.2 An imported definition referring to connectedness

Suppose a source with the **nonempty** convention defines a *connected component* using an expression such as:

> A maximal connected subset of a topological space.

The phrase `connected subset` in that source implicitly means a **nonempty** subset satisfying `NoSeparation`. When converting it into mathDef's adopted terminology, make that restriction explicit:

> A connected component of a topological space is a **nonempty connected subset** that is maximal under inclusion among connected subsets.

One can equivalently characterize the component containing a point as the union of connected subsets containing that point (with appropriate interpretation). The **nonempty** qualifier matters for the maximal-subset characterization: in the empty ambient space, a literal maximality definition without a nonempty restriction could erroneously designate the empty set as a component, while the usual point-based components form an empty collection.

**Important:** This is a worked *editorial transformation*, not a claim that all source definitions of connected components have precisely the text quoted above. If a source already imposes nonemptiness explicitly, or its remaining hypotheses logically imply it, no redundant qualifier is necessary. Other source notions—components in a graph, path components, irreducible components, etc.—need separate convention checks.

**Internal source annotation for the imported component definition:**

- The source's terminology `connected` means `nonempty ∧ NoSeparation`, at the verified applicable scope.
- mathDef's unqualified `connected` means `NoSeparation`.
- The adapted **nonempty** qualifier in the component definition restores the source's intended extension.
- Preserve the source's exact citation/locator and the editorial change in provenance; the user-visible Sources view can eventually explain the source convention.
- If the source convention has **not actually been checked**, do **not** claim it exists; mark it unverified and review before applying the transformation.

### 3.3 Do not reverse-inherit assumptions

A working assumption in a theorem ("throughout this proof let X be nonempty") is **not automatically a global convention for every definition in the book**. Conversely, a source-wide convention can affect many later definitions even when those entries never repeat it. Track scope and overrides, not only the URL.

If a new mathDef definition uses a term with multiple accepted mathematical meanings instead of merely a source-wide tacit restriction, decide the intended meaning explicitly and preserve genuine variants. The policy for empty connected spaces is **not** a general instruction to discard all nonempty-related distinctions.

## 4. Reference-source conventions: the future structured registry contract

**A source list alone is insufficient.** Future definition reviewers must be able to ask, for any source and any known convention: **"Is this convention in force *here*, and how do we know?"** Make that information part of the term-level reference/source infrastructure being developed during the deduplication project. This section specifies the expected data and review behavior; it **does not claim the registry or UI is implemented already**.

### 4.1 Separate two records

- **Convention catalog (mathDef-side):** stable convention ID, affected term/concept, mathDef's preferred precise interpretation, relevant boundary object, known alternative interpretation(s), rationale, optional reusable definition note, and citations supporting the existence of differing usage. For example `topology.connected.nonempty` records the dispute about `∅`.
- **Source-scoped convention assessment:** source identity and version/edition (not only host domain), exact source URL/locator, conventional interpretation, scope (whole work / chapter / section / stated local context), evidence and verification state. Multiple assessments per source are allowed, including local overrides.

A source assessment describes **that source**, **not all of Stacks, Wikipedia, a publisher, or an author's entire career**. Different articles, sections, editions, or authors can use different assumptions.

### 4.2 Two separate questions: evidence status and working interpretation

**Critical editorial asymmetry:** mathematical authors often **explicitly adopt a restriction** such as "all connected spaces in this work are nonempty," but would not ordinarily write "we do *not* make that restriction." Therefore a checked source with no discernible restriction should usually be **interpreted using mathDef's canonical broad definition**, *without* treating that interpretation as a verified claim about the author.

For each source/convention pairing, keep **two logically separate dimensions**:

- **Evidence status:** what we actually found (or did not find) after inspection.
- **Effective interpretation for mathDef's editorial work:** how to read a term *when using that source right now*, subject to known applicable restrictions. A working default is a defeasible assumption, not verified source evidence.

| Evidence status | What is known | Effective interpretation when wording/adapting definitions |
|---|---|---|
| `not_checked` | Source/convention not reviewed; **unknown**, not negative evidence | mathDef's canonical meaning is the baseline for *our writing*, but do not attribute agreement to the unchecked source. If correct source translation depends materially on the missing check, inspect the source or log an unresolved case. |
| `verified_applies` | Positive evidence for a specific narrower convention in its applicable scope | Apply the **verified restriction**, preserving its actual conditions and scope. Make any required qualification explicit when translating a dependent definition. |
| `verified_opposite` | Positive evidence that the **particular restriction under investigation** does not apply | **Inherit the current mathDef canonical meaning** for this convention unless another independently verified restriction applies. Keep the source's evidence; do not freeze the then-current canonical breadth as a source-specific value. |
| `checked_inconclusive` | Source/convention examined, no conclusive positive or negative evidence | **Inherit the current mathDef canonical meaning**, provisionally and operationally, **just as for `verified_opposite`**. Keep `checked_inconclusive` as the evidence label, *not* `verified_opposite`; no restriction is inserted into borrowed wording without affirmative evidence. |
| `conflicting_scopes` | Verified statements differ across sections/chapters/local contexts, or applicability is genuinely uncertain | Resolve by the **most specific applicable verified scope**. If irreconcilable and the choice affects mathematics, log for review; do not silently pretend there is one source-wide rule. |

**Default for inconclusive sources:** If we have examined a source and cannot substantiate a restrictive convention, we proceed *prima facie* as though it uses mathDef's broad definition. We do **not** remain undecided about how to word the imported definition solely because the source did not explicitly reject a restriction. If later evidence shows that the restriction did apply, update the source record and the dependent formulations accordingly.

This rule is about interpreting **unproven restrictions**. It does not cancel a narrower assumption clearly stated in the mathematical passage itself, an established applicable standing convention, or a substantive nonempty/nonzero axiom. When an apparent convention alters a mathematical construction beyond a simple qualification, compare the actual mathematics before editing.

### 4.3 Follow the *current* canonical definition dynamically, not a historical snapshot

**The effective interpretation of both `verified_opposite` and `checked_inconclusive` follows the *current* mathDef canonical meaning** for the affected concept. If mathDef subsequently broadens that meaning, these source interpretations **broaden automatically by default**; they are not pinned to the version that existed when the source was checked. No legacy-compatibility requirement should preserve an obsolete narrower working assumption.

For example:

1. mathDef currently takes "connected" to mean "no nontrivial separation" (so `∅` qualifies).
2. Source A positively requires nonemptiness (`verified_applies`): imports from A use the explicit nonempty qualifier where necessary.
3. Source B explicitly rejects that added restriction (`verified_opposite`): imports from B follow mathDef's current connectedness predicate.
4. Source C was inspected but no convention could be determined (`checked_inconclusive`): imports from C **also** follow mathDef's current predicate, *without claiming C explicitly endorses it*.
5. If mathDef later adopts a genuinely broader predicate for a term, B and C inherit that new predicate as the working default without source-specific compatibility shims. A remains constrained by its **verified** nonempty requirement (or any other exact restriction supported by evidence).

**Data-model requirement:** represent the fallback as `effective_interpretation: "inherit_current_mathdef_canonical"` (or equivalent resolution logic) tied to a stable **concept/convention ID**. Do **not** save `empty_allowed`, an old predicate, or a snapshot revision as a *fixed* operational value for `verified_opposite` / `checked_inconclusive`. The former may be recorded as *historical evidence*, but operational semantics must be computed from the latest canonical definition.

A change to the canonical meaning should trigger a **targeted recheck of dependent imported definitions**, especially those with previously inserted qualifiers or semantic transformations, so their actual mathematical statements remain correct. This is not a requirement to preserve the old interpretation or compatibility: revise affected definitions when necessary. The fallback is intended to minimize unnecessary restrictions, **not** to excuse mathematically false source attributions or contradictions in explicit source axioms.

### 4.4 Source assessment records and source-scope inheritance

The following is a suggested machine-readable record (illustrative, not yet populated):

```json
{
  "source_id": "source.example-book.edition",
  "source_url": "https://example.org/book-or-article",
  "source_title": "Example mathematical work",
  "edition_or_version": "edition or revision, if known",
  "term_ids_supported": ["connected-space"],
  "primary_for": [],
  "conventions": [
    {
      "convention_id": "topology.connected.nonempty",
      "status": "checked_inconclusive",
      "effective_interpretation": "inherit_current_mathdef_canonical",
      "canonical_concept_id": "topology.connected",
      "explicit_source_restriction": null,
      "scope": "section reviewed; no source-wide conclusion verified",
      "evidence_url": null,
      "evidence_locator": null,
      "checked_at": null,
      "notes": "Relevant sections reviewed without conclusive evidence of a restrictive standing convention; mathDef's current canonical meaning is the provisional default, not an attributed source claim."
    }
  ]
}
```

Here the URL and identity are **placeholders**, not a report about an actual source. To record a verified restrictive convention, set `status` to `verified_applies`, `explicit_source_restriction` to `nonempty_required`, and include the evidence, chapter/section/page, and exact applicability scope. For `verified_opposite`, retain the evidence explicitly rejecting the restriction, but use `effective_interpretation: "inherit_current_mathdef_canonical"`. For `checked_inconclusive`, use the **same operational interpretation** with the **different evidence status**. A source-wide restriction is inherited by subsequent passages only where the verified scope actually includes them; a narrower local override takes precedence. A source with **no assessment** is `not_checked`, not silently `checked_inconclusive`.

The eventual schema should support multiple independent conventions per source, even if most have not been checked. The term-level **Sources** link should show accessible references and useful convention warnings, while correction reports and source-reliability analytics remain **internal-only** and separate, as specified in the deduplication plan.

### 4.5 Translation audit trail for reused definitions

When an imported source definition has been rewritten to expose a convention, track:

1. Source identity, exact original passage location, and whether the mathematical text was *quoted* or *paraphrased*.
2. The convention ID, **verified applicable** source assessment and scope.
3. The original predicate expressed using the source's interpretation. Distinguish a **verified restriction** from the **provisional canonical fallback** for inconclusive checks.
4. The explicit mathDef formulation (for example, adding `nonempty` to `connected subset` **only when a nonempty source convention is verified**), with a short mathematical equivalence justification. Record when the formulation simply follows the current mathDef canonical predicate.
5. Which term/meaning/formulation was affected, and any related concepts whose definitions might need review.

This audit trail prevents inadvertent semantic drift or attribution errors. It also allows later editors to revisit inherited assumptions if an author's convention was misunderstood. When exact equivalence cannot be demonstrated, preserve the original as a candidate for *manual adjudication* rather than treating it as a straightforward wording repair.

### 4.6 When to apply this infrastructure

The current **deduplication and source-registry cleanup** should adopt this data model as appropriate and record actual verified source conventions as sources are reviewed. Its import/duplicate decisions must implement the **canonical-default behavior of checked-inconclusive sources**, without promoting their evidence status. Do **not** launch a separate retrospective crawl solely to fill every source–convention combination, and do not mark unchecked or inconclusive items as verified to improve a coverage metric. Counts of checked/unchecked assessments can be added later.

Do not implement the user-facing **Sources** drawer, source-reliability scoring, or extra UI behavior merely because this contract is documented. The user wishes to revisit display choices *after* mathematical deduplication. Preserve the agreed **user review of uncertain duplicates before the final global linking rebuild**.

## 5. Additional recurrent convention families (prompts, not blanket rules)

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

## 6. How to log a borderline case for user review

When the source record already contains multiple formulations, include **all existing formulations** for the term, not only the borderline pair. Suggested structure:

```text
Definition of: [complete existing term]

Subject: [mathematical branch]     Context: [if any]
Def A: [complete formulation]     Source: [URL]
Def B: [complete formulation]     Source: [URL]
Def C: [complete formulation]     Source: [URL]

Question: Are A and B separate useful meanings, or one canonical
          predicate with a note about source-specific conventions?
Canonical mathDef predicate: [precise mathematical condition proposed]
Boundary check: [e.g. agree whenever X ≠ ∅; disagree only for X = ∅]
Source-convention assessments: [source URL, scope, verified_applies /
  verified_opposite / checked_inconclusive / not_checked, plus working fallback]
Borrowed-definition translation: [if needed: source shorthand → explicit assumption]
Clearly retained: [e.g. C, using a distinct defining construction]
Preliminary recommendation: [merge with note / retain / defer, with rationale]
Status: awaiting user decision
```

Do not turn an undecided boundary convention into a new candidate term, a forced link, or a silently deleted mathematical meaning. Once the user resolves it, record the decision and the selected primary/reference sources.

## 7. Editorial upkeep

This document is **permanent**, unlike task-specific temporary plans or old research queues. When similar interpretive conventions arise, update this guide with the precise canonical mathDef meaning, the source-specific alternatives, scope and evidence, and the mathematical effect of translating a borrowed definition. Include a boundary-case example or counterexample when useful. Keep it distinct from the formal mathematical Subject and Context registries that the cleanup is establishing. The guide is an **interpretation aid**, not a corpus of authoritative definitions.

In future chats, read this file **at the beginning of definition-review work**. This ensures its guidance is available even when the conversation that first identified the convention is not in context.

## 8. User-adjudicated canonical choices (2026-10-27)

The following are **mathDef's editorial definitions**, explicitly decided by the user, not claims that the cited authors or mathematical literature unanimously agree. They override default suggestions to permit degenerate/empty objects when the user has deliberately chosen a narrower convention. The source-evidence states and their dynamic inheritance rules in §4 remain in force: an unchecked or inconclusive source is not evidence of endorsement; effective editorial interpretation follows the **current canonical meaning**, while a positively verified source-specific difference must be identified and documented.

- **Zero divisor (commutative rings).** The element `a` is a zero divisor only if **`a ≠ 0`** and some **`b ≠ 0`** satisfies `ab=0`. In particular `0` is not a zero divisor in mathDef. Some authors permit zero when the ring is nonzero; this difference is a boundary convention, not a second canonical meaning. Canonical convention ID: `commalg.zero_divisor.zero_included`.
- **Metric space.** An ordinary metric space `(X,d)` must have **`X ≠ ∅`**. The metric axioms on an empty set may be vacuous, but mathDef does not call the resulting pair a metric space. The metric-induced topology characterization remains informative for the canonical nonempty setting. When importing dependent definitions that used an empty metric space, remove or qualify such claims in the merged editorial layer; **do not conflate this with the empty topological space**, which can still be discussed under topology's independent conventions. Convention ID: `metric.metric_space.empty_underlying_set`.
- **Affine span / affine hull.** These are two searchable titles for **one mathematical construction**: finite affine combinations of a **nonempty** subset of a real affine space, equivalently the smallest affine subspace containing it, equivalently the intersection of affine-combination-closed supersets. The user notes *affine span* is common in algebraic contexts and *affine hull* in analytic contexts. For now mathDef **does not define `aff(∅)`**, although some mathematical conventions define it to equal `∅`. Retain both labels, both characterizations and relevant source provenance. Convention ID: `geometry.affine_hull.empty_input`.

These choices can be revisited following a mathematically substantiated user correction; do not revert them merely because a broader vacuous convention is logically possible. The concrete canonical meaning IDs and notes live in `data/math_definition_conventions.json`; edited historical wording is staged in `data/merged_cleanup_decisions.json`, not written into frozen original or research source files.
