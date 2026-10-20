"""Apply source-screened Wave 2 dependency links without rewriting Wave 1 reviews.

Guards:
* all 440 existing/added formulations have a review entry;
* all prior 445 screened links remain present and linked to their source reviews;
* all 24 incoming links have precise source phrase and source/target provenance;
* old no-target / ambiguity outcomes may be superseded ONLY with individual
  documented, newly supported links and explicit override events;
* no self-links or directed definition-dependency cycles.
"""
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter,defaultdict
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .stage5_review_gate import atomic_jsonl

def locator(meaning,observation_map):
    if isinstance(meaning.get("source_citation"),dict):
        return meaning["source_citation"].get("url")
    form=meaning["formulations"][0]
    ids=form.get("evidence_ids",[])
    return observation_map[ids[0]]["locator"] if ids and ids[0] in observation_map else None

def check_cycles(meanings,rels):
    by_form={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
    graph=defaultdict(set)
    for rel in rels.values():
        if rel["relation_type"]=="definition_uses":
            fr=by_form.get(rel["from_formulation"])
            if fr is None:
                raise PipelineError("Undefined graph source")
            to=rel["target_meaning"]
            if fr==to:
                raise PipelineError("Self-referential definition link")
            graph[fr].add(to)
    color={}
    def visit(u):
        if color.get(u)==1:
            raise PipelineError("Definition dependency cycle introduced: "+u)
        if color.get(u)==2:
            return
        color[u]=1
        for v in graph.get(u,set()):
            visit(v)
        color[u]=2
    for node in list(graph):
        visit(node)

def run(root,batch):
    w=Workspace(root)
    if not (w.root/"state/baseline.json").exists():
        raise PipelineError("Requires independently forked Wave 2")
    if w.state("relations").get("sealed"):
        raise PipelineError("Wave 2 relations already sealed")
    meanings=w.records("meanings")
    observations=w.records("observations")
    forms={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    expected_catalog=(487,499) if batch.name.endswith("batch_44.jsonl") else (485,497) if batch.name.endswith("batch_41.jsonl") else (480,492) if batch.name.endswith("batch_38.jsonl") else (479,491) if batch.name.endswith("batch_35.jsonl") else (477,489) if batch.name.endswith("batch_32.jsonl") else (476,488) if batch.name.endswith("batch_28.jsonl") else (474,486) if batch.name.endswith("batch_25.jsonl") else (471,483) if batch.name.endswith("batch_22.jsonl") else (469,481) if batch.name.endswith("batch_19.jsonl") else (462,474) if (batch.name.endswith("batch_17.jsonl") or batch.name.endswith("batch_18.jsonl")) else (455,467) if batch.name.endswith("batch_12.jsonl") else (453,465) if batch.name.endswith("batch_10.jsonl") else (447,459) if batch.name.endswith("batch_08.jsonl") else (441,453) if batch.name.endswith("batch_07.jsonl") else (435,447) if batch.name.endswith("batch_06.jsonl") else (431,443) if batch.name.endswith("batch_05.jsonl") else (428,440)
    if (len(meanings),len(forms))!=expected_catalog:
        raise PipelineError("Outdated or altered meaning catalog for curated relationship batch")
    if batch.name.endswith("batch_38.jsonl"):
        source=w.root/"state/wave2_foundations_batch_36.json"
        review=w.root/"state/wave2_strong_transcendence37_meaning_screen.json"
        snapshot=w.root/"state/wave2_formulation_reviews_snapshot_491_before_strong_transcendence37.jsonl"
        if not source.exists() or not review.exists() or not snapshot.exists():
            raise PipelineError("Strong transcendence batch requires independently verified Stacks source, mathematical screening and 491-review history")
        a=json.loads(source.read_text(encoding="utf-8"))
        b=json.loads(review.read_text(encoding="utf-8"))
        if (a.get("direct_definition_tag")!="00PZ" or
            not a.get("zero_divisor_sensitive_coefficient_condition_preserved") or
            b.get("screened_meanings")!=480 or
            b.get("individually_reviewed_formulations")!=492 or
            not b.get("previous_648_links_preserved") or
            not b.get("source_scoped_zero_divisor_condition_unchanged") or
            len(jsonl(snapshot))!=491):
            raise PipelineError("Missing individually source-screened meaning or historical formulation provenance")
    if batch.name.endswith("batch_41.jsonl"):
        source=w.root/"state/wave2_foundations_batch_39.json"
        screen=w.root/"state/wave2_alt_sources40_meanings_screened.json"
        historical=w.root/"state/wave2_formulation_reviews_snapshot_492_before_alt40.jsonl"
        if not (source.exists() and screen.exists() and historical.exists()):
            raise PipelineError("Independent alternative-source links require original 492-review history and complete source/meaning screens")
        earlier=json.loads(source.read_text(encoding="utf-8"))
        audited=json.loads(screen.read_text(encoding="utf-8"))
        if (earlier.get("original_planetmath_pages_remain_unverified")!=27
                or audited.get("screened_meanings")!=485
                or audited.get("reviewed_formulations")!=497
                or not audited.get("previous_650_screened_links_preserved")
                or not audited.get("unital_and_nonunital_boolean_ring_conventions_distinct")
                or len(jsonl(historical))!=492):
            raise PipelineError("Missing independent, source-scoped variant screening or historical review lineage")
    if batch.name.endswith("batch_44.jsonl"):
        source=w.root/"state/wave2_graph_source_batch_42.json"
        approved=w.root/"state/wave2_graph_meaning_screen_batch_43.json"
        previous_497=w.root/"state/wave2_formulation_reviews_snapshot_497_before_graph43.jsonl"
        if not (source.exists() and approved.exists() and previous_497.exists()):
            raise PipelineError("Graph link batch needs independently sourced and individually screened graph foundations and historical reviews")
        sr=json.loads(source.read_text(encoding="utf-8"))
        mr=json.loads(approved.read_text(encoding="utf-8"))
        if (sr.get("terms_after")!=384 or sr.get("observations_after")!=807 or
            mr.get("contextual_meanings")!=487 or mr.get("formulations")!=499 or
            not mr.get("simple_vs_multigraph_multiplicity_separated") or
            not mr.get("previous_497_review_dispositions_preserved") or
            len(jsonl(previous_497))!=497):
            raise PipelineError("Graph conventions or immutable 497-review provenance incomplete")
    catalog_digest=digest(list(meanings.values()))
    if batch.name.endswith("batch_06.jsonl"):
        checked=w.root/"state/wave2_new_foundations_batch_06_screened.json"
        correction=w.root/"state/wave2_presheaf_math_corrections.json"
        if not checked.exists() or not correction.exists():
            raise PipelineError("Batch 06 requires verified screened field/functor/groupoid/pseudofunctor and corrected presheaves")
        screened_report=json.loads(checked.read_text(encoding="utf-8"))
        corrected_report=json.loads(correction.read_text(encoding="utf-8"))
        if (screened_report.get("formulations")!=447 or
            screened_report.get("screened_relations_retained")!=545 or
            not screened_report.get("historical_snapshot_verified") or
            not corrected_report.get("groupoid_valued_strict_source_correction_applied")):
            raise PipelineError("Missing audited meaning lineage for Batch 06")
        snapshot=w.root/"state/wave2_formulation_reviews_snapshot_443_before_new_foundations.jsonl"
        historical=jsonl(snapshot)
        if len(historical)!=443:
            raise PipelineError("Missing historical 443-formulation review snapshot")
    if batch.name.endswith("batch_07.jsonl"):
        approved=w.root/"state/wave2_foundations_batch_07_screened.json"
        if not approved.exists():
            raise PipelineError("Batch 07 requires committed individual source and meaning screening for elementary definitions")
        proof=json.loads(approved.read_text(encoding="utf-8"))
        history=w.root/"state/wave2_formulation_reviews_snapshot_447_before_foundations07.jsonl"
        if (proof.get("independently_screened_meanings")!=441 or
            proof.get("total_formulations")!=453 or
            proof.get("screened_links_unchanged")!=563 or
            not proof.get("binary_operation_and_relation_variants_kept_separate") or
            len(jsonl(history))!=447):
            raise PipelineError("Batch 07 lacks exact source-scoped mathematical screening history")
    if batch.name.endswith("batch_08.jsonl"):
        checked=w.root/"state/wave2_foundations_batch_09_screened.json"
        snap=w.root/"state/wave2_formulation_reviews_snapshot_453_before_foundations09.jsonl"
        if not checked.exists() or not snap.exists():
            raise PipelineError("Batch 08 requires individually screened typed and bare graph and subset meanings")
        proof=json.loads(checked.read_text(encoding="utf-8"))
        if (proof.get("independently_screened_meanings")!=447 or
            proof.get("individually_reviewed_formulations")!=459 or
            proof.get("screened_relations_preserved")!=574 or
            not proof.get("typed_graph_and_bare_graph_separate_conventions") or
            len(jsonl(snap))!=453):
            raise PipelineError("Missing audited six-mathematical-meaning lineage for batch 08")
    if batch.name.endswith("batch_10.jsonl"):
        checked=w.root/"state/wave2_foundations_batch_10_screened.json"
        archived=w.root/"state/wave2_formulation_reviews_snapshot_459_before_foundations10.jsonl"
        no_targets=w.root/"state/wave2_foundation_dependency_no_target_batch_02.json"
        if not checked.exists() or not archived.exists() or not no_targets.exists():
            raise PipelineError("Batch 10 requires screened source contexts and complete prior review audit")
        proof=json.loads(checked.read_text(encoding="utf-8"))
        if (proof.get("contextual_meanings")!=453 or proof.get("formulation_reviews")!=465 or
            proof.get("screened_links_preserved")!=582 or
            not proof.get("unital_and_nonunital_ring_maps_distinct") or
            not proof.get("wellorder_nonempty_subset_requirement_checked") or
            len(jsonl(archived))!=459 or
            json.loads(no_targets.read_text(encoding="utf-8")).get("formulation_reviews_without_initial_decision")!=0):
            raise PipelineError("Batch 10 source-specific meaning and historical review checks failed")
    if batch.name.endswith("batch_12.jsonl"):
        approved=w.root/"state/wave2_foundations_batch_12_screened.json"
        old=w.root/"state/wave2_formulation_reviews_snapshot_465_before_foundations12.jsonl"
        if not approved.exists() or not old.exists():
            raise PipelineError("Site link batch 12 requires approved independent Stacks site/family source screening")
        proof=json.loads(approved.read_text(encoding="utf-8"))
        if (proof.get("contextual_meanings")!=455 or
            proof.get("formulations")!=467 or
            proof.get("screened_links_preserved")!=600 or
            not proof.get("site_family_coverage_not_equated_to_sieve_topology") or
            not proof.get("indexed_family_empty_index_set_allowed") or
            len(jsonl(old))!=465):
            raise PipelineError("Source-scoped site/family and historical 465-review gate failed")
    if batch.name.endswith("batch_17.jsonl"):
        home=w.root/"state/wave2_foundations_batch_16_screened.json"
        earlier=w.root/"state/wave2_foundations_batch_14_screened.json"
        snapshot=w.root/"state/wave2_formulation_reviews_snapshot_471_before_category16.jsonl"
        if not home.exists() or not earlier.exists() or not snapshot.exists():
            raise PipelineError("Homological link batch requires separately screened category axioms and historical review snapshot")
        h=json.loads(home.read_text(encoding="utf-8"))
        e=json.loads(earlier.read_text(encoding="utf-8"))
        if (h.get("reviewed_formulations")!=474 or
            h.get("screened_links_preserved")!=606 or
            not h.get("coimage_image_comparison_axiom_preserved") or
            not h.get("preadditive_additive_abelian_hierarchy_not_conflated") or
            not e.get("concrete_and_categorical_kernels_context_specific") or
            not e.get("preadditive_kernels_cokernels_not_assumed_to_exist") or
            len(jsonl(snapshot))!=471):
            raise PipelineError("Incomplete rigorous source and historical baseline for 15 homological relations")
    if batch.name.endswith("batch_18.jsonl"):
        correction=w.root/"state/wave2_strict2cat_equivalence_context_correction.json"
        historical=w.root/"state/wave2_formulation_reviews_snapshot_474_before_strict2cat.jsonl"
        if not correction.exists() or not historical.exists():
            raise PipelineError("Strict 2-category source-correction review and original held disposition must be preserved before batch 18")
        proof=json.loads(correction.read_text(encoding="utf-8"))
        if (proof.get("screened_meanings")!=462 or
            proof.get("formulation_reviews_preserved")!=474 or
            proof.get("screened_links_preserved")!=621 or
            not proof.get("weak_bicategory_variant_remains_future_research") or
            not proof.get("source_specific_strict_category_definition_screened") or
            not proof.get("held_ambiguity_original_disposition_preserved") or
            len(jsonl(historical))!=474):
            raise PipelineError("Unverified source-specific strict two-category equivalence context or review history")
    if batch.name.endswith("batch_19.jsonl"):
        screened=w.root/"state/wave2_analysis20_meaning_screen.json"
        history=w.root/"state/wave2_formulation_reviews_snapshot_474_before_analysis20.jsonl"
        if not screened.exists() or not history.exists():
            raise PipelineError("OpenStax link batch requires audited seven-meaning screening and frozen 474-review snapshot")
        proof=json.loads(screened.read_text(encoding="utf-8"))
        if (proof.get("meanings_total")!=469 or
            proof.get("formulations_total")!=481 or
            proof.get("prior_screened_links_preserved")!=622 or
            not proof.get("historical_474_formulation_reviews_preserved") or
            len(jsonl(history))!=474):
            raise PipelineError("Historical source-screening lineage failed for OpenStax link")
    if batch.name.endswith("batch_22.jsonl"):
        proof_path=w.root/"state/wave2_foundations_batch_22_screened.json"
        history=w.root/"state/wave2_formulation_reviews_snapshot_481_before_analysis22.jsonl"
        if not proof_path.exists() or not history.exists():
            raise PipelineError("Three calculus links require audited derivative/absolute meanings and prior 481-review snapshot")
        proof=json.loads(proof_path.read_text(encoding="utf-8"))
        if (proof.get("screened_meanings")!=471 or
            proof.get("formulation_reviews")!=483 or
            proof.get("screened_links_preserved")!=623 or
            not proof.get("prior_481_individual_reviews_preserved") or
            not proof.get("absolute_value_vs_distance_distinction_preserved") or
            len(jsonl(history))!=481):
            raise PipelineError("New real analysis meanings or historical provenance unverified")
    if batch.name.endswith("batch_25.jsonl"):
        evidence=w.root/"state/wave2_foundations_batch_24_screened.json"
        archived=w.root/"state/wave2_formulation_reviews_snapshot_483_before_foundations24.jsonl"
        if not evidence.exists() or not archived.exists():
            raise PipelineError("Mathematically screened polynomial/integral/moment meanings and 483-review snapshot required")
        proof=json.loads(evidence.read_text(encoding="utf-8"))
        historical=jsonl(archived)
        if (proof.get("screened_contextual_meanings")!=474 or
            proof.get("formulations")!=486 or
            proof.get("previous_screened_links_preserved")!=626 or
            not proof.get("moment_finiteness_hypotheses_retained") or
            not proof.get("zero_polynomial_degree_context_separated") or
            not proof.get("tagged_riemann_vs_improper_integrals_not_conflated") or
            len(historical)!=483):
            raise PipelineError("Incomplete individual source-scope and historical review verification")
    if batch.name.endswith("batch_28.jsonl"):
        screened=w.root/"state/wave2_foundations_batch_27_screened.json"
        snapshot=w.root/"state/wave2_formulation_reviews_snapshot_486_before_measure27.jsonl"
        if not screened.exists() or not snapshot.exists():
            raise PipelineError("Measure/moment batch requires separately screened sigma-algebra and measure and 486 historical reviews")
        proof=json.loads(screened.read_text(encoding="utf-8"))
        if (proof.get("screened_contextual_meanings")!=476 or
            proof.get("reviewed_formulations")!=488 or
            proof.get("screened_links_preserved")!=634 or
            not proof.get("measure_normalization_at_empty_set_retained") or
            not proof.get("extended_nonnegative_measure_values_retained") or
            not proof.get("sigma_algebra_topology_conventions_not_equated") or
            not proof.get("riemann_vs_lebesgue_stieltjes_contexts_not_conflated") or
            len(jsonl(snapshot))!=486):
            raise PipelineError("Unverified source-scope or historical review lineage for measure/moment dependencies")
    if batch.name.endswith("batch_32.jsonl"):
        proof=w.root/"state/wave2_uniformizer31_meaning_screen.json"
        historical=w.root/"state/wave2_formulation_reviews_snapshot_488_before_uniformizer31.jsonl"
        if not proof.exists() or not historical.exists():
            raise PipelineError("Uniformizer dependencies require audited Stacks definition screen and all 488 historical decisions")
        report=json.loads(proof.read_text(encoding="utf-8"))
        if (report.get("meaning_count")!=477 or
            report.get("reviewed_formulations")!=489 or
            report.get("screened_links_preserved")!=640 or
            not report.get("uniformizer_specific_to_DVR") or
            not report.get("principal_generator_equality_required") or
            len(jsonl(historical))!=488):
            raise PipelineError("DVR uniformizer source meaning or historical review lineage invalid")
    if batch.name.endswith("batch_35.jsonl"):
        report_path=w.root/"state/wave2_embedded34_meaning_screen.json"
        history_path=w.root/"state/wave2_formulation_reviews_snapshot_489_before_embedded34.jsonl"
        if not report_path.exists() or not history_path.exists():
            raise PipelineError("Missing individually screened Stacks 10.38.1 and 10.112.5 meanings with preserved prior review history")
        previous_report=json.loads(report_path.read_text(encoding="utf-8"))
        if (previous_report.get("screened_meanings")!=479 or
            previous_report.get("formulation_reviews")!=491 or
            previous_report.get("screened_links_unchanged")!=643 or
            not previous_report.get("ideal_coefficient_power_hypotheses_explicit") or
            not previous_report.get("fibre_prime_contraction_and_local_ring_explicit") or
            len(jsonl(history_path))!=489):
            raise PipelineError("Exact Stacks mathematical source and original 489 review history missing")
    ledger_path=w.root/"state/wave2_formulation_reviews.jsonl"
    reviews=jsonl(ledger_path)
    review_map={r["formulation_id"]:r for r in reviews}
    if len(reviews)!=len(forms) or len(review_map)!=len(forms) or set(review_map)!=set(forms):
        raise PipelineError("Missing or repeated formulation review identity")
    if any(r.get("meaning_catalog_digest")!=catalog_digest for r in reviews):
        raise PipelineError("Wave 2 relation review is stale against meanings")
    previous=w.records("relations")
    if len(previous) not in (445,469,481,505,529,545,563,574,582,600,606,621,622,623,626,634,640,643,648,650,655,659):
        raise PipelineError("Unexpected relationship ledger size, check earlier batches")
    incoming=jsonl(batch)
    batch_number = next((n for n in ("01","02","03","04","05","06","07","08","10","12","17","18","19","22","25","28","32","35","38","41","44") if batch.name.endswith(f"batch_{n}.jsonl")),None)
    if batch_number is None:
        raise PipelineError("Unknown curated relationship batch; explicit scope required")
    expected_count={"01":24,"02":12,"03":24,"04":24,"05":16,"06":18,"07":11,"08":8,"10":18,"12":6,"17":15,"18":1,"19":1,"22":3,"25":8,"28":6,"32":3,"35":5,"38":2,"41":5,"44":4}[batch_number]
    if len(incoming)!=expected_count or len({r.get("id") for r in incoming})!=expected_count:
        raise PipelineError(f"Expected {expected_count} distinct curated research relationships")
    before_count={"01":445,"02":469,"03":481,"04":505,"05":529,"06":545,"07":563,"08":574,"10":582,"12":600,"17":606,"18":621,"19":622,"22":623,"25":626,"28":634,"32":640,"35":643,"38":648,"41":650,"44":655}[batch_number]
    if len(previous) not in (before_count,before_count+expected_count):
        raise PipelineError(f"Incorrect previous link count for batch {batch_number}: {len(previous)}")
    fromlinks=defaultdict(list)
    for row in incoming:
        fid,mid=row.get("from_formulation"),row.get("target_meaning")
        if fid not in forms or mid not in meanings:
            raise PipelineError("Invalid reviewed relation endpoint: "+str(row.get("id")))
        source,form=forms[fid]
        target=meanings[mid]
        if source["id"]==mid:
            raise PipelineError("Self dependency")
        if form["review_state"]!="screened" or any(
             f["review_state"]!="screened" for f in target["formulations"]):
            raise PipelineError("Unscreened mathematical endpoint")
        if row.get("relation_type")!="definition_uses" or row.get("review_state")!="screened":
            raise PipelineError("Unexpected relationship classification")
        if row.get("human_verified") is not False:
            raise PipelineError("No human peer verification may be invented")
        phrase=row.get("source_phrase")
        if not phrase or phrase.casefold() not in form["text"].casefold():
            raise PipelineError("No exact source formulation anchor for "+row["id"])
        if row.get("source_locator")!=locator(source,observations) or row.get(
                "target_locator")!=locator(target,observations):
            raise PipelineError("Source/target locator diverged from primary evidence")
        if len(row.get("editorial_reason","").strip())<65:
            raise PipelineError("Mathematical rationale too short")
        if row["id"] in previous and previous[row["id"]]!=row:
            raise PipelineError("Previously screened Wave 2 link has changed")
        fromlinks[fid].append(row)
    proposed={**previous,**{r["id"]:r for r in incoming}}
    check_cycles(meanings,proposed)
    for fid,items in fromlinks.items():
        review=review_map[fid]
        if review["decision"] not in (
             "needs_review","linked","no_supported_target","held_ambiguity"):
            raise PipelineError("Unknown old link disposition")
        if review["decision"] in ("no_supported_target","held_ambiguity"):
            historical=review.get("original_wave1_disposition")
            wave2_audited=(historical is None and
                 review.get("source")=="wave2_individual_mathematical_no_supported_target_review" and
                 bool(review.get("original_wave2_pending_reason")) and
                 bool(review.get("reviewed_by")))
            if review["relation_ids"] or (historical not in
                 ("no_supported_target","held_ambiguity") and not wave2_audited):
                raise PipelineError("Invalid or undocumented attempted override of a reviewed no-target/ambiguity decision")
        for rel in items:
            if rel["id"] in review["relation_ids"] and rel["id"] not in previous:
                raise PipelineError("Review claims a non-existing relationship")
    # Persist explicit inherited-decision override history before mutation.
    override=[]
    for fid,items in sorted(fromlinks.items()):
        review=review_map[fid]
        if review["original_wave1_disposition"] in ("no_supported_target","held_ambiguity"):
            override.append({
                "formulation_id":fid,
                "old_wave1_disposition":review["original_wave1_disposition"],
                "old_review_digest":review["original_review_digest"],
                "original_editorial_reason":review["editorial_reason"] if not review.get(
                    "wave2_override_reason") else review.get("original_editorial_reason"),
                "new_link_ids":sorted(x["id"] for x in items),
                "override_reason":"Previously missing source-specific mathematical target now has an independently evidenced and screened Wave 2 meaning; compare each new link's exact formulation anchor, hypothesis scope and source locator.",
                "reviewed_by":"assistant_wave2_individual_mathematical_source_comparison_2026_10_19",
                "human_verified":False
            })
    override_path=w.root/f"events/wave2_link_disposition_overrides_batch{batch_number}.jsonl"
    override_path.parent.mkdir(parents=True,exist_ok=True)
    override_payload="".join(canonical(x)+"\n" for x in override)
    if override_path.exists() and override_path.read_text(encoding="utf-8")!=override_payload:
        raise PipelineError("Prior link-disposition override evidence differs; refuse silent revision")
    override_path.write_text(override_payload,encoding="utf-8")

    # Workspace ingest is idempotent for identical link IDs. All mathematical
    # consistency checks above happen before it writes any data.
    result=w.ingest("relations",batch,batch_size=expected_count)
    for fid,links in fromlinks.items():
        review=review_map[fid]
        was=review["decision"]
        if was in ("no_supported_target","held_ambiguity") and not review.get("wave2_override_reason"):
            review["original_editorial_reason"]=review["editorial_reason"]
            review["wave2_override_reason"]="Reassessed after separately sourced and screened Wave 2 foundational meanings became available; the individual mathematical evidence is recorded with each relationship."
        review["decision"]="linked"
        review["relation_ids"]=sorted(set(review["relation_ids"])|{r["id"] for r in links})
        review["editorial_reason"]="Individually checked current mathematical source formulation and new contextual prerequisite meaning against exact source locators; individual reasons are preserved on each relation."
        review["reviewed_by"]="assistant_wave2_individual_mathematical_source_comparison_2026_10_19"
        review["source"]="wave2_explicit_link_review"
    atomic_jsonl(ledger_path,[review_map[k] for k in sorted(review_map)])
    actual=w.records("relations")
    if len(actual)!=before_count+expected_count or len(ledger_path.read_text(encoding="utf-8").splitlines())!=len(forms):
        raise PipelineError("Unexpected post-intake review counts")
    referred={rid for x in review_map.values() for rid in x["relation_ids"]}
    if set(actual)!=referred:
        raise PipelineError("An independent relationship is missing a formulation-specific review")
    check_cycles(meanings,actual)
    counts=dict(Counter(x["decision"] for x in review_map.values()))
    still_pending=sum(r["decision"]=="needs_review" for r in review_map.values())
    report={
      "phase":f"wave2_source_grounded_relationship_batch_{batch_number}_screened",
      "meaning_count":len(meanings),"formulation_count":len(forms),
      "total_screened_links":len(actual),
      "inherited_wave1_links_preserved":445,
      "added_source_grounded_links":expected_count,
      "link_batch_unique_source_formulations":len(fromlinks),
      "review_decisions_after_batch":counts,
      "inherited_missing_or_held_dispositions_revisited":len(override),
      "original_wave1_dispositions_preserved_in_review_fields":True,
      "newly_defined_relations_reviewed_individually":True,
      "dependency_graph_has_cycles":False,
      "pending_wave2_link_reviews":still_pending,
      "wave2_link_stage_sealed":False,
      "original_production_baseline_consulted":False,
      "human_peer_verified":False,
      "next":"Continue source verification, review the remaining new formulations and all unresolved missing-target/ambiguity cases before stage sealing."
    }
    atomic_json(w.root/f"state/wave2_link_review_batch_{batch_number}.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",required=True,type=Path)
    p.add_argument("--batch",required=True,type=Path)
    a=p.parse_args()
    print(json.dumps(run(a.workspace,a.batch),indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
