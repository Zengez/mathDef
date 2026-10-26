# Independent Wave 2 — direct definition research (authoritative)

**Supersedes and replaces all earlier dependency-first Wave 2 handoffs**, including the removed `DEPENDENCY_FIRST_WORKFLOW.md` and `TEMP_DEPENDENCY_FIRST_WAVE2_PLAN.md`. Those earlier methods were specifically rejected by the owner after substantial repeated process overhead. Do not resume them from Git history, an archived PR, a previous conversation or a generated checkpoint.

## The actual project

Independently research mathematical meanings and make them visible on the Wave 2 prototype, with context-sensitive variants, attributed sources and correct links to known meanings. The first candidate scan is deliberately fast and error-tolerant, **not** a comprehensive classification/reconciliation project.

**Already available:** 595 screened independent meanings (639 formulations), 887 screened relations; another 16 provisional meanings (20 formulations), and 418 original candidate draft references covering 841 occurrences. No new full-corpus scan is needed to begin research.

**Research queue:** [the one-file 418-candidate TSV](reviews/wave2-salvage-2026-10-26/CANDIDATE_WORKLIST_418.tsv). These are leads, **not 418 guaranteed distinct or verified terms**. The 16 earlier guarded mathematical dispositions can inform later decisions but impose no workflow dependencies.

**Working site implementation:** `research_pipeline/adapters/mathdef/preview_site.py`, `preview.py`, `research_pipeline/ui/`, and independent screened `experiments/reconstruction-v2-independent/records/`. Do not rebuild the website; make independently researched new definitions/variants/links visible through this existing viewer. Its current screened-record reader does not yet include the separately provisional 16 meanings or candidate drafts. That *display gap*, not a graph gate, is the next software task.

### One efficient term pass

- Examine the tentative candidate and existing context/source lead.
- Research it to an appropriately rigorous draft, compare likely existing meaning/variants, and choose new/contextual variant/equivalent/not useful.
- Add or update the **independent preview's content and links** during the same term research pass. Use source locators with honest verification status. Queue newly encountered terms for *later*, without recursive detours.
- Validate simple structural integrity; record only substantive mathematical or source problems for focused later review.
- Commit practical content batches and test that they **render**, rather than running a separate scan, global reconciliation, staging, integration and publication pipeline.

The original production mathDef corpus and frozen independent Wave 1 are excluded from independent mathematical sourcing. There is no requirement to exhaust the candidate list or close all references before seeing new definitions.

**Do not recreate** the removed dependency graph, graph gate actions, node ledgers, alias amendment procedure, or archived Wave 2 wave-specific batch scripts unless the owner explicitly asks for those components anew.
