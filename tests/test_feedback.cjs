"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { buildIssue, issueUrl } = require("../web/feedback.js");

test("new definition requires only a term and preserves optional proposal", () => {
  assert.throws(() => buildIssue({kind:"new",term:"  "}), /term/i);
  const issue = buildIssue({kind:"new",term:"Bergman metric",subject:"SCV",
    message:"Definition with $g_{i\\bar j}$ and a reference",replacement:"",
    reference:"https://example.org/paper",consent:false,attribution:"do not publish me"});
  assert.match(issue.title,/^\[Definition request\] Bergman metric$/);
  assert.match(issue.body,/Bergman metric/);
  assert.match(issue.body,/SCV/);
  assert.match(issue.body,/\$g_\{i\\bar j\}\$/);
  assert.match(issue.body,/https:\/\/example.org\/paper/);
  assert.doesNotMatch(issue.body,/do not publish me/);
});

test("user may request public attribution explicitly", () => {
  const anonymous = buildIssue({kind:"new",term:"Frobenius",attribution:"A. Mathematician"});
  const attributed = buildIssue({kind:"new",term:"Frobenius",attribution:"A. Mathematician",consent:true});
  assert.doesNotMatch(anonymous.body,/A\. Mathematician/);
  assert.match(attributed.body,/A\. Mathematician/);
});

test("correction preserves exact source file rather than assuming file name from ID", () => {
  const issue=buildIssue({
    kind:"correction",category:"citation",definitionId:"scv.analytic-set-germ",
    definitionTerm:"Germ of a complex analytic set",
    definitionPath:"definitions/scv/analytic-set-germ.tex",
    message:"The reference is missing the relevant theorem",
    replacement:"Try this reference."
  });
  assert.match(issue.title,/\[Definition correction\]/);
  assert.match(issue.body,/scv\.analytic-set-germ/);
  assert.match(issue.body,/definitions\/scv\/analytic-set-germ\.tex/);
  assert.match(issue.body,/The reference is missing/);
  assert.throws(()=>buildIssue({...issue,kind:"correction",category:"citation",definitionId:"invalid/id",message:"Fix"}),/definition/i);
});

test("link reports preserve both the source and the target IDs", () => {
  const issue=buildIssue({
    kind:"correction",category:"wrongLink",
    definitionId:"algebra.group",definitionTerm:"Group",definitionPath:"definitions/algebra/group.tex",
    linkSourceId:"algebra.group",linkSourceTerm:"Group",
    linkTargetId:"functions.kernel",linkTargetTerm:"Kernel",
    linkPhrase:"kernel",message:"This should not be linked from this context."
  });
  assert.match(issue.body,/algebra\.group — Group/);
  assert.match(issue.body,/functions\.kernel — Kernel/);
  assert.match(issue.body,/Matched phrase: kernel/);
  assert.match(issue.body,/Incorrect or unnecessary definition link/);
});

test("issue URL uses GitHub create-issue draft and encodes special characters", () => {
  const url=issueUrl({kind:"new",term:"L^2 & B^2",message:"$f(x) \\in H^2$"});
  assert.ok(url.startsWith("https://github.com/Zengez/mathDef/issues/new?"));
  const parsed=new URL(url);
  assert.equal(parsed.searchParams.get("title"),"[Definition request] L^2 & B^2");
  assert.match(parsed.searchParams.get("body"),/\$f\(x\) \\in H\^2\$/);
  assert.throws(()=>buildIssue({kind:"correction",category:"math",
    definitionId:"algebra.group",message:""}),/describe/i);
});
