#!/usr/bin/env python3
"""Validate exact source provenance, coverage, and partition integrity."""
from pathlib import Path
import collections,csv,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'research_pipeline/discovery/targeted_technical_review_20261028'
SRC=ROOT/'research_pipeline/discovery/independent_term_review_20261028/survivor_batches'
SRC_CONTEXT=ROOT/'research_pipeline/discovery/contextual_review_20261028/batches'
ACTIVE_CLASSES={'recognizable_technical_term','possible_independent_term','requires_deeper_research'}
ALL_CLASSES=ACTIVE_CLASSES|{'descriptive_not_separate_term','false_positive','term_variant'}

def parse_folder(folder):
    out=[]
    for path in sorted(folder.glob('*.tsv')):
        with path.open(encoding='utf-8',newline='') as handle:
            out.extend(csv.DictReader(handle,delimiter='\t'))
    return out

def verify(root=ROOT):
    root=Path(root)
    base=root/'research_pipeline/discovery/targeted_technical_review_20261028'
    m=json.loads((base/'manifest.json').read_text(encoding='utf-8'))
    if m['schema']!='mathdef.targeted-technical-review-state.v1':raise ValueError('schema')
    if m['review_input']!=2175 or m['active_research']!=1148:raise ValueError('unexpected review scope')
    for folder,key in [('decisions','decisions'),('active','active')]:
        for x in m[key]:
            file=base/folder/x['name']
            data=file.read_bytes()
            if len(data)!=x['bytes'] or hashlib.sha256(data).hexdigest()!=x['sha256']:
                raise ValueError('corrupt batch '+str(file))
            with file.open(encoding='utf8',newline='') as handle:
                n=sum(1 for _ in csv.DictReader(handle,delimiter='\t'))
            if n!=x['records']:raise ValueError('row count '+str(file))
    rows=parse_folder(base/'decisions');act=parse_folder(base/'active')
    if len(rows)!=2175 or len(act)!=1148:raise ValueError('incomplete review')
    ids=[r['candidate_id'] for r in rows];activeids=[r['candidate_id'] for r in act]
    if len(set(ids))!=2175 or len(set(activeids))!=1148:raise ValueError('duplicate ids')
    if hashlib.sha256('\n'.join(sorted(ids)).encode()).hexdigest()!=m['original_candidate_ids_sha256']:
        raise ValueError('changed candidate population')
    if hashlib.sha256('\n'.join(sorted(activeids)).encode()).hexdigest()!=m['active_ids_sha256']:
        raise ValueError('changed active population')
    counts=dict(sorted(collections.Counter(r['review_status'] for r in rows).items()))
    if counts!=m['counts'] or set(counts)!=ALL_CLASSES:raise ValueError('status counts')
    expected={r['candidate_id'] for r in rows if r['review_status'] in ACTIVE_CLASSES}
    if expected!=set(activeids):raise ValueError('active queue mismatch')
    input_candidates=[r for r in parse_folder(root/'research_pipeline/discovery/independent_term_review_20261028/survivor_batches') if r['disposition']=='needs_targeted_review']
    if {r['candidate_id'] for r in input_candidates}!=set(ids) or len(input_candidates)!=2175:
        raise ValueError('review inputs differ from original 2175 cases')
    original_sourceids={r['candidate_id']:r['source_ids'] for r in input_candidates}
    original_context={r['candidate_id']:r for r in parse_folder(root/'research_pipeline/discovery/contextual_review_20261028/batches')}
    for row in rows:
        ident=row['candidate_id']
        if not row['phrase'] or not row['reason_code'] or not row['source_ids'] or row['source_ids']!=original_sourceids[ident]:
            raise ValueError('missing reason or source mismatch '+ident)
        if not row['source_titles'] or not row['source_snippets'] or row['source_titles']!=original_context[ident]['source_titles']:
            raise ValueError('missing original mathematical context '+ident)
        if row['source_feed_sha256']!=m['source_feed_sha256'] or row['reversible']!='True' or row['edited_definition']!='False':
            raise ValueError('source identity or review reversibility error '+ident)
    assert m['counts']['recognizable_technical_term']==598
    assert m['counts']['requires_deeper_research']==508
    print(json.dumps({'validated':True,'reviewed':len(rows),'active':len(act),'counts':counts},indent=2))
    return True

if __name__=='__main__':verify()