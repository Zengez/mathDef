#!/usr/bin/env python3
"""Source-linked mathematical-terminology adjudication after Pass 5.

This is an EDITORIAL worklist, not a proof that a phrase needs a separate
mathDef definition. Reversible statuses retain the original phrase/ID/context.
"""
from __future__ import annotations
import argparse, csv, json, re, collections, hashlib
from pathlib import Path

VERSION='mathdef.targeted-terminology-review.v1'
CANONICAL_FEED='0441b9c5fc2f7a515c3210a7471a3a3e8f9ca0b8dc63f570dcc8e1cb38a08fe2'
ROOT=Path(__file__).resolve().parent

def load_tsv(folder):
    result=[]
    for file in sorted(folder.glob('*.tsv')):
        with file.open(encoding='utf-8',newline='') as f:
            result.extend(csv.DictReader(f,delimiter='\t'))
    return result

# Curated independently recognizable mathematical concepts, including variant
# conventional spellings. Research URLs are assigned ONLY when verified.
KNOWN_TERMS='''
additive measure|adjacency matrix|adjunction bijection|almost-everywhere equivalence|almost-everywhere limit|
analytically conjugate|analytic-set germ|arithmetic operations|autonomous ode|autonomous vector|
barycentric coordinates|base-change map|based homotopy|basin components|bessel function|bergman-space construction|
binary biproduct|binary coproduct|bloch functions|blowup algebra|bochner integrability|bochner sense|
boundary trace|boundary traces|boundary-value problem|brownian motion|bézout's identity|
canonical inclusion|canonical injection|carleson measure|cartesian coordinates|cartier divisors|
categorical localization|category-valued functor|cauchy-equivalence class|cell decomposition|cellular decomposition|
chain rule|characteristic equations|characteristic function|characteristic functions|characteristic map|
characteristic maps|clopen neighborhoods|closed walk|cofiltered diagram|cofinal family|
coherence axiom|coherence axioms|coherence identity|cohomological differential|coloring map|
column space|commensurator group|commuting indeterminates|complex hypersurfaces|
constant coefficients|convex combinations|critical points|decision variables|displacement vectors|
distribution functions|dual problem|exhaustion function|exterior power|exterior-power map|
fibre category|fibred categories|fibred category|formal series|frobenius map|front set|
function element|galerkin method|geometrically integral|gluing data|holomorphic hull|
homogeneous element|homogeneous elements|homotopy classes|identically distributed|
independent variable|integrable martingale|integrally closed|inverse function|
jacobi identity|k-bilinear multiplication|k-linear operator|k-linear transformation|
kolmogorov complexity|kähler metric|least ordinal|levi problem|linear system|
localization map|many-one reduction|many-one reductions|markov process|meromorphic continuation|
normalized kernel|nth root|path distance|poincaré distance|point evaluations|
polynomial system|principal parts|pullback functor|punctured disk|quasi-coherent sheaf|
rees algebra|right coset|right cosets|separably closed|stirling number|stirling numbers|
supporting hyperplane|taylor expansion|turing reduction|unit ball|unit ideal|
adic absolute value|nonarchimedean absolute value|alexandrov space|ore-square condition|
quadratic program|relative compactness|weak equivalences|embedded lie subgroup|
weak operator topology|strong operator convergence|stereographic projection|
second-order scalar differential operator|kkt conditions|kleisli category|
krull topology|kuratowski closure|lagrange duality|lie ideal|lie brackets|
lindelöf space|moore category|monoidal structure|mollifier family|
möbius transformation|multiplication operator|natural transformation|
one-point alexandroff compactification|petrov galerkin method|
regularity in codimension one|smooth vector field|strong operator topology|
surjectivity locus|symbolic power|sum-of-divisors function|tagged partition|
topological dimension|topological field|torsion-free abelian group|
cartesian product|free module|radical ideal|injective hull|inner automorphism|
intermediate extension|internal hom|interpolation polynomial|joint independence|
leibniz identity|left-ordered group|lifting property|lie algebra structure|
local homomorphisms|locally factorial|measure-theoretic strong mixing|
nonarchimedean valued field|norm-closed two-sided ideal|
normalized discrete valuation|partially ordered group|
finite-dimensional real vector space|formal power series ring|
iterated partial derivative|inverse limit|sheaf cohomology|
strictly positive levi form|tangential cauchy riemann equations|
von neumann regular ring|multivariate normal distribution|
zero hilbert space|properly supported smoothing integral operator|
prefix-free partial computable machine|optimal universal partial computable machine|
nonseparable complete metric space|time-homogeneous markov process|
time-homogeneous markov chain|carleson-box bound|uniform carleson-box bound|
one-variable green function|locally convex space|partial derivatives|
strong mixing|fibre product|homotopy group|formally unramified ring map|
single-tape deterministic turing machine|single-tape nondeterministic turing machine|
short exact sequence|split short exact sequence|singular strong limit cardinals|
complex of abelian groups|left r-modules|jacobian matrix|initial segment|
initial value|initial-value problem|least-squares problem|left g-action|
vector space|holomorphic function element|semisimple module|basis conjugates|
compactness property|identity map|point evaluation|geodesic metric|
zero-ring convention|invariant probability|proper class of objects|
exterior power of a module|cofiltered diagram|surjective ring homomorphism|
convex polyhedron|closed loop|local charts|real-valued functions|
right quotient ring|partial order|opposite category|formal power series
'''.replace('\n','').split('|')
KNOWN_TERMS={p.strip() for p in KNOWN_TERMS if p.strip()}

# Additional established concepts identified by reviewing the actual 2,175 terms
# against their underlying source definitions and mathematical usage.
KNOWN_TERMS.update({p.strip() for p in """
action-induced equivalence|adic topology|affine open subset|algebraically closed field|
analytic subsets|associative multiplication|base category|base morphism|
base point|base points|bicategory equivalence|bilinear operation|
boolean isomorphism|borel probability measure|cancellation axiom|
canonical quotient map|cartesian coordinates|cauchy construction|
characteristic-zero field|cochain complex|coherence diagrams|
coefficient functions|coefficient sequences|coefficient weights|
cofinal family|commutative banach algebra|commutative r-algebras|
commutativity axiom|compact subspaces|compatible metric|
complex manifold structure|complex-vector-space structure|
computable convergence|computable limit|conic neighborhood|
connecting map|continuous semigroup|continuous semimartingale|
continuous semimartingales|conull subset|convergence modulus|
convex interpolation|convex map|convex program|coordinate change|
coordinate representation|coordinate systems|countable subcover|
covariance matrices|cr dimension|cr structure|cw structure|
darboux integrals|decision-tree model|dedekind cuts|
dedekind-cut construction|deductive system|definite integral|
degree-zero component|degree-zero subring|derivative seminorm|
deterministic machine|diagonal morphism|dirac distribution|
direct sums|direct-limit topology|directed preorder|directed system|
dirichlet boundary|dirichlet-space norm|disk-to-half-plane map|
division remainder|dot product|dual pair|dual-number ring|
dynkin system|edge set|edgeless graph|embedded prime|
empty family|empty cone|empty cover|empty diagram|empty face|
empty interval|empty semigroup|empty subbasis|empty support|
empty union|empty-family intersection|equivalent metric|
error probability|essential-supremum norm|euclidean norm|
euclidean projection|euclidean topology|evaluation homomorphism|
evaluation identity|exchange axiom|extended real line|
finite-element method|finite-precision representation|finite-type k-algebra|
first-order formula|first-order language|first-order model|
flat locus|floating-point system|forcing poset|forcing posets|
forgetful functor|formal integrability|formal indeterminates|
fréchet derivative|fréchet-differentiable map|function germs|
generalized eigenspace|generating set|generic-point map|
graph character|group character|halting set|hartogs figure|
heat kernel|hermitian covariance|homological degree|
homological degree|holomorphic embeddings|holomorphic hulls|
independence number|independent increments|indexing map|
inference rule|integrability condition|integer-linear combinations|
intermediate fields|intermediate subfield|inverse diffeomorphism|
inverse endomorphism|inverse transform|inverse-limit ring|
irreducible polynomials|isomorphic objects|isomorphism classes|
ith cohomology|ith homology|k-algebra map|k-linear combination|
k-linear combinations|k-vector subspace|kaplansky dévissage|
knott partition|kuratowski construction|lagrange duality|
labelled set|length-zero walk|limit cardinals|local subrings|
lower cuts|m-adic completion|macaulay locus|marginal distribution|
markov kernel|martingale transform|matroid circuits|
matroid cycle|matroid cycle matroid|maximal antichains|
maximal atlas|maximal chains|maximal clique|maximal matching|
measurable partition|measure-preserving bijections|
membership relation|meromorphic germs|meromorphic maps|
metric axioms|metrizable topology|modulo completion|
monoidal structure|multiplication-by-α endomorphism|
multiplicatively closed|multiplier algebra|
neighborhood filter|neumann boundary|noncomputable limit|
nonnegative-integer grading|normalized discrete valuation|
notation|ordinal-indexed increasing family|orthogonal coordinate change|
partially differentiable function|partially ordered quotient|
piecewise polynomial spline|polynomial-time decidable predicate|
positive-definite bergman metric|positively graded ring|
positively homogeneous symbol|power series ring|
probability distribution functions|probability row vector|
pushforward probability measure|quasi-coherent ideal sheaf|
quasi-compact open subset|quasi-compact topological space|
quotient structure sheaf|real-valued lévy process|
reduced closed subscheme|row-stochastic transition matrix|
sample standard deviation|schwartz distribution kernel|
set-theoretic fibre product|simple left r-modules|
singular chain complex|smoothly varying positive-definite inner product|
spectral sequence|specialization relation|split epimorphism|
square-zero element|square-zero quotient|stereographic projection|
strongly continuous semigroup|subbasic open|subnormal numbers|
surjective module map|symbolic power|tagged partition|
term algebra|test-function topology|time-homogeneous chain|
topological dimension|total variation norm|torsion-free abelian group|
translation vector space|two-sided multiplicative system|
univalent holomorphic function|unramified ring map|
unweighted euclidean volume measure|von neumann regular ring|
weak operator topology|weighted finite sum|zero hilbert space|
characteristic polynomial|characteristic function|
based homotopy classes|continuous at limit ordinals|
change of coordinates|fractional ideal|integrally closed domain|
finite-rank free r-modules|discrete valuation domain|
complexes in an additive category|group of units|
order embedding|surjective order embedding|
partially ordered group|associated monge ampère measure|
formal complex power series|uniform convergence on compact subsets|
nonconstant rational map|nondegenerate normal distribution|
nontrivial discrete valuation|countable neighborhood base|
matroid independence|iterated partial derivative|unit ideal|
cardinality bound|cauchy sequence|
weak homogeneous-dirichlet solution
""".replace('\n','').split('|') if p.strip()})

# Corrections from examining the original context: "front set" was clipped
# from "wave front set", which is the technical term.
for nonterm in ('front set','bochner sense','compactness property','compact subspaces','notation'):
    KNOWN_TERMS.discard(nonterm)

# Second mathematical adjudication sweep: standard concepts recognized from
# definitions, with mixed-context conventions left for later editorial review.
KNOWN_TERMS.update({p.strip() for p in """
de rham differential forms|
set-valued diagram|smooth atlases|square root|square-zero kernel|
categories fibred in groupoids|convergence on compact subsets|
resolution of an r-module|space of entire functions|
chains of irreducible closed subsets|hilbert space of entire functions|
morphism of locally ringed spaces|matching in an undirected graph|
boundary conditions|punctured neighborhood|euclidean vector space|
absolute-convergence set|adapted neighborhood|
ampère measure|associativity isomorphism|axiomatic set|
base-change stability|bicategory equivalences|borel bijections|
cancellation axioms|canonical well-order|cantor subset|cantor's diagonal|
cauchy-sequence model|coherent maps|compact complex|
complex-manifold structure|complexity theory|
conformal conjugacy|conformally conjugate|conic subset|
conjugate-linear parts|continuous semimartingale|
continuous injection|constrained problem|convex optimization|
coprimality restriction|d-induced topology|degree-raising differentials|
diagonal identity|disconnected components|disk measures|
displayed map|dual supremum|feller process|fiber bundle|
fiber products|fibre-product scheme|field inclusion|filled ball|
finite-dimensional subspaces|finite-rank vector|
finite-type k-algebra|flat locus|formal difference|
fréchet derivative|g-equivariant map|g-graded ring|
generated field|generating set|graph-only mapping|
group-theoretic kernel|hadamard formula|
hermitian covariance|hilbert-space norm|
homogeneous-dirichlet solution|hull span|
improper filter|inclusion-induced homomorphism|
infinite-dimensional basis|integrability condition|
isomorphism covers|kernel's support|
matroid independence|matrix identities|membership relation|
metrizable topology|modulo completion|monoid identities|
non-full subcategories|noetherian k-algebra|
nondegenerate differential|operator-norm convergence|
optimization algorithm|oracle set|order-preserving map|
ordered subfield|ordinal representation|ore-square completion|
p-cartesian morphism|parabolic equation|parametrized geodesic|
path component|path length|pettis integrability|
plain complexity|pluripotential theory|pointed set|
pointwise operations|pointwise-convergence topology|
poisson process|polar cone|polish topology|
population variance|positive-definite metric|
postcritical closure|power-series expansion|
prime divisors|prime-spectrum topology|principal character|
product topology|projection arrows|projective r-module|
primal problem|pth power|pth root|
punctured-neighborhood germ|quasi-compact neighbourhoods|
randomized machine|real-number system|
regularizing errors|relative independence|residue characteristic|
restricted norm|robin boundary|rooted tree|round-to-nearest arithmetic|
rounding error|runge approximation|runge pair|
saturated chain|semidirect product|semigroup homomorphism|
semisimple submodule|sesquilinear map|simple poles|
simple r-module|simple root|simplex category|
simplicial identities|simpson rule|spatial isomorphism|
sphere-valued map|spanning set|small extension|
splitting field|square-zero quotient|stereographic projection|
strict inclusions|surjective ring homomorphism|
symbolic sum|tensor powers|tensor-product algebra|
trapezoidal rule|transition kernel|transition semigroup|
transitive model|trapping neighborhood|trivial fibrations|
trivial triangles|trivial valuation|two-sided ideals|
unbounded-below problems|uniform attraction|unit sphere|
unital subring|unoriented angle|unreduced suspension|
upward closure|valuative criterion|valuative lifting|
valued field|variation norm|variational problem|
verdier's axioms|vertex coloring|vertex k-coloring|
walking-arrow category|wandering components|weil divisor|
weil divisors|well-formed formula|winding number|
z-graded ring|zero gap|
cartier divisors|matroid circuits|arithmetic progression|
associativity isomorphism|discrete-time map|dual pair|
flat epimorphism|metric topology|weak equivalence|
complex-valued stochastic process|nontrivial discrete valuation|
coherent sheaf|uniform approximation|
holomorphic coordinate systems|equivariant measure-preserving borel injection|
nonfield discrete valuation domain|smoothing integral operator|
bargmann fock hilbert space|
linearly ordered group|second-countable topological space|
finite-dimensional k-vector space|unital associative r-algebras|
nonnegative lebesgue stieltjes measure|
""".replace('\n','').split('|') if p.strip()})

CONTEXTUAL_FROM_REVIEW={p.strip() for p in """
affine equalities|increasing chain|increasing family|ordered pair of objects|
monic polynomial with coefficients|valuation ring with fraction field|
invertible comparison|associative composition|discrete stability|empty basis|
generated group|generated r-modules|holomorphic coordinates|
independent subset|infinite-dimensional complex|integrable weight|
localized map|noninvertible map|norm-convergent expansion|
projective r-modules|r-linear combination|r-linear combinations|
rectangular diagonal|relative endpoints|simple loopless|
sum dévissage|upward closed|weakest topology|worst-case time|
affine open subsets|bijective group homomorphism|
canonical quotient map|continuous linear functionals|
convergent power series|disjoint open sets|
finite-type ring homomorphism|finite-type ring map|
homotopic relative endpoints|identically zero function|
induced exterior-power map|integral linear combination|
loopless undirected graph|measurable null sets|
nonnegative measurable function|polynomial-time computable map|
positive-definite inner product|pseudodistance separates points|
real-valued discrete-time process|square-integrable random variables|
surjective r-algebra map|uncountable regular cardinal|
valued simple functions|injective ring map|nowhere dense subsets|
supported smooth functions|affine coordinate|affine coordinates|
additive groups|algebra homomorphisms|ambient composition|ambient module|
ambient ring|associative r-algebras|base arrow|
base morphism|borel subsets|canonical injections|
closed elements|closed pieces|coefficient weights|
common value|compatible chain|composable pairs|
computable extension|computed approximation|
consecutive vertices|constant multiple|constant series|
continuous injection|continuous weight|
conjugate-linear parts|complex-valued processes|
component tags|conventions change|
equivalent characterization|equivalent characterizations|
display multiplication|integer exponent|integer exponents|
integer multiples|integer multiplication|integer product|
integer solution|integer solutions|integer sum|
intermediate vertices|inverse endomorphism|
isomorphic objects|ith coordinate|join supremum|
large measure|lowering degree|mathematical operation|
mathematical structures|meromorphic maps|
metric axioms|minimum time|monoid identities|
modulo equality|modulo powers|multiple limits|
n-fold product|n-fold tensor|negative-power parts|
nonidentity automorphisms|nonincreasing order|
nonnegative diagonal|nonnegative distance|
nonnegative representation|nonnegative square|
nonnegative square roots|nontrivial specializations|
nonvanishing differential|norm axioms|norm changes|
normalized set|normalized model|random elements|
positive semidefinite property|requisite time derivatives|
singleton interval|size restriction|small multiple|
space sequential compactness|structures homomorphisms|
strict equalities|still covering|stacks convention|
standard time|unweighted euclidean volume measure|
absolute value by the norm|algebra is commutative|
disjoint locally closed subsets|generated proper ideal|
indexed open cover|closed line segment|closed real interval|
monic of degree|initial time|valid finite subcover|
quoted conventional notation|unsupported normed spaces|
""".replace('\n','').split('|') if p.strip()}

CONTEXTUAL_FROM_REVIEW.update({p.strip() for p in """
admitting composition|affect complexity|always idempotent|
attaching closed|binary coordinates|binary square|cells closure|
cells covering|characterize holomorphy|circle measure|
classes partition|closed norm|closed-subscheme structures|
collection hom|completing arrows|condition covers|
convention manifolds|convergent sum|converse implication|
cosets partition|create singularities|cut arithmetic|
decreasing degree|definition covers|descriptive variance|
designated vertices|deterministic partitions|
dimensional submanifold|direction subspace|
direction subspaces|directional difference|
discrete problem|discretized approximation|
disjoint cover|disjoint partition|displayed multiplication|
dotted arrows|effective error|eigenspace sum|
emphasizes identity|events ai|exact problem|
exclude fields|existing limit|existing topology|
expresses equality|false-negative probability|
family covers|forces equality|formal integer|formal theory|
forward limit|forward union|full axiom|full basin|
full dimension|full equality|function's norm|
functor axioms|guarantee descent|genuine functor|
ill-conditioned system|image preimage|
independent properties|integer divides|integer modulus|
intrinsic length|isomorphism covers|kernel's support|
large measure|mathematical structures|
maximal length|measure-theoretic multiplication|
module structures|morphisms functors|
negation rules|neumann representation|nontrivial closed|
normalized valuation|normally assumed|number quantifiers|
number system|numerical ode|numerical problem|
objects pairs|one-dimensional complex|
one-dimensional differentiability|one-variable polynomial|
op groupoids|open completely|
optimization problems|ordered bases|outgoing edges|
overlapping neighborhoods|own module|
per segment|pde methods|polynomial exponent|
polynomial restrictions|probability theory|
produces sums|product ij|proper differences|
proposed duality|q-vector-space basis|
query operation|querying machine|quotient stalks|
quotient-field characterization|r-algebra structure|
records adjacency|reflect order|reflects order|
relative fibre|repeated arrows|repeated multiple|
requisite time|reserve isometry|residual vector|
respects multiplication|restrict divisors|
restricted actions|restricted walks|revisit vertices|
ring axioms|ring constructions|ring multiplication|
row permutations|sample-point tags|
saying completely|schemes mapping|
selected subcover|sequential limits|
set distance|set-theoretic construction|
sheaf restrictions|sign relation|signed change|
simultaneously open|single morphism|size order|
size-unrestricted category|small diagram|small limits|
smooth loops|solid square|splits completely|
squared length|stacks characterization|
stacks criterion|state set|step-size rule|
structural tensor|structure homomorphisms|
subcollection hom|submanifold structure|
success probability|successive derivatives|
successive differential|successive quotient|
successor inclusion|supported weight|
supremal length|supremum modulus|sure equality|
surjective valuation|system hom|tensor isomorphisms|
tensor-product comparison|th integral|th power|
time derivatives|time equations|time index|time set|
topological subspace|topologically mixing|
total weight|transitivity composition|
trivial-cofibration fibration|two-element subset|
two-sided error|unbounded-below problems|
undirected edge|unit-preserving isomorphism|
unital composition|unknown solution|unordered subset|
valuative lifting|vector subspaces|vector-bundle structure|
weaken continuity|weighted moments|well-defined product|
well-defined ring|whole group|worst-case number|
zero gap|
carry identity elements|displayed factor order|
characterize real-valued probability distribution functions|
conventional single-tape deterministic turing machine|
functions of distance|finitely many affine half-spaces|
modulo principal fractional ideals|
path homotopic relative endpoints|
reduction modulo smaller powers|
""".replace('\n','').split('|') if p.strip()})

TERM_VARIANTS={
    'fibred categories':'fibred category',
    'characteristic functions':'characteristic function',
    'characteristic maps':'characteristic map',
    'many-one reductions':'many-one reduction',
    'right cosets':'right coset',
    'homogeneous elements':'homogeneous element',
    'injective hulls':'injective hull',
    'darboux integrals':'darboux integral',
    'holomorphic hulls':'holomorphic hull',
    'forcing posets':'forcing poset',
    'continuous semimartingales':'continuous semimartingale',
    'commutative local rings':'commutative local ring',
    'intermediate fields':'intermediate field',
    'integer exponents':'integer exponent',
    'integer solutions':'integer solution',
    'normal subgroups':'normal subgroup',
    'local subrings':'local subring',
    'coherence axioms':'coherence axiom',
    'square roots':'square root',
    'stirling numbers':'stirling number',
    'cartier divisors':'cartier divisor',
}

# Explicitly recognize these as contextual/expository wording. None is
# mathematically false; this just declines separate-heading nomination.
EXPOSITORY_EXACT='''
common field|disjoint sets|element set|increasing family|stronger condition|
alternative convention|ambient set|broader conventions|consecutive pair|
global bounds|hausdorff assumption|individual points|intended convention|
least order|literal equality|maximum cardinality|measurable events|
nonnegative integers|project convention|sign convention|single element|
smaller neighborhood|strict inclusions|stronger conditions|stronger sense|
support points|time interval|two-element subsets|undirected graphs|
common extension sets|disjoint measurable sets|disjoint open neighborhoods|
largest open subset|least positive integer|minimal under inclusion|
nonnegative real number|smallest closed set|smallest closed subset|
smallest normal subgroup|smallest positive integer|ordered by inclusion|
roots in an algebraic closure|broader conventions|compatible family|
common domain|common object|common polynomial|common value|
allowed assumption|adopted convention|categorical conventions|category convention|
classical proof|categorical sense|conventions admitting large categories|
unqualified term ring homomorphism|unqualified phrase algebra map|
weaker conull modulo completion|unlike weak duality|literal relation|
standard conventions|standard time|standard algorithms|standard convention|
intended convention|initial time|individual points|latter condition|
larger domain|larger integer|larger connected domain|common value|
stronger equivalence|stronger extension|most boundary|more events|
original open subsets|not necessarily|group multiplication|
identity elements|homotopy classes|additive notation|discrete topological|
metric topological|objects arrows|objects functors|elements integral|
function hom|functor hom|bijections hom|bijection hom|cochains hom|
cochain complex hom|interiors map|isomorphism hom|object hom|
term ring|term algebra|term closed|space an underlying real vector|
more events|method sometimes called|discrete topological|
standard hilbert norm|standard uniform bound|smallest topology|
source's general ring axioms|foundational conventions admitting large categories|
stronger term closed discrete subset|property stronger than|
strictly order|unlike real one-dimensional differentiability|
term closed discrete subset|this relation|separate convention
'''.replace('\n','').split('|')
EXPOSITORY_EXACT={p.strip() for p in EXPOSITORY_EXACT if p.strip()}
# Recognized research references; URLs have been independently retrieved.
SOURCES={
'fibred category':'https://stacks.math.columbia.edu/download/book.pdf',
'fibre category':'https://stacks.math.columbia.edu/download/book.pdf',
'fibred categories':'https://stacks.math.columbia.edu/download/book.pdf',
'frobenius map':'https://stacks.math.columbia.edu/tag/0CC6',
'galerkin method':'https://encyclopediaofmath.org/wiki/Galerkin_method',
'jacobi identity':'https://mathworld.wolfram.com/JacobiIdentities.html',
'kolmogorov complexity':'https://mathworld.wolfram.com/KolmogorovComplexity.html',
'levi problem':'https://encyclopediaofmath.org/wiki/Oka_theorems',
'front set':'https://en.wikipedia.org/wiki/Wave_front_set',
}
# Tiny conservative grammar vocabulary. If true in source snippet, likely not a term.
DISCOURSE={'so','unlike','precisely','sometimes','automatically','apparently','hence','therefore','thus','whereas','because','without','except','rather','indeed','note','given','specified','original','henceforth','separately','means','called','denotes','such','assume','suppose','adjective','literally','latter','former','instead','resulting','furthermore','moreover'}
CLAUSE_VERBS={'are','is','were','was','be','been','being','has','have','had','does','did','do','will','would','might','may','can','could','should','must','satisfies','implies','yields','defines','determines','characterizes','identifies','indicates','involves','requires','admits','consists','consisting','correspond','corresponds','having','containing','denoting','reaches','using','specified','allows','assumes','follows','occur','occurs','ensures','factors','presents','represents','recovers','represents','restricts','preserves','gives','gave','provides','chosen','choose','chooses','used','uses','multiply','multiplies','differentiate','differentiates','approximates','classifies','specify','shown','compare','gives'}
# In prose, these are qualifiers, rarely independent mathematical nomenclature.
GENERAL_QUALIFIERS={'common','broader','alternative','adopted','categorical','category','default','intended','usual','standard','additional','further','stronger','weaker','more','most','least','smaller','smallest','larger','largest','individual','analogous','respective','other','same','original','particular','certain','basic','appropriate','allowed','admissible','given','related','prescribed','corresponding','associated','compatible','actual','classical','literal','mere','valid','first','second','third','initial','final','some','any','other','many','few','listed','ordinary','general','specific','specified','unqualified','conventional','weaker','stronger','valid','entire','extra','additional','different','another','each','every','multiple','various','several','nonempty'}
EXPOSITION_END={'assumption','assumptions','condition','conditions','convention','conventions','case','cases','sense','contexts','context','hypothesis','hypotheses','notation','interpretation','usage','wording','claim','proof','constraint','bounds','steps','data','approach','methodology','presentation','perspective'}
# Terms that are named through those otherwise generic suffixes.
EXPOSE_EXCEPT={'boundary conditions','initial conditions','kkt conditions','cocycle conditions','cancellation axioms','coherence axiom','coherence axioms','coherence identity','empty-product convention','chain rule','least-upper-bound property','standard measure','integrability condition'}
PROSE_OPEN={'a','an','the','in','on','of','for','to','under','over','without','from','between','into','onto','so','unlike','precisely','sometimes','automatically','adjective','term','phrase','paper','papers','authors','source','sources','that','those','which','one','two','three','four','every','all','each','some','any','there','here','then','using','given','form','forms','ensures','equivalently'}
NOUN_LIST={'objects','arrows','functors','spaces','fields','subgroups','ideals','equations','elements','classes','categories','functions','sets','maps','morphisms','polynomials','subsets','operations','conditions','ring','module','category'}
PREFIX_NEXT={'space','spaces','series','ring','rings','topology','theorem','vector','field','fields','maps','map','algebra','algebras','module','modules','function','functions','operator','operators','category','categories','problem','set','sets','metric','group','groups','domain','domains','polynomial','polynomials','equation','equations','spectrum','closure','form','forms','measure','measures','value','values','inequality','identity','identities','distribution','distributions','morphism','morphisms','continuity','derivative','differential','differentials','structure','structures','homomorphism','homomorphisms','sheaf','sheaves','cohomology','homology','complex','complexes','manifold','manifolds','subset','subsets','ideal','ideals','subspace','subspaces','element','elements','family','families','class','classes','sequence','sequences','formulation','formulas','formula','property','properties','process','processes'}

# Not all common mathematically meaningful compositions warrant a dedicated
# definition. These remain reversible for future user adjudication.
DESCRIPTOR_END={'coefficient','coefficients','point','points','object','objects','values','value','variables','variable','event','events','subsets','sets','class','classes','families','family','elements','element','domains','domain','integers','integer','symbols','symbol','maps','morphisms','formulas','functions','function','sequences','sequence','charts','lines','indices','condition','property','curves','chains','spaces','space','operators','operator','roots','subgroups','terms','bound','bounds','coordinates','weights','coefficients','relations','cases'}

TECH_ENDS={'axiom','axioms','identity','identities','metric','distance','topology','morphism','homomorphism','bijection','isomorphism','mapping','map','method','measure','algebra','cohomology','group','scheme','stack','ring','module','ideal','field','derivative','differential','kernel','functor','category','space','set','polynomial','sequence','limit','convergence','continuity','distribution','projection','problem','complex','extension','representation','completion','localization','operator','transformation','invariant','dimension','power','trace','geodesic','isometry','model','theorem','formula','equation','partition','process','order','relation','graph','matroid','system','hull','hom','series','cover','closure','symbol','form'}
TECH_MODS={'abelian','algebraic','analytical','analytic','artinian','borel','carleson','cartier','cauchy','finitely','countably','cofiltered','cofinal','graded','filtered','holomorphic','meromorphic','projective','injective','surjective','bijective','isomorphic','isometric','locally','integrally','normed','dense','closed','open','preordered','ordered','topological','real','complex','kähler','hausdorff','weak','strong','finite','free','positive','negative','coherent','covariant','contravariant','functorial','fibre','fibred','infinite','noetherian','artinian','jordan','lie','unit','unital','formal','principal','prime','proper','relative','invariant','initial','terminal','natural','universal','inverse','direct','dual','exterior','homotopy','absolute','quasi-coherent','torsion-free','normal','left','right','stochastic','poincaré','frobenius','taylor','bessel','brownian','galerkin','reduced','k-linear','r-linear','finite-type','nonarchimedean','geometrically','smooth','regular','reproducing','strongly','weakly','uniform','operator','test','binary','homological','derived','noncommutative','nonlinear','symmetric','antisymmetric','multiplicative','additive','cohomological','equivariant','local','lexicographic','precompact','homogeneous','stable','associated','barycentric','cartesian','chain','closed','minimal','maximal','regular'}


def source_next_tokens(phrase,context):
    # Context has normalized snippet and may contain a truncated phrase. Only
    # count exact contiguous phrase boundaries, not internal word matches.
    out=[]
    for snip in context.split(' | '):
        for m in re.finditer(r'(?<![\w-])'+re.escape(phrase)+r'(?![\w-])',snip,flags=re.I):
            after=snip[m.end():].strip().split()
            before=snip[:m.start()].strip().split()
            out.append((before[-1].lower() if before else '', after[0].lower() if after else ''))
    return out


def classify(phrase,ctx):
    p=phrase.casefold().strip()
    w=p.split()
    if p in TERM_VARIANTS:
        return 'term_variant','regular_inflection','Plural or spelling variant of '+TERM_VARIANTS[p]+'; link to canonical notion before separate admission','high'
    if p=='front set':
        return 'descriptive_not_separate_term','wave_front_set_fragment','Source means wave front set; clipped two-word phrase is not separately named','high'
    if p in KNOWN_TERMS:
        return 'recognizable_technical_term','curated_math_terminology','Independent mathematical term/construction recognized; verify missing status and conventions','high'
    if not w:
        return 'false_positive','empty_fragment','empty phrase','high'
    if w[0] in PROSE_OPEN or (len(w)>=3 and w[0] in DISCOURSE):
        return 'false_positive','leading_prose','starts as an ordinary sentence, instruction, or discourse phrase','high'
    if any(x in CLAUSE_VERBS or x in DISCOURSE for x in w):
        return 'false_positive','clause_or_discourse','contains finite verb / grammatical connective; not an independent term heading','high'
    if w[-1] in {'and','or','of','in','for','to','by','with','without','under','over','an','the','from'}:
        return 'false_positive','incomplete_connector','ends on grammatical connector','high'
    if p in CONTEXTUAL_FROM_REVIEW:
        return 'descriptive_not_separate_term','context_checked_composition','Mathematical words form a contextual description or parameterized instance; no separate heading established','medium'
    if p in EXPOSITORY_EXACT:
        return 'descriptive_not_separate_term','confirmed_contextual_wording','Ordinary descriptive or expository wording; no separate mathematical head required','high'
    if w[-1] in EXPOSITION_END and p not in EXPOSE_EXCEPT:
        return 'descriptive_not_separate_term','convention_or_assumption','Discussion of a convention, assumption, hypothesis, or context rather than a standalone named term','medium'
    if w[0] in GENERAL_QUALIFIERS and w[-1] not in {'homomorphism','topology','space','field','ring','category','module','ideal','group','map','sequence','problem','subgroup','polynomial','measure','dimension','continuity','equivalence','order','complex','segment','operator','property','vector','algebra'}:
        return 'descriptive_not_separate_term','generic_qualifier','Ordinary generic qualifier attached to an existing mathematical noun','medium'
    if w[0] in GENERAL_QUALIFIERS and len(w)>2 and (w[1] in {'an','a','every','this','the','are','by','of','for','in','with'}):
        return 'false_positive','generic_sentence_fragment','Description crossing grammatical boundaries','high'
    follow=source_next_tokens(p,ctx.get('source_snippets',''))
    if follow and len(follow)>=1 and all(after in PREFIX_NEXT for _,after in follow) and p not in EXPOSE_EXCEPT:
        # Some valid technical terms have expanded names in contexts; avoid
        # decisive rejection if phrase independently recognized above.
        return 'descriptive_not_separate_term','incomplete_prefix_in_sources','Phrase is consistently a prefix of a longer mathematical expression in its cited context','medium'
    if len(w)>=4 and w[0] in {'so','unlike','sometimes','therefore','given','without','with','specified','including','from','among'}:
        return 'false_positive','long_prose_fragment','Prose clause not an independent heading','high'
    if w[0] in {'smallest','largest','smaller','bigger','larger','lower','higher','minimal','maximal','maximum','minimum'} and len(w)>=3:
        return 'descriptive_not_separate_term','extremal_description','Qualifies an extremal choice or description, not a separately named construction','medium'
    if len(w)>=4:
        if any(x in {'an','a','the','of','with','without','under','and','or','from','through','by','into','onto','over','in','on','for','to'} for x in w[1:-1]):
            return 'requires_deeper_research','long_technical_relation','Could express a technical relationship, but may be compositional; check before admitting','unresolved'
        if w[-1] in TECH_ENDS and (w[0] in TECH_MODS or any(x in TECH_MODS for x in w[1:3])):
            return 'possible_independent_term','multiword_technical_phrase','Qualified technical phrase; check convention and existing coverage','medium'
        return 'requires_deeper_research','long_compound','Long compound; classification needs independent-source check','unresolved'
    if len(w)==2 and w[0] in TECH_MODS and w[1] in TECH_ENDS:
        return 'possible_independent_term','technical_qualifier','Recognizable mathematical qualifier + concept, independence and coverage not established','medium'
    if len(w)==3 and w[-1] in TECH_ENDS and all(x in TECH_MODS for x in w[:2]):
        return 'possible_independent_term','compound_technical_qualifier','Potential named specialized concept; compare with existing definition','medium'
    if len(w)==2 and w[0] in GENERAL_QUALIFIERS:
        return 'descriptive_not_separate_term','generic_descriptive_noun','Ordinary qualifier of a known object, not itself a distinct concept','medium'
    if len(w)==2 and w[-1] in DESCRIPTOR_END and w[0] not in TECH_MODS:
        return 'descriptive_not_separate_term','unqualified_description','Unqualified descriptive noun phrase; no independent terminology indicated','medium'
    if len(w)==3 and w[0] in GENERAL_QUALIFIERS and w[-1] in DESCRIPTOR_END:
        return 'descriptive_not_separate_term','generic_compound_description','Generic qualified description rather than independent mathematical term','medium'
    # Any term not positively understood is retained, never silently rejected.
    return 'requires_deeper_research','uncertain_terminology','Potential technical meaning not reliably resolved by grammar or contextual evidence','unresolved'


def run(root:Path,out:Path,survivor_dir:Path|None=None,context_dir:Path|None=None):
    survivors=load_tsv(survivor_dir or root/'survivor_batches')
    contexts=load_tsv(context_dir or root/'contextual_batches')
    cx={r['candidate_id']:r for r in contexts}
    queue=[r for r in survivors if r['disposition']=='needs_targeted_review']
    assert len(survivors)==3109 and len(queue)==2175,(len(survivors),len(queue))
    assert len({r['candidate_id'] for r in queue})==2175
    out.mkdir(parents=True,exist_ok=True)
    records=[]
    for row in queue:
        c=cx[row['candidate_id']]
        phrase=row['phrase']
        status,code,reason,confidence=classify(phrase,c)
        records.append({
            'candidate_id':row['candidate_id'],'phrase':phrase,
            'review_status':status,'reason_code':code,'reason':reason,
            'confidence':confidence,'original_pass5_status':row['disposition'],
            'source_ids':c['source_ids'],'source_titles':c['source_titles'],
            'source_snippets':c['source_snippets'],
            'reference_url':SOURCES.get(phrase.casefold(),''),
            'edited_definition':False,'reversible':True,
            'source_feed_sha256':CANONICAL_FEED,
        })
    cols=list(records[0]);
    for p,rs in [('full_review.tsv',records),('research_queue.tsv',[x for x in records if x['review_status'] in {'recognizable_technical_term','possible_independent_term','requires_deeper_research'}])]:
        with (out/p).open('w',encoding='utf8',newline='') as f:
            wr=csv.DictWriter(f,fieldnames=cols,delimiter='\t',lineterminator='\n');wr.writeheader();wr.writerows(rs)
    counts=collections.Counter(x['review_status'] for x in records)
    reasons=collections.Counter((x['review_status'],x['reason_code']) for x in records)
    report={
        'schema':VERSION,'input':len(queue),'original_pass5_input':len(survivors),
        'counts':dict(sorted(counts.items())),
        'active_research':sum(counts[x] for x in ('recognizable_technical_term','possible_independent_term','requires_deeper_research')),
        'provisional_suppressed':sum(counts[x] for x in ('descriptive_not_separate_term','false_positive','term_variant')),
        'rule_counts':[{'status':a,'rule':b,'count':n} for (a,b),n in reasons.most_common()],
        'samples':{k:[r['phrase'] for r in records if r['review_status']==k][:25] for k in counts},
        'notes':[
            'Not a proof of definition validity or absence from published corpus.',
            'Suppression reversible and restricted to independent-term research queue.',
            'Sources reflect selected external references, not universal research coverage.',
            'User-approved overrides take precedence; original catalog untouched.'
        ]
    }
    (out/'summary.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return records,report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=ROOT);p.add_argument('--output',type=Path,default=ROOT/'results');p.add_argument('--survivor-dir',type=Path);p.add_argument('--context-dir',type=Path);a=p.parse_args();run(a.input,a.output,a.survivor_dir,a.context_dir)