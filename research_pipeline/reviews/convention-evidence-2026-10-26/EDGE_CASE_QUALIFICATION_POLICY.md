# Owner-approved audit rule: empty, zero, and trivial-object qualifications

**Decision:** approved by the mathDef owner in the 2026-10-25 (America/New_York) continuation chat. **Scope:** a standing mathematical review/repair preference, not source certification, a blanket restriction on definitions, or a Pass 2 gate/Pass 3 authorization.

## Default action

When an otherwise correct mathematical definition or assertion fails solely because an empty set/family, zero ring/module, trivial group, zero map, degenerate indexing set, or comparably trivial object was silently included, reviewers **may make a narrow explicit qualification without waiting for individual owner adjudication** if its intended convention is mathematically unambiguous **and an authorized, version-guarded edit route is available**. Possible repairs include stating a necessary nonempty/nonzero/nontrivial hypothesis **or** specifying the exceptional value/convention; prefer the least restrictive correction that preserves the intended mathematical meaning.

An omission that is common in mathematical exposition can be repaired without converting every routine boundary check into a new policy decision. **Every adopted qualification must be logged** in [EDGE_CASE_ASSUMPTION_LEDGER.json](EDGE_CASE_ASSUMPTION_LEDGER.json) for later manual audit.

## Guardrails

1. **Demonstrate the defect:** record the explicit boundary counterexample, precise hypothesis or convention needed, and the exact assertion to which it applies. Do not introduce qualifications based merely on words such as "nontrivial".
2. **Select the narrowest valid fix:** prefer a zero/empty-case convention when this preserves legitimate degenerate objects; otherwise limit the domain *only* where logically necessary. Distinguish mathematical necessity from an evidence-based inference about author intention.
3. **Respect provider-specific scope:** some conventions deliberately allow degenerate objects. For example Stacks Algebra admits the zero ring and generic Stacks localization permits denominators containing zero. A general exclusion would be an unjustified change. Do not falsely ascribe the inferred qualification to an original provider.
4. **Preserve variants:** if allowing the edge case defines another legitimate convention, keep it available as a context-specific variant. A later reviewer may accept/reject the local repair without requiring a global rewrite.
5. **No unrelated changes:** do not replace entire definitions, alter quantifiers unrelated to the exception, silently merge mathematically distinct meanings, or create a self-dependency.
6. **Record every *actual* addition:** one ledger entry per separately applied definition/assertion qualification. Include object and exception type, original/qualified wording, source formulation and version, effective-node fingerprint, rationale and counterexample, any checked provider links, application commit/receipt, and pending human-review status. Distinguish *proposals* from *applied* corrections; never mark a proposed entry as applied.
7. **Keep phase controls:** the current original sources, frozen Wave 1 and live independent Wave 2 graph remain protected under the existing gate and reviewed transaction workflow. This standing consent does not replace required version/identity checks, software integrity tests, or specifically restricted review phases. If no authorized edit mechanism exists, enter a review candidate in the ledger instead of rewriting immutable evidence.
8. **Escalate genuine ambiguity:** request explicit adjudication where the repair materially changes classification/theorem scope, multiple incompatible conventions are common, the source explicitly permits the disputed boundary case, or the exceptional object has nontrivial structural consequences.

## Initial case to track (not applied)

Historical rank **175**, `form.41e3aea7f356bae3.rank-of-map-finite-free`, exhibits an empty-maximum issue for the induced exterior-power characterization of rank over the zero ring. Stacks tag [00AQ](https://stacks.math.columbia.edu/tag/00AQ) allows the zero ring, while [00MR](https://stacks.math.columbia.edu/tag/00MR) says the zero map has rank zero. A narrow explicit zero-map convention is a plausible repair, but this **does not** license globally excluding the zero ring or altering the historical source text. The exact unresolved candidate and version hashes appear in the ledger.

## Review / retrieval

The JSON ledger separates `applied_qualifications` (actual new mathematical assumptions added under this policy, each needing later human review) from `review_candidates` (known edge cases without an applied edit). The future manual review should export and examine all `applied_qualifications`, along with proposed-but-unapplied entries if desired. Later entries must reference a verifiable source/version and Git commit or transaction receipt; absence of such evidence means "not applied".

**Other existing controls:** [APPROVED_DEPENDENCY_GRANULARITY_POLICY.md](APPROVED_DEPENDENCY_GRANULARITY_POLICY.md), [POST_POLICY_CHECKPOINT.md](POST_POLICY_CHECKPOINT.md), [SPECIALIZED_SELF_REFERENCE_AND_SOURCE_EDGE_FINDINGS.md](SPECIALIZED_SELF_REFERENCE_AND_SOURCE_EDGE_FINDINGS.md).
