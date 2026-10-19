/* Experiment-only viewer: no production database access, no auto-approval. */
"use strict";
(() => {
  const data = JSON.parse(document.getElementById("reconstruction-data").textContent);
  const groups = data.groups;
  const meanings = new Map(), byGroup = new Map(), edges = new Map();
  for (const group of groups) {
    byGroup.set(group.id, group);
    for (const meaning of group.meanings) meanings.set(meaning.id, meaning);
  }
  for (const rel of data.relations) {
    if (!edges.has(rel.from_formulation)) edges.set(rel.from_formulation, []);
    edges.get(rel.from_formulation).push(rel);
  }
  const results = document.getElementById("results");
  const sources = document.getElementById("sources");
  const sourcesContent = document.getElementById("sources-content");
  const verification = document.getElementById("verify");
  const verificationContent = document.getElementById("verify-content");
  const termInput = document.getElementById("term");
  const definitionInput = document.getElementById("definition");
  const mode = document.getElementById("mode");
  const suggestTerm = document.getElementById("suggest-term");
  let visibleLimit = 40;

  function child(parent, tag, contents, className) {
    const x = document.createElement(tag);
    if (contents !== null && contents !== undefined) x.textContent = contents;
    if (className) x.className = className;
    if (parent) parent.append(x);
    return x;
  }

  function mathText(value, parent) {
    const rex = /\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$/g;
    let offset = 0, match;
    while ((match = rex.exec(value))) {
      child(parent, "span", value.slice(offset, match.index));
      const span = child(parent, "span", match[0]);
      if (window.katex) {
        try {
          window.katex.render(match[1] || match[2], span, {
            throwOnError: false, displayMode: Boolean(match[1])
          });
        } catch (_) { span.textContent = match[0]; }
      }
      offset = rex.lastIndex;
    }
    child(parent, "span", value.slice(offset));
  }

  function openIssue(title, body) {
    const params = new URLSearchParams({title, body});
    window.open(data.github_issues + "?" + params.toString(), "_blank", "noopener,noreferrer");
  }

  function showSources(group) {
    sourcesContent.replaceChildren();
    for (const m of group.meanings) {
      child(sourcesContent, "h3", m.label);
      for (const form of m.formulations) {
        child(sourcesContent, "h4", form.id);
        const ul = child(sourcesContent, "ul");
        for (const source of form.sources) {
          const li = child(ul, "li");
          const a = child(li, "a", source.title + " — " + source.locator);
          a.href = /^https:\/\//i.test(source.locator || "") ? source.locator : source.url;
          a.target = "_blank"; a.rel = "noopener noreferrer";
          child(li, "span", " (" + source.role + ")", "muted");
        }
      }
      if (m.other_sources && m.other_sources.length) {
        child(sourcesContent, "h4", "Other encountered sources (not automatically supporting)");
        const ul = child(sourcesContent, "ul");
        for (const item of m.other_sources) {
          const li = child(ul, "li");
          const a = child(li, "a", item.title + " — " + item.locator);
          a.href = /^https:\/\//i.test(item.locator || "") ? item.locator : item.url;
          a.target = "_blank"; a.rel = "noopener noreferrer";
        }
      }
    }
    sources.showModal();
  }

  function proposeVerification(group) {
    verificationContent.replaceChildren();
    child(verificationContent, "p", "Select one or more formulations. You will review the prefilled verification claim on GitHub and sign in before submitting; editorial approval is still required.");
    const checks = [];
    for (const meaning of group.meanings) {
      child(verificationContent, "h3", meaning.label);
      for (const form of meaning.formulations) {
        const label = child(verificationContent, "label");
        const input = child(label, "input");
        input.type = "checkbox";
        label.append(document.createTextNode(" " + form.id));
        checks.push({input, meaning, form});
      }
    }
    const button = child(verificationContent, "button", "Prepare GitHub verification issue");
    button.type = "button";
    button.onclick = () => {
      const selected = checks.filter(item => item.input.checked);
      if (!selected.length) {
        child(verificationContent, "p", "Select at least one formulation.", "disclaimer");
        return;
      }
      const tick = String.fromCharCode(96);
      const rows = selected.map(x => "- [x] " + tick + x.form.id + tick +
        " (meaning " + tick + x.meaning.id + tick + ", SHA256 " +
        tick + x.form.sha256 + tick + ")");
      openIssue("Verification proposal: " + group.title,
        "### Formulations selected\n" + rows.join("\n") +
        "\n\n### What was checked and evidence\n[Please describe your assessment.]\n\n" +
        "This proposal requires maintainer review and approval.");
      verification.close();
    };
    verification.showModal();
  }

  function renderMeaning(m, parent, seen, depth) {
    const section = child(parent, "section", null, depth ? "recursive-meaning" : "meaning");
    child(section, "h3", m.label);
    for (const form of m.formulations) {
      const card = child(section, "div", null, "formulation");
      child(card, "div", "Not yet manually verified · " + form.id, "muted");
      mathText(form.text, child(card, "p", null, "math-text"));
      const correction = child(card, "button", "Suggest correction to this formulation", "subtle-button");
      correction.type = "button";
      correction.onclick = () => openIssue(
        "Definition correction proposal: " + m.display_term,
        "### Meaning and formulation\n" +
        "Term: " + m.display_term + "\nMeaning ID: " + m.id +
        "\nFormulation ID: " + form.id + "\nSHA256: " + form.sha256 +
        "\n\n### Suggested corrected definition\n[Add proposal here]" +
        "\n\n### Evidence and reason\n[Explain and provide authoritative citations]" +
        "\n\nAll corrections require human maintainer review."
      );
      for (const rel of edges.get(form.id) || []) {
        const target = meanings.get(rel.target_meaning);
        if (!target) continue;
        if (rel.relation_type !== "definition_uses") {
          // Implication and equivalence are mathematical relations, not
          // prerequisites to recursively unfold under the definition.
          const label = rel.relation_type === "logical_implication"
            ? "Implies: " : rel.relation_type === "equivalent_characterization"
            ? "Equivalent criterion (subject to hypotheses): " : "Related: ";
          const nav = child(card, "button", label + target.display_term);
          nav.type = "button";
          const justification = child(card, "p", rel.editorial_reason ||
            "Research-screened connection; verify the domain of validity.", "relation-explanation");
          nav.onclick = () => {
            termInput.value = target.display_term;
            definitionInput.value = "";
            render();
            window.scrollTo({top: 0, behavior: "smooth"});
          };
          continue;
        }
        if (mode.value === "standard") {
          const nav = child(card, "button", "View related: " + target.display_term);
          nav.type = "button";
          nav.onclick = () => {
            termInput.value = target.display_term;
            definitionInput.value = "";
            render();
            window.scrollTo({top: 0, behavior: "smooth"});
          };
          continue;
        }
        const button = child(card, "button", "Expand " + target.display_term + " — " + target.label);
        button.type = "button";
        const expansion = child(card, "div", null, "expansion " + mode.value);
        if (seen.has(target.id)) {
          button.disabled = true;
          button.title = "Circular dependency suppressed";
        } else {
          let active = false;
          button.onclick = () => {
            if (active) {
              expansion.replaceChildren();
              button.textContent = "Expand " + target.display_term + " — " + target.label;
              active = false; return;
            }
            const group = byGroup.get(target.term_group_id);
            if (!group) return;
            const ordered = [target].concat(group.meanings.filter(x => x.id !== target.id));
            for (const sibling of ordered) {
              if (seen.has(sibling.id)) continue;
              renderMeaning(sibling, expansion, new Set([...seen, sibling.id]), depth + 1);
            }
            button.textContent = "Collapse " + target.display_term;
            active = true;
          };
        }
        const linkCorrection = child(card, "button", "Report wrong link/priority", "subtle-button");
        linkCorrection.type = "button";
        linkCorrection.onclick = () => openIssue("Link context correction",
          "Source formulation: " + form.id + "\nCurrently prioritized meaning: " +
          target.id + "\nSuggested meaning/formulation:\n[Provide the better ID or context]\n\nReason:\n");
      }
    }
    return section;
  }

  function render() {
    results.replaceChildren();
    const q = termInput.value.trim().toLowerCase();
    const d = definitionInput.value.trim().toLowerCase();
    const hits = groups.filter(g =>
      (!q || [g.title, ...(g.aliases || [])].some(x => x.toLowerCase().includes(q))) &&
      (!d || g.meanings.some(m => m.formulations.some(f => f.text.toLowerCase().includes(d))))
    );
    for (const group of hits.slice(0, visibleLimit)) {
      const article = child(results, "article");
      child(article, "h2", group.title);
      const actions = child(article, "div", null, "actions");
      const sourceBtn = child(actions, "button", "View sources");
      sourceBtn.onclick = () => showSources(group);
      const verifyBtn = child(actions, "button", "Propose verification");
      verifyBtn.onclick = () => proposeVerification(group);
      for (const meaning of group.meanings) {
        renderMeaning(meaning, article, new Set([meaning.id]), 0);
      }
    }
    if (!hits.length) child(results, "p", "No matching terms");
    if (hits.length > visibleLimit) {
      const load = child(results, "button", "Show 40 more terms");
      load.type = "button";
      load.onclick = () => {
        visibleLimit += 40;
        render();
      };
    }
    child(results, "p", Math.min(hits.length, visibleLimit) +
      " of " + hits.length + " term groups displayed", "muted");
  }

  suggestTerm.addEventListener("click", () => openIssue(
    "Suggest a mathematical definition to add",
    "### Proposed mathematical term\n" + (termInput.value.trim() || "[Enter a term]") +
    "\n\n### Mathematical context\n[Context or domain]" +
    "\n\n### Suggested definition (optional)\n[Your suggested formulation]" +
    "\n\n### References\n[Authoritative source URLs or citation details]" +
    "\n\nSubmissions require maintainer review and do not update definitions automatically."
  ));
  function filterChanged() { visibleLimit = 40; render(); }
  termInput.addEventListener("input", filterChanged);
  definitionInput.addEventListener("input", filterChanged);
  mode.addEventListener("change", render);
  for (const dialog of [sources, verification]) {
    dialog.addEventListener("click", e => {if (e.target === dialog) dialog.close();});
  }
  render();
})();
