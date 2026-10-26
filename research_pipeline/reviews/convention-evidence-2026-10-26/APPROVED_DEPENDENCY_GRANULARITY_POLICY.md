# Approved default policy: typed component-prerequisite links

**Decision status:** APPROVED by the mathDef project owner in chat on
2026-10-25 (America/New_York), following review of the 13-card,
40-historical-case convention evidence inventory. This file records a
**project-wide default modeling policy** for subsequent review and
definition linking. It does not certify a source, adjudicate an
individual occurrence, or authorize a graph transaction.

## Approved principle

> A general mathematical concept may serve as a dependency of a
> specialized construction when it is explicitly instantiated in the
> appropriate context. Linking the general concept does **not**
> assert that it is identical to the entire specialized construction.

## Operational interpretation

1. **Meaning of a dependency:** A dependency on concept D means
   that D supplies a prerequisite concept, operation, predicate or
   constituent used by the parent formulation P. It does **not**
   by itself claim `P = D`, logical equivalence of their whole
   definitions, or interchangeability of their mathematical types.
2. **Typed instantiation:** Check the ambient objects, morphism
   types, parameter values, index sets, scalar rings, hypotheses
   (commutative/unital/nonzero, etc.) and quantifier scope. A
   general prerequisite can support a specialized application only
   when the specialized occurrence is valid under those hypotheses.
   Include or preserve the instantiation and any extra data in the
   parent; a bare shared word or symbol is not enough.
3. **Whole construction remains intact:** Linking one component
   must not discard other defining data, properties, hypotheses,
   universal maps, or equivalences in P. If an occurrence is
   compound, consider multiple appropriately typed dependencies
   or a later separately reviewed segmentation. Do not silently
   re-label the compound datum as exactly one component.
4. **Identity is a stronger claim:** Merge aliases or resolve an
   existing meaning as an exact *identity* only after establishing
   equivalence of the full mathematical object/predicate under a
   matched scope. Proper generalizations, specializations,
   construction/component relations and merely equivalent tests
   of a stronger property are not automatically exact identities.
5. **Multiple variants:** When mathematically valid definitions
   differ by setting or context, retain distinguishable variants
   and use relevant context when prioritizing linked expansion.
   Do not force all usages under an unchecked global unital,
   nonunital, commutative, set/class, zero-object, or index
   convention.
6. **Evidence boundary:** Original-source conventions that are
   not established remain explicitly source-verification
   deferrals. A mathematical counterexample can reject a proposed
   unconditional link; it cannot verify what a named provider
   originally intended.
7. **Graph integrity:** Before any link amendment, alias or
   resolution, inspect the *current* source/meaning versions,
   effective references and any observed/canonical alias history.
   Use the reviewed, version-bound transaction/preflight/receipt
   workflow, preserve immutable provenance, and avoid a
   definition's circular self-prerequisite. This policy supplies
   criteria for future review but grants **no execution permission**
   on its own.

## Illustrative applications (not approved individual graph changes)

- Generic **inverse limit of rings** can be a component
  prerequisite of **I-adic completion** with its specific
  quotient system and transition maps. It is not identical to
  every I-adic completion, nor is a general inverse limit
  automatically an I-adic completion (historical rank 245).
- **Quotient ring R/I** is a component of a square-zero extension
  or a formally smooth lifting problem. It does not determine
  the extension map, kernel or lifting quantifiers (rank 3).
- A **commutative unital ring** is a legitimately scoped
  instance of some more general ring notions, but the
  prerequisite must not silently convert a bare-ring source's
  unverified convention to a unital one (rank 7).
- The **relative de Rham complex** has B-module terms and an
  A-linear differential; the underlying A-linear cochain
  complex can be a prerequisite, but B-linearity and identity
  with an arbitrary cochain complex do not follow (rank 400).
- The **multiplication map** `S⊗_R S→S` and the claim that
  it is an isomorphism in the commutative-ring epimorphism
  criterion are not the same mathematical type (rank 420).

## Decision boundary and implementation status

- The **generic-versus-specialized/component-prerequisite
  modeling question is now answered as a default policy**.
  This supersedes only earlier notes that labeled *this
  particular policy question* pending.
- Individual evidence-card conclusions remain mathematical
  review recommendations until exact live occurrences are
  adjudicated and, where appropriate, corrected.
- **Thirteen historical source-convention deferrals are not
  certified or blanket-resolved** by this approval.
- This records an owner's policy choice, **not** a declaration
  that the 40 missing candidates have been resolved or the
  40 corresponding graph edges require modification.
- No protected Wave 2 graph data, mathematical formulation,
  source record, candidate registry, alias/resolution ledger,
  transaction receipt, frozen Wave 1 item, or production site
  is changed by this decision.
- The Pass 2 consolidation gate remains closed; Pass 3 is
  unauthorized. Separate explicit mathematical adjudication,
  review and approval still govern future graph modifications.

**Supporting review:** `ADJUDICATION_QUEUE.md`,
`CHAT_ADJUDICATION_A01_A05.md`,
`CHAT_ADJUDICATION_A06_A09.md`,
`CHAT_ADJUDICATION_A10_A13.md`,
`EVIDENCE.json`. Both engineering PR #13 and the stacked
convention-evidence PR #14 remain unmerged at the time of
this decision.
