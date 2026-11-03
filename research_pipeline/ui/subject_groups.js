/* Collapsible subject collections for reference-library search results.
 * Presentation only: group by supplied official subjects, never infer them.
 * Works in browsers and as a small pure module for Node tests. */
"use strict";
(function (root) {
  const escapeHtml = (value) => String(value).replace(/[&<>"']/g, ch =>
    ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]));

  function groupBySubject(entries, subjectsFor) {
    const groups = new Map();
    for (const entry of entries) {
      const value = subjectsFor(entry);
      const candidates = Array.isArray(value) ? value : [value];
      const subjects = new Set(candidates.filter(s => typeof s === "string" && s.trim())
        .map(s => s.trim()));
      if (!subjects.size) subjects.add("Unassigned");
      for (const subject of subjects) {
        if (!groups.has(subject)) groups.set(subject, []);
        groups.get(subject).push(entry);
      }
    }
    return Array.from(groups, ([subject, items]) => ({subject, items}))
      .sort((a, b) => a.subject.localeCompare(b.subject, undefined, {sensitivity:"base"}));
  }

  function create({label = "definitions", itemLabel = "term", pageSize = 100} = {}) {
    const sides = new Map();
    function stateFor(side) {
      if (!sides.has(side)) sides.set(side, {query:null, open:new Set(), limits:new Map()});
      return sides.get(side);
    }
    function render(side, query, entries, subjectsFor, itemHtml) {
      const groups = groupBySubject(entries, subjectsFor);
      const state = stateFor(side);
      // A new nonempty query reveals ALL its matching subjects. Clearing
      // the query returns to collapsed browsing. A plain rerender (such as
      // selecting a result) preserves the visitor's manual disclosure choices.
      if (state.query !== query) {
        state.query = query;
        state.open = new Set(query.trim() ? groups.map(group => group.subject) : []);
        state.limits = new Map();
      }
      return groups.map(({subject, items}, i) => {
        const open = state.open.has(subject);
        const limit = state.limits.get(subject) || pageSize;
        const region = escapeHtml(side) + "-subject-results-" + i;
        const count = items.length + " " + itemLabel + (items.length === 1 ? "" : "s");
        const header = '<h4 class="subject-collection-heading"><button type="button" ' +
          'class="subject-collection-toggle" data-subject-toggle="' + escapeHtml(subject) +
          '" aria-expanded="' + String(open) + '" aria-controls="' + region + '">' +
          '<span class="subject-collection-arrow" aria-hidden="true">' +
          (open ? "▾" : "▸") + '</span><span class="subject-collection-name">' +
          escapeHtml(subject) + " " + escapeHtml(label) +
          '</span><span class="subject-collection-count">' + escapeHtml(count) +
          '</span></button></h4>';
        let contents = "";
        if (open) {
          contents = items.slice(0, limit).map(itemHtml).join("");
          if (items.length > limit) {
            contents += '<button type="button" class="subject-collection-more" ' +
              'data-subject-more="' + escapeHtml(subject) + '">Show next ' +
              escapeHtml(itemLabel) + 's (' + (items.length - limit) +
              ' remaining)</button>';
          }
        }
        return '<section class="subject-collection">' + header +
          '<div id="' + region + '" class="subject-collection-items"' +
          (open ? "" : " hidden") + '>' + contents + '</div></section>';
      }).join("");
    }
    function toggle(side, subject) {
      const open = stateFor(side).open;
      if (open.has(subject)) open.delete(subject);
      else open.add(subject);
    }
    function showMore(side, subject) {
      const state = stateFor(side);
      state.limits.set(subject, (state.limits.get(subject) || pageSize) + pageSize);
    }
    return {render, toggle, showMore};
  }
  const api = {create, groupBySubject};
  if (root) root.ReferenceSubjectGroups = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : null);
