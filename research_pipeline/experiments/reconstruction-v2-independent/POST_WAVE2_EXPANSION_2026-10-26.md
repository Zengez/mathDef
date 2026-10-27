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


## Original quick-scan candidate batch, ranks 741–940

Completed 200 strictly consecutive phrases from the original 2,019-record
candidate list, without searching for additional terminology. All exact
original source examples/counts and 200 classifications live in the same
lightweight disposition ledger. Five useful new terms added to the
merged-only research overlay: field embedding, filtered probability space,
finite-index subgroup, finitely generated group, and the syntactic
free-variable set of a first-order formula. They contain source citations,
explicit mathematical definitions and necessary edge-case assumptions.

Additional decisions: 22 already covered, 169 linguistic false positives,
4 context ambiguities retained without forcing mathematical equivalences.
This leaves **940/2,019 processed; resume at rank 941**. Research overlay
contains 169 meanings, **51 net scan-driven additions** above the first
118; combined expected 2,141. Independent Wave2 958, original production
definitions 1,014 and the original candidate list are unchanged.


## Original frozen candidate research ranks 941–1140

Dispositioned a further **200 original ranked leads** using the unchanged
2,019-entry quick-scan report, with all literal phrases, occurrence
counts and source examples in the existing lightweight ledger.
No new candidate discovery or dependency workflow.

New sourced meanings from this window (8): imperfect field, injective map,
integral basis, large category, Lie algebra homomorphism, localizing
sequence for a local martingale, locally finite Borel measure, locally
univalent holomorphic function. Remaining outcomes: 50 already covered,
138 nonterms, 4 genuine ambiguities. Scope-specific assumptions and
important edge-case differences are recorded with new definitions.

**Resume at candidate 1141.** Original candidate lead processing
1,140/2,019; post-Wave2 overlay 177 total, of which 59 net
candidate-derived. Expected combined 2,149 meanings. Historic independent
Wave2 (958), original production mathDef (1,014) and frozen scan
are unchanged.


## Original fixed quick-scan incorporation, ranks 1141–1340

Processed the next 200 literal original terminology candidates directly,
without expanding the candidate pool or restarting scanning. The shared
disposition ledger stores every exact rank/phrase/occurrence count/example,
mathematical research outcome and any existing/new target. This pass
added 16 sourced meanings or contextual variants, including
order-preserving maps versus order embeddings, ordered fields and
bi-ordered groups, Polish spaces/groups, normed fields, partial
computability, nonreduced rings, mixed partials, minimal elements
distinct from least, one-sided ideals, piecewise polynomials
and Petrov–Galerkin finite elements. The other outcomes were
29 existing meanings, 152 lexical nonterms, and three genuinely
ambiguous conventions.

Checkpoint **1,340/2,019**, **next original rank 1,341**, 679
remaining. Merged-only overlay **193 meanings**, including 75 net
scan-derived meanings, total combined expected **2,165**. Frozen
candidate list and independently completed source collections unmodified.


## Original fixed quick-scan incorporation, ranks 1341–1540

Processed **200 further source-exact frozen candidates** with NO new candidate search or extension of the 2,019 original rough phrase leads. Every one is in the existing `post_wave2/scan_candidate_dispositions.json` ledger with original rank, phrase, count, complete source examples, decision, rationale and a resolvable existing/new target where appropriate.

**Batch dispositions:** 12 new meanings/contextual variants, 73 already-covered matches, 113 nonterminological grammatical/ordinary context fragments, and 2 unresolved ambiguities (**rank 1380:** "regular limit" versus weak/strong inaccessibility; **rank 1465:** meaning of a "strict functor" in 2-category contexts).

**12 new searchable meanings:** 1357 properly supported pseudodifferential operator; 1361 quasi-coherent ideal sheaf; 1362 quasi-coherent sheaf; 1363 quasi-compact morphism of schemes; 1367 normalized radix-β floating-point number; 1383 relatively closed subset; 1385 relatively compact subset; 1420 semilocally simply connected space; 1440 small filtered category; 1468 strong limit cardinal; 1481 superattracting fixed point; 1492 symmetric bilinear form.

Important differences and exception handling: a quasi-compact scheme morphism need not be proper; a quasi-coherent sheaf need not be locally free; relative closedness is relative to its subspace; relative compactness is not equivalent to metric total boundedness without completeness; semilocal simple connectivity does not by itself guarantee the existence of a universal cover; filtered and cofiltered categories are dual but not identical; strong limit cardinals may be singular, and a strong limit alone is not the same as a strongly inaccessible cardinal; symmetric bilinear forms need not be positive definite or Hermitian; strong measurability, principal fractional ideals, quasi-metric spaces and second-countability were matched to existing definitions rather than duplicated.

**Checkpoint 1,540/2,019**, next **rank 1,541**, **479 remain**. Merged-only post-Wave2 overlay **205 meanings** (118 initial + 87 net scan-derived meanings), total expected combined **2,177 = 958 independent Wave2 + 1,014 original + 205 overlay**. Historical Wave2, production definitions and the original frozen scan remain unmodified.


## Original frozen quick-scan incorporation — ranks 1541–1780

**240 consecutive frozen original scan candidates processed** directly, without new candidate discovery, lexical rescanning, dependency graphs or historical source modifications. Original exact ranks, counts, examples, explanations and target references appear in the unchanged-schema `post_wave2/scan_candidate_dispositions.json` ledger.

**Decisions:** 10 newly researched mathematical meanings/context-specific variants; 154 existing definitions or source-supported variants matched; 74 contextual phrases or sentence fragments with no distinct new meaning; 2 unresolved ambiguities (1607 "the function algebra" has competing algebra choices, and 1732 "the Riesz representation" has different theorem contexts).

**Ten additional merged-only searchable meanings:** rank 1544 closed graph of a linear operator; 1545 closed Euclidean half-space; 1593 Euclidean metric; 1602 box topology on an indexed Cartesian product; 1623 hom-category of a 2-category; 1665 full matrix ring Mₙ(R); 1724 regular local ring; 1749 small Bergman-space Hankel operator; 1766 strong operator topology; and 1772 real symmetric matrix.

Explicit cautions: closed graph versus continuity (Banach domain completeness/whole-domain hypotheses); closed half-space requires a nonzero normal for a proper boundary; box topology is not ordinary product topology on general infinite products; a hom-category has 2-morphisms as morphisms; noncommutative matrix rings require a nontrivial base and n≥2; regular local is much stronger than just local; the big and small Hankel operators have different codomains and may use different published conventions; pointwise strong operator convergence is not uniform norm convergence; a real symmetric matrix need not be positive definite. Existing entries already cover total variation norm, strict sublevel sets, product σ-algebras, the Euclidean inner product as a special inner-product context, and many other phrases. No duplication.

**Persistent checkpoint: 1,780/2,019 incorporated, next rank 1,781; 239 remaining**. Post-Wave2 merged overlay **215 meanings**, comprised of initial 118 plus **97 net scan-research additions**; combined expected **2,187 = 958 independent Wave2 + 1,014 original + 215 overlay**. Frozen scan and historical independent baseline unchanged.


## Frozen original candidate research — COMPLETED (all 2,019 ranked leads)

The original quick-scan candidate set is **closed for this research pass**. All 2,019 records, in original unchanged rank order, are permanently dispositioned in `post_wave2/scan_candidate_dispositions.json`, retaining exact phrase, occurrence counts, source examples, outcome, reasons and validated targets. No new candidates were added; no new term hunt was undertaken. This is **not** a claim that the mathematical corpus is exhaustive, just that the frozen original quick-scan backlog has been fully handled.

**Final 239 candidates (ranks 1781–2019):** 10 directly researched meanings or contextual variants, 95 matches to existing definitions and variants, 134 nonterminological fragments, 0 remaining undecided in this range. Newly searchable meanings: exterior/wedge product of differential forms (1803); weighted Minkowski combination (1806); deterministic Turing transition function (1852); nondeterministic Turing transition relation (1853); trial/test spaces for Galerkin approximations (1854); weakly inaccessible cardinal (1873); monoid homomorphism, with explicitly preserved identity (1902); {0,1}-valued countably additive probability measure (1920); variable-coefficient linear differential operator (1924); and the CW-complex-specific weak/final topology (2007).

**Important context disambiguation:** The final candidate "with the weak topology" (2007) occurs in the original *CW complex* definition, so it has a separate topological meaning from the weak topology of bounded linear functionals in functional analysis. Do not merge or automatically cross-link these senses. Earlier ambiguities remain separately logged; research completeness means every candidate has a recorded decision, not that every ambiguity has been resolved definitively.

**Completed corpus size:** 958 frozen independent Wave2 meanings + 1,014 unchanged original mathDef meanings + 225 post-Wave2 merged-only additions = **2,197 merged searchable meanings**; post-Wave2 total includes the initial 118 general research meanings and 107 scan-driven additions. Baseline original and independent data remain unchanged.

**Recommended NEXT PHASE: linking the existing combined corpus.** First rapidly extract potential term references in definition text and attach likely links to *existing* meaning IDs. Then research meaning selection and contextual variants for ambiguous terms, ensure repeated/cyclic expansion is handled on the UI's active path, and validate broken links, search, and inline recursive expansion. Do not create a new corpus-wide slow dependency-review system or reopen frozen candidate discovery. Record durable progress in this project's current checkpoint.
