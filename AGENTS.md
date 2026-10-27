# mathDef — active development instructions (October 26, 2026)

## Standing mathematical convention guidance — REQUIRED for definition reviews

**Before reviewing, deduplicating, rewriting, or mathematically comparing
definitions, read [`DEFINITION_CONVENTIONS.md`](DEFINITION_CONVENTIONS.md).**
This is a permanent repository reference, not a temporary chat note.
It documents tacit empty/nonempty, zero/nonzero, trivial/nontrivial,
vacuous-truth, indexing, and other boundary-case conventions that can
make mathematically identical core definitions appear different.

**Specifically:** differences only at an omitted/excluded empty or trivial
case are a **convention/boundary review signal**, not automatic evidence of
a distinct mathematical variant, and also not automatic proof of equivalence.
For example, an empty space is connected under the no-nontrivial-
separation predicate, but some treatments impose nonemptiness. **mathDef
adopts the broader predicate for connected spaces**, with a short explanatory
convention note rather than a duplicate near-identical definition card.
Other authors' restricted definitions remain legitimate within their
explicit or verified standing assumptions; this is a mathDef editorial
choice, not a universal claim about terminology.

**Important for dependent definitions:** if a source defines another
concept using "connected" under a verified nonempty convention, make that
condition **explicit in mathDef's adapted wording** wherever it is needed to
preserve the source's mathematics (for example, "nonempty connected subset"
in a maximal-connected-subset characterization of a component). Do not
silently transplant the source's implicit assumptions or present an adapted
definition as a verbatim quotation. Preserve the exact source, applicable
scope, evidence/verification state, and the wording transformation in the
term-level reference/source metadata. If a convention has not been checked,
its state is **not_checked**, not assumed absent or present. Other structural
differences and borderline cases remain subject to the user's review.

**Required interpretation rule (2026-10-27 clarification):** mathematical
authors often state **restrictive** conventions explicitly and do not
typically announce the absence of a restriction. Keep source **evidence
status** distinct from its **effective working interpretation**:

- `verified_applies`: follow a positively established restriction at its
  verified scope; make hidden source assumptions explicit when needed.
- `verified_opposite`: follow the **current mathDef canonical broad meaning**
  as the working interpretation; retain evidence that a particular
  restriction was rejected.
- `checked_inconclusive`: **also follow the current mathDef canonical broad
  meaning for editorial wording**, while preserving the **inconclusive**
  evidence status and never claiming the author explicitly endorsed it.
  Do not manufacture a restricted variant solely because no explicit
  rejection of nonemptiness/another restriction was found.
- `not_checked`: no source-specific convention assessment exists; use the
  canonical meaning as mathDef's own baseline, but do not attribute that
  reading to the source. Check/review if a source-derived assertion
  materially depends on unverified assumptions.
- A verified local restriction overrides this fallback within its scope.

**Dynamic inheritance:** `verified_opposite` and `checked_inconclusive`
must resolve by reference to the **latest mathDef canonical meaning**.
If that canonical meaning is later broadened, their working interpretations
broaden automatically; do not freeze old predicates, introduce backward-
compatibility assumptions, or pretend historical inconclusive checks became
verified. Reevaluate imported definitions whose exact mathematics depends
on the change, and correct their wording when warranted.

**The permanent guide specifies a convention catalog and per-source,
per-scope convention-assessment contract.** Its data schema/source-list
implementation belongs to the ongoing deduplication/source-registry cleanup;
the future user-facing Sources link remains deferred. No new candidate
discovery or premature final linking rebuild is authorized by this guidance.


## Cleaned-corpus global linking — completed stage-only October 27, 2026

**User explicitly authorized the full global linking rebuild on 2026-10-27.** It has been run successfully against the **cleaned canonical corpus** in the development branch, and its link-graph audit passed. See [GitHub Actions run 40586388342](https://github.com/Zengez/mathDef/actions/runs/40586388342). This updates the earlier staging-only prohibition against prematurely rebuilding links; it **does not** authorize production deployment or v2 feed update.

- One reproducible stage-only command after `stage_cleanup.py`: `python -m research_pipeline.adapters.mathdef.rebuild_cleaned_links --stage /tmp/mathdef-cleanup-stage --output /tmp/mathdef-cleaned-links --overrides data/definition_expansion_priority_overrides.json --context-resolutions data/global_link_context_resolutions_2026-10-27.json`.
- Results: **1,986 headings, 2,065 meanings, 2,104 formulations, 6,445 total relationships**; 3,728 surviving historical relationships retained, 2,717 newly rebuilt tentative, source-anchored definition-use links, 350 previously screened links positioned. **No dangling, duplicate, overlapping, or invalid inline anchor.** Build is idempotent.
- **43 explicit editorial-scoped source/target decisions** resolve 44 previously ambiguous occurrences, based on existing source-definition text, without promoting research verification or merging different meanings. **Exactly five convention-sensitive occurrences intentionally remain unresolved** (2 natural numbers, 2 inner product space, 1 ring homomorphism); see the final link-audit artifact.
- Of 140 historically dropped source-text edges (whose source formulation was consolidated or whose text was rewritten), **58 re-linked to the same meaning, 1 to an alternate meaning within the same heading, 2 became intentional redundant self-heading links, 79 no longer have a standalone literal target-heading phrase in the surviving text**. These are not new pending link errors. This classification is explicitly recorded in the final link-audit artifact.
- No frozen corpora, new terminology candidate queues, user-approved convention evidence, or original source research data were modified. Link artifacts are in GitHub Actions `mathdef-cleaned-global-link-audit` and can be reproducibly regenerated. **Publishing and source-UI deployment remain separate decisions.**

## Current status: independent Wave 2 COMPLETE; merged mathDef catalog is the main public site

**MAIN SITE PUBLICATION — 2026-10-26:** User explicitly confirmed that
backward compatibility with the old original-only website is **not** a concern.
The intended mathDef site is the **entire merged mathematical-definitions
library**, including all original content and separately researched contextual
meanings under shared term headings. The main homepage at
`https://zengez.github.io/mathDef/` is generated by:
1. `python scripts/build_index.py` — validate original .tex definitions and
   retain the historical original-only API export;
2. `python -m research_pipeline.adapters.mathdef.preview_site --site-root _site/reconstruction`
   — produce frozen research views and merged data;
3. `python -m research_pipeline.adapters.mathdef.publish_root --site-root _site`
   — render that exact merged catalog as the root site's searchable library.

The publisher checks **every original definition ID and each original
formulation text** against the source before allowing the release. The main
index now contains **2,197 contextual meanings across 2,048 searchable term
headings**, including all **1,014 original definitions**, 958 independent
Wave2 meanings, and 225 subsequent research meanings. Automatic
term links are labeled **Suggested** and research entries still identify
their provisional editorial status. Existing two-bar term/definition search,
in-line recursive expansion (default), other view modes and community feedback
are supported. Source files, review ledgers, and independent research
checkpoints are not rewritten for site publication. Research history remains
available under `/reconstruction/`.

**Deployment:** `.github/workflows/pages.yml` publishes the merged root
after the combined research builder. Do **not** silently revert production
to the old 1,014-definition standalone index or reintroduce a separate
production-only mathDef corpus in future edits. No additional vocabulary
candidate discovery is authorized by the publication request.

**CANONICAL CROSS-PROJECT DEFINITION FEED: v2 MERGED (2026-10-26).**
User confirmed the original-only v1 reference feed was not relied upon by
important current consumers; mathThm is a prototype they may substantially
rewrite. New integrations must use the merged v2 feed:
`https://zengez.github.io/mathDef/api/definitions/v2/manifest.json`
and `snapshot.json`. The snapshot mirrors the published merged main mathDef
catalog (term groups, multiple contextual meanings, alternative formulations,
original stable ID aliases, source attribution, and source-specific links).
The v2 manifest carries SHA-256 content versioning and full group/meaning/
formulation counts. `scripts/merged_definition_export.py` produces it on
every mathDef Pages publication, and mandatory CI verifies complete coverage.
The previous v1 feed remains an original-only historical endpoint rather than
misrepresenting it as the full current library.

For future mathThm/mathEd/mathThm-like consumers see `DEFINITION_EXPORT.md`
and `examples/consume_mathdef_v2.py` for the exact manifest/snapshot
contract, cache invalidation, SHA-256 validation, offline fallback, and
legacy ID lookup. Consumers select their own refresh schedule (often CI
build or daily), and no push notification or mathDef write access is needed.
**Do not edit mathThm automatically as a prerequisite**; migration is
documented for its future development. Existing independent corpus and
source research records remain unchanged. This integration work does not
authorize new terminology discovery.

**WHOLE-CORPUS CROSS-CHUNK LINK AUDIT COMPLETE (2026-10-26).**
A graph-wide, read-only audit checked **all 2,048 headings, 2,197 meanings,
2,246 formulations and 6,825 relations** in the public merged mathDef corpus.
There are 4,522 definition-use references (3,200 positioned, 1,322 screened
unpositioned) and 2,303 other directed relationships. All source/target IDs,
source offsets and phrases, deduplications, overlapping ranges, UI-visible
dependencies, rendered groups, and cross-cohort references passed. The
additional independent existing-term mention scan found **no unexplained
missing links**: six intentionally unresolved original mathematical
conventions remain, alongside two correctly suppressed directional metric-
ball false positives and correctly specialized CW weak-topology references.

Eleven links now internal to a single merged heading (five related, six
definition-use) remain in provenance metadata intentionally and are
suppressed as redundant navigation by the current UI, which shows all
meanings within the heading. They are **not broken or missing definitions**.

`research_pipeline/adapters/mathdef/audit_merged_links.py` is a **required
whole-graph publishing/CI validation** and generates a report at
`/audits/full-link-graph.json` on the public site. The verified report
and explicit limitations are recorded at
`research_pipeline/experiments/reconstruction-v2-independent/post_wave2/FULL_CORPUS_LINK_AUDIT_2026-10-26.md`.
The audit does not assert all suggested lexical links are human
mathematically certified; visitor suggestions remain welcome.
**Do NOT reclassify this existing-term link audit as permission to gather
new terminology candidates. No such discovery phase has begun.**

**As of 2026-10-26, the original 418-lead research pass is finished.**
The independent research preview contains **958 meanings**, with **1,511**
contextual relations (including **115 screened-to-direct incoming links**).
The original leads have dispositions: **350 incorporated** and **68 not
promoted**. The completed-pass record is
[`WAVE2_INITIAL_RECONSTRUCTION_COMPLETE_2026-10-26.md`](research_pipeline/experiments/reconstruction-v2-independent/WAVE2_INITIAL_RECONSTRUCTION_COMPLETE_2026-10-26.md).

**Do not restart the original 418-lead queue or revive dependency graphs,
stages, gates, and old audits.** The quick post-Wave2 terminology scan has
ALREADY COMPLETED across all 363 direct Wave 2 definitions and 1,014 original
mathDef definitions (+5 variants). The merged site has 1,972 original-plus-Wave2
baseline meanings, and the initial scan yielded 2,019 intentionally rough
phrase leads plus 473 known-term mention patterns.

**FROZEN ORIGINAL QUICK-SCAN CANDIDATE PHASE COMPLETE (2026-10-26).**
The original unchanged 2,019 phrase leads, gathered in the original-inclusive
rapid scan, have all been processed through rank **2,019 / 2,019** in
`research_pipeline/experiments/reconstruction-v2-independent/post_wave2/scan_candidate_dispositions.json`.
The final batch (ranks 1,781–2,019): **10 new mathematical meanings; 95
existing matches; 134 lexical/contextual fragments; 0 additional ambiguities**.
Existing ambiguities in earlier ranks remain documented in the ledger.

The post-Wave2 overlay `post_wave2/terms.json` has **225 meanings**:
118 initial researched meanings + 107 distinct scan-research additions.
The merged reference has **2,197 meanings**, composed of 958 independent
Wave2 + 1,014 original mathDef + 225 merged-only meanings. The 958 independent
Wave2 snapshot, original production `definitions/`, and original candidate
scan are unchanged. **There is no pending frozen terminology candidate rank.**
Do not initiate a new candidate discovery phase unless the user separately
authorizes it. Do not revive the discarded dependency graphs, mandatory slow
gates, review packets, retrospective independent Wave2 edits, or old queues.

**MERGED MATHEMATICAL LINKING AND FOLLOW-UP AMBIGUITY REVIEW COMPLETE (2026-10-26).**
The original frozen candidate queue remains **2,019/2,019 dispositioned**
(no new terminology discovery). The original corpus (**1,014 meanings**),
independent Wave2 (**958 meanings**), and merged-only overlay (**225 meanings**)
remain unchanged. The separate merged reference has **2,197 meanings** in
**2,048 headings**, comprising **2,246 formulations**.

The latest CI-verified linking pass creates **2,952 tentative, exact-source-
anchored** definition-use links (UI displays **Suggested**), positions **248
previously-screened** relations inline, and gives **1,732/2,246 formulations**
positioned links. Targeted context-based review addressed **111 of the
previously 117 ambiguous link occurrences**, either by research-backed
existing-meaning selection or suppression of source-specific false positives.

**ONLY 6 deliberate link ambiguities remain:** three `natural numbers`
occurrences (zero-included vs positive convention), two `inner product space`
occurrences (real vs complex scalar field), and one `ring homomorphism`
occurrence whose source expressly contrasts unital and non-unital
conventions. The generated `/reconstruction/merged/link-report.json`
records those examples for possible user feedback. They are **not** new
term candidates or missing definitions; do not force arbitrary meaning
selection. Other mathematical variants remain displayed without merging.

**VALIDATION:** 19 Python regression tests, exact anchored source-text,
independent and combined site builds, and actual headless Chromium tests
of two independent searches, nested/inline recursion, sibling reuse,
ancestor loop blocking, and mobile layout all passed.

**NO REQUIRED LINKING WORK GATES REMAIN.** Community suggestions can
address the remaining legitimate conventions if users encounter them.
Do not restart terminology searches, dependency graphs, per-edge
review packets, or edits to frozen independent Wave2/original sources.

Persistent follow-up research:
`research_pipeline/experiments/reconstruction-v2-independent/post_wave2/LINK_AMBIGUITY_REVIEW_2026-10-26.md`.
Earlier general linking closeout:
`research_pipeline/experiments/reconstruction-v2-independent/post_wave2/LINKING_CLOSEOUT_2026-10-26.md`.

## New explicit authorization: original-content merger and rapid scan (2026-10-26)

**After completing the independent Wave 2 reconstruction, the user explicitly
authorized scanning the 363 new definitions AND the original mathDef term
list/definition contents, and incorporating the original content into the new
searchable reference.** That changes the source-access rule *for the new
post-Wave2 merged view only*.

- Keep `/reconstruction/wave1/` frozen and `/reconstruction/wave2/` independently
  reconstructed at **958 meanings**; do not silently import the original corpus
  into that historical snapshot.
- The explicitly authorized `/reconstruction/merged/` view combines all original
  `definitions/*.tex`, `variants/*.tex` with independent Wave 2, preserving
  source IDs, citations, contexts and text. Production source files remain
  read-only. Match exact term labels under common search headings without
  asserting that their definitions are automatically equivalent.
- A fast lexical scan of new Wave 2 definitions and all original definition
  bodies yields **rough possible terminology** and existing-term mentions.
  These are error-tolerant starting leads only. **Do not turn the scan into
  another prerequisite-completion gate, graph closure or global approval audit.**
- See [post-Wave2 merge and scan record](research_pipeline/experiments/reconstruction-v2-independent/POST_WAVE2_ORIGINAL_MERGE_AND_SCAN_2026-10-26.md).

## Completed research method: build definitions, not a dependency-graph pipeline

The original dependency-first Wave 2 *workflow was abandoned by the project owner* because it made a deliberately rough candidate scan into an expensive, mandatory full-corpus mathematical review. **Do not resume or recreate its scans, aliases, amendment transactions, phase gates, staging ceremonies, or graph-resolution backlog.** No old workflow handoff, agent instruction in Git history, GitHub Actions log, old PR, or checkpoint supersedes this file.

### Fast, direct independent Wave 2 research

1. Use the already screened **independent** Wave 2 `research_pipeline/experiments/reconstruction-v2-independent/records/` as the starting draft corpus. Its screened relations are useful known links. The `population/records/` area contains 16 additional candidate meanings, not yet screened.
2. Use `research_pipeline/reviews/wave2-salvage-2026-10-26/CANDIDATE_WORKLIST_418.tsv` as a **tentative** research queue. Its existing 418 proposed candidate phrases and draft texts have source leads. Many will be duplicates, examples, notation, false positives, or variants. This is fine. **Never exhaustively pre-clear or globally deduplicate this queue before researching definitions.**
3. On each selected candidate, research the meaning and sources, choose its mathematical context and variants, compare plausible existing definitions, and **add/merge the researched definition and establish reasonable links within the same pass**. Save any newly noticed phrase as a future candidate; do not immediately recursively research it.
4. Add actual independent research definitions through simple batches to the **independent Wave 2 preview**, not via the removed `dependency_graph` / `generation_staging` workflows. Prioritize visible usable definitions and working links. A preliminary candidate-finding pass can contain mistakes and omitted terms.
5. Run **lightweight** checks on the resulting batch: valid IDs, supporting source URLs, mathematically honest statements, known conflict/edge-case flags, link endpoints that exist, no infinite nested-expansion loops. Document genuine mathematical ambiguities without blocking unrelated entries. User feedback is intended to improve completeness and linking iteratively.
6. Regularly show progress as definitions/variants/links actually visible in the prototype, not scans, review packets, gates or staging counters.

### Critical boundaries

- Original production mathDef was excluded as **mathematical input** for the historically independent reconstruction. It is NOW explicitly authorized as input to the separate **post-Wave2 merged view**, but must never be retrospectively counted as independently reconstructed. **Do not read/copy/search/import mathematical definitions, variants, data or citation content from `definitions/`, `variants/`, `data/`, or the production index** into Wave 2. Likewise do not import the frozen Wave 1 mathematical catalog. Code, shared UI and web build plumbing are reusable.
- Keep Wave 1 frozen. The independent Wave 2 draft and preview remain separate from production.
- Do not knowingly publish false mathematics or describe an unchecked lead as a verified direct source passage. State hypotheses and convention choices clearly; flag significant uncertain cases for later review. **Do not require perfect exhaustive review of every entry before making useful progress.**
- Do not add or re-enable graph-closure conditions, global first/second-pass review gates, or one-GitHub-Action-per-candidate submission workflows absent a new **explicit user request**.
- Do not run old Wave 2 batch-generation scripts, broad crawling, or old source-free reconciliation processes. The research materials and Git history already preserve prior evidence.
- Work on a branch for substantive changes, check the independent preview and production-site build before any merge, and never merge or publish production changes without authorized review.

For the retained assets and recovery details, see `research_pipeline/reviews/wave2-salvage-2026-10-26/SALVAGE_ASSESSMENT.md`. Older instructions are historical and superseded.
