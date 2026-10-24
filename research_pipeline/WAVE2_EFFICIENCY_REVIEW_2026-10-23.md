# Independent Wave2 audit throughput review — October 23, 2026

## Reviewed evidence and objectives

This review examined the independent Wave2 operating plan, dependency-first execution contract, Round171–177 continuation reports, `dependency_graph.py`, `dependency_global_audit.py`, the GitHub Action workflows, and current live graph state. Audit rigor and provenance take precedence over simply lowering the count of unresolved identities.

**Verified pre-change authoritative state:** 611 meanings; 659/659 scanned; 420 unresolved canonical candidates; 297 aliases; 19 reviewed append-only seed overrides; 765 scan amendments; 838 effective missing occurrences; 651 open / 8 closed; consolidation gate false. Round177 has already applied all 19 justified historical category/functor scope corrections. Re-reviewing or re-submitting these would waste both reviewer time and graph work.

### Bottleneck 1: repeat full derived-index rebuild with no new source work

In the normal graph pilot, `inventory_sync()` reconstructs effective derived indexes. `apply_inbox()` processes and rebuilds only when fresh events exist. However `propose()` historically called `rebuild()` again when the proposal queue was **empty**, even though 659/659 formulations are complete. Each rebuild rereads the base graph and applies 765 amendment events, 297 alias entries, 19 seed overrides and the 891 original seeds, then rewrites the indexes and checkpoint.

**Implemented:** `research_pipeline/engine/dependency_graph.py` `propose()` now checks the authoritative inventory hash, current complete scan counts, consistent source/version checkpoint identity, valid node count, amendment event count and state-row digest. If all formulations are fully complete and the checkpoint matches, it returns the already validated summary with `proposed_this_run=0` and `reused_fully_scanned_checkpoint=true`, without invoking `live_nodes()` or `rebuild()`. It still falls back to the former path for unscanned/incomplete formulations or an invalid/stale checkpoint.

**Verified:** two new regression tests in `research_pipeline/tests/test_dependency_graph.py` assert (a) no effective-node replay or derived-index rewrite in the fully complete case, and (b) the normal path is taken for incomplete/stale checkpoints. [Research CI #40055171553](https://github.com/Zengez/mathDef/actions/runs/40055171553) SUCCESS. [Graph pilot #40055171480](https://github.com/Zengez/mathDef/actions/runs/40055171480) SUCCESS.

This saves **one redundant full graph rebuild** per qualifying proposal step; it does *not* skip the inventory synchronization, reviewed inbox processing, regression tests or mathematically meaningful scan work. No measured wall-clock performance figure is claimed.

### Bottleneck 2: every internal commit deployed the public website

The previous `.github/workflows/pages.yml` triggered on **every push to main**, including audit markdown and internal graph data/code. The action history contains numerous canceled/superseded Pages runs when several internal review commits landed in quick succession.

**Implemented:** path filters restrict automatic Pages deployment to **production definitions, variants, data, frontend, build scripts and independent reconstruction preview inputs**. Internal `dependency_graph/**` indexes, source-free audit markdown and engine tests alone no longer trigger public Pages deployments. `workflow_dispatch` remains an explicit manual option. Changes to independent meaning/record sources and preview renderer inputs remain eligible to publish.

**Verified:** [Pages run #40055171503](https://github.com/Zengez/mathDef/actions/runs/40055171503) SUCCESS for the workflow-definition change. The new filter's effect on subsequent documentation-only commits can be checked directly in Actions run history. This optimization does not change the rendered site content.

### Bottleneck 3: full research CI for report/checkpoint-only edits

Previously `.github/workflows/research-pipeline-ci.yml` tested every `research_pipeline/**` change, including markdown-only progress files. This made one ordinary audit round trigger multiple redundant isolated test runs when the report and status document were committed separately.

**Implemented:** exclude `research_pipeline/**/*.md` from the automatic research-pipeline CI trigger while retaining tests for **all executable code, graph state, JSON review manifests and actual research data**. Manual workflow dispatch remains supported. The complete isolated test suite, source-free global audit, frozen-lineage validation and independent preview smoke tests were **not removed**.

**Verified:** [Research CI #40055171553](https://github.com/Zengez/mathDef/actions/runs/40055171553) SUCCESS. Code changes still receive the full regression suite. Documentation updates are not mathematical authority and should not consume repeated execution jobs.

### Bottleneck 4: frequent GitHub connector calls and duplicated human review

Rounds171–177 repeatedly needed fresh effective nodes, original source texts, candidate context and old correction history. Read-only `dependency_global_audit focus` already provides a compact, consolidated view; it should be preferred to full 659-node and 724-candidate downloads. After identifying 19 source-anchored seed errors and applying them in Round177, subsequent reviewers must not reopen those issues without new contradictory evidence.

**Operational improvements:**
- Created `WAVE2_CURRENT_HANDOFF.md` (short current scope, goals, numbers and actionable next steps) to avoid rereading the 26KB chronological status file every round.
- Choose one substantive review area, retrieve exact candidate/source references through the existing focus utility, review all relevant source variants, then submit one reviewed batch, not one push per small edit.
- Use a **single multi-file Git commit** for code, tests and necessary workflow edits. The actual optimization was committed as one four-file Git tree at `2ebd2816fb15ee56f1069ef81d514be1a980840f`, yielding one set of validation workflows rather than four.
- Update concise handoff after meaningful changes and keep full reports historical. Document a specific non-merge / mathematical ambiguity rather than claiming an unsolved candidate must be a duplicate.

### Optimizations deliberately NOT performed

- **Skipping inventory reconstruction unconditionally** would weaken crash/replay safety after out-of-band graph edits or new source inputs. We preserved the initial full synchronization.
- **Auto-sealing or auto-researching missing definitions** would violate the independent source-free phase contract and conflate scan completion with mathematical correctness.
- **Automatically suppressing flagged mathematical risks** solely because they were reviewed once would erase legitimate future review obligations; the single unresolved setoid-size question remains visible.
- **Changing production definitions or the frozen Wave1 to achieve better metrics** would compromise the independent reconstruction protocol.

## Status and handoff

No semantic graph packets, source definition changes, aliases or consolidations were created as part of this optimization. Authoritative state remains unchanged. Continue to prioritize actual mathematical mismatches and evidence quality over throughput counts. For repeatable use, start with [WAVE2_CURRENT_HANDOFF.md](WAVE2_CURRENT_HANDOFF.md) and current STATE.json; only expand into full historical reports if a source-specific challenge warrants it.
