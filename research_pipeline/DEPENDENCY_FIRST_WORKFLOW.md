# Dependency-first Wave 2: operating protocol

> **2026-10-23 independent Wave2 audit addition:** The global read-only scanner also emits a `groupoid_size_scope` review lead when a current **effective** dependency maps a groupoid to the only existing **small-groupoid** meaning, while the source does not state smallness or explicitly use the `Groupoids` category of small groupoids. Three current formulation/reference pairs triggered this extra check (setoid category, strict (2,1)-category, and category fibred in groupoids). They require mathematical/size-context review, not automatic amendments. The scanner check was source-text/effective-ledger inspected but was **not** run through remote Python test execution here; no source definitions were changed. See `WAVE2_SOURCE_FREE_AUDIT_CONTINUATION_2026-10-23_PACKETS166_167.md`.

**Experimental only.** The authoritative design is TEMP_DEPENDENCY_FIRST_WAVE2_PLAN.md, especially section 8. Automated closure is not mathematical certification, manual approval, promotion, publication, or a Wave 2 freeze. Frozen independent Wave 1 and historically screened independent Wave 2 remain read-only; original production mathDef definitions are forbidden inputs.

## Start here after interruption

Read this file, TEMP_DEPENDENCY_FIRST_WAVE2_PLAN.md, then independent dependency_graph/CHECKPOINT.json, STATE.json and INVENTORY.json. Inspect the shared missing candidate registry and the research queue. Never reparse an unchanged, complete, version-valid node. Source population records and Batches 139–142 remain separate, unchanged inputs.

## CURRENT AUDIT ACCELERATOR — global review without redundant per-node retrieval (2026-10-23)

**The phase contract below is unchanged.** At 659/659 scanned and zero ambiguous/unassigned, do **not** restart Pass1 or prematurely open the consolidation gate. Finish the mathematical/contextual review and candidate-equivalence audit first. All inputs are the original independent Wave2 graph; no original-production corpus, frozen Wave1, breadth Batch143 or external missing-definition research is consulted.

The reusable tool is now **\`research_pipeline.engine.dependency_global_audit\`**. It loads the inventory and **all effective append-only amendments once**, so previous corrected references remain intact:

\`\`\`bash
W=research_pipeline/experiments/reconstruction-v2-independent
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" scan \
  --limit 80 --candidate-limit 50 > /tmp/wave2-global-audit.json

# Only when reviewing original full statements and every current reference:
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" scan \
  --snapshot-output /tmp/wave2-effective-snapshot.json \
  --limit 80 > /tmp/wave2-audit-headlines.json
\`\`\`

The \`scan\` command computes meaning-level strong components and self-links, validates scanned state, checks existing/missing target identities, flags selected **heuristic** mathematical scope risks (such as a generic category being restricted to the small-category meaning, or ideal/module generation confusions), and collects **possible**, same-context-domain candidate lexical similarities. The summary reports all detected flags and returns a bounded prioritized sample. \`--snapshot-output\` writes a complete, temporary **review-only** source + effective-node bundle for all 659 formulations; do not commit these redundant generated snapshots. Scope checks are *leads*, not mathematical judgments: a missing warning is not proof that a reference is correct. Contextual reviewers must also sample unflagged records and examine known flagged source/citation/variant issues in progress logs. Similar candidate names are **not** automatic aliases.

### Preparing approved edits efficiently

The new \`prepare\` mode accepts an **explicit reviewer-authored** JSON decision manifest. Obtain \`expected_node_sha256\`, \`expected_occurrence_id\`, \`reference_index\`, \`formulation_id\`, version and full original mathematical context from the global snapshot or targeted review bundle:

\`\`\`json
{
  "schema_version": 1,
  "id": "reviewed-contextual-109",
  "inventory_sha256": "COPY_CURRENT_INVENTORY_SHA256",
  "unresolved_fingerprint": "COPY_CURRENT_STATE_UNRESOLVED_FINGERPRINT",
  "reviewed_by": "assistant-contextual-mathematics-reviewer",
  "review_rationale": "Explain the original full source and every surrounding dependency considered; the replacement has been mathematically checked.",
  "changes": [
    {
      "formulation_id": "COPY_EXISTING_FORMULATION_ID",
      "expected_node_sha256": "COPY_EFFECTIVE_NODE_SHA256",
      "reference_index": 0,
      "expected_occurrence_id": "COPY_OCCURRENCE_ID",
      "reason": "Explain in substantive mathematical detail why this precise target is wrong and the proposed replacement is correct.",
      "replacement": {
        "phrase": "ACTUALLY_REVIEWED_REFERENCE",
        "state": "existing",
        "target_meaning_id": "COPY_VERIFIED_EXISTING_MEANING_ID"
      }
    }
  ]
}
\`\`\`

\`\`\`bash
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" prepare \
  --manifest /tmp/reviewed-decisions.json \
  --output-dir /tmp/reviewed-wave2-packets --max-per-batch 5
\`\`\`

The preparer rejects stale inventory/graph fingerprints, changed effective predecessor node hashes, altered occurrence identities, duplicate edits, unknown targets, no-op corrections and **unreviewed new missing-candidate identities**. It bundles all decisions for one formulation into one **complete** replacement snapshot, retains all other references, and splits into independent packets of **at most five complete formulations**. It runs the already-existing \`dependency_review_preflight\` on every generated packet. **All packages are offline**: generation/preflight neither publishes nor edits the graph. Only after examining each proposed complete packet may reviewers submit several nonoverlapping packets together in one commit to \`dependency_graph/inbox/\`, provided the GitHub Action's unapplied-inbox limit is respected; afterward verify exact applied receipt and the independent graph and isolated-test Actions for that commit. Recompute anchors if the graph changes in between. If a packet fails, stop and reconcile; never count mere creation or passing mechanical checks as mathematical correctness.

Prioritize by error impact and contextual recurrence (false target / unjustified hypotheses / source rigor); group related definitions as one mathematical review. Distinguish **global dependency consistency** from **mathematical/source verification** and track outstanding certification separately. Retain the existing explicit Pass2 consolidation-gate requirements; neither zero cycles nor zero classifier backlog is sufficient to enter missing-definition research.

---

## CURRENT EXECUTION CONTRACT — occurrence-first, no-external-research initial pass (2026-10-21)

**Read this section first in every fresh Chat.** This is the current
execution order, superseding older advice to research a missing dependency
immediately or continue unrelated Batch143. The temporary design document
records the original intent; this file describes the executable process.

The purpose of this phase is to maximize *deterministic reuse* of the 659
already inventoried definition formulations and 611 meanings **without
adding new meanings or looking up external sources yet**. The historical
screened/provisional mathematical contents remain unchanged. Phase completion
describes the assistant's own mathematical reference identification, not
the user's manual certification.

**Pass 1: Existing-definition scan and linking; external research = OFF.**

1. Load `dependency_graph/CHECKPOINT.json`, `STATE.json`,
   `INVENTORY.json`, `unresolved_occurrences.jsonl`,
   `missing_candidates.jsonl`, and any fully reviewed scan snapshots.
   The graph is authoritative *only for what it has actually scanned*.
   Historical links and lexical proposals are hints, not exhaustive scans.
2. Run from the repository root:
   ```bash
   W=research_pipeline/experiments/reconstruction-v2-independent
   python -m research_pipeline.engine.dependency_graph --workspace "$W" --mode inventory
   python -m research_pipeline.engine.dependency_graph --workspace "$W" --mode worklist --limit 8
   ```
   The worklist includes each source formulation's full text and context,
   old link seeds, hash and local lexical hints; it does **not** consult
   external sources. Pick a manageable batch. Existing `complete` scans
   must not be redone without an explicit append-only amendment.
3. Read the **entire mathematical content** of each selected formulation.
   Identify each mathematical term/reference, including significant unnamed
   constructions missed by exact lexical matching. For each occurrence:
   - `existing`: link to an appropriately contextualized existing meaning
     only when justified from our current independent collection.
   - `unassigned`: record exact wording and contextual clues if the
     referenced mathematical idea has no confidently identified existing
     target. **Do not decide it is a genuinely missing distinct meaning.**
     Unassigned occurrences remain in the global pool for Pass 2.
   - `ambiguous`: several plausible existing meanings, with explicit reason.
   - `external`: explicit justified primitive/out-of-scope disposition.
   - `missing`: may be used if a source-free existing-corpus check already
     establishes an independently meaningful, precise missing candidate,
     but `unassigned` is preferable to premature source research.
   - `deferred`: other precisely described classification blocker.
4. Before assigning a `missing` identity, check **both** existing
   contextual meanings and the *entire stored occurrence/missing-candidate
   pool*, to avoid redoing even lightweight contextual work. Similar
   surface words alone do not establish equivalence; do not merge homonyms.
5. Submit a version-bound `ingest` package at
   `dependency_graph/inbox/UNIQUE_ID.json`, with each item containing
   `formulation_id`, `version_sha256`, `complete: true`,
   `review_rationale` (at least 40 characters) and **all** references
   observed in the formulation. A full pass is required to mark complete.
   Example:
   ```json
   {
     "schema_version": 1, "id": "semantic-initial-002", "mode": "ingest",
     "items": [
       {
         "formulation_id": "form.example", "version_sha256": "REAL_HASH_FROM_WORKLIST",
         "complete": true,
         "review_rationale": "Read the entire mathematical definition and considered every substantive reference.",
         "references": [
           {"phrase": "existing notion", "state": "existing",
            "target_meaning_id": "meaning.actual-id"},
           {"phrase": "unclassified construction", "state": "unassigned",
            "context": "Actual domain, object types and surrounding mathematical use"}
         ]
       }
     ]
   }
   ```
   The illustrative IDs above are placeholders; use real ones from inventory.
6. Commit the batch to `main`; the independent dependency-graph GitHub
   Action reads the inbox automatically, validates it, updates actual node
   files, rebuilds indexes, and writes a receipt in `applied/` in a single
   committed transaction. Verify run SUCCESS and receipt before claiming
   completion. Continue until `scan_complete == total_formulations`.
   Resuming after interruption loads committed nodes, skips completed
   unchanged scans, and repeats only unfinished units.

**Pass 2: Global occurrence consolidation; external definition research =
still OFF by default.**

1. With full Pass 1 scans, inspect the **entire**
   `unresolved_occurrences.jsonl` or run this read-only deterministic
   surface grouping (it does **not** declare synonymy or contextual identity):
   ```bash
   python -m research_pipeline.engine.dependency_graph --workspace "$W" --mode consolidation_worklist --limit 20
   ```
   For context-rich review without repeatedly joining inventory/source/node files,
   use the **generic, read-only** review bundle (substrings are a navigation
   filter, *never* an equivalence judgment):
   ```bash
   python -m research_pipeline.engine.dependency_context_worklist \
     --workspace "$W" --contains "residue field" --limit 20
   ```
   It includes original full source formulations, neighboring reference
   dispositions, existing local meaning targets, and the **current effective
   full-node SHA256** after any append-only amendments. Each bundle entry also
   includes a *draft* full-reference template without occurrence IDs, so the
   reviewer can prepare a version-anchored amendment without manual registry
   joins. Only manual contextual analysis may classify those references.

   Review every group and its originating formulation,
   wording and contextual information. Compare candidate uses across the
   whole existing corpus. Deduplicate possible missing meanings *as a
   classification problem*, not as multiple fresh source investigations.
   **Triage distinction:** A previously unmatched mathematical phrase may
   be (a) an actual separately definable prerequisite, (b) a defining
   equation/axiom or piece of the very structure under review, or (c) a
   notation/quantifier convention. Only (a) automatically merits a missing
   definition candidate; after full contextual review, (b)/(c) may receive
   a well-explained `external` disposition. A known named concept such as
   a group identity or an inverse is not dismissed just because it appears
   inside another definition. Never bulk-reclassify by lexical patterns.
2. If an unassigned occurrence has a clear existing target, classify it by
   append-only `amend` of the effective complete scan; if a genuinely
   missing contextual candidate is justified from internal evidence,
   amend it to `missing` with precise context. If unrelated or primitive,
   use an `external` disposition. Ambiguities should be classified
   explicitly or marked `deferred` with a reason. Use reviewed `alias`
   events for **demonstrated** equivalent missing phrases; never
   mechanically merge vaguely similar mathematical words.
3. The persistent *original* occurrence remains in the original immutable
   scan or revision ledger. Amendments have reviewer attribution, full
   replacement adjacency, rationale, exact prior-node hash and version
   anchor. Every update rebuilds occurrence and reverse-dependency
   ledgers. No missing-definition content is added in this pass.
4. When the first-pass entire set is completely scanned and there are **zero
   unassigned and zero ambiguous** references left, use its exact current
   `INVENTORY.json.source_inventory_sha256` and
   `STATE.json.summary.unresolved_fingerprint` to create a reviewed
   `consolidate` inbox package:
   ```json
   {
     "schema_version": 1, "id": "consolidation-round-001",
     "mode": "consolidate",
     "gate": {
       "schema_version": 1,
       "inventory_sha256": "REAL_SHA_FROM_INVENTORY",
       "unresolved_fingerprint": "REAL_SHA_FROM_STATE",
       "reviewed_by": "assistant-contextual-reviewer",
       "rationale": "Substantive record of how the entire saved unresolved-occurrence pool was consolidated and checked for duplicate candidate identities."
     }
   }
   ```
   The graph Action records `CONSOLIDATION.json` only when the scan is
   complete and occurrence classifications are appropriately resolved.
   **Any later inventory/content/occurrence changes invalidate this gate.**
   `STATE.json.summary.phase` will become
   `research_missing_dependencies` only with a valid gate.

**Pass 3: Research and populate missing meanings; external sources = ON.**

Only after the valid Pass 2 gate, investigate consolidated
`missing_candidates.jsonl` in prioritized groups. For every candidate,
compare contextual variants and sources, add source-supported new meanings
through the existing *provisional* population JSON packages, then make an
explicit version-anchored `resolve` event mapping the stable candidate to
the correct contextual target. New content is automatically inventoried and
its new formulations are scheduled for Pass 1 scanning; repeat the three
passes for the expanded dependency set. Separate unrelated subject-breadth
exploration is reserved for later structural stabilization.

**Crucial boundary:** A green CI check confirms only mechanical integrity.
Neither completed linking nor `CONSOLIDATION.json` grants mathematical
source certification or human approval. Never consult original production
mathDef definitions before the independent freeze.

**Observable phase controls:**

- `STATE.json.summary.phase`: `scan_and_link_existing`,
  `consolidate_occurrences`, or `research_missing_dependencies`.
- `STATE.json.summary.unassigned_occurrences`: unclassified mathematical
  references without prematurely assigned missing-meaning identity.
- `unresolved_occurrences.jsonl`: durable evidence pool independent of
  missing-candidate identities.
- `research_queue(...).missing_research_permitted`: true only with valid
  consolidation gate. This scheduler does not conduct research itself.
- `--mode worklist`: read-only/no-network reproducible next scan input.
- `--mode consolidation_worklist`: read-only grouped occurrence analysis, no equivalence claims.
- `research_queue(...).candidate_preview_only`: unapproved unresolved missing candidates are visible but NOT research tasks before the gate.
- `population/QUEUE.json.unconsolidated_missing_candidate_previews`: same non-actionable status for the preexisting population planner.

**Generic implementation and consistency details:** The graph engine
stores adjacency once per formulation, generates per-root nested views
on demand, and maintains reverse dependency indexes. `encountered` means
**semantically content-scanned** (a lexical proposal does not count),
`completed` means its reachable *existing* formulation scans finished,
and `closed` additionally means no unresolved transitive blocker.
The first-pass source inventory remains 611 meanings and 659 formulations
at this documented baseline (639 screened + 20 provisional); six were
reviewed complete at the last checkpoint. New and corrected source
formulations require fresh hashes and scanning. The inbox handler
paginates *unapplied* records rather than starving beyond 20 earlier
receipts; candidate resolutions are pinned to formulation-content
versions, not just display-term metadata.

---

## Stored schema

Workspace: research_pipeline/experiments/reconstruction-v2-independent/dependency_graph/

- INVENTORY.json: independently screened and separately provisional contextual meanings and every individual formulation, context and source-content hashes. Existing relations are imported as seeds and do NOT prove exhaustive scanning.
- nodes/FORMULATION_ID.json: complete atomic per-formulation adjacency snapshots, version hash, individual occurrences and scan status.
- occurrences.jsonl, edges.jsonl: reproducible exact occurrence and edge ledger.
- unresolved_occurrences.jsonl: unassigned, ambiguous, deferred, and missing occurrences pooled independently of early meaning identity.
- CONSOLIDATION.json: explicitly reviewed, full-inventory and occurrence-fingerprint-bound phase gate.
- missing_candidates.jsonl: shared contextual missing candidates, with incoming dependent forms and occurrence counts.
- reverse_index.json: reverse dependents for meaning nodes and missing candidates.
- resolutions.jsonl: append-only, version-anchored editorial mappings to newly admitted or pre-existing meanings.
- candidate_aliases.jsonl: reviewed, append-only identity mappings of two observed missing phrases to one canonical contextual candidate; original occurrence IDs remain in immutable node records.
- amendments.jsonl: append-only corrected complete scan snapshots, preserving original source-node versions and reviewer rationale.
- applied/: digest-bound processing receipts for committed inbox packages.
- STATE.json and CHECKPOINT.json: derived Open/Closed and scan/completion states, hashes, counts, and restart instructions.
- inbox/: review-authored semantic scan and missing-candidate resolution inputs.

An unscanned formulation is not a completed scan even if it has screened pre-existing links. Algorithmically suggested lexical matches are explicitly scan_incomplete. Only a separate exhaustive contextual review can supply a complete scan snapshot. The review does not certify mathematical correctness.

## CLI

From repository root, where WORKSPACE means research_pipeline/experiments/reconstruction-v2-independent:

    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode inventory
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode propose --limit 40
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode worklist --limit 8
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode status
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode queue --limit 20
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode tree --root-formulation FORMULATION_ID
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode ingest --batch "$WORKSPACE/dependency_graph/inbox/SCAN.json"
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode resolve --batch "$WORKSPACE/dependency_graph/inbox/RESOLUTIONS.json"
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode amend --batch "$WORKSPACE/dependency_graph/inbox/AMENDMENTS.json"
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode alias --batch "$WORKSPACE/dependency_graph/inbox/ALIASES.json"
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode apply_inbox --limit 20
    python -m unittest research_pipeline.tests.test_dependency_graph -v

The independent dependency graph GitHub Action performs bounded pilot proposals on push to its own code/tests or workflow_dispatch, sharing the existing population write concurrency group. It retries branch push collisions by recomputing from fresh main. A GitHub commit of the full graph folder is the only durable checkpoint across Chats or runners.

## Semantic intake contracts

A committed scan JSON batch contains schema_version=1 and items. Each item supplies formulation_id, exact INVENTORY version_sha256, references array, complete flag, and for complete scans a substantive review_rationale (40+ chars). Each occurrence must have phrase and state of existing, missing, ambiguous, external or deferred. Existing needs exact target_meaning_id; missing needs context to stabilize a shared missing_candidate_id; ambiguous/deferred needs an explanatory reason; external needs a justified disposition. Optional span offsets are checked against original formulation text.

Resolution batches contain schema_version=1 and resolutions array. Each resolution needs missing_candidate_id, target_meaning_id, target_version_sha256 (digest of the target INVENTORY meaning descriptor), and substantial contextual review_rationale. Resolution never creates a new definition. Add source-supported new meanings through the existing provisional population ledger, then sync the inventory and resolve the stable candidate. All previously screened reviews remain untouched.

## Crash-safe operation and closure

A node snapshot is a single atomically written file containing the entire occurrence list, digest, and completion marker. A missing, truncated, corrupted, mismatched or older-version file does not count as scanned. Rebuild derives reverse indexes, missing candidates, Open status, and checkpoint from valid committed snapshots; replay never needs in-memory stacks.

A rooted tree is expanded from stored immediate edges with a current-path visited set; the closing edge of a cycle is still shown, but its subtree terminates. Closure uses reverse propagation of blockers to a fixed point. Existing closed cycles are mechanically allowed; truly circular mathematical definitions remain a later mathematical audit problem.

Research queue prioritizes shared missing dependencies after contextual scans are reviewed. New dependency-driven provisional research may enlarge the graph and create more missing dependencies. Unrelated broad topic Batch 143 remains suspended until structural stabilization. Do not silently reinterpret old population/QUEUE.json recommendations as current priorities.

## Reviewed scan batches and append-only corrections (implemented)

Committed graph inbox files must have schema_version=1, id matching the filename
stem, and mode set to ingest, amend, resolve, or alias. The graph GitHub Action first
syncs inventory, invokes apply_inbox (maximum 20 batches), then creates at most
75 additional provisional lexical proposals in the current pilot, configurable
through workflow_dispatch (maximum 100 per run). Each successfully processed batch
gets a versioned digest receipt under graph/applied/; the receipt and graph
changes are pushed together in one Git commit. Replay with changed input is
rejected. No batch confers mathematical certification or promotion.

For same-formulation-version semantic corrections use an amend batch, **never**
overwrite a completed scan node. Each amendments[] entry supplies:

- amendment_id, formulation_id, version_sha256;
- expected_node_sha256 = digest of the current effective entire node;
- full replacement references, complete boolean, review_rationale;
- reason of 40 or more characters, reviewed_by.

The original node remains unchanged; amendments.jsonl keeps complete,
version-bound replacement snapshots and review rationales. Replay walks these
events in order; a stale/broken chain marks the node unscanned, never Closed.
The full effective graph, reverse index and rooted tree views incorporate
corrected scans and reviewed missing-candidate resolutions. The tree
renderer follows the saved occurrences index, preserving cycle-closing edges.

The adapter's own source-code SHA-256 is the proposal_fingerprint. When mathDef
reference-matching changes, unchanged proposals awaiting semantic review can
be refreshed without touching complete semantic scans or the historically
screened independent mathematical registry. A unique literal match from a
different mathematical domain is now marked ambiguous instead of a
confident cross-domain link.

The existing population GitHub Action now resynchronizes the graph inventory
after admitting new provisional meanings. The generic population queue
consults the dependency graph and disables unrelated breadth recommendations
while the graph explicitly retains breadth_expansion=on_hold.

## Reviewed missing-candidate aliases (implemented)

A reviewed identity alias is not string similarity. It is an explicit
mathematical judgment that two *observed missing phrases in their stated
contexts* refer to the same needed meaning. Submit an inbox JSON package
with mode=alias and aliases[]. Each entry needs unique alias_id,
alias_candidate_id, canonical_candidate_id, reviewed_by, and a substantive
reason (40+ characters). Both candidate IDs must already be present in the
committed shared registry, and no cycles, conflicting identities or alias
chains are permitted.

The original source phrases and IDs remain in each formulation's immutable
scan node. Rebuilt occurrences, reverse dependencies, rooted trees and
research queues use the canonical candidate ID, while missing_candidates.jsonl
retains the former record as status=alias and records its canonical identity.
This prevents duplicate source research without erasing evidence. Aliases
are not automatically formed from similar labels or shared topic categories.

Real independent pilot: semantic-foundations-001.json reviewed six complete
algebraic formulation dependency scans and identified the same notion
(principal ideal generated by one element) under two distinct surface phrases.
semantic-principal-ideal-alias-001.json merged the *candidate research identity*
using the reviewed alias protocol, reducing unresolved candidates by one.
Neither batch changed a screened definition or certified mathematical truth.

## Explicit limitations (follow-up implementation)

Automatic lexical proposals remain non-exhaustive, and all proposal-only nodes
stay Open. The occurrence-first phase gate prevents an automatic recommendation to research or add missing definitions before complete source-free scanning and global consolidation. Existing 891 screened/candidate relation seeds are historical
prerequisite evidence, never a complete enumeration of mathematical vocabulary.
Exact normalized phrase+context missing-candidate deduplication is deliberately
conservative; synonymous queries, contextual homonyms and different
object-type conventions require individually reviewed aliases, not automatic
semantic merging. Reviewed missing-candidate
resolutions themselves are currently immutable; correction requires a separate
append-only supersession mechanism rather than editing the resolution ledger
in place. Automatic source investigation and **bulk exhaustive** semantic reference
review are not implemented (six manually reviewed complete scans were piloted), and no mathematical certification, production publication or
Wave2 freeze occurs.

Retain the temporary design note until outstanding requirements and pilot reviews are incorporated into durable machinery.


## Pass 2 review efficiency tools — 2026-10-22 (multi-filter / preflight)

Two portable, **read-only**, subject-neutral helper improvements were
introduced during the third-to-fourth Pass-2 consolidation transition.
They never assert that two phrases are equivalent and do not change the
semantic graph, original definitions or external research phase.

**One grouped review of several navigation substrings** (OR selection,
deduplicated full formulation loads). Original `--contains "residue field"`
usage and `build_review_bundle(..., contains="...")` remain compatible:

```bash
W=research_pipeline/experiments/reconstruction-v2-independent
python -m research_pipeline.engine.dependency_context_worklist \
  --workspace "$W" \
  --contains-any "ideal" --contains-any "polynomial" \
  --contains-any "quotient" --limit 30
```

The multiple filter arguments are a reviewer navigation aid, not semantic
grouping or missing-candidate aliases. New regression tests verify OR
matching, unique formulation context bundles, backwards compatibility,
limit semantics and unchanged files.

**Validate a reviewed inbox package before committing it** using the
new module `research_pipeline.engine.dependency_review_preflight`:

```bash
python -m research_pipeline.engine.dependency_review_preflight \
  --workspace "$W" \
  --batch "$W/dependency_graph/inbox/REVIEWED_PACKAGE.json"
```

This preflight checks exact source inventory versions, the **effective**
complete-node SHA256 after all valid prior amendments, full replacement
adjacency validity, candidate identity preview, appended unique event IDs,
existing candidate identities, and alias chain/cycle conflicts. It does
not rewrite graph indexes, apply packages, infer contextual equivalence or
perform mathematical certification. It accepts reviewed `amend` and
`alias` packages; other package modes are intentionally not covered.
Committed `applied` receipts still determine actual completion. Preflight
must run on the *same* workspace snapshot to which the batch will be
submitted, and a concurrent edit can still invalidate the precondition;
revalidate against live repository state before commit.

CI regressions in
`research_pipeline/tests/test_dependency_context_worklist.py` and
`research_pipeline/tests/test_dependency_review_preflight.py`
cover source-load deduplication, read-only behavior, stale-node rejection,
alias cycle rejection, receipt replay and incorrect package naming.
Math-specific matching remains a deliberate reviewer responsibility.

**Reviewer lesson:** A single raw phrase can conjoin multiple distinct
mathematical operations (for example `R/I^n` contains both quotient-ring
formation and an ideal power), while a defining equality such as
`I∩J=IJ` is a predicate and not itself an independent prerequisite.
Full reviewed append-only amendments may separate those references,
retaining the original historical occurrence evidence. Do not collapse
`I^n` and `I^n M`, ordinary vs symbolic prime-ideal powers, or ordinary
comma vs iso-comma category constructions.



## Pass 2 bounded transaction sizing and preflight lesson (2026-10-22 Chunk 5)

A recent repository-connector attempt to fetch **eleven distinct effective
nodes together with the large amendment registry and inventory** timed out.
No immutable inbox package was created during the failed attempt; the live
graph and applied receipts were checked before reattempting. Splitting the
source-reviewed work into **roughly 3–5 formulations per graph inbox package**
allowed every subsequent package to apply with passing graph and isolated
test CI. This is an empirical connector reliability observation, **not**
permission to skip complete-formulation review or to discard context.

Recommended economical sequence for this experimental interface:

1. Fetch inventory and live unresolved registry once per topical review
   cluster. Select target phrases and inspect **full original source text**
   against existing independent meanings. Group only for *navigation*.
2. For a bounded batch of ~3–5 distinct formulations, fetch the original
   immutable node and the current append-only amendment events, reconstruct
   the **effective** node, and validate the full digest and source version.
   Reuse the same in-memory inventory/registry inside that batch.
3. Emit exactly one immutable full-adjacency reviewed `mode:amend` inbox
   package with context-specific rationale and preserved other references.
   If any connector request times out or reports an uncertain result, **check
   whether that exact path exists** before retrying; do not duplicate it.
4. Confirm the independent graph Action and `applied/<batch>.json` receipt,
   inspect the live `STATE.json` change, then collect all genuinely equivalent
   fresh raw missing candidate IDs and review them **separately** in a short
   `mode:alias` packet. A phrase-context hash intentionally creates more
   candidate IDs than semantic concepts.
5. Make small checkpoints after multiple successful batches. A passing
   Action proves mechanical validity, **not** mathematical correctness.
   Maintain manual review and a later whole-inventory consistency audit.

Preserve direction and type: finite generated ideals (over commutative
rings) reuse the existing finite generated **module** notion because the
ideal is a submodule of the regular module; an irreducible polynomial over
a field reuses irreducible **element** in the integral domain `k[x]`.
These are explicitly reviewed specialization links, not keyword matches.
Distinct concepts such as monic polynomials, simple versus multiple roots,
and additional map structure are not collapsed. For preimages, an
inverse-image **set** does not imply that a map has an inverse function.


## Accelerated audit v2 — source-free workflow (2026-10-23)

The following improvements have been implemented and tested. They do not alter the phase gate, mathematical sources, or the certification standard.

1. **Complete graph:** `dependency_global_audit scan` checks cycles across BOTH the original inventory seed edges and the latest effective scan edges. The prioritized queue uses severity, target fan-in and recurrence.
2. **Mathematical candidate notation:** lexical candidate suggestions preserve arrow order/direction and operators, marking mismatched notation as a conflict and lowering their priority. Surface similarity NEVER authorizes automatic aliases.
3. **Remember reviewed exceptions:** an optional `dependency_graph/audit_review_decisions.jsonl` records reviewed heuristic leads, with code, formulation ID, original version SHA256, effective node SHA256, occurrence ID (or null), reviewer, substantive rationale (40+ characters) and disposition `accepted_as_correct` or `needs_further_review`. These five identifying fields must match a current warning exactly. Structural/high-severity alerts cannot be suppressed; stale accepted reviews automatically return to the queue.
4. **Smaller reviewed edits:** explicit manifest changes may supply `updates` plus `remove_fields` instead of `replacement`, with an occurrence ID and effective predecessor SHA. Unchanged metadata is preserved and novel missing-candidate identities are rejected.
5. **Explicit safe staging:** `dependency_review_submit` checks EVERY packet and overlapping formulation before writing. Default is read-only. `--approved` stages reviewed packets into the isolated inbox; `--approved --commit` makes ONE local Git commit with only those files. No push or certification is automatic.
6. **One graph rebuild per amendment group:** contiguous amendment packets are validated together, applied with one ledger update and one derived-index rebuild, and retain individual immutable receipts. A stale event aborts the entire group before any ledger mutation.

Commands from a repository checkout:

```bash
W=research_pipeline/experiments/reconstruction-v2-independent
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" scan --limit 80 --candidate-limit 80 --snapshot-output /tmp/wave2-full-review.json
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" prepare --manifest /tmp/reviewed-decisions.json --output-dir /tmp/reviewed-packets --max-per-batch 5
python -m research_pipeline.engine.dependency_review_submit --workspace "$W" --packet-dir /tmp/reviewed-packets
# Only after explicit human/assistant contextual mathematical review:
python -m research_pipeline.engine.dependency_review_submit --workspace "$W" --packet-dir /tmp/reviewed-packets --approved --commit
```

The final command creates a local commit, never pushes. For connector-based GitHub work, commit the SAME mathematically reviewed packets atomically and verify every applied receipt and both CI workflows. The consolidation gate remains FALSE until the full mathematical/contextual/citation/alias review is complete.

---
