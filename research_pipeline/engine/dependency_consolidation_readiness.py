"""Read-only Pass 2 evidence assessment; never seals a gate or starts research.

Uses existing replay, provenance and consistency tools. Mechanical eligibility
is distinct from the reviewer's global contextual-consolidation decision.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

from .core import PipelineError, Workspace, digest
from .dependency_consistency_worklist import build_worklist, _QUALIFIERS, _has, _object_words
from .dependency_audit_acceleration import rank_findings
from .dependency_cycle_analysis import effective_references
from .dependency_global_audit import candidate_review_bundle, jsonl, load_live_snapshot
from .dependency_graph import (
    alias_map, amendment_events, collect, graph_path, meaning_version,
    missing_key, read, unresolved_fingerprint, _reference_state,
)
from .dependency_provenance_audit import summarize_provenance
from .population import snapshot as population_snapshot


def load_inputs(workspace):
    """Load only this independent workspace; source freshness is checked too."""
    workspace = Path(workspace)
    graph = graph_path(workspace)
    entries, meanings, seeds, _ = collect(workspace)  # read-only, validates scope
    draft, _ = population_snapshot(workspace)
    base = Workspace(workspace)
    required = ('occurrences.jsonl', 'edges.jsonl', 'unresolved_occurrences.jsonl',
                'reverse_index.json', 'CHECKPOINT.json', 'missing_candidates.jsonl')
    for name in required:
        if not (graph / name).is_file():
            raise PipelineError('Missing required derived graph file: ' + name)
    amendments = amendment_events(graph)
    return {'graph': load_live_snapshot(workspace),
        'current_formulations': entries,
        'current_meanings': {mid: {'display_term': m['display_term'], 'context': m['context'],
            'formulation_ids': [f['id'] for f in m.get('formulations', [])]}
            for mid, m in sorted(meanings.items())},
        'current_seeds': seeds,
        'observations': {**base.records('observations'), **draft['observations']},
        'sources': {**base.records('sources'), **draft['sources']},
        'source_issues': list(draft['issues'].values()),
        'population_reviews': list(draft['reviews'].values()),
        'amendment_event_count': len(amendments),
        'amendment_ledger_sha256': digest(amendments),
        'stored': {**{name: jsonl(graph / (name + '.jsonl'))
                     for name in ('occurrences', 'edges', 'unresolved_occurrences')},
            'reverse_index': read(graph / 'reverse_index.json'),
            'checkpoint': read(graph / 'CHECKPOINT.json'),
            'existing_consolidation_record': read(graph / 'CONSOLIDATION.json')}}


def assess(inputs, *, limit=12, exhaustive=False):
    """Return checks and contextual decisions; missing meanings are not defects."""
    if limit < 0:
        raise PipelineError('Review limit must be nonnegative')
    s = inputs['graph']
    inv, nodes, candidates = s['inventory'], s['nodes'], s['candidates']
    forms = inv['formulations']
    failures = []
    checks = {}

    def check(code, passed, detail=None):
        checks[code] = bool(passed)
        if not passed:
            failures.append({'code': code, 'evidence': detail})

    anchors = {'inventory_sha256': inv['source_inventory_sha256'],
        'state_unresolved_fingerprint': s['state']['summary'].get('unresolved_fingerprint'),
        'assessment_evidence_sha256': digest(inputs)}
    # Fail closed on malformed identity/review ledgers, retaining evidence ID.
    try:
        references = sorted(effective_references(s), key=lambda r: (
            r['from_formulation'], r['occurrence_id']))
        worklist = build_worklist(s, limit=limit, exhaustive=exhaustive)
    except (PipelineError, KeyError, TypeError, ValueError) as error:
        return {'schema_version': 1, 'read_only': True, **anchors,
            'status': 'blocked_by_mechanical_integrity', 'pass2_complete': 'not_determined',
            'pass3_authorized_by_this_assessment': False,
            'mechanical_integrity_failures': [{'code': 'invalid_graph_or_review_ledger',
                                               'evidence': str(error)}],
            'assessment_incomplete': True}
    stored = inputs['stored']
    unresolved = [r for r in references if r['state'] in ('missing', 'unassigned', 'ambiguous', 'deferred')]
    counts = Counter(r['state'] for r in references)
    fp = unresolved_fingerprint(inv, unresolved, candidates)
    anchors['recomputed_unresolved_fingerprint'] = fp
    check('inventory_matches_current_sources', forms == inputs['current_formulations']
          and inv['meanings'] == inputs['current_meanings']
          and inv.get('seed_relations', []) == inputs['current_seeds'])
    check('inventory_digest_valid', inv['source_inventory_sha256'] == digest(forms)
          and inv.get('seed_relations_sha256') == digest(inv.get('seed_relations', [])))
    complete = sum(nodes.get(fid, {}).get('scan_status') == 'complete'
                   and nodes[fid].get('version_sha256') == f['version_sha256']
                   for fid, f in forms.items())
    check('all_scans_complete', complete == len(forms), {'complete': complete, 'total': len(forms)})
    check('zero_unassigned', counts['unassigned'] == 0, counts['unassigned'])
    check('zero_ambiguous', counts['ambiguous'] == 0, counts['ambiguous'])
    ids = [r['occurrence_id'] for r in references]
    check('unique_occurrence_identities', len(ids) == len(set(ids)))
    check('occurrence_index_matches_replay', stored['occurrences'] == references)
    check('unresolved_index_matches_replay', stored['unresolved_occurrences'] == unresolved)
    edges = [{'from_formulation': r['from_formulation'], 'target_meaning_id': r['target_meaning_id'],
              'occurrence_id': r['occurrence_id'], 'origin': r.get('origin', 'scan')}
             for r in references if r['state'] == 'existing']
    check('edge_index_matches_replay', stored['edges'] == edges)
    summary = s['state']['summary']
    expected_counts = {'total_formulations': len(forms), 'total_meanings': len(inv['meanings']),
        'scan_complete': complete, 'missing_candidates': len(candidates),
        'unassigned_occurrences': counts['unassigned'], 'ambiguous_occurrences': counts['ambiguous'],
        'missing_occurrences': counts['missing'], 'scan_amendment_event_count': inputs['amendment_event_count']}
    check('state_counts_match_replay', all(summary.get(k) == v for k, v in expected_counts.items()), expected_counts)
    check('state_fingerprint_matches_replay', summary.get('unresolved_fingerprint') == fp
          and summary.get('inventory_sha256') == inv['source_inventory_sha256'])
    cp = stored['checkpoint']
    check('checkpoint_matches_state', cp.get('inventory_sha256') == inv['source_inventory_sha256']
          and cp.get('state_sha256') == digest(s['state'].get('formulations', {}))
          and cp.get('valid_node_snapshot_count') == len(nodes)
          and cp.get('scan_amendment_event_count') == inputs['amendment_event_count'])

    # Check registry identity/status/counts against the existing replay model.
    raw = set()
    for node in nodes.values():
        raw.update(r['missing_candidate_id'] for r in node['references'] if r['state'] == 'missing')
    for seed in inv.get('seed_relations', []):
        if seed.get('target_query') and not seed.get('target_meaning_id'):
            raw.add(missing_key(seed['target_query'], forms[seed['from_formulation']]['context']))
    aliases = alias_map(Path('.'), raw, events=s.get('aliases', []))
    resolutions = {r['missing_candidate_id']: r['target_meaning_id'] for r in s.get('resolutions', [])
        if r['missing_candidate_id'] in raw and r['target_meaning_id'] in inv['meanings']
        and r.get('target_version_sha256') == meaning_version(inv, r['target_meaning_id'])}
    by_candidate, by_form = defaultdict(list), defaultdict(list)
    reverse = defaultdict(set)
    for r in references:
        fid = r['from_formulation']
        by_form[fid].append(r)
        if r.get('missing_candidate_id'):
            by_candidate[r['missing_candidate_id']].append(r)
        if r.get('observed_missing_candidate_id'):
            reverse['missing-alias:' + r['observed_missing_candidate_id']].add(fid)
        if r.get('resolved_missing_candidate_id'):
            reverse['missing:' + r['resolved_missing_candidate_id']].add(fid)
        if r['state'] == 'existing':
            reverse['meaning:' + r['target_meaning_id']].add(fid)
        elif r['state'] == 'missing':
            reverse['missing:' + r['missing_candidate_id']].add(fid)
    check('reverse_index_matches_replay', stored['reverse_index'] == {k: sorted(v) for k,v in reverse.items()})
    registry = {c['id']: c for c in candidates}
    check('registry_identity_set_matches_replay', len(registry) == len(candidates) and set(registry) == raw)
    mismatches = []
    for cid, c in sorted(registry.items()):
        incoming = sorted({r['from_formulation'] for r in by_candidate[cid]})
        expected = {'alias_of': aliases.get(cid),
            'alias_ids': sorted(a for a, target in aliases.items() if target == cid),
            'status': 'alias' if cid in aliases else 'resolved' if cid in resolutions else 'unresearched',
            'resolved_target_meaning_id': resolutions.get(cid),
            'occurrence_count': len(by_candidate[cid]), 'incoming_formulation_ids': incoming,
            'upstream_formulation_count': len(incoming)}
        if any(c.get(k) != v for k, v in expected.items()):
            mismatches.append({'candidate_id': cid, 'expected': expected})
    check('registry_metadata_matches_replay', not mismatches, mismatches)
    invalid_refs = []
    for ref in references:
        try:
            _reference_state(ref, inv['meanings'], registry)
        except PipelineError as error:
            invalid_refs.append({'occurrence_id': ref['occurrence_id'],
                'from_formulation': ref['from_formulation'], 'reason': str(error)})
    check('reference_dispositions_valid', not invalid_refs, invalid_refs)
    check('canonical_and_alias_counts_match_state',
          summary.get('unresolved_missing_candidates') == sum(c['status'] == 'unresearched' for c in candidates)
          and summary.get('alias_candidate_records') == len(aliases))

    for f in worklist['findings']:
        if f['severity'] == 'integrity':
            failures.append({'code': f['code'], 'evidence': f})
    # The bounded worklist can hide later integrity findings; the count still
    # supplies a fail-closed signal without interpreting heuristic leads as gates.
    check('existing_integrity_audit_passed', worklist['summary']['mechanical_integrity_count'] == 0,
          worklist['summary']['mechanical_integrity_count'])
    provenance = summarize_provenance(inv, inputs['observations'], inputs['sources'],
                                     example_limit=len(forms))
    check('provenance_record_links_exist', not provenance['missing_evidence_records']
          and not provenance['missing_source_records'], provenance['examples'])

    untraceable = set(provenance['examples']['zero_evidence'])
    for category in ('missing_observations', 'missing_sources', 'missing_locators'):
        untraceable.update(r['formulation_id'] for r in provenance['examples'][category])
    canonical = [c for c in candidates if c.get('status') == 'unresearched' and not c.get('alias_of')]
    decisions = []
    for c in sorted(canonical, key=lambda c: (-c.get('occurrence_count', 0), c['id'])):
        cid = c['id']
        rows = [r for r in by_candidate[cid] if r['state'] == 'missing']
        concerns = []
        if not rows or not str(c.get('context', '')).strip():
            concerns.append('missing_context_or_live_occurrence')
        if any(r['from_formulation'] in untraceable for r in rows):
            concerns.append('source_traceability_needs_review')
        # A broad domain difference alone is legitimate. Flag only opposing,
        # explicit qualifier uses on shared object words, never synonymy.
        for axis, pair in _QUALIFIERS.items():
            sides = [[r for r in rows if _has(r.get('phrase', ''), q)
                      and not _has(r.get('phrase', ''), pair[1-i])]
                     for i, q in enumerate(pair)]
            if any(_object_words(a.get('phrase', '')) & _object_words(b.get('phrase', ''))
                   for a in sides[0] for b in sides[1]):
                concerns.append('explicit_candidate_' + axis + '_contrast')
        if concerns:
            decisions.append({'candidate_id': cid, 'concerns': concerns,
                'candidate': c, 'occurrences': rows,
                'reviewed_alias_events': [e for e in s.get('aliases', [])
                    if aliases.get(e['alias_candidate_id']) == cid],
                'sources': {r['from_formulation']: forms[r['from_formulation']] for r in rows},
                'effective_node_sha256': {r['from_formulation']: digest(nodes[r['from_formulation']])
                                         for r in rows if r['from_formulation'] in nodes},
                'evidence_sha256': digest([c, rows, {r['from_formulation']: forms[r['from_formulation']] for r in rows}]),
                'interpretation': 'Contextual review lead, not an alias error or automatic consolidation blocker.'})
    for d in decisions:
        primary = min(d['occurrences'], key=lambda r: (r['from_formulation'], r['occurrence_id'])) if d['occurrences'] else None
        if primary is None:
            # Orphan identities already fail the mechanical registry check;
            # no invented source anchor can authorize acceptance of them.
            continue
        fid = primary['from_formulation']
        d.update(severity='review', code='candidate_identity_context_review',
            formulation_id=fid, occurrence_id=primary['occurrence_id'],
            version_sha256=forms[fid]['version_sha256'],
            effective_node_sha256=digest(nodes[fid]) if fid in nodes else None,
            description='; '.join(d['concerns']), source_text=forms[fid]['text'],
            source_context=forms[fid].get('context', ''))
        d['evidence_sha256'] = digest([d['evidence_sha256'], d['effective_node_sha256'],
            d['reviewed_alias_events'], {r['from_formulation']: digest(nodes.get(r['from_formulation']))
                                  for r in d['occurrences']}])
    reviewed = rank_findings([d for d in decisions if 'formulation_id' in d], nodes, inv,
                            s.get('review_ledger', []))
    accepted_candidates = reviewed['accepted_count']
    decisions = [d for d in decisions if 'formulation_id' not in d] + reviewed['needing_review']
    decisions.sort(key=lambda d: (not any(c.startswith('explicit_candidate_') for c in d['concerns']),
                                 -d['candidate']['occurrence_count'], d['candidate_id']))
    selected = decisions if exhaustive else decisions[:limit]
    # Reuse the existing recurrence-ranked candidate focus and disclose omitted
    # parent contexts. Replace its raw scan references with full effective rows.
    focus = candidate_review_bundle(s, limit=len(canonical) if exhaustive else limit,
                                   max_formulations=max(1, len(forms)) if exhaustive else 3)
    missing_examples = []
    for item in focus['candidates']:
        cid = item['candidate_id']
        selected_fids = {f['formulation_id'] for f in item['source_formulations']}
        shown = [r for r in by_candidate[cid] if r['from_formulation'] in selected_fids]
        missing_examples.append({'candidate': registry[cid], 'occurrences': shown,
            'sources': {fid: forms[fid] for fid in sorted(selected_fids) if fid in forms},
            'source_formulations_omitted': item['sources_truncated'],
            'occurrences_omitted': len(by_candidate[cid]) - len(shown)})
    gate = stored['existing_consolidation_record']
    gate_matches = bool(gate and gate.get('inventory_sha256') == inv['source_inventory_sha256']
        and gate.get('unresolved_fingerprint') == fp and str(gate.get('reviewed_by', '')).strip()
        and len(str(gate.get('rationale', '')).strip()) >= 40 and gate.get('schema_version') == 1)
    gate_prerequisite_codes = {'all_scans_complete', 'zero_unassigned', 'zero_ambiguous'}
    integrity_failures = [f for f in failures if f['code'] not in gate_prerequisite_codes]
    unmet_prerequisites = [f for f in failures if f['code'] in gate_prerequisite_codes]
    context_fids = set(worklist['source_formulations'])
    for target in worklist['target_meanings'].values():
        context_fids.update(target['formulations'])
    for d in selected:
        context_fids.update(d['sources'])
    for example in missing_examples:
        context_fids.update(example['sources'])
    evidence_ids = {eid for fid in context_fids for eid in forms[fid].get('evidence_ids', [])}
    observations = {eid: inputs['observations'][eid] for eid in sorted(evidence_ids) if eid in inputs['observations']}
    source_ids = {o.get('source_id') for o in observations.values() if o.get('source_id')}
    return {'schema_version': 1, 'read_only': True, **anchors,
        'status': ('blocked_by_mechanical_integrity' if integrity_failures else
                   'blocked_by_unmet_gate_prerequisites' if unmet_prerequisites else
                   'mechanical_checks_passed_review_decision_required'),
        'pass2_complete': 'not_determined', 'pass3_authorized_by_this_assessment': False,
        'mechanical_checks': checks, 'mechanical_integrity_failures': integrity_failures,
        'unmet_gate_prerequisites': unmet_prerequisites,
        'gate_contract': {'implementation': 'dependency_graph.seal_consolidation',
            'all_scans_complete': checks['all_scans_complete'], 'zero_unassigned': checks['zero_unassigned'],
            'zero_ambiguous': checks['zero_ambiguous'], 'exact_scope_fingerprints_verified': (checks['state_fingerprint_matches_replay']
                and checks['inventory_matches_current_sources'] and checks['inventory_digest_valid']),
            'named_reviewer_and_substantive_global_rationale_required': True,
            'zero_missing_candidates_required': False, 'zero_deferred_occurrences_required': False,
            'existing_record_present': gate is not None, 'existing_record_matches_scope': gate_matches,
            'gate_written_by_assessment': False},
        'counts': {**expected_counts, 'canonical_missing_candidates': len(canonical),
            'alias_events': len(s.get('aliases', [])), 'effective_aliases': len(aliases),
            'resolution_events': len(s.get('resolutions', [])), 'effective_resolutions': len(resolutions),
            'inactive_resolution_events': len(s.get('resolutions', [])) - len(resolutions),
            'seed_override_events': len(s.get('seed_override_events', [])),
            'effective_seed_overrides': len({r['seed_override_id'] for r in references if r.get('seed_override_id')}),
            'deferred_occurrences': counts['deferred'], 'explicit_candidate_review_leads': len(decisions)},
        'provenance': provenance,
        'existing_review_evidence': {'audit_ledger_rows': len(s.get('review_ledger', [])),
            'reviewed_alias_events': len(s.get('aliases', [])),
            'population_review_status_counts': dict(sorted(Counter(r.get('status', 'unspecified')
                for r in inputs['population_reviews']).items())),
            'interpretation': 'Alias and individual review records are evidence of specific reviews, not an exhaustive coverage certificate. Missing per-candidate acceptance does not prove a candidate was never reviewed.'},
        'mathematical_consistency_review': worklist,
        'candidate_review': {'total': len(decisions), 'returned': len(selected),
            'omitted': len(decisions) - len(selected), 'accepted_review_count': accepted_candidates, 'leads': selected},
        'classified_missing_prerequisites': {'count': len(canonical),
            'interpretation': 'Registered missing identities, not unassigned references. Eligible for consideration as Pass 3 research inputs only after a separate authorized consolidation decision; mathematical legitimacy is not certified here.',
            'examples': missing_examples, 'omitted': len(canonical) - len(missing_examples),
            'source_context_limit_per_candidate': None if exhaustive else 3},
        'selected_source_evidence': {'observations': observations,
            'sources': {sid: inputs['sources'][sid] for sid in sorted(source_ids) if sid in inputs['sources']}},
        'source_issues_for_deferral_decision': [{'record': issue,
            'source_context': {fid: forms[fid] for fid in forms if fid == issue.get('related_formulation_id')
                               or forms[fid]['meaning_id'] == issue.get('related_meaning_id')},
            'record_sha256': digest(issue), 'deferral_adopted_by_assessment': False}
            for issue in sorted(inputs['source_issues'], key=lambda x: x['id']) if issue.get('status') == 'open'],
        'remaining_decisions': [
            'Provide an exact-scope global contextual review rationale; counts and existing aliases do not prove every canonical identity was reviewed.',
            'Triage remaining consistency and candidate-context leads as accepted, correction-needed or explicitly deferred; heuristic counts are not additional hard gate requirements.',
            'Document disposition and phase for open source/variant issues without silently changing their definitions or links.',
            'Deferred references are permitted by the executable gate but require explicit contextual justification; they do not become missing identities automatically.'],
        'uncertainties': ['Paraphrases with locators are not externally verified source text.',
            'No automatic proof of candidate equivalence, missing-meaning legitimacy or full mathematical correctness.',
            'The review ledger records accepted individual leads, not exhaustive Pass 2 coverage.',
            'No gate creation, phase transition or missing-definition research is authorized by this output.']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace', type=Path, required=True)
    group = p.add_mutually_exclusive_group()
    group.add_argument('--limit', type=int, default=12)
    group.add_argument('--exhaustive', action='store_true')
    args = p.parse_args()
    try:
        result = assess(load_inputs(args.workspace), limit=args.limit, exhaustive=args.exhaustive)
    except (PipelineError, ValueError, KeyError, TypeError, OSError) as error:
        result = {'read_only': True, 'status': 'assessment_failed', 'assessment_incomplete': True,
                  'pass3_authorized_by_this_assessment': False, 'error': str(error)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result['status'] in ('assessment_failed', 'blocked_by_mechanical_integrity', 'blocked_by_unmet_gate_prerequisites'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
