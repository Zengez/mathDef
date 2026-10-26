# Post-Wave2 expansion: rapid scan + original mathDef comparison (2026-10-26)

## User-authorized scope

The user explicitly requested a **fast, error-tolerant terminology scan** of both:

1. The **363 directly researched new definitions** added in the completed independent Wave 2 pass.
2. The complete **original mathDef term list, definition bodies and alternate formulations**.

The user also authorized incorporating the original mathDef mathematical content into the newer searchable collection. This is an explicit *post-completion change* to the original independent-reconstruction source restrictions, **not** a retroactive claim that Wave 2 was independently built using original mathDef.

## Deliverable

The existing `/reconstruction/wave1/` (frozen), `/reconstruction/wave2/` (completed independent snapshot, 958 meanings), and original production `/` are preserved untouched.

A new `/reconstruction/merged/` view combines the original `definitions/*.tex` (plus `variants/*.tex`) with the independent Wave 2 corpus at site-build time using the pre-existing original mathDef parser. Each original ID, distinct definition body, alternate formulation, citation and source-file location is retained. An original title matching a Wave 2 title is displayed under that existing term heading, but the original source meaning remains a **separate context** pending any later mathematically justified equivalence merge. No unchecked mathematical equivalence or blanket peer review is asserted.

On the first successful CI build, the original repository contained **1,014 definitions** (seven more than the 1,007-definition Oct. 16 snapshot), with **5 additional original formulation variants**. The combined view contained **1,972 contextual meanings** grouped under **1,831 term headings**. A total of 100 original definitions shared an exact normalized title with existing Wave 2 term groups; 914 new term headings were introduced.

The generated `/reconstruction/merged/scan-report.html` and `scan-report.json` contain the one-pass lexical scan results. First build discovered **2,019 tentative new-phrase leads** and **473 known-term mention patterns**. These are noisy, not vetted mathematical definitions or confirmed absent terms; duplicates and false positives are expected. They are not a dependency graph or a new multi-stage review queue.

## Boundaries

- The **958-meaning independent Wave 2 reconstruction completion checkpoint remains accurate and frozen for comparison**; it is not relabeled as 1,972 independent meanings.
- Production `definitions/`, `variants/` and their citation history are read-only for this task.
- No mathematical research / certification is inferred from proximity, common titles or lexical matches. Related metadata links are imported as related, not as definitional prerequisites.
- The rapid scan is **only candidate discovery**. Research into additional candidates, improved true synonym merging, and linking potential occurrences are optional *subsequent* work, not a prerequisite to using the combined reference.
- There is no requirement to fully resolve the 2,019 leads before displaying the merged corpus.
- If original production gains new definitions, the merged view and its scan automatically reflect the files present at build time; the completed independent Wave 2 baseline does not change.

## Rebuild

```bash
python -m research_pipeline.adapters.mathdef.preview_site --site-root /tmp/mathdef-merged-preview
python -m unittest research_pipeline.tests.test_original_merge -v
```

Site paths: `/reconstruction/merged/`, `/reconstruction/merged/scan-report.html`, and `/reconstruction/merged/scan-report.json`.
