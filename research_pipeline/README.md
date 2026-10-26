# Scholarly reconstruction research (retained data, simple workflow)

The **active** independent Wave 2 workflow is [WAVE2_SIMPLE_WORKFLOW.md](WAVE2_SIMPLE_WORKFLOW.md), not the obsolete dependency-first multi-pass research pipeline. The prior elaborate graph/gating machinery has been retired.

The already independently researched Wave 2 corpus is stored in `experiments/reconstruction-v2-independent/records/` (595 screened contextual meanings, 639 formulations, 887 existing-target screened relations), plus `population/records/` (16 additional provisional meanings, 20 formulations). The [recovered 418-candidate worklist](reviews/wave2-salvage-2026-10-26/CANDIDATE_WORKLIST_418.tsv) is a tentative queue for direct research; use the [salvage assessment](reviews/wave2-salvage-2026-10-26/SALVAGE_ASSESSMENT.md) to locate other reusable mathematics and source material.

Run the existing independent preview builder:

```bash
python -m research_pipeline.adapters.mathdef.preview_site --site-root /tmp/mathdef-reconstruction
```

It renders the frozen independent Wave 1 and the current **screened** Wave 2 draft without using the original production mathematical data. Its current Wave 2 input is the screened records; the extra provisional meanings and researched candidate drafts must be incorporated through a simple independent preview-content path before they appear in the website. Build on the existing `preview.py` and shared `ui/`, not a new frontend.

**Active rule:** Research candidates and add content/links in the same pass, allowing an imperfect queue and future user corrections. Do not resurrect global graph consolidation, serial phase gates or mass source-free re-audits. Continue to preserve original mathematical assumptions, source provenance, independence from the production 1007-term collection and frozen independent Wave 1. Historical scripts remain recoverable from Git history, but they are no longer the current workflow.
