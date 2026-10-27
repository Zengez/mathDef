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

  function orderFormulations(formulations, linkedMeaningId, sourceSubject) {
    const forms = Array.isArray(formulations) ? formulations : [];
    const requested = normalized(sourceSubject);
    const hasSubjectMatch = Boolean(requested) &&
      forms.some(form => normalized(form.subject) === requested);
    // No match/unknown Subject: retain the preexisting explicit target
    // meaning ordering. Equal-priority entries keep their source order.
    return forms.map((form, originalIndex) => ({
      form, originalIndex,
      subjectRank: hasSubjectMatch &&
        normalized(form.subject) === requested ? 0 : (hasSubjectMatch ? 1 : 0),
      linkedRank: form.meaning_id === linkedMeaningId ? 0 : 1,
    })).sort((a, b) =>
      a.subjectRank - b.subjectRank ||
      a.linkedRank - b.linkedRank ||
      a.originalIndex - b.originalIndex
    ).map(entry => entry.form);
  }

  return Object.freeze({orderFormulations});
});
