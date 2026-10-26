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
