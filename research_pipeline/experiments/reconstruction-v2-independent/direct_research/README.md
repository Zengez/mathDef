# Add mathematical terms directly to independent Wave 2

**The only content file for new, researched terms is [terms.json](terms.json).**
Edit that file; do **not** use any retired graph scan, intake, staging manifest,
candidate ID gate, or generic pipeline engine. A term appears in the separate
searchable Wave 2 preview when the updated file is committed to `main`.

Each object in `entries` has:
- `id`: a unique stable meaning ID;
- `term`, `context`, and `definition`: researched content shown on the site;
- `sources`: one or more HTTPS source locators with an honest `verification_status`;
- `aliases`: optional additional term-search labels;
- `links`: optional known `target_meaning` IDs, with `relation_type`
  `definition_uses` or `related`. They may refer to screened or newly added meanings.
- `candidate_id`: optional backlink to the rough 418-term research worklist;
- `research_status`, `assumptions`: simple review provenance and important hypotheses.

You can add meaningful variants by using the **same `term`** with a new `id`
and a different `context`. The existing UI groups these together and lists
both variants. Linking to terms not researched yet is optional and can be done
later. Duplicated IDs, missing sources and dangling links fail the preview build;
there is no global dependency gate.

To preview locally:
```bash
python -m research_pipeline.adapters.mathdef.preview_site --site-root /tmp/mathdef-reconstruction
python -m unittest research_pipeline.tests.test_direct_additions
```

Wave 1 and the original mathDef production definitions are never used as
mathematical sourcing for additions. They stay unchanged. A staged review
decision does not equal a certified definition; this file contains assistant-
reviewed research and is labeled accordingly. Corrections and additional
sources should be incorporated directly in the same entry.

Initial batch: 15 substantive new/specialized definitions recovered from
[previous mathematical reviews](../../../reviews/wave2-salvage-2026-10-26/PREVIOUSLY_REVIEWED_16.json).
The sixteenth reviewed reference (successor ordinal) already has an equivalent
independent meaning and is intentionally *not* duplicated.

## Initial independent Wave 2 reconstruction: complete

The first-pass reconstruction completed on 2026-10-26. The independent preview now
contains **958 contextual meanings** (595 screened + 363 direct). The initial
418-lead list is fully accounted for (350 incorporated, 68 dispositioned).
Relationships total **1,511** (887 screened + 509 new-to-known/new + 115 curated
screened-to-new). See [the completion checkpoint](../WAVE2_INITIAL_RECONSTRUCTION_COMPLETE_2026-10-26.md)
and the [candidate closeout](CANDIDATE_WORKLIST_CLOSEOUT_2026-10-26.md).

The new-to-existing links live in `terms.json`; the conservative original-to-new
links live in `incoming_links.json`. Those links are ordinary curated preview
content, not a dependency graph or a requirement for exhaustive closure.

**Next, not yet started:** scan the 363 newly added definitions for *new*
possible terminology. Continue to treat source leads honestly and preserve the
independently researched corpus; no re-entry into removed staging workflows.
