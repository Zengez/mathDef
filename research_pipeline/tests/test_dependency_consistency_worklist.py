"""Synthetic mathematical contrasts and review-anchor regression controls."""
import copy
import io
import json
import sys
import unittest
from unittest.mock import patch

from research_pipeline.engine.core import PipelineError, digest
from research_pipeline.engine.dependency_audit_acceleration import audit_fingerprint
from research_pipeline.engine.dependency_consistency_worklist import build_worklist, main
from research_pipeline.engine.dependency_graph import meaning_version, missing_key
from research_pipeline.tests.test_dependency_cycle_analysis import fixture


def linked(phrase='category C', target='small category', text='An object of a category C.'):
    s = fixture({'s': [[]], 't': [[]], 'u': [[]]})
    s['inventory']['meanings']['t']['display_term'] = target
    s['inventory']['formulations']['form.s.0']['text'] = text
    s['inventory']['formulations']['form.t.0']['text'] = 'Synthetic target definition: ' + target
    s['nodes']['form.s.0']['references'] = [{'state': 'existing', 'phrase': phrase,
        'target_meaning_id': 't', 'occurrence_id': 'occ.fixture'}]
    return s


def codes(s):
    return {f['code'] for f in build_worklist(s, exhaustive=True)['findings']}


def review(f):
    return {**audit_fingerprint(f), 'disposition': 'accepted_as_correct',
        'reviewed_by': 'synthetic reviewer',
        'rationale': 'Reviewed the complete source, all related edges and target context; this synthetic lead is intentional.'}


class ConsistencyWorklistTests(unittest.TestCase):
    def test_explicit_opposites_and_negative_controls(self):
        for phrase, target in [('left group action', 'right group action'),
                               ('covariant functor', 'contravariant functor'),
                               ('unital ring', 'nonunital ring'),
                               ('empty-allowed space', 'nonempty space')]:
            with self.subTest(phrase=phrase):
                self.assertIn('explicit_qualifier_contrast', codes(linked(phrase, target)))
                self.assertNotIn('explicit_qualifier_contrast', codes(linked(target, target)))
        self.assertNotIn('explicit_qualifier_contrast', codes(linked(
            'unital left module', 'left module over a ring, optionally nonunital')))
        self.assertNotIn('explicit_qualifier_contrast', codes(linked(
            'left group action', 'right adjoint functor')))

    def test_smallness_absence_is_only_a_textual_lead(self):
        s = linked()
        result = build_worklist(s)
        f = result['findings'][0]
        self.assertEqual(f['code'], 'target_restriction_not_explicit')
        self.assertFalse(f['mathematics_confirmed'])
        self.assertIn('not proof', f['description'])
        self.assertIn('t', result['target_meanings'])
        self.assertEqual(result['target_meanings']['t']['formulations']['form.t.0']['text'],
                         'Synthetic target definition: small category')
        for text in ('For a small category C.', 'For a finite category C.',
                     'The indexing category I has finitely many objects and finitely many morphisms.'):
            self.assertNotIn('target_restriction_not_explicit', codes(linked(text=text)))
        self.assertNotIn('target_restriction_not_explicit', codes(linked(
            'finite-type ring map', 'ring map of finite type', 'A finite-type ring map.')))

    def test_restriction_must_qualify_the_target_head(self):
        self.assertNotIn('target_restriction_not_explicit', codes(linked(
            'unit of a quotient ring', 'unit of a unital ring', 'An element is invertible in the quotient.')))

    def test_subset_predicate_ambient_target_and_corrected_control(self):
        s = linked('clopen subset U', 'topological space', 'U is open and closed in X.')
        self.assertIn('subset_predicate_to_ambient_space', codes(s))
        s['inventory']['meanings']['t']['display_term'] = 'clopen subset'
        self.assertNotIn('subset_predicate_to_ambient_space', codes(s))
        self.assertNotIn('subset_predicate_to_ambient_space', codes(linked(
            'topological space X', 'topological space')))
        self.assertNotIn('explicit_qualifier_contrast', codes(linked(
            'bounded linear operator', 'linear map')))

    def test_ambient_definition_explicitly_defines_open_subsets(self):
        s = linked('open subset U', 'topological space')
        self.assertIn('subset_predicate_to_ambient_space', codes(s))
        s['inventory']['formulations']['form.t.0']['text'] = 'The members of the topology are the open subsets of X.'
        self.assertNotIn('subset_predicate_to_ambient_space', codes(s))

    def test_historical_seed_comparison_preserves_occurrences(self):
        s = linked('ambient object', 'general construction')
        s['inventory']['seed_relations'] = [{'relation_id': 'rel.synthetic',
            'from_formulation': 'form.s.0', 'target_meaning_id': 'u', 'phrase': 'ambient object'}]
        r = build_worklist(s, exhaustive=True)
        f = next(f for f in r['findings'] if f['code'] == 'seed_scan_target_disagreement')
        self.assertEqual(f['occurrence_id'], 'occ.fixture')
        self.assertEqual(f['target_meaning_ids'], ['t', 'u'])
        self.assertEqual(len(f['related_references']), 2)
        self.assertTrue(any(e.get('relation_id') == 'rel.synthetic' for e in f['related_references']))
        s['inventory']['seed_relations'][0]['target_meaning_id'] = 't'
        self.assertNotIn('seed_scan_target_disagreement', codes(s))

    def test_corrected_seed_override_does_not_resurrect_old_target(self):
        s = linked('closed subset U', 'topological space')
        cid = missing_key('closed subset U', 'fixture')
        s['nodes']['form.s.0']['references'] = [{'state': 'missing',
            'phrase': 'closed subset U', 'context': 'fixture',
            'missing_candidate_id': cid, 'occurrence_id': 'occ.fixture'}]
        s['candidates'] = [{'id': cid}]
        seed = {'relation_id': 'rel.corrected', 'from_formulation': 'form.s.0',
                'target_meaning_id': 't', 'phrase': 'closed subset U'}
        s['inventory']['seed_relations'] = [seed]
        self.assertIn('subset_predicate_to_ambient_space', codes(s))
        s['seed_override_events'] = [{'schema_version': 1, 'seed_override_id': 'override.fixture',
            'relation_id': seed['relation_id'], 'expected_seed_sha256': digest(seed),
            'expected_version_sha256': s['inventory']['formulations']['form.s.0']['version_sha256'],
            'expected_old_target_meaning_id': 't', 'replacement': {'state': 'missing', 'missing_candidate_id': cid},
            'reviewed_by': 'fixture', 'review_rationale': 'Explicit contextual synthetic review preserves the subset predicate as a separate missing prerequisite.'}]
        self.assertNotIn('subset_predicate_to_ambient_space', codes(s))

    def test_variant_context_differences_not_dependency_set_differences(self):
        s = fixture({'s': [['t'], ['u']], 't': [[]], 'u': [[]]})
        # Different reference phrases alone are not a concern.
        self.assertNotIn('variant_phrase_target_difference', codes(s))
        for fid in ('form.s.0', 'form.s.1'):
            s['nodes'][fid]['references'][0]['phrase'] = 'a contextual prerequisite'
        r = build_worklist(s, exhaustive=True)
        f = next(f for f in r['findings'] if f['code'] == 'variant_phrase_target_difference')
        self.assertEqual(f['related_formulation_ids'], ['form.s.0', 'form.s.1'])
        self.assertIn('form.s.1', r['source_formulations'])
        self.assertIn('need not', f['description'])

    def test_version_valid_resolution_and_alias_reach_diagnostic(self):
        s = linked('closed subset U', 'topological space')
        raw, final = missing_key('closed subset U', 'fixture'), missing_key('closed predicate', 'fixture')
        s['nodes']['form.s.0']['references'] = [dict(s['nodes']['form.s.0']['references'][0],
            state='missing', missing_candidate_id=raw, context='fixture')]
        s['nodes']['form.u.0']['references'] = [{'state': 'missing', 'phrase': 'closed predicate',
            'missing_candidate_id': final, 'context': 'fixture', 'occurrence_id': 'occ.other'}]
        s['candidates'] = [{'id': raw, 'alias_of': final}, {'id': final}]
        s['aliases'] = [{'alias_id': 'alias.fixture', 'alias_candidate_id': raw,
            'canonical_candidate_id': final, 'reviewed_by': 'fixture',
            'reason': 'Synthetic explicit contextual review links these two observed candidates.'}]
        s['resolutions'] = [{'missing_candidate_id': final, 'target_meaning_id': 't',
            'target_version_sha256': meaning_version(s['inventory'], 't')}]
        r = build_worklist(s, exhaustive=True)
        f = next(f for f in r['findings'] if f['code'] == 'subset_predicate_to_ambient_space')
        self.assertEqual(f['reference']['observed_missing_candidate_id'], raw)
        self.assertEqual(f['reference']['resolved_missing_candidate_id'], final)
        self.assertEqual(f['reference']['origin'], 'scan:candidate_resolution')
        s['resolutions'][0]['target_version_sha256'] = 'stale'
        self.assertNotIn('subset_predicate_to_ambient_space', codes(s))

    def test_review_suppression_and_target_evidence_staleness(self):
        s = linked()
        f = build_worklist(s)['findings'][0]
        s['review_ledger'] = [review(f)]
        r = build_worklist(s)
        self.assertEqual(r['findings'], [])
        self.assertEqual(r['summary']['accepted_count'], 1)
        s['inventory']['formulations']['form.t.0']['text'] += ' Revised target hypothesis.'
        r = build_worklist(s)
        self.assertEqual(r['summary']['stale_review_count'], 1)
        self.assertEqual(len(r['findings']), 1)
        self.assertNotEqual(r['findings'][0]['evidence_sha256'], f['evidence_sha256'])

    def test_related_seed_changes_invalidate_review(self):
        s = linked('ambient object', 'general construction')
        s['inventory']['seed_relations'] = [{'relation_id': 'rel.synthetic',
            'from_formulation': 'form.s.0', 'target_meaning_id': 'u', 'phrase': 'ambient object'}]
        f = build_worklist(s)['findings'][0]
        s['review_ledger'] = [review(f)]
        self.assertEqual(build_worklist(s)['findings'], [])
        s['inventory']['seed_relations'][0]['relation_id'] = 'rel.changed'
        self.assertEqual(build_worklist(s)['summary']['stale_review_count'], 1)

    def test_mechanical_integrity_is_distinct_and_not_suppressible(self):
        s = linked()
        s['nodes']['form.s.0']['references'][0]['target_meaning_id'] = 'absent'
        r = build_worklist(s)
        f = r['findings'][0]
        self.assertEqual(f['concern_kind'], 'mechanical_integrity')
        self.assertEqual(r['summary']['mechanical_integrity_count'], 1)
        s['review_ledger'] = [review(f)]
        with self.assertRaises(PipelineError):
            build_worklist(s)

    def test_unknown_historical_seed_target_is_mechanical(self):
        s = linked('ambient object', 'general construction')
        s['inventory']['seed_relations'] = [{'relation_id': 'rel.invalid',
            'from_formulation': 'form.s.0', 'target_meaning_id': 'absent', 'phrase': 'old target'}]
        r = build_worklist(s)
        f = next(f for f in r['findings'] if f['severity'] == 'integrity')
        self.assertEqual(f['code'], 'unknown_existing_target')
        self.assertEqual(f['reference']['relation_id'], 'rel.invalid')
        self.assertEqual(f['concern_kind'], 'mechanical_integrity')

    def test_limits_determinism_no_mutations_and_single_snapshot_cli(self):
        s = linked('closed subset U', 'topological space')
        s['inventory']['seed_relations'] = [{'relation_id': 'rel.synthetic',
            'from_formulation': 'form.s.0', 'target_meaning_id': 'u', 'phrase': 'closed subset U'}]
        before = copy.deepcopy(s)
        all_rows = build_worklist(s, exhaustive=True)
        self.assertGreater(all_rows['summary']['returned'], 1)
        self.assertEqual(build_worklist(s, limit=1)['findings'], all_rows['findings'][:1])
        self.assertEqual(build_worklist(s, limit=0)['summary']['returned'], 0)
        self.assertEqual(build_worklist(s, limit=0)['summary']['omitted'], all_rows['summary']['returned'])
        self.assertEqual(s, before)
        self.assertEqual(all_rows, build_worklist(s, exhaustive=True))
        with self.assertRaises(PipelineError):
            build_worklist(s, limit=-1)
        with patch('research_pipeline.engine.dependency_consistency_worklist.load_live_snapshot', return_value=s) as loader:
            with patch.object(sys, 'argv', ['worklist', '--workspace', '/tmp/synthetic', '--limit', '1']):
                with patch('sys.stdout', new_callable=io.StringIO) as out:
                    main()
            loader.assert_called_once()
            self.assertEqual(json.loads(out.getvalue())['summary']['returned'], 1)

    def test_evidence_bonus_preserves_severity_order_and_negative_scope_controls(self):
        s = linked('closed subset U', 'topological space')
        s['nodes']['form.u.0']['references'] = [{'state': 'existing', 'phrase': 'broken',
            'target_meaning_id': 'absent', 'occurrence_id': 'occ.broken'}]
        r = build_worklist(s, exhaustive=True)
        self.assertEqual(r['findings'][0]['severity'], 'integrity')
        scores = [f['priority_score'] for f in r['findings']]
        self.assertEqual(scores, sorted(scores, reverse=True))
        for phrase, target in [('left module', 'left module'), ('nonempty space', 'nonempty space'),
                               ('general linear map', 'bounded operator')]:
            self.assertNotIn('explicit_qualifier_contrast', codes(linked(phrase, target)))


if __name__ == '__main__':
    unittest.main()
