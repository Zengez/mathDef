# Focused mathematical-term review — October 28, 2026

This is a **reversible, source-linked review worklist**, continuing the exact
2,175 `needs_targeted_review` candidates in Pass 5 of mathDef discovery.
It is **not** a new definition corpus and makes **no production changes**.

## Result

| Disposition | Count | Effect |
|---|---:|---|
| `recognizable_technical_term` | **598** | Retain for checking definitions, conventions, citations, and published coverage |
| `possible_independent_term` | **42** | Retain as plausible specialized terms needing mathematical validation |
| `requires_deeper_research` | **508** | Retain; nomenclature or independence still genuinely ambiguous |
| `descriptive_not_separate_term` | **940** | Suppress only from *independent-term review* (not mathematically false) |
| `false_positive` | **67** | Reversible grammatical / phrase-boundary rejection |
| `term_variant` | **20** | Preserve source phrase, but route to a canonical singular/spelling review |
| **All reviewed** | **2,175** | No candidate skipped or silently dropped |

**Active from this tranche:** 1,148 (598 + 42 + 508).
**Provisional exclusions or variant routing:** 1,027 (940 + 67 + 20).
This does **not** alter the other **934 plausible leads** previously identified
in the 7,240-item Pass 5 run. Across those two Pass 5 categories, **2,082**
remain active for some kind of research, including **508** that have not
received a reliable mathematical-term decision.

## The mathematical distinction

- A *recognizable technical term* is an authentic named notion or standard
  mathematical construction, **not proof that it is absent from mathDef**.
  Example: `Frobenius map`, `fibred category`, `Jacobi identity`,
  `Galerkin method`, and `Kähler metric`.
- A *compositional description* can be mathematically meaningful and
  correctly used inside a definition without requiring an independent term
  entry. Example: `larger integer`, `individual points`, and `usual convention`.
- A *variant* denotes a probable inflection/synonym relationship, not an
  independently researched new concept. Example: `fibred categories` versus
  `fibred category`.
- A phrase crossing punctuation/notation or a grammatical sentence is a
  lexical extraction artifact, not a mathematical definition candidate.
- Context matters. `de Rham differential forms` is valid mathematics even
  though `forms` is also an English verb; the safeguard explicitly protects
  it from false rejection. `front set`, by contrast, is clipped from
  `wave front set` in the cited source and is not necessarily an independent term.

## Verified spot-check references

The following sources were consulted for **selected** recognized notions:

- *Fibred category* and *fibre category*: The Stacks Project,
  [Categories, §4.33](https://stacks.math.columbia.edu/download/book.pdf).
- *Frobenius map*: [Stacks Project, §33.36 (tag 0CC6)](https://stacks.math.columbia.edu/tag/0CC6).
- *Galerkin method*: [Encyclopedia of Mathematics](https://encyclopediaofmath.org/wiki/Galerkin_method).
- *Jacobi identity*: [Wolfram MathWorld](https://mathworld.wolfram.com/JacobiIdentities.html).
- *Kolmogorov complexity*: [Wolfram MathWorld](https://mathworld.wolfram.com/KolmogorovComplexity.html).
- *Levi problem*: [Encyclopedia of Mathematics (Oka theorems)](https://encyclopediaofmath.org/wiki/Oka_theorems).
- *Wave front set*: [EPFL concept explainer](https://graphsearch.epfl.ch/en/concept/1904007),
  relevant for rejecting the clipped `front set` phrase as independent.

**No claim is made that all 598 recognized leads were independently
researched in the literature.** Most were classified using mathematical
terminology expertise, their source definition context and rule-based
screening. All unverified or ambiguous cases remain recoverable.

## Files, reproduction and continuation

- `decisions/*.tsv`: every original candidate ID, phrase, current disposition,
  reason, source formulation IDs, source headings and short source excerpts.
- `active/*.tsv`: the 1,148 retained cases for future verification; no need
  to repeat the initial filtering.
- `manifest.json`: feed identity, category counts, row counts, and exact
  SHA-256 hashes of all committed partitions.
- `summary.json`: review breakdown, rule counts and examples.
- `scripts/review_targeted_technical_terms.py`: complete deterministic rules
  and curated mathematical exceptions. Re-run using:

```sh
python -m scripts.review_targeted_technical_terms \
  --survivor-dir research_pipeline/discovery/independent_term_review_20261028/survivor_batches \
  --context-dir research_pipeline/discovery/contextual_review_20261028/batches \
  --output /tmp/mathdef-targeted-review-replay
python -m scripts.validate_targeted_technical_review
```

The validator checks the original 2,175 candidate IDs, original sources,
reversible classifications, exact active queue and all committed hashes.
When using a newer production definition snapshot, review again in a new
tranche rather than rewriting this historical checkpoint.

**Next focused research queue:** 508 ambiguous terms first, while the 598
recognized and 42 plausible terms go to actual missing-definition,
convention, and citation verification. Do not automatically admit any entry.