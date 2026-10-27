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


## Fourth research batch (2026-10-26)

Fourteen additional meanings added directly from research into mathematical
gaps, without a dependency graph or mandatory clearing of lexical leads:

- Homological algebra: chain homotopy, acyclic chain complex and cochain map
- Module theory: injective hull, essential submodule, cyclic left module,
  semisimple left module
- Category theory: full subcategory and essentially surjective functor
- Topology and analysis: totally bounded metric space, compactly supported
  function, Alexandrov topological space
- Measure theory: almost-everywhere convergence of functions
- Affine geometry: affine independence of a finite family

The precise conventions distinguish homological and cohomological grading,
essential versus arbitrary embeddings, full versus essentially surjective
functors, bounded versus totally bounded metric spaces, and Alexandrov
topological spaces versus curvature-bounded Alexandrov metric spaces.
Source locators were checked against the Stacks Project, Encyclopedia of
Mathematics, University of Pennsylvania affine geometry notes and
explicitly designated Wikipedia definition entries. The mathematical
content is **assistant-reviewed research, not formally peer certified**.

Post-Wave2 additions now total **34** source-attributed meanings. The
expected merged-only site contains **2,006 meanings**, consisting of 958
independent Wave 2 + 1,014 original mathDef + 34 post-completion.
Do not revise the 958-meaning completion inventory or re-run the 418-lead
queue. The first scan's 2,019 tentative new phrases remains a discovery
snapshot; it is not an audit gate.


## Fifth direct research batch (2026-10-26)

Thirteen more mathematical meanings added after initial original/independent/
combined duplicate checks:

- Category theory: fully faithful functor; essential image of a functor
- Algebra: torsion element, torsion module and torsion-free module over an
  integral domain; symmetric and exterior algebras of modules
- Homological algebra: injective resolution; contractible chain complex
- Geometry: supporting hyperplane and affine map (not necessarily bijective)
- General topology: separable metric space; specialization preorder

The torsion definitions use an explicitly stated **commutative integral
domain** and distinguish element torsion from the Tor derived functor.
The exterior algebra is defined by `m∧m=0`, not merely skew-commutativity,
so its statement remains valid in characteristic two. The specialization
preorder's orientation is stated to avoid conflicting conventions.

Source references were checked against the Stacks Project, Encyclopedia
of Mathematics, nLab and university affine transformation notes. Several
formalizations are transparent specializations or generalizations of their
source passages; they are **assistant-reviewed**, not peer-certified.

Total post-Wave2 additions: **47 meanings** in the combined-only
`post_wave2/terms.json`. Expected combined reference: **2,019 meanings**
(958 independent Wave2 + 1,014 original mathDef + 47 post-Wave2). This
coincidental equality to the **2,019 tentative phrase leads** from the
earlier scan does not imply those leads were all researched or resolved.
Preserve the 958-meaning frozen independent snapshot and initial scan.


## Sixth direct research batch (2026-10-26)

Eighteen new contextual mathematical meanings researched directly into the
combined-only reference, retaining the independently completed Wave2 at 958:

- Algebra: finite-length module, composition series of a module and module socle.
- Covering properties and general topology: Lindelöf, σ-compact,
  countably compact, sequentially compact and paracompact spaces, with a
  separate definition of a locally finite family of subsets.
- Baire category and analysis: meagre, comeagre, Baire topological spaces,
  equicontinuity of a family of maps between metric spaces.
- Convex geometry: relative interior, extreme point, face, exposed face and
  barycentric coordinates relative to an affine frame.

Mathematical scope and comparisons are included in the definitions:
countable-cover vs countable-subcover vs convergent-subsequence properties;
the Hausdorff convention for paracompactness; empty/zero-module cases;
meagre vs measure-zero; exposed vs general convex faces; Euclidean rather
than infinite-dimensional assertions about relative interior; and unique
barycentric coordinates only within an independent affine frame.

Primary or directly checked references: Stacks Project Section 10.52,
Encyclopedia of Mathematics (Socle, Compactness, Lindelöf, Paracompact,
Baire/Category, Equicontinuity, Barycentric Coordinates), the convex-geometry
reference chapter hosted by Harvard, and PlanetMath's face definition.
All source locators and local assumptions are inside individual records.
These are source-attributed, assistant-reviewed drafts, not human certification.

**Checkpoint:** the post-Wave2-only overlay now holds **65 meanings** (47
earlier + 18 newly researched). The combined reference is expected to have
**2,037 contextual meanings** (958 independent Wave2 + 1,014 original mathDef +
65 post-completion). The 2,019 earlier loose scan leads are neither fully
checked nor a required queue, and they remain unchanged by this batch.


## Seventh research batch (2026-10-26)

Fourteen directly researched group theory and algebraic meanings added
exclusively to the post-completion combined reference:

- Free group on a set, normal closure, group presentation
- Conjugacy class, centralizer, center and normalizer
- Element commutator, derived (commutator) subgroup, abelianization
- Semidirect product, group ring, group algebra over a field
- Characteristic subgroup

The batch is mathematically connected: a group presentation is a quotient
of a free group by a normal closure; abelianization is a quotient by the
derived subgroup; semidirect products require a specified action; the group
ring generalizes group algebras from field to commutative-ring coefficients.
The element commutator convention is explicitly `ghg⁻¹h⁻¹`.
The source role for group rings is labeled an independently reasoned
generalization of the directly checked group-algebra source, not a verbatim
claim. Empty-generator, zero-coefficient-ring and infinite-group finite-
support conventions are explicit.

References checked include Encyclopedia of Mathematics, PlanetMath,
LMFDB's reviewed semidirect-product entry, and mathematics lecture notes.
These entries remain assistant-reviewed drafts, not peer certified.

The post-Wave2 merged-only overlay now holds **79** meanings (65 prior + 14
new) for an expected **2,051** combined meanings. The independent 958-meaning
Wave2, 1,014 original definitions and first rough 2,019-lead scan stay
untouched. Continue by adding directly useful mathematical content,
never restarting old dependency graphs, staging, or exhaustive gates.


## Eighth direct research batch (2026-10-26)

Twenty new mathematical meanings were added directly to the **combined-only**
post-Wave2 research overlay, after title checks against the original corpus,
958 independent Wave2 entries and 79 prior post-Wave2 meanings.

- Separation axioms: T₀, T₁, regular (without T₁), normal (without T₁),
  completely regular (without T₁), and Tychonoff (completely regular plus T₁)
- Metrizable topological space
- Filters: proper filter, filter base, neighborhood filter, neighborhood base,
  and convergence of a filter
- Nets: directed-index net and Moore–Smith convergence
- One-point compactification of a locally compact, noncompact Hausdorff space
- Partition of unity and the stronger subordinate-to-cover variant
- Compact-open topology, box product topology and Sierpiński topological space

References were retrieved directly from Encyclopedia of Mathematics
(separation, filters, nets, neighborhoods, compactification and paracompactness),
Wolfram MathWorld (separation and function-space topology), ProofWiki
(filter convergence), PlanetMath (box topology) and PLS Lab (Sierpiński).
The individual source records identify the retrieved passages; mathematical
statements are still assistant-reviewed drafts, not independent peer review.

**Important conventions:** Regular/normal/completely regular mean WITHOUT
T₁ unless explicitly included; Tychonoff includes T₁. Filters are proper,
so their underlying set is nonempty. Nets have nonempty directed preorders.
One-point compactification is restricted to the locally compact noncompact
Hausdorff case. A subordinate partition of unity has supports inside the
specified open cover, not merely its nonzero loci.

Expected results: **99** researched post-Wave2 meanings (79 prior + 20 here),
**2,071** combined contextual meanings. Preserve the frozen independent
958-meaning Wave2, original 1,014-definition corpus and historical initial
2,019 rough phrase leads. No restarted dependency graph or candidate gate.


## Ninth direct research batch (2026-10-26)

Nineteen new meanings researched directly into the combined-only mathDef
reference, following source review against Encyclopedia of Mathematics and
nLab and duplicate checks against original and independent datasets:

- Category variants: subcategory, wide subcategory, replete full
  subcategory, thin category, skeletal category and skeleton
- Functor variants: identity functor, endofunctor and constant functor
- Elementary categorical constructions: coslice / under category,
  right adjoint, counit of adjunction, arrow category
- Monad theory: monad, comonad, algebra over a monad,
  Eilenberg–Moore category and Kleisli category
- Presheaf theory: category of elements of a contravariant
  Set-valued presheaf

Definitions include explicit equations for monad/comonad associativity
and unit laws; precise direction of adjunction unit/counit; Kleisli
composition; and contravariant category-of-elements arrows.
A skeletal category may have nontrivial automorphisms. A skeleton
requires representative choice under customary foundations; no claim of
unconditional existence is made. Wide/full/replete are not conflated.

Source passages were retrieved directly from nLab and Encyclopedia of
Mathematics on 2026-10-26; these remain assistant-reviewed definitions,
not peer-certified research. Preserve the per-entry reference locator
and assumptions.

Combined-only overlay now has **118** researched meanings
(99 earlier + 19 here). Expected merged reference: **2,090**
contextual meanings; the independent reconstructed Wave2 remains **958**,
original source remains **1,014 definitions**, and initial **2,019**
rough phrase-lead scan remains an untouched discovery snapshot.
No dependency-graph gates or global review queues should be restored.


## Active workflow correction — actual first-scan candidate incorporation (2026-10-26)

**The owner explicitly clarified that new-vocabulary searching is NOT the current
task.** We already have a 2,019-phrase discovery collection from the original
quick scan of 363 Wave2 direct meanings and 1,014 original mathDef definitions.
Work on THOSE existing phrases, in their recorded rank order. Only return to
new-term discovery when that is a separately authorized phase.

Initial scan-processing batch: ranks **1–60** have individually recorded
outcomes in `scan_candidate_dispositions.json`. These records contain the
exact phrase, occurrence count and source examples from the ORIGINAL
`scan-report.json`, plus outcome, existing meaning/source matches,
rationale and newly added target IDs. Totals:
- 4 candidates became new headings: real vector space, measure space,
  complex vector space, compact metric space
- 1 candidate ('Borel measure') became 3 explicitly different
  context-specific definitions, reflecting conventions A, B and C
- 22 candidates were already covered by existing content
- 1 ('graded ring') is covered by EXISTING distinct graded-ring variants
- 30 were ordinary grammatical fragments or nontechnical qualifiers
- 2 were marked genuinely ambiguous in context, rather than silently merged

This added **7 meanings** (118 previous + 7 = **125** post-Wave2).
The expected combined catalog is **2,097 meanings**.
The previously reported 2,019 *scan candidate phrases* remain a
different, unmodified number.

**Next work:** continue candidate rank **61 onward**, obtaining the actual
original scan records (not invented candidates) and recording quick
dispositions. For new concepts research and add actual mathematical meaning
records with source citations, context and related links; for duplicate
or synonymous phrases point to existing definitions rather than adding
redundant meanings; for distinct legitimate senses retain variants.
Do not undertake unrelated gap-finding or reinstate dependency graphs,
approval gates or an extensive manual-audit queue. Candidate dispositions
are a lightweight resumption log, not a research stage gate.


## Scan-driven candidate incorporation — ranks 61–100 (2026-10-26)

Continued strictly through the **next 40 ranked candidates from the original
frozen scan**, not unrelated vocabulary searches. The same
`scan_candidate_dispositions.json` ledger now holds exactly ranks **1–100**,
with literal scan phrase, occurrence count, source examples and disposition.
The complete first 100 comprise 7 new-term candidates (7 new headings), 1
multi-variant candidate (three Borel measure contexts), 39 already
represented meanings, 1 covered by existing variants, 48 lexical nonterms
and 4 contextual ambiguities. (These are candidate counts; the first 100
generated 10 new meanings in total.)

New definitions from this 40-candidate batch:
- Rank 63: **extended-real-valued function** with codomain ℝ∪{−∞,+∞},
  distinguishing the properness condition as a separate property.
- Rank 70: **integrable adapted sequence** with filtration measurability
  and per-time L¹ integrability, without a martingale condition.
- Rank 82: **quasi-norm** on a real/complex vector space; C-relaxed
  triangle inequality, not a norm unless C=1.

Citations are directly checked Encyclopedia of Mathematics, Berkeley/Durham
probability notes, ETH Zurich functional analysis notes and MathWorld.
The source-specific distinctions and assumptions are stored in the entries.

**Next cursor: scan rank 101**. Current post-Wave2 combined-only research
overlay: **128 meanings** (118 pre-scan + 10 incorporated scan-derived);
expected combined count **2,100**. Do not begin a new terminology search
while the original candidate set is the owner's chosen input. Preserve
independent Wave2's 958 meanings and the original 1,014 mathDef definitions.


## Scan-driven candidate incorporation — ranks 101–140 (2026-10-26)

Processed **exactly the next 40 ranked phrases** in the frozen original
`/reconstruction/merged/scan-report.json`, with the phrase, count, and
source examples copied literally to the same verified disposition ledger.
This batch produced **8 new researched meanings**, **18 existing/synonymous
matches or specializations**, and **14 lexical nonterms**. No new candidate
collection was built.

New searchable meanings:
- 106: absolutely convergent ordinary Dirichlet series (at a specified s)
- 107: homomorphism of unital R-algebras (the scoped sense of algebra map)
- 123: closed linear subspace (norm topology, Banach completeness caveat)
- 124: compact Hausdorff space
- 127: complex-valued function (arbitrary set as domain)
- 129: continuously real-differentiable complex-valued function (real C¹,
  not holomorphy)
- 130: convergent complex power series (positive-radius convention)
- 131: at most countable subset (includes finite/empty, with countability
  convention explicitly distinguished)

Useful no-new-entry decisions include rank 114 (attracting fixed point is
period-one attracting periodic point), rank 126 (complex Hilbert spaces
are covered by Hilbert-space scalar-field conventions), and ranks 101–103
(existing unital ring/ring-map content). The source locators and convention
choices are stored in the new `terms.json` records.

**Next original-scan rank: 141.** Current combined-only overlay **136**
meanings; expected combined **2,108** (958 independent + 1,014 original +
136 researched post-Wave2). Both completed historical previews and original
production source remain unchanged. The 2,019 scanned phrases are neither
newly collected nor automatically accepted as definitions.


## Scan-driven candidate incorporation — ranks 141–180 (2026-10-26)

Continued in **strict rank order** through the same frozen original quick-scan
collection. Recorded all 40 literal candidates, counts, source examples,
dispositions and canonical targets in `scan_candidate_dispositions.json`.
Results: **4 new concepts**, **1 distinct contextual variant**, **15 already
covered**, **19 grammatical/nonterm fragments**, **1 contextual ambiguity**.

Five sourced merged-only meanings added:
- Rank 142: finite-dimensional Euclidean space; both vector and affine
  realizations, with a positive-definite real inner product
- Rank 143: finite-dimensional vector space over a specified field;
  dimension zero allowed
- Rank 144: finite field extension, finite *degree*, not finite cardinality
- Rank 163: Hausdorff second-countable topological space, without falsely
  assuming local Euclidean/manifold structure
- Rank 166: isolated point of a subset, related but more general than the
  already reconstructed isolated point of the whole topological space

Existing-reference decisions include fraction field (rank 169), minimal
polynomial (170), residue field (172), local homomorphism (175), and negative
set for a signed measure (178). 'Its first return map' (168) remains a
contextual ambiguity, also noted earlier at rank 88, rather than forcing
a possibly wrong sense.

**Next rank: 181 / 2,019.** Exactly **180 ranks processed**, **23 added
sourced meanings** from those ranks, combined-only overlay now **141**
meaning records, expected combined catalog **2,113** (958 independent +
1,014 original + 141 post-Wave2). Independent Wave2 and original
production definitions are frozen. No new candidate-finding step happened.


## Frozen quick-scan candidate research — ranks 181–220 (2026-10-26)

Processed exactly the next 40 of the original 2,019 frozen phrase leads,
recording literal source IDs, occurrence counts, and dispositions in the
existing ledger: **4 new meanings**, **23 existing**, **11 lexical
nonterms**, **1 context ambiguity**, and **1 covered by existing variants**.
No candidates were collected outside the original scan.

New merged-only meanings are:
- Rank 185: open bounded interval in ℝ; endpoints excluded
- Rank 187: Hilbert-space orthonormal basis; dense linear span rather than
  a necessarily Hamel basis
- Rank 193: fixed-space morphism of sheaves of sets; compatibility with
  restrictions, independently of ring or module structure
- Rank 201: sub-σ-algebra on the same underlying set, allowing both trivial
  and whole σ-algebras without assuming measure-completeness

Existing-reference cases include pointed space, peak point, Radon measure,
test function, associated graded module, Bergman projection, field norm and
exterior derivative. The empty product (216) has categorical versus
multiplicative-identity meanings already present, not to be merged. The
noninvertible-map lead (182) is context ambiguous.

**Next cursor: rank 221.** Processed **220/2,019** of original leads.
**27 added mathematical meanings** from these leads, **145 total
post-Wave2 merged-only meanings** and expected **2,117** combined
(958 independent + 1,014 original + 145 overlay). Original and
independent historical content remain frozen.


## Frozen original terminology scan: ranks 221–340 (2026-10-26)

In one larger pass, processed exactly **120 original ranked phrase leads**,
using the already-frozen 2,019-candidate scan report. All literal phrases,
occurrence counts, source-example IDs and decisions are appended to the
**same** `scan_candidate_dispositions.json` ledger. No independent term
collection, external vocabulary hunt, dependency graph, approval packets or
new scan was undertaken.

Research outcomes for this batch:
- **7 new sourced meanings** from actual ranks 223 (free abelian group),
  244 (spherical/chordal metric), 251 (zero polynomial), 252 (zero ring),
  259 (Banach-valued simple measurable function), 279 (affine open
  subscheme) and 318 (complex-analytic subset).
- **33 already-defined terms** (e.g. filled Julia set, orthogonal projection,
  measure pushforward, quotient topology, von Neumann ordinal, Young function,
  Hardy H∞, algebraically closed field, I-adic completion map).
- **78 lexical fragments**, quantifiers, and nonterminological references.
- **1 contextual ambiguity**, rank 224, where a stripped "identically infty
  function" does not determine the sign or allowed extended-valued convention.
- **1 covered multi-variant expression**, rank 265 (empty product, with
  algebraic and categorical interpretations retained separately).

Important mathematical distinctions in the new meanings: free abelian
does NOT mean every torsion-free abelian group; spherical metric is explicitly
the stereographic **chordal** normalization, not geodesic distance; the
formal zero polynomial's degree requires a declared convention; Stacks
includes the zero ring (0=1); simple Banach-valued measurability need not
mean finite-measure support; affine open means open *and affine as a
scheme*; complex analytic subsets are not the descriptive-set-theoretic
Souslin analytic sets nor merely their germs.

**Next candidate rank 341.** Original candidates now **340/2,019**
processed; original scan-derived mathematical meanings **34**.
Post-Wave2 overlay **152**, expected combined **2,124** meanings
(958 independent Wave2 + 1,014 original source + 152 post-Wave2).
No changes to completed historical Wave2 or original production definitions.


## Original quick-scan candidate processing — ranks 341–540 (2026-10-26)

In a larger consecutive batch, dispositioned the **next 200 literal original
candidate records** from the already-frozen 2,019-lead scan. The existing
`scan_candidate_dispositions.json` retains their exact original phrases,
counts, source examples, mappings and decisions. **No new terminology
candidates were searched for, collected, or appended.**

- **6** genuinely new researched mathematical meanings: rank 413
  associative algebra over a field (nonunital base convention), rank 470
  bounded continuous real-valued function, rank 482 Cantor space,
  rank 506 cofinal subset of a partially ordered set, rank 532
  complete discrete valuation ring, rank 537 completely multiplicative
  arithmetic function. Each is added directly to `terms.json` with
  external research sources, scoped assumptions and links.
- **36** already-covered terms or justified specializations, including
  Bargmann–Fock space, centered finite difference, chromatic metric
  space, Bessel-potential Sobolev space and compact operators.
- **156** grammatical fragments/nonterms, rather than forcing low-quality
  new definitions. Special notes guard against the incorrect claims
  'bijective smooth map = diffeomorphism' and 'bijective monotone map =
  order isomorphism' absent inverse smoothness/monotonicity.
- **2** source/convention ambiguities (524 compact complex Lie group versus
  connected complex torus; 534 general complete nonarchimedean local
  field versus a characteristic-zero p-adic field).

**Deduplication correction:** original
`definitions/scv/complex-analytic-subset.tex` already contains the
meaning that was redundantly added at former scan rank 318. The
extra post-Wave2 overlay entry was removed, rank 318 was changed to an
existing-definition disposition, and research citations/edge-case notes
were retained in the ledger's `reconciliation` field. Rank 539 likewise
maps to the existing original definition.

**Checkpoint: 540 of 2,019 original candidates processed; next rank 541.**
Post-Wave2 overlay **157**, with **39 net scan-derived meanings** and 118
earlier additions. Expected combined meanings **2,129** =
958 independent Wave2 + 1,014 original + 157 post-Wave2.
The original frozen scan, original production definitions, and independent
Wave2 are not edited or relabeled.


## Original scan candidate incorporation — ranks 541–740 (2026-10-26)

Processed the **next 200 actual original 2,019-lead quick-scan candidate
records**, in strictly consecutive rank order. The existing
`scan_candidate_dispositions.json` contains the literal phrase,
occurrence count, original source examples, short contextual justification
and source-valid target mapping for every rank. **No new candidates** were
sought or appended, no dependency graphs were reintroduced.

The batch contributed **seven source-attributed mathematical meanings**
directly to merged-only `terms.json`:

- Rank 541: complex Euclidean space ℂⁿ (complex and real dimensions,
  fixed standard Hermitian inner product)
- Rank 542: Hermitian complex matrix (A=A*, without assumed positivity)
- Rank 556: computable sequence of rationals (uniformly effective exact
  output, no implied effective modulus or computable limit)
- Rank 567: constant map (explicit empty-domain and empty-codomain
  convention)
- Rank 586: conull measurable subset of a measure space (not simply
  `μ(A)=μ(X)` in infinite-measure spaces)
- Rank 639: unital cohomologically graded differential algebra
  (degree +1 d²=0, graded Leibniz and convention choice)
- Rank 650: discrete subset in the subspace topology (need not be closed)

The other **193** ranked phrases resolved to **29** already-covered
meanings, **161** sentence/quantifier fragments that are not named
mathematical concepts, and **three** context ambiguities (computable
limit 555, density function 624, empty interval 680). Definitions
include assumptions and source references. These remain
assistant-reviewed research, not independently certified proofs.

Checkpoint: **740/2,019 original leads completed**, **1,279 remain**;
next rank **741**. The post-Wave2 merged-only overlay now contains
**164** meanings (118 pre-scan additions + 46 net scan-derived meanings);
expected combined corpus **2,136** meanings (958 independent Wave2 +
1,014 original + 164 researched overlay). Original scan and historical
source snapshots remain untouched.


## Original frozen scan incorporation — ranks 741–940 (2026-10-26)

Processed the next **200 literal original quick-scan candidate phrases**
from the fixed 2,019-candidate scan report, preserving occurrence counts,
source examples, each decision and canonical target mapping in the same
`scan_candidate_dispositions.json`. **No new candidates discovered.**

Research dispositions in this batch:
- **5** mathematically distinct source-attributed meanings added directly
  to merged-only overlay: rank 769 **field embedding** (unital injective
  field map); 770 **filtered probability space** (time-increasing filtration,
  no automatic usual conditions); 779 **finite-index subgroup** (cosets
  finite, normality not required); 798 **finitely generated group** (finite
  generators, not necessarily finite/presented); and 874 **free-variable
  set of a first-order formula** (recursion on syntax and quantifier scope).
- **22** existing matches, including exhaustion function, feasible point
  as a member of a feasible set, finite measure, finite basis /
  finite-dimensionality, closure operator, graded associative ring,
  Hamel basis, Hermitian matrix, and homeomorphism.
- **169** scan-generated grammatical fragments, quantifier clauses or
  contextual descriptors, not independent terms.
- **4** context ambiguities: 803 'fixed field' as a parameter versus an
  automorphism-group invariant; 871 'formal series' with unspecified
  exponent/algebra conventions; 881 'function algebra' across several
  contexts; 933 'Hilbert function space' versus RKHS (continuous point
  evaluations cannot be assumed).

Retained crucial safeguards: finite normal extensions need NOT be
separable/Galois; a general field embedding is not an automorphism;
and a subgroup with finite index need not be normal.

**Persistent next rank 941.** Original scan **940/2,019** processed, 1,079
remaining. Overlay now **169** meanings (= 118 earlier + 51 net researched
scan additions); expected merged catalog **2,141** meanings (= 958
independent + 1,014 original + 169 overlay). Historical source
collections and the frozen candidate scan remain untouched.


## Frozen original quick-scan candidate incorporation — ranks 941–1140 (2026-10-26)

Processed the **next 200 consecutive original source-exact candidate phrases**
without collecting additional candidate terminology or rescanning sources.
The existing `scan_candidate_dispositions.json` retains original occurrence
counts and source examples, mathematically informed outcomes, target
mappings and concise reasoning.

Eight directly incorporated **new mathematical meanings**:
959 imperfect field; 1004 injective map; 1008 integral basis of a
number field; 1100 large category; 1106 Lie algebra homomorphism;
1116 localizing sequence for a local martingale; 1121 locally finite Borel
measure; 1122 locally univalent holomorphic function. Each includes
mathematical definitions, sourced references, explicit scope and exception
conventions. Important distinctions: injection is not arbitrary-category
monomorphism; Lie algebra homomorphism is bracket-preserving and need
not integrate to a Lie group map; localizing stopping times must make
the stopped process a martingale; locally finite Borel measure does not
imply general Radon regularity; local univalence need not imply global
injectivity.

The other **192** original candidates were resolved as **50 existing**
and appropriately contextualized notions, **138** grammatical fragments
or property references, and **4** genuinely unresolved contexts (981
infinite-dimensional complex spaces, 989 infty function with lost sign,
1108 linear differential operator with unspecified setting, and 1138
maximal fields). Original frozen and independent Wave2 definitions were
not modified.

**Checkpoint: 1,140/2,019 ranked candidates processed**,
**879 remain; next rank 1141**. Post-Wave2 merged-only overlay **177**
meanings (118 earlier + 59 net scan additions), expected merged total
**2,149** (958 independent Wave2 + 1,014 original + 177 post-Wave2).


## Original frozen candidate scan incorporation — ranks 1141–1340 (2026-10-26)

Processed **200** further consecutive original candidates using ONLY the
frozen 2,019-item original quick-scan report; no discovery,
recollection or extra candidate collection. Every source-exact
phrase/count/example and its outcome is in the established
`scan_candidate_dispositions.json` ledger.

Research decisions: **16 new researched mathematical meanings/variants**,
**29 existing matches**, **152 scan-produced nonterms/grammatical
fragments**, and **3 context ambiguities** (1161 meromorphic maps,
1199 'noncommutative rings' convention and 1285 ordered set conventions).

The 16 direct additions to merged-only `post_wave2/terms.json`
are: rank 1163 minimal element of a poset (NOT necessarily least);
1165 mixed second partial derivative (opposite orders not equal
without regularity); 1181 multiplicative order of a group element;
1198 strictly noncommutative ring; 1201 nondecreasing real function;
1227 nonreduced commutative ring; 1239 normed/absolute-valued
field; 1270 one-sided left or right ideal (NOT automatically
two-sided); 1280 order-preserving map (NOT necessarily an
embedding); 1281 ordered field; 1282 bi-invariant ordered group;
1305 partial computable function (nonhalting versus undefined);
1317 Petrov–Galerkin finite element discretization (distinct
trial and test spaces); 1318 piecewise polynomial function
(no automatic spline regularity); 1322 Polish topological
group; 1323 Polish space (topologically completely metrizable,
not necessarily complete for every compatible metric).

New definitions include source attribution, context, and assumptions.
Uncertain mathematical equivalences were not asserted. Historical
original definitions and independent Wave2 stay unchanged.
**Checkpoint 1,340/2,019 processed; next rank 1,341; 679 remain.**
Overlay: **193**, including **75 net scan-derived meanings** beyond
118 pre-scan meanings. Expected merged total:
**2,165 = 958 independent + 1,014 original + 193 merged overlay**.
