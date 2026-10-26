# Supplemental type audit: ambient category need not be small

**Status:** source-free read-only audit lead; the current specialized
parent sources, generic categories and graph nodes have not changed.
The project owner-approved linking policy allows context-appropriate
specializations but **does not** make a small category interchangeable
with an arbitrary (possibly large) category.

## Exact existing-link evidence

Both generic category constructions carry a reference
`"categories I and C" → meaning.wave2.foundation.small-category`:

| Parent formulation | Source version | Raw node occurrence |
|---|---|---|
| `form.8f7683667fac9d28.category-limit` | `56395e0c4f7f93d321a6be152fe7e8a1fcae59867ade38ca422dacb0a45dbb3a` | `occ.325b28c2e8c20ca50819` |
| `form.8f7683667fac9d28.category-colimit` | `2ea47a3ea54397ebe3be84c01729658a09390b637e20bc824e99aaf2db608913` | `occ.618bdf1c11fdee34a6a3` |

Both source texts only assume a diagram `F:I→C`,
with cone/cocone universal properties; neither
source formula says `C` is small. The referenced
small-category formulation
`form.wave2.foundation.small-category`, source version
`0493c803df1840502c823ff5057298699040205253e27dfa6bcf11beac976604`,
requires that `Ob(C)` is a set.

In addition, `F:I→C` points to
`meaning.wave2.foundation.category-functor`
in each generic construction. That stored
functor formulation, source version
`83a4393782e9586ea43ae3b1d93a4ce943a6e23e1a7db99563c366cd9219cf04`,
explicitly defines a functor **between small categories**.
The generic source therefore has **two overlapping
smallness assumptions** introduced by its links.

## Mathematical determination

- For a set-indexed inverse-limit diagram, the
  indexing category `I` is usually small. This
  assumption is mathematically sufficient for
  many standard existence theorems.
- The ambient category `C` can be large
  (e.g. the category of **all** commutative
  unital rings relative to a chosen universe),
  while remaining locally small. The ring
  inverse limit `lim_n R/I^n` lives in
  such an ambient category; a generic
  limit construction does not require all
  rings to form a set in the same universe.
- Given a universe convention, one may
  choose a larger ambient universe making
  a category small, but that is **additional
  size data**, not established by the
  present source text.
- A functor from a small I to a locally-small,
  possibly large C still preserves identities
  and composition. A definition limited
  to functors between small categories
  is an appropriate *specialized example*
  of this broader concept, not generally
  synonymous with it.

Consequently, the current targets appear
**overly narrow if interpreted as exhaustive
typing of generic limits/colimits**. This
may be a valid component/specialization
link if the UI explicitly labels it as
such; it should not declare the source
to require C small.

## Proposed, non-applying next action

Review the two full effective nodes and the
existing `category-functor` meaning variants
against provider/universe conventions. Possible
future remedies are to retain these links
as explicitly scoped examples while
documenting that the source allows large C,
or to link to a more general category/functor
prerequisite **if independently present and
version reviewed**.

Do **not** alter `small-category` into an
unrestricted category globally, invent
large-category source terms, or strip
previously reviewed small-category references
without examining all their incoming parents.

This lead is **not part of the historical 40**
case partition and therefore does not
change the counts 13+6+20+1.
No approved amendment or preflight was run.
