"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const feedback = require("../ui/feedback.js");

test("independent feedback attributes the correct stage and repository", () => {
  const previous = global.RESEARCH_UI;
  try {
    global.RESEARCH_UI = {
      project_name: "AstroRef", stage: "Wave 2 — evolving research draft",
      repository_url: "https://github.com/example/astroref",
      feedback_issue_url: "https://github.com/example/astroref/issues/new"
    };
    const correction = feedback.buildIssue({
      kind: "correction", category: "citation",
      definitionId: "preview.term.sample", definitionTerm: "Orbit",
      message: "Source evidence needs verification.",
      stage: "Wave 2 — evolving research draft", projectName: "AstroRef",
      previewUrl: "https://example.org/reconstruction/wave2/"
    });
    assert.match(correction.title, /^\[Wave 2/);
    assert.match(correction.body, /independently reconstructed content, NOT/);
    assert.match(correction.body, /Preview URL: https:\/\/example.org\/reconstruction\/wave2\//);
    assert.match(correction.body, /AstroRef/);
    const u = new URL(feedback.issueUrl({
      kind: "new", term: "Orbital resonance",
      stage: "Wave 1 — frozen baseline", projectName: "AstroRef"
    }));
    assert.equal(u.origin, "https://github.com");
    assert.equal(u.pathname, "/example/astroref/issues/new");
    assert.match(u.searchParams.get("title"), /Wave 1/);
    assert.match(u.searchParams.get("body"), /Wave 1/);

    global.RESEARCH_UI.feedback_issue_url = "https://example.org/other-endpoint";
    assert.throws(() => feedback.issueUrl({kind:"new",term:"Orbit"}), /Invalid configured/);
  } finally {
    if (previous === undefined) delete global.RESEARCH_UI;
    else global.RESEARCH_UI = previous;
  }
});
