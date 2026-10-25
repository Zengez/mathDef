"""Read-only scope/coverage validation; does not validate mathematical judgments."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from research_pipeline.engine.core import digest
from research_pipeline.engine.dependency_global_audit import load_live_snapshot
from research_pipeline.engine.dependency_cycle_analysis import effective_references


def main():
    here = Path(__file__).resolve().parent
    rows = lambda name: [json.loads(s) for s in (here / name).read_text().splitlines()]
    sha = lambda name: hashlib.sha256((here / name).read_bytes()).hexdigest()
    checkpoint = json.loads((here / 'checkpoint.json').read_text())
    snapshot = load_live_snapshot(ROOT / 'research_pipeline/experiments/reconstruction-v2-independent')
    refs = effective_references(snapshot)
    manifest = rows('manifest.jsonl')
    contexts = {r['formulation_id']: r for r in rows('source-contexts.jsonl')}
    candidates = sorted((c for c in snapshot['candidates']
                         if c['status'] == 'unresearched' and not c.get('alias_of')
                         and not c.get('resolved_target_meaning_id')),
                        key=lambda c: (-c['occurrence_count'], -c['upstream_formulation_count'], c['id']))
    summary = snapshot['state']['summary']
    for key in ('inventory_sha256', 'unresolved_fingerprint'):
        assert checkpoint[key] == summary[key], f'Active scope drift: {key}'
    for filename, key in [('manifest.jsonl', 'manifest_sha256'),
                          ('reviews.jsonl', 'reviews_sha256'),
                          ('source-contexts.jsonl', 'source_contexts_sha256')]:
        assert sha(filename) == checkpoint[key], filename
    assert len(candidates) == len(manifest) == checkpoint['total_canonical']
    for rank, (candidate, row) in enumerate(zip(candidates, manifest), 1):
        assert row['rank'] == rank and row['initial_review_status'] == 'UNREVIEWED'
        for key in ('inventory_sha256', 'unresolved_fingerprint'):
            assert row[key] == checkpoint[key]
        for a, b in [('id', 'candidate_id'), ('context', 'context'), ('query', 'query'),
                     ('occurrence_count', 'occurrence_count'),
                     ('incoming_formulation_ids', 'incoming_formulation_ids')]:
            assert candidate[a] == row[b], (candidate['id'], a)
        assert sorted(candidate['alias_ids']) == row['observed_alias_ids']
        assert len(row['incoming_formulation_ids']) == row['incoming_formulation_count']
    for fid, context in contexts.items():
        assert context['source'] == snapshot['inventory']['formulations'][fid], fid
        assert context['effective_node_sha256'] == digest(snapshot['nodes'][fid]), fid
        assert context['effective_references'] == [r for r in refs if r['from_formulation'] == fid], fid
    by_id = {m['candidate_id']: m for m in manifest}
    latest, event_ids = {}, set()
    for event in rows('reviews.jsonl'):
        cid = event['candidate_id']
        for key in ('inventory_sha256', 'unresolved_fingerprint'):
            assert event[key] == checkpoint[key]
        assert event['review_id'] not in event_ids
        event_ids.add(event['review_id'])
        assert event['review_evidence_sha256'] == digest({k: v for k, v in event.items()
                                                        if k != 'review_evidence_sha256'})
        if cid in latest:
            assert event['supersedes_review_id'] == latest[cid]['review_id']
        done, remaining = event['parent_formulations_reviewed'], event['parent_formulations_remaining']
        assert len(done) == len(set(done)) and len(remaining) == len(set(remaining))
        assert not set(done) & set(remaining)
        assert set(done + remaining) == set(by_id[cid]['incoming_formulation_ids'])
        assert event['coverage_status'] == ('PARTIAL' if remaining else 'COMPLETE')
        for fid, evidence in event['parent_evidence'].items():
            assert fid in done and evidence['context_record_sha256'] == digest(contexts[fid])
            assert evidence['source_version_sha256'] == contexts[fid]['source']['version_sha256']
            assert evidence['effective_node_sha256'] == contexts[fid]['effective_node_sha256']
            assert evidence['candidate_occurrences'] == [r for r in contexts[fid]['effective_references']
                                                        if r.get('missing_candidate_id') == cid]
        assert set(event['parent_evidence']) == set(done)
        for mid, evidence in event['compared_existing_meanings'].items():
            assert evidence['descriptor'] == snapshot['inventory']['meanings'][mid]
            for fid, source in evidence['formulations'].items():
                assert source == snapshot['inventory']['formulations'][fid]
        assert not event['semantic_graph_changes_applied']
        latest[cid] = event
    for status, key in [('COMPLETE', 'complete_candidate_ids'), ('PARTIAL', 'partial_candidate_ids')]:
        assert checkpoint[key] == [m['candidate_id'] for m in manifest
                                   if m['candidate_id'] in latest
                                   and latest[m['candidate_id']]['coverage_status'] == status]
    untouched = [m['candidate_id'] for m in manifest if m['candidate_id'] not in latest]
    assert checkpoint['untouched_candidate_ids'] == untouched
    assert checkpoint['latest_review_ids'] == {cid: e['review_id'] for cid, e in latest.items()}
    assert checkpoint['reviewed_parent_formulation_ids'] == sorted(contexts)
    unfinished = [m['candidate_id'] for m in manifest if m['candidate_id'] not in latest
                  or latest[m['candidate_id']]['coverage_status'] == 'PARTIAL']
    assert checkpoint['next_unfinished_candidate_id'] == unfinished[0]
    next_parents = (latest[unfinished[0]]['parent_formulations_remaining'] if unfinished[0] in latest
                    else by_id[unfinished[0]]['incoming_formulation_ids'])
    assert checkpoint['next_parent_formulation_id'] == next_parents[0]
    assert not checkpoint['semantic_graph_changed'] and not checkpoint['gate_opened']
    print(f'PASS: {len(manifest)} inventoried; {len(latest)} contextual records; '
          f'{len(contexts)} source anchors; {len(untouched)} untouched. Mathematical judgments require review.')


if __name__ == '__main__':
    main()
