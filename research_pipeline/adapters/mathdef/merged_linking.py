"""Fast, source-preserving links within the post-Wave2 *merged-only* catalog.

Pure display augmentation. Never mutates original mathDef .tex source, Wave 1,
or the independent completed Wave 2 corpus. This is deliberately not a lexical
discovery stage, dependency graph, or proof that a matched link is correct.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import re
import unicodedata

WORD_RE = re.compile(r"[^\W_]+(?:[-’'][^\W_]+)*", re.UNICODE)
MATH_ENV_RE = re.compile(
    r"\\begin\{(?:equation|align|gather|multline|displaymath|math|eqnarray)\*?\}"
    r".*?\\end\{(?:equation|align|gather|multline|displaymath|math|eqnarray)\*?\}",
    re.DOTALL,
)
BAD_SINGLE = frozenset({
    "set", "space", "map", "one", "real", "point", "order", "line", "element",
    "field", "group", "ring", "form", "degree", "function", "number", "limit",
    "zero", "sum", "product", "image", "closed", "open", "finite", "infinite",
    "normal", "regular", "identity", "constant", "left", "right", "measure",
    "simple", "family", "sequence", "matrix", "module", "ideal", "graph",
    "metric", "norm", "operator", "topology", "category", "derivative",
})
IGNORE_WORDS = frozenset({"a", "an", "the", "of", "on", "in", "at", "to", "for", "and", "or",
                          "with", "by", "over", "under", "from", "its", "is", "as", "or"})
# Context-critical distinctions noticed during direct candidate research.
# Explicitly enumerate only actual source-meaning -> matched term -> target meaning
# links. All other contexts follow ordinary matching/ambiguity rules.
CONTEXT_OVERRIDES = {
    ("meaning.mathdef.original.alg-topology.cell-complex", "weak topology"):
        "meaning.mathdef.postwave.scan-weak-topology-cw-complex-20261026",
}


# Explicit representative meanings for headings whose independently
# researched and original formulations describe the SAME ordinary object,
# or whose broad convention includes all special cases. These choices
# only order the definitions on expansion; they do not erase alternatives.
# Restrict this to vetted identities, never all multi-meaning headings.
BROAD_REPRESENTATIVE = {
    "topological space": "meaning.wave2.foundation.topological-space",
    "open set": "meaning.mathdef.original.topology.open-set",
    "metric space": "meaning.mathdef.original.metric.metric-space",
    "abelian group": "meaning.mathdef.original.algebra.abelian-group",
    "bijection": "meaning.mathdef.original.functions.bijection",
    "probability space": "meaning.mathdef.original.prob.probability-space",
    "cardinality": "meaning.mathdef.original.sets.cardinality",
    "measurable space": "meaning.mathdef.original.measure.measurable-space",
    "homeomorphism": "meaning.mathdef.original.topology.homeomorphism",
    "subspace topology": "meaning.mathdef.original.topology.subspace-topology",
    "locally ringed space": "meaning.mathdef.original.schemes.locally-ringed-space",
    "natural transformation": "meaning.mathdef.original.category.natural-transformation",
    "local ring": "meaning.mathdef.original.commalg.local-ring",
    "equivalence relation": "meaning.mathdef.original.relations.equivalence-relation",
    "binary relation": "meaning.mathdef.original.relations.binary-relation",
    "additive category": "meaning.mathdef.original.category.additive-category",
    "open cover": "meaning.mathdef.original.topology.open-cover",
    "inverse image of a subset": "meaning.wave2.direct.b86257b3cce62907e97e",
    "borel measure": "meaning.mathdef.postwave.scan-borel-measure-basic-20261026",
    "contravariant functor": "meaning.mathdef.original.category.contravariant-functor",
    "natural isomorphism": "meaning.mathdef.original.category.natural-isomorphism",
    "hausdorff space": "meaning.mathdef.original.topology.hausdorff-space",
    "small category": "meaning.mathdef.original.category.small-category",
    "opposite category": "meaning.mathdef.original.category.opposite-category",
    "abelian category": "meaning.mathdef.original.category.abelian-category",
    "equivalence class": "meaning.mathdef.original.relations.equivalence-class",
    "exact sequence": "meaning.wave2.foundation13.exact-sequence-abelian-category",
    "finite field extension": "meaning.mathdef.postwave.scan-finite-field-extension-20261026",
    "limit ordinal": "meaning.mathdef.original.sets.limit-ordinal",
    "rational number": "meaning.mathdef.original.number.rational-number",
    "total order": "meaning.mathdef.original.relations.total-order",
    "affine combination": "meaning.mathdef.original.geometry.affine-combination",
    "preadditive category": "meaning.mathdef.original.category.preadditive-category",
    "separable algebraic extension": "meaning.50d335de00e5f11d.separable-algebraic-extension",
    "stochastic process": "meaning.wave2.found85.stochastic-process",
    "full subcategory": "meaning.mathdef.postwave.full-subcategory-20261026",
    "initial object": "meaning.mathdef.original.category.initial-object",
    "quotient topology": "meaning.mathdef.original.topology.quotient-topology",
    "valuation ring": "meaning.mathdef.original.arithmetic.valuation-ring",
    "cartesian product": "meaning.mathdef.original.sets.cartesian-product",
    "discrete topology": "meaning.mathdef.original.topology.discrete-topology",
    "monoidal category": "meaning.mathdef.original.category.monoidal-category",
    "normal subgroup": "meaning.mathdef.original.algebra.normal-subgroup",
    "polynomial ring": "meaning.wave2.direct.9db64b2f9cdb8258e3d8",
    "principal ideal domain": "meaning.mathdef.original.arithmetic.principal-ideal-domain",
    "quotient ring": "meaning.mathdef.original.algebra.quotient-ring",
    "successor ordinal": "meaning.mathdef.original.sets.successor-ordinal",
    "von neumann ordinal": "meaning.mathdef.original.sets.ordinal",
    "affine scheme": "meaning.mathdef.original.schemes.affine-scheme",
    "chromatic number": "meaning.mathdef.original.graph.chromatic-number",
    "coequalizer": "meaning.mathdef.original.category.coequalizer",
    "connected space": "meaning.mathdef.original.topology.connected-space",
    "discrete valuation ring": "meaning.mathdef.original.arithmetic.discrete-valuation-ring",
    "limit of a diagram": "meaning.mathdef.original.category.limit",
    "locally finite borel measure": "meaning.mathdef.postwave.scan-locally-finite-borel-measure-20261026",
    "morphism of schemes": "meaning.mathdef.original.schemes.morphism-schemes",
    "power set": "meaning.mathdef.original.sets.power-set",
    "prime number": "meaning.mathdef.original.number.prime-number",
    "projective module": "meaning.mathdef.original.commalg.projective-module",
    "quotient group": "meaning.mathdef.original.algebra.quotient-group",
    "radical ideal": "meaning.mathdef.original.commalg.radical-ideal-property",
    "surjective function": "meaning.mathdef.original.functions.surjective",
    "symmetric relation": "meaning.mathdef.original.relations.symmetric-relation",
    "transitive set": "meaning.mathdef.original.sets.transitive-set",
    "unique factorization domain": "meaning.mathdef.original.arithmetic.unique-factorization-domain",
}



# A word-level substring in a longer name is not necessarily a reference to
# that shorter, mathematically distinct concept. In these two definitions,
# the "open ball" text denotes the asymmetric forward/backward quasi-metric
# ball being defined, NOT an ordinary symmetric metric-ball definition.
SUPPRESSED_CONTEXT_MATCHES = {
    ("meaning.mathdef.original.quasimetric.forward-ball", "open ball"),
    ("meaning.mathdef.original.quasimetric.backward-ball", "open ball"),
}

def words(value: str) -> tuple[str, ...]:
    """Unicode-aware literal words; no stemming, hallucinated terms or embeddings."""
    value = unicodedata.normalize("NFKC", value).casefold()
    return tuple(m.group(0) for m in WORD_RE.finditer(value))


def masked_prose(value: str) -> str:
    """Retain exact character offsets while ignoring TeX mathematics and code.

    The recognized math delimiters are intentionally modest. An unrecognized
    formula may be skipped conservatively by the label matcher, not converted
    into a mathematical link.
    """
    masked = list(value)

    def blank(start, end):
        for k in range(start, end):
            if value[k] not in "\r\n":
                masked[k] = " "

    for m in MATH_ENV_RE.finditer(value):
        blank(m.start(), m.end())

    i = 0
    while i < len(value):
        if masked[i] == " " and value[i] != " ":
            i += 1
            continue
        if value.startswith(r"\[", i):
            delimiter, end_delimiter = r"\[", r"\]"
        elif value.startswith(r"\(", i):
            delimiter, end_delimiter = r"\(", r"\)"
        elif value[i] == "$" and (i == 0 or value[i-1] != "\\"):
            delimiter = "$$" if value.startswith("$$", i) else "$"
            end_delimiter = delimiter
        else:
            i += 1
            continue
        end = value.find(end_delimiter, i+len(delimiter))
        if end < 0:
            # Better no link than trusting an unmatched mathematical delimiter.
            blank(i, len(value))
            break
        end += len(end_delimiter)
        blank(i, end)
        i = end
    return "".join(masked)


def name_index(catalog):
    """Build a first-word index; detect label collisions without guessing."""
    groups = catalog["groups"]
    index = defaultdict(list)
    labels = defaultdict(set)
    for group in groups:
        for label in [group["title"], *group.get("aliases", [])]:
            parts = words(label)
            if not parts or len(parts) > 8:
                continue
            if len(parts) == 1 and (len(parts[0]) < 7 or parts[0] in BAD_SINGLE):
                continue
            labels[parts].add(group["id"])
    # A modest, explicit plural inflection is useful in ordinary definition
    # prose (open set/open sets; vector space/vector spaces). Do not generalize
    # arbitrarily or stem mathematical terminology.
    singular = list(labels.items())
    irregular = {"matrix": "matrices", "index": "indices", "vertex": "vertices",
                 "basis": "bases", "category": "categories", "topology": "topologies",
                 "property": "properties", "family": "families"}
    for parts, gids in singular:
        if len(parts) < 2:
            continue
        final = parts[-1]
        plural = irregular.get(final)
        if plural is None and final.endswith("s"):
            continue
        if plural is None and len(final) > 2:
            plural = final + "s"
        if plural:
            labels[(*parts[:-1], plural)].update(gids)
    for parts, gids in labels.items():
        index[parts[0]].append((parts, tuple(sorted(gids))))
    for entries in index.values():
        entries.sort(key=lambda v: (-len(v[0]), v[0], v[1]))
    return index


def context_words(meaning):
    label = meaning.get("label", "")
    generic = {"original", "mathdef", "wave", "research", "direct", "post",
               "definition", "independent", "screened", "context", "source"}
    return set(words(label)) - generic - IGNORE_WORDS


def record_ambiguity(report, group, source, phrase, occurrence):
    """Keep a small, retrievable sample of actual source contexts per homonym.

    The full counts may be much larger, but this audit is restricted to
    previously existing terms and their original formulation text.
    """
    label = group["title"]
    report["ambiguous_contexts"][label] += 1
    examples = report["ambiguous_context_examples"][label]
    if len(examples) < 80 and occurrence:
        form_id, body, start, end = occurrence
        examples.append({
            "from_formulation": form_id,
            "source_meaning": source["id"],
            "source_context": source.get("label", ""),
            "matched_text": body[start:end],
            "excerpt": body[max(0, start-105):min(len(body), end+105)].replace("\\n", " "),
            "eligible_meanings": [
                {"id": meaning["id"], "context": meaning.get("label", "")}
                for meaning in group["meanings"]
            ][:12],
        })


def choose_meaning(group, source_meaning, phrase, report, occurrence=None,
                   scoped_resolutions=None):
    """Use exact meaning IDs; abstain rather than selecting arbitrary variants."""
    scoped_key = (source_meaning["id"], group["id"])
    if scoped_resolutions and scoped_key in scoped_resolutions:
        mid = scoped_resolutions[scoped_key]
        if not any(m["id"] == mid for m in group["meanings"]):
            raise ValueError("Scoped link context resolution targets missing meaning: " + mid)
        report["scoped_context_selection_uses"][source_meaning["id"]+" -> "+group["id"]] += 1
        return mid
    override = CONTEXT_OVERRIDES.get((source_meaning["id"], phrase))
    if override:
        return override
    meanings = group["meanings"]
    if len(meanings) == 1:
        return meanings[0]["id"]
    # Use a documented broad representative for matched ordinary meanings.
    # The full set of context-specific definitions remains displayed by the
    # renderer; this only determines which variant appears first.
    representative = BROAD_REPRESENTATIVE.get(group["title"].casefold())
    if representative and any(m["id"] == representative for m in meanings):
        return representative
    # For an unconstrained random variable, the arbitrary measurable-space
    # codomain definition is mathematically general enough to cover both the
    # real-valued and nonreal cases. Where the source explicitly says "real
    # random variable", show the real-valued formulation first instead.
    if group["title"].casefold() == "random variable":
        excerpt = ""
        if occurrence:
            _, body, start, end = occurrence
            excerpt = body[max(0, start-30):min(len(body), end+28)]
        real_named = re.search(
            r"\breal(?:-valued)?\s+random\s+variables?\b",
            excerpt, re.IGNORECASE,
        )
        mid = ("meaning.wave2.prob90.random-variable-real" if real_named else
               "meaning.wave2.prob90.random-variable-general")
        if any(m["id"] == mid for m in meanings):
            return mid

    # Ordinary functional-analysis normed spaces have real or complex scalars.
    # Do not force this narrower convention on unrelated nonstandard scalar
    # divisions. The explicit source meanings here have that scope.
    if group["title"].casefold() == "normed vector space" and (
        source_meaning["id"] in {
            "meaning.mathdef.original.functional.banach-space",
            "meaning.wave2.pop142.bounded-linear",
            "meaning.mathdef.postwave.scan-closed-linear-subspace-20261026",
            "meaning.wave2.pop142.bounded-operator-norm",
        }
    ):
        mid = "meaning.mathdef.original.functional.normed-space"
        if any(m["id"] == mid for m in meanings):
            return mid

    # The mathematical source identifies a subset's (derived-set) limit point,
    # not a subsequential accumulation of an indexed sequence.
    if group["title"].casefold() == "accumulation point" and (
        source_meaning["id"] in {
            "meaning.mathdef.original.real.limit-of-function",
            "meaning.mathdef.original.topology.limit-point",
        }
    ):
        mid = "meaning.wave2.cross110.set-accumulation"
        if any(m["id"] == mid for m in meanings):
            return mid

    # Time indices in these source statements disambiguate the two researched
    # martingale variants without imposing a global default.
    if group["title"].casefold() == "martingale":
        martingale_context = {
            "meaning.mathdef.original.stochastic.martingale":
                "meaning.wave2.research81.martingale-discrete",
            "meaning.mathdef.original.stochastic.local-martingale":
                "meaning.wave2.research81.martingale-continuous-index",
            "meaning.mathdef.postwave.scan-localizing-sequence-local-martingale-20261026":
                "meaning.wave2.research81.martingale-continuous-index",
        }
        mid = martingale_context.get(source_meaning["id"])
        if mid and any(m["id"] == mid for m in meanings):
            return mid

    # An ordinary metric ball is appropriate in this metric closure statement;
    # the forward/backward quasi-metric ball sources are deliberately left
    # ambiguous rather than linked to a symmetric metric ball.
    if group["title"].casefold() == "open ball" and (
        source_meaning["id"] == "meaning.mathdef.original.topology.closure"
    ):
        mid = "meaning.mathdef.original.metric.open-ball"
        if any(m["id"] == mid for m in meanings):
            return mid

    # The two scheme/reduced sources work in commutative algebra. Do not use
    # this specialization for a possibly noncommutative reduced ring.
    if group["title"].casefold() == "reduced ring" and (
        source_meaning["id"] in {
            "meaning.6c51aeb904a0fe74.geometrically-reduced-algebra",
            "meaning.6a21c2d4f3354c8f.reduced-scheme",
        }
    ):
        mid = "meaning.mathdef.original.commalg.reduced-ring"
        if any(m["id"] == mid for m in meanings):
            return mid

    # Krull dimension/height/depth are suprema of the nonnegative integer
    # lengths of chains or regular sequences (possibly +infinity).
    # These commutative-algebra contexts use the general order-theoretic
    # least-upper-bound concept, not specifically a real-valued supremum.
    if group["title"].casefold() == "supremum":
        subject = set(words(source_meaning.get("label", "")))
        if subject & {"commutative", "module", "ideal", "height", "dimension",
                      "depth", "prime"}:
            mid = "meaning.wave2.direct.066b1d1b9032a2e86bdd"
            if any(m["id"] == mid for m in meanings):
                return mid

    # Source-precise rather than global convention choices.
    scoped = {
        ("open ball", "meaning.wave2.direct.23c297a4a1c27fe4ec73"):
            "meaning.mathdef.original.metric.open-ball",
        ("closed ball", "meaning.mathdef.original.geometry.sphere"):
            "meaning.wave2.directional113.closed-norm",
        ("minimal polynomial", "meaning.mathdef.original.algebra.algebraic-element"):
            "meaning.mathdef.original.arithmetic.minimal-polynomial",
        ("supremum", "meaning.mathdef.original.commalg.krull-dimension"):
            "meaning.wave2.direct.066b1d1b9032a2e86bdd",
        # In the original zero-polynomial definition 'rings with zero divisors'
        # means nontrivial zero-divisor pairs, not the element zero itself.
        ("zero divisor", "meaning.mathdef.postwave.scan-zero-polynomial-20261026"):
            "meaning.wave2.direct.8f2dea7e2bd1211c0cf6",
    }
    mid = scoped.get((group["title"].casefold(), source_meaning["id"]))
    if mid and any(m["id"] == mid for m in meanings):
        return mid

    # Some ring maps are non-unital by convention. A ring map used to specify
    # an affine scheme morphism must preserve identities; only that precise
    # mathematical context warrants the unital specialization automatically.
    if group["title"].casefold() == "ring homomorphism" and (
        {"scheme", "schemes", "affine", "commutative"} &
        set(words(source_meaning.get("label", "")))
    ):
        unital = "meaning.wave2.foundation.ring-map-unital"
        if any(m["id"] == unital for m in meanings):
            return unital

    # Infimum/supremum as real or extended-real numbers is a specialization
    # of order-theoretic bounds. Prefer a meaningful context only if the
    # source subject makes the intended object clear.
    if group["title"].casefold() in {"supremum", "infimum"}:
        subject = set(words(source_meaning.get("label", "")))
        if subject & {"real", "numerical", "optimization", "analysis", "scv",
                      "complex", "functional", "stochastic", "probability"}:
            mid = ("meaning.mathdef.original.real.supremum"
                   if group["title"].casefold() == "supremum" else
                   "meaning.mathdef.original.real.infimum")
            if any(m["id"] == mid for m in meanings):
                return mid
        if subject & {"order", "relations", "topology", "poset", "sets"}:
            mid = ("meaning.wave2.direct.066b1d1b9032a2e86bdd"
                   if group["title"].casefold() == "supremum" else
                   "meaning.wave2.direct.d90bc393eeba8fd1be9e")
            if any(m["id"] == mid for m in meanings):
                return mid

    if (group["title"].casefold() == "martingale" and
        source_meaning["id"] == "meaning.mathdef.original.stochastic.martingale-transform"):
        mid = "meaning.wave2.research81.martingale-discrete"
        if any(m["id"] == mid for m in meanings):
            return mid
    if group["title"].casefold() == "binary operation" and (
        {"algebra", "group", "monoid", "semigroup"} &
        set(words(source_meaning.get("label", "")))
    ):
        mid = "meaning.wave2.foundation.binary-operation-internal"
        if any(m["id"] == mid for m in meanings):
            return mid
    # A minimal polynomial is not the same object for an algebraic element
    # and a linear operator. Select the arithmetic variant only when the source
    # explicitly concerns an algebraic element or number/field extension.
    if group["title"].casefold() == "minimal polynomial" and (
        {"arithmetic", "algebraic", "number", "field"} &
        set(words(source_meaning.get("label", "")))
    ):
        field_poly = "meaning.mathdef.original.arithmetic.minimal-polynomial"
        if any(m["id"] == field_poly for m in meanings):
            return field_poly
    # Context-sensitive prioritization is meaningful only with substantial
    # category overlap and a decisive winner. Otherwise mark for human review.
    source_context = context_words(source_meaning)
    if not source_context:
        record_ambiguity(report, group, source_meaning, phrase, occurrence)
        return None
    scores = []
    for target in meanings:
        common = source_context & context_words(target)
        scores.append((len(common), target["id"]))
    scores.sort(key=lambda x: (-x[0], x[1]))
    if scores[0][0] >= 2 and scores[0][0] >= scores[1][0] + 2:
        return scores[0][1]
    record_ambiguity(report, group, source_meaning, phrase, occurrence)
    return None


def link_merged_catalog(catalog: dict, *, max_auto_links_per_form: int = 35,
                        scoped_resolutions: dict | None = None) -> dict:
    """Add occurrence-anchored, *tentative* definition-use links in-place.

    The input is the already merged independent + original + post-Wave2 catalog.
    Existing screened links remain authoritative and are not duplicated.
    """
    groups = catalog["groups"]
    relations = catalog["relations"]
    by_gid = {group["id"]: group for group in groups}
    meaning_gid = {m["id"]: g["id"] for g in groups for m in g["meanings"]}
    meanings = {m["id"]: m for g in groups for m in g["meanings"]}
    index = name_index(catalog)
    prior = defaultdict(dict)
    for rel in relations:
        if rel.get("relation_type") == "definition_uses":
            prior[rel["from_formulation"]][rel["target_meaning"]] = rel

    report = {
        "schema_version": 1,
        "status": "tentative_lexical_links_not_semantically_verified",
        "scope": "combined_post_wave2_only",
        "forms_visited": 0,
        "forms_with_link": 0,
        "new_tentative_links": 0,
        "existing_screened_links_anchored": 0,
        "skipped_existing": 0,
        "skipped_self": 0,
        "skipped_overlapping": 0,
        "skipped_context_false_positive": 0,
        "skipped_limit": 0,
        "scoped_context_selection_uses": Counter(),
        "ambiguous_contexts": Counter(),
        "ambiguous_context_examples": defaultdict(list),
        "ambiguous_labels": Counter(),
        "links_by_form": {},
        "notes": [
            "Links are fast lexical candidates, not mathematically certified dependencies.",
            "Original and independent Wave2 corpora remain frozen.",
            "Ambiguous meanings are abstained from unless a scoped contextual override applies.",
            "Occurrences in TeX mathematics are ignored, preserving original text offsets.",
        ],
    }
    added_id = 0
    for group in groups:
        for source in group["meanings"]:
            for form in source["formulations"]:
                report["forms_visited"] += 1
                form_id = form["id"]
                body = form["text"]
                plain = masked_prose(body)
                tokens = [(m.group(0).casefold(), m.start(), m.end())
                          for m in WORD_RE.finditer(plain)]
                hits = []
                pos = 0
                while pos < len(tokens):
                    token = tokens[pos][0]
                    matches = []
                    for parts, group_ids in index.get(token, ()):
                        end_word = pos + len(parts)
                        if end_word > len(tokens):
                            continue
                        if tuple(t[0] for t in tokens[pos:end_word]) != parts:
                            continue
                        # Prevent fabricating a phrase across a hidden formula,
                        # a paragraph break, TeX macro or punctuation. The
                        # *original* gap, not the math-masked text, matters.
                        if any(not re.fullmatch(r"\s+|\s*[-–]\s*",
                                body[tokens[k][2]:tokens[k+1][1]])
                               for k in range(pos, end_word-1)):
                            continue
                        matches.append((parts, group_ids, end_word))
                    if not matches:
                        pos += 1
                        continue
                    # A longest exact phrase wins; ambiguity of that phrase is
                    # logged, never resolved via arbitrary dictionary order.
                    parts, group_ids, end_word = matches[0]
                    phrase = " ".join(parts)
                    pos = end_word
                    if (source["id"], phrase) in SUPPRESSED_CONTEXT_MATCHES:
                        report["skipped_context_false_positive"] += 1
                        continue
                    if len(group_ids) != 1:
                        report["ambiguous_labels"][phrase] += 1
                        continue
                    target_gid = group_ids[0]
                    target_group = by_gid[target_gid]
                    if target_gid == group["id"]:
                        report["skipped_self"] += 1
                        continue
                    start = tokens[end_word-len(parts)][1]
                    end = tokens[end_word-1][2]
                    target = choose_meaning(
                        target_group, source, phrase, report,
                        (form_id, body, start, end),
                        scoped_resolutions=scoped_resolutions
                    )
                    if not target:
                        continue
                    target_gid = meaning_gid[target]
                    if target_gid == group["id"]:
                        report["skipped_self"] += 1
                        continue
                    hits.append((end-start, start, end, target, phrase, target_gid))
                # Earliest occurrence per meaning per formulation. No source
                # text rewriting; the index renderer inserts a small marker.
                dedup = set()
                written = 0
                for _length, start, end, mid, phrase, gid in sorted(
                    hits, key=lambda h: (h[1], -h[0], h[3])
                ):
                    if mid in dedup:
                        report["skipped_existing"] += 1
                        continue
                    dedup.add(mid)
                    old = prior[form_id].get(mid)
                    if old is not None:
                        # Even an existing curated link deserves an actual
                        # inline anchor if we find its literal occurrence.
                        if old.get("span_start", -1) < 0:
                            old["span_start"], old["span_end"] = start, end
                            old["source_phrase"] = body[start:end]
                            report["existing_screened_links_anchored"] += 1
                        continue
                    if written >= max_auto_links_per_form:
                        report["skipped_limit"] += 1
                        continue
                    # Never place two separate cues on the same characters.
                    # Curated and automatic links can share a conceptual
                    # target but never duplicate a form/meaning edge.
                    if any(start < lo_end and end > lo_start for lo_start, lo_end in
                           ((r.get("span_start", -1), r.get("span_end", -1))
                            for r in prior[form_id].values())
                           if lo_start >= 0):
                        report["skipped_overlapping"] += 1
                        continue
                    rel = {
                        "id": f"rel.mathdef.merged.lexical.{added_id:06d}",
                        "from_formulation": form_id,
                        "target_meaning": mid,
                        "relation_type": "definition_uses",
                        "review_state": "lexical_candidate",
                        "human_verified": False,
                        "source_phrase": body[start:end],
                        "span_start": start,
                        "span_end": end,
                        "editorial_reason": "Automatic literal title/alias match, context not individually verified",
                    }
                    added_id += 1
                    relations.append(rel)
                    prior[form_id][mid] = rel
                    written += 1
                if written or any(r.get("span_start", -1) >= 0
                                  for r in prior[form_id].values()):
                    report["forms_with_link"] += 1
                if written:
                    report["links_by_form"][form_id] = written
                report["new_tentative_links"] += written

    report["scoped_context_selection_uses"] = dict(sorted(
        report["scoped_context_selection_uses"].items()
    ))
    # Flatten non-JSON-native Counters to sortable, bounded diagnostics.
    for name in ("ambiguous_contexts", "ambiguous_labels"):
        records = sorted(report[name].items(), key=lambda x: (-x[1], x[0]))
        report[name+"_total_occurrences"] = sum(count for _, count in records)
        report[name] = [{"phrase": phrase, "occurrences": count}
                        for phrase, count in records[:150]]
    report["ambiguous_context_examples"] = {
        label: report["ambiguous_context_examples"][label]
        for label, _ in sorted(
            ((item["phrase"], item["occurrences"])
             for item in report["ambiguous_contexts"]),
            key=lambda item: -item[1],
        )[:60]
    }
    report["forms_with_link_fraction"] = (
        round(report["forms_with_link"] / report["forms_visited"], 4)
        if report["forms_visited"] else 0
    )
    report["new_tentative_link_examples"] = [
        {"from_formulation": rel["from_formulation"],
         "target_meaning": rel["target_meaning"],
         "source_phrase": rel["source_phrase"]}
        for rel in relations if rel.get("review_state") == "lexical_candidate"
    ][:100]
    return report
