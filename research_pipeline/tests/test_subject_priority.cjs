"use strict";
const assert = require("node:assert/strict");
const test = require("node:test");
const {orderFormulations} = require("../ui/subject_priority.js");

const form = (key, subject, meaning_id) => ({key, subject, meaning_id});

test("source Algebra prioritizes the algebraic basis variant over the linked topology variant", () => {
  const topology = form("basis.topology", "Topology", "m.topology");
  const linear = form("basis.linear", "Linear Algebra", "m.linear");
  const algebra = form("basis.algebra", "Algebra", "m.algebra");
  const input = [topology, linear, algebra];
  const output = orderFormulations(input, "m.topology", "Algebra");
  assert.deepEqual(output.map(x => x.key),
    ["basis.algebra", "basis.topology", "basis.linear"]);
  assert.deepEqual(input.map(x => x.key),
    ["basis.topology", "basis.linear", "basis.algebra"],
    "Ordering a nested expansion must not mutate global search-order data");
});

test("selected meaning resolves ties among matching subjects, preserving stable sibling ordering", () => {
  const forms = [
    form("first", "Algebra", "m.first"),
    form("second", "Algebra", "m.second"),
    form("third", "Analysis", "m.other"),
    form("fourth", "Algebra", "m.second"),
  ];
  assert.deepEqual(
    orderFormulations(forms, "m.second", "Algebra").map(f=>f.key),
    ["second","fourth","first","third"]);
});

test("no matching official Subject keeps the linked-meaning-first fallback", () => {
  const forms = [
    form("first", "Topology", "m.topology"),
    form("second", "Commutative Algebra", "m.commutative"),
    form("third", "Linear Algebra", "m.linear"),
  ];
  assert.deepEqual(orderFormulations(forms, "m.linear", "Algebra").map(f=>f.key),
    ["third","first","second"], "related but differently registered subjects are not exact matches");
  assert.deepEqual(orderFormulations(forms, "m.commutative", null).map(f=>f.key),
    ["second","first","third"]);
  assert.deepEqual(orderFormulations(forms, "m.topology", "   ").map(f=>f.key),
    ["first","second","third"]);
});

test("unknown linked meaning and missing Subject preserve original order when no match exists", () => {
  const forms=[form("a",null,"x"),form("b",undefined,"y"),form("c","Algebra","z")];
  assert.deepEqual(orderFormulations(forms,"not-present",undefined).map(x=>x.key),["a","b","c"]);
  assert.deepEqual(orderFormulations(forms,null,"algebra").map(x=>x.key),["c","a","b"]);
  assert.deepEqual(orderFormulations([],null,"Algebra"),[]);
});

test("official Subject comparisons are case and whitespace insensitive", () => {
  const forms=[form("a","Topology","x"),form("b","Algebra","y")];
  assert.equal(orderFormulations(forms,"x","  algebra  ")[0].key,"b");
});

test("approved editorial override supersedes exact Subject and linked-meaning preference", () => {
  const forms=[
    form("match","Algebra","m.linked"),
    form("override","Topology","m.other"),
    form("fallback","Geometry","m.geometry")
  ];
  assert.deepEqual(orderFormulations(forms,"m.linked","Algebra","override").map(x=>x.key),
    ["override","match","fallback"]);
  assert.deepEqual(orderFormulations(forms,"m.linked","Algebra",null).map(x=>x.key),
    ["match","override","fallback"]);
  assert.equal(orderFormulations(forms,"m.linked","Algebra","invalid")[0].key,"match",
    "An obsolete unknown override must not hide a definition");
});

test("override works even when source Subject is absent", () => {
  const forms=[form("a",null,"a"),form("b","Algebra","b")];
  assert.equal(orderFormulations(forms,"a",undefined,"b")[0].key,"b");
});
