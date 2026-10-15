# arXiv definition harvesting

arXiv papers often contain explicitly labeled definitions in LaTeX theorem environments.
MathDef now supports per-paper provenance in curated definition files:

- source: canonical arXiv abstract-page URL
- arxiv: inspected paper ID and version (for example, 2406.02401v2)
- locator: numbered definition and printed page (for example, Definition 2.1, p. 6)
- source_title: full research-paper title
- status: draft until mathematical review

## Candidate scanner

Run from the repository root with Python 3.10+:

    python3 scripts/arxiv_candidate_scan.py --category math.DS --max-papers 12
    python3 scripts/arxiv_candidate_scan.py --id 2406.02401 --id 2511.16503
    python3 scripts/arxiv_candidate_scan.py --id 2406.02401 --source downloaded-source.tar.gz

The default local output is _arxiv_candidates.csv. This is a metadata-only inventory:
paper ID, title, LaTeX filename, line, definition environment, optional heading, SHA-256
hash of the body, character count, and link to the paper. It does not write definition
prose to disk and never automatically publishes candidates into the website.

The scanner checks LaTeX definition and defn environments, including names from
newtheorem declarations. It cannot detect every prose definition or unusual macro.
Source-only papers, alternative source formats, and PDF-only papers may require
manual review. An extracted candidate is not proof of mathematical correctness.

## Responsible access and acceptance

arXiv's API terms request at least three seconds between legacy requests. This
scanner uses a minimum 3.2-second interval, the dedicated export.arxiv.org host,
download and in-memory archive size limits, and no filesystem extraction.
For massive retrospective corpora, use arXiv's documented bulk S3 approach rather
than attempting to scrape the entire archive through its legacy API.

Accept a candidate only after reading the relevant paper context. Identify
hypotheses, nonstandard conventions, and whether the author is introducing a
paper-specific term. Write independent LaTeX prose rather than republishing text.
Record the exact paper version and Definition number/page; preserve existing IDs
and ensure linked related IDs exist. Keep status draft pending individual review.

References: https://info.arxiv.org/help/api/tou.html
and https://info.arxiv.org/help/bulk_data/index.html

Thank you to arXiv for use of its open access interoperability.

## Remote candidate scans

Open GitHub Actions, select Scan arXiv definition candidates, and choose Run workflow.
Set a mathematics category such as math.DS and a conservative number of papers.
The workflow saves a downloadable artifact called arxiv-definition-candidates.
Nothing is added automatically to the definitions folder, and no schedule runs.

Some PDF-only or non-TeX source articles cannot be parsed by this method.
Review the logs if an individual source fetch fails or if no candidates are found.
Offline scanner unit tests do not verify live arXiv download availability.

## First successful source-scan trial

The October 15, 2026 math.DS trial inspected 12 recent papers and located 30 explicit LaTeX definition candidates in 7 of them; see [run 38797055015](https://github.com/Zengez/mathDef/actions/runs/38797055015) for the locator-only CSV artifact. Six entries in `definitions/solenoids/` were added only after manual inspection of Hurder and Lukina, [arXiv:2610.20131](https://arxiv.org/abs/2610.20131). The current arXiv-derived collection is 28 independently worded draft definitions from six research papers. The trial does not claim a comprehensive crawl of arXiv, and its candidate counts are not accepted-definition counts.
