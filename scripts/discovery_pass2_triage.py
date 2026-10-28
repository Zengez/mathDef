#!/usr/bin/env python3
"""Conservative, non-destructive Pass 2 triage of high-recall mathDef leads.

Input is the durable discovery checkpoint (not a newly extracted corpus).
A lexical filter can identify malformed fragments but cannot establish whether
a phrase is a valid mathematical term. All ambiguous cases remain reviewable.
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

SCHEMA = "mathdef.discovery-pass2-triage.v1"
FUNCTION_WORDS = frozenset("""
a an the and or but if then than that which where whose who whom when
with without from into onto over under between within through across along
for of to in on at by as is are was were be been being has have had
it its their these those this there here each every any some all
such let suppose assume given consider called defined means denote
""".split())
PRONOUNS = frozenset("we our you your they them he she his her".split())
VERBS = frozenset("""
satisfies satisfy contains contain consists consist exists exist follows
follow implies imply yields yield holds hold forms form becomes become
induces induce admits admit defines define generates generate
is are was were has have had can may must should will
""".split())
GENERIC_ENDINGS = frozenset("thing example case result way type kind".split())

def classify(phrase):
    words = phrase.split()
    if not 2 <= len(words) <= 5:
        return "higher_thinking_review", "unusual phrase length"
    if any(len(w) == 1 for w in words):
        return "likely_false_positive", "isolated single-letter token"
    if words[0] in FUNCTION_WORDS:
        return "likely_false_positive", "begins with grammatical connector"
    if words[-1] in FUNCTION_WORDS or words[-1] in GENERIC_ENDINGS:
        return "likely_false_positive", "ends with grammatical connector or generic prose"
    if any(w in PRONOUNS for w in words):
        return "likely_false_positive", "contains a prose pronoun"
    if any(w in VERBS for w in words):
        return "likely_false_positive", "contains finite prose verb"
    if any(w in FUNCTION_WORDS for w in words[1:-1]):
        return "higher_thinking_review", "internal grammatical connector; could be a named term"
    if len(words) >= 4:
        return "higher_thinking_review", "long compound; needs contextual mathematical judgment"
    return "plausible_term_review", "lexically plausible term; mathematical validation needed"

def run(checkpoint, output):
    state = json.loads(Path(checkpoint).read_text(encoding="utf-8"))
    if state.get("schema") != "mathdef.discovery-checkpoint.v1":
        raise ValueError("Expected durable canonical discovery checkpoint")
    # Deduplicate by normalized phrase across all source formulations.
    leads = {}
    for fid, form in state["formulations"].items():
        for phrase, n in form["phrase_counts"].items():
            record = leads.setdefault(phrase, {"phrase":phrase,"occurrences":0,
                "formulation_count":0,"examples":[]})
            record["occurrences"] += n
            record["formulation_count"] += 1
            if len(record["examples"]) < 3:
                record["examples"].append({"formulation_id":fid,
                    "group_id":form["group_id"],"group_title":form["group_title"]})
    # The seen-leads registry is the high-recall candidate set. Do not
    # classify already-defined phrases as new candidate terms.
    known_leads = set(state["seen_leads"])
    if not known_leads:
        raise ValueError("No candidate inventory in discovery checkpoint")
    missing = known_leads - leads.keys()
    results=[]
    for phrase in sorted(known_leads & leads.keys()):
        entry = leads[phrase]
        status, reason = classify(phrase)
        results.append({**entry,"triage":status,"reason":reason,
                        "mathematically_validated":False,"editorial_rejection":False})
    counts=Counter(x["triage"] for x in results)
    output=Path(output)
    output.mkdir(parents=True,exist_ok=True)
    with (output/"pass2_triage.tsv").open("w",encoding="utf-8",newline="") as file:
        writer=csv.writer(file,delimiter="\t")
        writer.writerow(["phrase","triage","reason","occurrences","formulation_count","source_formulations"])
        for x in results:
            writer.writerow([x["phrase"],x["triage"],x["reason"],x["occurrences"],
                             x["formulation_count"],
                             "|".join(y["formulation_id"] for y in x["examples"])])
    for kind in ("higher_thinking_review","plausible_term_review","likely_false_positive"):
        with (output/(kind+".tsv")).open("w",encoding="utf-8",newline="") as file:
            writer=csv.writer(file,delimiter="\t")
            writer.writerow(["phrase","reason","occurrences","source_formulations"])
            for x in results:
                if x["triage"]==kind:
                    writer.writerow([x["phrase"],x["reason"],x["occurrences"],
                        "|".join(y["formulation_id"] for y in x["examples"])])
    summary={"schema":SCHEMA,"input":"durable discovery-checkpoints branch",
             "source_formulations":len(state["formulations"]),
             "previously_encountered_leads":len(known_leads),
             "triaged_active_leads":len(results),
             "historical_leads_no_longer_in_active_corpus":len(missing),
             "counts":dict(sorted(counts.items())),
             "notes":["This is conservative lexical triage, not mathematical validation.",
                      "Likely false positives are NOT editorially rejected or removed.",
                      "Ambiguous and long phrases are flagged for higher-thinking review.",
                      "No definition, checkpoint, or editorial decision is changed."]}
    (output/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return summary

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--checkpoint",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    run(a.checkpoint,a.output)
