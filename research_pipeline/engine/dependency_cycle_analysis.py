"""Read-only effective-edge replay and exact OR-of-AND formulation analysis.

A formulation requires ALL its dependencies; a meaning may choose ONE stored
formulation. This is a structural model, not a judgment of mathematical validity
or interchangeability. Unknown/missing prerequisites are outside the existing-
meaning projection; no result certifies a closed definition expansion.
"""
from collections import defaultdict
from pathlib import Path

from .core import PipelineError, digest
from .dependency_graph import alias_map, meaning_version, missing_key, stable_id
from .dependency_seed_overrides import (
    effective_seed_reference, replay_seed_overrides, scan_missing_sources,
)


def effective_references(snapshot):
    """Mirror rebuild's read-only projection from replayed nodes and ledgers.

    Never trust derived edges or registry resolution status in place of the
    version-bound resolution ledger. Reuse the engine's alias/seed validators.
    """
    inv, nodes = snapshot['inventory'], snapshot['nodes']
    refs = defaultdict(list)
    available = set(scan_missing_sources(nodes))
    for seed in inv.get('seed_relations', []):
        if seed.get('target_query') and not seed.get('target_meaning_id'):
            available.add(missing_key(seed['target_query'],
                inv['formulations'][seed['from_formulation']]['context']))
    aliases = alias_map(Path('.'), available, events=snapshot.get('aliases', []))
    resolutions = {}
    seen = set()
    rows = snapshot.get('resolutions', [])
    for row in rows:
        cid, mid = row['missing_candidate_id'], row['target_meaning_id']
        if cid in seen:
            raise PipelineError('Duplicate append-only candidate resolution ' + cid)
        seen.add(cid)
        if cid not in available or mid not in inv['meanings']:
            continue
        if cid in aliases:
            raise PipelineError('An aliased missing candidate cannot own a resolution')
        if row.get('target_version_sha256') == meaning_version(inv, mid):
            resolutions[cid] = row
    overrides = replay_seed_overrides(inv, snapshot.get('seed_override_events', []),
        scan_missing_sources(nodes, aliases),
        aliased={r['alias_candidate_id'] for r in snapshot.get('aliases', [])},
        resolved={r['missing_candidate_id'] for r in rows})
    for seed in inv.get('seed_relations', []):
        fid = seed['from_formulation']
        ref = effective_seed_reference({'phrase': '', **seed}, overrides.get(seed['relation_id']),
                                       stable_id('seed', seed['relation_id']))
        if 'state' not in ref:
            if not seed.get('target_query'):
                continue
            ref.update(state='missing', missing_candidate_id=missing_key(
                seed['target_query'], inv['formulations'][fid]['context']))
        refs[fid].append(ref)
    for fid, node in sorted(nodes.items()):
        refs[fid].extend(node['references'])
    effective = []
    for fid in sorted(refs):
        for original in refs[fid]:
            ref = dict(original)
            if ref['state'] == 'missing':
                cid = ref['missing_candidate_id']
                if cid in aliases:
                    ref.update(observed_missing_candidate_id=cid,
                               missing_candidate_id=aliases[cid])
                cid = ref['missing_candidate_id']
                if cid in resolutions:
                    ref.update(state='existing',
                        target_meaning_id=resolutions[cid]['target_meaning_id'],
                        resolved_missing_candidate_id=cid,
                        origin=ref.get('origin', 'scan') + ':candidate_resolution')
            effective.append({'from_formulation': fid, **ref})
    return effective


def analyze_cycles(snapshot):
    """Analyze union SCCs and decide acyclic selection within each SCC exactly.

    Least fixed point: remove a meaning when one complete, version-valid
    formulation has no dependencies remaining in the SCC. Removal order and
    chosen formulations witness an acyclic selection. If no removal is possible
    and all alternatives are known, every possible selection has a finite
    nonempty subgraph with positive outdegree, hence a cycle. This does NOT
    require a particular edge or cycle to be common to every selection.
    """
    from .dependency_global_audit import strongly_connected
    inv, nodes = snapshot['inventory'], snapshot['nodes']
    forms, meanings = inv['formulations'], inv['meanings']
    references = effective_references(snapshot)
    adjacency = {mid: set() for mid in meanings}
    by_form = defaultdict(set)
    edges = []
    unresolved = defaultdict(list)
    invalid = set()
    for ref in references:
        fid = ref['from_formulation']
        if fid not in forms:
            raise PipelineError('Unknown source formulation in cycle analysis: ' + fid)
        if ref['state'] == 'existing':
            target = ref['target_meaning_id']
            if target not in meanings:
                invalid.add(fid)
                continue  # Global auditor separately reports unknown targets.
            source = forms[fid]['meaning_id']
            adjacency[source].add(target)
            by_form[fid].add(target)
            edges.append({**ref, 'source_meaning_id': source,
                'origin': ref.get('origin', 'scan'),
                'version_sha256': forms[fid]['version_sha256'],
                'effective_node_sha256': digest(nodes[fid]) if fid in nodes else None})
        elif ref['state'] != 'external':
            unresolved[fid].append(ref)
    alternatives = defaultdict(list)
    eligible = set()
    for fid, source in sorted(forms.items()):
        alternatives[source['meaning_id']].append(fid)
        node = nodes.get(fid, {})
        if (node.get('scan_status') == 'complete' and fid not in invalid
                and node.get('version_sha256') == source['version_sha256']):
            eligible.add(fid)
    components = []
    for members in strongly_connected(adjacency):
        remaining = set(members)
        witness = []
        while remaining:
            choices = [(mid, fid) for mid in sorted(remaining)
                       for fid in alternatives[mid] if fid in eligible
                       and not (by_form[fid] & remaining)]
            if not choices:
                break
            mid, fid = choices[0]
            remaining.remove(mid)
            witness.append({'meaning_id': mid, 'formulation_id': fid})
        unknown = sorted(fid for mid in members for fid in alternatives[mid]
                         if fid not in eligible)
        no_alternatives = sorted(mid for mid in members if not alternatives[mid])
        classification = ('avoidable_by_formulation_choice' if not remaining else
                          'undetermined_incomplete_formulations' if unknown or no_alternatives
                          else 'unavoidable_under_stored_formulations')
        member_set = set(members)
        diagnostics = {}
        for mid in members:
            for fid in alternatives[mid]:
                diagnostics[fid] = {
                    'meaning_id': mid, 'eligible_complete_scan': fid in eligible,
                    'source': forms[fid],
                    'effective_node_sha256': digest(nodes[fid]) if fid in nodes else None,
                    'existing_dependencies': sorted(by_form[fid]),
                    'remaining_core_dependencies': sorted(by_form[fid] & remaining),
                    'unresolved_references': unresolved[fid],
                }
        components.append({'meaning_ids': members, 'classification': classification,
            'acyclic_selection_witness': witness if not remaining else [],
            'elimination_prefix': witness, 'blocking_core_meaning_ids': sorted(remaining),
            'incomplete_formulation_ids': unknown, 'meanings_without_formulations': no_alternatives,
            'formulations': diagnostics,
            'internal_edges': [e for e in edges if e['source_meaning_id'] in member_set
                               and e['target_meaning_id'] in member_set],
            'requires_mathematical_review': True})
    return {'graph_kind': 'union_of_all_effective_existing_meaning_dependencies',
        'includes_candidate_resolutions': True, 'includes_historical_seed_overrides': True,
        'choice_model': 'one complete stored formulation per meaning; all its scan and seed edges retained',
        'scope': 'Existing-meaning projection only. Missing, ambiguous, deferred and unassigned prerequisites are not assumed closed. Stored alternatives are not certified interchangeable.',
        'mathematics_certified': False, 'components': components, 'edges': edges}
