# Temporary mathematically uncertain deduplication decisions

**Working branch:** `work/dedup-subject-context-sources-20261027`  
**State:** all three recorded questions were explicitly adjudicated by the user on 2026-10-27; retained historical alternatives below are no longer awaiting a decision. **Do not perform the final global linking rebuild or publish without the separately authorized final review.**  
**Scope:** Only preexisting mathematical terms/meanings. This file is not a candidate-discovery list.

The historical comparison sections below reproduce **all previously existing formulations under each searchable heading** before the user-adjudicated consolidation; their preliminary recommendations and 'Decision needed' descriptions are archival, superseded by the recorded final decisions at the end of this file. Source URLs are distinguished from verified evidence: a citation that is only a previous research lead is not represented as passage-verified. Stable IDs follow each form.

## Definition of: Zero divisor

**Proposed Subject:** Commutative Algebra. **Context:** Commutative rings; convention governing zero itself.

**Def A — Original mathDef** (`meaning.mathdef.original.commalg.zero-divisor`, form `form.mathdef.original.commalg.zero-divisor.primary`):

> For a commutative ring $R$, an element $a\in R$ is a \emph{zero divisor} if some nonzero $b\in R$ satisfies $ab=0$. Under this convention $0$ is a zero divisor whenever $R$ is nonzero; some authors require zero divisors to be nonzero.

Source: https://en.wikipedia.org/wiki/Zero_divisor (existing original editorial citation).

**Def B — researched nonzero-element convention** (`meaning.wave2.direct.8f2dea7e2bd1211c0cf6`, form `form.meaning.wave2.direct.8f2dea7e2bd1211c0cf6`):

> Under the nonzero-element convention, an element a of a commutative ring R is a zero divisor if a≠0 and there is a nonzero b∈R with ab=0. Some authors also call 0 a zero divisor in a nonzero ring, so the convention matters.

Source lead: https://stacks.math.columbia.edu/tag/00EW ; recorded only as `original_research_lead_not_independently_rechecked`, **not verified support for excluding zero**.

**Decision needed:** Whether Def A and Def B should be one canonical zero-divisor predicate with a documented source/convention note, or two explicitly searchable mathematical meanings.

**Clearly retained:** Both sets of citations, the distinction between commutative and noncommutative ring theories where applicable, and a mathematically explicit rule about the zero element.

**Boundary check:** In a nonzero ring, Def A includes $a=0$ while Def B excludes it. The two agree for nonzero $a$. This is a genuine boundary convention, not a different annihilation construction. The zero ring additionally needs care because Def A requires nonzero $b$.

**Preliminary recommendation:** Favor one mathDef broad predicate (Def A) plus a convention note explaining the requirement $a\ne0$ in sources that positively adopt it. Preserve Def B as evidence of competing usage without attributing a restriction to its previously unchecked Stacks lead. Confirm primary source/section scope before asserting a source-specific restriction. **Status: adjudicated by the user on 2026-10-27; see final decisions below.**

## Definition of: Metric space

**Proposed Subject:** Metric Geometry. **Context:** The empty underlying set and metric-induced topology.

**Def A — Original mathDef** (`meaning.mathdef.original.metric.metric-space`, form `form.mathdef.original.metric.metric-space.primary`):

> A \emph{metric space} is a pair $(X,d)$, where $d:X\times X\to[0,\infty)$ is a function such that
> \[
> d(x,y)=0\iff x=y,\qquad d(x,y)=d(y,x),\qquad
> d(x,z)\le d(x,y)+d(y,z).
> \]

Source: https://en.wikipedia.org/wiki/Metric_space (original editorial citation).

**Def B — researched metric axioms** (`meaning.wave2.analysis98.metric-space`, form `form.wave2.analysis98.metric-space`):

> A metric space is a pair (X,d) where X is a nonempty set and d:X×X→ℝ satisfies d(x,x)=0, symmetry d(x,y)=d(y,x), the triangle inequality d(x,z)≤d(x,y)+d(y,z), and d(x,y)>0 whenever x≠y.

Source: existing independent Wave 2 research evidence associated with this formulation.

**Def C — researched compatible metric topology** (same researched meaning, form `form.wave2.analysis98.metric-space.compatible`):

> For a nonempty set X with a metric d, the balls B_d(x,r)={y in X:d(x,y)<r}, r>0, generate a canonical topology τ_d. The metric-space data (X,d) determine the compatible triple (X,τ_d,d), and conversely a triple (X,τ,d) with τ=τ_d determines (X,d). A metrizable topology alone does not specify a unique metric.

Source: existing independent Wave 2 research evidence associated with this formulation.

**Decision needed:** Consolidate Def A with Def B after resolving the empty-space convention? Retain Def C as a separate informative metric/compatible-topology formulation, or move it to an explanatory characterization?

**Clearly retained:** Def C's additional connection to topology if mathematically useful. Do not erase the distinction between a metric, an induced topology, and an arbitrary metrizable topology.

**Boundary check:** Metric axioms on an empty $X$ are vacuous, and the unique map $\varnothing\times\varnothing\to[0,\infty)$ is a metric under Def A. Def B excludes $X=\varnothing$ explicitly. Def C likewise states nonempty, but its construction extends naturally with the empty topology.

**Preliminary recommendation:** Prefer the broad canonical metric axioms (Def A), with verified nonempty assumptions tracked per source rather than a duplicate card solely for an excluded empty space. Retain Def C as a genuinely different informative induced-topology perspective after checking its scope and deciding whether to make nonemptiness an explicit hypothesis or simply let the construction extend to the empty space. **Status: adjudicated by the user on 2026-10-27; see final decisions below.**

---

More genuinely uncertain cases may be appended during the remaining whole-corpus comparison. Clear duplicates and mathematically distinct objects are handled in the durable machine-readable cleanup ledger without seeking unnecessary user review.

## Definition of: Affine span / affine hull (two existing searchable headings)

**Proposed Subject:** Geometry / Convex Geometry. **Contexts:** General real affine spaces versus subsets of finite-dimensional R^d; empty versus nonempty subsets.

**Def A — original mathDef, heading "Affine span"** (meaning.mathdef.original.geometry.affine-span; form.mathdef.original.geometry.affine-span.primary):

> For a nonempty subset $S$ of a real affine space, its \emph{affine span} (affine hull) is the smallest affine subspace containing $S$. Equivalently, it consists of all finite affine combinations $\sum_{i=1}^k a_ip_i$ with $p_i\in S$ and $\sum_i a_i=1$. For $S=\varnothing$, some conventions give the empty affine hull.

Source: https://en.wikipedia.org/wiki/Affine_hull (historical original editorial citation; its nonempty convention has not been independently verified).

**Def B — researched "affine hull", finite-combination construction** (meaning.wave2.pop140.affine-hull; first statement of form.meaning.wave2.pop140.affine-hull):

> For an integer d≥1 and a set S⊆ℝ^d, aff(S) is the set of all vectors ∑_{i=1}^{k} αᵢxᵢ with k≥1, xᵢ∈S, αᵢ∈ℝ and ∑_{i=1}^{k} αᵢ=1. In particular aff(∅)=∅.

**Def C — researched "affine hull", intersection construction** (same researched meaning and same formulation ID as Def B; a second statement within the existing text, not a separately indexed form):

> Equivalent formulation: Let d≥1 and S⊆ℝ^d. Define aff(S) as the intersection of all affine-closed subsets C⊆ℝ^d containing S, where affine-closed means containing every finite affine combination of its members; the empty set is affine-closed.

Source for B and C: https://hankyang.seas.harvard.edu/Semidefinite/background.html (provisional_source_paraphrase_not_rechecked_2026_10_26; previously recorded research lead, not passage-verified here).

**Precise mathematical comparison:** For nonempty S⊆ℝ^d, the original smallest-affine-subspace definition and researched finite-affine-combination construction yield the same set. Original A, however, gives a nonempty hypothesis and does not definitively define the hull of ∅, whereas B/C set aff(∅)=∅ by allowing the empty affine-closed set. A permits arbitrary real affine spaces, whereas B/C explicitly use finite-dimensional Euclidean coordinate space.

**Source convention evidence:** Neither source has a documented source-specific nonempty standing-convention assessment. Both remain not_checked. We do not infer that either author positively excluded or admitted the empty case. Future checked_inconclusive status, if documented, would operationally inherit mathDef's latest broad canonical meaning, without asserting author agreement.

**Decision needed:** Should A and B consolidate into one broad, empty-allowed canonical meaning with a note on the usual nonempty affine-subspace formulation, while keeping C as a useful distinct affine-closed-intersection characterization? Or should the general affine-space and finite-dimensional coordinate formulations remain separate contexts?

**Clearly retained:** Both terms as searchable labels, all existing primary/reference URLs with honest evidence labels, and the mathematically distinct intersection construction C.

**Preliminary recommendation:** Prefer the general finite-affine-combination definition including the empty subset, add a convention note for definitions treating affine subspaces as nonempty, and retain C's affine-closed-intersection perspective. Do not discard the general affine-space scope without deliberate translation. **Status: adjudicated by the user on 2026-10-27; see final decisions below.**

---

## Final decisions — explicitly approved by the user 2026-10-27

**These three items are CLOSED, not pending reminders.** User adjudication takes precedence over the preliminary recommendations preserved above for historical comparison. These are mathDef's canonical editorial conventions, not a factual claim that every cited author endorses the same definitions. All previously existing source URLs, citation-verification statuses, original IDs and useful alternative mathematical presentations are preserved in the staged overlay.

1. **Zero divisor — nonzero required.** Canonical: a nonzero element `a` of a commutative ring `R` such that `ab=0` for some nonzero `b∈R`. In particular, **zero is never a zero divisor** under mathDef's convention. Merge the broader original meaning into the researched nonzero-only meaning (rather than displaying near-identical variants), and preserve the original historical ID, sources and the warning that some authors include zero. No Stacks-wide convention is inferred from an unchecked source lead.

2. **Metric space — nonempty underlying set required.** Canonical: a pair `(X,d)` with **`X≠∅`** and the ordinary metric axioms. Fold original empty-allowing A into the researched nonempty-axioms B; retain the compatible induced-topology presentation C as an informative alternative formulation. Keep original ID and citations as provenance. Stage-local dependent wording for *totally bounded metric space*, *separable metric space* and *compact metric space* must no longer assert an empty metric space exists. This change does **not** change the convention for empty topological spaces or the mathDef connectedness predicate.

3. **Affine span and affine hull — one concept, two searchable terms, nonempty input.** The user identifies “affine span” as typical algebraic terminology and “affine hull” as typical analytic terminology, describing the **same** construction. Use a general real affine space `A`, nonempty subset `S⊆A` and finite affine combinations with coefficient sum one; **exclude the empty input from the canonical definition for now**, subject to possible future community correction. Preserve the finite-combination and intersection-of-affine-closed-supersets formulations, with the nonempty hypothesis stated; preserve the original affine-span ID and both existing URLs. The 'Affine span' title must remain searchable as an alias for 'affine hull'. No source-specific nonempty convention is attributed without positive evidence.

**Implementation:** `data/merged_cleanup_decisions.json` records two within-heading meaning mergers and five exact-historical-text user-approved editorial revisions; `data/merged_cleanup_cross_heading_review.json` records the affine cross-heading consolidation; `data/math_definition_conventions.json` dynamically ties all three conventions to the surviving meaning IDs. The edits are stage-only and source provenance remains distinct from verified source evidence.

**Next:** Continue the planned existing-term mathematical cleanup and stage-only validation. These three adjudications require no further user decision unless subsequent research uncovers a genuinely different issue. Global final linking/publication remains separately gated.
