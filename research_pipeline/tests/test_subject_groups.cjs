"use strict";
const assert = require("node:assert/strict");
const test = require("node:test");
const {create, groupBySubject} = require("../ui/subject_groups.js");

const subjects = d => d.formulations.map(f => f.subject);
const item = d => '<button data-entry="' + d.id + '">' + d.term + '</button>';
const entries = [
  {id:"1",term:"Basis",formulations:[{subject:"Linear Algebra"},{subject:"Topology"}]},
  {id:"2",term:"Group",formulations:[{subject:"Algebra"},{subject:"Algebra"}]},
  {id:"3",term:"Orphan",formulations:[{subject:null}]},
];

test("groups by official formulation subject, not research-origin category", () => {
  const groups = groupBySubject(entries, subjects);
  assert.deepEqual(groups.map(g => [g.subject, g.items.map(e => e.id)]), [
    ["Algebra",["2"]],
    ["Linear Algebra",["1"]],
    ["Topology",["1"]],
    ["Unassigned",["3"]],
  ]);
  assert.equal(groups.reduce((n,g) => n+g.items.length,0),4,
    "A multi-subject term may appear in multiple collections");
  assert.equal(entries.length,3,"The unique term search result count must remain unchanged");
});

test("initial browsing is collapsed; a search opens every matching subject", () => {
  const ui=create({label:"definitions",itemLabel:"term",pageSize:100});
  const initial=ui.render("term","",entries,subjects,item);
  assert.equal((initial.match(/aria-expanded="false"/g)||[]).length,4);
  assert(!initial.includes('data-entry="1"'),"Do not render hidden result buttons initially");
  assert(initial.includes("Linear Algebra definitions"));
  assert(initial.includes("1 term"));
  const searched=ui.render("term","basis",[entries[0]],subjects,item);
  assert.equal((searched.match(/aria-expanded="true"/g)||[]).length,2);
  assert.equal((searched.match(/data-entry="1"/g)||[]).length,2);
  assert(!searched.includes("Algebra definitions"),"Only matching groups appear after filtering");
});

test("manual disclosures persist on selection but reset on a new query or clear", () => {
  const ui=create();
  ui.render("term","",entries,subjects,item);
  ui.toggle("term","Algebra");
  assert(ui.render("term","",entries,subjects,item).includes('data-entry="2"'));
  ui.render("term","group",[entries[1]],subjects,item);
  ui.toggle("term","Algebra");
  assert(!ui.render("term","group",[entries[1]],subjects,item).includes('data-entry="2"'));
  assert(ui.render("term","grou",[entries[1]],subjects,item).includes('data-entry="2"'));
  const cleared=ui.render("term","",entries,subjects,item);
  assert(!cleared.includes('data-entry="2"'));
  assert(cleared.includes('data-subject-toggle="Algebra"'));
  const independent=ui.render("definition","topology",[entries[0]],subjects,item);
  assert(independent.includes('data-entry="1"'));
});

test("per-subject pagination exposes all matching terms without a global first-100 cutoff", () => {
  const many=Array.from({length:7},(_,i)=>({
    id:String(i),term:"Term "+i,formulations:[{subject:"Analysis"}]
  }));
  const ui=create({pageSize:3});
  let html=ui.render("term","term",many,subjects,item);
  assert.equal((html.match(/data-entry=/g)||[]).length,3);
  assert(html.includes("4 remaining"));
  ui.showMore("term","Analysis");
  html=ui.render("term","term",many,subjects,item);
  assert.equal((html.match(/data-entry=/g)||[]).length,6);
  ui.showMore("term","Analysis");
  html=ui.render("term","term",many,subjects,item);
  assert.equal((html.match(/data-entry=/g)||[]).length,7);
  assert(!html.includes("remaining"));
});

test("subject labels are escaped before insertion into HTML", () => {
  const ui=create();
  const bad=[{id:"x",term:"X",formulations:[{subject:'<script>" & Algebra'}]}];
  const html=ui.render("term","x",bad,subjects,item);
  assert(!html.includes("<script>"));
  assert(html.includes("&lt;script&gt;"));
  assert(html.includes("&quot;"));
  assert(html.includes("&amp;"));
});
