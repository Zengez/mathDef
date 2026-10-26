# Exact Stacks k-algebra convention audit — historical rank 23

**Source-specific convention verified; no graph transaction.**
The current official Stacks pages for all five recorded parent
formulations were checked, in the provider's Algebra convention:
[§10.2, tag 00AQ](https://stacks.math.columbia.edu/tag/00AQ)
uses **commutative rings with identity**, including the zero ring.
The base field k and k-algebra structure are fixed in each source.
A k-algebra need not itself be a field or integral domain.
The canonical prerequisite should preserve the chosen structure map
`k→A`, rather than equate A with k or with a generic ring
unrelated to its base.

## Five exact source locators and parent versions

| Parent formulation | SHA256 (recorded source version) | Provider locator |
|---|---|---|
| `form.2a93c6a662a51d67.geometrically-normal-algebra` | `68689a98d4dcab5f31be729276e6af144f7dfbfee27a90284fc9f8702e51565e` | [Stacks 037Y](https://stacks.math.columbia.edu/tag/037Y) |
| `form.2a93c6a662a51d67.geometrically-normal-perfect-closure-test` | `cc46546e3bbe29636cddb3895177f1f87106af1791dea524f036dc7c5b495e1d` | [Stacks 037Y](https://stacks.math.columbia.edu/tag/037Y) |
| `form.2c5739452921ea24.geometrically-irreducible-algebra` | `5c6670e740f685c5f4a7d1f06875dfbdfac5a4d393ec5768f1286a437ec92e93` | [Stacks 00I2](https://stacks.math.columbia.edu/tag/00I2) |
| `form.6c51aeb904a0fe74.geometrically-reduced-algebra` | `0ff735e7dd78ff7b173a86cc92272a14bf9e0775efaab3e93c89f2b6b3492d5a` | [Stacks 05DS](https://stacks.math.columbia.edu/tag/05DS) |
| `form.c236facceae1dd0f.geometrically-regular-noetherian-algebra` | `023b5e04405670214b0229ffe8a702f941edef107e422cdf08f41bcc7e979990` | [Stacks 045K](https://stacks.math.columbia.edu/tag/045K) |

**Verified direct meanings:**
- [Tag 037Y, Lemma 10.165.1 and Definition 10.165.2](https://stacks.math.columbia.edu/tag/037Y):
  geometric normality tests all field extensions;
  the *perfect closure* criterion and finite purely
  inseparable tests are equivalent.
- [Tag 00I2](https://stacks.math.columbia.edu/tag/00I2):
  geometric irreducibility requires **exactly one**
  minimal prime after scalar extension, not merely
  an unqualified prime-existence claim.
- [Tag 05DS, Definition 10.43.1](https://stacks.math.columbia.edu/tag/05DS):
  geometric reducedness requires reduced scalar
  extension to **each** field extension.
- [Tag 045K, Definition 10.166.2 and Lemma 10.166.1](https://stacks.math.columbia.edu/tag/045K):
  geometric regularity is defined for a **Noetherian**
  k-algebra and tested against *finitely generated*
  or *finite purely inseparable* field extensions,
  not as an unconditional requirement that
  arbitrary-field base changes remain Noetherian
  regular rings.

## Additional paraphrase qualification (not resolved here)

The current `form.c236facceae1dd0f.geometrically-regular-noetherian-algebra`
paraphrase adds that the test is "equivalently ... for all
field extensions K/k under the hypotheses of the Stacks
criterion." That caveat is **too vague** to count as
verification that an arbitrary, possibly infinitely
generated scalar extension of a Noetherian
k-algebra is a Noetherian regular ring. The cited
Stacks definition explicitly uses finitely generated
extension fields, together with the equivalent
finite-purely-inseparable test. The all-extensions
phrase must be audited independently; **do not**
silently replace Stacks' quantifier.

**Disposition:** The rank-23 *k-algebra prerequisite*
source convention is directly verified in its
five recorded provider sections. However, the
separate geometric-regularity paraphrase qualification
is a newly specified source-correctness audit lead.
The original observational evidence is still a
paraphrase with historical version unverified;
no source text, graph link or version was changed.
