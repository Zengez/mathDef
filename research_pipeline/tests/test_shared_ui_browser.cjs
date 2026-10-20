/* Read-only Chromium smoke for reusable UI against independent Wave 1/2. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

(async () => {
  const site = path.resolve(process.env.UI_SMOKE_SITE || "/tmp/mathdef-independent-preview");
  const browser = await chromium.launch({headless: true});
  try {
    for (const stage of ["wave1", "wave2"]) {
      const file = path.join(site, stage, "index.html");
      assert.ok(fs.existsSync(file), "Missing independently generated " + stage + " site");
      const page = await browser.newPage({viewport:{width:1320,height:860}});
      const errors = [];
      page.on("pageerror", e=>errors.push(String(e)));
      const base = process.env.UI_SMOKE_BASE;
      const url = base ? base.replace(/\/$/, "") + "/" + stage + "/" : "file://" + file;
      await page.goto(url, {waitUntil:"domcontentloaded"});
      await page.waitForFunction(() => document.querySelector("#total")?.textContent.includes("terms"));
      assert.ok(await page.locator(".masthead .logo").isVisible(), "Original-style logo missing");
      assert.equal(await page.locator(".masthead h1").innerText(), "∈ mathDef");
      assert.match(await page.locator(".subtitle").innerText(), /Explore mathematical language/);
      assert.match(await page.locator(".research-stage-notice").innerText(),
        stage === "wave1" ? /Wave 1/ : /Wave 2/);
      const output = process.env.UI_SMOKE_SCREENSHOTS || "/tmp";
      await page.screenshot({path:path.join(output,"reconstruction-"+stage+"-masthead.png"),fullPage:false});

      // The original-looking suggestion dialog must route reports about
      // independent research to a stage-specific draft, not production data.
      await page.getByRole("button",{name:/Suggest a definition/}).first().click();
      assert.ok(await page.locator("#feedback-dialog").evaluate(el=>el.open));
      await page.locator("#feedback-term").fill("Independent test term");
      await page.locator(".feedback-prepare").click();
      const draft = await page.locator("#feedback-github-link").getAttribute("href");
      assert.ok(draft && draft.startsWith("https://github.com/Zengez/mathDef/issues/new?"));
      const draftUrl = new URL(draft);
      assert.match(draftUrl.searchParams.get("title"), stage==="wave1" ? /Wave 1/ : /Wave 2/);
      assert.match(draftUrl.searchParams.get("body"), /independently reconstructed content, NOT/);
      await page.locator("#feedback-close").click();

      assert.equal(await page.locator(".search-box").count(), 2);
      assert.ok((await page.locator(".pane").count()) === 2);
      await page.locator("#term-query").fill("Galois field extension");
      const matches = page.locator("#term-results .result");
      assert.ok(await matches.count() >= 1);
      await matches.first().click();
      assert.ok(await page.locator("#term-detail .definition").count() >= 1);
      assert.ok(await page.locator("#term-detail .source-links a[href^='https://']").count() >= 1,
        "Independent formulation-level sources unavailable");
      await page.locator("#definition-query").fill("field extension");
      assert.ok((await page.locator("#definition-results .result").count()) >= 1,
        "Content-only search missing independently acquired evidence");
      await page.locator("#focus").click();
      assert.ok(await page.locator("#workspace").evaluate(el=>el.classList.contains("focused")));
      await page.locator("#split").click();
      await page.locator("[data-explore-mode='inline']").click();
      await page.locator("[data-explore-mode='nested']").click();
      await page.locator("#term-query").fill("symmetric monoidal category");
      const sym = page.locator("#term-results .result");
      if (await sym.count()) {
        await sym.first().click();
        const toggle = page.locator("#term-detail button[data-expand]").first();
        if (await toggle.count()) {
          await toggle.click();
          assert.ok((await page.locator("#term-detail .dependency-content").count()) > 0,
            "Recursive independent relation did not expand");
        }
      }
      await page.setViewportSize({width:375,height:810});
      const overflow = await page.evaluate(()=>({
        width:innerWidth,doc:document.documentElement.scrollWidth
      }));
      assert.ok(overflow.doc <= overflow.width + 4,
        "Horizontal mobile overflow: " + JSON.stringify(overflow));
      await page.setViewportSize({width:1320,height:860});
      await page.screenshot({path:path.join(output, "reconstruction-"+stage+".png"),fullPage:false});
      assert.deepEqual(errors,[], "UI runtime console errors");
      await page.close();
    }
    console.log("Reusable reconstruction GUI smoke passed for frozen Wave 1 and unsealed Wave 2");
  } finally {
    await browser.close();
  }
})().catch(err=>{console.error(err);process.exit(1);});
