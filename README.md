# mathDef

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
