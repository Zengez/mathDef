"""Synthetic, source-independent cycle regressions; never modify a live graph."""
import copy
import itertools
import json
from pathlib import Path
import tempfile
import unittest

from research_pipeline.engine.core import PipelineError, Workspace, digest
from research_pipeline.engine.dependency_cycle_analysis import analyze_cycles
from research_pipeline.engine.dependency_global_audit import (
    analyze_snapshot, load_live_snapshot, strongly_connected,
)
from research_pipeline.engine.dependency_graph import (
    inventory_sync, store, resolve, amend, meaning_version, missing_key,
)


def fixture(options):
    forms, nodes, meanings = {}, {}, {}
    for mid, variants in sorted(options.items()):
        meanings[mid] = {'display_term': mid, 'formulation_ids': []}
        for i, targets in enumerate(variants):
            fid = f'form.{mid}.{i}'
            meanings[mid]['formulation_ids'].append(fid)
            forms[fid] = {'meaning_id': mid, 'display_term': mid,
                'text': 'Synthetic structural example.', 'context': 'fixture',
                'version_sha256': digest([mid, i])}
            nodes[fid] = {'scan_status': 'complete',
                'version_sha256': forms[fid]['version_sha256'],
                'references': [{'state': 'existing', 'target_meaning_id': target,
                    'phrase': target, 'occurrence_id': f'{fid}.{j}'}
                    for j, target in enumerate(targets)]}
    return {'inventory': {'meanings': meanings, 'formulations': forms,
                         'seed_relations': [], 'source_inventory_sha256': 'fixture'},
            'nodes': nodes, 'state': {'summary': {}}, 'resolutions': [], 'aliases': []}


class CycleAnalysisTests(unittest.TestCase):
    def test_metric_open_ball_candidate_resolution_and_primitive_choice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            Workspace(root).init({'schema_version': 1, 'project': 'Synthetic cycle',
                'term_kind': 'term', 'content_kind': 'definition', 'adapter': 'mathdef',
                'external_reference_mode': True, 'independent_second_wave': True})
            records = root / 'records'
            meanings = [
                {'id': 'meaning.metric', 'display_term': 'Metric space',
                 'context': 'synthetic', 'formulations': [
                     {'id': 'form.metric.primitive', 'text': 'Distance axioms.'},
                     {'id': 'form.metric.compatible', 'text': 'Topology from open balls.'}]},
                {'id': 'meaning.ball', 'display_term': 'Open ball',
                 'context': 'synthetic', 'formulations': [
                     {'id': 'form.ball', 'text': 'Ball in a metric space.'}]}]
            (records / 'meanings.jsonl').write_text(''.join(json.dumps(m)+'\n' for m in meanings))
            (records / 'relations.jsonl').write_text('')
            inventory_sync(root)
            inv = load_live_snapshot(root)['inventory']
            cid = missing_key('open ball', 'synthetic')
            refs = {'form.metric.primitive': [], 'form.metric.compatible': [
                {'phrase': 'open ball', 'state': 'missing', 'context': 'synthetic'}],
                'form.ball': [{'phrase': 'metric space', 'state': 'existing',
                               'target_meaning_id': 'meaning.metric'}]}
            store(root, [{'formulation_id': fid, 'version_sha256': inv['formulations'][fid]['version_sha256'],
                'complete': True, 'review_rationale': 'Reviewed all references in this synthetic complete formulation.',
                'references': ref} for fid, ref in refs.items()])
            self.assertEqual(analyze_cycles(load_live_snapshot(root))['components'], [])
            resolve(root, [{'missing_candidate_id': cid, 'target_meaning_id': 'meaning.ball',
                'target_version_sha256': meaning_version(inv, 'meaning.ball'),
                'review_rationale': 'Explicit synthetic identity resolution for the cycle regression.'}])
            before = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
            snapshot = load_live_snapshot(root)
            report = analyze_snapshot(snapshot)
            analysis = report['cycle_analysis']
            actual = [json.loads(x) for x in (root/'dependency_graph/edges.jsonl').read_text().splitlines()]
            self.assertEqual([{k: e[k] for k in actual[0]} for e in analysis['edges']], actual)
            component = analysis['components'][0]
            self.assertEqual(component['classification'], 'avoidable_by_formulation_choice')
            self.assertIn({'meaning_id': 'meaning.metric', 'formulation_id': 'form.metric.primitive'},
                          component['acyclic_selection_witness'])
            self.assertTrue(any(e['origin'] == 'scan:candidate_resolution' for e in component['internal_edges']))
            self.assertEqual(report['summary']['effective_cycle_components'], 1)
            self.assertEqual(report['summary']['cycle_components'], 0)  # explicitly legacy scope
            self.assertEqual(before, {p: p.read_bytes() for p in root.rglob('*') if p.is_file()})
            snapshot['resolutions'][0]['target_version_sha256'] = 'stale'
            self.assertEqual(analyze_cycles(snapshot)['components'], [])
            # Only the disposable fixture is amended: the immutable original
            # primitive scan stays empty, but effective replay must now cycle.
            current = load_live_snapshot(root)
            fid = 'form.metric.primitive'
            amend(root, [{'amendment_id': 'amend.synthetic.cycle',
                'formulation_id': fid, 'version_sha256': inv['formulations'][fid]['version_sha256'],
                'expected_node_sha256': digest(current['nodes'][fid]),
                'complete': True, 'reviewed_by': 'fixture',
                'reason': 'Synthetic regression changes a fixture adjacency to test effective replay.',
                'review_rationale': 'Reviewed all synthetic references to test amended formulation adjacency.',
                'references': [{'state': 'existing', 'phrase': 'open ball',
                                'target_meaning_id': 'meaning.ball'}]}])
            self.assertEqual(analyze_cycles(load_live_snapshot(root))['components'][0]['classification'],
                             'unavoidable_under_stored_formulations')
            original = json.loads((root/'dependency_graph/nodes'/f'{fid}.json').read_text())
            self.assertEqual(original['references'], [])

    def test_unavoidable_disjunctive_core_has_no_common_required_edge(self):
        s = fixture({'a': [['b'], ['c']], 'b': [['a']], 'c': [['a']]})
        c = analyze_cycles(s)['components'][0]
        self.assertEqual(c['classification'], 'unavoidable_under_stored_formulations')
        self.assertEqual(c['blocking_core_meaning_ids'], ['a', 'b', 'c'])
        self.assertEqual(c['acyclic_selection_witness'], [])

    def test_self_loop_and_unknown_alternative(self):
        s = fixture({'a': [['a'], []]})
        self.assertEqual(analyze_cycles(s)['components'][0]['classification'], 'avoidable_by_formulation_choice')
        s['nodes']['form.a.1']['scan_status'] = 'unscanned'
        self.assertEqual(analyze_cycles(s)['components'][0]['classification'], 'undetermined_incomplete_formulations')
        del s['nodes']['form.a.1']
        self.assertEqual(analyze_cycles(s)['components'][0]['classification'], 'undetermined_incomplete_formulations')
        s = fixture({'a': [['a']]})
        self.assertEqual(analyze_cycles(s)['components'][0]['classification'], 'unavoidable_under_stored_formulations')

    def test_alias_chain_resolution_and_duplicate_rejection(self):
        s = fixture({'a': [['b']], 'b': [['a']]})
        first, middle, final = [missing_key(x, 'synthetic') for x in ('first', 'middle', 'final')]
        s['nodes']['form.a.0']['references'] = [
            {'state': 'missing', 'phrase': 'first', 'missing_candidate_id': first},
            {'state': 'missing', 'phrase': 'middle', 'missing_candidate_id': middle},
            {'state': 'missing', 'phrase': 'final', 'missing_candidate_id': final}]
        s['aliases'] = [{'alias_id': str(i), 'alias_candidate_id': a,
            'canonical_candidate_id': b, 'reviewed_by': 'fixture',
            'reason': 'Explicitly reviewed contextual identity for a synthetic regression.'}
            for i, (a,b) in enumerate([(first, middle), (middle, final)])]
        row = {'missing_candidate_id': final, 'target_meaning_id': 'b',
               'target_version_sha256': meaning_version(s['inventory'], 'b')}
        s['resolutions'] = [row]
        analysis = analyze_cycles(s)
        self.assertEqual(len(analysis['components']), 1)
        e = analysis['edges'][0]
        self.assertEqual(e['observed_missing_candidate_id'], first)
        self.assertEqual(e['resolved_missing_candidate_id'], final)
        s['resolutions'].append(copy.deepcopy(row))
        with self.assertRaisesRegex(PipelineError, 'Duplicate'):
            analyze_cycles(s)

    def test_seed_override_retains_provenance_removes_old_cycle(self):
        s = fixture({'a': [[]], 'b': [['a']]})
        seed = {'relation_id': 'rel.fixture', 'from_formulation': 'form.a.0',
                'target_meaning_id': 'b', 'phrase': 'historical dependency'}
        s['inventory']['seed_relations'] = [seed]
        self.assertEqual(len(analyze_cycles(s)['components']), 1)
        cid = missing_key('unpopulated concept', 'synthetic')
        s['nodes']['form.a.0']['references'] = [{'state': 'missing', 'phrase': 'unpopulated concept',
            'context': 'synthetic', 'missing_candidate_id': cid}]
        event = {'schema_version': 1, 'seed_override_id': 'override.fixture',
            'relation_id': seed['relation_id'], 'expected_seed_sha256': digest(seed),
            'expected_version_sha256': s['inventory']['formulations']['form.a.0']['version_sha256'],
            'expected_old_target_meaning_id': 'b', 'replacement': {'state': 'missing', 'missing_candidate_id': cid},
            'reviewed_by': 'fixture', 'review_rationale': 'Explicit contextual synthetic review of a historical seed with a separate missing prerequisite.'}
        s['seed_override_events'] = [event]
        self.assertEqual(analyze_cycles(s)['components'], [])
        from research_pipeline.engine.dependency_cycle_analysis import effective_references
        replaced = effective_references(s)[0]
        self.assertEqual(replaced['seed_override_id'], event['seed_override_id'])
        self.assertEqual(replaced['relation_id'], seed['relation_id'])
        event['expected_version_sha256'] = 'stale'
        self.assertEqual(len(analyze_cycles(s)['components']), 1)

    def test_seed_on_primitive_formulation_prevents_false_escape(self):
        s = fixture({'a': [[], ['b']], 'b': [['a']]})
        s['inventory']['seed_relations'] = [{'relation_id': 'rel.primitive',
            'from_formulation': 'form.a.0', 'target_meaning_id': 'b', 'phrase': 'b'}]
        c = analyze_cycles(s)['components'][0]
        self.assertEqual(c['classification'], 'unavoidable_under_stored_formulations')
        self.assertEqual(c['formulations']['form.a.0']['existing_dependencies'], ['b'])

    def test_fixed_point_matches_exhaustive_selection(self):
        # All pairs of dependency subsets for two alternatives of a, plus b.
        subsets = [[], ['a'], ['b'], ['a', 'b']]
        for a1, a2, b in itertools.product(subsets, repeat=3):
            s = fixture({'a': [a1, a2], 'b': [b]})
            original = copy.deepcopy(s)
            analysis = analyze_cycles(s)
            for component in analysis['components']:
                members = set(component['meaning_ids'])
                avoidable = any(not strongly_connected({'a': set(a) & members, 'b': set(b) & members})
                                for a in (a1, a2)) if len(members) == 2 else any(
                                    not (set(deps) & members)
                                    for deps in ([a1, a2] if 'a' in members else [b]))
                self.assertEqual(component['classification'] == 'avoidable_by_formulation_choice', avoidable)
            self.assertEqual(s, original)
            self.assertEqual(analysis, analyze_cycles(s))


if __name__ == '__main__':
    unittest.main()
