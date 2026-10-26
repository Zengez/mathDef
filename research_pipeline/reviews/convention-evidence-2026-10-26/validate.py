"""Validate this task's evidence anchors and byte preservation, read-only.

Run: python -m research_pipeline.reviews.convention-evidence-2026-10-26.validate
No source certification, policy acceptance or graph operation is performed.
"""
from collections import Counter, defaultdict
import json
import hashlib
from pathlib import Path
import subprocess

from research_pipeline.engine.core import digest, Workspace
from research_pipeline.engine.population import snapshot as population_snapshot
from .capture import NAMES, HISTORY, AUDIT
from research_pipeline.engine.dependency_cycle_analysis import effective_references
from research_pipeline.engine.dependency_global_audit import load_live_snapshot
from research_pipeline.engine.dependency_graph import meaning_version
from research_pipeline.engine.dependency_review_export import workspace_files
from research_pipeline.engine.dependency_reconciliation_status import reconciliation_status

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
W=ROOT/'research_pipeline/experiments/reconstruction-v2-independent'
BASE='51696c08b1e5e8b7964ad4f1599e61acc9301ff9'


def validate():
    e=json.loads((HERE/'EVIDENCE.json').read_text())
    notes=json.loads((HERE/'ANALYSES.json').read_text())
    assert set(e['historical_input_byte_sha256'])==set(NAMES)
    assert e['historical_commit']==HISTORY
    for name,sha in e['historical_input_byte_sha256'].items():
        raw=subprocess.check_output(['git','show',HISTORY+':'+AUDIT+name],cwd=ROOT)
        assert hashlib.sha256(raw).hexdigest()==sha
    snap=load_live_snapshot(W); inv=snap['inventory']
    assert workspace_files(W)==json.loads((HERE/'PROTECTED_FILE_HASHES.json').read_text())
    assert e['current_state']==snap['state']['summary']
    assert e['current_inventory_sha256']==inv['source_inventory_sha256']
    assert e['current_state']['phase']=='consolidate_occurrences'
    assert e['current_state']['consolidation_gate_valid'] is False
    assert e['graph_changes_applied'] is e['external_verification_performed'] is e['gate_change_authorized'] is False
    cases=e['cases'];assert len(cases)==len(notes)==40
    assert Counter(c['historical_disposition'] for c in cases)=={'source_convention_deferral':13,'contextual_ambiguity_or_variant':27}
    assert len({c['rank'] for c in cases})==40
    current={c['id']:c for c in snap['candidates']}
    refs=defaultdict(list)
    for ref in effective_references(snap):refs[ref['from_formulation']].append(ref)
    base=Workspace(W); draft,_=population_snapshot(W)
    observations={**base.records('observations'),**draft['observations']}
    sources={**base.records('sources'),**draft['sources']}
    for fid,ctx in e['current_contexts'].items():
        assert ctx['source']==inv['formulations'][fid]
        assert ctx['observations']=={oid:observations[oid] for oid in ctx['source']['evidence_ids']}
        assert ctx['sources']=={o['source_id']:sources[o['source_id']] for o in ctx['observations'].values()}
        assert ctx['live_node']==snap['nodes'][fid]
        assert ctx['effective_node_sha256']==digest(snap['nodes'][fid])
        assert ctx['effective_references']==refs[fid]
        assert inv['formulations'][fid]['text'] in (HERE/'CONTEXTS.md').read_text()
    for mid,item in e['current_meaning_variants'].items():
        assert item['descriptor']==inv['meanings'][mid]
        assert item['complete_meaning_version_sha256']==meaning_version(inv,mid)
        assert item['formulation_context_keys']==inv['meanings'][mid]['formulation_ids']
        assert all(fid in e['current_contexts'] for fid in item['formulation_context_keys'])
    for case in cases+e['related_applied_identity_cases']:
        r=case['historical_review']
        assert digest({k:v for k,v in r.items() if k!='review_evidence_sha256'})==r['review_evidence_sha256']
        assert case['current_registry_record']==current[case['canonical_candidate_id']]
        if case in cases:
            assert case['contextual_analysis']==notes[str(case['rank'])]
            assert case['current_effective_status']=='unresolved_canonical'
        for p in case['parents']:
            old=e['historical_contexts_by_digest'][p['historical_context_key']]
            assert digest(old)==p['historical_context_key']
            assert old['effective_node_sha256']==p['historical_anchor']['effective_node_sha256']
            assert old['source']['version_sha256']==p['historical_anchor']['source_version_sha256']
            fid=p['current_context_key']
            assert p['current_source_version_sha256']==inv['formulations'][fid]['version_sha256']
            assert p['current_effective_node_sha256']==digest(snap['nodes'][fid])
            for ref in refs[fid]:
                if ref.get('target_meaning_id'):
                    assert ref['target_meaning_id'] in e['current_meaning_variants']
    assert sum(len(c['parents']) for c in cases)==104
    assert len({p['current_context_key'] for c in cases for p in c['parents']})==93
    assert [c['rank'] for c in cases if any(p['node_changed'] for p in c['parents'])]==[399]
    assert not any(p[k] for c in cases for p in c['parents'] for k in
        ['source_version_changed','source_text_changed','observation_records_changed','provider_records_changed'])
    assert not any(any(change.values()) for c in cases for change in c['existing_target_changes'].values())
    assert e['alias_events']==snap['aliases'] and e['resolution_events']==snap['resolutions']
    assert e['seed_override_events']==snap['seed_override_events']
    queue=json.loads((ROOT/'research_pipeline/reviews/canonical-identity-2026-10-24/LIVE_RECONCILIATION_QUEUE.json').read_text())
    status=reconciliation_status(W,queue,snapshot=snap)
    assert status==json.loads((HERE/'TRANSACTION_STATUS.json').read_text())
    assert status['status_counts']=={'applied_receipt_verified':6,'superseded_by_verified_transaction':2}
    assert status['active_review_case_count']==0
    supplement=json.loads((HERE/'SUPPLEMENTARY.json').read_text())
    packets=[json.loads(p.read_text()) for p in (W/'dependency_graph/inbox').glob('*.json')]
    for row in supplement['edge_corrections']:
        assert row['source_text_changed'] is False and row['current_same_occurrence']==[]
        assert any(a.get('formulation_id')==row['formulation_id'] and a.get('expected_node_sha256')==row['historical_effective_node_sha256'] for packet in packets for a in packet.get('amendments',[]))
    issues={r['id']:r for r in map(json.loads,(W/'population/records/issues.jsonl').read_text().splitlines())}
    for issue in supplement['source_issues']:
        assert issue['current_record']==issues[issue['issue_id']]==issue['historical_record']
        assert digest(issue['current_record'])==issue['current_record_sha256']==issue['historical_record_sha256']
    cards=json.loads((HERE/'ADJUDICATION_QUEUE.json').read_text())['cards']
    assert sorted(r for c in cards for r in c['historical_ranks'])==sorted(c['rank'] for c in cases)
    assert all(not c['graph_action_submitted'] and c['not_gate_acceptance'] for c in cards)
    paths=subprocess.check_output(['git','diff','--name-only',BASE],cwd=ROOT,text=True).splitlines()
    untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
    prefix=HERE.relative_to(ROOT).as_posix()+'/'
    assert all(p.startswith(prefix) for p in paths+untracked)
    print(json.dumps({'validation':'passed','cases':40,'parent_visits':104,'primary_parent_formulations':93,
        'complete_current_contexts':len(e['current_contexts']),'decision_cards':len(cards),
        'verified_transactions':6,'superseded_historical_reviews':2,'protected_files_unchanged':2293,
        'protected_file_map_sha256':digest(workspace_files(W)),
        'gate_closed':True,'external_source_verification_performed':False},indent=2))

if __name__=='__main__':validate()
