# Repeatable mathDef term discovery / promotion

**Canonical input:** the exact cleaned, linked production catalog generated
at build time, with the matching SHA-256-verified v2 snapshot. Never scan
only the original .tex files or frozen Wave 2 sources when asked for the
current corpus.

## One-step fast run (also usable on Instant)

Open **Actions > Discover terms in current merged mathDef corpus > Run workflow**.
The workflow checks out the current main branch, builds the canonical corpus,
verifies consistency, and scans every meaning and formulation. Download the
**mathdef-current-corpus-discovery** artifact to obtain summary.json, full
candidates.json, and sortable candidates.tsv plus new_candidates.tsv. Artifacts are retained
for 90 days, while scan checkpoints persist in Git.

To trigger from an assistant with GitHub connector access but no workflow
dispatch operation: create a new discovery/<unique-run-name> branch from
the current main and commit a text request file under discovery_requests/.
That branch's push runs the same workflow against its checked-out corpus.
No main edits are needed. An authorized user may instead start the workflow
from the GitHub Actions UI.

Local equivalent (Python 3.12, standard library):

    python scripts/build_index.py
    python -m research_pipeline.adapters.mathdef.preview_site --site-root _site/reconstruction
    python -m research_pipeline.adapters.mathdef.publish_root --site-root _site
    python -m scripts.current_corpus_discovery --site-root _site --output _discovery

The exported feed is validated before discovery. A new heading or additional
meaning automatically enters the scanner's scope; no count constants or
scanner edits are required.


## Persistent skip-unchanged scanning

The persistent checkpoint is a separate Git branch named
`discovery-checkpoints`. Each formulation is indexed by its stable ID and
SHA-256 text hash. Routine runs **do not rescan unchanged formulations**;
they reuse previous phrase inventories. Newly added or changed formulations
are scanned, and newly published terminology can be checked against cached
tokens without rereading the definition text.

Previously encountered suggestions remain visible in the complete
`candidates.json` and `candidates.tsv`; only genuinely new leads appear
in `new_candidates.tsv`. **Having been scanned never means rejected.**
The separate editorial `decisions.json` controls actual decisions.

Force a full rescan from the Actions manual-run `force_rescan` checkbox,
or with local command `--force-rescan`. For a targeted rescan use
`--force-formulation FORM_ID` or `--force-group GROUP_ID` locally.
For an individual previously discovered candidate phrase, specify
`--force-phrase 'candidate phrase'` locally or include `force_phrases` in the
branch request JSON. Its containing formulation(s) will be explicitly rescanned,
and it will appear separately in `revisited_candidates.tsv`; no previous
rejection is assumed.

When triggering from a `discovery/**` branch, add a JSON file as the
single request file in the trigger commit, e.g.:
```json
{"force_rescan": true}
```
Or specify `force_formulations`, `force_groups`, or `force_phrases` arrays instead.
The workflow saves checkpoint data in `discovery-checkpoints` after
successful runs. Those commits do not affect the published mathDef site.
A missing checkpoint causes a full initial scan; later runs are incremental.
Run history persists beyond the 90-day Actions artifact retention window.

## Iteration and editorial authority

1. Pass 1 emits high-recall lexical leads, known mentions, and possible
   lexical variants. These are NOT validated mathematical definitions.
2. Review and research the leads, including mathematical conventions and
   duplicate/context-sensitive meaning checks.
3. Optionally add manually reviewed phrases to decisions.json. Each entry
   has phrase, status (accepted/rejected/deferred/duplicate/ignored), reason,
   and optional target_group_id. This distinguishes reviewed from new leads.
4. Add accepted sourced formulations via the existing curated inputs,
   normally the post_wave2/terms.json collection. Do not modify frozen
   historical Wave 1 or Wave 2 records, or automatically admit candidates.
5. When an approved change reaches main, Pages rebuilds the CLEANED canonical
   catalog, links, UI index and versioned v2 snapshot/manifest in one build.
   Consumers including mathThm compare the SHA-256 manifest and refresh when
   it changes. The v1 API remains historical.
6. Rerun discovery. New definitions are scanned in full; known headings
   are recognized automatically; recorded editorial decisions remain
   available to avoid repeated reviews.

## Guarantees and boundaries

Production remains guarded by source preservation, cross-corpus exact ID
checks, link audits, SHA-256 output consistency and browser smoke tests.
Historical fixed term/formulation totals are no longer release criteria.
The canonical version is the *built* site, not an old copied corpus file.

The older original_merge.fast_scan is deliberately a frozen historical
benchmark, not the current iterative scanner. Wikipedia/arXiv scanners
provide separate source-based leads and do not publish definitions.
