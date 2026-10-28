"""Verify complete, immutable mathDef contextual screening inventory."""
from __future__ import annotations
import csv, hashlib, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"research_pipeline/discovery/contextual_review_20261028"
CLASSES={"clear_false_positive","contextual_description","contextual_fragment",
         "legitimate_lead","existing_variant","deeper_research"}

def verify(root=ROOT):
    root=Path(root)
    m=json.loads((root/"manifest.json").read_text(encoding="utf-8"))
    if m.get("rows")!=9071 or len(m.get("parts",[]))!=20:
        raise ValueError("unexpected review count/parts")
    seen_ids=set();seen_phrases=set();counts=Counter();total=0
    for part in m["parts"]:
        filename=part["name"]
        if "/" in filename or not filename.endswith(".tsv"):
            raise ValueError("invalid part name")
        raw=(root/"batches"/filename).read_bytes()
        if (len(raw)!=part["bytes"] or
            hashlib.sha256(raw).hexdigest()!=part["sha256"]):
            raise ValueError("part content changed: "+filename)
        with (root/"batches"/filename).open(encoding="utf-8",newline="") as f:
            rows=list(csv.DictReader(f,delimiter="\t"))
        if len(rows)!=part["records"]:
            raise ValueError("part count changed: "+filename)
        for row in rows:
            ident=row["candidate_id"];phrase=row["phrase"]
            if (not phrase or ident in seen_ids or phrase in seen_phrases or
                ident!="term."+hashlib.sha256(phrase.encode()).hexdigest()[:20]):
                raise ValueError("duplicate/malformed candidate "+ident)
            if row["review_class"] not in CLASSES or not row["source_ids"]:
                raise ValueError("missing disposition or original source")
            seen_ids.add(ident);seen_phrases.add(phrase)
            counts[row["review_class"]]+=1
        total+=len(rows)
    if total!=m["rows"] or dict(counts)!=m["summary"]["counts"]:
        raise ValueError("review coverage/status counts differ from manifest")
    if m["summary"]["classified"]!=9071:
        raise ValueError("review incomplete")
    return {"passed":True,"reviewed":total,"unique_ids":len(seen_ids),
            "counts":dict(sorted(counts.items()))}

if __name__=="__main__":
    print(json.dumps(verify(),indent=2))
