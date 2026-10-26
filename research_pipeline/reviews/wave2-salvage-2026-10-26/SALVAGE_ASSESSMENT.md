# Wave 2 salvage assessment — 2026-10-26

**Purpose:** Retain the usable mathematics and prototype while ending the unnecessary requirement to complete a fully reconciled dependency graph before researching or displaying new definitions. This is a diagnostic/recovery assessment, **not** another stage gate or an instruction to re-audit everything. The independent Wave 2 preview and its data remain separate from the production 1007-entry mathDef collection and frozen independent Wave 1.

## Salvaged immediately: usable assets

| Asset | Verified current inventory | Reuse decision |
| --- | --- | --- |
| Original mathDef website/database | Main README documents 1007 draft mathematical definitions; existing public UI and feedback mechanisms | **Preserve entirely.** Production is neither a source for the independent Wave 2 reconstruction nor something to change during recovery. |
| Frozen independent Wave 1 | Independent preview exists; CI expects 419 contextual meanings | **Preserve as comparison baseline**, never overwrite. |
| Independent Wave 2 screened mathematical content | `records/meanings.jsonl`: **595** contextual meanings containing **639** formulations; `records/relations.jsonl`: **887** source-screened existing-target definition links; **953** source observations; **14** source records | **Keep and use now.** These are real independent mathematical drafts, not merely dependency planning. Individual correctness remains provisional; do not demand a blanket re-review. |
| Additional independent provisional population | `population/records/meanings.jsonl`: **16** contextual meanings and **20** formulations; `population/records/relations.jsonl`: **21** candidate relations; **20** observations, **1** source | **Keep as candidate content.** Already drafted, but distinguish from the 595 screened ones. Their status does not make them automatically certifiable/public. |
| Existing working independent preview | `research_pipeline/adapters/mathdef/preview_site.py`, `preview.py`, `preview.js`, plus reusable `research_pipeline/ui` renderer | **Reuse interface and rendering.** Crucial limitation: current `preview.build(draft=True)` invokes `read_working_draft` and loads **screened `records/` only**; it **does not display the extra 16 provisional meanings or 418 backlog drafts**. Solve this display gap for research content, rather than reconstructing a new website. |
| Original preliminary missing-candidate research | **418/418** frozen canonical candidate identities (some with previously reviewed aliases), **841/841** incoming uses, **16** historical JSON batch files, at least one draft mathematical statement and an HTTPS source locator per entry, **291 unique source URLs** | **Keep; immediately usable as a queue.** All 418 are now normalized as lightweight [`CANDIDATE_WORKLIST_418.tsv`](CANDIDATE_WORKLIST_418.tsv), with original IDs, phrase, context, tentative draft, URLs, source-status caveats, occurrence counts, and any reviewed staging disposition. No additional pass is needed simply to discover these candidates again. |
| Guarded disposition records already completed | **16/418** original identities have `generation_staging/records/` on **draft PR #19**: 13 preliminary `new_meaning`, 2 `specialization`, 1 `equivalent_to_existing` | **Salvage mathematical comparisons and provisional definitions**, including the exact successor-ordinal equivalence. They are not admitted independent meanings, graph resolutions or website content. Do not require all other candidates to go through these gates before research can continue. |
| Dependency graph and amendment history | All **659/659** formulations scanned; **3,598** scan-reference occurrences; **775** amendment events; **300** alias candidate records; **418** graph identities unresolved | **Archive/retain as reference hints and provenance**, not as the principal task scheduler or definition-admission gate. Counts of graph mutations do not represent newly researched website definitions. |
| Historical source and mathematical review material | Independent Wave 2 `wave2/` research ledgers and cited evidence, plus original observations/formulations | **Keep searchable.** Consult selectively when a real ambiguity/error arises; never conduct another blanket audit solely because a new term was added. |

### Integrity verification of the recovered queue

The new TSV was assembled exclusively from the 16 original preliminary-research batches on the draft research branch. Its creation verified:
- Exactly **418 unique** frozen canonical missing-candidate IDs with priorities 1 through 418, no omitted or duplicate priority.
- Every candidate has a **tentative mathematical definition** and at least one **HTTPS source URL**; diverse historical field names were normalized, without changing the mathematical text.
- Original reference-occurrence counts sum to **841**, matching the frozen cohort.
- **16** staged records have their disposition shown, but are not presented as published or accepted.
- The source-status labels remain original claims/leads; **291 distinct URLs are not 291 independently verified references**. A source URL does not prove a definition is correct.

The TSV is a **worklist, not an import of 418 mathematically verified terms**. It includes notational conventions, unnamed operations, already-known mathematical meanings, specializations and genuine missing definitions. For example, `α∪{α}` is already the existing successor-ordinal meaning; this was correctly identified by earlier guarded review.

## What NOT to carry forward as mandatory work

1. **No mathematically complete first scan.** Original intent: ultrafast candidate *extraction*, accepting duplicates, uncertainty, false positives and omissions. The 418/841 queue already exceeds that initial goal.
2. **No Pass 1 → exhaustive classification Pass 2 → sealed gate → research Pass 3 as required chronology.** This is the main time sink; work should go directly from candidate queue to term research and visible experimental-site definitions.
3. **No repeated source/corpus audits for every new term.** Compare the *meaning* with likely overlapping independent meanings and source evidence once during that term's research; save source/edge caveats. Do not demand literal or lexically forced merges.
4. **No per-candidate GitHub Action/commit as a prerequisite.** Prepare 20–50 real mathematical content decisions together where useful; commit/test once per practical output batch.
5. **No automatic reopening of hundreds of historical graph nodes** as the cost of writing or displaying one definition. Incrementally link what was confidently researched, maintain a "needs link review" note otherwise, and improve with future research/user corrections.
6. **No new generalized pipeline before the prototype can consume simple new additions.** Existing 94-engine-module directory and extensive workflow/test infrastructure can remain archived; avoid another refactor campaign.

## Shortest constructive route (proposal; no production edits made here)

1. **Use the 595 screened meanings and 887 screened relations immediately** through the already working independent Wave 2 preview. Preserve all source citations and original IDs. The extra 16 provisional meanings are next to include, honestly labeled.
2. **Close the narrow display gap**, rather than rebuilding the system: implement one simple independent-preview content intake (e.g. a plain JSONL of new researched meanings containing term/context/definition/source URL and optional known target IDs), display it through the existing preview renderer, and mechanically check that referenced IDs exist. Treat this as a straightforward website content input, **not as another gated research pipeline**.
3. **Pilot actual new content**, beginning with the 13 new-meaning/2-specialization research dispositions whose mathematics was already compared, plus a handful of straightforward unstaged candidates. On each candidate: inspect current draft + source, compare likely existing meanings, **add or merge the content and links right then**, record newly encountered future-term leads in the queue. Mark dubious cases for separate later review.
4. **Make a visible website change in the first implementation batch.** Success is definitions and meaningful clickable links appearing in the independent Wave 2 prototype, not completing another audit, report or ledger.
5. **Retain the existing graph snapshot as optional advice** (source occurrence contexts, inbound linking hints) but never require the 418 original unresolved graph identities to be reduced to zero before showing new content.
6. **Benchmark actual useful output:** accepted/provisional research definitions that render, source citations attached, working links, and rough effort per completed term/batch. Stop/reassess immediately if process overhead approaches the cost of term research.

### Scope and safeguards worth keeping

- Keep original mathDef production corpus unchanged and **do not import it into independent Wave 2**.
- Preserve frozen Wave 1 and source/author attribution where known.
- No knowingly false mathematics, unsupported equivalence merges, or silently invented source certification; retain mathematical edge conditions and risk-based holds.
- No circular clickable-expansion loops, unknown target IDs, or corrupt data structures.
- Mathematical uncertainty, incomplete linking and imperfect initial coverage are **allowed** and clearly indicated in the experimental website. Community correction was always intended as an ongoing feedback mechanism.

## Immediate stopping rule

**Do not do more staging, graph consolidation, infrastructure tuning or source-wide verification merely because they are next on the old checkpoint.** The next useful activity after this salvage handoff is **directly making researched Wave 2 mathematical content render in the existing independent prototype**.

This salvage operation created only the normalized research worklist and this assessment on the existing **draft research branch**, without changing the independent dataset on `main`, the protected production mathDef content, or Wave 1. Do not merge PR #19 in its present state merely because the salvage assessment was completed.


## October 26 cleanup implementation — old workflow retired from the working tree

This section supersedes any earlier statement in this assessment suggesting the dependency graph should be retained as an active in-tree reference or that graph resolution remains an outstanding workflow.

The cleanup on [PR #20](https://github.com/Zengez/mathDef/pull/20) removes the rejected `dependency_graph/` subtree, `generation_staging/`, graph engine and gate actions, 178 obsolete automated workflows, and the former agent/hand-off instructions directing assistants back into source-free consolidation. Git history still contains the originals, but **they are no longer prerequisites or active instructions**.

The immediately useful mathematical artifacts are retained in the repository:
- [418-entry tentative worklist](CANDIDATE_WORKLIST_418.tsv) with 841 original occurrences and source pointers;
- [16 full source-evidence JSON research batches](source_evidence/) (the original source-research detail, as source leads and qualified evidence);
- [16 previously reviewed mathematical dispositions](PREVIOUSLY_REVIEWED_16.json), stripped of gate transaction mechanics;
- the unchanged independently researched Wave 2 `records/`, provisional `population/records/`, earlier local `wave2/` mathematical notes, source evidence, original frozen Wave1, and functioning preview.

**The single current execution instruction is [WAVE2_SIMPLE_WORKFLOW.md](../../WAVE2_SIMPLE_WORKFLOW.md) and the root [AGENTS.md](../../../AGENTS.md).** Work on independently researched definitions and links directly; do not resurrect former dependency graph machinery from Git history.


## Second cleanup: remove remaining generated bookkeeping, retain mathematical substance (2026-10-26)

After the first merged removal of dependency-graph gates and 178 Actions, a second independent audit found another **728 obsolete files** occupying approximately **48.9 MiB** as Git working-tree content. This is not a new review gate; it is a record of actual removals. The removed files are generated `state/wave2_*snapshot*` variants and old stage progress logs, already-applied `intake/` packets, old per-batch `events/` edits, historical source-priority task queues, abandoned `reconstruction-v1/` pre-freeze test workspace, deprecated Stage 2–5 Python engines and their tests, and superseded review proposals.

**Still retained and functionally checked:** `records/` (595 screened meanings, 639 formulations, 887 screened relations), `population/records/` (16 independent provisional meanings plus other evidence), the entire immutable 418-candidate salvage dossier including original 16 source-evidence files, 16 reviewed mathematical dispositions, `wave2/` source/mathematical review notes (aside from two generated task queues), `state/wave2_formulation_reviews.jsonl` (the current detailed mathematical review record), `events/revisions.jsonl` and the meaning-text revision attestation for provenance, the five active stage-state summaries and baseline record, frozen `reconstruction-v1-recovery/`, and `evaluation/compare.py` for a later explicitly approved *post-independent-freeze* comparison. Evaluation does not authorize reading production math as inputs to Wave 2.

**Still current:** root `AGENTS.md` and `research_pipeline/WAVE2_SIMPLE_WORKFLOW.md`; existing independent preview code and shared UI. All old state snapshots and execution scripts remain recoverable from Git commit history, but **must not be treated as executable next steps**. Progress should mean researched meanings, variants and actual working links appearing in the experimental viewer.
