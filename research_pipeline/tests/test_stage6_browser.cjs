/* Browser-only Stage 6 smoke test. Run against the isolated experiment preview,
 * never against production mathDef. No forms or GitHub issues are submitted.
 */
"use strict";
const assert = require("node:assert/strict");
const path = require("node:path");
const fs = require("node:fs");
const { chromium } = require("playwright");

(async () => {
  const root = path.resolve("research_pipeline/experiments/reconstruction-v1-recovery/preview");
  const html = path.join(root, "index.html");
  assert.ok(fs.existsSync(html), "Build independent Stage 6 preview first");
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1260, height: 830 } });
    const errors = [];
    page.on("pageerror", e => errors.push(String(e)));
    await page.goto("file://" + html, { waitUntil: "domcontentloaded" });
    await page.locator("#term").fill("unique factorization domain");
    assert.deepEqual(await page.locator("article h2").allTextContents(), ["unique factorization domain"],
      "Term-only search must not return unrelated concepts from its source section");
    await page.getByRole("button", { name: "View sources" }).first().click();
    assert.ok(await page.locator("#sources").evaluate(dialog => dialog.open), "Source modal failed to open");
    assert.ok((await page.locator("#sources-content a").count()) >= 1, "Missing source reference in modal");
    await page.locator("#sources form button").click();

    await page.locator("#term").fill("symmetric monoidal category");
    assert.ok((await page.locator("article h2").allTextContents()).includes("symmetric monoidal category"));
    const expand = page.getByRole("button", { name: /^Expand monoidal category/ }).first();
    assert.ok(await expand.isVisible(), "Expected source-defined monoidal dependency");
    await expand.click();
    assert.ok((await page.locator(".recursive-meaning").count()) >= 1, "Recursive explanation did not render");
    await page.getByRole("button", { name: /^Collapse monoidal category/ }).first().click();
    assert.equal(await page.locator(".recursive-meaning").count(), 0, "Collapse left descendants visible");

    await page.locator("#term").fill("formally étale ring map");
    assert.ok((await page.locator("article h2").allTextContents()).includes("formally étale ring map"));
    assert.ok((await page.getByRole("button", { name: /^Implies: / }).count()) >= 2,
      "Implications must be navigational rather than recursively expanded as prerequisites");

    await page.locator("#term").fill("");
    await page.locator("#definition").fill("transcendence basis");
    assert.ok((await page.locator("article").count()) > 0, "Definition-only search returned nothing");
    await page.locator("#definition").fill("");
    await page.locator("#term").fill("function");
    await page.locator("#term").fill("projective module");
    assert.ok((await page.locator("article").count()) > 0, "Term filtering stopped working");

    await page.getByRole("button", { name: "Propose verification" }).first().click();
    assert.ok(await page.locator("#verify").evaluate(dialog => dialog.open), "Verification dialog did not open");
    await page.locator("#verify form button").click();

    await page.locator("#term").fill("affine scheme");
    const screenshot = process.env.STAGE6_SCREENSHOT || "/tmp/mathdef-stage6-browser-smoke.png";
    await page.screenshot({ path: screenshot, fullPage: false });
    assert.deepEqual(errors, [], "Browser JavaScript errors during smoke tests");
    console.log(JSON.stringify({
      status: "passed",
      checks: ["term-only search", "distinct source-section meanings", "source modal",
        "nested recursive expansion", "collapse", "implication treatment",
        "definition-text search", "verification dialog", "no JavaScript exceptions"],
      screenshot
    }, null, 2));
  } finally {
    await browser.close();
  }
})().catch(err => { console.error(err); process.exit(1); });
