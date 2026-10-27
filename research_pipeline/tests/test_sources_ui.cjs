"use strict";
const assert = require("node:assert/strict");
const test = require("node:test");
const {summarize} = require("../ui/sources_ui.js");

const entry={
  id:"g.basis",term:"Basis",formulations:[
    {key:"f.top",label:"Topological",meaning_id:"m.top"},
    {key:"f.alg",label:"Algebraic",meaning_id:"m.alg"}
  ]
};
const source=(id,title,meaning_id,formulation_id,provenance_only=false)=>({
  id,url:"https://example.org/"+id,titles:[title],
  occurrences:[{group_id:"g.basis",meaning_id,formulation_id,provenance_only,
    role:provenance_only?"source-file provenance":"definition evidence",
    verification_status:"untracked"}]
});
const registry={
  groups:[{group_id:"g.basis",term:"Basis",meanings:[
    {meaning_id:"m.top",subject:"Topology",source_ids:["s.top"],
      primary_source_by_formulation:{"f.top":"s.top"}},
    {meaning_id:"m.alg",subject:"Algebra",source_ids:["s.alg","s.encounter","s.prov"],
      primary_source_by_formulation:{"f.alg":"s.alg"}}
  ]}],
  sources:{
    "s.top":source("s.top","Topological source","m.top","f.top"),
    "s.alg":source("s.alg","Algebra source","m.alg","f.alg"),
    "s.encounter":source("s.encounter","Mentioned book","m.alg",null),
    "s.prov":source("s.prov","Internal provenance","m.alg","f.alg",true)
  }
};
test("source UI groups evidence by distinct meanings and formulations",()=>{
 const view=summarize(registry,entry);
 assert.equal(view.meanings.length,2);
 assert.equal(view.meanings[0].forms[0].references[0].id,"s.top");
 assert.equal(view.meanings[1].forms[0].references.find(x=>x.primary).id,"s.alg");
 assert.equal(view.meanings[1].forms[0].references.find(x=>x.provenance).id,"s.prov");
 assert.equal(view.meanings[1].encountered[0].id,"s.encounter");
});
test("formulation-filtered sources stay scoped to the selected meaning",()=>{
 const view=summarize(registry,entry,"f.alg");
 assert.equal(view.meanings.length,1);
 assert.equal(view.meanings[0].forms.length,1);
 assert.equal(view.meanings[0].forms[0].key,"f.alg");
 assert.deepEqual(view.meanings[0].encountered,[]);
});
test("no invented evidence and missing term return empty view",()=>{
 assert.equal(summarize(registry,{id:"missing"}),null);
 const view=summarize(registry,{id:"g.basis",formulations:[]});
 assert.equal(view.meanings.length,0);
});

test("mixed evidence at the same URL never promotes provenance to mathematical support",()=>{
 const copy=structuredClone(registry);
 copy.sources["s.alg"].occurrences.push({
   group_id:"g.basis",meaning_id:"m.alg",formulation_id:"f.alg",
   provenance_only:true,role:"source-file provenance",
   verification_status:"untracked"
 });
 const view=summarize(copy,entry);
 const refs=view.meanings[1].forms[0].references.filter(x=>x.id==="s.alg");
 assert.equal(refs.length,2);
 assert.equal(refs.filter(x=>x.primary).length,1);
 assert.equal(refs.filter(x=>x.provenance).length,1);
 assert(refs.find(x=>x.provenance).evidence.every(x=>x.provenance_only));
 assert(refs.find(x=>x.primary).evidence.every(x=>!x.provenance_only));
});
