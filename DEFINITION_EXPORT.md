# mathDef cross-project reference feed — canonical merged collection

**Current contract: v2 (complete merged mathDef, October 2026).**
This is the supported, read-only, public API for projects such as **mathThm**
to retrieve mathDef's terms, contexts/variants, definitions, sources and
definition links, and to detect newly published revisions. No GitHub login
or authentication token is required. The producer updates this feed together
with the main mathDef website; consumers decide when to check for updates.

## Endpoints to use in NEW integrations

| Resource | Stable public URL | Purpose |
|---|---|---|
| **v2 manifest** | https://zengez.github.io/mathDef/api/definitions/v2/manifest.json | Lightweight SHA-256 change signal and content counts |
| **v2 snapshot** | https://zengez.github.io/mathDef/api/definitions/v2/snapshot.json | Complete, versioned set of searchable term groups, variants and links |
| Reference UI | https://zengez.github.io/mathDef/ | Same dataset as the v2 snapshot |
| Link-audit report | https://zengez.github.io/mathDef/audits/full-link-graph.json | Structural/link-audit diagnostics, not mathematical certification |

**These v2 URLs are the canonical feed.** The old
`/api/definitions/v1/manifest.json` and `/api/definitions/v1/snapshot.json`
remain accessible only as an **original .tex-only historical feed**, containing
only the original definitions (see its live manifest for the current count),
but *not* the integrated research. Do not use
v1 for new projects, and do not misinterpret its `dataset: "production"` tag
as claiming to reflect the new main website. v2 is the actual production
merged collection. Retaining v1 costs little and allows old experiments to
continue until intentionally migrated.

## What's exported

The v2 snapshot is JSON:

```json
{
  "schema": "mathdef.definition-snapshot.v2",
  "definitions": [
    {
      "id": "preview.term.<stable-within-current-catalog-id>",
      "term": "Name of mathematical concept",
      "aliases": ["Alternate name"],
      "original_ids": ["topology.example-definition-id"],
      "meaning_ids": ["meaning.mathdef.original.topology.example-definition-id"],
      "meanings": [
        {
          "id": "meaning.mathdef.original.topology.example-definition-id",
          "label": "Original mathDef · Topology",
          "display_term": "Name of mathematical concept",
          "source_origin": "original_mathdef",
          "research_status": "original_mathdef_editorial_draft",
          "original_definition_id": "topology.example-definition-id",
          "formulation_ids": ["form.mathdef.original.topology.example-definition-id.primary"]
        }
      ],
      "formulations": [
        {
          "key": "form.mathdef.original.topology.example-definition-id.primary",
          "meaning_id": "meaning.mathdef.original.topology.example-definition-id",
          "label": "Original mathDef · Topology",
          "body": "Mathematical definition with LaTeX",
          "sources": [
            {"title": "Source reference", "url": "https://example.org"}
          ],
          "dependencies": []
        }
      ],
      "dependencies": [],
      "related": []
    }
  ]
}
```

The example illustrates the **shape**, not a real term in the dataset; inspect
the published JSON for the complete fields and exact real IDs.

**Important identity distinction:** Each element of `definitions` is a
*searchable heading/term group*, not necessarily one mathematical meaning.
A heading can contain several related or context-specific meanings (for
example, a real-field and a complex-field interpretation) and several
source-attributed formulations. **Never assume matching term names imply
equivalent mathematical statements.** The array `meanings` explicitly
identifies each interpretation, its origin and its `formulation_ids`.
Each formulation's `meaning_id` identifies which one it supports.

Each heading supplies: `id`, `term`, `aliases`, `original_ids`,
`meaning_ids`, `meanings`, `formulations`, and the same
`body`, `source`, `category`, `status`, `related` and
`dependencies` fields used by the main site's renderer.

Each formulation includes `key`, `meaning_id`, `label`, `body`,
`source`, a full `sources` list (including attribution and verification
provenance as available), and `dependencies`. A dependency points to a
**target heading** via `id` and, when known, a more specific interpretation
via `target_meaning`; it may also carry `review_state`,
`source_phrase`, and `start`/`end` character offsets. These indices
refer to the **exact formulation body string**, not its rendered HTML.
A value of -1 means no literal inline position was established; show such
dependencies below the definition rather than guessing a position.

`related` contains IDs of **term groups**, useful for navigation; it
does not assert that all meanings under two headings are equivalent.
A provisional automatically inferred link has
`review_state: "lexical_candidate"`. Treat it as **suggested**, not
mathematically verified. The site has user-feedback mechanisms for these.
The six intentional convention ambiguities remain unlinked.

The v2 export is created by the *same site publisher*, using the canonical
merged catalog and the same rendered `definitions-index.json`. An explicit
coverage check requires **all** meanings, formulations and original-definition
aliases to appear before publication, even as the catalog grows. At the
initial v2 release, expect **2,048 headings**, **2,197 meanings**,
**2,246 formulations**, and **1,014 original definition IDs**. These counts
are **not fixed schema limits** and should increase as mathDef grows.

**Stable IDs and migration:** Older original IDs like
`topology.compactness` appear in `original_ids`, and the corresponding
original meaning provides `original_definition_id`. For an old theorem
hint referencing that ID, find the heading whose `original_ids` contains
it. **Do not assume a v2 heading ID equals the old original definition ID.**
Prefer `meaning_id` and contextual references to choose a formulation
when multiple meanings are present. Retain enough alias/index metadata so
future published changes can be picked up at the next synchronization.

## How to check for updates and cache safely

The v2 **manifest** contains:

```json
{
  "schema": "mathdef.definition-manifest.v2",
  "snapshot_schema": "mathdef.definition-snapshot.v2",
  "dataset": "merged",
  "version": "sha256:<full-64-character-digest>",
  "sha256": "<full-64-character-digest>",
  "definition_count": 2048,
  "meaning_count": 2197,
  "formulation_count": 2246,
  "original_definition_count": 1014,
  "snapshot_path": "snapshot.json"
}
```

The displayed count values illustrate the initial release; the actual
digest and later counts are taken from the live manifest.

Recommended consumer synchronization procedure:

1. GET `manifest.json` (with cache revalidation or `Cache-Control: no-cache`).
   Require schema v2 and `dataset: "merged"`.
2. If `version` matches the **last successfully verified cached version**,
   use that cached snapshot. A SHA-256 hash is an *equality token*, not a
   sortable revision number or Git commit.
3. Otherwise GET the snapshot URL **relative to the manifest's directory**,
   adding `?v=<sha256>` to avoid stale CDN copies.
4. Calculate SHA-256 on the **raw response bytes** before parsing or reformatting
   JSON. Compare against the manifest; reject mismatches.
5. Validate `snapshot.schema`, array shapes, unique group IDs, and
   `definition_count`, `meaning_count`, `formulation_count` against
   the manifest. Atomically save the complete snapshot first, then the new
   cached manifest. Never partially overwrite a known-good import.
6. Rebuild the local term/alias index and optional original-ID-to-group map.
   When matching mathematical language, disambiguate a heading's multiple
   meanings using the theorem's *actual context* instead of guessing.
7. If anything fails (transient network, Pages mid-deployment, CDN caching,
   invalid JSON, mismatched hash), **keep the last verified snapshot**.
   Don't erase a working theorem site because mathDef was momentarily
   unavailable.

A complete, standard-library Python implementation of this procedure is
checked into the repository:

**[`examples/consume_mathdef_v2.py`](examples/consume_mathdef_v2.py)**

Try it from a separate project or local clone with:

```bash
python examples/consume_mathdef_v2.py --cache-dir .cache/mathdef
```

It prints group/meaning counts, whether a refresh occurred, and a
sample original-definition ID lookup. It makes **read-only HTTPS GET**
requests and does not write into mathDef's repository. Copy/adapt its
`sync_mathdef` function when integrating into mathThm. No external
Python packages are required.

## Choosing when to refresh

| Consumer project setup | Suggested refresh behavior |
|---|---|
| GitHub Pages static project built via Actions | Poll the v2 manifest at every build; optionally schedule daily/weekly rebuilds |
| Long-running server application | Revalidate the manifest periodically; keep the last valid in-memory/local snapshot |
| Local editor, scripts, or research notebook | Refresh on launch or through an explicit `refresh definitions` command |
| Offline or infrequently connected application | Ship the last verified snapshot and update when connectivity returns |

mathDef does **not** need access to another project's repository and does
not send cross-project push notifications. The feed is read-only; community
requests for additions/corrections must follow mathDef's suggestion
workflow. New definitions become available **after a successful mathDef
GitHub Pages deployment**, not merely after a Git commit. Consumer schedules
need not align with mathDef's schedule.

### Integration note specifically for mathThm

The current mathThm prototype was built against v1 and may bundle the old
original-only snapshot. That is expected historical behavior, **not**
evidence the merged feed is broken. Before further mathThm development,
point its feed client to v2, require the new schemas/dataset, index
`definitions` as term groups, and translate any existing
`topology.*`-style hints via `original_ids`. Favor the exact
`target_meaning` or other context evidence when showing one of several
formulations. See the runnable example above. **No mathThm repository
changes are required to establish or test the producer contract.**

## Producer: source, publication and tests

- The original `.tex` corpus builds the **historical v1 export** in
  `scripts/build_index.py`.
- `research_pipeline.adapters.mathdef.preview_site` reconstructs the
  frozen baseline and produces the merged, original-inclusive catalog.
- `research_pipeline.adapters.mathdef.publish_root` builds the public
  root reference and **v2 feed from the same merged catalog**.
- `scripts/merged_definition_export.py` writes
  `_site/api/definitions/v2/manifest.json` and `snapshot.json`.
- The required GitHub Pages workflow checks original ID retention,
  canonical index completeness, full graph integrity, and manifest counts
  before deploying both files in the **same Pages artifact**.

Local build:

```bash
python scripts/build_index.py
python -m research_pipeline.adapters.mathdef.preview_site --site-root _site/reconstruction
python -m research_pipeline.adapters.mathdef.publish_root --site-root _site
python -m unittest tests.test_merged_definition_export -v
```

If an **incompatible** feed change becomes necessary, create v3 and migrate
consumers explicitly rather than silently changing v2. Ordinary additions
to the arrays, descriptions, cited source lists, dependency positions or
metadata that fit the v2 schema increment the SHA-256 content hash but do
not require a new API version.
