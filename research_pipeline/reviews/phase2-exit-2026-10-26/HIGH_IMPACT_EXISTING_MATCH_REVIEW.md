# High-impact candidate-vs-existing-meaning review — 2026-10-26

**Status: source-free classification, read-only.** The candidate pool is not yet approved for Pass 3 research and no canonical identity was merged, resolved, promoted, frozen or published. This report compares source-free candidate records with the **611 independent Wave 2 contextual meanings only**, not with production mathDef. It complements the pinned machine ranking `PRIORITY_PREVIEW.json`.

**Current graph:** `main` at independent data commit `a7ce2ba3cdd07e6d0b9809d4e39014fb8533228c`, inventory `34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113`, unresolved fingerprint `7b69e2fdcb30a4536883df44308d386219b7621533886d65276b8992959f4773`. Inspected the 727 current missing-candidate registry records and the complete independent `INVENTORY.json` meaning descriptions.

## What the 418 unresolved classes represent

- **418** current unresolved canonical IDs, representing **841** effective missing occurrences across the scanned initial corpus.
- By number of distinct upstream formulation sources, **290** identities have exactly one, **101** have two to four, **18** have five to nine, **7** have ten to nineteen, and **2** have at least twenty.
- The most repeated two canonical IDs account for **99 of 841 occurrences** (~11.8%). Their recurrence makes them efficient first-generation research subjects but does not by itself certify them as genuinely distinct new definitions.
- All 418 are **candidate previews**, not 418 user-facing mathematical terms. Some may be notation, deferred primitive vocabulary, source-specific formulations, or already-known ideas under other terms. Such statuses require contextual review; do not force a new definition for every ID.

## Nine highly reused independent prerequisites: no safe existing-meaning substitution

The following nine are **187 incoming occurrences** across **166 per-candidate distinct-parent counts** (which may overlap between candidates) as counted in the current machine registry; this is not a claim that all 187 become published links. Context, object types and source conventions were compared to the currently populated independent meanings.

| Canonical ID | Candidate | Uses (occurrences) | Closest populated notion; reason **not** to auto-resolve |
| --- | --- | ---: | --- |
| `missing.fcb5ab865c6d9dbb3d79` | Ordinary size-unrestricted category | 60 | `meaning.wave2.foundation.small-category` requires object **set**. Generic category permits a large object class; linking every ordinary category to small category reintroduces an unjustified size axiom. |
| `missing.c5104821c3c70afa1f63` | Ordinary covariant functor | 39 | `meaning.wave2.foundation.category-functor` defines a functor **between small categories**. Special constructions (monoidal, exact, representable) do not define every ordinary functor or remove source/target size constraints. |
| `missing.50fc57153b93520a247a` | Quotient ring A/I | 16 | `meaning.559efcb6f15ddc96.total-quotient-ring` is a localization, not the general ideal-coset quotient ring. Quotients by prime ideals add domain structure that arbitrary ideal quotients need not have. |
| `missing.b86257b3cce62907e97e` | Set-theoretic inverse image f⁻¹[B] | 15 | A general mapping or inverse **function** does not supply the subset preimage operation; inverse images do not require bijectivity. No independent standalone matching meaning was found by exact name/context inspection. |
| `missing.9db64b2f9cdb8258e3d8` | Polynomial algebra R[X_i] | 14 | Individual polynomial/construction applications in the corpus are not the general polynomial **ring** with independent indeterminates and finite monomial support. No exact matching standalone meaning found. |
| `missing.38969d113c4ee1db6e98` | Residue field A/m, κ(p) | 11 | A field or local ring by itself does not define the specific maximal-ideal quotient and its point/localization instantiation. No exact matching standalone meaning found. |
| `missing.5645554e6bee6b40edda` | Commutative unital ring | 11 | `meaning.wave2.foundation.integral-domain` additionally requires nonzero and no nonzero zero divisors. `meaning.wave2.foundation.commutative-prime-ideal` presupposes a commutative ring, rather than defining the general ring object. |
| `missing.7462fa5f90275b34779a` | Free R-module | 11 | The existing finite **locally free** module meaning is restricted by finiteness/local triviality; freeness of arbitrary rank is a global basis property, not equivalent to local freeness. |
| `missing.6baca7285e379e18e82b` | Quotient module M/N | 10 | Modules and module-theoretic relative constructions appear, but the general induced coset **R-module quotient** is a separate reusable algebraic object; arbitrary quotient modules must not be identified with quotient rings or scalar-restriction constructions. |

**Count cross-check:** 60+39+16+15+14+11+11+11+10 = **187**. These are **9** provisional independent-missing meanings with an especially strong case for deliberate first-generation research or explicit supported existing-meaning discovery. They are **not** approved new source observations, publications, meanings or resolution events.

## Consequences for the publish-first phase boundary

1. Do not continue treating the highest-impact ordinary-category/functor candidates as likely lexical aliases of the smaller specialized meanings; that would undo mathematical scope corrections already present in the effective graph. A future source-backed general meaning is a plausible independent addition and its incoming occurrences can then resolve by reviewed, exact-version transactions.
2. The high-impact quotient ring / inverse image / polynomial ring / residue field / free module / quotient module concepts similarly deserve **bounded** first-generation source research rather than more cosmetic synonym rounds. The case for a missing independent general meaning is stronger than the case for forced matching to the specialized forms now present.
3. Each candidate must still be checked when the research gate opens against all independently admitted and provisional meanings and their contexts; the above is a **targeted negative existing-match finding**, not proof of exhaustive absence.
4. The 290 single-parent candidates should not be required to undergo as many global duplicate comparisons as a concept serving forty parents. Source-free global consolidation should have an explicit stop condition and a fingerprint-bound rationale. Each still receives a deliberate research/no-new-definition/defer disposition in the bounded batch under the owner's publication-first plan.
5. Do not inspect or compare with the original production `definitions/` before an independently frozen release candidate. A candidate absent from Wave 2 might exist in the current public website; publication integration is responsible for merging rather than blindly adding duplicate search headings.

**No changes applied:** independent source inventory, raw candidate IDs, existing/alias targets, 2,293 protected files, qualification ledger, immutable reviewed receipts and Pass 2 phase/gate remain unchanged. No Python tests or external source page checks were run for this read-only analysis.

**Next bounded work:** issue a mathematically reviewed Pass 2 exit dossier, quarantine/fix demonstrably bad source formulations by scoped procedures, and approve the first-generation research queue only via the existing consolidation gate (or an explicitly reviewed changed gate contract). Recursively discovered prerequisites do not expand the first publication's required queue.
