# Post-Wave2 merged-only research expansion

The independent Wave 2 reconstruction finished on 2026-10-26 at **958 meanings**
and **1,511 curated relations**. Its source records and
`direct_research/terms.json` remain unchanged.

The original mathDef definitions were subsequently incorporated in the separate
`/reconstruction/merged/` searchable reference, and the deliberately rough first
terminology scan was completed: 363 direct Wave 2 definitions plus 1,014 original
definitions (5 additional original variants), yielding 2,019 *unverified phrase
leads* and 473 known-term mention patterns.

**Add subsequent researched meanings here**, in `terms.json`, not to the frozen
independent Wave 2 content and not to the production `definitions/` source files.
The combined site build applies this file *after* the original-plus-independent
merger, while saving the original rapid scan against its initial input scope.
The old dependency graphs, stage gates and 418-lead queue are retired.

For each next useful lead, compare actual existing meanings, clarify mathematical
scope and competing conventions, cite a source, and directly add the meaning and
links to this file. New leads encountered along the way may be left for future
work; do not recursively process them as a publication prerequisite. Batch size
and review depth should remain proportional to the goal of visible, useful
content. Avoid blanket equivalence assertions based on matching labels.

## First new batch (2026-10-26)

Four researched meanings (with four source locator records and six links):
unital ring; unital ring homomorphism; locally small category; nonnegatively
graded ring (specifically nonnegative integer grading under the cited Stacks
convention). These were selected from substantive vocabulary noticed in
the initial 363-definition sample scan, not from a mandatory 2,019-item queue.
Their labels and any established aliases remain searchable in the combined view.

Run `python -m research_pipeline.adapters.mathdef.preview_site
--site-root /tmp/mathdef-merged-preview` and
`python -m unittest research_pipeline.tests.test_original_merge
research_pipeline.tests.test_direct_additions -v` to check local rendering.

## Second batch (2026-10-26)

Four more direct researched meanings: cofiltered category, real affine space,
generating set of a left module, and locally finite Borel measure. Each has a
checked direct source locator and explicit convention/edge-case notes; their
links point only to existing independently researched meanings. The combined
reference should now show **1,980 meanings**, comprising 958 independent
Wave 2 + 1,014 original mathDef + **8 post-Wave2 additions**. The fast scan's
original 2,019 rough leads and 473 known-term mentions remain the starting
discovery snapshot rather than mandatory approval tasks.

## Third direct research batch (2026-10-26)

Twelve mathematical meanings added after checking the original, screened
independent, direct-research and prior post-Wave2 terms for likely duplicates:
chain map; injective left module; basis for a topology; subbasis for a
topology; final topology; topological support of a function; finitely
supported function (algebraic); partial function; affine hyperplane;
formal power series ring in one variable; bounded subset of a metric space;
and upper set of a partially ordered set.

The distinction between **topological support (closed nonzero locus)**
and **algebraic finite support (nonzero locus, no closure)** is explicit.
Likewise the formal ring `R[[T]]` is not confused with analytically
convergent power series, and final topology is not conflated with initial
topology. Nonempty/nontrivial conditions are only imposed when needed
and recorded in each meaning's assumptions.

These 12 entries contain source records checked against Stacks Project,
Encyclopedia of Mathematics, university topology notes, Wolfram MathWorld
and a mathematics handbook. Citations are **assistant-checked drafts,
not independent formal peer review**. Total subsequent expansion is
20 meanings. Expected merged count: 1,992; independent Wave 2: still 958.
The original 2,019-lead rough scan remains unchanged.

Do not restart a graph-building, global citation audit or per-term staged
workflow. Continue directly with useful substantive meanings in this file.
