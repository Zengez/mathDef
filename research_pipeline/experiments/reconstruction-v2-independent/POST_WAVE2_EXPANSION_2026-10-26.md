# Post-Wave2 expansion — first content batch, 2026-10-26

**Purpose.** Continue after the completed original-inclusive merge and rapid
terminology scan, with real searchable definitions rather than another
dependency-graph process.

**Frozen checkpoints.** Wave 1 is preserved; independent Wave 2 remains 958
meanings / 1,002 formulations / 1,511 relations. The original-inclusive
combined baseline was 1,972 meanings in 1,831 headings from the independent
958 plus original 1,014 definitions. The completed scanner input remains
363 direct definitions and 1,014 original definitions (+5 original variants),
with its initial 2,019 loose new phrases and 473 known mentions; its scan is
deliberately unchanged by this additional admission.

**This batch.** Add four source-attributed draft meanings exclusively to
`post_wave2/terms.json` and the combined searchable site:
- `unital ring`: associative ring with identity, not assuming commutativity,
  zero-ring convention explicit. Source: Encyclopedia of Mathematics.
- `unital ring homomorphism`: preserves the multiplicative identity, alongside
  addition and multiplication. Source: Encyclopedia of Mathematics.
- `locally small category`: each Hom collection is a set, object collection
  need not be small. Source: nLab.
- `nonnegatively graded ring`: nonnegative-integer grading of a commutative
  unital ring, rather than conflating it with arbitrary group gradings.
  Source: Stacks Project tag 00JL.

Each record stores scope, source-verification status and existing-target
relationships. The combined view should now have **1,976 meanings**; independent
Wave 2 and original production mathematical text remain untouched. Exact
search-heading count comes from the site build; it is not assumed all additions
create new headings.

**Method/next:** Favor correct direct content with realistic provenance and
limited candidate checking. Later batches may address further worthwhile rough
leads from either source corpus, detect genuine variants/synonyms and add
contextually sensible links. Do not require full resolution of the 2,019
unverified phrases before publication; remove false positives opportunistically
rather than turning them into audit packets. Verify preview/build CI before merge.

## Continued research: second content batch (same day)

Four more scan-motivated, source-checked draft meanings are appended to the
existing merged-only `post_wave2/terms.json`:

- **Cofiltered category:** all three indexing-category axioms, including
  equalization of parallel arrows. Source: Stacks Project Definition 4.20.1.
- **Real affine space:** nonempty torsor for the additive group of a real vector
  space, with no distinguished origin. Source: Encyclopedia of Mathematics,
  affine-space definition specialized to the real field.
- **Generating set of a left module:** finite linear-combination criterion,
  including the empty-generator/zero-module edge case. Source: Encyclopedia
  of Mathematics, module generators.
- **Locally finite Borel measure:** finite measure on an open neighborhood
  of each point, explicitly NOT equating local finiteness with full Radon
  regularity. Sources: nLab, Princeton MAT425 notes.

The expansion file now contains **8 researched meanings** in total, with
source-checked citations and direct, nonmandatory contextual links. The merged
reference is expected to contain **1,980 meanings** after CI. The independent
Wave2 snapshot stays **958** and its completion record remains closed.

## Third expansion batch — further original-inclusive vocabulary

Twelve directly researched concepts from the previously identified
mathematical vocabulary are now included in `post_wave2/terms.json`.
New coverage spans homological algebra, module theory, general topology,
topological and algebraic function support, partial functions, affine
geometry, commutative algebra, metric geometry and order theory.

**Boundary discipline.** This is the post-Wave2 *combined* reference only.
New research is deliberately not written into the independent finished
958-meaning Wave2 or the original `definitions/*.tex` files.
Context-sensitive differences (topological versus algebraic support;
analytic versus formal series; initial versus final topology; partial
versus total functions) have been preserved rather than silently
merged as equivalent. The added source locators and conventions are in
the actual definition records, not separate gate/checklist paperwork.

The post-Wave2 research overlay totals **20 meanings**, predicting
**1,992 combined meanings** (958 independent + 1,014 original + 20
post-Wave2); the exact number of term headings is emitted by CI. Preserve
the 2,019 original rough scan leads and 473 known mentions without
claiming they are all mathematical terms. More definitions can be
researched and added directly in further batches.


## Fourth expansion batch — 14 directly researched new meanings

Fourteen meanings with explicit assumptions and source locators were added
directly to the `post_wave2/terms.json` combined-only overlay. The research
concentrated on homological algebra, modules, category theory, measure
theory, general topology and affine geometry. All 14 are new contextual
meanings under distinct headings after comparing the independent screened
and direct catalogs, the original production file list and previous
post-Wave2 additions.

Highlights include (1) injective hull / essential submodule interplay,
(2) degree +1 chain homotopy / acyclic complexes / degree-raising cochain
maps, (3) full subcategory versus essentially surjective functor,
(4) finite epsilon-net total boundedness, (5) compact support as
topological closure of the nonzero locus, (6) almost-everywhere convergence,
(7) affinely independent points, and (8) arbitrary-intersection
Alexandrov topology, which is NOT metric-curvature Alexandrov geometry.

Sources include checked Stacks Project definitions (Sections 4.2, 12.13,
47.2, 47.5), Encyclopedia of Mathematics entries, mathematical lecture
notes and a small number of explicitly identified Wikipedia definitions.
Retain their precise provenance statuses. These are assistant-reviewed
drafts, not human mathematical certification.

Combined counts expected after CI: **2,006 meanings**, while the independent
958-meaning Wave 2 and original 1,014-definition corpus remain untouched;
the post-Wave2 overlay has **34** meanings. This expansion is NOT
a completion claim for the 2,019 intentionally noisy tentative scan leads.
