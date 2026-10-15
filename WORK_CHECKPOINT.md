# mathDef working checkpoint — 2026-10-15

## Purpose
Durable handoff/checkpoint for interrupted or timed-out mathDef research sessions. Always read this file and the live repository tree before resuming. Commit every bounded batch separately. Never describe an uncommitted batch as completed.

## Verified starting point
- Repository: https://github.com/Zengez/mathDef
- Site: https://zengez.github.io/mathDef/
- Last observed repository: **879 .tex definitions in 39 subject folders**. This is a snapshot, not a fixed target.
- Already present: Bergman space, Bergman kernel, weighted Bergman space and kernel, Bergman metric and projection, reproducing kernel Hilbert space; do not add duplicates.
- October coverage pass already added 91 entries (31 advanced function spaces; 41 several complex variables; 19 complex analysis).
- Source/discovery audit: [COVERAGE_REVIEW.md](COVERAGE_REVIEW.md); scanner: [scripts/wikipedia_candidate_scan.py](scripts/wikipedia_candidate_scan.py); scan docs: [WIKIPEDIA_DISCOVERY.md](WIKIPEDIA_DISCOVERY.md); source metadata auditor: [scripts/audit_corpus.py](scripts/audit_corpus.py).
- Previous 879-entry audit: 257 citations pointing to broad Wikipedia topic lists; 82 definition bodies shorter than 90 characters; 0 reviewed entries; 2 intentionally distinct entries titled Open set. Details in COVERAGE_REVIEW.md.
- Do not start or continue AWS/arXiv bulk download; user explicitly put that on hold.

## Next batch: direct-source audit (NOT YET COMPLETED)
1. Select a **small batch of up to 10** entries with broad Wikipedia topic-list source links (prefer function spaces/complex analysis initially).
2. Retrieve existing definition files. Read each definition and locate a **specific authoritative reference page** (individual EoM/Wikipedia article, textbook or permanent Stacks tag).
3. Verify definition hypotheses, measure/norm conventions, and mathematical correctness. Correct the body only when grounded, explaining significant changes in the commit.
4. If a precise source is verified, update its `source`; otherwise leave unchanged and log an unresolved issue. Do not falsely mark `reviewed` solely for changing the URL.
5. Run GitHub Actions build and tests after the committed batch, and update this checkpoint with actual counts and sample IDs.

## Subsequent batches
- Advance batches of up to 10 citation repairs.
- Then audit definition bodies under 90 characters, followed by full LaTeX/KaTeX rendering checks.
- Run bounded Wikipedia category scans in underrepresented subjects; review titles as *candidates*, not proven missing definitions.
- Priority new source families: Encyclopedia of Mathematics, NIST DLMF, Stacks Project, nLab, Mathlib, rigorous university textbooks, selected Wikipedia mathematical concept pages. Preserve domain and convention qualifiers.

## Process rules
- Make a small GitHub commit per batch, plus a checkpoint update.
- Check the live Git tree before edits; compare existing IDs, terms, and aliases.
- Never claim all entries were mathematically verified: source and build validation are distinct.
- Record completed batches, commit SHAs, unresolved items, and the next specific task here so another chat can resume immediately.
- If no writes or checks were done, label them pending rather than completed.

## Session status
- **Completed this session:** inspected the live 879-entry tree, Bergman examples, existing coverage review and Wikipedia discovery documentation. Created this checkpoint file.
- **Pending:** first <=10-entry reference-repair batch and verification workflow.
