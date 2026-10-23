# Independent Wave2 — affine fibre type-safety and source-mathematics audit (2026-10-23)

**Status:** two reviewed full-node graph amendments staged; exact applied receipt and independent graph/test CI verification required before claiming applied. This pass does not modify original mathematical source texts, external citations, independent Wave1 or mathDef production.

## Concrete incorrect prerequisite targets

Two original finite-type ring-map sources refer to the **whole affine fibre** `Spec(S⊗_R κ(p))`, specifically:
1. `form.3718becace9c852d.quasifinite-at-prime`
2. `form.3fcd082413a6b2eb.relative-dimension-at-prime`

Their effective references both linked that entire fibre to `meaning.wave2.foundation.local-ring-fibre-at-prime`. That meaning is instead the **local ring at q** `S_q/pS_q`, a different typed object. The corpus also already has `meaning.8a65ad25b01e5104.scheme-theoretic-fibre`, defined as `X×_Y Spec(κ(p))`; with `X=Spec(S)`, `Y=Spec(R)` this is the correct whole fibre. Packet 135 performs **2 precise reference-target amendments**, retaining all other references and original-source wording. The selected nodes were rebuilt from the **last effective append-only amendment**, not stale original snapshots, and are pinned to their full predecessor-node hashes.

## Separate source-level mathematical issue discovered, NOT silently corrected

The original independent quasi-finite-at-a-prime formulation states that, for a finite-type ring map, being an isolated point q of its fibre is equivalent to the **local fibre ring having Krull dimension zero**. This equivalence is false without an additional closed-point/residue-field finiteness hypothesis.

**Counterexample:** For any field k let R=k, S=k[t], q=(0) in Spec(k[t]). The fibre is Spec(k[t]). Its generic point q is not isolated in that topological space; but the local fibre ring at q is k[t]_(0)=k(t), a **field of dimension zero**. The finite-type map k→k[t] is not quasi-finite at q. Hence local ring dimension zero alone cannot certify quasi-finiteness at that point. The original mathematical source formulation and its citation must be checked/corrected in a later explicitly authorized mathematical source-verification phase; the current dependency graph correction does not purport to fix the source text. Do not mark this formulation peer-certified or mathematically sound based merely on structural closure.

## Verification, scope and next step

- Verify the exact applied receipt `semantic-global-audit-affine-fibre-type-135.json` with `human_certified=false`, independent graph CI SUCCESS and isolated test CI SUCCESS.
- Expect amendment events +2 if fully applied, no new meanings/formulations, no source-text change and no unrelated reference losses.
- Continue inspecting apparent whole-object/local-object, tensor-product underlying-module versus ring-object, and finite-generation hypotheses with original context. Maintain the phase gate FALSE; no external missing-definition research or breadth expansion.
