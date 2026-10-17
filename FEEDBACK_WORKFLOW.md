# Community feedback and editorial review

**First release (October 2026):** mathDef supports suggestions from the site. A visitor can propose a missing mathematical term (optionally supplying a definition), suggest corrections to any main/nested/In-Line definition, or flag a particular automatically generated source-to-target definition link.

## Visitor workflow

1. Use **+ Suggest a definition** next to term search to request a missing entry. The mathematical term is required; subject area, proposed definition, additional context and source URL are optional.
2. Use **Suggest correction** on the selected definition or **Correct** on a recursively expanded definition. The relevant stable definition ID and source filename are supplied automatically.
3. Use **⚑ Report link** beside a nested header or an In-Line definition cue to report a bad link. The suggestion records the precise source ID, target ID and matched phrase, and preselects "Incorrect or unnecessary definition link." To request a missing link, choose that category on the source definition's correction form.
4. Optional **Attribution name or ID** is included in the public issue only if the contributor explicitly selects **Include this name publicly in the suggestion**. GitHub inherently displays the username of whoever actually creates the issue; attribution cannot be anonymous under this first GitHub-only implementation.
5. The visitor selects **Prepare suggestion**, then **Review & submit on GitHub**. The site opens a prefilled GitHub Issue. The visitor must **log in and click GitHub's Submit new issue**; preparing a draft on mathDef does *not* submit it.

The issue URL contains the submitted text and may be recorded by browser history and normal GitHub behavior. The form warns people not to include secrets or personal details. No site-side database, GitHub token, or upload API is required for this version.

**Feedback is not automatically accepted or applied.** This is a request/review mechanism, not a public editing interface. The browser never changes the repository's definitions, citations, or link overrides.

## The review queue

GitHub Issues is the initial persistent public queue:

- [Open suggestions](https://github.com/Zengez/mathDef/issues?q=is%3Aissue%20is%3Aopen)
- Definition proposals have titles beginning **[Definition request]**.
- Corrections have titles beginning **[Definition correction]**, and the issue body records the type, stable ID, relevant source, and any reported dependency pair.

The queue is readable by maintainers and by connected tooling including ChatGPT's GitHub integration, and GitHub itself preserves authorship, comments, status, and discussions. At review, verify the mathematical statement against the cited material and check existing definitions/aliases before creating an entry.

Suggested disposition workflow:

1. **Triage:** identify the intended entry and decide whether the report is a duplicate, mathematical error, citation issue, incorrect/missing link, or new topic.
2. **Discuss/verify:** record evidence, alternative conventions and any disagreements in comments; ask clarifying questions where essential.
3. **Resolve:** for a real mathematical or citation correction, edit the corresponding definition and cite authoritative sources; for link feedback, edit [data/link_overrides.json](data/link_overrides.json) using the reported source/target IDs, and rebuild.
4. **Close** with a reason: accepted (link relevant commit), revised (explain adjustment), rejected (explain why), or deferred (leave open or label with rationale). Review labels are optional, and we have not automated maintainer judgments.
5. For later archival/reporting, export review records to Markdown in the repo if desired. GitHub Issues themselves are currently the durable source of truth.

## Account-free submissions: deliberately deferred

The form and eventual review process are separated from GitHub login. **At present, submission requires a GitHub account**, because GitHub Issues cannot be posted to anonymously from a GitHub Pages static site. Providing unauthenticated intake safely would require a trusted external endpoint or form service, rate limiting, spam protection and a way to insert items into the queue without exposing a write token. Future versions may support this, optionally allowing contributors to enter a public attribution name/ID; until then, the optional field is only an *additional* public credit on GitHub-authored issues.

## Files and testing

- [web/feedback.js](web/feedback.js): pure Markdown-issue builder and GitHub URL preparation, plus the dialog controller.
- [web/index.html](web/index.html) and [web/styles.css](web/styles.css): accessible dialog and suggestion controls.
- [web/app.js](web/app.js): correction and link-report actions on all definition contexts.
- [tests/test_feedback.cjs](tests/test_feedback.cjs): checks source/target IDs, URL encoding, new-term optional fields, correction validation, and explicit attribution consent.
- [DEPENDENCY_LINKING.md](DEPENDENCY_LINKING.md): current automatic-linking and link-override process.

The static build validates JavaScript syntax and tests, but visual browser QA and a real end-to-end issue submission by a consenting GitHub user are separate checks. Do not create test issues that would be mistaken for genuine community suggestions.
