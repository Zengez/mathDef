"use strict";
// End-to-end smoke against the generated merged website in a real headless
// Chromium browser. Exercises *existing* linked definitions only.
const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");
const {chromium} = require(
  process.env.MATHDEF_PLAYWRIGHT_PATH ||
  "/tmp/mathdef-browser-test/node_modules/playwright-core"
);

const root = process.env.MATHDEF_PREVIEW_ROOT || "/tmp/mathdef-merge-check/merged";
const url = process.env.MATHDEF_PREVIEW_URL || "http://127.0.0.1:8765/merged/";
const entries = JSON.parse(fs.readFileSync(path.join(root, "definitions-index.json"), "utf8"));
const lookup = new Map(entries.map((d) => [d.id, d]));

function validAnchoredDependency(group) {
  const siblings = new Set((group.formulations || []).flatMap(
    f => f.dependencies || []).map(dep => dep.id));
  for (const form of group.formulations || []) {
    for (const dep of form.dependencies || []) {
      const target = lookup.get(dep.id);
      if (!target || !(dep.start >= 0)) continue;
      const grandchild = (target.formulations || []).flatMap(f => f.dependencies || [])
        .find(inner => inner.id !== group.id && inner.id !== dep.id &&
                 !siblings.has(inner.id) && inner.start >= 0);
      if (grandchild) return {dep, target, grandchild};
    }
  }
  return null;
}

async function main() {
  const chrome = [
    process.env.CHROME_PATH,
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ].find(x => x && fs.existsSync(x));
  assert(chrome, "Browser smoke requires preinstalled Chrome/Chromium");
  const browser = await chromium.launch({
    headless: true, executablePath: chrome,
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  });
  let result = {};
  try {
    const page = await browser.newPage({viewport: {width: 1320, height: 900}});
    const uncaught = [];
    page.on("pageerror", error => uncaught.push(error.message));
    await page.goto(url, {waitUntil: "domcontentloaded"});
    await page.locator("#total").filter({hasText: String(entries.length)}).waitFor();

    // Independently filtered term and definition search controls.
    await page.locator("#term-query").fill("CW complex");
    await page.locator("#definition-query").fill("weak topology");
    assert.equal(await page.locator("#term-query").inputValue(), "CW complex");
    assert.equal(await page.locator("#definition-query").inputValue(), "weak topology");
    assert((await page.locator("#definition-results button[data-id]").count()) > 0,
           "Definition-content search should include weak-topology references");

    const chosen = entries.map(d => ({d, match:validAnchoredDependency(d)}))
      .find(x => x.match);
    assert(chosen, "Need at least one recursively expandable anchored chain");

    await page.locator("#term-query").fill(chosen.d.term);
    await page.locator('#term-results button[data-id="' + chosen.d.id + '"]').click();
    await page.locator('button[data-explore-mode="inline"]').click();

    const first = page.locator(
      '#term-detail button.inline-cue[data-expand$=">' + chosen.match.dep.id + '"]'
    ).first();
    assert((await first.count()) > 0, "Linked definitions should appear inline");
    await first.click();
    assert((await page.locator("#term-detail .inline-insert").count()) >= 1,
           "Clicking an inline definition link must reveal the child definition");

    const embedded = page.locator("#term-detail .inline-insert button.inline-cue").first();
    assert((await embedded.count()) > 0,
           "Selected nested definition should expose another linked definition");
    if ((await embedded.count()) > 0) {
      await embedded.click();
      assert((await page.locator("#term-detail .inline-insert").count()) >= 1,
             "Nested definition navigation must not crash");
    }

    // A path cannot recursively expand its own original ancestor.
    const original = chosen.d.id;
    const cycle = await page.locator(
      '#term-detail .inline-insert button.inline-cue[data-expand$=">' + original + '"]'
    ).count();
    assert.equal(cycle, 0, "Ancestor term must be suppressed on recursive path");

    await page.setViewportSize({width: 390, height: 844});
    assert((await page.locator("#term-detail article").count()) === 1,
           "Mobile viewport should keep the selected definition visible");
    assert.deepEqual(uncaught, [], "Client-side exceptions should not occur");

    // Controlled three-node graph: A refers to siblings B and C; B also
    // refers to C; C points back to A. Sibling C must be reachable below B,
    // while the ancestor A must not be expandable below A -> B -> C.
    const sample = (id, term, body, links) => {
      const deps = links.map(([targetId, targetTerm]) => {
        const start = body.toLowerCase().indexOf(targetTerm.toLowerCase());
        assert(start >= 0);
        return {
          id: targetId, label: targetTerm,
          formulation: "f." + id, target_meaning: "m." + targetId,
          start, end:start+targetTerm.length,
          review_state:"lexical_candidate", source_phrase:body.slice(start,start+targetTerm.length)
        };
      });
      return {
        id, term, aliases: [], category: "Browser regression", source: "https://example.org",
        status: "screened_draft", body, dependencies: deps, related: [],
        formulations: [{
          key: "f." + id, label: "Browser regression", body,
          meaning_id: "m." + id, dependencies: deps,
          sources: [{title:"Fixture", url:"https://example.org", locator:"https://example.org"}]
        }]
      };
    };
    const synthetic = [
      sample("a", "Alpha concept", "A beta concept and gamma concept.", [
        ["b", "beta concept"], ["c", "gamma concept"]]),
      sample("b", "Beta concept", "A gamma concept and alpha concept.", [
        ["c", "gamma concept"], ["a", "alpha concept"]]),
      sample("c", "Gamma concept", "An alpha concept.", [
        ["a", "alpha concept"]]),
    ];
    const isolated = await browser.newPage({viewport:{width:960,height:780}});
    const isolatedErrors=[];
    isolated.on("pageerror", e => isolatedErrors.push(e.message));
    await isolated.route("**/definitions-index.json", route =>
      route.fulfill({status:200,contentType:"application/json",body:JSON.stringify(synthetic)}));
    await isolated.goto(url,{waitUntil:"domcontentloaded"});
    await isolated.locator("#total").filter({hasText:"3"}).waitFor();
    await isolated.locator("#term-query").fill("Alpha concept");
    await isolated.locator('#term-results button[data-id="a"]').click();
    await isolated.locator('button[data-explore-mode="inline"]').click();
    await isolated.locator('#term-detail button.inline-cue[data-expand="a>b"]').click();
    assert((await isolated.locator('#term-detail button.inline-cue[data-expand="a>b>c"]').count()) > 0,
           "Sibling C must remain expandable beneath sibling B");
    await isolated.locator('#term-detail button.inline-cue[data-expand="a>b>c"]').click();
    assert((await isolated.locator('#term-detail .inline-insert').count()) >= 2,
           "Inline recursive expansion should reach depth two");
    assert.equal(await isolated.locator('#term-detail button[data-expand="a>b>c>a"]').count(),0,
                 "Ancestor A must not reappear after A -> B -> C");
    await isolated.locator('button[data-explore-mode="nested"]').click();
    assert((await isolated.locator('#term-detail button[data-expand="a>b>c"]').count()) > 0,
           "Nested mode should preserve the sibling link");
    assert.deepEqual(isolatedErrors,[]);
    await isolated.close();

    result = {
      name: chosen.d.term,
      first_target: chosen.match.dep.id,
      search_term: "CW complex",
      definition_search: "weak topology",
      recursive_inline_expansion: "passed",
      ancestor_loop_suppression: "passed",
      sibling_reuse_under_another_path: "passed",
      narrow_viewport: "passed",
      uncaught_errors: uncaught.length,
    };
  } finally {
    await browser.close();
  }
  console.log("MERGED_BROWSER_SMOKE_JSON=" + JSON.stringify(result));
}
main().catch(err => {console.error(err); process.exit(1);});
