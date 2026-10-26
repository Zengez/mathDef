"""Context metadata contracts; synthetic mutations and non-applying live reads."""
from copy import deepcopy
import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from research_pipeline.engine.core import PipelineError, Workspace, digest
from research_pipeline.engine.dependency_context_reviews import (
    GENESIS, attach_reviews, candidate_basis, extend_log, history_checkpoint,
    preflight, read_json, replay_reviews, validate_qualification_ledger, load_context_snapshot,
)
from research_pipeline.engine.dependency_cycle_analysis import effective_references
from research_pipeline.engine.dependency_global_audit import (
    analyze_snapshot, candidate_review_bundle, load_live_snapshot,
)
from research_pipeline.engine.dependency_graph import (
    alias_candidates, graph_path, inventory_sync, missing_key, read, store,
)
from research_pipeline.engine.dependency_review_export import workspace_files

WHY = 'Reviewed all original source hypotheses and preserved the component typing, quantifiers and specialized parent data.'
PROVENANCE = [{'artifact': 'synthetic-review-evidence', 'sha256': digest('fixture evidence')}]


def proposal(snapshot, cid, eid='context.proposal.1', *, previous=GENESIS, prior=None):
    basis = candidate_basis(snapshot, cid)
    return {'event_id': eid, 'previous_event_sha256': previous, 'kind': 'proposal', 'payload': {
        'basis': basis, 'prior_review_event_sha256': prior,
        'interpretation': {'kind': 'component_prerequisite',
            'context': 'Generic single-object predicate, instantiated with every original parent condition retained.',
            'hypotheses': ['Use the explicit objects and hypotheses recorded in each original source.']},
        'occurrence_interpretations': [{'formulation_id': r['formulation_id'], 'occurrence_id': r['occurrence_id'],
            'relation': 'component_instantiation',
            'instantiation': 'Use the single-object prerequisite with the parent objects and original quantifiers preserved.',
            'retained_parent_conditions': [r['source']['text']], 'rationale': WHY}
            for r in basis['occurrences']],
        'authored_by': 'synthetic-fixture-author', 'authored_at': '2026-10-25T12:00:00-04:00',
        'rationale': WHY, 'provenance': deepcopy(PROVENANCE), 'qualification_reference': None}}


def review(p, eid='context.review.1', *, previous=None, decision='approve'):
    return {'event_id': eid, 'previous_event_sha256': previous or digest(p), 'kind': 'review', 'payload': {
        'proposal_event_id': p['event_id'], 'proposal_event_sha256': digest(p), 'decision': decision,
        'reviewed_by': 'synthetic-fixture-reviewer', 'authored_at': '2026-10-25T12:01:00-04:00',
        'rationale': WHY, 'provenance': deepcopy(PROVENANCE)}}


class ContextReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.w = self.root/'workspace'
        Workspace(self.w).init({'schema_version': 1, 'project': 'Synthetic context fixture',
            'term_kind': 'item', 'content_kind': 'description', 'adapter': 'fixture',
            'external_reference_mode': True, 'independent_second_wave': True})
        self.rows = [{'id': 'meaning.'+name, 'display_term': name, 'context': 'Synthetic analysis',
            'formulations': [{'id': 'form.'+name, 'text': text}]} for name,text in [
            ('real', 'For every real index t, the original object has property P at t and also satisfies Q.'),
            ('integer', 'For every integer n, the original object has property P at n and retains its own conditions.'),
            ('individual', 'Two specified individual objects have property P; no process indexing is supplied.')]]
        (self.w/'records/meanings.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in self.rows))
        (self.w/'records/relations.jsonl').write_text('')
        inventory_sync(self.w); self.inv = read(graph_path(self.w)/'INVENTORY.json')
        store(self.w, [{'formulation_id': 'form.'+name,
            'version_sha256': self.inv['formulations']['form.'+name]['version_sha256'],
            'references': [{'phrase': 'property '+name, 'state': 'missing', 'context': context}],
            'complete': True, 'review_rationale': WHY} for name,context in [
            ('real', 'Property P for every real index, with an explicitly specialized original scope.'),
            ('integer', 'Single-object property P instantiated for every integer index.'),
            ('individual', 'Single-object property P instantiated for the two named objects.')]])
        self.ids = {name: missing_key('property '+name, ctx) for name,ctx in [
            ('real', 'Property P for every real index, with an explicitly specialized original scope.'),
            ('integer', 'Single-object property P instantiated for every integer index.'),
            ('individual', 'Single-object property P instantiated for the two named objects.') ]}
        alias_candidates(self.w, [{'alias_id': 'alias.fixture.'+str(i), 'alias_candidate_id': self.ids[a],
            'canonical_candidate_id': self.ids[b], 'reviewed_by': 'fixture-reviewer', 'reason': WHY}
            for i,(a,b) in enumerate([('integer','individual'),('individual','real')],1)])
        self.snapshot = load_context_snapshot(self.w); self.cid = self.ids['real']
        self.p = proposal(self.snapshot, self.cid); self.events = [self.p, review(self.p)]

    def replay(self, events=None, snapshot=None):
        events = self.events if events is None else events
        return replay_reviews(self.snapshot if snapshot is None else snapshot, events, history_checkpoint(events))

    def test_proposed_reviewed_rejected_and_applied_are_distinct(self):
        self.assertIsNone(self.replay([self.p])['candidates'][self.cid]['reviewed_interpretation'])
        rejected = self.replay([self.p, review(self.p, decision='reject')])
        self.assertIsNone(rejected['candidates'][self.cid]['reviewed_interpretation'])
        accepted = self.replay()
        self.assertFalse(accepted['graph_changes_applied'])
        self.assertFalse(accepted['candidates'][self.cid]['reviewed_interpretation']['graph_change_applied'])
        self.assertEqual(accepted['review_events'], self.events)
        self.assertEqual(accepted['candidates'][self.cid]['original_evidence']['canonical_candidate']['context'],
                         self.p['payload']['basis']['canonical_candidate']['context'])
        for decision in ['applied', 'resolve', 'alias', True, None]:
            with self.subTest(decision=decision), self.assertRaises(PipelineError):
                self.replay([self.p, review(self.p, decision=decision)])

    def test_history_checkpoint_detects_truncation_reorder_and_replacement(self):
        checkpoint = history_checkpoint(self.events)
        for events in [self.events[:1], list(reversed(self.events)), [deepcopy(self.p), review(self.p)]]:
            if events == self.events:events[0]['payload']['authored_by']='replacement-author'
            with self.subTest(events=len(events)), self.assertRaises(PipelineError):
                replay_reviews(self.snapshot, events, checkpoint)

    def test_pure_append_preserves_prior_history_and_rejects_reused_ids(self):
        before = deepcopy(self.events)
        p2 = proposal(self.snapshot, self.cid, 'context.proposal.2', previous=digest(self.events[-1]),
                      prior=digest(self.events[-1]))
        p2['payload']['interpretation']['context'] += ' New explicitly reviewed wording.'
        appended = extend_log(self.snapshot, self.events, history_checkpoint(self.events),
                              [p2, review(p2,'context.review.2')])
        self.assertEqual(appended['events'][:2], before)
        self.assertEqual(self.events, before)
        with self.assertRaises(PipelineError):
            extend_log(self.snapshot, self.events, history_checkpoint(self.events), [self.p])
        with self.assertRaises(PipelineError):
            extend_log(self.snapshot, self.events, history_checkpoint(self.events), [])

    def test_changed_prior_interpretation_and_conflicting_approval_rejected(self):
        p2 = proposal(self.snapshot, self.cid,'context.proposal.2',previous=digest(self.events[-1]))
        with self.assertRaisesRegex(PipelineError,'prior reviewed'):
            self.replay(self.events+[p2])
        # Two proposals may be pending, but their competing approvals cannot both replace genesis.
        p2 = proposal(self.snapshot,self.cid,'context.proposal.2',previous=digest(self.p))
        first_review = review(self.p,previous=digest(p2))
        second_review = review(p2,'context.review.2',previous=digest(first_review))
        with self.assertRaisesRegex(PipelineError,'Concurrent'):
            self.replay([self.p,p2,first_review,second_review])

    def test_all_graph_ledger_and_source_changes_invalidate_pins(self):
        def source(s):s['inventory']['formulations']['form.real']['text']+=' Changed.'
        def variant(s):s['inventory']['meanings']['meaning.real']['formulation_ids'].append('new.variant')
        def node(s):s['nodes']['form.real']['review_rationale']+=' Changed.'
        def registry(s):next(c for c in s['candidates'] if c['id']==self.cid)['context']+=' Changed.'
        def alias(s):s['aliases'][0]['reason']+=' Changed.'
        def resolution(s):s['resolutions'].append({'missing_candidate_id':self.cid,'target_meaning_id':'meaning.real','target_version_sha256':'0'*64})
        def seed(s):s['seed_override_events'].append({'malformed':'new seed'})
        def state(s):s['state']['summary']['phase']='other'
        def review_ledger(s):s['review_ledger'].append({'review':'changed'})
        for mutate in [source,variant,node,registry,alias,resolution,seed,state,review_ledger]:
            s=deepcopy(self.snapshot);mutate(s)
            with self.subTest(mutation=mutate.__name__), self.assertRaises(PipelineError):
                self.replay(snapshot=s)

    def test_exact_occurrence_alias_description_and_hash_pins(self):
        for field in ['source_version_sha256','effective_node_sha256','observed_candidate_id',
                      'source_record_sha256','source_snapshot_sha256','source_meaning_id','alias_event_ids']:
            p=deepcopy(self.p);p['payload']['basis']['occurrences'][0][field]='tampered'
            with self.subTest(field=field), self.assertRaisesRegex(PipelineError,'basis'):
                self.replay([p])
        p=deepcopy(self.p);p['payload']['basis']['canonical_candidate']['context']='replacement'
        with self.assertRaises(PipelineError):self.replay([p])

    def test_all_occurrences_required_including_specialized_representative(self):
        self.assertEqual(len(self.p['payload']['basis']['occurrences']),3)
        for index in range(3):
            p=deepcopy(self.p);p['payload']['occurrence_interpretations'].pop(index)
            with self.subTest(omitted=index), self.assertRaisesRegex(PipelineError,'Coverage'):
                self.replay([p])
        p=deepcopy(self.p);p['payload']['occurrence_interpretations'].append(p['payload']['occurrence_interpretations'][0])
        with self.assertRaises(PipelineError):self.replay([p])

    def test_alias_chains_cycles_unknown_endpoints_and_reused_events(self):
        anchors=self.p['payload']['basis']['occurrences']
        integer=next(a for a in anchors if a['formulation_id']=='form.integer')
        self.assertEqual(integer['alias_event_ids'],['alias.fixture.1','alias.fixture.2'])
        for modification in ['cycle','unknown','duplicate','self']:
            s=deepcopy(self.snapshot)
            if modification=='cycle':s['aliases'][-1]['canonical_candidate_id']=self.ids['integer']
            elif modification=='unknown':s['aliases'][-1]['canonical_candidate_id']='missing.unknown'
            elif modification=='duplicate':s['aliases'].append(s['aliases'][0])
            else:s['aliases'][0]['canonical_candidate_id']=s['aliases'][0]['alias_candidate_id']
            with self.subTest(modification=modification), self.assertRaises(PipelineError):
                candidate_basis(s,self.cid)
        for bad in [self.ids['integer'],'missing.unknown',None,[]]:
            with self.assertRaises(PipelineError):candidate_basis(self.snapshot,bad)

    def test_whole_quantified_property_is_not_generic_component_identity(self):
        # Structurally explicit false generalization, not a claim of NLP theorem proving.
        p=deepcopy(self.p);p['payload']['interpretation']['kind']='whole_parent_property'
        with self.assertRaisesRegex(PipelineError,'whole-parent'):self.replay([p])
        p=deepcopy(self.p);p['payload']['occurrence_interpretations'][0]['relation']='equivalent_to_whole_parent'
        with self.assertRaisesRegex(PipelineError,'quantified'):self.replay([p])
        p=deepcopy(self.p);p['payload']['occurrence_interpretations'][0]['retained_parent_conditions']=[]
        with self.assertRaises(PipelineError):self.replay([p])

    def test_homogeneous_whole_process_property_cannot_claim_component_identity(self):
        w=self.root/'homogeneous'
        Workspace(w).init({'schema_version':1,'project':'Synthetic homogeneous quantified property',
            'term_kind':'item','content_kind':'description','adapter':'fixture',
            'external_reference_mode':True,'independent_second_wave':True})
        row=deepcopy(self.rows[0]);row['formulations'][0]['text']='A whole process property requires P at every real coordinate, retaining the full universal quantifier.'
        (w/'records/meanings.jsonl').write_text(json.dumps(row)+'\n')
        (w/'records/relations.jsonl').write_text('')
        inventory_sync(w);inv=read(graph_path(w)/'INVENTORY.json')
        context='Entire process predicate requiring P at every real index, not the single-coordinate component.'
        store(w,[{'formulation_id':'form.real','version_sha256':inv['formulations']['form.real']['version_sha256'],
            'references':[{'phrase':'whole quantified property','context':context,'state':'missing'}],
            'complete':True,'review_rationale':WHY}])
        snapshot=load_context_snapshot(w)
        original=proposal(snapshot,missing_key('whole quantified property',context))
        self.assertEqual(len(original['payload']['basis']['occurrences']),1)
        self.assertEqual(original['payload']['basis']['alias_history'],[])
        for field in ['whole_scope','equivalence']:
            p=deepcopy(original)
            if field=='whole_scope':p['payload']['interpretation']['kind']='whole_parent_property'
            else:p['payload']['occurrence_interpretations'][0]['relation']='equivalent_to_whole_parent'
            with self.subTest(field=field),self.assertRaises(PipelineError):
                replay_reviews(snapshot,[p],history_checkpoint([p]))
        # We do not claim that arbitrary dishonest prose can be theorem-checked.

    def test_missing_or_changed_occurrence_and_empty_candidate_fail_closed(self):
        for how in ['missing','renamed','all_removed']:
            changed=deepcopy(self.snapshot)
            if how=='missing':changed['nodes']['form.integer']['references']=[]
            elif how=='renamed':changed['nodes']['form.integer']['references'][0]['occurrence_id']='occ.changed'
            else:
                for node in changed['nodes'].values():node['references']=[]
            with self.subTest(how=how),self.assertRaises(PipelineError):self.replay(snapshot=changed)

    def test_self_dependency_resolution_and_alias_fields_are_not_supported(self):
        for field,value in [('target_meaning_id','meaning.real'),('alias_of',self.ids['integer']),
                            ('new_dependencies',['meaning.real']),('change_applied',True)]:
            p=deepcopy(self.p);p['payload']['interpretation'][field]=value
            with self.subTest(field=field),self.assertRaises(PipelineError):self.replay([p])

    def test_malformed_events_and_missing_provenance_fail_closed(self):
        mutations=[lambda p:p.update(event_id='../unsafe'),lambda p:p.update(kind='apply'),
                   lambda p:p.update(previous_event_sha256='0'*64),
                   lambda p:p['payload'].update(authored_by=''),
                   lambda p:p['payload'].update(rationale='too short'),
                   lambda p:p['payload'].update(provenance=[]),
                   lambda p:p['payload'].update(authored_at='2026-10-25'),
                   lambda p:p['payload']['interpretation'].update(hypotheses=[]),
                   lambda p:p['payload']['basis'].update(unknown_field=True)]
        for mutate in mutations:
            p=deepcopy(self.p);mutate(p)
            with self.subTest(mutation=mutate), self.assertRaises(PipelineError):self.replay([p])
        p=deepcopy(self.p);p['payload']['interpretation']['context']=float('nan')
        with self.assertRaises(PipelineError):self.replay([p])
        with self.assertRaises(PipelineError):self.replay([self.p,self.p])

    def test_approval_must_reference_exact_proposal_once(self):
        for changed in ['digest','missing','repeated']:
            events=deepcopy(self.events)
            if changed=='digest':events[-1]['payload']['proposal_event_sha256']='0'*64
            elif changed=='missing':events[-1]['payload']['proposal_event_id']='unknown.proposal'
            else:events.append(review(self.p,'second.review',previous=digest(events[-1])))
            with self.subTest(changed=changed),self.assertRaises(PipelineError):self.replay(events)

    def test_input_objects_and_all_existing_graph_results_remain_identical(self):
        before=deepcopy(self.snapshot);events=deepcopy(self.events)
        view=attach_reviews(self.snapshot,self.events,history_checkpoint(self.events))
        self.assertEqual(self.snapshot,before);self.assertEqual(self.events,events)
        self.assertEqual(effective_references(view),effective_references(before))
        for fn in [analyze_snapshot,candidate_review_bundle]:
            report=fn(view);metadata=report.pop('candidate_context_reviews')
            self.assertEqual(report,fn(before));self.assertEqual(metadata,self.replay())
        from research_pipeline.engine.dependency_consistency_worklist import build_worklist
        report=build_worklist(view,exhaustive=True);report.pop('candidate_context_reviews')
        self.assertEqual(report,build_worklist(before,exhaustive=True))
        self.assertEqual(load_context_snapshot(self.w),before)
        self.assertEqual(replay_reviews(before,[],history_checkpoint([]))['candidates'],{})

    def files(self,events=None):
        events=self.events if events is None else events
        log=self.root/'review-log.json';cp=self.root/'checkpoint.json'
        log.write_text(json.dumps({'schema_version':1,'events':events}))
        cp.write_text(json.dumps(history_checkpoint(events)))
        return log,cp

    def test_disposable_preflight_checks_all_bytes_and_never_applies(self):
        before=workspace_files(self.w);log,cp=self.files()
        report=preflight(self.w,log,cp)
        self.assertEqual(report['status'],'mechanically_valid_not_applied')
        self.assertTrue(report['disposable_copy_verified'])
        self.assertFalse(report['graph_changes_applied'])
        self.assertEqual(report['workspace_before_sha256'],report['workspace_after_sha256'])
        self.assertEqual(before,workspace_files(self.w))

    def test_copy_or_original_changes_abort_even_when_replay_fails(self):
        log,cp=self.files();original=load_live_snapshot
        for altered in ['original','copy']:
            def changed(path):
                snapshot=original(path)
                target=self.w if altered=='original' else path
                (target/'concurrent-change').write_text('changed')
                raise PipelineError('simulated invalid replay')
            with patch('research_pipeline.engine.dependency_global_audit.load_live_snapshot',side_effect=changed):
                with self.assertRaisesRegex(PipelineError,'changed during'):
                    preflight(self.w,log,cp)
            (self.w/'concurrent-change').unlink(missing_ok=True)

    def test_changed_review_input_and_stale_inventory_are_rejected(self):
        log,cp=self.files();original=load_live_snapshot
        def changed(path):
            snapshot=original(path);log.write_text('{}');return snapshot
        with patch('research_pipeline.engine.dependency_global_audit.load_live_snapshot',side_effect=changed):
            with self.assertRaisesRegex(PipelineError,'changed during'):preflight(self.w,log,cp)
        log,cp=self.files()
        p=self.w/'records/meanings.jsonl';p.write_text(p.read_text().replace('also satisfies Q','also satisfies NEW'))
        with self.assertRaisesRegex(PipelineError,'stale against'):preflight(self.w,log,cp)

    def test_duplicate_json_and_nonfinite_fields_rejected(self):
        path=self.root/'bad.json'
        for raw in ['{"events":[],"events":[]}','{"value":NaN}','{"value":Infinity}']:
            path.write_text(raw)
            with self.assertRaises(PipelineError):read_json(path)

    def test_readers_reject_stale_or_forged_sidecars(self):
        view=attach_reviews(self.snapshot,self.events,history_checkpoint(self.events))
        view['candidate_context_reviews']['candidates'][self.cid]['reviewed_interpretation']['reviewed_by']='forged'
        for fn in [analyze_snapshot,candidate_review_bundle]:
            with self.assertRaisesRegex(PipelineError,'sidecar'):fn(view)
        view=attach_reviews(self.snapshot,self.events,history_checkpoint(self.events))
        view=deepcopy(view);view['nodes']['form.real']['review_rationale']+=' Changed after attachment.'
        with self.assertRaisesRegex(PipelineError,'basis'):analyze_snapshot(view)

    def test_qualification_reference_pins_exact_proposal_and_stays_unapplied(self):
        anchor=self.p['payload']['basis']['occurrences'][0]
        row={'id':'qualification.fixture','status':'review_candidate_not_applied','change_applied':False,
             'affected_formulation_id':anchor['formulation_id'],
             'affected_occurrence_id':anchor['occurrence_id'],'affected_candidate_id':self.cid,
             'source_version_sha256':anchor['source_version_sha256'],
             'effective_node_sha256':anchor['effective_node_sha256'],
             'counterexample':'Synthetic degenerate case requiring later explicit source qualification.',
             'application_commit':None,'transaction_receipt':None}
        ledger={'schema_version':1,'review_candidates':[row],'applied_qualifications':[]}
        p=deepcopy(self.p)
        p['payload']['qualification_reference']={'ledger_sha256':digest(ledger),'review_candidate_id':row['id']}
        events=[p,review(p)]
        result=replay_reviews(self.snapshot,events,history_checkpoint(events),qualification_ledger=ledger)
        self.assertFalse(result['graph_changes_applied'])
        self.assertEqual(result['qualification_ledger']['applied_qualifications'],[])
        for field in ['affected_formulation_id','affected_occurrence_id','affected_candidate_id',
                      'source_version_sha256','effective_node_sha256']:
            bad=deepcopy(ledger);bad['review_candidates'][0][field]='0'*64 if 'sha256' in field else 'unknown.id'
            p2=deepcopy(p);p2['payload']['qualification_reference']['ledger_sha256']=digest(bad)
            with self.subTest(field=field),self.assertRaises(PipelineError):
                replay_reviews(self.snapshot,[p2],history_checkpoint([p2]),qualification_ledger=bad)
        with self.assertRaises(PipelineError):replay_reviews(self.snapshot,events,history_checkpoint(events))

    def test_cli_preflight_and_opt_in_auditors_keep_raw_values(self):
        log,cp=self.files()
        prefix=[sys.executable,'-m']
        command=prefix+['research_pipeline.engine.dependency_context_reviews','--workspace',str(self.w),
                       '--log',str(log),'--checkpoint',str(cp)]
        result=subprocess.run(command,capture_output=True,text=True,check=True)
        self.assertEqual(json.loads(result.stdout)['status'],'mechanically_valid_not_applied')
        for module,args in [('dependency_global_audit',['focus','--candidate-id',self.cid]),
                            ('dependency_consistency_worklist',['--exhaustive'])]:
            base=prefix+['research_pipeline.engine.'+module,'--workspace',str(self.w)]
            raw=json.loads(subprocess.run(base+args,capture_output=True,text=True,check=True).stdout)
            reviewed=json.loads(subprocess.run(base+['--context-review-log',str(log),
                '--context-review-checkpoint',str(cp)]+args,capture_output=True,text=True,check=True).stdout)
            reviewed.pop('candidate_context_reviews');self.assertEqual(raw,reviewed)
        output=self.root/'should-not-exist'
        rejected=subprocess.run(prefix+['research_pipeline.engine.dependency_global_audit','--workspace',str(self.w),
            '--context-review-log',str(log),'--context-review-checkpoint',str(cp),'prepare',
            '--manifest',str(self.root/'does-not-exist.json'),'--output-dir',str(output)],capture_output=True,text=True)
        self.assertNotEqual(rejected.returncode,0);self.assertFalse(output.exists())
        rejected=subprocess.run(command[:-2],capture_output=True,text=True)
        self.assertNotEqual(rejected.returncode,0)

    def test_raw_ledger_bytes_and_extra_files_are_bound_even_without_graph_change(self):
        alias_path=self.w/'dependency_graph/candidate_aliases.jsonl'
        alias_path.write_text(alias_path.read_text()+'\n')
        changed=load_context_snapshot(self.w)
        self.assertEqual(changed['aliases'],self.snapshot['aliases'])
        self.assertEqual(changed['nodes'],self.snapshot['nodes'])
        with self.assertRaisesRegex(PipelineError,'basis'):self.replay(snapshot=changed)
        with self.assertRaisesRegex(PipelineError,'load_context_snapshot'):
            candidate_basis(load_live_snapshot(self.w),self.cid)

    def test_review_artifacts_cannot_be_inside_protected_workspace(self):
        log,cp=self.files()
        inside=self.w/'context-log.json';inside.write_bytes(log.read_bytes())
        with self.assertRaisesRegex(PipelineError,'outside the protected workspace'):
            preflight(self.w,inside,cp)
        log.write_text(json.dumps({'schema_version':True,'events':self.events}))
        with self.assertRaisesRegex(PipelineError,'schema'):preflight(self.w,log,cp)

    def test_historical_seed_coverage_is_not_a_live_node_index(self):
        from research_pipeline.tests.test_dependency_seed_overrides import SeedOverrideReplayTests
        fixture=SeedOverrideReplayTests();fixture.setUp();self.addCleanup(fixture.doCleanups)
        snapshot=load_context_snapshot(fixture.root)
        snapshot['seed_override_events']=[fixture.event]
        basis=candidate_basis(snapshot,fixture.candidate)
        self.assertEqual({r['reference_kind'] for r in basis['occurrences']},{'live_node','historical_seed'})
        seed=next(r for r in basis['occurrences'] if r['reference_kind']=='historical_seed')
        self.assertTrue(seed['occurrence_id'].startswith('seed.'))
        self.assertEqual(seed['raw_observed_reference']['relation_id'],fixture.seed['relation_id'])


class QualificationLedgerTests(unittest.TestCase):
    def ledger(self):
        return {'schema_version':1,'review_candidates':[{'id':'edgecase.fixture','status':'review_candidate_not_applied',
            'change_applied':False,'affected_formulation_id':'form.fixture','source_version_sha256':'1'*64,
            'effective_node_sha256':'2'*64,'counterexample':'Explicit synthetic degenerate-object counterexample.',
            'application_commit':None,'transaction_receipt':None}], 'applied_qualifications':[]}

    def test_proposals_cannot_claim_applied_status_or_application_evidence(self):
        l=self.ledger();self.assertEqual(validate_qualification_ledger(l)['claimed_applied_qualifications'],0)
        for k,v in [('change_applied',True),('application_commit','a'*40),('transaction_receipt','receipt'),('status','applied')]:
            bad=deepcopy(l);bad['review_candidates'][0][k]=v
            with self.subTest(field=k),self.assertRaises(PipelineError):validate_qualification_ledger(bad)
        bad=deepcopy(l);bad['applied_qualifications']=deepcopy(bad['review_candidates'])
        with self.assertRaises(PipelineError):validate_qualification_ledger(bad)

    def test_claimed_applied_requires_complete_evidence_without_certifying_it(self):
        row={'id':'applied.fixture','affected_formulation_id':'form.fixture','source_version_sha256':'1'*64,
             'effective_node_sha256_before':'2'*64,'application_commit':'a'*40}
        for key in ['exception_kind','original_wording','qualified_wording','counterexample','mathematical_rationale',
                    'source_convention_status','transaction_receipt_or_reason_not_applicable','manual_review_state']:
            row[key]='synthetic evidence'
        l={'schema_version':1,'review_candidates':[],'applied_qualifications':[row]}
        self.assertFalse(validate_qualification_ledger(l)['application_evidence_verified'])
        row['application_commit']=None
        with self.assertRaises(PipelineError):validate_qualification_ledger(l)


class LiveContextReviewTests(unittest.TestCase):
    """Real six mismatches plus two specialized uses; no persisted live overlay."""
    def test_eight_occurrences_six_mismatches_are_nonapplying_fixtures(self):
        w=Path(__file__).resolve().parents[1]/'experiments/reconstruction-v2-independent'
        before=workspace_files(w);snapshot=load_context_snapshot(w)
        pairs=[('missing.826fb5c503bdaf25ce7f','integrability'),('missing.b599bdc9343a25050226','clopen')]
        expected={'occ.3eda46790ce1c2aed5c5','occ.b8df608b462159d8948d','occ.98619b3d2a58ee9006e9',
                  'occ.417c86f577e85affc4cb','occ.00775f87f3c5601a0719','occ.1612dec2b099f44c923b'}
        events=[];covered=set()
        for cid,name in pairs:
            p=proposal(snapshot,cid,'fixture.'+name,previous=digest(events[-1]) if events else GENESIS)
            p['payload']['interpretation']['context']=(
                'L1 integrability of one measurable real random variable Y: E|Y| is finite; parent indices remain local.'
                if name=='integrability' else 'Clopen predicate on U within an arbitrary specified topological space X: U and X minus U are open.')
            for row in p['payload']['occurrence_interpretations']:
                row['instantiation']=(
                    'Use L1 for each indicated real variable, retaining integer/real time or the two individual variables as in the full source.'
                    if name=='integrability' else 'Instantiate the generic clopen predicate at the original ambient space, retaining any spectrum and idempotent conditions.')
            covered.update(r['occurrence_id'] for r in p['payload']['basis']['occurrences'])
            self.assertEqual(len(p['payload']['basis']['occurrences']),4)
            events.extend([p,review(p,'fixture.'+name+'.review')])
        self.assertTrue(expected<=covered);self.assertEqual(len(covered),8)
        self.assertTrue({'occ.2cf87f7b73f5c5a33bb4','occ.982109ad4faf2e20b72d'}<=covered)
        view=attach_reviews(snapshot,events,history_checkpoint(events))
        self.assertEqual(effective_references(view),effective_references(snapshot))
        raw_report=analyze_snapshot(snapshot);with_report=analyze_snapshot(view)
        with_report.pop('candidate_context_reviews');self.assertEqual(raw_report,with_report)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);log=root/'log.json';cp=root/'checkpoint.json'
            log.write_text(json.dumps({'schema_version':1,'events':events}));cp.write_text(json.dumps(history_checkpoint(events)))
            result=preflight(w,log,cp)
            self.assertEqual(result['status'],'mechanically_valid_not_applied')
        self.assertEqual(before,workspace_files(w))
