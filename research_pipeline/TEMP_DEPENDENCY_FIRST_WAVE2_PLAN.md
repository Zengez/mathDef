# TEMPORARY DESIGN NOTE — Dependency-first Wave 2 workflow

**Status:** Agreed design intent only; **NOT implemented or activated**.
**Date:** 2026-10-21.
**Project:** independent reconstruction of mathematical definitions in `Zengez/mathDef`.
**Lifecycle:** Keep this temporary file while developing and testing the proposed
scripts/methodology; delete or archive it only after the durable documentation,
tests, and implementation faithfully incorporate its decisions.

> **START HERE IF CHAT CONTEXT IS LOST.** This note records the user's intended
> process and subsequent clarified decisions. Do not resume broad Batch143
> source/topic population simply because older checkpoints say to do so. First
> implement/pilot the dependency-first mechanism described here, unless the user
> explicitly changes priorities. This is a design checkpoint, not a request to
> start executing the new algorithm automatically.

## 1. Purpose and scope

At any point, including immediately after Wave 1, we have existing terms,
contextual meanings, one or more definition formulations/variants, and source
provenance. Wave 2 is intended to:

1. Find missing mathematical terms/meanings and missing variants; add them,
   including source-supported contents.
2. Cross-link references in each definition formulation to the **appropriate
   contextual meaning** already in the collection, or discover missing meanings
   needed to complete those references.
3. Compare attributed sources to the contents and source-specific variants.
4. Check mathematical contents and the contextual validity of variants.

**Scheduling decision:** Prioritize systematic linking and dependency-driven
completion of the **current independent collection**, *before* deliberately
researching unrelated mathematical subject areas. Definitions added to satisfy
discovered missing dependencies are **expected** to enlarge the collection;
the pause applies only to *unrelated breadth expansion*, not dependency-driven
additions. After the present network stabilizes, run a separate deliberate
breadth/variant discovery phase, then integrate that material using the same
dependency workflow.

The requested 'completed'/'closed' state is **the assistant's automated
research/linking state**, *not* verified or approved by the user. Do not
silently equate mechanical graph completion, successful GitHub Actions, or
assistant mathematical screening with authoritative correctness.

## 2. Exact list/state terminology from the discussion

Unit of traversal: **a definition formulation/variant in a specified
mathematical context**, rather than an undifferentiated display word. The
persistent graph's link begins at a formulation and points to a contextual
meaning; a meaning may expose several alternative formulations.

- **Open Terms:** Initially every existing formulation/variant is open. The
  list stays populated across dependency-completion iterations. A node can be
  removed when its own links and all recursively reachable dependencies have
  completed processing and none remain missing/ambiguous/unresolved. In the
  user's language, anything not on Open is implicitly **closed**.
- **Encountered:** The user's initial scan/visit of a formulation, equivalent
  to the assistant's 'scanned' label. A currently encountered formulation is
  **never descended into a second time** during a traversal, preventing
  infinite recursion.
- **Completed:** The user's linking traversal has finished processing a
  formulation's references and descending into previously unencountered
  existing references; equivalent to the assistant's 'linked' traversal
  completion. **Completed does not imply closed**: some direct or transitive
  references can still be in the Missing Meanings registry.
- **Missing Meanings:** A single **shared, deduplicated registry** of
  contextual meaning candidates not currently represented. It is consulted
  before any expensive investigation into a candidate; multiple references
  to the same missing meaning attach occurrences to ONE candidate.
- **Closed (implicit):** A formulation no longer on Open, once all discovered
  relevant dependencies are accounted for. A cycle of existing references
  does not, by itself, prevent structural closure; circular *mathematical
  definitions* can be flagged separately for the later consistency audit.

Implementations may materialize additional internal states (unscanned,
actively visiting, waiting, ambiguity, blocked, explicit exceptional
disposition), but these must preserve the user's definitions above. Treat
an unencountered formulation as unscanned in the current traversal. Persistent
per-version scan results can replace redundant future traversals.

## 3. Initial graph/link pass — user's DFS logic

0. Snapshot the current **independent** collection (both existing screened
   records and separately stored provisional population records), including
   each contextual meaning and each formulation/variant. Put **all** of the
   existing formulation nodes on Open Terms. Do not access the original
   production mathDef mathematical corpus.
1. Select an Open formulation that has not yet been encountered in this
   traversal. Mark it encountered **before** exploring references. Scan its
   content for candidate mathematical terminology. The originating formulation
   is also counted as encountered.
2. For **each** candidate reference, perform inexpensive contextual lookup
   **in this order**:
   (i) existing relevant meanings/variants in the current registry;
   (ii) already-recorded missing-meaning candidates (including aliases,
   expected object type, source wording and contextual hints);
   (iii) only then register a genuinely new missing-meaning *candidate*.
   Do not do a full source investigation or formalize an elaborate new
   meaning before checking the shared Missing Meanings registry.
3. If an existing contextual meaning matches, create a provisional link
   (with origin formulation, reference/phrase/context and target meaning).
   If its relevant formulations have not been encountered, descend into them
   depth-first and repeat scanning/linking. If already encountered, simply
   create the link and **do not recursively revisit the node**.
4. If the reference matches a previously registered missing candidate, reuse
   that candidate ID, add the new incoming occurrence, and **do not
   re-research** it. Where a word could refer to several meanings and context
   is insufficient, record ambiguity; do not invent an arbitrary link.
5. When no further **existing unencountered** reference can be descended
   into, mark the current formulation **completed** and unwind. Return to
   the original formulation and continue remaining unvisited references.
   Eventually mark the original completed.
6. Pick another Open formulation not completed in this traversal; continue
   until all the initial formulations are completed/scanned.
7. Remove from Open all nodes whose own and recursively reachable
   dependencies have finished traversal **and** have no outstanding missing or
   ambiguous reference. Keep blocked nodes Open with explicit reasons.
   Conceptually reset ephemeral encountered/completed walk lists, **not**
   Open or the persistent graph, cached scans, missing registry, provenance
   or reverse dependency index.

**Cycle clarification:** A→B→C→A is traversed just once per node, because
A is already encountered when C reaches it. Linking C→A remains valid.
DFS recursion is not permitted to loop; this is distinct from a later
mathematical review of whether the definitions are mutually circular.

## 4. Missing-meaning research, iteration, and incremental optimization

Once the initial graph pass has consolidated missing candidates:

1. Prioritize the registry, e.g. number of affected formulation occurrences,
   number of *distinct* upstream dependents, contextual significance,
   source availability and research cost. Do not investigate duplicates.
2. Research a bounded cluster of missing contextual meanings from reputable
   sources, identify their meaningful variants/conventions, write attributed
   source observations and independently authored mathematical formulations.
   Maintain the existing source-rights, rationale, identity and append-only
   provenance safeguards. At this stage they can remain **provisional**.
3. Admit newly researched meanings into the **independent** research corpus
   via the existing package engine; they may themselves introduce new missing
   meanings. Scan only these new or materially changed formulations and
   affected ambiguous references. Do **not** start unrelated breadth research.
4. Update all incoming occurrences of a resolved missing candidate via a
   reverse dependency index, and propagate changed closure/open status
   upstream. Recheck candidate matching when new contextual meanings become
   available; re-open only genuinely affected nodes.
5. Iterate until Open empties, or all remaining Open nodes have explicit
   documented blockers/dispositions. If desirable, run a fresh full scan
   with cleared ephemeral visitation state to catch omissions; the persistent
   missing registry continues to deduplicate references.

**Performance improvement over literal rescanning:** Store a
source/formulation-version hash, detected reference occurrences, resolved
meaning IDs, ambiguity/missing-candidate IDs, outgoing edges, incoming
(reverse) edges, and an explicit invalidation key. A formulation with
unchanged content should normally be **scanned once**, not anew on every
iteration. A corrected formulation invalidates only itself and affected
upstream/downstream matches. Batch/commit changes should be replay-safe.
A worklist/DFS and graph closure propagation can be generic; parsing and
context matching belong to the mathDef adapter.

Do not use an unbounded recursive expedition to the most foundational
vocabulary: distinguish defined dependencies from mathematical primitives,
accepted conventions and deliberately out-of-scope references, using
**explicitly justified** dispositions rather than silently declaring them
resolved.

## 5. Deliberate breadth expansion only after stabilization

An empty Open list means **dependency closure relative to the references
actually detected**, not exhaustive coverage of mathematics. Once the
current collection has stabilized, separately explore broad authoritative
sources for new terms, contexts, variants and mathematical areas. Add them
to the independent population and send them through the exact same
incremental missing-meaning/linking process. Repeating breadth expansion
and dependency stabilization in **rounds** is desirable; indefinite
concurrent unrelated topic growth while trying to complete the present
network is not.

A source may legitimately offer alternative equivalent formulations or
context-specific variants. The graph must distinguish these, and must not
merge homonymous concepts ('closure' in topology versus field theory).
Context-specific term matching is an assisted mathematical judgment,
not just string matching.

## 6. Mathematical checking versus completion

During the fast dependency-driven phase:
- Make context-sensitive mathematical judgments and source-backed
  descriptions for **new** definitions and references.
- Record where a candidate reference occurs, what it means here,
  provenance/rationale, and whether the target was existing/missing/ambiguous.
- Avoid knowingly wrong links or reproduced source errors. Flag source
  defects, conflicts, unsupported conventions and possible definitional
  cycles without continually re-auditing unrelated historical definitions.
- **Do not demand the user's manual verification or final comprehensive
  citation review** in order to mark a formulation as automatically linked
  or a dependency component structurally closed.

After network/coverage stabilization, run a separate heavier review of
sources, correctness, variants, unresolved/ambiguous matches, redundant
definitions, genuinely circular definitions, link consistency and rendering.
No provisional formulation becomes authoritative merely by achieving closure.
Keep eventual human verification as a distinct status and capability.

## 7. Engineering constraints and implementation plan

Build on, rather than discard, existing generic:
- `research_pipeline/engine/population.py` append-only, provisional
  source/term/observation/meaning/relation/review/issue intake.
- `research_pipeline/engine/population_queue.py` backlog planner.
- `research_pipeline/adapters/mathdef/` for mathematical scope policy.
- Consolidated GitHub Actions processing and existing independent
  reconciliation/promotion mechanisms.

Suggested small, reusable additions (final names flexible):
- A durable per-formulation scanner cache and reference occurrence ledger.
- A shared missing-contextual-meaning candidate registry with aliases,
  lightweight disambiguation and many incoming occurrences.
- Forward/reverse graph indices with DFS/worklist incremental closure
  propagation, including safe cycle handling.
- A scheduler that replaces unrelated breadth-first selection with missing
  dependency research until stabilized.
- Deterministic tests and checkpoint/status summaries.

The **generic engine** should not hard-code mathematical vocabulary; retain
the ability to adapt the machinery later to mathematical theorems or
mathematics-education concepts via adapters.

Start with a **read-only inventory and graph pilot** against the current
independent reconstruction, including recent provisional batches. Do not
rewrite or reseal earlier reviewed records, auto-promote drafts, overwrite
Wave 1, alter public mathDef, or consult original production mathDef.
Measure candidate match ambiguity, duplicate avoidance, open/closed trends,
missed references and incremental rescan counts. Then add verified
append-only write modes and test multi-batch interruption/recovery.

Minimal acceptance scenarios:
1. A→B→C→A links all edges with finite traversal; all are structurally
   closed if all contextual meanings exist, while possible definitional
   circularity remains separately auditable.
2. A→B→missing C leaves A/B Open even though encountered/completed; when C
   is added, only C and affected dependencies are processed, and closure
   propagates correctly.
3. Two formulations reference the *same* missing contextual meaning:
   exactly one candidate record and two occurrence records; the second
   incurs no duplicate source research.
4. Two homonymous references have different contexts: separate targets or
   flagged ambiguity, never a confidently invented link.
5. Adding C creates missing D; dependency population expands, but unrelated
   broad source research stays paused.
6. A material formulation revision invalidates only appropriate cached
   scans and dependencies; a replay does not duplicate links, missing
   candidates or accepted revisions.
7. Automated closed status does **not** turn candidate mathematical
   screening into certification or human verification.

## 8. **NEW EXPLICIT REQUIREMENT: durable repository dependency map and crash-safe replay**

**Added after user clarification, 2026-10-21. This is required for the
implementation, not an optional optimization.** During graph discovery,
write the results to *real machine-readable files committed in the
independent repository workspace*, updating durable state continuously in
small, restartable units. If a Chat response times out or a GitHub workflow
is interrupted, a new Chat should be able to read this graph and resume
without re-parsing or re-researching any already completed work.

### 8.1 Precompute / persist the initial structure before expensive research

As the FIRST structural pass, enumerate **every contextual meaning and every
individual formulation/variant**, including the already screened independent
Wave 2 catalog and recent provisional population batches. Build a durable
inventory, then extract potential references from those formulations. Record:

- formulation and owning meaning IDs, source and **source-content hashes**;
- every detected mathematical reference occurrence and exact context/phrase;
- the best matching **existing contextual meaning** when known, the shared
  *already identified* missing-meaning candidate when it exists, or an
  unresolved/ambiguous reference;
- existing versus missing status (and a separate ambiguous/external state);
- outgoing and reverse incoming relationships;
- whether the formulation has actually completed its *content scan*,
  whether its traversal is completed, and whether it is structurally
  Open or Closed; and
- the last durable checkpoint/scan version that justifies those statuses.

**Very important:** Merely enumerating a formulation or importing an
already-reviewed link does NOT prove we have identified *every* mathematical
reference in that formulation. Initialize it as `unscanned` or
`scan_incomplete` until its content has been fully examined and its complete
outgoing reference set has been durably recorded. Do not invent links or
mark the node complete from the absence of extracted references.

The user's proposed representation can be understood as **one rooted
recursive dependency tree for every formulation**, even where the trees
repeat shared descendants. Such views are useful, but storing each expanded
tree verbatim would duplicate most of the graph and could explode in size
or grow forever along A→B→C→A. Store each formulation and its **immediate
children once** in a normalized directed graph; then construct any
per-root nested tree view by recursively reading the saved adjacency index.
During a tree rendering, stop descending when a node already occurs on
the *current path*, but still display the edge that closes the cycle.
Missing nodes terminate their tree branch and keep their shared candidate
identity. This is semantically equivalent to the user's redundant-root
nested reference trees, without costly redundant storage.

For example, a cached record for A referencing existing B and missing C
can be as small as:

```json
{
  "formulation_id": "form.A",
  "version_sha256": "sha256-of-source-formulation-and-context",
  "scan_status": "complete",
  "references": [
    {
      "occurrence_id": "form.A:ref.1",
      "phrase": "B",
      "state": "existing",
      "target_meaning_id": "meaning.B"
    },
    {
      "occurrence_id": "form.A:ref.2",
      "phrase": "C",
      "state": "missing",
      "missing_candidate_id": "missing.C"
    }
  ],
  "structural_status": "open"
}
```

(The SHA string and identifiers above are **illustrative**; no graph scan
has yet been performed, and no record above is claimed to exist.)

### 8.2 Proposed on-repository files

Keep the real derived structure in an isolated workspace directory such as:

```
research_pipeline/experiments/reconstruction-v2-independent/
  dependency_graph/
    INVENTORY.json              # explicit scan universe + source version
    nodes/                      # keyed per-formulation, full reference snapshot
    missing_candidates.jsonl    # stable deduplicated contextual candidates
    occurrences.jsonl           # all appearances of candidate references
    edges.jsonl                 # resolved/provisional links, origin -> meaning
    reverse_index.json          # origin nodes for each target/candidate
    STATE.json                  # open/closed and processed status, counts
    CHECKPOINT.json             # latest fully committed successful scan unit
```

These are suggested filenames, not a requirement to use monolithic giant
JSON files. Prefer small per-formulation records and indexes that can be
reconstructed from the authoritative records. The format should remain
domain-agnostic in the core engine and mathematics-specific only in its
adapter. Graph files must not rewrite previously screened definition data.

### 8.3 Safe interruption, restart and incremental updates

1. A scan unit may be a single formulation or a *small bounded batch* of
   formulations, but all saved results and status transitions must be
   **idempotent, version-bound and recoverable**. Once a formulation's full
   reference set is assembled, persist it atomically *before* marking its
   scan complete. Never mark a node complete merely because scanning started.
2. **Commit successful bounded updates to GitHub.** Only committed content
   survives a fresh chat or disposable GitHub Actions runner. Uncommitted
   local data or an in-memory DFS stack is NOT a recovery mechanism. At a
   timeout, the latest committed checkpoint defines what was actually done.
3. A failed partial scan is either ignored or replayed against the same
   version hash; it can never leave an apparently completed record with
   missing children. Use atomic staging/manifest-last commits or an
   equivalent validated transaction protocol. Deterministic IDs and
   duplicate-safe upserts prevent multiplying occurrences and candidate
   records on replay.
4. On restart, load the existing graph from GitHub, verify content hashes
   for changed formulations, and begin with **unscanned, interrupted or
   invalidated units**. Do NOT reparse already persisted unchanged forms.
   The DFS encountered/completed sets may safely reset because the durable
   adjacency and scan statuses survive. No need to remember where a Chat
   response was interrupted; its unfinished units are still queued.
5. As missing candidate C is researched and admitted, update C's graph
   node and the references pointing to that **stable missing candidate
   ID**, propagate closure through the reverse dependency index, and
   scan the newly added definition(s). Do not rebuild every root's nested
   tree or redo unrelated lexical scans.
6. If a formulation changes, detect the hash mismatch, mark affected
   cached results stale, and rescan that formulation and necessary impacted
   references; never silently retain outdated links as certified closure.
7. Maintain explicit durable counts of inventory nodes, scanned/complete
   nodes, Open/Closed nodes, missing/ambiguous candidates and unresolved
   occurrences. The snapshot must distinguish **known scanned work** from
   inventory awaiting scanning.

**Efficiency trade-off:** Committing every single term immediately is safe
but may incur substantial GitHub overhead. A small bounded group of
completed independent scan units per verified GitHub commit is also safe:
at worst the uncommitted tail is repeated, and no unfinished node is falsely
completed. Use the smallest practical commit cadence consistent with the
short Chat response/Action timeout window. This is the only sense in which
we should deviate from 'update the structure as you go through each term.'

### 8.4 Required interruption/restart tests

- Stop after writing part of a node's children: restart must consider that
  node unscanned/uncompleted, not falsely Closed.
- Stop after persisting adjacency but before writing a complete marker:
  restart must finalize or replay safely, not duplicate occurrences.
- Commit A and B, interrupt before C: resume from C without rescanning A/B;
  A/B retain references to shared missing candidates.
- Materialize A→B→C→A from the adjacency graph as a finite per-root nested
  view, while retaining C→A in the actual saved links.
- Admit a missing meaning that resolves references from multiple already
  scanned definitions: update their status through reverse dependencies,
  without rescanning unaffected formulations.
- Restore from a clean Git checkout in a new process without requiring any
  transient local workspace, hidden chat state or manual recovery notes.

The first engineering milestone should therefore be a **committed,
recoverable initial inventory + graph snapshot** (with explicit `unscanned`
statuses where semantic scans remain pending). Only after that should
we spend substantial time researching the deduplicated missing-meaning
queue or expand unrelated mathematical breadth.

## 9. Decision and next action (as of this note)

- **Agreed:** dependency-first, stable-inventory-first construction with
  expected dependency-driven growth, *then* deliberate breadth expansion.
- **Agreed:** encountered = scanned; completed = finished link traversal;
  Open/implicitly Closed reflect transitive unresolved dependencies.
- **Agreed:** consult BOTH the existing contextual meanings and the shared
  Missing Meanings registry **before** any expensive missing-meaning research.
- **Agreed:** link cycles without recursing endlessly; handle mathematical
  circularity in later audit.
- **Agreed:** closure is automated assistant work, not user sign-off.
- **Recommended engineering refinement:** permanent hash-bound scan cache,
  reverse dependency index, incremental worklist instead of full rescans.
- **Not yet implemented:** new scanner/graph/scheduler; pending planned
  unrelated-breadth Batch143 should be held while this workflow is
  implemented and piloted.

For prior research state, consult `research_pipeline/adapters/mathdef/resume_plan.json`
and the latest independent population `STATUS.json`/`QUEUE.json`; those
legacy breadth-oriented checkpoints describe the completed B139–B142 work
but **do not override this newer design decision**.


## 10. LATER CLARIFICATION — First complete the original graph, then interpret and research missing meanings

**Agreement added 2026-10-21 after the original design and its §8 recovery
specification.** For the FIRST bulk pass, minimize external mathematical
research and changes to the definition corpus. It is preferable to finish
identifying references within the existing population *before* researching
missing meanings, even where discovering and linking references takes
substantial contextual mathematical judgment.

The required ordering is now:

1. **Source-free content scan and existing-meaning linking:** For all currently
   known formulation variants, read/scan their contents, reuse existing
   meanings where justified, and save a versioned **occurrence** when an
   apparent mathematical reference has no clear existing contextual target.
   An occurrence need not yet assert the identity of a distinct missing
   meaning. Capture its wording, context and origin; don't research outside
   sources or add definitions during this pass. Store source-free lexical
   hints only as proposals, never claim them exhaustive.
2. **Global missing-occurrence consolidation:** Once all original formulations
   have complete semantic scans, compare every unresolved occurrence across
   the entire existing corpus. Determine which can match existing meanings,
   which are homonyms, which are likely references to the same missing
   contextual meaning, and which are external/primitive or deferred. First
   do this without research where possible. The user's idea is to research
   any *needed contextual interpretation* once and compare it against all
   likely occurrences, rather than spend effort on each instance while
   scanning. Keep original occurrences even when grouped or classified.
   This phase is NOT yet the new-definition-population phase.
3. **Source-backed missing-definition research and admission:** Only once
   the missing-occurrence pool has been considered globally and the first
   pass is explicitly marked consolidated, research and admit missing
   meanings/variants through the existing independent provisional
   population system. Then scan only new/changed formulations and repeat
   the above procedure for the expanded dependency network.
4. **Unrelated breadth expansion:** Only after dependency-driven
   stabilization, search new unrelated areas; integrate discoveries using
   the same passes. Manual certification is still much later.

For efficiency and interruption recovery, keep a distinct
`unresolved_occurrences.jsonl` independent of the deduplicated
`missing_candidates.jsonl`. An `unassigned` occurrence is a valid record
that does not yet presuppose a separate missing mathematical meaning; an
explicitly reviewed candidate is a later interpretation of such evidence.
The phase gate is bound to exact inventory and unresolved-pool fingerprints
so a stale prior pass cannot authorize new research after content changes.

The **current executable handbook** is
`research_pipeline/DEPENDENCY_FIRST_WORKFLOW.md`. Its first section states
the concrete commands and the current phase's prohibitions. Future chats
should use that executable handbook along with the durable graph
`STATE.json`, `CHECKPOINT.json` and exact worklists.
