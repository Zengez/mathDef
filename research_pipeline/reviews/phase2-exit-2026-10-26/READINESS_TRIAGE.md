# Phase 2 effective-state cleanup and targeted source-formulation decisions — 2026-10-26

**Status:** source-free mathematical audit and non-applying correction designs. This document is **not** a corrected mathematical source, approved graph transaction, authorization to research new missing definitions, permission to open Pass 2, or a human/independent source certificate.

**Baseline:** independent Wave 2 `main` mathematical checkpoint `a7ce2ba3cdd07e6d0b9809d4e39014fb8533228c`; inventory `34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113`; unresolved pool fingerprint `7b69e2fdcb30a4536883df44308d386219b7621533886d65276b8992959f4773`; all 659 formulation scans complete; 418 unresolved canonical candidates; zero unassigned/ambiguous; consolidation gate closed. Source evidence and engineering policy remain on separate draft PRs #14 and #15. Publication-first strategy is separately proposed in draft PR #16.

## 1. Remove obsolete smallness warnings from the pending-correction queue

**Verification method:** inspected the actual 775-event, 2.38 MB current `dependency_graph/amendments.jsonl` Git blob and current 301-event `candidate_aliases.jsonl`, compared to independent `INVENTORY.json`, rather than relying on stale original `dependency_graph/nodes/*.json` snapshots. This is an exact recorded-history inspection, **not** a fresh complete Python graph replay. Prior receipt and CI verification is described in Rounds 179 and 184.

| Source | Exact latest applied correction | Current interpretation | New action? |
| --- | --- | --- | --- |
| `form.74cd6dc48e0606fc.setoid-category` | `amend.round179.groupoid_size_scope.74cd6dc48e0606fc.setoid-category`; historical small-groupoid seed separately overridden by `seedoverride.wave2.review184.001` | Size-unrestricted groupoid candidate `missing.1ebe938ec77d5606093e`; original phrase `groupoid C` preserved | **No. Already handled, including residual seed.** |
| `form.0bf601085c1029d4.two-one-category` | `amend.round179.groupoid_size_scope.0bf601085c1029d4.two-one-category` | Same canonical ordinary-groupoid prerequisite; original local hom-category / invertibility conditions retained | **No.** |
| `form.5e4b8f6efeda6522.category-fibred-in-groupoids` | `amend.round179.groupoid_size_scope.5e4b8f6efeda6522.category-fibred-in-groupoids` | Same canonical ordinary-groupoid prerequisite; generic functor additionally preserved | **No.** |
| `form.8f7683667fac9d28.category-limit` | `amend.pass2.category_diagram.20261022.05` | No effective forced small-category target for general target C; category occurrence ultimately aliases to `missing.fcb5ab865c6d9dbb3d79`; ordinary diagram aliases to `missing.c5104821c3c70afa1f63` | **No.** |
| `form.8f7683667fac9d28.category-colimit` | `amend.pass2.category_diagram.20261022.04` | Same general-category and ordinary-functor interpretation; cocone direction remains separate from cone | **No.** |

For the three groupoid parents, candidate alias events `alias.round179.unrestricted_groupoid.groupoid_C.20261024` and `alias.round179.unrestricted_groupoid.groupoids.20261024` converge on `missing.1ebe938ec77d5606093e`. Its current registry count is **four** incoming occurrences from **three** formulations; this includes reviewed historical-seed provenance, not four new definition obligations. The explicitly small `Groupoids` target in the *groupoid-valued presheaf* source remains intentionally distinct.

**Conclusion:** The previous ambient-category and three-groupoid reports were legitimate at their capture times but describe already-applied repairs when read against the current append-only graph. Do not spend additional packets, synonym sweeps or Codex usage on reapplying them. A future automated audit should display the **effective** graph plus verified historical overrides to avoid recreating these false-positive leads.

## 2. Two source formulations with demonstrably false equivalence wording

These need eventual independently reviewed **source-formulation** correction, not a missing-candidate alias or dependency edge retarget. A mechanical phase gate should not be mistaken for permission to publish these precise bad equivalence phrases.

### 2.1 Quasi-finite at a prime (confirmed counterexample)

- **Source formulation:** `form.3718becace9c852d.quasifinite-at-prime`
- **Source version:** `bb42d9415ad7e72f4f29336e25f35d9c66ee68c9dad870e2a7bf6f40fedecf60`.
- **Recorded text:** “Let R→S be a finite-type ring homomorphism and q∈Spec(S) lying over p∈Spec(R). The map is quasi-finite at q if q is an isolated point of the fibre Spec(S⊗_R κ(p)); equivalently its local fibre has dimension zero.”
- **Effective dependency provenance:** latest `amend.global-audit.affine-fibre-type.20261023.1` already corrected the **whole fibre** target to `meaning.8a65ad25b01e5104.scheme-theoretic-fibre`; retain that amendment.

**Proof the equivalence as written is false:** let (R=k), (S=k[t]) and (q=(0)). The fibre is (operatorname{Spec} k[t]). Its generic point (q) is not isolated, but (mathcal O_{operatorname{Spec} k[t],q}=k(t)) is a field, so has Krull dimension zero. Thus local dimension zero by itself is not equivalent to quasi-finiteness at (q).

**Narrow correction option:** keep the isolated-point criterion and qualify the second statement, e.g. “For this finite-type fibre, equivalently (q) is **closed in the fibre** and the local fibre ring at (q) has Krull dimension zero.” In the Noetherian finite-type (kappa(p))-scheme, the local dimension-zero condition makes (q) a minimal prime of its affine-fibre ring; closedness makes it maximal. A prime simultaneously minimal and maximal is an isolated point of the finite-minimal-prime Noetherian spectrum. Conversely an isolated point of a finite-type scheme over a field is closed (finite-type algebras are Jacobson), and its local ring has dimension zero. Do **not** extend this simplified equivalence to arbitrary non-finite-type schemes without new review.

**Production release disposition:** correct or temporarily hold **this formulation** before production import. Do not hold unrelated accepted definitions or rescan its already-fixed fibre dependency. Verify an exact source locator during the separate source-mathematics correction step.

### 2.2 Submersive continuous map (confirmed counterexample)

- **Source formulation:** `form.83a528850cdf6a59.submersive-continuous-map`.
- **Source version:** `1620373fbacadf98c746265b93e795858111ec79dac3aeb43f8185ec7dab2be1`.
- **Recorded text:** “A continuous map f:X→Y is submersive if it is surjective and Y has the quotient topology for f; equivalently, U⊆Y is open exactly when f^{-1}(U) is open in X.”
- **Effective prerequisite graph:** latest `amend.pass2.preimages_topology.20261022.03` already retains surjectivity, quotient-topology and ordinary preimage prerequisites separately. No edge correction needed.

**Proof the last iff statement alone is false:** take (X={x}), (Y={a,b}), both discrete, (f(x)=a). Every (Usubseteq Y) is open and every (f^{-1}(U)subseteq X) is open; thus the claimed biconditional holds for all (U), but (f) is not surjective.

**Narrow correction option:** “A continuous map (f:X	o Y) is submersive if and only if **(i)** (f) is surjective and **(ii)** for each (Usubseteq Y), (U) is open in (Y) exactly when (f^{-1}(U)) is open in (X).” If a quotient-map convention is invoked, confirm it already requires surjectivity. Do not silently replace submersive with “open map.”

**Production release disposition:** correct or hold this specific source formulation; preserve valid ordinary inverse-image links and other definition variants.

## 3. Significant but narrower source/context qualifications

### 3.1 Perfect closure: char-zero scope gap

- Positive-characteristic source `form.f77b42c1adb38c56.perfect-closure`, version `1a879075ce5896d96acafcb3985438f7ac31fe91f4abb8443c8358d6f200dc76`, defines the usual (p)-power-root construction only for (p>0), and **does not** claim to cover characteristic zero.
- `form.2a93c6a662a51d67.geometrically-normal-perfect-closure-test`, version `cc46546e3bbe29636cddb3895177f1f87106af1791dea524f036dc7c5b495e1d`, and `form.6c51aeb904a0fe74.geometric-reducedness-perfect-test`, version `cd57cb4cc434771d2c5d005e0220fd1bc2a7bd8800ba426019fdb7e2a12a95b9`, invoke (k^{\mathrm{perf}}) without explicitly restricting the base field to (p>0).

**Mathematical interpretation:** In characteristic zero, (k) is already perfect; adopt the harmless piecewise convention (k^{\mathrm{perf}}=k) there. In positive characteristic, retain the original smallest perfect purely inseparable extension construction. An explicit char-zero **variant/qualification** resolves the interface without inserting a false positive-characteristic premise into the geometric-normality/reducedness statements.

**Action:** record as a scoped definition/variant integration correction before publication. The geometric property equivalences and exact source attributions must still be independently checked; this is not blanket certification of those formulas. Do not rewrite the valid positive-characteristic version as an error.

### 3.2 Rank of a map on the zero ring: total-case interpretation

- `form.41e3aea7f356bae3.rank-of-map-finite-free`, version `3f4fb3118efa02abefc7d1b7318bf9fb0947d7aa0ac024303ca6d0a0179450bf`, already appends “(and is zero when φ itself is zero)” to the maximum-nonzero-exterior-power criterion.
- For (R=0), every map of finite-free (R)-modules is the zero homomorphism, and (igwedge^0arphi=mathrm{id}_R=0). Hence the unqualified maximum-of-nonzero-maps set is empty.

**Non-exclusionary mathematically consistent reading of the *existing* text:** give its explicit zero-map clause precedence: (operatorname{rank}(arphi)=0) when (arphi=0); otherwise (max{rge1:\bigwedge^rarphi
e0}). In the nonzero-map case (igwedge^1arphi=arphi
e0), so the maximum set is nonempty, and finite-freeness bounds it above. For (R
e0) this agrees with the familiar (rge0) maximum formulation. For (R=0) it gives rank zero without falsely banning the zero ring.

**Disposition:** a documented zero-map-first convention is preferable to a global (R\ne0) assumption. Treat rank 175 as a *bounded editorial/source-convention qualification*, not evidence that the zero ring must be excluded from all Stacks-derived sources. Existing `EDGE_CASE_ASSUMPTION_LEDGER.json` keeps its one **unapplied** review candidate; nothing is promoted to the applied list here. Any eventual source text edit requires a version-guarded reviewed transaction and corresponding evidence.

### 3.3 Topological ring/module: continuity of additive inverse

- `form.646e4dcbd9b6f1e1.topological-ring`, version `03f497391324c755234793649bde87ad83ea94dc581a2ee3637168e25e5fa14d`.
- `form.646e4dcbd9b6f1e1.topological-module`, version `0760928492e0ac3367e6d3c68783c325a204a8da9f76c4d167973eb79934ba7d`.

Both require continuous addition and multiplication/action but omit continuous additive inversion. This is a real mathematical gap under their explicitly broad nonunital framework. For integers with upper-set/Alexandrov topology, addition is continuous but negation is not; zero multiplication is continuous. Likewise an integer additive group with upper-set topology and zero module action gives a module counterexample.

**Preferred bounded remedy:** explicitly require that the underlying additive group be a **topological group** (addition and negation both continuous), while retaining the currently allowed nonunital ring and nonunital module-action scopes. Alternatively, a distinctly sourced unital-action variant makes inversion automatic, but should not silently substitute for the broad source. No source edit or module convention is assumed applied here.

**Disposition:** definite mathematical source-statement repair candidate before publishing *those* formulations. Not an argument that all categorical/ring prerequisites are bad or that Phase 2's candidate registry must remain unconsolidated indefinitely.

## 4. Phase 2 stopping discipline for the publish-first milestone

### Can be closed as already repaired at current effective state

- Three unrestricted-groupoid size links, the residual setoid small-groupoid historical seed, and both generic limit/colimit size assumptions. Do not regenerate previous fix packets.
- Previously corrected candidate-resolved edges recorded in `SOURCE_DEFERRALS.md` and the 6 exact receipt-verified transactions. Preserve history rather than resubmitting.
- Mechanically checked initial 659/659 scans, 0 ambiguous/unassigned and pass2 19/19 readiness **subject to its explicit noncertification caveat**.

### High-value bounded work before the first-generation research transition

1. Mathematically review and document a **non-applying corrective source-wording plan** for quasi-finiteness and submersivity; propose exact source revisions only through a separately authorized provenance-preserving source revision workflow.
2. Decide explicitly how the characteristic-zero (k^{\mathrm{perf}}) convention is represented as a distinct scope/variant. Do not narrow generic geometric statements by mistake.
3. Decide topological ring/module inverse-continuity source typing (nonunital allowed vs supported unital variant). Preserve both if genuinely sourced.
4. Use the new review-only context metadata machinery (draft PR #15) to record typed generic integrability and clopen interpretations without replacing source or alias history. The six historic occurrences remain **unapplied**.
5. Keep the three partial provider convention questions (133, 166, 175) and relevant other source/citation limitations specifically documented; distinguish a proved counterexample from a provider wording uncertainty. A source issue can be release-held **per formulation** without blocking other eligible meanings.
6. Write a complete Pass 2 **reviewed consolidation rationale and deferral register** tied to the current inventory/unresolved fingerprint. A zero unassigned count is necessary but not sufficient for opening the gate. The revised release-first milestone aims for one first-generation research pass, not an infinite audit of ever-added terms. Require explicit transition approval and the existing phase-gate workflow; **do not force-close blockers or mutate the current gate**.

### Non-goals / boundaries

No reading, comparing or altering production mathematical definitions or frozen Wave 1 before an independently documented bounded freeze; no `definitions/`, `variants/`, Pages or searchable-index updates here. No source-free source-citation certification, no new source research, no Pass 3, no Codex request, no graph `inbox/` transactions, no protected-file modifications. The source-/wording alternatives above are mathematical **proposals**, not already accepted revisions.

## 5. Durable handoff

Next Chat work should continue from this 2026-10-26 issue audit and the live `dependency_graph/STATE.json`. Stop restarting historically resolved small-category/groupoid scope issues; instead take **one bounded source-correction review round** (the two false equivalences plus the two topological group axioms), preserve source IDs/variants, then prepare the phase transition dossier with deferred first-generation research boundaries. Re-run actual graph/tests only when a reviewed and authorized protected-data edit is proposed. Preserve the progress record and don't silently turn illustrative fixes into applied statements.
