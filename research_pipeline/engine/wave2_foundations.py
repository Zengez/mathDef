"""First Wave 2 foundation intake: source locators plus one directly verified definition.

This is deliberately NOT an automatic dictionary fill. Encyclopedia of
Mathematics entries were independently discovered through public search, but
several direct page fetches returned 502. Those leads are kept as term/locator
leads ONLY, not promoted into mathematical observations or screened definitions.
The Stacks tag 00OD was directly read and is accepted as paraphrase evidence.
"""
import argparse
import json
from pathlib import Path
from .core import Workspace, PipelineError, atomic_json, canonical

LEADS = (
    ("group", "group", "src.eom", "https://encyclopediaofmath.org/index.php?title=Group", "indexed_only_not_directly_verified"),
    ("abelian-group", "abelian group", "src.eom", "https://encyclopediaofmath.org/wiki/Abelian_group", "direct_fetch_failed_502"),
    ("ring", "ring", "src.eom", "https://encyclopediaofmath.org/wiki/Ring", "indexed_only_not_directly_verified"),
    ("ring-ideal", "ideal of a ring", "src.eom", "https://encyclopediaofmath.org/wiki/Ideal", "indexed_only_not_directly_verified"),
    ("prime-ideal-commutative", "prime ideal of a commutative ring", "src.eom", "https://encyclopediaofmath.org/wiki/Prime_ideal%282%29", "indexed_only_not_directly_verified"),
    ("module-left", "left module over a ring", "src.eom", "https://encyclopediaofmath.org/wiki/Module", "direct_fetch_failed_502"),
    ("category", "category", "src.eom", "https://encyclopediaofmath.org/wiki/Category", "direct_fetch_failed_502"),
    ("topological-space", "topological space", "src.eom", "https://encyclopediaofmath.org/wiki/Topological_space", "indexed_only_not_directly_verified"),
    ("regular-noetherian-ring", "regular Noetherian ring", "src.stacks", "https://stacks.math.columbia.edu/tag/00OD", "direct_page_read")
)

def run(workspace):
    w = Workspace(workspace)
    baseline = w.root / "state/baseline.json"
    if not baseline.exists() or json.loads(baseline.read_text())["mode"] != "second_wave":
        raise PipelineError("Wave 2 foundation intake must run on a genuine fork")
    for stage in ("terms","observations"):
        if w.state(stage).get("sealed"):
            raise PipelineError("Wave 2 term/content stage already sealed")
    src = w.records("sources")
    existing = w.records("terms")
    leads, terms = [], []
    for key, label, source_id, url, outcome in LEADS:
        assert source_id in src and src[source_id]["authority_reviewed"]
        assert src[source_id]["access"] == "free" and src[source_id]["rights"] == "locator_only"
        term = {"id": "term.wave2." + key, "label": label,
                "source_id": source_id, "locator": url,
                "discovery_provenance": "wave2_independent_public_source_discovery_2026_10_19",
                "human_verified": False}
        if term["id"] in existing and term != existing[term["id"]]:
            raise PipelineError("Attempt to silently revise existing Wave 2 term " + term["id"])
        terms.append(term)
        leads.append({
            "term_id": term["id"], "label": label, "source_id": source_id,
            "url": url, "source_access_outcome": outcome,
            "substantive_observation_created": outcome == "direct_page_read",
            "review_state": "source_research_lead",
            "editorial_note": ("Permanent Stacks Project Definition 10.110.7 read and "
                               "checked for scope: regular Noetherian rings are "
                               "characterized by regularity of all prime localizations."
                               if outcome == "direct_page_read" else
                               "Public search index established this encyclopedia term and "
                               "article locator. Full text not directly verified; do NOT "
                               "count as an acquired mathematical definition or claim "
                               "a completed source review."),
            "human_verified": False
        })
    out = w.root / "intake/foundations_batch_01_terms.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(canonical(row)+"\n" for row in terms)
    if out.exists() and out.read_text() != text:
        raise PipelineError("Changed immutable foundation intake file")
    out.write_text(text, encoding="utf-8")
    term_result = w.ingest("terms", out, batch_size=3)

    regular_term = next(x for x in terms if x["id"] == "term.wave2.regular-noetherian-ring")
    observation = {
        "id":"obs.wave2.regular-noetherian-ring.stacks-00od",
        "term_id":regular_term["id"], "source_id":regular_term["source_id"],
        "locator":regular_term["locator"], "record_kind":"paraphrase",
        "text":("A Noetherian ring R is regular if, for every prime ideal p of R, "
                "the localization R_p is a regular local ring."),
        "context":"Commutative algebra, Noetherian rings",
        "source_definition":"Stacks Project Definition 10.110.7 (tag 00OD)",
        "editorial_note":"Independently paraphrased after directly reading the Stacks definition; candidate evidence, not a refereed or sealed mathematical meaning.",
        "reviewed_by":"assistant_independent_source_read_2026_10_19",
        "human_verified":False
    }
    data_path = w.root / "intake/foundations_batch_01_observations.jsonl"
    row_text=canonical(observation)+"\n"
    if data_path.exists() and data_path.read_text() != row_text:
        raise PipelineError("Changed immutable observation intake file")
    data_path.write_text(row_text, encoding="utf-8")
    observation_result = w.ingest("observations", data_path, batch_size=1)

    notes_path = w.root / "wave2/foundation_source_discovery_batch_01.jsonl"
    notes_text="".join(canonical(x)+"\n" for x in leads)
    if notes_path.exists() and notes_path.read_text() != notes_text:
        raise PipelineError("Changed previously recorded source audit")
    notes_path.write_text(notes_text,encoding="utf-8")
    result={
      "state":"first_source_recovery_batch_completed_unsealed",
      "catalog_sources_reused":2,
      "new_term_locators":len(terms),
      "term_count_after_intake":len(w.records("terms")),
      "new_authored_mathematical_observations":1,
      "observation_count_after_intake":len(w.records("observations")),
      "idempotent_replay_skips":{
          "term_records_already_present":term_result["already_present"],
          "observation_records_already_present":observation_result["already_present"]
      },
      "directly_read_and_source_checked":1,
      "discovered_via_search_only_not_verified":8,
      "of_those_direct_fetch_returned_502":3,
      "remaining_direct_page_checks_needed":8,
      "all_wave2_stages_still_unsealed":True,
      "published_as_screened_definition":False,
      "original_mathdef_corpus_read":False,
      "next":"Individually verify eight remaining source pages or seek alternate accessible references; acquire reviewed evidence before grouping new meanings.",
    }
    if len(w.records("terms")) != 327 or len(w.records("observations")) != 750:
        raise PipelineError("Unexpected Wave 2 counts; audit for duplicate/dropped terms")
    if any(w.state(st).get("sealed") for st in
           ("sources","terms","observations","meanings","relations")):
        raise PipelineError("Premature Wave 2 stage seal")
    atomic_json(w.root / "state/wave2_foundations_batch_01.json", result)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,required=True)
    x=p.parse_args()
    print(json.dumps(run(x.workspace),ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
