/* Optional portable browser integration: synthetic catalogs only, no frozen data.
 * PLAYWRIGHT_CHROMIUM_EXECUTABLE=/usr/bin/chromium node this-file.cjs
 */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const http = require("node:http");
const os = require("node:os");
const path = require("node:path");
const {spawnSync} = require("node:child_process");
const {chromium} = require("playwright");

(async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "reference-browser-"));
  let browser, server;
  try {
    const built = spawnSync("python", ["-c", `
import sys
from pathlib import Path
from research_pipeline.tests.test_reference_ui import ReferenceUITests
from research_pipeline.ui.renderer import render
fixture=ReferenceUITests(); fixture.setUp()
try:
    for stage in ('wave1','wave2'):
        render(fixture.root/'catalog.json',fixture.root/'brand.json',Path(sys.argv[1])/stage,
               stage+' synthetic fixture','Software fixture; no frozen records read.')
finally:
    fixture.doCleanups()
`, root], {cwd:path.resolve(__dirname, "../.."), encoding:"utf8"});
    assert.equal(built.status, 0, built.stderr);
    server = http.createServer((req,res) => {
      const relative = decodeURIComponent(new URL(req.url,"http://localhost").pathname);
      const file = path.resolve(root,"." + relative + (relative.endsWith("/") ? "index.html" : ""));
      if (!file.startsWith(root + path.sep)) { res.writeHead(403); res.end(); return; }
      fs.readFile(file,(error,bytes) => {
        if (error) { res.writeHead(404); res.end(); return; }
        const mime={".html":"text/html", ".json":"application/json", ".js":"text/javascript", ".css":"text/css"};
        res.writeHead(200,{"Content-Type":mime[path.extname(file)] || "application/octet-stream"});res.end(bytes);
      });
    });
    await new Promise(resolve=>server.listen(0,"127.0.0.1",resolve));
    const base="http://127.0.0.1:"+server.address().port+"/";
    browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || undefined});
    for (const stage of ["wave1","wave2"]) {
      const page=await browser.newPage({viewport:{width:1320,height:860}});
      const errors=[];page.on("pageerror",e=>errors.push(String(e)));
      await page.route("**/*",r=>r.request().url().startsWith(base)?r.continue():r.abort());
      await page.goto(base+stage+"/");
      await page.waitForFunction(()=>document.querySelector("#total")?.textContent.includes("definitions"));
      assert.equal(await page.locator(".search-box").count(),2);
      await page.locator("#term-query").fill("Orbit");
      await page.locator("#term-results .result").first().click();
      assert.match(await page.locator("#term-detail").innerText(),/gravitational trajectory/);
      assert.match(await page.locator("#term-detail").innerText(),/Iterates of a transformation/);
      assert.ok(await page.locator("#term-detail .source-links a").count()>=2);
      await page.locator("#definition-query").fill("transformation");
      assert.equal(await page.locator("#definition-results .result").count(),1);
      await page.locator("#term-query").fill("Planet");
      await page.locator("#term-results .result").first().click();
      for (const mode of ["inline","nested"]) {
        await page.locator(`[data-explore-mode='${mode}']`).click();
        const toggle=page.locator("#term-detail button[data-expand]").first();
        if (await toggle.getAttribute("aria-expanded")==="false") await toggle.click();
        assert.match(await page.locator("#term-detail").innerText(),/gravitational trajectory/);
      }
      await page.locator("#focus").click();
      assert.ok(await page.locator("#workspace").evaluate(e=>e.classList.contains("focused")));
      await page.locator("#split").click();
      await page.getByRole("button",{name:/Suggest/}).first().click();
      assert.ok(await page.locator("#feedback-dialog").evaluate(e=>e.open));
      await page.locator("#feedback-cancel").click();
      await page.setViewportSize({width:375,height:810});
      const [width,content]=await page.evaluate(()=>[innerWidth,document.documentElement.scrollWidth]);
      assert.ok(content<=width+4);
      assert.deepEqual(errors,[]);
      await page.close();
    }
    console.log("PASS: both synthetic stage previews; searches, contexts, sources, nested/inline, feedback and mobile. External requests blocked.");
  } finally {
    if (browser) await browser.close();
    if (server) await new Promise(resolve=>server.close(resolve));
    fs.rmSync(root,{recursive:true,force:true});
  }
})().catch(error=>{console.error(error);process.exit(1);});
