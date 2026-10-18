"use strict";
/* GitHub Issue draft adapter. No public submission can modify published data. */
(function(root){
  const BASE="https://github.com/Zengez/mathDef/issues/new";
  const CATEGORIES={
    math:"Mathematical or wording error",citation:"Incorrect or missing citation",
    wrongLink:"Incorrect or unnecessary definition link",
    missingLink:"Missing definition link",other:"Other improvement"
  };
  const oneLine=(value,max=180)=>String(value||"").replace(/[\r\n\t]+/g," ").replace(/\s+/g," ").trim().slice(0,max);
  const idValid=(v)=>/^[a-z0-9]+(?:[.-][a-z0-9]+)*$/.test(v||"");
  const pathValid=(v)=>/^definitions\/[a-z0-9/-]+\.tex$/.test(v||"");
  function buildIssue(d){
    if(!["new","correction"].includes(d.kind))throw Error("Unrecognized suggestion type.");
    let title, parts=[];
    const note=String(d.message||"").trim().slice(0,3800);
    const extra=String(d.replacement||"").trim().slice(0,3000);
    const ref=oneLine(d.reference,450);
    if(d.kind==="new"){
      const term=oneLine(d.term,150);
      if(!term)throw Error("Please enter the missing term.");
      title="[Definition request] "+term;
      parts=[
        "## Suggested mathematical term",term,
        "## Subject area",oneLine(d.subject,100)||"_Not specified_",
        "## Proposed definition (optional)",note||"_Not supplied; requesting a definition._",
        "## Further context (optional)",extra||"_None_"
      ];
    }else{
      if(!idValid(d.definitionId)||!CATEGORIES[d.category])throw Error("Missing target definition or correction type.");
      if(!note)throw Error("Please describe the correction.");
      const term=oneLine(d.definitionTerm,150)||d.definitionId;
      title="[Definition correction] "+term;
      parts=[
        "## Correction type",CATEGORIES[d.category],
        "## Definition", "- ID: "+d.definitionId+"\n- Term: "+term,
        "## Explanation",note,
        "## Suggested replacement (optional)",extra||"_None_"
      ];
      if(d.definitionVariantKey){
        parts.push("## Formulation being reviewed",
          "- Key: "+oneLine(d.definitionVariantKey,80)+
          "\n- Label: "+oneLine(d.definitionVariantLabel,180));
        if(pathValid(d.definitionVariantPath)){
          parts.push("## Formulation source file",
            "https://github.com/Zengez/mathDef/blob/main/"+d.definitionVariantPath);
        }
      }
      if(d.linkFormulationKey){
        parts.push("## Formulation containing the reported link",
          oneLine(d.linkFormulationLabel,180)+" ["+oneLine(d.linkFormulationKey,80)+"]");
      }
      if(d.linkSourceId||d.linkTargetId){
        if(!idValid(d.linkSourceId)||!idValid(d.linkTargetId))throw Error("Invalid link context.");
        parts.push("## Definition link being reported",
          "- From: "+d.linkSourceId+" — "+oneLine(d.linkSourceTerm,150)+
          "\n- To: "+d.linkTargetId+" — "+oneLine(d.linkTargetTerm,150)+
          "\n- Matched phrase: "+(oneLine(d.linkPhrase,140)||"_Not available_"));
      }
      if(pathValid(d.definitionPath)){
        parts.push("## Definition source file","https://github.com/Zengez/mathDef/blob/main/"+d.definitionPath);
      }
    }
    parts.push("## Reference (optional)",ref||"_Not provided_");
    parts.push("## Additional public attribution",
      (d.consent&&oneLine(d.attribution,100))||"_No additional public name requested; GitHub automatically identifies the issue author._");
    parts.push("---","_Proposed via mathDef. This report does not automatically change published definitions or links._");
    return {title,body:parts.join("\n\n")};
  }
  function issueUrl(d){
    const issue=buildIssue(d);
    return BASE+"?title="+encodeURIComponent(issue.title)+"&body="+encodeURIComponent(issue.body);
  }
  function init(lookup){
    const get=(id)=>document.getElementById(id), dlg=get("feedback-dialog"), form=get("feedback-form");
    if(!dlg||!form)throw Error("Feedback form is missing.");
    const fields={
      term:get("feedback-term"),subject:get("feedback-subject"),
      category:get("feedback-category"),message:get("feedback-message"),
      replacement:get("feedback-replacement"),reference:get("feedback-reference"),
      attribution:get("feedback-attribution"),consent:get("feedback-consent")
    };
    let context=null;
    const clearReady=()=>{get("feedback-github-link").hidden=true;get("feedback-ready").hidden=true;};
    function start(kind,id,link,formulationKey){
      const d=kind==="correction"?lookup(id):null;
      if(kind==="correction"&&!d)return;
      context={kind};
      if(d)Object.assign(context,{definitionId:d.id,definitionTerm:d.term,definitionPath:d.path});
      const formulation=d&&formulationKey&&
        (d.formulations||[]).find(f=>f.key===formulationKey);
      if(formulation)Object.assign(context,{
        definitionVariantKey:formulation.key,definitionVariantLabel:formulation.label,
        definitionVariantPath:formulation.path
      });
      if(link)Object.assign(context,link);
      form.reset();clearReady();get("feedback-error").hidden=true;
      const adding=kind==="new";
      get("feedback-title").textContent=adding?"Suggest a definition":"Suggest a correction";
      get("feedback-new-fields").hidden=!adding;
      get("feedback-correction-fields").hidden=adding;
      get("feedback-message-label").textContent=adding?"Suggested definition (optional)":"Explain the correction (required)";
      fields.message.required=!adding;
      fields.term.required=adding;
      fields.category.value=link?"wrongLink":"math";
      get("feedback-context").textContent=adding
        ?"Request a mathematical term that is not yet in the collection; a definition is optional."
        :"Target: "+d.term+" ["+d.id+"]"+
          (formulation?" | Formulation: "+formulation.label:"")+
          (link?" | Link: "+link.linkSourceTerm+" → "+link.linkTargetTerm:"");
      if(!dlg.open)dlg.showModal();
      (adding?fields.term:fields.category).focus();
    }
    document.addEventListener("click",(event)=>{
      const trigger=event.target.closest("[data-feedback-action]");
      if(!trigger)return;
      const action=trigger.dataset.feedbackAction;
      if(action==="new")return start("new");
      if(action==="correct")return start("correction",trigger.dataset.feedbackId,
        null,trigger.dataset.feedbackFormulation);
      if(action==="link"){
        const source=lookup(trigger.dataset.feedbackSourceId);
        const target=lookup(trigger.dataset.feedbackTargetId);
        if(source&&target)start("correction",source.id,{
          linkSourceId:source.id,linkSourceTerm:source.term,
          linkTargetId:target.id,linkTargetTerm:target.term,
          linkPhrase:trigger.dataset.feedbackPhrase||"",
          linkFormulationKey:trigger.dataset.feedbackFormulation||"",
          linkFormulationLabel:(source.formulations||[]).find(
            f=>f.key===trigger.dataset.feedbackFormulation)?.label||""
        });
      }
    });
    get("feedback-close").addEventListener("click",()=>dlg.close());
    get("feedback-cancel").addEventListener("click",()=>dlg.close());
    form.addEventListener("input",clearReady);
    form.addEventListener("change",clearReady);
    form.addEventListener("submit",(event)=>{
      event.preventDefault();
      if(!context||!form.reportValidity())return;
      const error=get("feedback-error");error.hidden=true;
      try{
        const url=issueUrl({
          ...context,term:fields.term.value,subject:fields.subject.value,
          category:fields.category.value,message:fields.message.value,
          replacement:fields.replacement.value,reference:fields.reference.value,
          attribution:fields.attribution.value,consent:fields.consent.checked
        });
        if(url.length>7800)throw Error("This suggestion is too long for a prefilled GitHub issue. Please shorten it slightly.");
        const link=get("feedback-github-link");
        link.href=url;link.hidden=false;
        get("feedback-ready").hidden=false;
        link.focus();
      }catch(err){
        error.textContent=err.message;
        error.hidden=false;
      }
    });
    return {start};
  }
  const api={buildIssue,issueUrl,init};
  root.mathDefFeedback=api;
  if(typeof module!=="undefined"&&module.exports)module.exports=api;
})(typeof window!=="undefined"?window:globalThis);
