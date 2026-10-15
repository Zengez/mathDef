"use strict";
(() => {
  const el = (id) => document.getElementById(id);
  const state = {split:true, active:"term", selected:{term:null,definition:null}};
  let entries=[], lookup=new Map();
  const LIMIT=100;
  const escape=(v)=>String(v).replace(/[&<>"']/g,(c)=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const normalized=(v)=>String(v)
    .replace(/\\(?:emph|textbf|textit|mathrm|text|operatorname)\{([^{}]*)\}/g," $1 ")
    .replace(/\\[A-Za-z]+\*?/g," ").replace(/[{}$\\^_\[\]()]/g," ").replace(/\s+/g," ").trim().toLowerCase();
  function matches(d,side,query){
    if(!query)return true;
    const text=side==="term"?[d.term,...d.aliases].join(" "):d.body;
    return normalized(text).includes(normalized(query))||text.toLowerCase().includes(query.toLowerCase());
  }
  function score(d,q){
    const t=normalized(d.term),s=normalized(q);
    return !s?3:t===s?0:t.startsWith(s)?1:2;
  }
  function math(root){
    if(typeof window.renderMathInElement==="function")window.renderMathInElement(root,{
      delimiters:[{left:"$$",right:"$$",display:true},{left:"\\[",right:"\\]",display:true},{left:"\\(",right:"\\)",display:false},{left:"$",right:"$",display:false}],throwOnError:false,strict:"ignore"
    });
  }
  function latexBody(source){
    return source.trim().split(/\n\s*\n/).map((block)=>{
      let s=escape(block.trim()).replace(/\n/g," ");
      s=s.replace(/\\emph\{([^{}]*)\}/g,"<em>$1</em>").replace(/\\textbf\{([^{}]*)\}/g,"<strong>$1</strong>");
      return "<p>"+s+"</p>";
    }).join("");
  }
  function sourceUrl(d){return "https://github.com/Zengez/mathDef/blob/main/"+d.path.split("/").map(encodeURIComponent).join("/");}
  function select(side,id){state.selected[side]=id;render(side);}
  function detail(side){
    const root=el(side+"-detail"),d=lookup.get(state.selected[side]);
    if(!d){
      root.innerHTML='<div class="placeholder"><strong>Select a result above</strong><p>The definition and its related terms appear here.</p></div>';return;
    }
    const links=d.related.map((id)=>lookup.get(id)).filter(Boolean);
    const topicLink=d.source ? '<a class="source" href="'+escape(d.source)+'" target="_blank" rel="noopener noreferrer">Mathematical reference ↗</a>' : "";
    const reviewLabel=d.status==="draft" ? '<span class="draft-label">Draft · not individually reviewed</span>' : (d.status==="reviewed" ? '<span class="reviewed-label">Reviewed entry</span>' : '<span class="draft-label">Prototype entry</span>');
    root.innerHTML='<article><div class="subject">'+escape(d.category)+'</div><h4>'+escape(d.term)+'</h4>'+reviewLabel+
      (d.aliases.length?'<p class="aliases">Also called: '+d.aliases.map(escape).join(", ")+'</p>':"")+
      '<div class="definition">'+latexBody(d.body)+'</div><div class="related"><h5>Related definitions</h5><div class="related-list">'+
      (links.length?links.map((r)=>'<button type="button" data-related="'+escape(r.id)+'">'+escape(r.term)+' ↗</button>').join(""):'<span class="empty">No related terms entered.</span>')+
      '</div></div><div class="source-links">'+topicLink+'<a class="source" href="'+sourceUrl(d)+'" target="_blank" rel="noopener noreferrer">View LaTeX source ↗</a></div></article>';
    root.querySelectorAll("[data-related]").forEach((button)=>button.addEventListener("click",()=>select(side,button.dataset.related)));
    math(root);
  }
  function render(side){
    const q=el(side+"-query").value.trim();
    const found=entries.filter((d)=>matches(d,side,q)).sort((a,b)=>score(a,q)-score(b,q)||a.term.localeCompare(b.term)||a.id.localeCompare(b.id));
    el(side+"-count").textContent=found.length+(found.length===1?" result":" results");
    const root=el(side+"-results");
    root.innerHTML=found.length?found.slice(0,LIMIT).map((d)=>{
      const picked=d.id===state.selected[side];
      return '<button type="button" class="result'+(picked?' selected':'')+'" data-id="'+escape(d.id)+'" aria-pressed="'+picked+'"><span class="name">'+escape(d.term)+'</span><span class="category-label">'+escape(d.category)+'</span></button>';
    }).join("")+(found.length>LIMIT?'<div class="empty">First '+LIMIT+' shown. Narrow your search for more.</div>':"")
    :'<div class="empty">No matching definitions. Try another phrase.</div>';
    root.querySelectorAll("[data-id]").forEach((button)=>button.addEventListener("click",()=>select(side,button.dataset.id)));
    math(root);detail(side);
  }
  function mode(split){
    state.split=split;
    el("workspace").className="workspace "+(split?"split":"focused");
    el("split").classList.toggle("active",split);el("focus").classList.toggle("active",!split);
    el("split").setAttribute("aria-pressed",String(split));el("focus").setAttribute("aria-pressed",String(!split));
    el("hint").textContent=split?"Two independent result lists, side by side.":"Use either search box to choose the active results.";
    for(const side of ["term","definition"])el(side+"-pane").classList.toggle("hidden",!split&&state.active!==side);
  }
  for(const side of ["term","definition"]){
    el(side+"-query").addEventListener("input",()=>{
      state.active=side;
      const old=lookup.get(state.selected[side]);
      if(old&&!matches(old,side,el(side+"-query").value.trim()))state.selected[side]=null;
      render(side);if(!state.split)mode(false);
    });
    el(side+"-query").addEventListener("focus",()=>{state.active=side;if(!state.split)mode(false);});
  }
  el("split").addEventListener("click",()=>mode(true));
  el("focus").addEventListener("click",()=>mode(false));
  fetch("./definitions-index.json",{cache:"no-cache"}).then((r)=>{
    if(!r.ok)throw new Error("HTTP "+r.status);return r.json();
  }).then((data)=>{
    if(!Array.isArray(data))throw new Error("Invalid index");
    entries=data;lookup=new Map(data.map((d)=>[d.id,d]));
    el("total").textContent=entries.length+" definitions";
    render("term");render("definition");mode(true);
  }).catch((e)=>{
    el("total").textContent="Load error";el("error").hidden=false;
    el("error").textContent="Could not load the definition index. Check the site build. ("+e.message+")";
    console.error("mathDef:",e);
  });
})();
