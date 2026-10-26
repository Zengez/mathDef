"""Read-only, evidence-anchored dependency consistency REVIEW LEADS.

Usage: python -m research_pipeline.engine.dependency_consistency_worklist
  --workspace research_pipeline/experiments/reconstruction-v2-independent
  [--limit 12 | --exhaustive]

Textual contrasts and target disagreement do not establish mathematical error.
No synonym inference, source fetching, formulation selection or graph edits.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re

from .core import PipelineError, digest
from .dependency_audit_acceleration import rank_findings
from .dependency_cycle_analysis import effective_references
from .dependency_global_audit import analyze_snapshot, load_live_snapshot
from .dependency_graph import norm

# Explicit, bounded vocabulary: absence of an arbitrary adjective is not evidence.
_QUALIFIERS = {
    'side': ('left', 'right'),
    'variance': ('covariant', 'contravariant'),
    'unit': ('unital', 'nonunital'),
    'size': ('small', 'unrestricted'),
    'emptiness': ('nonempty', 'empty-allowed'),
}
_SCOPE = ('small', 'finite', 'unital', 'nonempty', 'positive')
_NOUNS = r'(?:categor(?:y|ies)|groupoids?|rings?|modules?|spaces?|actions?|integers?|operators?|functors?)'


def _has(text, word):
    # Normalize common orthography without equating mathematical objects.
    text = re.sub(r'\bnon[- ]unital\b', 'nonunital', norm(text))
    text = re.sub(r'\bnon[- ]empty\b', 'nonempty', text)
    text = re.sub(r'\bfinite[- ]type\b', 'finite type', text)
    return bool(re.search(r'(?<![\w-])' + re.escape(word) + r'(?![\w-])', text))


def _object_words(text):
    return set(re.findall(_NOUNS, norm(text)))


def build_worklist(snapshot, *, limit=12, exhaustive=False):
    """One loaded snapshot per batch; no per-candidate disk access or replay.

    Reuse global mechanical/scope diagnostics and its exact review machinery.
    Broad ideal-vs-module generation warnings are omitted here: specialization
    alone is insufficient evidence (the original scanner remains available).
    """
    if limit < 0:
        raise PipelineError('Review limit must be nonnegative')
    inv, nodes = snapshot['inventory'], snapshot['nodes']
    forms, meanings = inv['formulations'], inv['meanings']
    baseline = analyze_snapshot(snapshot, candidate_limit=0, include_effective_snapshot=True)
    references = effective_references(snapshot)
    by_form = defaultdict(list)
    groups = defaultdict(list)
    for ref in references:
        by_form[ref['from_formulation']].append(ref)
        if ref['state'] == 'existing' and ref.get('target_meaning_id') in meanings:
            groups[(ref['from_formulation'], norm(ref.get('phrase', '')))].append(ref)
    hashes = {fid: digest(node) for fid, node in nodes.items()}
    targets = {}
    for mid, meaning in sorted(meanings.items()):
        target_forms = {fid: {**forms[fid], 'effective_node_sha256': hashes.get(fid)}
                        for fid in meaning.get('formulation_ids', []) if fid in forms}
        targets[mid] = {'meaning_id': mid, 'meaning': meaning,
                        'formulations': target_forms,
                        'target_evidence_sha256': digest([meaning, target_forms])}
    findings = []

    def emit(code, fid, ref, evidence, *, related=(), severity='review'):
        source = forms[fid]
        findings.append({'severity': severity, 'code': code,
            'formulation_id': fid, 'meaning_id': source['meaning_id'],
            'display_term': source['display_term'], 'source_text': source['text'],
            'source_context': source.get('context', ''),
            'version_sha256': source['version_sha256'],
            'effective_node_sha256': hashes.get(fid),
            'occurrence_id': ref.get('occurrence_id'), 'reference': ref,
            'description': evidence, 'related_references': list(related)})

    # Reuse all strict mechanical checks, plus the existing contextual leads.
    # Accepted rows must participate too so the final combined ranking can
    # apply an evidence-bound review without resurrecting suppressed rows.
    for f in baseline['all_review_queue'] + baseline['accepted_review_ledger_matches']:
        if f['code'] != 'ideal_vs_module_generation':
            findings.append({k: v for k, v in f.items() if k not in
                ('review_disposition', 'review_rationale', 'priority_score')})

    # The old scanner counts invalid seeds but only emits unknown-target
    # findings for scans. Cover unknown effective seed/resolution targets too.
    for ref in references:
        if (ref['state'] == 'existing' and ref.get('target_meaning_id') not in meanings):
            emit('unknown_existing_target', ref['from_formulation'], ref,
                 'Effective existing dependency targets an absent inventory meaning.',
                 severity='integrity')

    for (fid, phrase), rows in sorted(groups.items()):
        source = forms[fid]
        for ref in rows:
            label = meanings[ref['target_meaning_id']]['display_term']
            common_object = _object_words(phrase) & _object_words(label)
            if common_object:
                contrasts = []
                for axis, (a, b) in _QUALIFIERS.items():
                    if axis == 'unit' and ('optional' in norm(label) or 'not necessarily' in norm(label)):
                        continue
                    # Both sides must be explicit, unambiguous single qualifiers.
                    left = [w for w in (a, b) if _has(phrase, w)]
                    right = [w for w in (a, b) if _has(label, w)]
                    if len(left) == len(right) == 1 and left != right:
                        contrasts.append({'axis': axis, 'reference': left[0], 'target': right[0]})
                if contrasts:
                    emit('explicit_qualifier_contrast', fid, ref,
                        'The reference and target label explicitly use opposing qualifiers on a shared object word: '
                        + json.dumps(contrasts, sort_keys=True) + '. Context or a deliberate conversion may justify this link; review both definitions.')
                else:
                    # A narrowly scoped absence lead; check full source as well
                    # as occurrence wording to reduce implicit-context noise.
                    absent = [q for q in _SCOPE if re.match(
                        r'^(?:an? )?' + q + r'\s+(?:(?:left|right)\s+)?' + _NOUNS + r'\b', norm(label))
                              and not _has(phrase, q) and not _has(source['text'], q)
                              and not _has(source.get('context', ''), q)]
                    # Finite categories are small; absence of the literal word
                    # 'small' is no evidence when finiteness is explicit.
                    if (re.search(r'\bfinite\s+categor(?:y|ies)\b', norm(source['text'] + ' ' + source.get('context', '')))
                            or (re.search(r'\bcategor(?:y|ies)\b.{0,100}\bfinitely many objects\b', norm(source['text']))
                                and re.search(r'(?:and |and finitely many )morphisms\b', norm(source['text'])))):
                        absent = [q for q in absent if q != 'small']
                    # "optionally nonunital" is not a mandatory unit assumption.
                    if _has(label, 'nonunital') or 'optional' in norm(label):
                        absent = [q for q in absent if q != 'unital']
                    if absent:
                        emit('target_restriction_not_explicit', fid, ref,
                            'Target label explicitly restricts ' + ', '.join(absent)
                            + ', absent from the reference, source formulation and stated context. This is textual absence, not proof the hypothesis is unjustified.')
            # An ambient topology definition can explicitly define open
            # subsets too; that link alone is then not an object-type lead.
            target_text = ' '.join(f['text'] for f in targets[ref['target_meaning_id']]['formulations'].values())
            explicitly_defines_open_subsets = bool(re.search(
                r'\bare (?:the )?open subsets?\b', norm(target_text)))
            if (re.match(r'^(?:clopen|closed|open)\s+(?:subsets?|sets?)\b', phrase)
                    and norm(label) == 'topological space'
                    and not (phrase.startswith('open ') and explicitly_defines_open_subsets)):
                emit('subset_predicate_to_ambient_space', fid, ref,
                     'The reference begins with an open/closed/clopen subset predicate, but the target is the ambient topological-space meaning. Determine whether the occurrence intends the predicate, ambient structure, or both.')
        distinct = {r['target_meaning_id'] for r in rows}
        if phrase and len(distinct) > 1:
            primary = sorted(rows, key=lambda r: (r.get('origin', 'scan').startswith('preexisting_relation'),
                                                  r.get('occurrence_id', '')))[0]
            origins = {r.get('origin', 'scan').startswith('preexisting_relation') for r in rows}
            emit('seed_scan_target_disagreement' if len(origins) > 1 else 'same_phrase_multiple_targets',
                 fid, primary, 'The identical normalized phrase has distinct effective existing targets in the same formulation. A general/specialized decomposition or multiple legitimate prerequisites may explain this; compare all target definitions before judging.', related=rows)

    # Compare exact phrases across stored alternatives, never raw dependency
    # set differences. Differing prerequisites alone are legitimate.
    variants = defaultdict(list)
    for (fid, phrase), rows in groups.items():
        if phrase:
            variants[(forms[fid]['meaning_id'], phrase)].extend(rows)
    for (mid, phrase), rows in sorted(variants.items()):
        fids = sorted({r['from_formulation'] for r in rows})
        target_sets = {fid: {r['target_meaning_id'] for r in rows if r['from_formulation'] == fid}
                       for fid in fids}
        if len(fids) > 1 and len({tuple(sorted(v)) for v in target_sets.values()}) > 1:
            primary = min(rows, key=lambda r: (r['from_formulation'], r.get('occurrence_id', '')))
            emit('variant_phrase_target_difference', primary['from_formulation'], primary,
                 'Stored alternatives of this meaning attach the identical normalized phrase to different target sets. Alternative formulations need not have the same prerequisites. Review the contextual differences, not just the names.', related=rows)

    # Deduplicate identical occurrence/code leads; no deduplication of distinct
    # mathematical identities or source occurrences.
    unique = {}
    for f in findings:
        key = (f['code'], f['formulation_id'], f.get('occurrence_id'))
        unique.setdefault(key, f)
    anchored = []
    for f in unique.values():
        related = f.get('related_references', [])
        target_ids = sorted({r['target_meaning_id'] for r in [f.get('reference', {}), *related]
                             if r.get('target_meaning_id') in targets})
        related_fids = sorted({r['from_formulation'] for r in related
                               if r.get('from_formulation') in forms})
        row = dict(f, occurrence_id=f.get('occurrence_id'), target_meaning_ids=target_ids,
            related_formulation_ids=related_fids,
            concern_kind='mechanical_integrity' if f['severity'] == 'integrity' else 'mathematical_review_lead',
            mathematics_confirmed=False)
        # Source-node anchors alone cannot detect target revisions, resolutions
        # or seed changes. The optional existing ledger extension binds all of
        # that evidence without altering legacy review fingerprints elsewhere.
        row['evidence_sha256'] = digest({'diagnostic_version': 1,
            'finding': {k: row[k] for k in ('code', 'description', 'version_sha256', 'effective_node_sha256')},
            'effective_source_references': by_form[row['formulation_id']],
            'related': {fid: [forms[fid], hashes.get(fid), by_form[fid]] for fid in related_fids},
            'targets': {mid: targets[mid]['target_evidence_sha256'] for mid in target_ids}})
        anchored.append(row)
    # Existing scoring applied to the full projection, including seed and
    # candidate-resolution fan-in. It does not recompute finding node anchors.
    projected_nodes = {fid: {'references': refs} for fid, refs in by_form.items()}
    ranked = rank_findings(anchored, projected_nodes, inv, snapshot.get('review_ledger', []))
    # Bounded evidence bonuses preserve integrity > high > review ordering.
    # Impact scoring alone otherwise fills the first page with repetitions of
    # the same generic/specialized module target pair.
    bonuses = {'explicit_qualifier_contrast': 120,
               'subset_predicate_to_ambient_space': 100,
               'target_restriction_not_explicit': 40}
    for row in ranked['needing_review']:
        row['impact_priority_score'] = row['priority_score']
        row['evidence_priority_bonus'] = bonuses.get(row['code'], 0)
        row['priority_score'] += row['evidence_priority_bonus']
    ranked['needing_review'].sort(key=lambda r: (-r['priority_score'], r['code'],
        r['formulation_id'], r.get('occurrence_id') or ''))
    selected = ranked['needing_review'] if exhaustive else ranked['needing_review'][:limit]
    # Context tables deduplicate source/target text shared by multiple leads.
    selected_fids = {fid for row in selected for fid in [row['formulation_id'], *row['related_formulation_ids']]}
    selected_targets = {mid for row in selected for mid in row['target_meaning_ids']}
    report = {'schema_version': 1, 'read_only': True, 'mathematics_certified': False,
        'external_research_performed': False, 'automatic_edits': False,
        'graph_scope': 'All stored formulations and effective scan/seed dependencies; aliases, version-valid resolutions and seed overrides replayed. No formulation is silently selected.',
        'inventory_sha256': inv['source_inventory_sha256'],
        'effective_evidence_sha256': digest([inv, nodes, references]),
        'state': snapshot['state']['summary'],
        'summary': {'total_review_candidates': len(ranked['needing_review']),
            'returned': len(selected), 'omitted': len(ranked['needing_review']) - len(selected),
            'exhaustive': exhaustive, 'accepted_count': ranked['accepted_count'],
            'stale_review_count': ranked['stale_review_count'],
            'by_code': ranked['review_by_code'],
            'mechanical_integrity_count': sum(f['severity'] == 'integrity' for f in ranked['needing_review']),
            'effective_reference_count': len(references)},
        'findings': selected,
        'source_formulations': {fid: {'source': forms[fid], 'effective_node_sha256': hashes.get(fid),
                                     'effective_references': by_form[fid]} for fid in sorted(selected_fids)},
        'target_meanings': {mid: targets[mid] for mid in sorted(selected_targets)},
        'cycle_summary': {k: v for k, v in baseline['summary'].items() if 'cycle' in k},
        'formulation_choice_components': [{k: c[k] for k in (
            'meaning_ids', 'classification', 'acyclic_selection_witness',
            'blocking_core_meaning_ids', 'requires_mathematical_review')}
            for c in baseline['cycle_analysis']['components']],
        'limitations': [
            'Review leads are evidence of textual contrasts or target differences, not proofs of mathematical inconsistency.',
            'No automatic synonymy, qualifier implication, arrow reversal, object equivalence or validity judgment.',
            'Only explicit qualifier vocabulary and exact normalized reference phrases are compared; absence of a lead is not correctness.',
            'Use evidence_sha256 with existing review-ledger fields for accepted reviews; legacy source-only reviews cannot suppress changed target/seed evidence.',
            'Formulation-choice cycles are separately summarized, never interpreted as automatic mathematical errors.']}

    if 'candidate_context_reviews' in snapshot:
        from .dependency_context_reviews import validated_view
        report['candidate_context_reviews'] = validated_view(snapshot)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--context-review-log', type=Path)
    parser.add_argument('--context-review-checkpoint', type=Path)
    parser.add_argument('--qualification-ledger', type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--limit', type=int, default=12)
    group.add_argument('--exhaustive', action='store_true')
    args = parser.parse_args()
    if bool(args.context_review_log) != bool(args.context_review_checkpoint):
        parser.error('Context review log and trusted checkpoint must be supplied together')
    if args.qualification_ledger and not args.context_review_log:
        parser.error('Qualification ledger requires an explicit context review log')
    if args.context_review_log:
        from .dependency_context_reviews import attach_review_files, load_context_snapshot
        snapshot = attach_review_files(load_context_snapshot(args.workspace), args.context_review_log, args.context_review_checkpoint,
                                       qualification_ledger_path=args.qualification_ledger)
    else:
        snapshot = load_live_snapshot(args.workspace)
    print(json.dumps(build_worklist(snapshot, limit=args.limit,
                                    exhaustive=args.exhaustive), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
