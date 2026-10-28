#!/usr/bin/env python3
"""Aggressive, fully reversible independent-terminology triage of remaining mathDef leads.

This script is an editorial worklist classifier, not a proof of mathematical
validity or independent verification of accepted entries. Only the active
7,240-case subpool is touched; historical discoveries remain intact.
"""
from __future__ import annotations
import csv,collections,re,hashlib,unicodedata,zipfile,json,random
from pathlib import Path
from functools import lru_cache

import argparse
PARSER=argparse.ArgumentParser(description=__doc__)
PARSER.add_argument('--snapshot',type=Path,required=True)
PARSER.add_argument('--checkpoint',type=Path,required=True)
PARSER.add_argument('--source-review-dir',type=Path,required=True)
PARSER.add_argument('--output',type=Path,required=True)
ARGS=PARSER.parse_args() if __name__=='__main__' else None
if ARGS:
 ROWS=[]
 for path in sorted(((ARGS.source_review_dir/'batches') if (ARGS.source_review_dir/'batches').is_dir() else ARGS.source_review_dir).glob('*.tsv')):
  with path.open(encoding='utf-8',newline='') as source:
   ROWS.extend(r for r in csv.DictReader(source,delimiter='\t')
               if r.get('review_class')=='deeper_research')
 SNAPSHOT=json.loads(ARGS.snapshot.read_text(encoding='utf-8'))
 CP=json.loads(ARGS.checkpoint.read_text(encoding='utf-8'))
else:
 ROWS=[];SNAPSHOT={'definitions':[]};CP={'formulations':{}}
FULL_TEXT={f['key']:f['body'] for d in SNAPSHOT['definitions'] for f in d['formulations']}
if ARGS:
 assert len(ROWS)==7240 and len(FULL_TEXT)==2104
 assert CP['last_feed_sha256']=='0441b9c5fc2f7a515c3210a7471a3a3e8f9ca0b8dc63f570dcc8e1cb38a08fe2'
WORD=re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*",re.U)
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$|\\\(.*?\\\)|\\\[.*?\\\]',re.S)
COMMAND=re.compile(r'\\[A-Za-z]+(?:\[[^]]*\])?',re.U)
TOKEN_CACHE={}
for fid,original in FULL_TEXT.items():
 text=unicodedata.normalize('NFKC',original)
 for rx in (MATH,COMMAND): text=rx.sub(lambda m:' '*len(m.group()),text)
 matches=list(WORD.finditer(text))
 words=[m.group().casefold() for m in matches]
 if words!=CP['formulations'][fid]['words']:
  continue
 TOKEN_CACHE[fid]=(words,[m.span() for m in matches],text,original)
if ARGS: assert len(TOKEN_CACHE)>=2090,len(TOKEN_CACHE)

def norm(s):
 return ' '.join(WORD.findall(unicodedata.normalize('NFKC',s).casefold().replace('_',' ')))
def singular(p):
 w=p.split()
 if not w:return p
 last=w[-1]
 if last.endswith('ies') and len(last)>5:w[-1]=last[:-3]+'y'
 elif last.endswith('sses') and len(last)>5:w[-1]=last[:-2]
 elif last.endswith('s') and not last.endswith(('ss','us','is','ics')) and len(last)>3:w[-1]=last[:-1]
 return ' '.join(w)
KNOWN={}
for d in SNAPSHOT['definitions']:
 for title in [d['term'],*d.get('aliases',[])]:
  for k in {norm(title),norm(title).replace('-',' ')}:
   KNOWN.setdefault(k,[]).append({'title':title,'id':d['id']})
KNOWN_SINGLE=set(' '.join(k.split()[:1]) for k in KNOWN)
KNOWN_FINAL={k.split()[-1] for k in KNOWN if k and len(k.split())>=2}

MATH_NOUN=set('''abelian algebra algebraic algebraist algorithm analysis analytic angle angles approximation arrow arrows automaton automata automorphism automorphisms ball balls basis bases boundary bundle bundles cardinal cardinality category categories chain chains class classes closure cohomology coefficient coefficients colimit colimits compactification compactness component components condition conditions cone connection continuity convergence convolution correspondence cover covering curve curves cycle cycles degree decomposition definition derivative derivation derivatives determinant difference differential differentiability dimension dimensions distribution divisor divisors domain domains dual duality embedding endomorphism endpoint endpoints equality equation equations equivalence error errors evaluation event events extension extensions factor factorization family families field fields filter filters filtration flow form forms formula formulas frame function functions functional functionals functor functors germ germs graph graphs group groups homology homomorphism homeomorphism ideal ideals identity image images immersion index indices injectivity integral integrals interior interpolation intersection invariant isometry isomorphism kernel kernels lattice lattices length limit limits line lines manifold manifolds map maps mapping mappings matrix matrices measure measures metric metrics model models module modules monoid monoids morphism morphisms neighborhood neighborhoods neighbourhood norm norms normalization number numbers object objects operator operators order ordering orbit orbits pair pairs path paths point points polynomial polynomials power powers predicate predicates prime primes probability process processes product products projection projections property properties quotient radical rank ratio ratios relation relations representation representations residue resolution ring rings root roots rule rules scheme schemes section sections sequence sequences series set sets sheaf sheaves singularity space spaces spectrum sphere spheres stability stack stacks structure structures subgroup subgroups submodule submodules subset subsets subspace subspaces sum sums surface symbol symbols symmetry tensor tensors theorem theory topology transformation union value values variable variables variety varieties vector vectors vertex vertices volume weight weights word words'''.split())
TECH_MOD=set('''abelian absolute affine algebraic analytic annular artinian associative asymptotic atomic automorphic automorphism banach base-based basic bergman bessel bilinear binary biregular borel bounded canonical cartesian cauchy central chain closed cofinite compact complete complex connected continuous countable covariant cyclic dense derived differentiable differential discrete distributive dual effective elliptic endomorphic equivariant exact exponential faithful finite finitely filtered free frechet gaussian generic geodesic global graded hausdorff hermitian hilbert holomorphic homogeneous hyperbolic ideal imaginary induced injective integral interior internal invariant invertible irreducible isometric isomorphic jordan kahler laplace left lie linear local locally logarithmic maximal measurable meromorphic metric minimal mixed modular monic monotone multiplicative natural negative nilpotent noncommutative nonempty nonlinear nontrivial nonzero normal normed noetherian nowhere open opposite ordered ordinary orthogonal partial perfect periodic polynomial positive prime principal primitive projective proper pure quasi rational real reduced reflexive regular relative relatively right scalar separable simple simply smooth solvable spectral spherical stable standard strict subanalytic subcanonical subdirect sublinear submultiplicative surjective symmetric tangent tensor topological torsion total totally transfinite trivial unbounded uncountable unital universal upper uniform unitary weak weakly well zero zariski'''.split())
# Learn mathematical concept heads from ALL current production headings.
MATH_NOUN.update(KNOWN_FINAL)
MATH_NOUN.update('''axiom axioms preorder preorders system systems operation operations calculus integration invariant invariants duality dualities conjugacy partition partitions compactness discontinuity solution solutions principle principles monad monads adjunction adjunctions cobordism lemma lemmas centralizer centralizers normalizer normalizers coordinate coordinates bracket brackets characteristic characteristics computation computations argument arguments combination combinations derivative derivatives eigenvalue eigenvalues eigenspace eigenspaces recurrence reduction induction compactification spectrum spectra integration geometry dynamical systems dynamics semigroup semigroups diagram diagrams convention conventions semimartingale process processes distributions distribution polygon polygons polytope polytopes method methods variation boundary indicator indicators array arrays row rows operations elements matrices matrix homology homotopy coherence field theory normality equality inequalities smoothness equivalences formalism period periods trivialization intersection operations transformations discriminant singularities singularity symbol symbols convention hypothesis hypotheses objects maps image images inversion conditions subalgebra category product topology'''.split())

GENERIC_ADJ=set('''a an the this that these those those their its some any all every each either another other different same specified particular appropriate suitable certain arbitrary chosen given various additional further respective relevant arbitrary possible potential general usual familiar typical typical resulting corresponding associated related underlying sufficient necessary enough particular entire full multiple many more most most numerous one two three four five distinct separate distinct unspecified certain ordinary conventional predetermined explicit implicit approximate precise possible fixed nonempty empty infinite finite bounded unbounded local global large small extra supplementary such natural enough important only proper regular smooth perfect strict normal real complex positive negative'''.split())
# Domain-known names among the borderline pool. These are leads only, NOT verified missing definitions.
SEED_KEEP=set('''lie bracket|local homology|moore category|toeplitz operator|carleson-tent characteristic|metrizability condition|slater's condition|generic filter|finite rank vector bundle|finite-rank vector bundle|negative-infinity locus|order-theoretic filter|empty sum|joint distributions|generalized eigenspaces|reproducing-kernel hilbert space|monoidal structure|moment bounds|monge ampère measure|monge-ampère measure|minkowski combination|adapted sequence|mollifier family|nonempty polyhedron|finite diagram|transition map|vector bundle|nontrivial bergman hilbert space|normal cone|local principal ideal domain|immersed lie subgroup|infinite index|infinite-dimensional complex hilbert space|n-fold tensor powers|outer approximation|positive waiting times|geodesic metric|birkhoff uniform-recurrence convention|abelian category|module categories|cr manifold|quotient-group structure|model category|finite intersection|weakly equivalent|weak convergence|closed immersion|open immersion|free resolution|finite resolution|trivialization|flat connection|local cohomology|homomorphism of commutative rings|finite-sample bias|formal filtered colimit|smoothing order operators|numerical radius|gromov-hyperbolic|semisimple module|integral closure'''.split('|'))
KEEP_EXPLICIT_EXTRA=set('''octahedral axiom|specialization preorder|dynamical systems|dynamical system|contractible complex|contractible complexes|duality data|inversion map|extension of scalars|localized ring|row operations|neighborhood base|weighted minkowski combination|bochner integral|monge ampère measure|monge-ampère measure|rham cohomology|de rham cohomology|algebraic field extension|closed ray|monoidal structure|nontrivial bergman hilbert space|finite image|global dimension|local cohomology|moore category|geodesic equation|linear wave equation|empty sum|empty intersection|slater's condition|adapted sequence|kernel support|lie bracket|simplicial complex|variation of constants|cauchy problem|semisimple ring|finitely generated ideal|finite type scheme|formal sums|singular cohomology|annihilator ideal|least upper bound|zero divisor|finite-dimensional subspace|weak convergence|closed partition|fréchet space|frechet space|fixed point property|prime spectrum|topological space|normal cone|complex vector bundle|reproducing kernel|multiplication operator|eilenberg-moore category|joint distributions|subspace lattice|coordinate transformations|moduli space|chain homotopy|homological dimension|presentation matrix|multivariate polynomial|noncommutative ring|integral closure|algebraic closure|metric completion|quasi-compact opens|proper morphism|smooth morphism|trivialization|complex coordinate|zero ideal|enveloping algebra|quotient ring|nonzero quotient|failure symbol'''.split('|'))

# Mathematical vocabulary exceptions from quality audit (not certified new definitions).
KEEP_EXPLICIT_EXTRA.update('test space|mass function|outward normal derivative|relative de rham complex|monic irreducible minimal polynomial|tucker kkt conditions|absolutely convergent sum|measured space|failure symbol|monte carlo randomized algorithm|formal filtered colimit|complex rank|smooth vector field|algebraic field extension|positive probability measure|permutation group|compact support|convergence in probability|convex quadratic program|regularity condition|finite composition series|open immersion|analytic subvariety|fraction field|piecewise polynomial|conditional expectation|weakly convergent sequence|matrix condition number|radon measure|ring with identity|group action|closure operator|compact convex subset'.split('|'))
TECH_MOD.update('outward test mass minkowski weighted bochner monte carlo tucker kkt rham kahler carleson octahedral specialization absolute probabilistic stochastic expected magnetic abstract tempered locally induced bessel factor quasicoherent spectral eilenberg infinitesimal bilinear multilinear polytopal weakly pointwise measurable distributional inverse adapted conic noncompact compactly analytic regularity contractible conditional ordinary equivalent'.split())
KEEP_EXPLICIT_EXTRA.update('''fixed field|formal power series|maximum clique|koszul formula|i-adic completion map|commuting projection|vegas randomized algorithm|commutative ring map|truth values|leading coefficient|indexing set|discrete-time stochastic process|whitney construction|gaunt category|ambient topology|curvature bounds|finite cw complex|essential isolated singularity|kernel of evaluation|one-dimensional affine subspace|finite residue field|countably infinite index set|zero-dimensional scheme|overfield|prime decomposition|positive scalar multiples|test function|proof system|semigroup action|propositional formula|normal form|local field|absolute moment|analytic hypersurface|set-theoretic section|generalized continuum hypothesis|fock space|bessel-potential sobolev space|order-theoretic filter|weak equivalence|finite product|regular representation|affine blowup|homogeneous localization'''.split('|'))
NORMAL_DESCRIPTIONS={'standard convention','exact arithmetic','finite time','finite integer','infinite values','positive probability','positive weights','rational epsilon','real coefficients','associative conventions','ordinary category','compact time','infinite subset','imaginary parts'}

KEEP_EXPLICIT_EXTRA.update('codimension one|dyadic characteristic|defining relations|finite CW complex|worst-case polynomial time|maximum matching'.casefold().split('|'))
SUBJECT=set('''element elements variable variables quantity quantities given let suppose assume consider choose take set class case example fact proof theorem definition note remark statement construction observation interpretation assumption hypothesis assertion consequence result condition conditions part section scenario setting situation discussion choice option method approach interpretation instance convention contexts context comparisons requirements hypotheses stipulation treatment application manner means time times dimension dimensions point points set sets any all every those these some each most different another other same possible further more one two three four five order way ways type types kind kinds structure data item items input output cost information status cases'''.split())
FINITE_VERBS=set('''is are was were be been being has have had do does did can could may might must will would should shall require requires required prove proves proven imply implies yield yields follow follows contain contains consist consists form forms define defines denote denotes mean means let lets assume assumes consider considers choose chooses take takes use uses show shows state states holds hold obtain obtains exists exist preserves preserve depend depends vary varies assign assigns apply applies measure measures arise arises holds becomes become gives give say says need needs require requires allows allow permit permits indicate indicates include includes count counts corresponds correspond extend extends admit admits send sends map maps sets forms subtracts compute computes determine determines satisfies satisfy distinguish distinguishes use uses choose chooses given give yields generate generates acts act exist exists approaches approach operate operates yield yields detected detects accept accepts reject rejects describes describe require requires impose imposes remain remains'''.split())
FINITE_AMBIGUOUS=set('''form forms cover covers map maps state states count counts measure measures order orders number numbers value values function functions ring rings group groups filter filters flow flows set sets lie lies sign signs path paths point points'''.split())
PARTICIPLES=set('''being having using taking given forming involving containing consists satisfying assuming requiring allowing making finding obtaining including preserving fixing defining mapping sending showing demonstrating considering depending choosing ensuring representing covering comparing computing applying joining varying associating yielding taking wanting remaining assigning limiting restricting adapting requiring extending equipping occurring appearing corresponding combining'''.split())
PREP=set('''of in on with for from to by under over between within into onto towards around after before across through without above below at against as unless if while when where during upon along among throughout'''.split())
CONNECTOR=set('''and or but as if then than otherwise whenever whereas because although though however nevertheless moreover further furthermore respectively similarly meanwhile particularly normally usually necessarily merely often sometimes generally typically specially hence thus therefore namely equivalently roughly rather also even especially indeed additionally so nor yet else already still only not'''.split())
PUNCT_STOP=set('.,;:!?\n')

def evidence(phrase):
 p=phrase.split();n=len(p)
 distinct_source=0; occurrence=0; cross_strong=0; cross_math=0; next_tokens=collections.Counter();prev_tokens=collections.Counter(); follows=[];precedes=[]
 for fid,f in CP['formulations'].items():
  if phrase not in f['phrase_counts']: continue
  o=TOKEN_CACHE.get(fid)
  if not o:continue
  words,spans,text,original=o; found=False
  for i in range(len(words)-n+1):
   if words[i:i+n]!=p:continue
   found=True;occurrence+=1
   segs=[original[spans[k][1]:spans[k+1][0]] for k in range(i,i+n-1)]
   if any(any(s in gap for s in PUNCT_STOP) for gap in segs):cross_strong+=1
   if any(('\\' in gap or '$' in gap or len(gap)>10) for gap in segs):cross_math+=1
   if i+n<len(words):next_tokens[words[i+n]]+=1
   if i>0:prev_tokens[words[i-1]]+=1
   if len(follows)<3:follows.append(' '.join(words[i+n:i+n+5]))
   if len(precedes)<3:precedes.append(' '.join(words[max(0,i-4):i]))
  if found:distinct_source+=1
 return {'observed_count':occurrence,'source_count':distinct_source,'cross_punctuation':cross_strong,
  'cross_math':cross_math,'next':next_tokens,'prev':prev_tokens,
  'next_examples':follows,'prev_examples':precedes}

def known_match(phrase):
 for p in {phrase, phrase.replace('-',' '), singular(phrase),singular(phrase.replace('-',' '))}:
  if p in KNOWN:return KNOWN[p][0]['title']
 return None

def prefix_of_published(phrase):
 # Prefix only, never assume a strict prefix is not a meaningful concept by itself.
 s=phrase+' '
 return [k for k in KNOWN if k.startswith(s) and len(k.split())<=len(phrase.split())+2]

# Carefully selected exception examples to protect valid mathematical terms.
KEEP_EXPLICIT=set('''homomorphism of commutative rings|order-theoretic filter|complex vector bundle|nontrivial bergman hilbert space|finite-rank vector bundle|finite diagram|n-fold tensor powers|infinite index|turing machine|moore category|strictly positive waiting times|euclidean spaces|nonempty polyhedron|singular finite positive measures|monoidal structure|mollifier family|piecewise polynomials|ideal class|finite sequence|empty intersection|empty sum|infinite-dimensional complex hilbert space|finite-dimensional vector space|conformal metric|complete metric|pointwise convergence|geodesic metric|smooth vector field|union of sets|finite union|fundamental group|normal cone|local principal ideal domain|scalar product|ring of integers|Bergman Toeplitz operator|Toeplitz operator|first-order condition|left r-modules|normed spaces|rham cohomology|de rham cohomology|closure of subsets|abelian groups|dense open subsets'''.casefold().split('|'))

# Known generic surface patterns likely to be sentence pieces, or contextual descriptions.
DISCOURSE_ONSETS=set('''of in on with for to from by at under over between within into onto as when while where if however thus hence therefore also otherwise moreover further similarly respectively some other different more most whenever unless despite because though although assuming involving requiring satisfying having being using taking without above below among around after before'''.split())

# Return classification, rule, reason, confidence. All suppression remains reversible.
def classify(row,ev):
 p=row['phrase'];w=p.split();n=len(w);last=w[-1];first=w[0];fc=int(row['formulation_count'])
 prev=ev['prev']; nxt=ev['next']; obs=ev['observed_count']
 named=known_match(p)
 if named:return 'existing_definition','published_title_or_alias',f'exact/inflected existing heading: {named}', 'high'
 if p == 'open and closed':
  return 'existing_definition','clopen_synonym','open-and-closed property of a subset is covered by existing clopen-set definition','medium'
 if p in NORMAL_DESCRIPTIONS:
  return 'remove_description','targeted_generic_description','ordinary prose qualification, not a standalone technical term','high'
 if p in {'smooth vector','algebraic field','compact topological','proper vertex','connected closed'}:
  return 'remove_fragment','targeted_incomplete_noun','observed expression is a clipped prefix of longer mathematical construction','high'
 if p in SEED_KEEP or p in KEEP_EXPLICIT or p in KEEP_EXPLICIT_EXTRA:
  return 'candidate_lead','known_technical_concept','recognized technical object; validate naming/conventions and published coverage','high'
 if obs and ev['cross_punctuation']==obs:
  return 'remove_false_positive','punctuation_boundary','all recorded occurrences cross sentence/punctuation boundary','high'
 if obs and ev['cross_math']==obs:
  return 'remove_false_positive','math_gap_boundary','all recorded occurrences cross removed mathematical notation','high'
 if first in DISCOURSE_ONSETS:
  return 'remove_false_positive','leading_function_word','candidate begins at a grammatical connector/preposition','high'
 if last in CONNECTOR or last in PREP:
  return 'remove_false_positive','open_grammar_tail','candidate ends at incomplete grammatical connector/preposition','high'
 if any(x in CONNECTOR for x in w[1:]) and len(w)>2:
  return 'remove_false_positive','embedded_discourse','contains sentence-level connector rather than a mathematical name','high'
 if any(x in FINITE_VERBS-FINITE_AMBIGUOUS for x in w):
  return 'remove_false_positive','finite_verb','finite verbal clause, not a term heading','high'
 if first in PARTICIPLES:
  return 'remove_false_positive','initial_participle','begins with a verbal participle rather than a mathematical noun','high'
 if any(x in {'this','these','those','their','its','whose','some','each','every','that'} for x in w):
  return 'remove_false_positive','anaphoric_determiner','context-dependent reference to surrounding sentence','high'
 if 'one' in w or 'two' in w or 'three' in w or 'four' in w or 'more' in w or 'most' in w:
  # Many genuine named terms have numbers. Exempt hyphenated or known math concepts.
  if first in ('one','two','three','four','more','most') and first+'-' not in p:
   return 'remove_description','bare_quantifier','ordinary numerical/quantifier description rather than established standalone term','medium'
  if any(x in ('one','two','three','four','more','most') for x in w[1:]):
   return 'remove_false_positive','cross_quantified_clause','quantifier in middle of candidate indicates sentence fragment','high'
 if last in {'form','forms'} and len(w)>=2 and w[-2].endswith('s') and ev['next'].get('a',0)+ev['next'].get('an',0)+ev['next'].get('the',0)>=1:
  return 'remove_false_positive','plural_subject_verb','plural noun followed by finite verb form(s)','high'
 if any(x in {'when','whenever','while','unless','because','although','though'} for x in w[1:]):
  return 'remove_false_positive','embedded_clause_connector','clause boundary in purported noun phrase','high'
 if first in ('another','different','additional','further','various','specified','certain','particular','suitable','appropriate','sufficient','necessary','corresponding','respective','given','chosen','arbitrary','usual','normal','general','same','related','underlying','possible','potential'):
  return 'remove_description','generic_qualifier','contextual qualifier not demonstrated to name an independent mathematical notion','medium'
 if first in ('such','certain','other','every','some','any','each','every','all'):
  return 'remove_description','unspecified_quantifier','ordinary quantification, not an independent named notion','medium'
 if last in ('otherwise','again','however','first','second','third','also','only','some','such','many','one','two'):
  return 'remove_false_positive','dangling_terminal','phrase ends with sentence-level adverb/quantifier','high'
 if p.endswith(("'s", "’s")):
  return 'remove_false_positive','possessive_without_head','incomplete possessive mathematical phrase','medium'
 # Truncated term: last word adjective; next word consistently heads a longer concept.
 if last in TECH_MOD or last in {'linear','normed','bounded','complex','real','affine','smooth','continuous','locally','first','second','right','left','nondeterministic','finite-dimensional','infinite-dimensional','open','closed','group','module'}:
  if nxt:
   most,count=nxt.most_common(1)[0]
   if most in MATH_NOUN and count/max(obs,1)>=0.65 and p+' '+most not in KEEP_EXPLICIT:
    return 'remove_fragment','adjective_boundary',f'usually followed by {most!r}; phrase clips a longer mathematical noun', 'medium'
 # Descriptive compounds anchored by commonplace modifiers rather than convention name.
 if first in {'nonempty','nonzero','finite','infinite','bounded','unbounded','unique','usual','specified','certain','arbitrary','further','given','different','appropriate','relatively','corresponding','positive','negative','distinct','fixed','chosen'} and n>=2:
  if n==2 and last in MATH_NOUN and first in {'finite','infinite','bounded','unbounded','positive','negative','relatively'}:
   # e.g. finite measure, positive integer, bounded operator MAY be math concept -> keep.
   return 'candidate_lead','mathematical_modifier','standard mathematical qualifier plus mathematical object; verify independent definition','medium'
  return 'remove_description','compositional_qualification','generic property of an already specified mathematical object','medium'
 if n>=3 and first in {'sets','elements','objects','morphisms','points','vectors','matrices','functions','sequences','groups','rings','modules'} and any(x in {'of','in','on','with','for','to','from','by','under'} for x in w):
  return 'remove_description','ordinary_collection_relation','ordinary description of a collection/context; no independent named term established','medium'
 # Dedicated representation of condition relative to ambient data.
 if first in {'class','collection','pair','family','sequence','subcollection','set','subset','number','choice','value','elements','objects','list','sum','product','intersection','union'} and n>=3:
  if first in {'intersection','union','sum','product'} and n<=4 and last in MATH_NOUN:
   return 'candidate_lead','standard_operation','possible standard operation/invariant of an explicit mathematical object','medium'
  return 'remove_description','generic_relational_noun','compositional noun phrase; no distinct standalone notion evidenced','medium'
 # If the ORIGINAL source uses this uninterrupted technical phrase as a
 # grammatical subject of a definition ("X is", "X means"), it is a
 # credible candidate even when its head is not on a static whitelist.
 cue_count=sum(nxt.get(x,0) for x in ('is','are','means','denotes','consists','requires'))
 if (cue_count>=1 and last in MATH_NOUN and first not in
     {'family','collection','set','sets','element','elements','number','numbers',
      'one','two','three','four','all','some','any','several','many','general',
      'usual','arbitrary','specified','different','various','additional',
      'appropriate','corresponding','respective','possible','potential',
      'distinct','maximum','minimum','certain','same','entire'} and
     not any(x in CONNECTOR for x in w) and
     not (len(w)>3 and w[0] in MATH_NOUN and any(x in {'of','in','to','with'} for x in w))):
  return 'candidate_lead','definition_subject_cue','appears as named mathematical subject immediately before a definitional predicate; verify conventions','medium'
 # A specialist noun-headed expression that survived the syntactic boundary
 # checks must not be suppressed merely because its modifier is unfamiliar.
 # It may name a rare concept (e.g., a Koszul formula or gaunt category).
 if n==2 and last in MATH_NOUN and first not in GENERIC_ADJ and first not in SUBJECT:
  return 'needs_targeted_review','unfamiliar_technical_noun','mathematical head with non-generic modifier; verify as independent terminology','unresolved'
 if (n==3 and last in MATH_NOUN and first not in GENERIC_ADJ and
     first not in SUBJECT and not PREP.intersection(w) and
     (w[1] in TECH_MOD or w[1] in MATH_NOUN or '-' in w[0] or '-' in w[1])):
  return 'needs_targeted_review','unfamiliar_technical_compound','specialized technical compound; not safe to dismiss without mathematical check','unresolved'
 if n>=4:
  # Four+ word phrases: may be legitimate long named concepts, but require technical structure rather than arbitrary prose.
  if any(x in {'and','or','the','that','this','these','those','their','its','our'} for x in w):
   return 'remove_false_positive','compound_clause','crosses grammatical elements, not a standalone mathematical term', 'high'
  if first in {'finite','infinite','some','all','only','any','large','small','different','distinct','local','relative','real','complex','one','two','many'} and last in MATH_NOUN:
   return 'remove_description','compositional_long_description','qualified ambient mathematical construction; no independent term established','medium'
  if any(x in {'of','in','on','with','for','to','by','under','over','between','from','into'} for x in w):
   # technical named constructs often X of Y, but 4-5 word composites almost always object mentions.
   if (first in MATH_NOUN or first in TECH_MOD) and last in MATH_NOUN and fc>=2:
    return 'needs_targeted_review','specialized_relational_phrase','long technical relational phrase; could name an independent construction','unresolved'
   return 'remove_description','compositional_long_relation','contextual mathematical noun phrase without evidence of independent naming','medium'
  if first in TECH_MOD and last in MATH_NOUN:
   return 'candidate_lead','long_technical_compound','qualified mathematical concept; retain for rigorous verification','medium'
  if any(x in SUBJECT for x in w):
   return 'remove_description','generic_long_noun','long contextual noun construction, not a named mathematical term on present evidence','medium'
  return 'needs_targeted_review','unclassified_long_technical','long technical expression without decisive syntax or known naming','unresolved'
 if n==3:
  if first in MATH_NOUN and w[1] in PREP and last in MATH_NOUN:
   if fc>1 and first not in {'set','class','family','pair','collection','element','object','number','value','choice','sequence'}:
    return 'candidate_lead','relational_technical_noun','recurrent technical X of/in Y structure','medium'
   return 'remove_description','ordinary_relational_phrase','ordinary mathematical X of Y expression; no independent name evidenced','medium'
  if w[1] in PREP:
   if first in TECH_MOD and last in MATH_NOUN:
    return 'needs_targeted_review','qualified_relational_term','possibly named qualified relational construction','unresolved'
   return 'remove_description','relational_composition','contextual relation, not an established separate term on evidence','medium'
  if any(x in {'under','over','in','on','from','to','as'} for x in w):
   return 'remove_description','contextual_prepositional_phrase','contextual state or action, not standalone mathematical term','medium'
  if first in TECH_MOD and w[1] in TECH_MOD and last in MATH_NOUN:
   return 'candidate_lead','two_technical_modifiers','technical mathematical adjectival compound','medium'
  if last in MATH_NOUN and first in TECH_MOD:
   return 'candidate_lead','three_word_technical_term','technical qualifier plus mathematical noun head', 'medium'
  if first in MATH_NOUN and last in MATH_NOUN:
   return 'needs_targeted_review','technical_noun_compound','combination of mathematical nouns merits direct terminology review','unresolved'
  if last in MATH_NOUN and first in TECH_MOD:
   return 'candidate_lead','technical_compound','technical qualifier plus mathematical noun','medium'
  return 'remove_description','unqualified_three_word_phrase','no evidence of independently named mathematical object','medium'
 if n==2:
  if last in MATH_NOUN and first in TECH_MOD:
   return 'candidate_lead','qualified_technical_head','recognizable mathematical qualifier plus head; verify independent term status','medium'
  if first in MATH_NOUN and last in MATH_NOUN:
   return 'needs_targeted_review','two_mathematical_nouns','technical noun+noun phrase could name a notion','unresolved'
  if last in MATH_NOUN and first in KNOWN_SINGLE:
   return 'needs_targeted_review','published_term_modifier','first word matches a published mathematical term; check compound','unresolved'
  if first in TECH_MOD or last in TECH_MOD or '-' in first or '-' in last or first in MATH_NOUN:
   return 'needs_targeted_review','lexically_technical','technical qualifier without clear named head; inspect context','unresolved'
  return 'remove_description','generic_two_word_phrase','no independent mathematical term evidenced','medium'
 return 'needs_targeted_review','unrecognized_candidate','needs context and terminology check','unresolved'

if __name__=='__main__':
 OUT=[]
 for i,row in enumerate(ROWS):
  ev=evidence(row['phrase'])
  cat,rule,reason,confidence=classify(row,ev)
  OUT.append({**row,'disposition':cat,'review_rule5':rule,'review_reason5':reason,'confidence5':confidence,
   'boundary_occurrences':ev['observed_count'],'boundary_punctuation_count':ev['cross_punctuation'],'boundary_math_count':ev['cross_math'],
   'following_words': '|'.join(x for x,c in ev['next'].most_common(3)),
   'previous_words':'|'.join(x for x,c in ev['prev'].most_common(3)),
   'pass5':'2026-10-28.1','reversible':'true','validated_as_new_definition':'false'})
 counts=collections.Counter(x['disposition'] for x in OUT)
 print('TOTAL',len(OUT),'COUNTS',counts)
 print('TOP RULES',collections.Counter((x['disposition'],x['review_rule5']) for x in OUT).most_common(55))
 dest=ARGS.output;dest.mkdir(parents=True,exist_ok=True)
 cols=list(OUT[0].keys())
 with (dest/'all_7240.tsv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,cols,delimiter='\t');w.writeheader();w.writerows(OUT)
 for cls in counts:
  with (dest/f'{cls}.tsv').open('w',encoding='utf-8',newline='') as f:
   w=csv.DictWriter(f,cols,delimiter='\t');w.writeheader();w.writerows(x for x in OUT if x['disposition']==cls)
 (dest/'summary.json').write_text(json.dumps({'source_input':7240,'classified':len(OUT),'counts':dict(counts),'survivors':counts['candidate_lead']+counts['needs_targeted_review'],'retained_categories':['candidate_lead','needs_targeted_review'],'notes':['Editorial triage is reversible; no mathematical definition verified.','Generic descriptions are excluded from independent-definition candidate pool, not asserted mathematically false.'],'version':'2026-10-28.1'},indent=2)+'\n')
 for cls in counts:
  print('\n',cls)
  rng=random.Random(28)
  samp=rng.sample([x for x in OUT if x['disposition']==cls],min(30,counts[cls]))
  for x in samp:print(x['phrase'][:53].ljust(53),'|',x['review_rule5'][:32])