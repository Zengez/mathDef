"use strict";
/* Read-only source evidence UI. The source registry is provided by the
 * domain adapter, fetched only after a visitor asks to see its citations.
 * All user/source strings are DOM text nodes, not HTML interpolation.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.ReferenceSourcesUI = api;
})(typeof window === "object" ? window : null, () => {
  function summarize(registry, entry, focusedForm = null) {
    if (!registry || !entry || !Array.isArray(registry.groups)) return null;
    const group = registry.groups.find(x => x.group_id === entry.id);
    if (!group) return null;
    const meanings = group.meanings.map(meaning => {
      const forms = (entry.formulations || []).filter(f =>
        f.meaning_id === meaning.meaning_id && (!focusedForm || f.key === focusedForm));
      const refsFor = formId => (meaning.source_ids || []).flatMap(sid => {
        const source = registry.sources[sid];
        if (!source) return [];
        const evidence = (source.occurrences || []).filter(o =>
          o.group_id === entry.id &&
          o.meaning_id === meaning.meaning_id &&
          o.formulation_id === formId);
        return evidence.length ? [{...source, evidence,
          primary: formId != null &&
            (meaning.primary_source_by_formulation || {})[formId] === sid,
          provenance: evidence.every(e => e.provenance_only)}] : [];
      });
      return {...meaning,
        title: forms[0]?.label || (entry.formulations || []).find(f =>
          f.meaning_id === meaning.meaning_id)?.label || meaning.meaning_id,
        forms: forms.map(form => ({...form, references: refsFor(form.key)})),
        encountered: focusedForm ? [] : refsFor(null)};
    }).filter(m => m.forms.length);
    return {term: group.term, meanings, focusedForm};
  }
  function create(config, lookup) {
    const dlg = document.getElementById("sources-dialog");
    const content = document.getElementById("sources-content");
    const intro = document.getElementById("sources-intro");
    const title = document.getElementById("sources-dialog-title");
    const correction = document.getElementById("sources-correct");
    const filename = config.sources_file;
    let promise = null, registry = null, selection = null;
    const child = (parent, tag, value, cls) => {
      const element = document.createElement(tag);
      if (value != null) element.textContent = String(value);
      if (cls) element.className = cls;
      if (parent) parent.append(element);
      return element;
    };
    const safeHref = uri => {
      try {
        const parsed = new URL(uri);
        return ["https:", "http:"].includes(parsed.protocol) ? parsed.href : null;
      } catch (_) {return null;}
    };
    const fmt = raw => String(raw || "").replace(/_/g, " ");
    const unique = values => [...new Set(values.filter(Boolean))];
    function showReferences(parent, references, kind) {
      for (const ref of references.slice().sort((a,b) =>
        Number(b.primary)-Number(a.primary) ||
        (a.titles?.[0]||a.id).localeCompare(b.titles?.[0]||b.id))) {
        const wrap = child(parent,"div",null,"sources-reference");
        const locator = ref.evidence.find(e => safeHref(e.locator))?.locator;
        const link = safeHref(locator) || safeHref(ref.url);
        const name = ref.titles?.[0] || ref.url;
        if (ref.primary && kind !== "provenance")
          child(wrap,"span","Selected primary reference · best available recorded citation","sources-primary");
        if (link) {
          const a = child(wrap,"a",name);
          a.href = link; a.target = "_blank"; a.rel = "noopener noreferrer";
        } else child(wrap,"span",name);
        const evidenceLines = unique(ref.evidence.map(e =>
          [e.role || "Citation", e.verification_status === "untracked" ||
            !e.verification_status ? "verification not recorded" :
            "verification: " + fmt(e.verification_status)].join(" · ")));
        for (const line of evidenceLines) child(wrap,"p",line,"sources-meta");
        const locations = unique(ref.evidence.map(e=>e.locator)
          .filter(v=>v && !safeHref(v) && v !== ref.url));
        for(const location of locations)
          child(wrap,"p","Locator: " + location,"sources-meta");
        for(const assessment of ref.source_convention_assessments || []) {
          const details = child(wrap,"details",null,"sources-convention");
          child(details,"summary","Source-specific convention assessment");
          child(details,"p","Status: " + fmt(assessment.status || "not checked"));
          if (assessment.scope?.name) child(details,"p",
            "Scope: " + assessment.scope.name);
          if (assessment.evidence_summary) child(details,"p",
            assessment.evidence_summary);
          if (assessment.working_interpretation)
            child(details,"p","mathDef working interpretation: " +
              String(assessment.working_interpretation));
        }
      }
    }
    function section(parent, label, references, cls) {
      if (!references.length) return;
      const box = child(parent,"section",null,cls || "");
      child(box,"h5",label,"sources-section-title");
      showReferences(box,references,cls === "sources-provenance" ? "provenance" : "citation");
    }
    function render() {
      if (!selection) return;
      const d = lookup(selection.id);
      title.textContent = d ? "Sources — " + d.term : "Sources";
      content.replaceChildren();
      if (!registry || !d) {
        child(content,"p",registry?"Term no longer available.":"Loading sources…","sources-empty");
        return;
      }
      const view = summarize(registry,d,selection.formId);
      if (!view) {
        child(content,"p","No source registry entry for this term.","sources-empty");
        return;
      }
      if (selection.formId) {
        intro.textContent="References for the selected formulation. The primary reference is selected from recorded evidence; this is not a universal verification claim.";
        const all = child(content,"button","Show sources for all definitions","sources-show-all");
        all.type="button"; all.onclick=()=>{selection.formId=null;render();};
      } else intro.textContent="Sources are grouped by meaning and formulation. A selected primary reference reflects available recorded evidence, not a reliability score or a claim of independent verification.";
      for (const meaning of view.meanings) {
        const outer = child(content,"section",null,"sources-meaning");
        child(outer,"h3",meaning.title);
        child(outer,"p",[meaning.subject,meaning.context].filter(Boolean).join(" · "),"sources-subject");
        for(const form of meaning.forms) {
          const formBox=child(outer,"section",null,"sources-formulation");
          const index=(d.formulations || []).findIndex(x=>x.key===form.key)+1;
          child(formBox,"h4","Definition " + index + " — " + form.label);
          const references=form.references.filter(x=>!x.provenance);
          const provenance=form.references.filter(x=>x.provenance);
          section(formBox,"Selected primary reference",
            references.filter(x=>x.primary));
          section(formBox,"Other cited references",
            references.filter(x=>!x.primary));
          section(formBox,"Original file / editorial provenance (not an independent mathematical source)",
            provenance,"sources-provenance");
          if(!form.references.length) child(formBox,"p",
            "No cited sources recorded for this formulation.","sources-empty");
        }
        section(outer,"Other encountered references (not automatically supporting definitions)",
          meaning.encountered.filter(x=>!x.provenance));
        section(outer,"Other provenance records",
          meaning.encountered.filter(x=>x.provenance),"sources-provenance");
      }
      if(!view.meanings.length) child(content,"p",
        "No matching formulation recorded.","sources-empty");
    }
    async function open(id,formId=null) {
      if (!filename || !dlg || !lookup(id)) return;
      selection={id,formId};
      correction.dataset.feedbackId=id;
      correction.dataset.feedbackFormulation=formId || "";
      registry=null;
      if(!dlg.open)dlg.showModal();
      title.textContent="Sources — "+lookup(id).term;
      content.replaceChildren();
      child(content,"p","Loading sources…","sources-empty");
      try {
        if(!promise) promise=fetch("./"+filename,{cache:"no-cache"}).then(r=>{
          if(!r.ok)throw Error("HTTP "+r.status);
          return r.json();
        }).then(result=>{
          if(!result || result.schema_version!==1 ||
            !Array.isArray(result.groups) || !result.sources)
            throw Error("Invalid source registry");
          return result;
        }).catch(e=>{promise=null;throw e;});
        const loaded=await promise;
        if (!dlg.open || !selection || selection.id!==id) return;
        registry=loaded;
        render();
      } catch(e) {
        if(!dlg.open || !selection || selection.id!==id)return;
        content.replaceChildren();
        child(content,"p","Could not load source references. Please try opening Sources again.","sources-empty");
      }
    }
    document.getElementById("sources-close").onclick=()=>dlg.close();
    document.getElementById("sources-done").onclick=()=>dlg.close();
    correction.addEventListener("click",()=>dlg.close());
    dlg.addEventListener("click",event=>{if(event.target===dlg)dlg.close();});
    return {open};
  }
  return Object.freeze({create,summarize});
});
