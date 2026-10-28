#!/usr/bin/env python3
"""Verify completeness and immutable provenance of the 2026-10-28 independent-term review."""
from __future__ import annotations
import csv,hashlib,json
from collections import Counter
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]/'research_pipeline/discovery/independent_term_review_20261028'
CATEGORIES={'candidate_lead','needs_targeted_review','remove_description',
            'remove_false_positive','remove_fragment','existing_definition'}
SURVIVORS={'candidate_lead','needs_targeted_review'}

def verify(base=BASE):
    base=Path(base)
    manifest=json.loads((base/'manifest.json').read_text(encoding='utf-8'))
    if manifest.get('schema')!='mathdef.independent-terminology-filter.v1':
        raise ValueError('Review manifest schema mismatch')
    stats=Counter();ids=set();phrases=set();survivors=set()
    for part in manifest['parts']:
        name=part['name']
        if '/' in name or not name.endswith('.tsv'):raise ValueError('Bad part name')
        b=(base/'batches'/name).read_bytes()
        if len(b)!=part['bytes'] or hashlib.sha256(b).hexdigest()!=part['sha256']:
            raise ValueError('Corrupt review batch: '+name)
        with (base/'batches'/name).open(newline='',encoding='utf-8') as f:
            rows=list(csv.DictReader(f,delimiter='\t'))
        if len(rows)!=part['records']:raise ValueError('Batch row count mismatch')
        for r in rows:
            ident=r['candidate_id'];phrase=r['phrase'];disp=r['disposition']
            if disp not in CATEGORIES or not phrase or ident in ids or phrase in phrases:
                raise ValueError('Duplicate/malformed review entry: '+ident)
            if ident!='term.'+hashlib.sha256(phrase.encode('utf-8')).hexdigest()[:20]:
                raise ValueError('Candidate stable ID mismatch: '+ident)
            if not r.get('source_ids') or not r.get('review_reason5'):
                raise ValueError('Candidate lacks source/reason')
            if r['reversible']!='true' or r['validated_as_new_definition']!='false':
                raise ValueError('Unauthorized final definition adjudication')
            ids.add(ident);phrases.add(phrase);stats[disp]+=1
            if disp in SURVIVORS:survivors.add(ident)
    if len(ids)!=7240 or stats!=manifest['counts']:
        raise ValueError('Total or review class discrepancy')
    other=set();rows2=0
    for part in manifest['survivor_parts']:
        name=part['name'];b=(base/'survivor_batches'/name).read_bytes()
        if len(b)!=part['bytes'] or hashlib.sha256(b).hexdigest()!=part['sha256']:
            raise ValueError('Corrupt survivor batch '+name)
        with (base/'survivor_batches'/name).open(encoding='utf-8',newline='') as f:
            rr=list(csv.DictReader(f,delimiter='\t'))
        if len(rr)!=part['records']:raise ValueError('Survivor batch count mismatch')
        for r in rr:
            if r['disposition'] not in SURVIVORS or r['candidate_id'] in other:
                raise ValueError('Invalid survivor record')
            other.add(r['candidate_id']);rows2+=1
    if other!=survivors or rows2!=manifest['survivors']:
        raise ValueError('Survivors do not match decisions')
    return {'ok':True,'total':len(ids),'survivors':len(survivors),
            'suppressed':len(ids)-len(survivors),'counts':dict(sorted(stats.items()))}

if __name__=='__main__':print(json.dumps(verify(),indent=2))