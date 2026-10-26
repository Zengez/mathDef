# Wave 2 — Initial independent reconstruction COMPLETE (2026-10-26)

**Completion scope:** the original 595 independent screened meanings, the initial independent candidate research pass, direct addition of useful mathematical meanings, and conservative integration of new meanings with existing screened definitions. This records the **finished initial reconstruction**, not formal mathematical publication or an exhaustive taxonomy of mathematics.

## Verified completion inventory

| Item | Count |
|---|---:|
| Original independently screened contextual meanings | 595 |
| Original screened formulations | 639 |
| Direct researched contextual meanings | 363 |
| **Independent Wave 2 contextual meanings** | **958** |
| **Total formulations** | **1,002** |
| Distinct displayed term groups in CI preview | 917 |
| Original source-screened links | 887 |
| Outgoing links from newly researched definitions | 509 |
| Curated incoming links from original definitions to new meanings | 115 |
| **Total independent Wave 2 links** | **1,511** |
| Original rapid-scan candidate leads considered | 418 |
| Original leads represented by directly researched entries | 350 |
| Original leads not promoted (covered/contextual/notation), each recorded | 68 |

**Traceability:** [Closeout of all 418 candidate leads](direct_research/CANDIDATE_WORKLIST_CLOSEOUT_2026-10-26.md); researched definitions [terms.json](direct_research/terms.json); curated incoming connections [incoming_links.json](direct_research/incoming_links.json). The 68 dispositions were recorded as research judgments, **not** exhaustive proofs that no other variant may merit its own term.

**Link integration boundary:** The incoming links connect **already screened initial independent formulations** to the previously researched direct meanings. They were selected conservatively from explicit textual matches, rejecting unclear semantic coincidences. The 841 original rough-reference occurrences were not required to turn into 841 links. Links not obvious from the existing text were allowed to remain unresolved. No scan of newly added definitions for additional terminology was performed as part of this completion.

## Evidence supporting completion

- All 418 rough candidate leads were examined and either added as independent mathematical meanings/contextual variants or given a closeout disposition; there is no active candidate-admission gate or graph-closure task.
- The existing Wave 2 preview builds from independent research inputs only, with the original mathDef production corpus excluded as a source. The frozen Wave 1 reference remains separate.
- Branch CI on the final integration checked the independent Wave 1/2 preview build, original production builder regression, directly added searchable terms, all incoming-link endpoints and phrase evidence, and the reusable reference UI. The completion-status change is also covered by the standard checks.
- The public Pages workflow is configured to deploy the separate `/mathDef/reconstruction/wave2/` preview on pushes to `main` that change preview code or direct research data. **A successful CI build is not itself proof that GitHub Pages has finished deploying**; actual hosted availability must be checked separately if needed.

## What completion does *not* mean

- This is **not** a blanket human review or mathematical peer review of all 958 meanings.
- Many directly researched meanings still cite explicitly labeled *source leads not independently rechecked*. Do not describe those as verified direct source passages.
- It does not guarantee every useful alternate definition, synonym, or mathematical relation is present. Correct problems when discovered; do not impose a retroactive audit gate.
- It does not mean the deprecated `STAGES` engine was formally sealed or should be used again; the preview intentionally reads the independent screened records plus direct additions without that gate.

## Stop point and next step

**STOP POINT REACHED:** Original Wave 2 initial reconstruction and its existing-to-new link integration are complete. The immediate *next* expansion, **not yet started**, is a deliberately fast, error-tolerant scan **of the 363 newly added definitions** for possible *additional* mathematical terminology. That will create tentative leads for a subsequent expansion pass, followed by selective research-and-add work. It is not permission to reopen the abandoned recursive dependency graph, global alias reconciliation, or multi-stage approval machinery.

The initial Wave 2 snapshot is retained on `main` in its independent experiment directory. Subsequent expansion work must preserve the independently reconstructed material and distinguish newly researched additions from this checkpoint.
