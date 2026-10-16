# mathDef

Current collection snapshot: **983 definitions across 40 subject folders** (October 15, 2026). See [the definition catalog](CATALOG.md) for per-subject counts, provenance guidance, and the mathematical review checklist.

An interactive, GitHub-hosted collection of mathematical definitions written in LaTeX.

## Features

- Two separate live searches: **Search terms** (term name and aliases only) and **Search definitions** (definition body only).
- Independent result selections and optional side-by-side split view.
- Click matches to read the definition in place; click related definitions to follow links.
- Definitions are individual `.tex` files, grouped by subject.

## Add a definition

Create `definitions/<subject>/<name>.tex`:

```tex
% id: topology.open-set
% term: Open set
% aliases: Open subset
% related: topology.neighborhood, topology.topological-space
% source: https://en.wikipedia.org/wiki/List_of_general_topology_topics
% status: draft

Let $(X,\tau)$ be a topological space. A subset $U\subseteq X$
is \emph{open} if $U\in\tau$.
```

The `id` and `term` metadata fields are required. IDs must be unique and stable.
Aliases are separated by `|`; related references are comma-separated IDs.
Other definitions are allowed to have the same *term* with different IDs.

The body and displayed term can contain LaTeX mathematics: `$...$`, `\(...\)`,
`\[...\]`, `$$...$$`. For prose, use ordinary text or simple `\emph{...}`
and `\textbf{...}`. This prototype uses KaTeX for mathematical expressions,
**not** a complete LaTeX document compiler; arbitrary environments, packages,
and macros outside math mode are not yet supported.

## Local preview

Python 3.9+ is the only local build requirement:

```sh
python3 scripts/build_index.py
python3 -m http.server 8000 --directory _site
```

Visit http://localhost:8000/. KaTeX loads from jsDelivr and needs internet access.

## GitHub Pages

A GitHub Actions workflow validates all definitions, constructs the index,
and publishes the generated site from `main`. If necessary, set
**Settings → Pages → Build and deployment → Source: GitHub Actions**.
Intended site URL: https://zengez.github.io/mathDef/

Definition searches presently match words in the body and raw LaTeX source.
This initial dataset is illustrative, not a curated reference.

## Wikipedia topic expansion (October 2026)

The initial expansion follows the navigation page
[Lists of mathematics topics](https://en.wikipedia.org/wiki/Lists_of_mathematics_topics)
into subject lists and glossaries, including algebra, linear algebra, real
and complex analysis, topology, number theory, graph theory, probability,
mathematical logic, and dynamical systems.

Each expansion entry is an **original, concise mathematical formulation**,
not a verbatim copy of Wikipedia prose. Its optional `source` field links
to the Wikipedia **topic list used for discovery**, not necessarily to
the precise article defining that term. It should not be mistaken for a
formal citation of the individual mathematical statement. New entries have
`status: draft` until someone checks mathematical precision and scope;
older illustrative entries use the default `example` status.

When adding content, make sure the term is a genuine definition (rather
than a theorem, historical entry, or unsupported generalization), check
the mathematical conventions, and link only related IDs that exist.

## Build checks

The builder rejects missing IDs, duplicate IDs, empty bodies, and dangling
related references. Source metadata must use an HTTPS URL. Links may point to a specific entry or a subject overview; the source provides context for review, not a guarantee that each formulation was independently checked. The GitHub workflow checks JavaScript syntax and builds the
whole definition index before attempting publication.

**Current limitations:** search uses substring matching rather than full
LaTeX semantic matching; the front end renders KaTeX-compatible math,
not arbitrary compilable TeX documents; the expanded collection is a
draft research corpus, not an exhaustive or peer-reviewed encyclopedia.

## Expanding beyond Wikipedia

Later draft definitions use mathematical references such as the [Encyclopedia of Mathematics](https://encyclopediaofmath.org/wiki/Functional_analysis), [nLab](https://ncatlab.org/nlab/show/category+theory), and [The Stacks Project](https://stacks.math.columbia.edu/tag/0ELP). The `source` URL identifies material consulted for terminology or mathematical context, which may be a subject page rather than an exact statement reference. The original definition prose is written independently and marked `status: draft` pending precise mathematical review.

## arXiv paper-based definitions

Added explicit, numbered definitions located in arXiv papers, with precise `arxiv`, `locator`, and `source_title` metadata in addition to the canonical paper `source` URL. The first 28 independently paraphrased paper entries were inspected in six research papers. A live 12-paper math.DS source scan generated 30 definition-location candidates, with six entries subsequently added from one scanned paper. See [ARXIV_HARVEST.md](ARXIV_HARVEST.md) for a reproducible candidate-scanning workflow and an explicit distinction between locating candidates and editorial acceptance.

## Systematic mathematics source discovery and review

The later source-review pass added **91** new mathematical definitions, particularly Bergman spaces, Bergman kernels, reproducing-kernel Hilbert spaces, Hardy/Dirichlet/Bloch spaces, complex analysis, and several complex variables. It also replaced the original informal description of a set with the axiomatic-set-theory convention, supplied individual reference links for the initial 21 examples, and added synonyms for several function spaces.

The [Wikipedia discovery and audit tools](WIKIPEDIA_DISCOVERY.md) use MediaWiki's categorymembers API to enumerate article-title candidates and compare against current terms and aliases. Run the [discovery workflow](https://github.com/Zengez/mathDef/actions/workflows/wikipedia-discovery.yml) manually for additional categories. The resulting reports are **review queues**, never automatic imports. See [COVERAGE_REVIEW.md](COVERAGE_REVIEW.md) for reliable reference families, methodological limitations, and editorial follow-up priorities.

## Current staged mathematical review and Wikipedia discovery

An expanded 15 October 2026 category traversal covered 220 Wikipedia mathematics categories and discovered 10,233 unique article titles across four overlapping subject scans. [See scope, results, and limitations](WIKIPEDIA_BROAD_SCAN_2026-10-15.md). The first filtered selection added 29 rigorous-style draft definitions in advanced category theory, matroids, functional analysis, differential geometry, stochastic processes, PDEs, and special functions. The previously broad reference citations of all 36 existing functional-analysis entries were examined and made more specific. This is **not** a claim that all 908 definitions have received complete mathematical or citation reviews.

## Continuing mathematical review

The latest incremental work reviewed **41 older entries** in commutative algebra and scheme theory, updated their specific source citations, and added **26 new advanced measure-theory and stochastic-process definitions**. That intermediate checkpoint contained 934 entries. The latest batch history, review caveats, and next steps are in [WORK_CHECKPOINT.md](WORK_CHECKPOINT.md). The bibliography and structural checks do not mean every entry has received a mathematical peer review.

## Latest review checkpoint

The October 15, 2026 repository contains 983 definitions. The most recent work audited all 36 original PDE definitions and all 35 numerical-analysis definitions, while adding 12 graduate-level microlocal-analysis and pseudodifferential-operator entries. Every edit and unresolved caveat is recorded in [WORK_CHECKPOINT.md](WORK_CHECKPOINT.md), and all newly added entries are draft pending individual mathematical validation.
