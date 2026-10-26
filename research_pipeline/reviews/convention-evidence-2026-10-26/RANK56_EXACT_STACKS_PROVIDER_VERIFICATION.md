# Additional exact provider verification — rank 56

**Status:** current official provider definitions verified; no
mathematical graph edit, source observation change, alias,
candidate resolution, or gate action.

Historical rank **56**, canonical candidate
`missing.d066de85583ac1b1a7d4`, represents
`IM` and `I^nM` for an ideal I acting on
an R-module M. The three recorded source formulations
and their observation locators were compared directly
with current Stacks official text:

1. `form.1be2fa074ef447b0.i-adic-completeness`,
   source version
   `a374648a4acf14117a98135079658cf2a521bdbb5abd3c37b954b406e92cc73f`
   (confirmed against EVIDENCE.json), records
   [Stacks Definition 10.96.2, tag 00M9](https://stacks.math.columbia.edu/tag/00M9).
   The actual provider defines completeness via
   `M→lim_n M/I^nM`, with no asserted exotic nonunital
   module action and no need to set n=0.
2. `form.1be2fa074ef447b0.i-adic-module-completion`
   uses the same tag's introductory
   `lim_n M/I^nM` and compatible residue-class
   construction. [Section 10.96](https://stacks.math.columbia.edu/tag/00M9)
   later explicitly treats `n≥1` for the
   `I^nM` quotient tower.
3. `form.951ae8411d8a974b.depth-module-ideal`
   reproduces [Stacks Definition 10.72.1,
   tag 00LE](https://stacks.math.columbia.edu/tag/00LE),
   which uses the two cases `IM≠M` and
   `IM=M` for finite R-modules.
   Neither case invokes the zeroth power.

**Mathematical scope:** Stacks Algebra treats R as a
commutative unital ring. Its ordinary R-modules
are unital in the relevant algebra context;
hence `RM=M` and the usual
`I^0M=RM=M` extension is mathematically
valid **if** the exponent-zero convention is
adopted. But the **three recorded source formulations
do not depend on adopting it**. Their actual
necessary operation is the finite-sum span of products
`im`, with positive powers where required.

The old rank-56 deferral's concern about nonunital
module counterexamples is still valid as a
**warning not to globally broaden** the candidate,
but no nonunital variant is present in these three
recorded provider definitions. This narrows the
source-check work substantially. Remaining action is
to model the already well-typed **ideal action
prerequisite** without equating it to
ideal multiplication in R or to the completion
`lim M/I^nM`.

Do not declare the three historical reconstructed
paraphrases fully provider-certified from this
targeted convention check. The exact archived
source version, provenance observations and all
other mathematical claims retain their original
verification status. No graph correction is
authorized by the official-provider evidence.
