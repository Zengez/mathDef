"""Task-local read-only evidence capture. No graph operation or external lookup.

Run from repository root. Writes only this review directory. Historical inputs
are restricted to named audit/report blobs at a pinned commit, never its graph.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess

from research_pipeline.engine.core import Workspace, digest
from research_pipeline.engine.dependency_global_audit import load_live_snapshot
from research_pipeline.engine.dependency_cycle_analysis import effective_references
from research_pipeline.engine.dependency_graph import meaning_version
from research_pipeline.engine.dependency_review_export import workspace_files
from research_pipeline.engine.population import snapshot as population_snapshot

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WORKSPACE = ROOT / 'research_pipeline/experiments/reconstruction-v2-independent'
HISTORY = '978db08b2fe736638237c6967f934dbfe96894a3'
AUDIT = 'research_pipeline/reviews/canonical-identity-2026-10-24/'
NAMES = ['POSTCOVERAGE_RECONCILIATION.json','POSTCOVERAGE_RECONCILIATION.md',
         'reviews.jsonl','source-contexts.jsonl','manifest.jsonl','CHAT_ADJUDICATION.md',
         'CHAT_ADJUDICATION_TRANCHE2.md','CHAT_ADJUDICATION_TRANCHE3.md',
         'CHAT_ADJUDICATION_TRANCHE4.md','CHAT_POSTCOVERAGE_ADJUDICATION.md','TRANCHE_5.md']


def capture():
    before = workspace_files(WORKSPACE)
    assert before == json.loads((HERE / 'PROTECTED_FILE_HASHES.json').read_text())
    raw = {name: subprocess.check_output(['git','show', HISTORY+':'+AUDIT+name],cwd=ROOT)
           for name in NAMES}
    inventory = json.loads(raw['POSTCOVERAGE_RECONCILIATION.json'])
    reviews = defaultdict(list)
    for line in raw['reviews.jsonl'].splitlines():
        row = json.loads(line); reviews[row['candidate_id']].append(row)
    history_contexts = {}
    for line in raw['source-contexts.jsonl'].splitlines():
        row=json.loads(line); history_contexts[digest(row)] = row
    selected = [x for x in inventory['canonical_flagged_entries'] if x['disposition'] in
                ('source_convention_deferral','contextual_ambiguity_or_variant')]
    assert len(selected)==40
    snap=load_live_snapshot(WORKSPACE); inv=snap['inventory']
    by_form=defaultdict(list)
    for ref in effective_references(snap):
        by_form[ref['from_formulation']].append(ref)
    candidates={c['id']:c for c in snap['candidates']}
    base=Workspace(WORKSPACE); draft,_=population_snapshot(WORKSPACE)
    observations={**base.records('observations'),**draft['observations']}
    sources={**base.records('sources'),**draft['sources']}
    cases=[]; required_forms=set(); required_meanings=set(); used_history={}
    related = [x for x in inventory['canonical_flagged_entries'] if x['rank'] in (115,348,413)]
    for item in selected+related:
        review=reviews[item['candidate_id']][-1]
        assert review['review_evidence_sha256']==item['review_evidence_sha256']
        parents=[]
        for anchor in item['parents']:
            fid=anchor['formulation_id'];required_forms.add(fid)
            historic=history_contexts[anchor['context_record_sha256']]
            used_history[anchor['context_record_sha256']]=historic
            assert historic['source']['version_sha256']==anchor['source_version_sha256']
            current=inv['formulations'][fid]; node=snap['nodes'][fid]
            allrefs=by_form[fid]
            current_occ=[r for r in allrefs if r.get('missing_candidate_id')==item['candidate_id']
                         or r.get('resolved_missing_candidate_id')==item['candidate_id']]
            oldids={r['occurrence_id'] for r in anchor['candidate_occurrences']}
            parents.append({'historical_anchor':anchor,
                'historical_context_key':anchor['context_record_sha256'],
                'current_context_key':fid,
                'current_source_version_sha256':current['version_sha256'],
                'current_effective_node_sha256':digest(node),
                'source_version_changed':current['version_sha256']!=anchor['source_version_sha256'],
                'node_changed':digest(node)!=anchor['effective_node_sha256'],
                'source_text_changed':historic['source']['text']!=current['text'],
                'observation_records_changed':historic['observations']!={oid:observations[oid] for oid in current.get('evidence_ids',[])},
                'provider_records_changed':historic['sources']!={observations[oid]['source_id']:sources[observations[oid]['source_id']] for oid in current.get('evidence_ids',[])},
                'current_candidate_occurrences':current_occ,
                'historical_occurrences_still_present':[r for r in allrefs if r['occurrence_id'] in oldids],
                'historical_occurrences_no_longer_present':sorted(oldids-{r['occurrence_id'] for r in allrefs})})
        compared=review.get('compared_existing_meanings',{})
        required_meanings.update(compared)
        cases.append({'rank':item['rank'],'canonical_candidate_id':item['candidate_id'],
            'query':item['query'],'historical_disposition':item['disposition'],
            'historical_review':review,'current_registry_record':candidates.get(item['candidate_id']),
            'current_effective_status':{'unresearched':'unresolved_canonical','resolved':'resolved_to_existing_meaning','alias':'aliased_to_canonical'}.get(candidates.get(item['candidate_id'],{}).get('status'),'inspect_registry'),
            'parents':parents,'current_compared_candidate_records':{c['id']:candidates.get(c['id']) for c in review.get('compared_candidate_contexts',[])},
            'existing_target_changes':{mid:{'descriptor_changed':old['descriptor']!=inv['meanings'][mid],
                'formulation_version_set_changed':{fid:f['version_sha256'] for fid,f in old['formulations'].items()}!={fid:inv['formulations'][fid]['version_sha256'] for fid in inv['meanings'][mid]['formulation_ids']}} for mid,old in compared.items()},
            'historical_compared_meaning_ids':sorted(compared)})
    related_cases=cases[40:];cases=cases[:40]
    # Supplementary applied items and remaining source issues, not extra members
    # of the 13+27 inventory. Retain their complete historical contexts too.
    supplementary_forms=set()
    def find_forms(value):
        if isinstance(value,dict):
            fid=value.get('formulation_id')
            if fid in inv['formulations']: supplementary_forms.add(fid)
            for k,v in value.items():
                if k in inv['formulations']: supplementary_forms.add(k)
                find_forms(v)
        elif isinstance(value,list):
            for v in value: find_forms(v)
    for key in ['separate_gate_reconciliation_items','additional_existing_edge_review_leads',
                'provisional_source_issues_for_later_reconciliation','topological_algebra_scope']:
        find_forms(inventory[key])
    supplementary_forms.update(['form.22c049b8eee93897.system-of-parameters',
      'form.b9defeff446a0526.ideal-of-definition-local-ring',
      'form.a81a0fbec29f2186.differential-operator-order',
      'form.wave2.broad67.compact-open-cover','form.wave2.broad67.compact-closed-fip'])
    supplementary_forms.intersection_update(inv['formulations'])
    # Get actual order-zero source from the immutable resolution packet owners.
    for cid in ['missing.f9304694577e53d812c1','missing.b963edbe734f35266d3a']:
        for fid,refs in by_form.items():
            if any(r.get('resolved_missing_candidate_id')==cid for r in refs):supplementary_forms.add(fid)
    required_forms.update(supplementary_forms)
    for fid in list(required_forms):
        required_meanings.add(inv['formulations'][fid]['meaning_id'])
        required_meanings.update(r['target_meaning_id'] for r in by_form[fid] if r.get('target_meaning_id'))
    # All variants of every compared/source/linked meaning, not just one text.
    for mid in required_meanings: required_forms.update(inv['meanings'][mid]['formulation_ids'])
    current_contexts={}
    for fid in sorted(required_forms):
        f=inv['formulations'][fid]
        obs={oid:observations[oid] for oid in f.get('evidence_ids',[])}
        current_contexts[fid]={'source':f,'effective_node_sha256':digest(snap['nodes'][fid]),
            'live_node':snap['nodes'][fid],'effective_references':by_form[fid],
            'observations':obs,'sources':{o['source_id']:sources[o['source_id']] for o in obs.values()}}
    meaning_contexts={mid:{'descriptor':inv['meanings'][mid],
                          'complete_meaning_version_sha256':meaning_version(inv,mid),
                          'formulation_context_keys':inv['meanings'][mid]['formulation_ids']}
                      for mid in sorted(required_meanings)}
    notes_path=HERE/'ANALYSES.json'
    if notes_path.exists():
        notes=json.loads(notes_path.read_text());assert len(notes)==40
        for case in cases:case['contextual_analysis']=notes[str(case['rank'])]
    result={'schema_version':1,'purpose':'Read-only adjudication evidence; no accepted policy or graph transaction',
        'mathematics_certified':False,'external_verification_performed':False,
        'graph_changes_applied':False,'gate_change_authorized':False,
        'historical_commit':HISTORY,'historical_input_byte_sha256':{n:hashlib.sha256(b).hexdigest() for n,b in raw.items()},
        'current_inventory_sha256':inv['source_inventory_sha256'],'current_state':snap['state']['summary'],
        'scope_counts':{'source_convention_deferral':13,'contextual_ambiguity_or_variant':27,'cases':40,
            'parent_visits':sum(len(c['parents']) for c in cases),
            'primary_parent_formulations':len({p['current_context_key'] for c in cases for p in c['parents']}),
            'stored_contexts_with_variants_and_targets':len(current_contexts)},
        'cases':cases,'related_applied_identity_cases':related_cases,'current_contexts':current_contexts,'current_meaning_variants':meaning_contexts,
        'historical_contexts_by_digest':used_history,
        'historical_supplementary_evidence':{k:inventory[k] for k in ['source_convention_policy',
            'selected_additional_scope_questions','separate_gate_reconciliation_items',
            'additional_existing_edge_review_leads','provisional_source_issues_for_later_reconciliation','topological_algebra_scope']},
        'supplementary_current_context_keys':sorted(supplementary_forms),
        'alias_events':snap['aliases'],'resolution_events':snap['resolutions'],
        'seed_override_events':snap['seed_override_events']}
    assert workspace_files(WORKSPACE)==before
    (HERE/'EVIDENCE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result['scope_counts']))
    for c in cases:
        changed=[p['current_context_key'] for p in c['parents'] if p['source_version_changed'] or p['node_changed']]
        print(c['rank'],c['query'],c['current_effective_status'],'CHANGED',changed)

if __name__=='__main__':capture()
