"use strict";
(() => {
  const el = (id) => document.getElementById(id);
  const SIDES = ["term", "definition"];
  const VIEW_MODES = ["standard", "nested", "inline"];
  const LIMIT = 100;
  let savedMode = "nested";
  try {
    const value = localStorage.getItem("mathdef-explore-mode");
    if (VIEW_MODES.includes(value)) savedMode = value;
  } catch (_e) { /* Private browsing can disable storage. */ }
  const state = {
    split: true, active: "term", selected: {term: null, definition: null},
    exploreMode: savedMode, expanded: {term: new Set(), definition: new Set()},
  };
  let entries = [], lookup = new Map();
  const escape = (v) => String(v).replace(/[&<>"']/g, (c) =>
    ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const normalized = (v) => String(v)
    .replace(/\\(?:emph|textbf|textit|mathrm|text|operatorname)\{([^{}]*)\}/g," $1 ")
    .replace(/\\[A-Za-z]+\*?/g," ").replace(/[{}$\\^_\[\]()]/g," ")
    .replace(/\s+/g," ").trim().toLowerCase();

  function matches(d, side, query) {
    if (!query) return true;
    const text = side === "term" ? [d.term, ...d.aliases].join(" ") : d.body;
    return normalized(text).includes(normalized(query)) || text.toLowerCase().includes(query.toLowerCase());
  }
  function score(d,q) {
    const t = normalized(d.term), s = normalized(q);
    return !s ? 3 : t===s ? 0 : t.startsWith(s) ? 1 : 2;
  }
  function math(root) {
    if (typeof window.renderMathInElement === "function") window.renderMathInElement(root, {
      delimiters: [
        {left:"$$",right:"$$",display:true},{left:"\\[",right:"\\]",display:true},
        {left:"\\(",right:"\\)",display:false},{left:"$",right:"$",display:false}
      ], throwOnError:false, strict:"ignore"
    });
  }
  function latexParagraph(source) {
    let s = escape(source.trim()).replace(/\n/g, " ");
    s = s.replace(/\\emph\{([^{}]*)\}/g,"<em>$1</em>")
         .replace(/\\textbf\{([^{}]*)\}/g,"<strong>$1</strong>");
    return "<p>" + s + "</p>";
  }
  function latexBody(source) {
    return source.trim().split(/\n\s*\n/).map(latexParagraph).join("");
  }
  function sourceUrl(d) {
    return "https://github.com/Zengez/mathDef/blob/main/" + d.path.split("/").map(encodeURIComponent).join("/");
  }
  function select(side, id) {
    state.selected[side] = id;
    render(side);
  }
  function expanded(side, path) {
    return state.expanded[side].has(path.join(">"));
  }
  function key(path) {
    return path.join(">");
  }
  function visibleDependencies(d, blocked) {
    const dedup = new Set();
    return (d.dependencies || []).filter((dep) => {
      if (!lookup.has(dep.id) || blocked.has(dep.id) || dedup.has(dep.id)) return false;
      dedup.add(dep.id);
      return true;
    });
  }
  function nextBlocked(blocked, deps) {
    // At deeper levels all siblings shown at this level remain accessible,
    // even while collapsed, as do every ancestor and its accessible siblings.
    return new Set([...blocked, ...deps.map((dep) => dep.id)]);
  }
  function correctionButton(id, compact = false) {
    return '<button type="button" class="suggest-correction' + (compact ? ' compact' : '') +
      '" data-feedback-action="correct" data-feedback-id="' + escape(id) +
      '" aria-label="Suggest a correction to ' + escape(lookup.get(id).term) +
      '">✎ ' + (compact ? 'Correct' : 'Suggest correction') + '</button>';
  }
  function linkReport(sourceId, dep, compact = false) {
    const source = lookup.get(sourceId), target = lookup.get(dep.id);
    return '<button type="button" class="suggest-link' + (compact ? ' compact' : '') +
      '" data-feedback-action="link" data-feedback-source-id="' + escape(sourceId) +
      '" data-feedback-target-id="' + escape(dep.id) +
      '" data-feedback-phrase="' + escape(dep.label || '') +
      '" aria-label="Report link from ' + escape(source.term) + ' to ' + escape(target.term) +
      '" title="Report an incorrect definition link">⚑' +
      (compact ? '' : ' Report link') + '</button>';
  }
  function nodeButton(side, dep, path, inline) {
    const target = lookup.get(dep.id);
    const open = expanded(side, path);
    const button = '<button type="button" class="' + (inline ? 'inline-cue' : 'dependency-toggle') +
      '" data-expand="' + escape(key(path)) + '" aria-expanded="' + String(open) + '">' +
      (inline ? '(definition: ' + escape(target.term) + ')' :
       '<span class="dependency-arrow" aria-hidden="true">' + (open ? '▾' : '▸') +
       '</span> Definition: ' + escape(target.term)) + '</button>';
    if (!inline) return button;
    return '<span class="inline-cue-actions">' + button +
      linkReport(path[path.length - 2], dep, true) + '</span>';
  }
  function renderNestedChildren(side, d, path, blocked) {
    const deps = visibleDependencies(d, blocked);
    if (!deps.length) return "";
    const childBlocked = nextBlocked(blocked, deps);
    return '<div class="dependency-children" aria-label="Definitions used">' +
      deps.map((dep) => {
        const target = lookup.get(dep.id), childPath = [...path, dep.id];
        const open = expanded(side, childPath);
        return '<section class="dependency-box"><div class="dependency-head">' +
          nodeButton(side, dep, childPath, false) +
          '<div class="dependency-feedback">' + correctionButton(dep.id, true) +
          linkReport(d.id, dep, true) + '</div></div>' +
          (open ? '<div class="dependency-content"><div class="definition">' + latexBody(target.body) +
            '</div>' + renderNestedChildren(side, target, childPath, childBlocked) + '</div>' : '') +
          '</section>';
      }).join("") + '</div>';
  }
  function paragraphsWithPositions(body) {
    const result = [], separator = /\n\s*\n/g;
    let start = 0, match;
    while ((match = separator.exec(body))) {
      if (body.slice(start, match.index).trim()) {
        result.push({start, end: match.index, source: body.slice(start, match.index)});
      }
      start = separator.lastIndex;
    }
    if (body.slice(start).trim()) result.push({start, end: body.length, source: body.slice(start)});
    return result;
  }
  function renderInlineBody(side, d, path, blocked) {
    const deps = visibleDependencies(d, blocked);
    const childBlocked = nextBlocked(blocked, deps);
    const body = paragraphsWithPositions(d.body);
    const marked = new Set();
    const html = body.map((paragraph) => {
      // Mark the occurrence immediately after the matched term. The marker
      // is replaced with a button after escaping and TeX-prose conversion.
      const situated = deps.filter((dep) =>
        dep.start >= paragraph.start && dep.end <= paragraph.end && dep.start >= 0);
      situated.sort((a,b) => a.end - b.end || a.start - b.start);
      let source = paragraph.source, shift = 0;
      situated.forEach((dep, i) => {
        const local = dep.end - paragraph.start + shift;
        const marker = "MDDEFCUE" + i + "END";
        source = source.slice(0, local) + marker + source.slice(local);
        shift += marker.length;
        marked.add(dep.id);
      });
      let item = latexParagraph(source);
      situated.forEach((dep, i) => {
        item = item.replace("MDDEFCUE" + i + "END",
          nodeButton(side, dep, [...path, dep.id], true));
      });
      const children = situated.filter((dep) => expanded(side, [...path, dep.id]));
      return item + children.map((dep) => {
        const childPath = [...path, dep.id], target = lookup.get(dep.id);
        return '<div class="inline-insert"><div class="inline-insert-heading">' +
          '<div class="inline-insert-title">Definition: ' + escape(target.term) + '</div>' +
          '<div class="dependency-feedback">' + correctionButton(dep.id, true) +
          linkReport(d.id, dep, true) + '</div></div><div class="definition">' +
          renderInlineBody(side, target, childPath, childBlocked) + '</div></div>';
      }).join("");
    }).join("");
    // Manually included dependencies may have no textual match. Place their
    // controls below the text instead of silently dropping them in inline mode.
    const extra = deps.filter((dep) => !marked.has(dep.id));
    return html + (extra.length ? '<div class="inline-extras">' + extra.map((dep) => {
      const childPath = [...path, dep.id], target = lookup.get(dep.id);
      return '<div>' + nodeButton(side, dep, childPath, true) +
        (expanded(side, childPath) ? '<div class="inline-insert"><div class="inline-insert-heading">' +
          '<div class="inline-insert-title">Definition: ' + escape(target.term) + '</div>' +
          '<div class="dependency-feedback">' + correctionButton(dep.id, true) +
          linkReport(d.id, dep, true) + '</div></div><div class="definition">' +
          renderInlineBody(side, target, childPath, childBlocked) + '</div></div>' : '') + '</div>';
    }).join("") + '</div>' : "");
  }
  function exploration(side, d) {
    const path = [d.id], blocked = new Set(path);
    if (state.exploreMode === "standard") return '<div class="definition">' + latexBody(d.body) + '</div>';
    if (state.exploreMode === "inline") {
      return '<div class="definition inline-definition">' + renderInlineBody(side, d, path, blocked) + '</div>';
    }
    return '<div class="definition">' + latexBody(d.body) + '</div>' +
      renderNestedChildren(side, d, path, blocked);
  }
  function detail(side) {
    const root = el(side + "-detail"), d = lookup.get(state.selected[side]);
    if (!d) {
      root.innerHTML = '<div class="placeholder"><strong>Select a result above</strong><p>The definition and its related terms appear here.</p></div>';
      return;
    }
    const links = d.related.map((id) => lookup.get(id)).filter(Boolean);
    const refLabel = d.arxiv ? ("arXiv:" + d.arxiv + " · " + (d.locator || "")) : "Mathematical reference";
    const topicLink = d.source ? '<a class="source" href="' + escape(d.source) +
      '" target="_blank" rel="noopener noreferrer">' + escape(refLabel) + ' ↗</a>' : "";
    const paperTitle = d.source_title ? '<p class="paper-title">' + escape(d.source_title) + '</p>' : "";
    const reviewLabel = d.status === "draft" ? '<span class="draft-label">Draft · not individually reviewed</span>' :
      (d.status === "reviewed" ? '<span class="reviewed-label">Reviewed entry</span>' :
       '<span class="draft-label">Prototype entry</span>');
    root.innerHTML = '<article><div class="subject">' + escape(d.category) + '</div>' +
      '<div class="definition-title-row"><h4>' + escape(d.term) + '</h4>' +
      correctionButton(d.id) + '</div>' + reviewLabel +
      (d.aliases.length ? '<p class="aliases">Also called: ' + d.aliases.map(escape).join(", ") + '</p>' : "") +
      exploration(side, d) +
      '<div class="related"><h5>Related definitions</h5><div class="related-list">' +
      (links.length ? links.map((r) =>
        '<button type="button" data-related="' + escape(r.id) + '">' + escape(r.term) +
        ' ↗</button>').join("") : '<span class="empty">No related terms entered.</span>') +
      '</div></div>' + paperTitle + '<div class="source-links">' + topicLink +
      '<a class="source" href="' + sourceUrl(d) +
      '" target="_blank" rel="noopener noreferrer">View LaTeX source ↗</a></div></article>';
    math(root);
  }
  function render(side) {
    const q = el(side + "-query").value.trim();
    const found = entries.filter((d) => matches(d, side, q)).sort((a,b) =>
      score(a,q) - score(b,q) || a.term.localeCompare(b.term) || a.id.localeCompare(b.id));
    el(side + "-count").textContent = found.length + (found.length === 1 ? " result" : " results");
    const root = el(side + "-results");
    root.innerHTML = found.length ? found.slice(0, LIMIT).map((d) => {
      const picked = d.id === state.selected[side];
      return '<button type="button" class="result' + (picked ? ' selected' : '') +
        '" data-id="' + escape(d.id) + '" aria-pressed="' + String(picked) +
        '"><span class="name">' + escape(d.term) + '</span><span class="category-label">' +
        escape(d.category) + '</span></button>';
    }).join("") +
      (found.length > LIMIT ? '<div class="empty">First ' + LIMIT + ' shown. Narrow your search for more.</div>' : "") :
      '<div class="empty">No matching definitions. Try another phrase.</div>';
    root.querySelectorAll("[data-id]").forEach((button) =>
      button.addEventListener("click", () => select(side, button.dataset.id)));
    math(root);
    detail(side);
  }
  function mode(split) {
    state.split = split;
    el("workspace").className = "workspace " + (split ? "split" : "focused");
    el("split").classList.toggle("active",split);
    el("focus").classList.toggle("active",!split);
    el("split").setAttribute("aria-pressed",String(split));
    el("focus").setAttribute("aria-pressed",String(!split));
    el("hint").textContent = split ? "Two independent result lists, side by side." :
      "Use either search box to choose the active results.";
    for (const side of SIDES) el(side + "-pane").classList.toggle("hidden",!split && state.active !== side);
  }
  function explorationMode(value) {
    if (!VIEW_MODES.includes(value)) return;
    state.exploreMode = value;
    try { localStorage.setItem("mathdef-explore-mode", value); } catch (_e) {}
    document.querySelectorAll("[data-explore-mode]").forEach((button) => {
      const selected = button.dataset.exploreMode === value;
      button.classList.toggle("active", selected);
      button.setAttribute("aria-pressed", String(selected));
    });
    SIDES.forEach(detail);
  }
  for (const side of SIDES) {
    el(side + "-query").addEventListener("input", () => {
      state.active = side;
      const old = lookup.get(state.selected[side]);
      if (old && !matches(old, side, el(side + "-query").value.trim())) state.selected[side] = null;
      render(side);
      if (!state.split) mode(false);
    });
    el(side + "-query").addEventListener("focus", () => {
      state.active = side;
      if (!state.split) mode(false);
    });
    el(side + "-detail").addEventListener("click", (event) => {
      const toggle = event.target.closest("button[data-expand]");
      if (toggle) {
        const path = toggle.dataset.expand;
        const set = state.expanded[side];
        if (set.has(path)) set.delete(path);
        else set.add(path);
        detail(side);
        return;
      }
      const related = event.target.closest("button[data-related]");
      if (related) select(side, related.dataset.related);
    });
  }
  document.querySelectorAll("[data-explore-mode]").forEach((button) =>
    button.addEventListener("click", () => explorationMode(button.dataset.exploreMode)));
  el("split").addEventListener("click", () => mode(true));
  el("focus").addEventListener("click", () => mode(false));
  window.mathDefFeedback.init((id) => lookup.get(id));
  fetch("./definitions-index.json", {cache:"no-cache"}).then((response) => {
    if (!response.ok) throw new Error("HTTP " + response.status);
    return response.json();
  }).then((data) => {
    if (!Array.isArray(data)) throw new Error("Invalid index");
    entries = data;
    lookup = new Map(data.map((d) => [d.id, d]));
    el("total").textContent = entries.length + " definitions";
    render("term"); render("definition"); mode(true);
    explorationMode(state.exploreMode);
  }).catch((error) => {
    el("total").textContent = "Load error"; el("error").hidden = false;
    el("error").textContent = "Could not load the definition index. Check the site build. (" + error.message + ")";
    console.error("mathDef:",error);
  });
})();
