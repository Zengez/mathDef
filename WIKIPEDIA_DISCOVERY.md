# Systematic mathematical definition discovery

## Why the original expansion missed important topics

Subject lists on Wikipedia are not exhaustive and not a substitute for category
enumeration. For example, Wikipedia's Category:Complex analysis includes Bergman
space, Bloch space, Dirichlet space, Hardy space, Szegő kernel, and a subcategory
for Several complex variables; the first mathDef expansion missed many of them.

## Category-aware Wikipedia candidate scanner

Use Python 3.10+ (standard library, no third-party dependencies):

    python3 scripts/wikipedia_candidate_scan.py --seed 'Complex analysis' --depth 1 --max-categories 12

More seeds may be supplied using repeated --seed options. It follows category
links using the MediaWiki categorymembers API, handles pagination, enforces
request spacing (at least 1 second), and caps categories and article counts.
Seeds by default cover several major areas of advanced mathematics.

Output is a local-only CSV of article titles, source categories, Wikipedia
URLs, exact matches against mathDef terms/aliases, and approximate related-ID
candidates. 'Not matched' means only that the title is not in the current
glossary; not that the article contains a rigorous mathematical definition.
Possible matches are suggestions, not confirmed semantic equivalences.

Nothing is inserted into the public definition collection automatically.
The scanner downloads category listing metadata, not copyrighted article prose.
Always inspect the actual mathematics; Wikipedia errors are possible.

## Current merged-corpus coverage (2026-10-28)

The historical .tex-only command above is retained for reproducing the old
original-corpus study. For current discovery, build mathDef's canonical cleaned
release and supply its generated v2 snapshot:

    python scripts/build_index.py
    python -m research_pipeline.adapters.mathdef.preview_site --site-root _site/reconstruction
    python -m research_pipeline.adapters.mathdef.publish_root --site-root _site
    python scripts/wikipedia_candidate_scan.py --snapshot _site/api/definitions/v2/snapshot.json --seed 'Complex analysis'

The GitHub Actions Wikipedia workflows perform this build and pass the
snapshot automatically. All published meanings and aliases are then recognized
without editing a hand-maintained count or original-only term list. An article
title not found in the catalog remains a **research lead**, not an accepted
mathematical definition. The main, repeatable internal-corpus phrase scanner is
documented separately in research_pipeline/discovery/README.md.

## Cross-reference sources

- Encyclopedia of Mathematics — https://encyclopediaofmath.org
- NIST Digital Library of Mathematical Functions — https://dlmf.nist.gov
- The Stacks Project — https://stacks.math.columbia.edu
- nLab — https://ncatlab.org/nlab/show/HomePage
- Jiří Lebl, Tasty Bits of Several Complex Variables — https://www.jirka.org/scv/
- Wikipedia mathematics categories — https://en.wikipedia.org/wiki/Category:Mathematics

For each promoted concept, prefer a specific reference page over a generic
subject index, state the ambient space and hypotheses precisely, distinguish
norm/measure conventions, and rewrite in independent mathematical language.
Terms must be individually checked, even when a source has academic authority.

## Verification levels

Structural build checks detect unique IDs, nonempty bodies, and related-link
consistency. Candidate discovery checks coverage only. The separate corpus
audit reports duplicate display names and missing or broad source metadata.
None of these checks proves mathematical correctness or validates every KaTeX
expression. A manual mathematical and citation review remains necessary.
