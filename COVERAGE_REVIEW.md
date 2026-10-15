# Mathematics source review and systematic discovery

**Snapshot:** October 15, 2026. **908 definitions in 40 subject folders.**

## Why previous source harvesting missed Bergman space and kernel

The initial batch followed Wikipedia's `Lists of mathematics topics` and a few subject-list pages.
Those lists do not enumerate every article in subject categories. In contrast,
[Category:Complex analysis](https://en.wikipedia.org/wiki/Category:Complex_analysis)
includes Bergman space, Bloch space, Hardy space, Dirichlet space and Szegő kernel
along with many adjacent topics. We now query actual Wikipedia category memberships
and selected subcategories with the documented
[MediaWiki categorymembers API](https://www.mediawiki.org/wiki/API:Categorymembers).

## Coverage checks actually completed

1. **Complex analysis:** a trial across **12 categories**, depth one, inventoried **582 distinct
   Wikipedia page titles**. At the time of the scan, 24 titles matched mathDef terms or
   aliases. This was a lexical title check, *not* a count of genuine missing mathematical
   definitions. Many results were mathematicians, articles about theorems, or synonyms.
2. **Several complex variables:** a later trial across **3 categories** found **126 titles**,
   including 8 exact name matches, 4 possible name variants, 91 high-priority title
   candidates, and 23 low-priority titles. Fifteen mathematically formulated entries
   have subsequently been added from this and related source navigation.
3. **Editorial metadata:** the previous 864-entry inventory contained **257 sources pointing
   to broad topic lists**, **82 short definitions**, and **two identical displayed names**
   (`Open set`, deliberately distinct metric/topological IDs). Initially the 21 demo entries
   lacked sources; all 21 were given individual mathematical reference links.
   The corpus still has no entries formally promoted to `reviewed` after a full
   individual mathematical review. A metadata audit is not a mathematical proof check.

The project now includes 91 extra draft definitions from the targeted pass:
31 in advanced holomorphic function spaces, 41 in several complex variables,
and 19 in core complex analysis. All use separately identified concept references.

## Mathematical issues and conventions caught

- **Bergman spaces for p below 1:** the usual `A^p` membership condition defines a
  quasi-normed space for `0 < p < 1`, not a Banach space under the `p`-expression.
  The new entry distinguishes `p >= 1` from `p < 1` explicitly; this is a useful
  example of why a Wikipedia page cannot be transcribed uncritically.
- **Bergman kernel normalization:** for ordinary Lebesgue area measure on the
  complex unit disk the kernel is `1/(pi (1-z conj(w))^2)`; for area normalized
  by `1/pi` the `pi` disappears. Both conventions are documented.
- **Primitive set terminology:** in axiomatic set theory, set and membership
  are primitive concepts governed by axioms; the initial demo's
  'collection of distinct objects' wording was replaced.
- **Term collisions:** two distinct entries named `Open set` are intentional.
  Do not merge mathematically different settings by display name alone.

## References ranked by use case (not an absolute accuracy hierarchy)

| Resource | Especially useful for | Appropriate treatment |
|---|---|---|
| [Encyclopedia of Mathematics](https://encyclopediaofmath.org) | Classical analysis, kernel theory, topology, algebra | Prefer direct entry URL; independently check hypotheses and notation |
| [NIST DLMF](https://dlmf.nist.gov) | Special functions and formulas | Cite chapter/section and equation numbers when possible |
| [The Stacks Project](https://stacks.math.columbia.edu) | Commutative algebra and algebraic geometry | Prefer permanent lemma/definition tags |
| [nLab](https://ncatlab.org/nlab/show/HomePage) | Category theory and homotopy | Identify convention-dependent levels of generality |
| [Jiří Lebl: Several Complex Variables](https://www.jirka.org/scv/) | Holomorphy, Levi and pseudoconvex geometry | Check textbook definitions and surrounding assumptions |
| [Mathlib](https://leanprover-community.github.io/mathlib4_docs/) | Formally specified concepts | Cross-check formal hypotheses; library conventions may be specialized |
| [Wolfram MathWorld](https://mathworld.wolfram.com/) | Mathematical term discovery | Cross-check against more precise graduate references |
| [PlanetMath](https://planetmath.org/) | Alternative terminology and conceptual links | Use as discovery or a second reference, not automatic authority |
| [Wikipedia mathematics categories](https://en.wikipedia.org/wiki/Category:Mathematics) | Broad coverage discovery | Use page titles only as candidates, not as verified definitions |

## Systematic inventory procedure

Run the [Wikipedia discovery workflow](https://github.com/Zengez/mathDef/actions/workflows/wikipedia-discovery.yml)
with a category and subcategory depth, or locally run:

```bash
python3 scripts/wikipedia_candidate_scan.py --seed 'Functional analysis' --depth 1 --max-categories 12
python3 -m scripts.audit_corpus --out _definition_audit.csv
python3 scripts/build_index.py
```

Outputs consist of a title-only candidate review CSV and a separate metadata audit.
Check the actual source content before writing a concise, independent LaTeX
definition. Search both existing term names and aliases; verify equivalences and
ambient assumptions; cite a **specific concept page**, not a subject index.
Keep `status: draft` until a real mathematical review, and preserve a stable
semantic ID if a term has alternate conventions or multiple meanings.

## Editorial priorities

1. Replace 257 broad topic-list citations with direct, checked references.
2. Review the shortest definitions and identify missing hypotheses or qualifiers.
3. Add formal reviews of high-value nodes instead of marking all draft definitions reviewed.
4. Process advanced mathematics Wikipedia categories in bounded batches, excluding
   biographies, theorem-only pages, broad category pages, and duplicates.
5. Check LaTeX rendering against the actual published site; successful index
   generation validates the data model but not every mathematical formula.

## Build checks versus mathematical verification

The site build checks JavaScript syntax, parser/unit tests, unique IDs, nonempty
definitions, source URL format, and that related IDs resolve. It cannot establish
that every theorem-level assumption or mathematical equivalence is correct.
References, source descriptions and review flags are editorial metadata;
only individual contextual mathematical checking should justify `status: reviewed`.

## Latest automated audit — 879 definitions

The [latest successful discovery and editorial audit run](https://github.com/Zengez/mathDef/actions/runs/38806321333)
was executed after the 91-definition expansion and the initial reference-link repairs:

- **879** entries: **858** marked draft and **21** marked example; **none** yet individually marked reviewed.
- **0** entries without a source URL (the first 21 examples now have specific reference pages).
- **257** entries whose reference remains an overly broad Wikipedia topic list.
- **82** entries shorter than the audit heuristic's 90-character threshold; these are *review candidates*, not verified defects.
- **1** entry with a LaTeX environment needing rendering inspection.
- **2** entries with identical displayed term `Open set` but intentionally different IDs.

A new Several Complex Variables title-level comparison found **126** Wikipedia titles:
**17** exact matches, **4** possible name variants, **82** high-priority candidate titles,
and **23** lower-priority pages. High priority means only 'not matched and
not excluded by the title heuristic', not necessarily a useful definitional article.

By source host, the 879 entries use 365 English Wikipedia URLs,
301 Encyclopedia of Mathematics URLs, 108 nLab URLs, 41 Stacks Project URLs,
36 Stanford references, and 28 arXiv paper links. The host count is not
an endorsement of the accuracy or specificity of an individual link.

## Broad category scan and targeted review — October 15, 2026

- In a GitHub Actions matrix scan, followed depth-two subcategory links from 24 subject-category seeds in four independent groups. Visited **220 categories** (55 in each group), inventorying **11,053 title records**, corresponding to **10,233 distinct Wikipedia article titles** across groups. These are metadata *candidates*, not verified mathematical notions.
- Added 29 advanced mathematical definitions from the discovered concepts, with per-entry source pages, and verified that the site build passed.
- Revisited and refined individual source links across **all 36 original functional-analysis definitions** (one earlier Banach-space fix and three additional batches of 14, 14, and 7), including Hausdorff conventions and resolvent signs.
- Structural consistency and GitHub deployment passed for the 908-definition collection. **The requested full manual rigor/citation audit is still incomplete**; its precise state and proposed next priority areas are documented in [WORK_CHECKPOINT.md](WORK_CHECKPOINT.md).
- The previous **257 citations pointing to generic Wikipedia topic lists** remain a significant editorial backlog. That figure came from the earlier 879-entry scan, not a fresh verification of every one of the 908 entries. No entry was promoted to `reviewed` solely for acquiring a direct URL.

[Full discovery inventory and source cautions](WIKIPEDIA_BROAD_SCAN_2026-10-15.md).
