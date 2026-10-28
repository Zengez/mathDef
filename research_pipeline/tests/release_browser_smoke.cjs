"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const {chromium}=require(process.env.MATHDEF_PLAYWRIGHT_PATH ||
  "/tmp/mathdef-browser-test/node_modules/playwright-core");
const root=process.env.MATHDEF_PREVIEW_ROOT || "_site";
const url=process.env.MATHDEF_PREVIEW_URL || "http://127.0.0.1:8765/";
const data=JSON.parse(fs.readFileSync(path.join(root,"definitions-index.json"),"utf8"));
const sources=JSON.parse(fs.readFileSync(path.join(root,"sources-index.json"),"utf8"));
assert(data.length>0,"Release has no term groups");
assert.equal(sources.groups.length,data.length);
const chrome=["/usr/bin/google-chrome","/usr/bin/google-chrome-stable",
  "/usr/bin/chromium","/usr/bin/chromium-browser"].find(fs.existsSync);
assert(chrome,"Chrome/Chromium browser must be available for release");
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:chrome,
  args:["--no-sandbox","--disable-dev-shm-usage"]});
try {
 const page=await browser.newPage({viewport:{width:1280,height:860}});
 let errors=[];
 page.on("pageerror",e=>errors.push(e.message));
 await page.goto(url,{waitUntil:"domcontentloaded"});
 await page.locator("#total").filter({hasText:String(data.length)}).waitFor();
 assert.equal(await page.locator('button[data-explore-mode="inline"]')
   .getAttribute("aria-pressed"),"true");
 // Both search fields filter independently.
 await page.locator("#term-query").fill("Basis");
 await page.locator("#definition-query").fill("topology");
 assert(await page.locator("#term-results [data-id]").count()>0);
 assert(await page.locator("#definition-results [data-id]").count()>0);
 const group=data.find(d=>d.formulations.length>1 &&
   sources.groups.find(s=>s.group_id===d.id)?.source_ids.length);
 assert(group,"At least one term with multiple source-attributed formulations");
 await page.locator("#term-query").fill(group.term);
 await page.locator('#term-results button[data-id="'+group.id+'"]').click();
 await page.locator('#term-detail button[data-show-sources="'+group.id+'"]')
   .first().click();
 await page.locator("#sources-dialog[open]").waitFor();
 await page.locator("#sources-content .sources-meaning").first().waitFor();
 assert(await page.locator("#sources-content .sources-formulation").count()>=2);
 // The Sources correction form preselects the citation category.
 await page.locator("#sources-correct").click();
 await page.locator("#feedback-dialog[open]").waitFor();
 assert.equal(await page.locator("#feedback-category").inputValue(),"citation");
 await page.locator("#feedback-close").click();
 // Scoped source panels isolate a single formulation.
 const scoped=page.locator('#term-detail button[data-source-formulation]').first();
 await scoped.click();
 await page.locator("#sources-dialog[open]").waitFor();
 await page.locator("#sources-content .sources-formulation").first().waitFor();
 assert.equal(await page.locator("#sources-content .sources-formulation").count(),1);
 await page.locator("#sources-done").click();
 // Inline and nested paths and scoped presentation remain functional.
 await page.locator('button[data-explore-mode="nested"]').click();
 assert(await page.locator("#term-detail article").count()===1);
 await page.locator('button[data-explore-mode="inline"]').click();
 await page.setViewportSize({width:390,height:844});
 await page.locator('#term-detail button[data-show-sources="'+group.id+'"]').first().click();
 await page.locator("#sources-dialog[open]").waitFor();
 assert(await page.locator("#sources-content .sources-meaning").count()>0);
 await page.locator("#sources-done").click();
 assert.deepEqual(errors,[],"No browser JavaScript exceptions");
 console.log("RELEASE_BROWSER_SMOKE=PASSED "+JSON.stringify({groups:data.length,
   sources:sources.groups.length,selected:group.term,jsErrors:errors.length}));
} finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1});
