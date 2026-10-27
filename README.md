# mathDef

**Main mathDef site:** [zengez.github.io/mathDef](https://zengez.github.io/mathDef/). The published library combines **2,197 contextual meanings** under **2,048 searchable term headings**, including **all 1,014 original .tex definitions**, 958 independently reconstructed Wave 2 meanings, and 225 subsequent research additions (October 2026). The [original definition catalog](CATALOG.md) documents the initial source files and their subject distribution.

An interactive, GitHub-hosted collection of mathematical definitions written in LaTeX.

## Editorial provenance and research status

The **historical October 16 original-corpus audit** covered 1,007 definitions in 40 subjects. Its citation-suitability findings were: **822 sources verified as suitable without changes, 185 entries whose citations or wording were corrected, and 0 citation entries pending**. See [CITATION_AUDIT.csv](CITATION_AUDIT.csv), [CITATION_AUDIT_PROCESS.md](CITATION_AUDIT_PROCESS.md), and [WORK_CHECKPOINT.md](WORK_CHECKPOINT.md). These counts describe citation review, **not** formal mathematical peer review or individual approval of every KaTeX rendering. Entries retain their draft/example statuses until those separate checks occur.

## Whole-corpus internal link audit (October 2026)

The fully merged 2,197-meaning library has undergone a **single graph-wide
link audit** covering all 6,825 screened and tentative relationships,
including original/reconstructed/post-Wave2 cross-links. The audit found
**no broken link endpoints, invalid positioned links, duplicate target
relations, rendered-index discrepancies, or unexplained gaps in references
to existing search terms**. Six mathematically convention-dependent
references remain intentionally unlinked and eligible for visitor feedback.

The audit is required during each GitHub Pages deployment, with current
machine-readable results at
[`/audits/full-link-graph.json`](https://zengez.github.io/mathDef/audits/full-link-graph.json).
See [the full audit record](research_pipeline/experiments/reconstruction-v2-independent/post_wave2/FULL_CORPUS_LINK_AUDIT_2026-10-26.md).
These are automated structural/context coverage checks: **Suggested**
automatic links are not individually human-certified.

## Features

- Two separate live searches: **Search terms** (term name and aliases only) and **Search definitions** (definition body only).
- Independent result selections and optional side-by-side split view.
- Click matches to read the definition in place; click related definitions to follow links.
- Three recursive definition exploration modes: **Standard**, **Nested**, and **In-Line** (default). During the site build, matching terms/aliases in definition bodies generate candidate links, with ambiguity checks and branch-local cycle prevention. The main site's merged-meaning matcher lives in [merged_linking.py](research_pipeline/adapters/mathdef/merged_linking.py); six genuinely convention-dependent occurrences are deliberately left unresolved. Original-corpus link overrides remain in [data/link_overrides.json](data/link_overrides.json). See [DEPENDENCY_LINKING.md](DEPENDENCY_LINKING.md) for the legacy original-data matcher and the [linking review](research_pipeline/experiments/reconstruction-v2-independent/post_wave2/LINK_AMBIGUITY_REVIEW_2026-10-26.md) for current combined-corpus context choices.
- Visitors can **suggest a missing definition**, **suggest a correction** to any displayed or recursively expanded definition, or **report an erroneous automatic link**. Suggestions become public GitHub Issues for editorial review; no changes are applied automatically. The first version requires a GitHub account to finish submitting. An optional attribution name is published only with explicit consent. See [FEEDBACK_WORKFLOW.md](FEEDBACK_WORKFLOW.md).
- A term may show **multiple equivalent or context-specific, individually sourced meanings and formulations under one heading**. The original definitions remain in `definitions/` and their manually maintained alternatives in `variants/`; the independent research records and merged-only overlay supply additional displayed contexts without rewriting those original files. **Function** now displays both its assignment formulation and its set-theoretic relation formulation. See [FORMULATIONS.md](FORMULATIONS.md).
- Definitions are individual `.tex` files, grouped by subject.

## Add a definition

Create `definitions/<subject>/<name>.tex`:

```tex
% id: topology.open-set
% term: Open set
% aliases: Open subset
% related: topology.neighborhood, topology.topological-space
% source: https://en.wikipedia.org/wiki/Open_set
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

Build the expanded main library from its original and independent research inputs:

```sh
python3 scripts/build_index.py
python3 -m research_pipeline.adapters.mathdef.preview_site --site-root _site/reconstruction
python3 -m research_pipeline.adapters.mathdef.publish_root --site-root _site
python3 -m http.server 8000 --directory _site
```

Visit http://localhost:8000/ for the merged mathDef main site. The independent research comparison views remain available under `/reconstruction/`. KaTeX loads from jsDelivr and needs internet access.

## GitHub Pages

A GitHub Actions workflow validates the original data, constructs the merged index,
and publishes the **combined** collection as the main site from `main`.
Every original .tex definition and its formulations are verified as retained
within the published meanings. The research previews remain under
`/reconstruction/`. The prior original-only snapshot export remains
separately available under `/api/definitions/v1/` for provenance.
If necessary, set
**Settings → Pages → Build and deployment → Source: GitHub Actions**.
Main site URL: https://zengez.github.io/mathDef/

Definition searches presently match words in the body and raw LaTeX source.
The site is an editorially audited **draft** mathematical reference, not yet a formally peer-reviewed encyclopedia.

## Historical Wikipedia topic expansion (October 2026)

The initial expansion follows the navigation page
[Lists of mathematics topics](https://en.wikipedia.org/wiki/Lists_of_mathematics_topics)
into subject lists and glossaries, including algebra, linear algebra, real
and complex analysis, topology, number theory, graph theory, probability,
mathematical logic, and dynamical systems.

Each expansion entry was an **original, concise mathematical formulation**, not a verbatim copy of Wikipedia prose. **At initial import**, many `source` fields referred to broad topic lists used for discovery rather than to direct concept references. The subsequent per-entry citation audit replaced or confirmed sources for all current entries; the older broad-list description is historical. The citations provide mathematical evidence, but the definitions remain drafts pending formal peer review.

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

Later draft definitions use mathematical references such as the [Encyclopedia of Mathematics](https://encyclopediaofmath.org/wiki/Functional_analysis), [nLab](https://ncatlab.org/nlab/show/category+theory), and [The Stacks Project](https://stacks.math.columbia.edu/tag/0ELP). The `source` URL identifies the mathematical reference checked for citation suitability during the October 16, 2026 audit. It does not certify complete mathematical correctness, editorial approval, or site rendering. Original definition prose remains independently written and generally marked `status: draft`.

## arXiv paper-based definitions

Added explicit, numbered definitions located in arXiv papers, with precise `arxiv`, `locator`, and `source_title` metadata in addition to the canonical paper `source` URL. The first 28 independently paraphrased paper entries were inspected in six research papers. A live 12-paper math.DS source scan generated 30 definition-location candidates, with six entries subsequently added from one scanned paper. See [ARXIV_HARVEST.md](ARXIV_HARVEST.md) for a reproducible candidate-scanning workflow and an explicit distinction between locating candidates and editorial acceptance.

## Systematic mathematics source discovery and review

The later source-review pass added **91** new mathematical definitions, particularly Bergman spaces, Bergman kernels, reproducing-kernel Hilbert spaces, Hardy/Dirichlet/Bloch spaces, complex analysis, and several complex variables. It also replaced the original informal description of a set with the axiomatic-set-theory convention, supplied individual reference links for the initial 21 examples, and added synonyms for several function spaces.

The [Wikipedia discovery and audit tools](WIKIPEDIA_DISCOVERY.md) use MediaWiki's categorymembers API to enumerate article-title candidates and compare against current terms and aliases. Run the [discovery workflow](https://github.com/Zengez/mathDef/actions/workflows/wikipedia-discovery.yml) manually for additional categories. The resulting reports are **review queues**, never automatic imports. See [COVERAGE_REVIEW.md](COVERAGE_REVIEW.md) for reliable reference families, methodological limitations, and editorial follow-up priorities.

## Historical staged review and Wikipedia discovery (October 15, 2026)

An expanded 15 October 2026 category traversal covered 220 Wikipedia mathematics categories and discovered 10,233 unique article titles across four overlapping subject scans. [See scope, results, and limitations](WIKIPEDIA_BROAD_SCAN_2026-10-15.md). The first filtered selection added 29 rigorous-style draft definitions in advanced category theory, matroids, functional analysis, differential geometry, stochastic processes, PDEs, and special functions. The previously broad reference citations of all 36 existing functional-analysis entries were examined and made more specific. At that time this was **not** a claim that the then-908 definitions had received complete mathematical or citation reviews; the separate citation phase for the current 1,007 entries has since been completed.

## Historical mathematical-review checkpoint (October 15, 2026)

That checkpoint reviewed **41 older entries** in commutative algebra and scheme theory, updated their specific source citations, and added **26 new advanced measure-theory and stochastic-process definitions**. That intermediate checkpoint contained 934 entries. The full batch history, review caveats, and next steps are in [WORK_CHECKPOINT.md](WORK_CHECKPOINT.md). The bibliography and structural checks do not mean every entry has received a mathematical peer review.

## Historical PDE and numerical checkpoint (October 15, 2026)

At that intermediate October 15, 2026 checkpoint, the repository contained 995 definitions. Work then audited all 36 original PDE definitions and all 35 numerical-analysis definitions, while adding 12 graduate-level microlocal-analysis and pseudodifferential-operator entries. Every edit and unresolved caveat is recorded in [WORK_CHECKPOINT.md](WORK_CHECKPOINT.md), and all newly added entries are draft pending individual mathematical validation.

## Public cross-project definition export

The standard Pages build publishes a read-only, SHA-256 versioned definition snapshot and a small update manifest so companion projects such as mathThm can detect changes and refresh their local definition cache. See [DEFINITION_EXPORT.md](DEFINITION_EXPORT.md) for the stable endpoints, consumer protocol, scope, and validation details. Independent Wave 1 and Wave 2 research previews are not part of this production feed.
