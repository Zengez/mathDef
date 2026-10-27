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


## Fifth expansion batch — 13 more direct meanings

The combined-only follow-up reference gained 13 researched meanings:
fully faithful functor, essential image, torsion element/module/torsion-free
module over an integral domain, injective resolution, symmetric algebra,
exterior algebra, supporting hyperplane, separable metric space,
specialization preorder, contractible chain complex and affine map.
All source locators and edge-case assumptions are attached to the actual
meaning entries. References include Stacks Project Sections 4.2, 10.13,
13.18 and 15.22, Encyclopedia of Mathematics, nLab and university notes.

**Snapshot protection:** The post-Wave2 overlay is now 47 meanings.
Independent Wave2 remains exactly 958 and original production remains
1,014 definitions; the combined view should contain 2,019 meanings upon
successful rendering. The first rapid candidate report happened to produce
2,019 rough *phrase leads*. Those **two equal numbers count unrelated
objects**; do not conflate them, and do not infer candidate completion.

Maintain efficient direct content work, not candidate-approval gates.


## Sixth expansion batch — 18 mathematical meanings, no stage gate

Another 18 source-attributed meanings have been added directly to the
post-completion combined-only `post_wave2/terms.json` overlay. They address
module length/composition series/socle; several distinct topological
compactness and covering properties; Baire category and equicontinuity; and
convex geometric interior, extremality, exposed faces and barycentric coordinates.

This research specifically avoids a major potential error: **countably
compact** means every countable open cover has a finite subcover, whereas
**Lindelöf** means every arbitrary open cover has a countable subcover.
Neither should be conflated with sequential compactness outside metric
spaces. The empty cases, Hausdorff convention, module zero-length case and
non-exposed faces are recorded explicitly in each entry.

Total after this content batch: **65** post-Wave2 meanings and expected
**2,037** combined meanings, while the original 958-meaning independently
reconstructed Wave2 and original 1,014-entry corpus are preserved. Initial
scan still has 2,019 noisy new-phrase leads and 473 known-title patterns.
CI validation and deployment determine whether these expected numbers
are published; never claim publication before successful Pages delivery.


## Seventh expansion batch — 14 group and algebra definitions

The combined-only overlay gained 14 researched terms: free group, normal
closure, presentation by generators/relations, conjugacy class,
centralizer, group center, group commutator, derived subgroup,
abelianization, semidirect product, group ring, field-coefficient
group algebra, characteristic subgroup, and normalizer.

Definitions include actual mathematical statements and links in the
post-Wave2 JSON content. Checked mathematical references and honest
scope assumptions are stored per term. Important differences include
normality versus characteristic status, normalizers versus centralizers,
conjugacy under inner automorphisms, universal abelian quotient versus
commutator element, and semidirect versus direct products.

Expected counts after validation: **2,051 contextual meanings** and
**79 post-Wave2 researched additions**; independent Wave2 remains 958
and original mathDef 1,014 source definitions. The earlier fast scan
reports 2,019 rough leads, unrelated to the current meanings count.
The workflow stays immediate research, content and usable links, with
no mandatory review queue or dependency graph.


## Eighth expansion batch — 20 foundational topology meanings

Twenty new definitions were written directly into the post-Wave2 combined-only
JSON overlay: six separation/conventional regularity variants, metrizability,
five filter/neighbor concepts, two net concepts, one-point compactification,
two partition-of-unity variants, compact-open and box topologies, and the
Sierpiński space.

Source passages were retrieved directly from mathematical references and
recorded with `source_passage_retrieved_2026-10-26`, rather than relying
solely on suggested citations. Each record contains context, exact
mathematical conditions, edge cases and links to existing or newly added
meanings. Special care was taken with T₃/T₄ conventions, proper filters,
nonempty directed index sets, topological support, and one-point Hausdorff
compactification.

Post-Wave2 additions after this batch total **99**. Expected combined
catalog = 958 independent + 1,014 original + 99 post-Wave2 = **2,071**
meanings. Counts should be treated as draft expectations until verified by
CI and published Pages workflow; they are not claims of formal proof-level
or human citation certification. The initial 2,019 tentative phrase scan
was already completed and remains a discovery resource, not a queue.


## Ninth expansion batch — 19 category-theory definitions

Direct content batch adds 19 missing categorical meanings in the merged
post-Wave2 research overlay. The definitions intentionally connect
subcategory/fullness/wide/repletion and skeletal/skeleton variants to
identity/constant/endofunctor constructions, coslice and arrow
categories, right adjoints and counits, and the structure of monads,
comonads, algebras, Eilenberg–Moore and Kleisli categories.

Sources were retrieved from Encyclopedia of Mathematics and nLab.
The mathematical assumptions and source-status records are attached
to each definition rather than to a mandatory separate review packet.
Especially important edge-case discipline: nontrivial automorphisms
are allowed in a skeletal category; construction of skeletons may
invoke choice; monads require η:Id→T and μ:T²→T with both identities;
and for a contravariant presheaf F:C^op→Set the elements-category arrow
(c,x)→(d,y) must satisfy F(f)(y)=x.

Checkpoint expects **118** post-completion researched meanings and
**2,090** meanings in combined catalog (958 + 1,014 + 118). The
historical scan's 2,019 tentative phrase leads remains separate and
unresolved leads are not a completion gate. CI and Pages publish
runs provide actual build/deployment confirmation.


## Owner-directed correction: original scan candidates are current input

The owner clarified that the quick-scan TERMINOLOGY leads — not arbitrary new
terms found by an independent search — must now be researched and incorporated.
The prior seven-to-nine post-Wave2 direct research batches were useful but
drifted into unrelated gap hunting. That stops here. The actual canonical
initial fast-scan result remains frozen at **2,019 phrases** and **473 known
title mentions**.

First processing pass records exactly the original ranked scan candidates
**1–60** with their source-document examples in the concise file
`post_wave2/scan_candidate_dispositions.json`. We differentiated existing
definitions (22), already-covered variants (1), contextual ambiguity (2),
grammatical false positives (30), four new terms and one multi-variant term.
Seven meanings were researched and inserted: real and complex vector spaces,
measure space, three conventions for Borel measure, and compact metric space.
The three Borel-measure senses follow the explicitly differentiated source
conventions: measure on Borel σ-algebra, finite on compact sets, and Borel
outer measure. These are NOT mathematical synonyms.

Persistent next pointer: **scan rank 61**, using actual candidate records.
Further active term hunting is deferred until explicitly designated a
separate collection-building phase. Completed independent Wave2 remains 958
meanings and original mathDef source 1,014 definitions; expected current
combined count after validation is 2,097 meanings. This is an
assistant-reviewed, source-attributed content merge, not a peer-certified audit.


## Scan-driven follow-up ranks 61–100 (2026-10-26)

Processed an additional 40 ranked phrases from the original 2,019-lead
report. The real scan-ranked examples and decisions were APPENDED to the
existing ledger rather than creating any replacement candidate list.
Added three genuinely useful meanings for ranks 63, 70 and 82, with
explicit research sources. Existing uses and malformed text fragments are
mapped or discarded, while ambiguous Euclidean-space and first-return-map
contexts were noted without silently choosing a potentially incorrect
sense.

**First 100 scan candidates now processed.** Ten researched meanings
incorporated (including three distinct Borel measure contexts); combined-only
overlay totals **128** new post-Wave2 meanings. Next candidate is rank
**101**, not a new term-crawling pass. All 958 independent Wave2 meanings,
1,014 original mathDef definitions, and the full frozen original scan
remain unaffected.


## Original quick-scan research and disposition, ranks 101–140

This batch used only literal candidates from the original frozen 2,019-phrase
scan, with exact example origins and IDs carried into the existing
`post_wave2/scan_candidate_dispositions.json`. Decisions: 8 new, 18 already
covered, 14 nonterminological phrases. No additional candidates were
harvested. Eight source-attributed, mathematically scoped new meanings were
added to the **merged-only** overlay: absolute convergence for ordinary
Dirichlet series, R-algebra homomorphism, norm-closed linear subspace,
compact Hausdorff space, complex-valued function, real-C¹ complex-valued
function, positive-radius convergent complex power series, and at-most-
countable subset.

Definitions explicitly distinguish algebra-map unital conventions,
norm-closed versus topologically closed subspaces, real versus complex
differentiability, positive radius versus mere center convergence, and
finite-or-countably-infinite versus denumerable-only terminology. Sources
are saved for each meaning; no blanket claims of source certification.

**Checkpoint: 140/2,019 original scan leads processed; next rank 141.**
Merged-only overlay has 136 meanings, expected total merged content 2,108
(958+1,014+136). The independent Wave 2 and original source files remain
unchanged; original scan content/count is not altered.


## Original quick-scan candidates, ranks 141–180

Processed exactly the next original 40 leads, reusing the **same** frozen
original scan and mapping literal example/source IDs in the same disposition
ledger. Four genuinely new concepts and one meaning variant were added:
finite-dimensional Euclidean space, finite-dimensional vector space,
finite field extension, Hausdorff second-countable space, and an
isolated-point-of-subset variant linked to the existing isolated point
of the whole space. Every meaning includes mathematical context,
explicit assumptions, source references, and researched scope.

Recorded 15 already-covered leads, 19 nonterminological fragments and one
contextual first-return-map ambiguity. No unrelated terminology search,
dependency-graph gate or exhaustive audit. **180 / 2,019** old candidates
processed and **23** new sourced meanings incorporated from them.
New post-Wave2 overlay total **141**; expected merged total **2,113**.
Persistent next candidate rank **181**; independent 958 and original 1,014
remain unchanged.


## Original frozen quick-scan ranks 181–220

Research directly incorporated four mathematical meanings from actual scan
candidates (open interval, Hilbert orthonormal basis, morphism of sheaves
of sets, sub-σ-algebra) with exact context, explicit assumptions, research
sources, and links in the post-Wave2 merged-only overlay. The same persistent
ledger now contains **220** literal source-matched dispositions; this
40-candidate batch yielded 23 existing, 11 lexical nonterm, 1 ambiguous,
1 existing multiple-variant and 4 new dispositions.

**Next original candidate rank 221**, source collection unchanged at
2,019 leads, overlay now **145** sourced meanings, expected combined
**2,117** meanings. Independent Wave 2 remains 958 meanings and original
production source remains 1,014 definitions.


## Original frozen scan candidate research, ranks 221–340

Processed **120** original quick-scan candidates using only the already
frozen, ranked 2,019-lead scan. Seven mathematically scoped meanings were
added to the merged-only overlay: free abelian group, spherical chordal
metric, zero polynomial, zero ring, Banach-valued simple measurable
function, affine open subscheme, and complex-analytic subset. Definitions
have source attribution, assumptions and context-sensitive distinctions.

Dispositioned 33 existing senses, 78 lexical nonterms, one ambiguous
identically-infinity case, and one existing-multiple-variant empty-product
case, each with verbatim original scan phrase/count/example identifiers.

Persistent checkpoint: **340/2,019 processed**, next **341**. Scan-derived
additions total **34** and merged-only post-Wave2 overlay is **152**
meanings; expected merged content = 958+1,014+152 = **2,124**.
No new candidates collected and no edits to frozen production originals
or independent Wave2 snapshot.


## Original scan candidates 341–540: one larger research pass

Processed **200 consecutive frozen original quick-scan phrase leads**,
without adding candidates or starting a new discovery sweep. Research
decisions: 6 genuinely new mathematical meanings, 36 already covered,
156 linguistic false positives, 2 genuine contextual ambiguities. The
six new meanings are associative F-algebra, bounded continuous
real-valued function, Cantor space, cofinal subset of a poset, complete
discrete valuation ring, and completely multiplicative arithmetic
function. All new meanings have source attribution, explicit assumptions
and mathematical distinctions; all candidate examples/dispositions are
in the existing lightweight ledger.

Also corrected a genuine historical duplicate: rank 318's
complex-analytic-subset meaning coincided with existing original
`definitions/scv/complex-analytic-subset.tex`. Its additional source
rationale survives in ledger reconciliation metadata; redundant overlay
content was removed. Thus net scan-derived additions after this batch
are **39** rather than 40.

**Persistent next rank 541**; **540/2,019 candidate leads processed**.
Overlay = **157** meanings, expected combined total **2,129**.
Historical independent Wave2 958 and original mathDef 1,014 remain frozen.


## Source-exact original quick-scan incorporation, ranks 541–740

Resolved 200 additional literal candidate records from the already
collected frozen original scan, without collecting a new vocabulary
candidate. Seven mathematical meanings were added directly to the
merged-only overlay: complex Euclidean space, Hermitian matrix,
computable rational sequence, constant map, conull measurable set,
cohomologically graded differential algebra, and discrete topological
subset. Sources, definitions, edge-case conventions and links are
stored in the overlay; the source-exact dispositions and target
mappings remain in the original established ledger.

Additional dispositions: 29 existing, 161 lexical nonterms and
3 genuine ambiguities. The mathematical decisions keep distinct
complex versus real scalar fields, Hermitian versus positive-definite,
computability of a sequence versus of its limit, measure conullness
versus arbitrary infinite-mass equality, graded signs and square-zero
differentials, and discrete versus closed discrete topological subsets.

**Next original rank: 741.** 740/2,019 candidates reviewed.
Overlay total 164; expected merged total 2,136 meanings.
No new scan or candidate harvesting. Historic Wave2 958 and
original production definitions 1,014 remain unmodified.
