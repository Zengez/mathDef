# Wave 2 — source-free semantic reference scanning pilot (2026-10-21)

## Newest verified checkpoint — Batches 005–007 and corrective amendments

This section supersedes the earlier 42/659 status and the earlier
instruction to correct six field-extension aliases. Those corrections
were **completed** with append-only amendments.

| Committed package | New complete scans | Reference decisions | Existing links | Unassigned | Elementary/external | Verified run |
|---|---:|---:|---:|---:|---:|---|
| `semantic-existing-initial-005.json` | 12 | 62 | 35 | 19 | 8 | [39676180583](https://github.com/Zengez/mathDef/actions/runs/39676180583), success |
| `semantic-existing-initial-006.json` | 12 | 60 | 31 | 22 | 7 | [39676750624](https://github.com/Zengez/mathDef/actions/runs/39676750624), success |
| `semantic-existing-initial-007.json` | 12 | 62 | 27 | 30 | 5 | [39677495139](https://github.com/Zengez/mathDef/actions/runs/39677495139), success |
| **New scan work** | **36** | **184** | **93** | **71** | **20** | |

The source-free corrective package
`semantic-existing-correction-field-extension-001.json` amended **six**
existing completed scans: it replaced a single `unassigned` reference per
formulation with the correct preexisting contextual target
`meaning.7210832bc589f307.field-extension`, indexed under the title
`extension field`. Its full adjacency replacements and expected-node
hashes are saved in the append-only amendment ledger; all original
complete-scan files are preserved. Successful independent graph Action:
[39677088365](https://github.com/Zengez/mathDef/actions/runs/39677088365).

**Latest checked `dependency_graph/STATE.json`:**

- 611 contextual meanings and 659 independent definition formulations.
- **78 fully semantically scanned** (42 previously + 36 new), **581
  preliminary lexical scans** pending semantic review. All 659 Open
  (none structurally closed while downstream scans remain incomplete).
- **128 `unassigned` occurrences** presently in the effective graph. This
  count reflects the six append-only corrections, not six new missing
  meanings. **377 ambiguous lexical occurrences** still exist across
  incomplete proposals; all pending classification.
- Existing missing registry remains 13 candidate rows with 12 unresolved
  candidate meanings; no new terms, meanings, variants or external-source
  evidence researched or added.
- **6 graph amendment events**, phase `scan_and_link_existing`,
  `consolidation_gate_valid=false`, unrelated breadth on hold, missing
  definition research **not permitted**.

**Operational observations:**

1. The definition population remains unchanged; initial processing of
   references can proceed without switching to outside source lookup.
2. Version anchoring prevented a Batch 006 ingestion with a SHA value
   missing its final hexadecimal character. Corrected the exact same
   inbox file and reran; only the successful run and its receipt count.
3. Target-ID checks were performed before Batches 005–007, and a SHA
   check should also be made against `dependency_graph/nodes/` before
   each first commit to avoid the extra Action cycle.
4. The existing spelling `extension field` illustrates why confident
   synonym/context lookup matters. Six unassigned occurrences were
   recovered with only internal contextual review. No need to recreate
   the definition or repeat source research.

**Next fresh-Chat action:** Read
`research_pipeline/DEPENDENCY_FIRST_WORKFLOW.md`,
`research_pipeline/adapters/mathdef/resume_plan.json`,
the *live* `dependency_graph/STATE.json` and `CHECKPOINT.json`.
Run the source-free deterministic `--mode worklist --limit 8`.
Examine entire mathematical formulations, check existing contextual
meanings before recording `unassigned` occurrences, validate all meaning
IDs and version hashes against the saved inventory, and submit bounded
`mode=ingest` packages. Confirm success + graph applied receipt + counts
before claiming additional completion. Do not start missing-definition
research, global missing-occurrence consolidation, or unrelated breadth
until the whole initial collection has full semantic scans.

---


## Governing procedure

The current operating guide is [DEPENDENCY_FIRST_WORKFLOW.md](DEPENDENCY_FIRST_WORKFLOW.md).
The order is (1) source-free full-content scans and links to existing contextual
meanings, (2) global comparison and classification of **all** unassigned
reference occurrences, and only then (3) independent external source research
and population of consolidated missing meanings. Deliberate unrelated
breadth-first mathematical expansion is postponed further.

This work did not consult original production mathDef mathematical content,
did not browse external sources, did not alter reviewed definitions, did
not admit provisional definitions, and did not perform mathematical
certification or human sign-off.

## Actual verified work

| Committed graph inbox batch | Full semantic scans added | Reference decisions | Reviewed output | Verified GitHub Action |
|---|---:|---:|---|---|
| `semantic-existing-initial-002.json` | 12 | 63 | 40 existing links, 13 unassigned, 10 elementary/external | [39670049976](https://github.com/Zengez/mathDef/actions/runs/39670049976) SUCCESS |
| `semantic-existing-initial-003.json` | 12 | 63 | 32 existing links, 22 unassigned, 9 elementary/external | [39670636799](https://github.com/Zengez/mathDef/actions/runs/39670636799) SUCCESS |
| `semantic-existing-initial-004.json` | 12 | 66 | 31 existing links, 28 unassigned, 7 elementary/external | [39671358918](https://github.com/Zengez/mathDef/actions/runs/39671358918) SUCCESS |
| **Total new** | **36** | **192** | **103 existing links, 63 unassigned, 26 external** | |

Each batch is stored at
`experiments/reconstruction-v2-independent/dependency_graph/inbox/`,
with exact per-formulation content hashes; derived immutable node adjacency,
incoming/reverse indexes, state, and receipt files have been committed by
the consolidated GitHub Action. In the graph, a screened historical link
and an unreviewed lexical proposal are NOT treated as exhaustively scanned
mathematical references.

After these three batches, verified live `STATE.json` is:

- 611 existing contextual meanings and 659 individual formulations
  (639 independent screened, 20 previously provisional).
- 42 complete context-reviewed semantic scans in total (six preexisting + 36
  newly finished), 617 incomplete lexical proposal snapshots.
- All 659 remain Open; 0 Closed, as expected while linked descendants
  have incomplete scans.
- 63 unassigned reference occurrences saved for the later global
  consolidation phase. 393 ambiguous lexical occurrences remain, mostly
  from incomplete proposals, and are NOT yet fully reviewed.
- Twelve earlier unresolved canonical missing candidates remain; **none
  of this session's 63 unassigned references was prematurely registered
  as a distinct researched missing meaning**.
- Phase `scan_and_link_existing`; consolidation gate absent;
  missing-definition research NOT permitted; breadth Batch143 on hold.

## Lessons / caveats

1. Contextual matching found many correct links the string-only algorithm
   treated as ambiguous: ring homomorphisms, integral domains, ideals,
   Noetherian spaces, filtered colimits, Galois groups, etc.
2. A known **missed existing synonym** needs a reviewed correction:
   `meaning.7210832bc589f307.field-extension` has display term
   `extension field`, so six or more `field extension K/k` occurrences
   in the second group were left `unassigned`. No new definition should
   be researched for those occurrences; inspect the exact relevant
   snapshots and submit append-only `amend` events with correct
   content-version and expected-node digest. This is an existing-corpus
   reference correction, not external research.
3. The third batch's original submission contained an incorrect invented
   Noetherian-ring target ID, and its first Action failed safely.
   The correct existing target
   `meaning.86b5d488b98c612f.noetherian-commutative-ring`
   was committed in the same inbox package before successful admission.
   Pre-commit candidate ID existence verification would prevent this
   avoidable GitHub execution cycle. The successful receipt is the source
   of truth; the rejected older commit is NOT an applied scan.
4. The process handled 36 complete mathematical source-free scans and
   192 reference decisions in one Chat exchange, with successful bounded
   commits and restartable checkpoint recovery; we should continue
   measuring this before drawing quantitative efficiency conclusions.

## Next action for any fresh Chat

Read `DEPENDENCY_FIRST_WORKFLOW.md` and
`adapters/mathdef/resume_plan.json`. Inspect current
`experiments/reconstruction-v2-independent/dependency_graph/STATE.json`
and `CHECKPOINT.json`, then run:

```bash
W=research_pipeline/experiments/reconstruction-v2-independent
python -m research_pipeline.engine.dependency_graph --workspace "$W" --mode worklist --limit 8
```

Review entire unchanged independent formulations, connect confident existing
contextual meanings, and write unresolved mathematical usages as
`state: "unassigned"` with source phrase/context. Save reviewed
`complete: true` packages to graph inbox, wait for GitHub Action
receipt and check current STATE before counting progress. No external
mathematical research or adding missing definitions yet. Correct previously
missed field-extension links through reviewed append-only amendments in
a bounded maintenance group, not by rewriting immutable initial scans.
