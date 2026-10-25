# Prepared version-bound edge reconciliation dossiers — read-only

**Anchor:** canonical review commit `6616d53ac5449bd8ea81b8e804631709fac74459`, PR #10; generated from the immutable source/target snapshots in `POSTCOVERAGE_RECONCILIATION.json`. **No correction packet submitted, no graph mutation, no semantic acceptance, no gate transition.**

The underlying Wave 2 workflow requires **complete formulation replacement snapshots** (not tiny patches), unchanged source inventory and occurrence identities, a maximum of **five complete formulations per submitted packet**, mandatory `dependency_review_preflight`, per-packet receipts and a new graph audit **after** any separately approved application. These dossiers only prepare inputs for that later controlled process.

## 1. Real-time adapted process incorrectly pointing to discrete filtration

- Source meaning: `meaning.wave2.found85.adapted-continuous`
- Source formulation: `form.wave2.found85.adapted-continuous`
- Effective occurrence: `occ.4dc2044654482ca4b966`
- Existing target: `meaning.wave2.found85.discrete-filtration`
- Source version SHA-256: `48b208ec4f94d6e18403dd1c39b4948a79f85b0d06470bb2c897f8660c4a4650`
- Effective-node SHA-256: `c9620ad31916c4847819ce84edae793209445401fb29d81e794d52ba1f37e678`
- Source snapshot SHA-256: `261800ec342f517f5fa41bb23bfd1897d186ce93bc8c5d5a947feb2bb712652e`
- Classification: `gate_blocker_probable_wrong_target_chat_adjudicated`

**Stored source paraphrase:**

> A real-valued process (X_t)_{t≥0} adapted to a filtration (F_t)_{t≥0} satisfies that X_t is F_t-measurable for every real t≥0.

**Effective reference set — preserve every unaffected entry when preparing any future amendment:**

| Occurrence | State | Target / candidate or disposition | Phrase |
|---|---|---|---|
| `seed.3065e90deb78cb04c7cd` | existing | meaning.wave2.found85.stochastic-process | real-valued process |
| `occ.855464fab82bc14babf7` | existing | meaning.wave2.found85.stochastic-process | stochastic process indexed by t≥0 |
| `occ.4dc2044654482ca4b966` | existing | meaning.wave2.found85.discrete-filtration | sigma-algebra filtration |
| `occ.4d6cc3a8a1fa33be4827` | existing | meaning.wave2.prob90.random-variable-real | measurable real random variable |
| `occ.3cee100f060f105c219b` | missing | missing.65d334caa51c845ea335 | continuous-time filtration (F_t) |
| `occ.c1e5572c0de62eaf6914` | external | Measurability of each X_t against 𝔽_t is precisely the defining adaptedness requirement; ordinary random-variable measurability is already linked. | X_t is F_t-measurable |
| `occ.d0188a6d2c332df3d71a` | external | Continuous indexing t does not mean sample paths t↦X_t are continuous. | adaptedness not sample-path continuity |

**Target formulation(s) from the anchored review:**


- `form.wave2.found85.discrete-filtration` (version `8b78c7b55abf6e03fea01ce940241ff10e2d48647edf53fef9318f37c2aad9a8`): For a measurable space (Ω,F), a discrete-time filtration is a family (F_n)_{n≥0} of sub-σ-algebras of F such that F_n⊆F_m whenever n≤m.

**Mathematical analysis:** The ambient family is indexed by all real t>=0, while the target has integer n>=0. On Omega={0,1}, trivial-to-full sigma-algebra jumps at1/2 and3/4 have the same integer samples and different F_0.6. No sampling construction is supplied by the source. The correct distinct real-time occurrence occ.3cee100f060f105c219b already targets missing.65d334caa51c845ea335.

**Proposed later treatment (not applied):** In a source-version-bound complete-node replacement, preserve the explicit real-time missing occurrence and all other references. For the direct *ambient filtration* phrase, remove the direct discrete-target meaning link from the effective reference set or formally reclassify it as not an exact prerequisite; only add a separate sampled-filtration reference if a sampled construction is explicitly supported by source evidence. Do not erase the historical original occurrence or delete the separate discrete-filtration meaning. This is the strongest presently grounded correction candidate.

**Future acceptance checks:** Version/source hash unchanged; anchor exact occurrence and related intended missing candidate preserved; no novel reference introduced without justification; preflight passes; changed reference set creates no accidental self-edge/cycle; after explicit authorization, all 19 mechanical checks, the 60 regression tests, an exhaustive consistency scan and provenance audit are rerun. Prior checks do not preapprove the amended graph.

## 2. Ext over arbitrary coefficients pointing to commutative internal Hom module

- Source meaning: `meaning.788671763be693df.ext-group`
- Source formulation: `form.788671763be693df.ext-group`
- Effective occurrence: `occ.321952d7b781466d1856`
- Existing target: `meaning.3a0545450d7a5285.internal-hom-module`
- Source version SHA-256: `fa8adfb0f893348f71089e3e7327faa0ae57fc2e627f3e52e7be3e1218fbbd27`
- Effective-node SHA-256: `8ffbb188345e54307d2810a0ae2c4c31cff89b47b5f3a068ebd221219e6d7813`
- Source snapshot SHA-256: `af91d2f365df6eda70011bcd929aafc12fff5f44e38e80566284041b1984f81a`
- Classification: `gate_scope_reconciliation_required_chat_retained`

**Stored source paraphrase:**

> For R-modules M and N, Ext_R^i(M,N) is the ith cohomology of the cochain complex Hom_R(F_•,N) obtained by applying Hom_R(−,N) to a free resolution F_•→M.

**Effective reference set — preserve every unaffected entry when preparing any future amendment:**

| Occurrence | State | Target / candidate or disposition | Phrase |
|---|---|---|---|
| `seed.604d24d5fd8ce1d81906` | existing | meaning.788671763be693df.free-module-resolution | free resolution |
| `occ.7939694146fd228daa08` | existing | meaning.wave2.module94.unital-left-module | R-modules M and N |
| `occ.f6418d5db37174229e41` | existing | meaning.788671763be693df.free-module-resolution | free resolution F_•→M |
| `occ.321952d7b781466d1856` | existing | meaning.3a0545450d7a5285.internal-hom-module | Hom_R(F_i,N) |
| `occ.67ef12cdedd693268e03` | missing | missing.3093c306593220970d2c | cochain complex Hom_R(F_•,N) |
| `occ.89f573bdf67816397eec` | missing | missing.1bd554e6f230b14c5f9b | ith cohomology of a cochain complex |
| `occ.cb578ebc3e081c8fbb2c` | external | The superscript indexes cohomology, not ordinary ring exponentiation, and no particular free resolution is preferred. | Ext_R^i |

**Target formulation(s) from the anchored review:**


- `form.3a0545450d7a5285.internal-hom-module` (version `f5b90dc34ea1acc534f01c7bf3695afc7b6766ad777d10676407d9dab5ea9d68`): For modules M,N over a commutative ring R, the internal Hom Hom_R(M,N) is the R-module of R-linear homomorphisms M→N, with pointwise addition and scalar multiplication (r·f)(m)=r·f(m).

**Mathematical analysis:** The stored target is an R-module of Hom for COMMUTATIVE R. Over general noncommutative R, Hom_R(M,N) is an abelian group, but pointwise R action need not preserve R-linearity. For R=M2(Q), M=N=R, f=id and a=E11, the map x→ax fails linearity at r=E12: a*r=E12 but r*a=0. A center action is different scalar scope. The bare source does not state commutativity.

**Proposed later treatment (not applied):** Determine if the source's intended coefficient ring is commutative/unital by checking authorized source or original definitions; if yes, make that assumption explicit before keeping the internal-Hom R-module link. If the formulation is intentionally valid over arbitrary associative rings, its Hom terms have a canonical abelian-group structure; use a correctly typed general-Hom/additive-group prerequisite rather than commutative internal Hom. Preserve Ext and its chain/cochain structure; do not assert a canonical full-R module structure.

**Future acceptance checks:** Version/source hash unchanged; anchor exact occurrence and related intended missing candidate preserved; no novel reference introduced without justification; preflight passes; changed reference set creates no accidental self-edge/cycle; after explicit authorization, all 19 mechanical checks, the 60 regression tests, an exhaustive consistency scan and provenance audit are rerun. Prior checks do not preapprove the amended graph.

## 3. Locally connected space: global topology basis vs local connected neighborhoods

- Source meaning: `meaning.ab260940ea9c523d.locally-connected-space`
- Source formulation: `form.ab260940ea9c523d.locally-connected-space`
- Effective occurrence: `occ.cdc96f16a3e31332ec7d`
- Existing target: `meaning.6a3376e5ecb82bfb.topology-basis`
- Source version SHA-256: `67e0cc00105f0276659d7efd0cc39e3d62cf9ba7595d895939a9ba62079f33cb`
- Effective-node SHA-256: `db80cd24148a8a93ca6c6857cdb2d9729760b3e65272baa95c2baedcde9958c6`
- Source snapshot SHA-256: `891b1b5d156d7249d228b4517f26ba2aaf0417bcc6a91de71cb4ec2143bba114`
- Classification: `contextual_edge_review_not_automatically_wrong_or_gate_blocker`

**Stored source paraphrase:**

> A topological space X is locally connected if each point x possesses a fundamental system of connected neighbourhoods.

**Effective reference set — preserve every unaffected entry when preparing any future amendment:**

| Occurrence | State | Target / candidate or disposition | Phrase |
|---|---|---|---|
| `seed.6f61ddd65f10872afc36` | existing | meaning.ab260940ea9c523d.connected-topological-space | connected neighbourhoods |
| `occ.67c95d194a06c061ece4` | existing | meaning.wave2.foundation.topological-space | topological space X |
| `occ.7886d14b31bb7a1dcecd` | existing | meaning.ab260940ea9c523d.connected-topological-space | connected neighborhood |
| `occ.cdc96f16a3e31332ec7d` | existing | meaning.6a3376e5ecb82bfb.topology-basis | neighborhood basis |
| `occ.466d90b0de4bc627c881` | missing | missing.eb8e1a62d06acf7c487c | fundamental system of connected neighborhoods |
| `occ.806f208c508e37ea4447` | external | The system is required to refine arbitrary neighborhoods, not a single globally connected covering. | each point possesses a fundamental system |

**Target formulation(s) from the anchored review:**


- `form.6a3376e5ecb82bfb.topology-basis` (version `a7bc3b5148e132fc44f8010f0d456f24c3e014249c120b46f28f283e449647a8`): For a topological space X, a basis is a family B of open sets such that, whenever an open U contains x, some member of B contains x and is itself contained in U.

**Mathematical analysis:** A fundamental system at x consists of connected neighborhoods cofinal inside ALL neighborhoods of x, not merely a cover of X by connected sets. The individual neighborhoods need not be open. A global topology basis contains open sets throughout the space and need not be a neighborhood system at one point, so occ.cdc96f16a3e31332ec7d is not a direct identity with this datum. There is a legitimate related theorem: if every point has the stated system, each connected component of an open U is open, because each of its points has a connected neighborhood inside U contained in that component. This yields a global connected-open basis, but it is a derived characterization requiring explanation.

**Proposed later treatment (not applied):** Keep the specifically reviewed pointwise connected-neighborhood candidate. Determine whether the existing global open-basis link was intended as an underlying definition or a derived consequence; a pointwise cofinal family of (possibly nonopen) neighborhoods is not literally the global basis defined by the target. If the all-points theorem is intentionally cited, document its argument and type, otherwise reclassify the direct link. Lower priority than the first two.

**Future acceptance checks:** Version/source hash unchanged; anchor exact occurrence and related intended missing candidate preserved; no novel reference introduced without justification; preflight passes; changed reference set creates no accidental self-edge/cycle; after explicit authorization, all 19 mechanical checks, the 60 regression tests, an exhaustive consistency scan and provenance audit are rerun. Prior checks do not preapprove the amended graph.

## Decision register

- The first dossier has a strong source-anchored **wrong ambient target** conclusion; a correction remains intentionally unapplied.
- The second has a **source convention vs target-typing** fork; verify commutativity before any retargeting.
- The third is a **direct-link vs derived consequence** issue; the valid all-points connected-open-basis theorem does not mean a local system equals a global family.
- Do not apply the 11 independent proposed candidate alias/resolution transactions while changing these edges without separate identity-source review and event receipts.
- The main audit remains **421/421 context covered, 421 unresolved canonical identities in the live graph**, with gate closed and Pass 3 unauthorized.
