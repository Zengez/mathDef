"use strict";
/* Portable display-only helper: prioritize the source formulation's official
 * Subject, not an inferred category from term text or historic source cohort.
 *
 * Both inline and nested expansion call this through the common UI renderer.
 * No mutation of catalog order, links or canonical mathematical variants.
 */
(function (root, factory) {
  const priority = factory();
  if (typeof module === "object" && module.exports) module.exports = priority;
  if (root) root.ReferenceSubjectPriority = priority;
})(typeof window === "object" ? window : null, () => {
  const normalized = value =>
    typeof value === "string" ? value.trim().toLocaleLowerCase() : "";

  function orderFormulations(formulations, linkedMeaningId, sourceSubject,
                             preferredFormulationId = null) {
    const forms = Array.isArray(formulations) ? formulations : [];
    const requested = normalized(sourceSubject);
    const hasSubjectMatch = Boolean(requested) &&
      forms.some(form => normalized(form.subject) === requested);
    // Overrides are explicit, editor-approved decisions attached to an
    // individual link, never automatically created by visitor suggestions.
    // Matching targets win even against a different exact Subject.
    const hasApprovedTarget = Boolean(preferredFormulationId) &&
      forms.some(form => form.key === preferredFormulationId);
    // No override/match: retain the existing linked-meaning-first behavior.
    // Keep original order for equal-ranked forms; do not mutate the corpus.
    return forms.map((form, originalIndex) => ({
      form, originalIndex,
      overrideRank: hasApprovedTarget && form.key === preferredFormulationId
        ? 0 : (hasApprovedTarget ? 1 : 0),
      subjectRank: hasSubjectMatch &&
        normalized(form.subject) === requested ? 0 : (hasSubjectMatch ? 1 : 0),
      linkedRank: form.meaning_id === linkedMeaningId ? 0 : 1,
    })).sort((a, b) =>
      a.overrideRank - b.overrideRank ||
      a.subjectRank - b.subjectRank ||
      a.linkedRank - b.linkedRank ||
      a.originalIndex - b.originalIndex
    ).map(entry => entry.form);
  }

  return Object.freeze({orderFormulations});
});
