"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const feedback = require("../web/feedback.js");

test("dialog targets nested link source and keeps new/correction requirements separate", () => {
  const oldDocument = global.document;
  const identifiers = [
    "feedback-dialog","feedback-form","feedback-term","feedback-subject",
    "feedback-category","feedback-message","feedback-replacement",
    "feedback-reference","feedback-attribution","feedback-consent",
    "feedback-github-link","feedback-ready","feedback-error","feedback-title",
    "feedback-new-fields","feedback-correction-fields",
    "feedback-message-label","feedback-context","feedback-close","feedback-cancel"
  ];
  const nodes = new Map(identifiers.map(id => [id, {
    value:"",textContent:"",hidden:false,required:false,checked:false,open:false,
    listeners:{},addEventListener(name,fn){this.listeners[name]=fn;},
    focus(){this.focused=true;},reportValidity(){return true;},
    reset(){},showModal(){this.open=true;},close(){this.open=false;}
  }]));
  const listeners = {};
  global.document = {
    getElementById(id){return nodes.get(id);},
    addEventListener(name,fn){listeners[name]=fn;}
  };
  const get=id=>nodes.get(id);
  const entries = {
    "algebra.group":{id:"algebra.group",term:"Group",path:"definitions/algebra/group.tex"},
    "algebra.normal-subgroup":{
      id:"algebra.normal-subgroup",term:"Normal subgroup",
      path:"definitions/algebra/normal-subgroup.tex"
    }
  };
  try {
    const controller=feedback.init(id=>entries[id]);
    controller.start("new");
    assert.equal(get("feedback-term").required,true);
    assert.equal(get("feedback-message").required,false);
    assert.equal(get("feedback-new-fields").hidden,false);
    assert.equal(get("feedback-correction-fields").hidden,true);
    controller.start("correction","algebra.group");
    assert.equal(get("feedback-term").required,false);
    assert.equal(get("feedback-message").required,true);
    assert.equal(get("feedback-new-fields").hidden,true);
    assert.match(get("feedback-context").textContent,/algebra\.group/);
    const button={dataset:{
      feedbackAction:"link",feedbackSourceId:"algebra.group",
      feedbackTargetId:"algebra.normal-subgroup",feedbackPhrase:"normal subgroup"
    }};
    listeners.click({target:{closest(){return button;}}});
    assert.equal(get("feedback-category").value,"wrongLink");
    assert.match(get("feedback-context").textContent,/Group → Normal subgroup/);
    get("feedback-message").value="Wrong link in this context.";
    get("feedback-attribution").value="Anonymous visitor";
    get("feedback-consent").checked=false;
    get("feedback-form").listeners.submit({preventDefault(){}});
    const prepared = new URL(get("feedback-github-link").href);
    const body = prepared.searchParams.get("body");
    assert.match(body,/algebra\.group/);
    assert.match(body,/algebra\.normal-subgroup/);
    assert.match(body,/Wrong link in this context/);
    assert.doesNotMatch(body,/Anonymous visitor/);
    assert.equal(get("feedback-github-link").hidden,false);
    get("feedback-form").listeners.input();
    assert.equal(get("feedback-github-link").hidden,true);
  } finally {
    if(oldDocument===undefined)delete global.document;
    else global.document=oldDocument;
  }
});
