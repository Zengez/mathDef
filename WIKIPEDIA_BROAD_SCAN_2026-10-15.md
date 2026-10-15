# Broad Wikipedia mathematics category discovery — October 15, 2026

## Verified scope

A GitHub Actions matrix workflow [run 38809181537](https://github.com/Zengez/mathDef/actions/runs/38809181537) traversed mathematics category memberships via the Wikimedia MediaWiki API, including subcategories up to depth two rather than relying on a manually supplied mathematics-topic index.

| Scan group | Categories visited | Article title records | High-priority by lexical heuristic |
|---|---:|---:|---:|
| Analysis and geometry | 55 | 2,742 | 2,142 |
| Algebra and logic | 55 | 2,902 | 2,495 |
| Discrete and applied | 55 | 2,852 | 2,550 |
| Stochastic processes and dynamics | 55 | 2,557 | 2,232 |
| **Total** | **220 visits** | **11,053** | **9,419 heuristic flags** |

Across groups the 11,053 title records represent **10,233 distinct article titles**. The scans use overlapping category regions, so the unique-title total is smaller than the record total. “High priority” means *not matched by a normalized term/alias and not excluded by a simple title heuristic*. It is not evidence that a mathematical definition is missing. Many flagged pages concern people, results, historical topics, or specialized applications.

## Method and reproducibility

Workflow: [wikipedia-broad-audit.yml](.github/workflows/wikipedia-broad-audit.yml). Scanner: [wikipedia_candidate_scan.py](scripts/wikipedia_candidate_scan.py). It uses the documented [MediaWiki categorymembers API](https://www.mediawiki.org/wiki/API:Categorymembers), handles continuation, spaces requests apart, enumerates articles and subcategories, and compares titles against metadata `term` and `aliases`.

Each independent scan's title-only CSV and JSON summary were saved as GitHub Actions artifacts in the successful workflow. Artifacts are retained for 45 days and may need to be regenerated later; the workflow remains available for manual reruns. The crawler does **not** import definition prose or make automatic mathDef edits.

## First candidate triage and accepted mathematical definitions

The first 29 independently worded mathematical definitions from this inventory were added in two bounded commits:
- `256ad77b`: 10 category/homological concepts and 4 matroid-related concepts (including abelian and derived categories, Grothendieck topologies, simplicial sets, matroids and Tutte polynomials).
- `8bc6e698`: 15 entries spanning Schatten/compact-operator theory, differential geometry, stochastic processes, viscosity solutions, and special functions.

Each accepted entry cites an individual Wikipedia mathematical concept page and remains `status: draft` pending a separately recorded editorial review. Some rigorous references such as nLab, the Stacks Project, the Encyclopedia of Mathematics, NIST DLMF, Mathlib and textbooks should be used to check hypotheses independently before promoting an entry to reviewed.

## Remaining editorial work

1. Continue source-specific manual mathematical verification of old definitions, **20–30 entries at a time**, explicitly checking field, topology, quantifiers, regularity, convergence and normalization.
2. Repair overly generic references in the legacy corpus. The previous audit reported **257 broad Wikipedia topic-list citations** among 879 entries; update the number with a new full metadata scan rather than assume the same count after edits.
3. Triage candidate titles by actual mathematical meaning, avoiding title-only assumptions and near-duplicate concepts.
4. Audit rendered LaTeX/KaTeX, especially multiline mathematics and obscure macros. Static build success is not a proof of correct mathematical meaning.

The full 908-entry mathematical proof-level and citation audit **has not yet been completed**. Its progress is preserved in [WORK_CHECKPOINT.md](WORK_CHECKPOINT.md).
