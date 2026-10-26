# Specialized prerequisite and boundary-case review — 2026-10-25

**Status: reviewed mathematical proposals only.** No resolution, source
rewrite, amendment, alias, candidate registry mutation, gate transition,
new meaning, or production/Wave 1 change has occurred. The owner-approved
generic-component prerequisite semantics is controlling; it does not
authorize case-specific graph changes.

**Evidence:** pinned complete `EVIDENCE.json`, `REANCHORING_OPTIONS.json`,
`EXACT_EFFECTIVE_OCCURRENCE_REVIEW.json`, and current integration
tooling. The [companion anchored JSON](SPECIALIZED_SELF_REFERENCE_AND_SOURCE_EDGE_REVIEW.json)
pins each of the five cases to the exact parent source version,
effective-node SHA256, canonical candidate ID and occurrence ID.
Current official Stacks pages were independently revisited for
rank 175 and rank 298.

## Three specialized missing identities must not resolve to their own parents

| Historical rank | Canonical missing identity | Own parent meaning | Disposition |
| --- | --- | --- | --- |
| **172** | `missing.244d6cfceb0dd22abbca` | `meaning.29b2c34cc33d4b62.degree-zero-localization` | Do not identity-resolve |
| **223** | `missing.50540c0ba5822a8df022` | `meaning.b85b64499f3fb523.grothendieck-group-finite-projectives` | Do not identity-resolve |
| **245** | `missing.6149b958a6aa818d4806` | `meaning.1be2fa074ef447b0.i-adic-ring-completion` | Do not identity-resolve |

All three canonical contexts are **too specialized**: they already
describe the particular full construction that their parent formulation
is defining. Replacing a missing prerequisite by the corresponding
parent meaning would cause an immediate defining self-edge.

- **Rank 172:** In a graded ring, the generic operation
  `T↦T_0` gives its degree-zero component as an additive
  subgroup (a subring where graded multiplication is present).
  Specializing `T=S_f` at a homogeneous f yields
  `S_{(f)}=(S_f)_0`. A generic degree-zero component
  operation is a valid possible prerequisite; the
  particular `S_{(f)}` is *not* its own prerequisite.
  This parent already depends on graded rings and
  ring localization. Keep degree and fraction hypotheses.
- **Rank 223:** For a commutative monoid `P`,
  its group completion `G(P)` is universal among
  monoid homomorphisms `P→A` to abelian groups.
  For `P=\pi_0(\mathrm{Proj}_{fg}(R))` under
  direct sum, its completion describes `K_0(R)`.
  The generic *group completion* is reusable; the
  specific completion of exactly that monoid is
  the full K-zero construction, not an independent
  self-referential prerequisite. Do not replace
  this with K-prime-zero using all finite modules.
- **Rank 245:** The inverse limit of a diagram
  in commutative rings is a ring of compatible
  tuples with componentwise operations. Specializing
  to `R/I^n` with reduction maps gives the
  `I`-adic ring completion, so that *specific*
  ring inverse limit is the source's whole object.
  The parent already links to a generic categorical
  limit, and may preserve the ring-limit instantiation
  without a new specialized canonical missing node.
  **Additional review lead:** the generic limit
  formulation has a seed dependency on
  `meaning.wave2.foundation.small-category`
  for both `I` and `C`, even though its source
  says only a diagram `F:I→C`. For a general
  ring category, `C` need not be small.
  The index category `I` can be small even
  when `C\) is large. Check universe/category
  scope separately; this is a possible existing-link
  typing concern, not a confirmed graph correction.

None of these is a command to drop a legitimate prerequisite.
First verify whether a generic operation is *already* linked,
and only then decide whether a remaining candidate is
redundant, warrants future separate definition research,
or needs an explicitly versioned context clarification.

## Rank 298 — possible explanatory dependency, not a required definition

**Candidate:** `missing.8f2dea7e2bd1211c0cf6`;
**source meaning:** strongly transcendental element under
`R⊆S`; **exact occurrence:** `occ.6414b479b47d231c54a8`.

The live source agrees with the official
[Stacks Definition 10.123.7 (tag 00PZ)](https://stacks.math.columbia.edu/tag/00PZ):
for every `u∈S` and polynomial coefficient tuple, the
vanishing of `uP(x)` forces each `ua_i=0`.
The formula neither **uses the phrase zero divisor**
nor assumes `u≠0` or `P(x)≠0`. The canonical candidate
instead describes a **nonzero** zero divisor as a member
of a nontrivial zero product. That concept is relevant to
the motivation for the stronger condition, but is not a
mathematically required ingredient of parsing this
definition.

**Best provisional disposition:** treat the scan-added
"zero-divisor phenomena in S" as a possible explanatory
reference, not an unresolved *necessary prerequisite*.
A later reviewer could propose setting only this
occurrence to `external`, with a precise explanation
that annihilator/zero-divisor comparisons are contextual
motivation and nonzero factor assumptions are **not**
part of the condition. Keep unrelated source and ring
references byte-identical. This would require an
**individual explicitly reviewed** version-bound whole-node
amendment and a fresh preflight; none has been
prepared, submitted, or approved here.

Do not resolve the candidate by name similarity to
the repository's zero-inclusive annihilator meaning.
The occurrence's only recorded source phrase was
introduced in the accelerated scan and is not present
in the original Stacks definition.

## Rank 175 — an exact zero-ring exception in the original rank wording

**Candidate:** `missing.25dac0c185025e52a26a`;
**source:** `form.41e3aea7f356bae3.rank-of-map-finite-free`;
**occurrence:** `occ.36b73d7bd2a48315f0c7`.

Two independently checked current official Stacks pages:
[Definition 10.102.5, tag 00MR](https://stacks.math.columbia.edu/tag/00MR)
defines rank of a finite-free module map by the maximum
`r` for which `\bigwedge^r\varphi` is nonzero,
and immediately says a zero map has rank zero.
[Stacks convention tag 00AQ](https://stacks.math.columbia.edu/tag/00AQ)
explicitly allows the **zero ring**.

For `R=0`, the maps of any finite free R-modules are
zero. Also `\bigwedge^0 R^m=R=0` and
`\bigwedge^0\varphi=\mathrm{id}_R=0`.
Hence there is **no** nonnegative integer r for which
the induced map is nonzero. Taking the "maximal r" in
the literal definition yields a maximum of an empty
set, undefined without an additional convention.
The accompanying assertion that the rank of the
zero map is zero is consistent only when treated
as an explicit override or with a qualifying
nonzero-ring condition (or another documented
choice). This source-edge question persists even
though the induced exterior-map operation is
otherwise mathematically legitimate.

**Scope:** do not exclude the zero ring globally,
and do not silently assert Stacks explicitly chose
one edge-case repair. Future options:

1. Preserve the printed exterior-power criterion for
   `R≠0` and separately define the rank to be 0
   over `R=0` / for zero maps by explicit convention.
2. Find an authoritative Stacks erratum/clarification
   addressing its zero-ring convention, then quote
   only the verified revised condition.

No parent text or authoritative observation is
rewritten at present; the source-version SHA256
is saved in the anchored JSON.

## Engineering and phase boundaries

The supported reviewed manifest/preflight mechanism
requires already-registered missing IDs for `missing`
replacement, immutable occurrence IDs, exact expected
effective-node digest, inventory/unresolved fingerprints
and full-node snapshots. It does **not** support silent
context overwrite, reverse aliases or unapproved
new candidate identities. The [Codex engineering
handoff](CODEX_CONTEXT_ADJUDICATION_HANDOFF.md)
for a guarded interpretation overlay is ready on
this branch and remains an engineering task, not
authorization to apply the six scope corrections.

**Next read-only priorities:** verify the big-category
scope of the existing category-limit seed; collect a
standalone, individually reviewed rank-298 optional
external-disposition *proposal* without applying it;
then reconcile remaining source-convention edge cases.
The consolidated Pass 2 gate stays closed.
