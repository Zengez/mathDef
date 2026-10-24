"""Disposable independent-workspace readiness checks; never seal any gate."""
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from research_pipeline.engine.core import Workspace, digest
from research_pipeline.engine.dependency_audit_acceleration import audit_fingerprint
from research_pipeline.engine.dependency_consolidation_readiness import assess, load_inputs, main
from research_pipeline.engine.dependency_graph import (
    alias_candidates, amend, live_nodes, inventory_sync, meaning_version, missing_key, read, resolve, store,
)
from research_pipeline.engine.dependency_seed_overrides import append_seed_overrides


class ConsolidationReadinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Workspace(self.root).init({'schema_version': 1, 'project': 'Synthetic readiness',
            'term_kind': 'term', 'content_kind': 'definition', 'adapter': 'mathdef',
            'external_reference_mode': True, 'independent_second_wave': True})
        self.records = self.root/'records'
        self.meanings = [{'id': 'meaning.'+name, 'display_term': name,
            'context': 'Synthetic algebra', 'formulations': [{'id': 'form.'+name,
                'text': 'Synthetic complete formulation '+name, 'evidence_ids': ['obs.fixture']}]}
            for name in ('a','b','c')]
        self.write_records('meanings', self.meanings)
        self.write_records('relations', [])
        self.write_records('observations', [{'id': 'obs.fixture', 'source_id': 'src.fixture',
            'locator': 'Fixture section 1', 'record_kind': 'paraphrase', 'text': 'Synthetic evidence'}])
        self.write_records('sources', [{'id': 'src.fixture', 'title': 'Synthetic source'}])
        inventory_sync(self.root)
        self.put({'form.a': [self.missing('unpopulated prerequisite')], 'form.b': [], 'form.c': []})

    def write_records(self, kind, rows):
        (self.records/(kind+'.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in rows))

    def missing(self, phrase):
        return {'state': 'missing', 'phrase': phrase, 'context': 'Synthetic algebra'}

    def put(self, refs):
        inv = read(self.root/'dependency_graph/INVENTORY.json')
        current = live_nodes(self.root/'dependency_graph', inv)
        items = [{'formulation_id': fid,
            'version_sha256': inv['formulations'][fid]['version_sha256'], 'complete': True,
            'review_rationale': 'Reviewed every reference and the full synthetic formulation context.',
            'references': rows} for fid, rows in refs.items()]
        if not current:
            return store(self.root, items)
        for item in items:
            fid = item['formulation_id']
            item.update(amendment_id='amend.'+digest([fid,current[fid],item]),
                expected_node_sha256=digest(current[fid]), reviewed_by='fixture',
                reason='Reviewed synthetic same-version adjacency change for a disposable fixture.')
        return amend(self.root, items)

    def result(self, **kw):
        return assess(load_inputs(self.root), **kw)

    def test_mechanical_eligibility_never_concludes_pass2(self):
        r = self.result()
        self.assertEqual(r['status'], 'mechanical_checks_passed_review_decision_required')
        self.assertTrue(all(r['mechanical_checks'].values()))
        self.assertEqual(r['mechanical_integrity_failures'], [])
        self.assertEqual(r['pass2_complete'], 'not_determined')
        self.assertFalse(r['pass3_authorized_by_this_assessment'])
        self.assertFalse(r['gate_contract']['existing_record_present'])
        self.assertTrue(r['gate_contract']['named_reviewer_and_substantive_global_rationale_required'])
        self.assertFalse((self.root/'dependency_graph/CONSOLIDATION.json').exists())

    def test_mathematical_lead_is_outstanding_without_invented_blocker(self):
        self.meanings[2]['display_term'] = 'topological space'
        self.write_records('meanings', self.meanings)
        inventory_sync(self.root)
        self.put({'form.a': [{'state': 'existing', 'phrase': 'closed subset U',
                             'target_meaning_id': 'meaning.c'}]})
        r = self.result()
        self.assertEqual(r['mechanical_integrity_failures'], [])
        self.assertGreater(r['mathematical_consistency_review']['summary']['total_review_candidates'], 0)
        self.assertEqual(r['pass2_complete'], 'not_determined')

    def test_open_source_issue_requires_deferral_decision_not_automatic_block(self):
        data = load_inputs(self.root)
        data['source_issues'] = [{'id': 'issue.fixture', 'status': 'open',
            'related_formulation_id': 'form.a', 'reason': 'Synthetic source convention needs later reconciliation.'}]
        r = assess(data)
        self.assertEqual(r['mechanical_integrity_failures'], [])
        issue = r['source_issues_for_deferral_decision'][0]
        self.assertFalse(issue['deferral_adopted_by_assessment'])
        self.assertIn('form.a', issue['source_context'])

    def test_legitimate_missing_is_not_unclassified(self):
        r = self.result(exhaustive=True)
        self.assertEqual(r['counts']['canonical_missing_candidates'], 1)
        self.assertEqual(r['counts']['unassigned_occurrences'], 0)
        self.assertFalse(r['gate_contract']['zero_missing_candidates_required'])
        c = r['classified_missing_prerequisites']['examples'][0]
        self.assertEqual(c['candidate']['query'], 'unpopulated prerequisite')
        self.assertIn('form.a', c['sources'])
        self.assertIn('obs.fixture', r['selected_source_evidence']['observations'])

    def test_unassigned_reference_blocks_but_deferred_does_not(self):
        self.put({'form.a': [{'state': 'unassigned', 'phrase': 'unknown', 'context': 'Synthetic algebra'}]})
        r = self.result()
        self.assertEqual(r['status'], 'blocked_by_unmet_gate_prerequisites')
        self.assertEqual(r['mechanical_integrity_failures'], [])
        self.assertFalse(r['gate_contract']['zero_unassigned'])
        self.put({'form.a': [{'state': 'deferred', 'phrase': 'unknown',
            'reason': 'Explicit synthetic contextual deferral for later review.'}]})
        r = self.result()
        self.assertEqual(r['counts']['deferred_occurrences'], 1)
        self.assertFalse(r['gate_contract']['zero_deferred_occurrences_required'])
        self.assertEqual(r['status'], 'mechanical_checks_passed_review_decision_required')

    def test_real_registry_metadata_defect_blocks(self):
        data = load_inputs(self.root)
        data['graph']['candidates'][0]['occurrence_count'] += 1
        r = assess(data)
        self.assertEqual(r['status'], 'blocked_by_mechanical_integrity')
        self.assertIn('registry_metadata_matches_replay', [f['code'] for f in r['mechanical_integrity_failures']])

    def test_index_and_checkpoint_defects_block(self):
        for mutate, expected in [(lambda d: d['stored']['occurrences'].clear(), 'occurrence_index_matches_replay'),
                                 (lambda d: d['stored']['reverse_index'].clear(), 'reverse_index_matches_replay'),
                                 (lambda d: d['stored']['checkpoint'].update(state_sha256='stale'), 'checkpoint_matches_state')]:
            data = load_inputs(self.root)
            mutate(data)
            self.assertIn(expected, [f['code'] for f in assess(data)['mechanical_integrity_failures']])

    def test_alias_and_version_bound_resolution_provenance(self):
        self.put({'form.a': [self.missing('first prerequisite')],
                  'form.b': [self.missing('canonical prerequisite')]})
        first = missing_key('first prerequisite', 'Synthetic algebra')
        canonical = missing_key('canonical prerequisite', 'Synthetic algebra')
        alias_candidates(self.root, [{'alias_id': 'alias.fixture', 'alias_candidate_id': first,
            'canonical_candidate_id': canonical, 'reviewed_by': 'fixture',
            'reason': 'Explicit synthetic contextual identity review of these two prerequisite uses.'}])
        inv = read(self.root/'dependency_graph/INVENTORY.json')
        resolve(self.root, [{'missing_candidate_id': canonical, 'target_meaning_id': 'meaning.c',
            'target_version_sha256': meaning_version(inv, 'meaning.c'),
            'review_rationale': 'Explicit contextual synthetic review resolves the canonical prerequisite to C.'}])
        data = load_inputs(self.root)
        r = assess(data)
        self.assertEqual(r['mechanical_integrity_failures'], [])
        self.assertEqual(r['counts']['effective_aliases'], 1)
        self.assertEqual(r['counts']['effective_resolutions'], 1)
        self.assertEqual(r['counts']['canonical_missing_candidates'], 0)
        refs = data['stored']['occurrences']
        first_row = next(row for row in refs if row['from_formulation']=='form.a')
        self.assertEqual(first_row['observed_missing_candidate_id'], first)
        self.assertEqual(first_row['resolved_missing_candidate_id'], canonical)
        data['graph']['resolutions'][0]['target_version_sha256'] = 'stale'
        r = assess(data)
        self.assertEqual(r['status'], 'blocked_by_mechanical_integrity')  # indexes now stale
        self.assertEqual(r['counts']['inactive_resolution_events'], 1)

    def test_seed_override_preserves_provenance_without_original_target(self):
        self.write_records('relations', [{'id': 'rel.fixture', 'relation_type': 'definition_uses',
            'from_formulation': 'form.a', 'target_meaning': 'meaning.c', 'source_phrase': 'unpopulated prerequisite'}])
        inventory_sync(self.root)
        inv = read(self.root/'dependency_graph/INVENTORY.json')
        seed = inv['seed_relations'][0]
        append_seed_overrides(self.root, [{'schema_version': 1, 'seed_override_id': 'override.fixture',
            'relation_id': seed['relation_id'], 'expected_seed_sha256': digest(seed),
            'expected_version_sha256': inv['formulations']['form.a']['version_sha256'],
            'expected_old_target_meaning_id': 'meaning.c',
            'replacement': {'state': 'missing', 'missing_candidate_id': missing_key('unpopulated prerequisite','Synthetic algebra')},
            'reviewed_by': 'fixture', 'review_rationale': 'A source-version-anchored synthetic review preserves a separate missing prerequisite instead of C.'}])
        data = load_inputs(self.root)
        r = assess(data)
        self.assertEqual(r['mechanical_integrity_failures'], [])
        self.assertEqual(r['counts']['missing_occurrences'], 2)
        seed_ref = next(row for row in data['stored']['occurrences'] if row.get('relation_id'))
        self.assertEqual(seed_ref['seed_override_id'], 'override.fixture')
        self.assertEqual(seed_ref['original_target_meaning_id'], 'meaning.c')
        self.assertEqual(seed_ref['state'], 'missing')

    def test_current_source_change_invalidates_evidence_and_inventory(self):
        old = self.result()
        self.meanings[0]['formulations'][0]['text'] += ' Changed source.'
        self.write_records('meanings', self.meanings)
        r = self.result()
        self.assertNotEqual(old['assessment_evidence_sha256'], r['assessment_evidence_sha256'])
        self.assertFalse(r['mechanical_checks']['inventory_matches_current_sources'])

    def test_graph_review_change_invalidates_assessment_fingerprint(self):
        data = load_inputs(self.root)
        old = assess(data)
        data['graph']['review_ledger'] = [{'code': 'synthetic_review', 'formulation_id': 'form.a',
            'source_version_sha256': 'fixture', 'effective_node_sha256': 'fixture', 'occurrence_id': None,
            'disposition': 'needs_further_review', 'reviewed_by': 'fixture',
            'rationale': 'Synthetic contextual review remains outstanding for this assessment snapshot.'}]
        self.assertNotEqual(old['assessment_evidence_sha256'], assess(data)['assessment_evidence_sha256'])

    def test_broken_alias_fails_closed(self):
        data = load_inputs(self.root)
        data['graph']['aliases'] = [{'alias_candidate_id': 'unused', 'canonical_candidate_id': 'unused'}]
        r = assess(data)
        self.assertEqual(r['status'], 'blocked_by_mechanical_integrity')
        self.assertTrue(r['assessment_incomplete'])

    def test_broken_source_link_is_integrity_not_external_certification(self):
        data = load_inputs(self.root)
        data['observations'].clear()
        r = assess(data)
        self.assertFalse(r['mechanical_checks']['provenance_record_links_exist'])
        self.assertFalse(r['provenance']['external_content_verified_by_this_command'])
        data = load_inputs(self.root)
        data['observations']['obs.fixture']['locator'] = ''
        r = assess(data)
        self.assertTrue(r['mechanical_checks']['provenance_record_links_exist'])
        self.assertGreater(r['candidate_review']['total'], 0)  # traceability review, not invented gate

    def test_explicit_candidate_context_review_can_be_accepted(self):
        self.put({'form.a': [self.missing('left group action')],
                  'form.b': [self.missing('right group action')]})
        left, right = [missing_key(p, 'Synthetic algebra') for p in ('left group action','right group action')]
        alias_candidates(self.root, [{'alias_id': 'alias.contrast', 'alias_candidate_id': left,
            'canonical_candidate_id': right, 'reviewed_by': 'fixture',
            'reason': 'Synthetic deliberately controversial identity for review-only contrast regression.'}])
        data = load_inputs(self.root)
        r = assess(data, exhaustive=True)
        self.assertEqual(r['mechanical_integrity_failures'], [])
        self.assertEqual(r['candidate_review']['total'], 1)
        lead = r['candidate_review']['leads'][0]
        self.assertIn('explicit_candidate_side_contrast', lead['concerns'])
        self.assertEqual(set(lead['sources']), {'form.a','form.b'})
        data['graph']['review_ledger'] = [{**audit_fingerprint(lead),
            'disposition': 'accepted_as_correct', 'reviewed_by': 'fixture',
            'rationale': 'Reviewed the complete contextual contrast and intentionally retained these distinct source presentations.'}]
        r = assess(data)
        self.assertEqual(r['candidate_review']['total'], 0)
        self.assertEqual(r['candidate_review']['accepted_review_count'], 1)

    def test_candidate_context_truncation_is_explicit(self):
        extra = copy.deepcopy(self.meanings[0])
        extra['id'] = 'meaning.d'
        extra['display_term'] = 'd'
        extra['formulations'][0]['id'] = 'form.d'
        self.write_records('meanings', self.meanings + [extra])
        inventory_sync(self.root)
        inv = read(self.root/'dependency_graph/INVENTORY.json')
        store(self.root, [{'formulation_id': 'form.d',
            'version_sha256': inv['formulations']['form.d']['version_sha256'],
            'complete': True, 'review_rationale': 'Complete synthetic reference classification for an extra source.',
            'references': [self.missing('unpopulated prerequisite')]}])
        self.put({'form.b': [self.missing('unpopulated prerequisite')],
                  'form.c': [self.missing('unpopulated prerequisite')]})
        shown = self.result()['classified_missing_prerequisites']['examples'][0]
        self.assertEqual(len(shown['sources']), 3)
        self.assertEqual(shown['source_formulations_omitted'], 1)
        complete = self.result(exhaustive=True)['classified_missing_prerequisites']['examples'][0]
        self.assertEqual(len(complete['sources']), 4)
        self.assertEqual(complete['occurrences_omitted'], 0)

    def test_limit_exhaustive_deterministic_read_only_cli(self):
        data = load_inputs(self.root)
        before = copy.deepcopy(data)
        r = assess(data, limit=0)
        self.assertEqual(r['classified_missing_prerequisites']['examples'], [])
        self.assertEqual(r['classified_missing_prerequisites']['omitted'], 1)
        self.assertEqual(r, assess(data, limit=0))
        self.assertEqual(data, before)
        with patch('research_pipeline.engine.dependency_consolidation_readiness.load_inputs', return_value=data) as loader:
            with patch.object(sys, 'argv', ['readiness','--workspace',str(self.root),'--exhaustive']):
                with patch('sys.stdout', new_callable=io.StringIO) as out:
                    main()
            loader.assert_called_once()
            self.assertEqual(json.loads(out.getvalue())['classified_missing_prerequisites']['omitted'], 0)
        self.assertFalse((self.root/'dependency_graph/CONSOLIDATION.json').exists())


if __name__ == '__main__':
    unittest.main()
