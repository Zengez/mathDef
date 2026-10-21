# Wave 2 — source-free semantic reference scanning pilot (2026-10-21)

## Latest continuation — Batches 017–022 (189/659 complete)

This section supersedes all earlier numeric checkpoints. The authoritative
`dependency_graph/STATE.json`, saved node records and `applied/` receipts
take precedence if newer Actions have run.

The independent Wave2 contextual catalog remains **611 meanings** and
**659 existing formulations**. This continuation advanced from **168**
completed source-free semantic scans to **189** (**21 new scans**) with
**99 full-scan reference decisions**:

| Batch | Completed formulations | Reference decisions | Verified successful graph Action |
|---|---:|---:|---|
| `semantic-existing-initial-017` | 1 | 4 | [39690064912](https://github.com/Zengez/mathDef/actions/runs/39690064912) |
| `semantic-existing-initial-018` | 4 | 17 | [39690483687](https://github.com/Zengez/mathDef/actions/runs/39690483687) |
| `semantic-existing-initial-019` | 4 | 19 | [39690581793](https://github.com/Zengez/mathDef/actions/runs/39690581793) |
| `semantic-existing-initial-020` | 4 | 20 | [39690901573](https://github.com/Zengez/mathDef/actions/runs/39690901573) |
| `semantic-existing-initial-021` | 4 | 22 | [39691039590](https://github.com/Zengez/mathDef/actions/runs/39691039590) |
| `semantic-existing-initial-022` | 4 | 17 | [39691186057](https://github.com/Zengez/mathDef/actions/runs/39691186057) |

**Verification:** Every package has an `applied/<batch>.json` receipt,
and its graph Action finished successfully. The isolated pipeline
tests also passed, including run 39691185891.

**Current verified graph:** 189 complete, 470 incomplete lexical
proposals, no unscanned; 271 unassigned reference occurrences,
313 preliminary lexical ambiguities, 13 historical missing-candidate
rows (12 unresolved), 10 append-only correction events. All 659 are
Open and phase remains `scan_and_link_existing`. The consolidation
gate and missing-definition research remain OFF.

**Operational finding:** Batch 020 initially failed at validation because
two entries referred to nonexistent meaning ID
`meaning.wave2.foundation.mapping-total`. No scan was applied by that
failed run. We checked the independent catalog and corrected the
*unapplied* batch to the actual total-function meaning
`meaning.wave2.foundation.mapping-element-assignment`. Rerunning
the GitHub Action succeeded and generated the verified receipt. This
reinforces the existing rule to validate every target against the live
independent catalog, not to infer IDs from plausible names.

The work exclusively reviewed the contents of existing independent
formulations and linked existing meanings (or recorded unassigned
references). No outside mathematical sources, original production
definitions, additional mathematical meanings, global consolidation,
research into missing candidates, promotion, Wave1 modifications,
reviewed Wave2 content edits or unrelated Batch143 work occurred.

**Next deterministic worklist:** `form.709d3d2f82950c5b.inverse-system`,
then `form.709d3d2f82950c5b.partially-ordered-set`, then
`form.709d3d2f82950c5b.preordered-set`. Use
`python -m research_pipeline.engine.dependency_graph --workspace research_pipeline/experiments/reconstruction-v2-independent --mode worklist --limit 8`
or equivalent GitHub read access; verify exact hashes and target IDs;
commit bounded unique `inbox/` batches and wait for successful
receipt before increasing completion counts.

---


## Most recent verified continuation — batch 016

This section supersedes the older 160-completed handoff below.
The live graph following GitHub Action 39689345544 reports **168 / 659**
complete source-free semantic scans, with **491** remaining preliminary
lexical-only forms. All 659 are still structurally Open.

The successfully committed and applied
`dependency_graph/inbox/semantic-existing-initial-016.json` contains
eight full source-free scans, covering topological modules and rings,
scheme gluing, closed subschemes of affine schemes, and the five
generalization/specialization relation and map formulations through
`specialization-topological` (the next entry is
`specializing-continuous-map`). The graph Action
[39689345544](https://github.com/Zengez/mathDef/actions/runs/39689345544)
finished SUCCESS; matching `applied/semantic-existing-initial-016.json`
receipt is committed and verified. Isolated pipeline tests also passed.

Verified graph summary: 611 contextual meanings, 659 total formulations,
168 complete, 491 incomplete, 0 unscanned; 258 unassigned occurrence
records, 323 ambiguous preliminary lexical occurrences, 13 previously
identified candidate records with 12 unresolved, 10 append-only
correction events; phase `scan_and_link_existing` and research gate
closed. No external source research, additional definitions, promotion,
human mathematical certification, original production-corpus comparison,
or unrelated breadth work occurred.

A **follow-up batch 017 is not applied or committed**. Attempts to create
its new inbox file were rejected by the GitHub write integration before
any data changed. Those attempted scans do not count toward the total.
The next worklist item remains
`form.672a4a502273760f.specializing-continuous-map`,
followed by the Grothendieck fibration, strongly-cartesian arrow, and
universal exact sequence formulations. Resume through the ordinary
`inbox` contract and verify the receipt before claiming their completion.
If new-file GitHub writes remain blocked, inspect the active connection
rather than bypassing access controls or modifying immutable scan nodes.

---


## Newest verified continuation — Batches 012–015 (160/659 complete)

**This section supersedes older 78- and 126-scan counts below.** Direct
GitHub graph STATE.json, node snapshots, and applied inbox receipts remain
authoritative if any newer batch has been applied.

| Independent, source-free scan package | Complete scans added | Reference decisions | Successful graph Action |
|---|---:|---:|---|
| `semantic-existing-initial-012.json` | 8 | 34 | [39687479871](https://github.com/Zengez/mathDef/actions/runs/39687479871) |
| `semantic-existing-initial-013.json` | 10 | 48 | [39687813998](https://github.com/Zengez/mathDef/actions/runs/39687813998) |
| `semantic-existing-initial-014.json` | 8 | 41 | [39688077352](https://github.com/Zengez/mathDef/actions/runs/39688077352) |
| `semantic-existing-initial-015.json` | 8 | 45 | [39688373726](https://github.com/Zengez/mathDef/actions/runs/39688373726) |
| **This continuation** | **34** | **168** | **All four applied, receipts verified** |

This continuation scanned the existing independent meanings and formulations
in deterministic order, including finite limits/colimits, primitive elements,
associated primes, affine schemes, local rings, coherent rings, diagrammatic
set limits/colimits, field extensions, fibred groupoids, locally ringed
spaces, quotient rings, exact functors, separable extensions, scheme morphisms,
filtered colimits, and topological/profinite groups. Cross-context concepts
were linked to real IDs only after checking the existing independent registry.
Uncertain mathematical references were kept as `unassigned`; simple
quantifiers or elementary scope conditions were given explicit `external`
dispositions. A total of **168 full-scan occurrence decisions** were saved.

**Verified current graph, following Action 39688373726:**

- **611** contextual meanings, **659** formulations: **160 complete semantic
  scans**, **499 preliminary lexical-only**, **0 unscanned**.
- **254 unassigned** mathematical-reference occurrences (up from 218 at
  restart), and **328 preliminary ambiguous** occurrences (down from 349).
- **13** historical missing-candidate records, **12** unresolved candidates;
  **10** existing append-only correction events, none new in this continuation.
- **659 Open**, **0 Closed**, phase `scan_and_link_existing`,
  `consolidation_gate_valid=false`. Mathematical-research gate remains OFF;
  this is neither independent mathematical certification nor approval.
- All four receipts are stored at
  `experiments/reconstruction-v2-independent/dependency_graph/applied/`.
  All four submitted packages were version-checked against current
  `dependency_graph/nodes` and each existing meaning target against the
  original independent meaning registry before being committed.
- No external mathematical-source lookup, production-mathDef comparison,
  definition research/admission, frozen Wave1 modification, screened Wave2
  content change, provisional promotion, global consolidation, or Batch143
  breadth expansion occurred.

**Next saved deterministic worklist:** the first pending formulation is
`form.646e4dcbd9b6f1e1.topological-module`, followed by
`form.646e4dcbd9b6f1e1.topological-ring`,
`form.65fea875f9a5aa40.gluing-data-schemes`, and
`form.6676171d9e5698af.affine-closed-subscheme`.
Resume by checking live STATE/CHECKPOINT; use
`--mode worklist --limit 8` to obtain full content and exact version
anchors. Do not repeat batches 012–015 or earlier verified 011a/011b.
Complete the remaining 499 source-free semantic scans before starting Pass 2.

---


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
