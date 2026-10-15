# mathDef

Current collection snapshot: **760 definitions across 31 subject folders** (October 15, 2026). See [the definition catalog](CATALOG.md) for per-subject counts, provenance guidance, and the mathematical review checklist.

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
