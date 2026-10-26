"""Explicit, read-only candidate-context metadata; never a graph transaction.

Proposal and review events are hash chained, checkpointed and bound to every
incoming occurrence. Approval means reviewer-authored interpretation metadata,
not an applied graph/source change or mathematical/source certification.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from .core import PipelineError, digest
from .dependency_cycle_analysis import effective_references
from .dependency_graph import KEY_RE, collect, missing_key

GENESIS = digest(None)


def _keys(value, required):
    if not isinstance(value, dict) or set(value) != set(required.split()):
        raise PipelineError('Unexpected or missing context-review fields: ' + required)


def _text(value, minimum=1):
    if not isinstance(value, str) or len(value.strip()) < minimum:
        raise PipelineError('Context review requires substantive text/provenance')


def _id(value):
    if not isinstance(value, str) or not KEY_RE.fullmatch(value):
        raise PipelineError('Invalid context-review identity')


def _sha(value):
    if not isinstance(value, str) or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
        raise PipelineError('Invalid SHA256 context-review pin')


def _strings(value):
    if not isinstance(value, list) or not value:
        raise PipelineError('Explicit hypotheses/retained conditions are required')
    for item in value:
        _text(item)


def _provenance(payload, author):
    _text(payload[author]); _text(payload['rationale'], 60)
    _text(payload['authored_at'])
    try:
        stamp = datetime.fromisoformat(payload['authored_at'])
        if stamp.tzinfo is None:
            raise ValueError('timezone missing')
    except ValueError as exc:
        raise PipelineError('Review time must include a timezone') from exc
    refs = payload['provenance']
    if not isinstance(refs, list) or not refs:
        raise PipelineError('Review requires explicit evidence provenance')
    for ref in refs:
        _keys(ref, 'artifact sha256'); _text(ref['artifact']); _sha(ref['sha256'])


def read_json(path):
    """Reject ambiguous duplicate keys and non-JSON NaN/Infinity inputs."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise PipelineError('Duplicate JSON field in review input')
            result[key] = value
        return result
    def constant(_):
        raise PipelineError('Nonfinite JSON review input')
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=constant)


def history_checkpoint(events):
    return {'event_count': len(events), 'ledger_sha256': digest(events),
            'tip_sha256': digest(events[-1]) if events else GENESIS}


def _history(events, checkpoint):
    _keys(checkpoint, 'event_count ledger_sha256 tip_sha256')
    if (type(checkpoint['event_count']) is not int or checkpoint != history_checkpoint(events)):
        raise PipelineError('Review history checkpoint mismatch: truncation/replacement/reordering')
    previous, seen = GENESIS, set()
    for event in events:
        _keys(event, 'event_id previous_event_sha256 kind payload')
        _id(event['event_id'])
        if event['event_id'] in seen or event['previous_event_sha256'] != previous:
            raise PipelineError('Duplicate event or broken append-only review chain')
        seen.add(event['event_id']); previous = digest(event)


def graph_fingerprints(snapshot):
    """Complete ordered ledgers and source/variant/replay inputs, not just counts."""
    fields = ('inventory', 'state', 'nodes', 'candidates', 'aliases',
              'resolutions', 'seed_override_events', 'review_ledger', 'context_review_file_pins')
    return {key + '_sha256': digest(snapshot[key]) for key in fields}


def _alias_history(snapshot):
    # Validate even inactive historical events, without resurrecting them.
    direct, seen = {}, set()
    for event in snapshot['aliases']:
        eid = event.get('alias_id'); _id(eid)
        a, b = event.get('alias_candidate_id'), event.get('canonical_candidate_id')
        _id(a); _id(b)
        if eid in seen or a in direct or a == b:
            raise PipelineError('Duplicate/conflicting historical alias')
        _text(event.get('reviewed_by')); _text(event.get('reason'), 40)
        seen.add(eid); direct[a] = b
    finals = {}
    for alias in direct:
        current, visited = alias, set()
        while current in direct:
            if current in visited:
                raise PipelineError('Cycle in historical alias ledger')
            visited.add(current); current = direct[current]
        finals[alias] = current
    return direct, finals


def load_context_snapshot(workspace):
    """Explicit context-review input: fresh sources and ALL workspace file bytes.

    Default graph snapshots stay unchanged. This extra pin also binds original
    nodes, historical amendment rationales, receipts and other provenance that
    may not alter the current effective graph projection.
    """
    from .dependency_global_audit import load_live_snapshot
    from .dependency_review_export import workspace_files
    snapshot = load_live_snapshot(workspace)
    files = workspace_files(Path(workspace))
    entries, meanings, seeds, revisions = collect(Path(workspace))
    descriptors = {mid: {'display_term': value['display_term'], 'context': value['context'],
                        'formulation_ids': [f['id'] for f in value.get('formulations', [])]}
                   for mid, value in meanings.items()}
    inv = snapshot['inventory']
    if (entries != inv['formulations'] or descriptors != inv['meanings']
            or seeds != inv['seed_relations'] or digest(entries) != inv['source_inventory_sha256']
            or digest(seeds) != inv['seed_relations_sha256'] or len(revisions) != inv['revision_count']):
        raise PipelineError('Inventory is stale against current source records')
    snapshot['context_review_file_pins'] = {'file_count': len(files), 'files_sha256': digest(files)}
    return snapshot


def candidate_basis(snapshot, candidate_id):
    """Capture facts only; this does not propose or approve an interpretation."""
    _id(candidate_id)
    if 'context_review_file_pins' not in snapshot:
        raise PipelineError('Use load_context_snapshot to bind complete workspace provenance')
    pins = snapshot['context_review_file_pins']
    _keys(pins, 'file_count files_sha256')
    if type(pins['file_count']) is not int or pins['file_count'] < 1:
        raise PipelineError('Invalid protected workspace file count')
    _sha(pins['files_sha256'])
    inv = snapshot['inventory']
    registry = snapshot['candidates']
    if len({c['id'] for c in registry}) != len(registry):
        raise PipelineError('Duplicate registry identity')
    candidate = next((c for c in registry if c['id'] == candidate_id), None)
    if (not candidate or candidate.get('status') != 'unresearched'
            or candidate.get('alias_of') or candidate.get('resolved_target_meaning_id')
            or any(r['missing_candidate_id'] == candidate_id for r in snapshot['resolutions'])):
        raise PipelineError('Context review requires a live unresolved canonical candidate')
    direct, finals = _alias_history(snapshot)
    if any(target not in {c['id'] for c in registry} for target in finals.values()):
        raise PipelineError('Unknown final target in historical aliases')
    if candidate_id in direct:
        raise PipelineError('Aliased identity cannot own a context review')
    effective = [ref for ref in effective_references(snapshot)
                 if ref.get('state') == 'missing' and ref.get('missing_candidate_id') == candidate_id]
    if not effective:
        raise PipelineError('Candidate has no current effective occurrences')
    anchors, seen = [], set()
    seeds = {s['relation_id']: s for s in inv.get('seed_relations', [])}
    for ref in effective:
        fid, oid = ref['from_formulation'], ref['occurrence_id']
        if (fid, oid) in seen:
            raise PipelineError('Duplicate effective occurrence identity')
        seen.add((fid, oid))
        source, node = inv['formulations'][fid], snapshot['nodes'].get(fid)
        if node is None or node.get('scan_status') != 'complete' or node.get('version_sha256') != source['version_sha256']:
            raise PipelineError('Incomplete or stale source scan')
        if ref.get('relation_id'):
            kind, raw = 'historical_seed', seeds[ref['relation_id']]
        else:
            matches = [r for r in node['references'] if r['occurrence_id'] == oid]
            if len(matches) != 1 or matches[0].get('state') != 'missing':
                raise PipelineError('Missing or inconsistent live occurrence')
            kind, raw = 'live_node', matches[0]
        observed = ref.get('observed_missing_candidate_id', ref['missing_candidate_id'])
        chain, current = [], observed
        while current != candidate_id:
            if current not in direct or finals.get(current) != candidate_id:
                raise PipelineError('Unknown or inconsistent occurrence alias path')
            event = next(e for e in snapshot['aliases'] if e['alias_candidate_id'] == current)
            chain.append(event['alias_id']); current = direct[current]
        anchors.append({'formulation_id': fid, 'occurrence_id': oid, 'reference_kind': kind,
                        'source_version_sha256': source['version_sha256'],
                        'source_snapshot_sha256': source.get('source_snapshot_sha256'),
                        'source_record_sha256': digest(source), 'source': deepcopy(source),
                        'effective_node_sha256': digest(node),
                        'observed_candidate_id': observed, 'alias_event_ids': chain,
                        'raw_observed_reference': deepcopy(raw),
                        'effective_reference': deepcopy(ref),
                        'source_meaning_id': source['meaning_id']})
    return {'canonical_candidate': {k: candidate[k] for k in ('id', 'query', 'context')},
            'candidate_record_sha256': digest(candidate),
            'graph_fingerprints': graph_fingerprints(snapshot),
            'alias_history': [deepcopy(e) for e in snapshot['aliases']
                              if finals.get(e['alias_candidate_id']) == candidate_id],
            'occurrences': sorted(anchors, key=lambda a: (a['formulation_id'], a['occurrence_id']))}


def validate_qualification_ledger(ledger):
    """Basic evidence-shape validation, NOT proof that claimed edits were applied."""
    if not isinstance(ledger, dict) or type(ledger.get('schema_version')) is not int or ledger['schema_version'] != 1:
        raise PipelineError('Unsupported qualification ledger')
    seen = set()
    for group in ('review_candidates', 'applied_qualifications'):
        if not isinstance(ledger.get(group), list):
            raise PipelineError('Qualification ledger requires separate proposed/applied lists')
        for row in ledger[group]:
            if not isinstance(row, dict):
                raise PipelineError('Qualification record must be an object')
            _id(row.get('id'))
            if row['id'] in seen:
                raise PipelineError('Duplicate qualification identity')
            seen.add(row['id'])
            _id(row.get('affected_formulation_id')); _sha(row.get('source_version_sha256'))
            if group == 'review_candidates':
                if (row.get('status') != 'review_candidate_not_applied' or row.get('change_applied') is not False
                        or row.get('application_commit') is not None or row.get('transaction_receipt') is not None):
                    raise PipelineError('Proposed qualification cannot claim application')
                _sha(row.get('effective_node_sha256')); _text(row.get('counterexample'), 20)
            else:
                if row.get('change_applied', True) is not True or row.get('status', 'applied') != 'applied':
                    raise PipelineError('Applied qualification list cannot contain a proposal')
                for key in ('exception_kind', 'original_wording', 'qualified_wording', 'counterexample',
                            'mathematical_rationale', 'source_convention_status',
                            'transaction_receipt_or_reason_not_applicable', 'manual_review_state'):
                    _text(row.get(key))
                _sha(row.get('effective_node_sha256_before'))
                commit = row.get('application_commit')
                if not isinstance(commit, str) or len(commit) != 40 or any(c not in '0123456789abcdef' for c in commit):
                    raise PipelineError('Applied qualification requires application commit evidence')
    return {'review_candidates': len(ledger['review_candidates']),
            'claimed_applied_qualifications': len(ledger['applied_qualifications']),
            'application_evidence_verified': False}


def replay_reviews(snapshot, events, checkpoint, *, qualification_ledger=None):
    """Fail closed before returning any interpretation. No mutation of inputs."""
    if not isinstance(events, list):
        raise PipelineError('Review log events must be a list')
    try:
        json.dumps(events, allow_nan=False)
    except (ValueError, TypeError) as exc:
        raise PipelineError('Review events must be finite JSON data') from exc
    _history(events, checkpoint)
    if qualification_ledger is not None:
        validate_qualification_ledger(qualification_ledger)
    proposals, decisions, active, bases = {}, {}, {}, {}
    for event in events:
        data = event['payload']
        if event['kind'] == 'proposal':
            _keys(data, 'basis prior_review_event_sha256 interpretation occurrence_interpretations authored_by authored_at rationale provenance qualification_reference')
            _provenance(data, 'authored_by')
            if not isinstance(data['basis'], dict) or not isinstance(data['basis'].get('canonical_candidate'), dict):
                raise PipelineError('Missing canonical candidate basis')
            cid = data['basis']['canonical_candidate'].get('id')
            if cid not in bases:
                bases[cid] = candidate_basis(snapshot, cid)
            basis = bases[cid]
            if data['basis'] != basis:
                raise PipelineError('Stale or inconsistent candidate/source/occurrence/ledger basis')
            interpretation = data['interpretation']
            _keys(interpretation, 'kind context hypotheses')
            if interpretation['kind'] != 'component_prerequisite':
                raise PipelineError('Only component interpretations; no whole-parent identity or retargeting')
            _text(interpretation['context'], 40); _strings(interpretation['hypotheses'])
            expected_prior = active.get(cid, {}).get('review_event_sha256')
            if data['prior_review_event_sha256'] != expected_prior:
                raise PipelineError('Stale prior reviewed interpretation')
            coverage = data['occurrence_interpretations']
            if not isinstance(coverage, list):
                raise PipelineError('Explicit occurrence interpretation coverage required')
            keys = []
            for row in coverage:
                _keys(row, 'formulation_id occurrence_id relation instantiation retained_parent_conditions rationale')
                _id(row['formulation_id']); _id(row['occurrence_id'])
                if row['relation'] != 'component_instantiation':
                    raise PipelineError('No equivalence to an entire quantified/specialized parent')
                _text(row['instantiation'], 40); _strings(row['retained_parent_conditions']); _text(row['rationale'], 60)
                keys.append((row['formulation_id'], row['occurrence_id']))
            expected = [(r['formulation_id'], r['occurrence_id']) for r in basis['occurrences']]
            if keys != expected:
                raise PipelineError('Coverage must include every occurrence exactly once in canonical order')
            qualification = data['qualification_reference']
            if qualification is not None:
                _keys(qualification, 'ledger_sha256 review_candidate_id')
                if (qualification_ledger is None or digest(qualification_ledger) != qualification['ledger_sha256']
                        or qualification['review_candidate_id'] not in
                        {r['id'] for r in qualification_ledger['review_candidates']}):
                    raise PipelineError('Qualification reference must pin a proposed, not applied, ledger entry')
                entry = next(r for r in qualification_ledger['review_candidates']
                             if r['id'] == qualification['review_candidate_id'])
                if not any(entry['affected_formulation_id'] == r['formulation_id']
                           and entry['source_version_sha256'] == r['source_version_sha256']
                           and entry['effective_node_sha256'] == r['effective_node_sha256']
                           and entry.get('affected_candidate_id', cid) == cid
                           and entry.get('affected_occurrence_id', r['occurrence_id']) == r['occurrence_id']
                           for r in basis['occurrences']):
                    raise PipelineError('Qualification source/occurrence pins do not match this proposal')
            proposals[event['event_id']] = event
        elif event['kind'] == 'review':
            _keys(data, 'proposal_event_id proposal_event_sha256 decision reviewed_by authored_at rationale provenance')
            _provenance(data, 'reviewed_by')
            pid = data['proposal_event_id']; _id(pid)
            proposal = proposals.get(pid)
            if (proposal is None or pid in decisions or digest(proposal) != data['proposal_event_sha256']
                    or data['decision'] not in ('approve', 'reject')):
                raise PipelineError('Invalid, reused or changed proposal review')
            decisions[pid] = event
            if data['decision'] == 'approve':
                content = proposal['payload']; cid = content['basis']['canonical_candidate']['id']
                if content['prior_review_event_sha256'] != active.get(cid, {}).get('review_event_sha256'):
                    raise PipelineError('Concurrent review changed the prior interpretation')
                active[cid] = {'review_event_id': event['event_id'], 'review_event_sha256': digest(event),
                               'reviewed_by': data['reviewed_by'], 'interpretation': deepcopy(content['interpretation']),
                               'occurrence_interpretations': deepcopy(content['occurrence_interpretations']),
                               'graph_change_applied': False}
        else:
            raise PipelineError('Unknown context event kind; no apply/resolve/alias events supported')
    candidates = {}
    for cid, basis in bases.items():
        candidates[cid] = {'original_evidence': deepcopy(basis),
                           'reviewed_interpretation': active.get(cid),
                           'proposals': [{'event_id': p['event_id'], 'event_sha256': digest(p),
                               'interpretation': deepcopy(p['payload']['interpretation']),
                               'status': decisions[p['event_id']]['payload']['decision']
                                   if p['event_id'] in decisions else 'proposed_not_reviewed'}
                               for p in proposals.values() if p['payload']['basis']['canonical_candidate']['id'] == cid]}
    return {'schema_version': 1, 'view_kind': 'parallel_candidate_context_review_metadata',
            'graph_changes_applied': False, 'mathematics_certified': False,
            'gate_change_authorized': False, 'checkpoint': history_checkpoint(events),
            'candidates': candidates, 'review_events': deepcopy(events),
            'qualification_ledger': deepcopy(qualification_ledger),
            'warning': 'Reviewer assertions are not mechanically proven. Original source, canonical context, '
                       'aliases, quantifiers and graph edges remain authoritative and unchanged.'}


def extend_log(snapshot, prior_events, prior_checkpoint, new_events, *, qualification_ledger=None):
    """Pure append operation: preserve prior events byte-equivalent as JSON values."""
    replay_reviews(snapshot, prior_events, prior_checkpoint, qualification_ledger=qualification_ledger)
    if not isinstance(new_events, list) or not new_events:
        raise PipelineError('Append needs new review events')
    combined = deepcopy(prior_events) + deepcopy(new_events)
    checkpoint = history_checkpoint(combined)
    replay_reviews(snapshot, combined, checkpoint, qualification_ledger=qualification_ledger)
    return {'events': combined, 'checkpoint': checkpoint}


def attach_reviews(snapshot, events, checkpoint, *, qualification_ledger=None):
    """Opt-in read-only sidecar; never replace canonical contexts or references."""
    report = replay_reviews(snapshot, events, checkpoint, qualification_ledger=qualification_ledger)
    return {**snapshot, 'candidate_context_reviews': report}


def validated_view(snapshot):
    """Revalidate sidecars at each reader boundary; reject edited/stale metadata."""
    view = snapshot.get('candidate_context_reviews')
    if view is None:
        return None
    if not isinstance(view, dict):
        raise PipelineError('Invalid context review sidecar')
    expected = replay_reviews(snapshot, view.get('review_events'), view.get('checkpoint'),
                              qualification_ledger=view.get('qualification_ledger'))
    if view != expected:
        raise PipelineError('Modified or inconsistent context review sidecar')
    return expected


def attach_review_files(snapshot, log_path, checkpoint_path, *, qualification_ledger_path=None):
    """Explicit file opt-in for analysis readers; no implicit workspace loading."""
    log = read_json(log_path)
    _keys(log, 'schema_version events')
    if type(log['schema_version']) is not int or log['schema_version'] != 1:
        raise PipelineError('Unsupported context review log schema')
    ledger = read_json(qualification_ledger_path) if qualification_ledger_path else None
    return attach_reviews(snapshot, log['events'], read_json(checkpoint_path),
                          qualification_ledger=ledger)


def preflight(workspace, log_path, checkpoint_path, *, qualification_ledger_path=None):
    """Receipt-shaped mechanical evidence from a disposable byte-identical copy."""
    from .dependency_review_export import workspace_files
    workspace = Path(workspace).resolve()
    before = workspace_files(workspace)
    paths = [Path(log_path), Path(checkpoint_path)]
    if qualification_ledger_path is not None:
        paths.append(Path(qualification_ledger_path))
    if any(p.resolve().is_relative_to(workspace) for p in paths):
        raise PipelineError('Review logs/checkpoints must remain outside the protected workspace')
    raw = {p: p.read_bytes() for p in paths}
    log, checkpoint = read_json(paths[0]), read_json(paths[1])
    _keys(log, 'schema_version events')
    if type(log['schema_version']) is not int or log['schema_version'] != 1:
        raise PipelineError('Unsupported context review log schema')
    ledger = read_json(paths[2]) if len(paths) == 3 else None
    with tempfile.TemporaryDirectory(prefix='candidate-context-preflight-') as directory:
        copied = Path(directory) / 'workspace'
        shutil.copytree(workspace, copied)
        if workspace_files(copied) != before:
            raise PipelineError('Disposable workspace copy differs from original')
        try:
            snapshot = load_context_snapshot(copied)
            view = replay_reviews(snapshot, log['events'], checkpoint, qualification_ledger=ledger)
        finally:
            if (workspace_files(copied) != before or workspace_files(workspace) != before
                    or any(p.read_bytes() != value for p, value in raw.items())):
                raise PipelineError('Workspace or review inputs changed during read-only preflight')
    return {'schema_version': 1, 'status': 'mechanically_valid_not_applied',
            'read_only': True, 'graph_changes_applied': False, 'mathematics_certified': False,
            'gate_change_authorized': False, 'disposable_copy_verified': True,
            'workspace_file_count': len(before), 'workspace_before_sha256': digest(before),
            'workspace_after_sha256': digest(before), 'source_inventory_fresh': True,
            'review_log_sha256': digest(log), 'review_history_checkpoint': checkpoint,
            'input_byte_sha256': {str(p): hashlib.sha256(value).hexdigest() for p, value in raw.items()},
            'review_view': view,
            'warning': 'Not an applied graph receipt; no submit/apply dispatcher consumes this evidence.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--log', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--qualification-ledger', type=Path)
    args = parser.parse_args()
    try:
        report = preflight(args.workspace, args.log, args.checkpoint,
                           qualification_ledger_path=args.qualification_ledger)
    except (PipelineError, OSError, ValueError) as exc:
        parser.exit(1, str(exc) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
