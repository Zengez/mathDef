# Proposal: publish-first Wave 2 milestone and bounded audit-wave releases

**Date:** 2026-10-26  
**Status:** owner-requested direction, implementation proposal; documentation only. **Not a publication, phase-gate transition, source certification, or approval of individual mathematical changes.**  
**Scope:** Zengez/mathDef independent reconstruction and future incremental updates.

## Complementary efficiency improvement: opportunistic provisional completion

Keep the dependency-first screening sequence, but when contextual/identity review has already established most of a trustworthy definition or other final content item, finish and save it as a **provisional, origin-linked comparison anchor** instead of making later research repeat the same work. Compare future candidates against both accepted and provisional meanings, with trust tiers and no automatic equivalence. The trigger, phase restrictions, reusable record requirements and clustering safeguards are documented in [OPPORTUNISTIC_PROVISIONAL_COMPLETION_PROPOSAL.md](OPPORTUNISTIC_PROVISIONAL_COMPLETION_PROPOSAL.md). This remains a proposal and **does not authorize new source research during the currently closed source-free Phase 2**.

## New objective and stop rule

Deliver a searchable **production** mathDef update containing the mathematically eligible additions of the current independent Wave 2 collection and a **single first-generation, bounded research pass** over the currently unresolved missing-candidate pool. Do this **before** recursive research into dependencies newly discovered inside those additions.

Do not equate the 418 presently unresolved canonical candidate identities with 418 publishable terms. A candidate may be a genuine separate meaning, an already represented contextual variant, a justified primitive or non-definitional phrase, a duplicate, or an unsupported/deferred item. Each first-generation candidate receives one bounded classification/research attempt and an explicit disposition. Publishing a useful subset does not require converting every unsupported candidate into a fabricated definition.

**Nonrecursive research boundary:** only the fixed, version-pinned input queue is *required* for this release. Record newly exposed second-generation unknowns in a future intake queue with exact occurrence, context, provenance, candidate parent and source/target anchor. Do **not** recursively research them, expand the release's required scope, or mark them as complete. Existing genuine links may be connected when mathematically justified; no invented target or broken website link.

The original 659 Wave 2 formulations have all been initially scanned; this does not certify their mathematical correctness. Current independent STATE is still in `consolidate_occurrences` with Pass 2 consolidation gate closed. Preserve its existing gate and receipt integrity. Complete bounded material Pass 2 correctness/identity disposition and explicitly review/authorize a transition before performing the first-generation research pass. Repeated low-yield synonym rechecks should not indefinitely block that reviewed transition.

## Milestone A: first publishable combined corpus

1. **Stabilize source-free consolidation.** Address critical wrong mathematical targets, material convention/hypothesis inconsistencies, inappropriate self-links and cross-context mismatches; use existing exact version/occurrence checks and the optional reviewer-context overlay. Track cases needing later source verification as scoped deferrals. Never treat 19/19 mechanical readiness as mathematical certification.
2. **Version-pin the first-generation candidate queue.** Capture the actual unresolved candidate identities, occurrences, alias histories, source versions, review dispositions, and immutable baseline digest. The historical count (418) is a checkpoint, not a quota or a fresh scan of newly added formulations.
3. **One bounded research pass.** For genuine candidates, consult admissible sources, write original mathematical paraphrases and retain exact provenance. Distinguish contextual meanings, variant formulations, synonyms, and duplicate labels. Check each proposed definition's own correctness and essential conditions but do not chase new missing dependencies. Admit source-screened additions into independent records through reviewed mechanisms; keep unsupported items deferred.
4. **Release-level quality checks (mandatory).** Validate stable identities; clearly typed mathematical meaning and hypotheses (including degenerate object cases); trusted source/locator and permitted paraphrase; no known substantive mathematical falsehood; no unjustified equivalence/alias; no dangling production link; presentable KaTeX/LaTeX; accessible/searchable term name and definition; compatibility with current production site and export feed. Fail/punt an individually defective entry without blocking otherwise eligible entries. Retain the owner's **applied** empty/zero/trivial-qualification ledger with evidence for later review; proposals are never claimed applied.
5. **Create an independent release-candidate freeze** recording which entries were screened, which remained provisional/held, explicit incomplete dependencies and external-review limits, content hashes, reproducible preview and tests. This is a deliberately **bounded** release freeze, NOT a declaration that the entire mathematical dependency graph is closed or recursively audited. Existing full-freeze/promotion checks may need a reviewed new eligibility mode; never bypass or silently weaken them.
6. **Only after the independent snapshot is frozen**, compare it with the original production corpus. Produce a per-identity disposition: new searchable term; genuinely distinct contextual meaning under an existing term; equivalent variant; correct existing definition unchanged; scoped correction; deferred/held. Preserve production IDs, sources, valid formulations, curated link overrides and feedback routes. Do not replace original content merely because the independent wording differs.
7. **Implement and test the production reconciliation/export bridge.** The independent term -> meaning -> formulation schema is not identical to production `definitions/*.tex` and `variants/`. Conversion must be deterministic, diffable, merge-safe and capable of preserving multiple contexts and sources. A staging comparison should show exact add/update/no-op/held counts and content diffs. Production site `scripts/build_index.py`, Pages build, public definition v1 snapshot, search, inline/nested links, source modal and feedback must remain working. Require an explicit reviewed release manifest and deployment go/no-go.
8. **Publish a single reviewed production update** via the existing GitHub Pages path. Verify the deployed site/search/export and preserve a rollback tag or known-good commit plus immutable manifest. A public draft label / "not yet manually verified" marking must not be misrepresented as peer review.

Unresolved second-generation dependencies are **not publication blockers** by themselves. Missing targets should stay plain/unlinked or explicitly pending rather than generate dead or wrong links. Any evident mathematical error, provenance defect, duplicate collision, broken search/index or rendering failure **is** a release blocker for the affected record.

## Milestone B: recurring bounded audit-wave / update releases

Use a reusable batch contract for **N = 1, 418, or any number** of new/modified contextual meanings. Each release/audit wave is anchored to the **diff since the preceding production release**, not to a forced rescanning of the entire database.

Suggested stages:

1. **Capture** a deterministic manifest of added/changed terms, meanings, formulations, aliases, citations, and links, plus current full-site baseline SHA and provenance. Include user suggestions and previously deferred candidates only when explicitly selected for the batch.
2. **Audit the bounded batch**, checking mathematical correctness, domain/context hypotheses and empty/zero/trivial exceptions, source/variant support, equivalence, incoming/outgoing existing links, potential local cycles, citation accuracy and presentation. Any newly discovered missing prerequisites enter the **next wave's candidate backlog** by default; no unbounded recursive investigation.
3. **Prepare version-guarded patch transactions** (add new meaning, append variant, correct/retire formulation, fix link, update source, explain nonmerge), with source/target IDs, predecessor digests, reason and review evidence. Retain old history. Revalidate changed existing terms affected by inbound links without indiscriminately re-auditing the whole corpus.
4. **Run staging gates**, including mathematical review of edited claims; schema/rights/provenance; exact no-unintended-change hashes; link integrity and cycles; site search and renderer/browser smoke; public JSON export compatibility; rollback/recovery preflight.
5. **Publish and record** a dated, immutable release identifier; a machine-readable changeset, Markdown changelog, and a short README **Latest Update** summary linking to the full notes. Report exact counts of **new searchable headings**, new contextual meanings, new variants, existing-term corrections, link changes, deferrals and known open problems. A batch of one is a valid release.
6. **Follow up** via a separate optional audit wave on the now-published batch; its fixes become the next reviewed patch rather than requiring immediate removal of the batch. Re-running an audit should be incremental/idempotent, with stable IDs and preserved history.

A wave may precede a release (normal process for new incoming batches), or examine the previously released batch more deeply (the intended first follow-up). Do not assert that an audit wave is a formal peer review, complete mathematical coverage, or proof that no further dependency exists.

## Release notes sketch

- `CHANGELOG.md`: one dated section per production release.
- `data/releases/<release-id>.json` (proposed, not yet implemented): immutable machine manifest with baseline/head hashes, independent-source freeze ID, per-meaning and per-formulation dispositions, changed paths, test evidence, known limitations and review status.
- `README.md`: concise Latest Update with release ID, number of new searchable terms / added variants / corrections and link to `CHANGELOG.md`.
- Existing source and change evidence remain in append-only research records, not replaced by human-readable summaries.

## Integration safety and engineering design choices still to implement

- Current `AGENTS.md` and source-free dependency-first execution contract intentionally isolate the independent reconstruction. The owner has **changed the milestone priority**, but this document alone does not override their file-access and application controls. Carefully revise the contract, allow first-generation work only after reviewed Pass 2 transition, and expressly authorize original-corpus comparison **only after a documented bounded independent freeze**.
- The existing provisional-population promotion adapter promotes into independent Wave 2 **only**; it does not publish production definitions. A production migration/reconciliation bridge remains to be engineered.
- The original production website already builds a term-and-definition search index and GitHub Pages read-only export from production `definitions/` and `variants/`; avoid replacing that interface or silently mixing preview records with production feeds.
- Keep previously reported PRs #13, #14 and #15 as separate draft engineering/evidence work until reviewed; do not silently merge them into main as a side effect of this plan.
- Initially support a non-destructive preview/staging run. Test with a synthetic tiny batch and a 1-entry real candidate before generating a large production patch. Do not deploy any production change merely because preview, test suite or artifact generation passes.
- Decide any new schema, audit-wave CLI/manifest, delta computation or adapter behavior in reusable engine code with mathDef-specific policy kept in an adapter. Preserve history and make reruns idempotent.

## Next bounded engineering action

Implement an isolated, **read-only release readiness and staging-diff prototype** that consumes a frozen independent snapshot and reports new/variant/collision/deferred dispositions **without writing production data**. Plan the necessary explicit waiver/eligibility mode for a nonrecursive but mathematically safe release, with tests. Do not actually compare against production before the bounded freeze; exercise against synthetic fixtures until then.

This proposal records the owner's desire to **publish first and audit recursively later**. It intentionally does not claim the first release is ready now, and does not initiate a release, open Pass 2 gate, or apply mathematical graph transactions.
