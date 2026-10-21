"""Batch134 individually review Bell, Stirling, convex hull, and simple graph degree links.

Fourteen individual source/target checks. Never invent missing independently
screened convex-set and falling-factorial meanings.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":477,"observations":946,"meanings":591}
PW="https://proofwiki.org/wiki/Definition%3A"
BELL=PW+"Bell_Number";STIR=PW+"Stirling_Numbers_of_the_Second_Kind"
HULL=PW+"Convex_Hull";DEG=PW+"Degree_of_Vertex"
PART=PW+"Set_Partition";NAT=PW+"Natural_Number"
VSPACE="https://stacks.math.columbia.edu/tag/09FM";SUB=PW+"Subset"
SIMPLE=PW+"Simple_Graph";CARD="https://stacks.math.columbia.edu/tag/000D"
F="form.wave2.cross133."
EDGES=(
 ("01",F+"bell-number","meaning.wave2.group116.set-partition","partitions",BELL,PART,
  "A Bell number counts the different UNINDEXED partitions of an n-element set into disjoint nonempty blocks. The independently reviewed set-partition definition supplies the precise counted combinatorial objects, including the empty partition for n=0."),
 ("02",F+"bell-number","meaning.wave2.set63.natural-including-zero","n∈ℕ₀",BELL,NAT,
  "Bell numbers have index n in the zero-inclusive natural numbers and the special B_0=1 base case. This existing independently screened zero-inclusive natural-number context avoids erroneously omitting the empty-set partition count."),
 ("03",F+"stirling-second-kind.1","meaning.wave2.set63.natural-including-zero","n,k∈ℕ₀",STIR,NAT,
  "The recurrence for second-kind Stirling numbers has indices n,k including zero, with Kronecker delta boundaries when n or k is zero. The independently screened zero-inclusive natural numbers supply the exact integer parameter domain."),
 ("04",F+"stirling-second-kind.2","meaning.wave2.set63.natural-including-zero","n∈ℕ₀",STIR,NAT,
  "The falling-factorial polynomial expansion identity for S(n,k) is indexed by nonnegative integer n with k=0,...,n. The zero-inclusive natural number system supplies the index domain and includes the polynomial identity x^0=1 case."),
 ("05",F+"convex-hull-real.1","meaning.b64bc15f46fe0245.vector-space-over-field","real vector space V",HULL,VSPACE,
  "A finite convex combination ∑ λ_j u_j is taken in a REAL vector space, which is a vector space over field R. The independently sourced general vector-space definition supplies addition and scalar multiplication, specialized to the real field."),
 ("06",F+"convex-hull-real.1","meaning.wave2.foundation.subset-nonstrict","U⊆V",HULL,SUB,
  "Convex hull starts with an arbitrary subset U of ambient real vector space V, including U=∅. The independently sourced nonstrict subset relation supplies U⊆V; the empty case gives conv(∅)=∅ and is not silently excluded."),
 ("07",F+"convex-hull-real.2","meaning.b64bc15f46fe0245.vector-space-over-field","real vector space V",HULL,VSPACE,
  "The intersection-of-convex-supersets construction operates inside a REAL vector space V with its vector and scalar operations. The independently screened vector-space concept supplies ambient structure without assuming a norm or finite dimensionality."),
 ("08",F+"convex-hull-real.2","meaning.wave2.foundation.subset-nonstrict","U⊆V",HULL,SUB,
  "The intersection formula quantifies over convex subsets C of V satisfying U⊆C. The generic nonstrict subset definition supplies inclusion; the separate convex-set predicate still needs its own independently reviewed meaning."),
 ("09",F+"convex-hull-real.3","meaning.b64bc15f46fe0245.vector-space-over-field","real vector space V",HULL,VSPACE,
  "The least-convex-superset property refers to subsets of an ambient real vector space. The independently reviewed vector-space context supplies the underlying addition and scalar multiplication, and no metric or completeness is required."),
 ("10",F+"convex-hull-real.3","meaning.wave2.foundation.subset-nonstrict","U⊆V",HULL,SUB,
  "The least convex superset C of U is ordered by subset inclusion and contains U. The independently screened subset relation supplies that order; minimality alone without containing all convex supersets would be insufficient."),
 ("11",F+"vertex-degree-simple.1","meaning.wave2.graph42.simple-undirected","simple undirected graph",DEG,SIMPLE,
  "The incident-edge degree definition assumes G is a simple UNDIRECTED graph with no loops or parallel edges. This independently sourced graph concept supplies the vertex set V and edge family E; multigraph incidence and loop-counting need separate contexts."),
 ("12",F+"vertex-degree-simple.1","meaning.081430bc340a055a.cardinality","cardinality",DEG,CARD,
  "The degree of v counts incident edges as a set cardinality, which may be a finite natural or infinite cardinal when the graph is infinite. The independently screened cardinality definition supplies counting without imposing finiteness."),
 ("13",F+"vertex-degree-simple.2","meaning.wave2.graph42.simple-undirected","simple undirected graph",DEG,SIMPLE,
  "Counting distinct neighbors of v matches edge incidence only for a simple loopless undirected graph. The screened simple-graph definition supplies exactly this edge structure, not a general multigraph with loop or parallel-edge multiplicity."),
 ("14",F+"vertex-degree-simple.2","meaning.081430bc340a055a.cardinality","cardinality",DEG,CARD,
  "The neighbor-count formulation is the cardinality of the set of distinct adjacent vertices; this independent cardinality meaning covers finite and infinite vertex sets. It is not generally the multigraph degree when parallel edges or loops exist.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Previous individual source-to-definition relationship changed")
    path.write_text(content,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Independent unsealed Wave2 required")
    if {k:len(w.records(k)) for k in BASE}!=BASE:
        raise PipelineError("Batch133 mathematically reviewed baseline missing")
    report=json.loads((w.root/"state/wave2_cross133_meaning_screen.json").read_text())
    if report.get("screened_meanings")!=591 or report.get("reviewed_formulations")!=632 or not report.get("degree_equivalent_only_for_simple_graphs"):
        raise PipelineError("Batch133 mathematical screening not verified")
    meanings=w.records("meanings");observations=w.records("observations")
    forms={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    if len(forms)!=632:raise PipelineError("632 individual formulations required")
    before_rel=w.records("relations")
    if len(before_rel) not in (855,869):raise PipelineError("Unexpected previous link count")
    old={i:r for i,r in before_rel.items() if not i.startswith("rel.wave2.cross134.")}
    if len(old)!=855:raise PipelineError("All 855 older screened prerequisite links must remain")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    before=jsonl(ledger);before_index={r["formulation_id"]:r for r in before}
    if (len(before)!=632 or len(before_index)!=632
        or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in before)
        or {i for r in before for i in r["relation_ids"]}!=set(before_rel)):
        raise PipelineError("Complete current individual formulation history invalid")
    links=[]
    for n,fid,target,phrase,surl,turl,reason in EDGES:
        if fid not in forms or target not in meanings:
            raise PipelineError("Missing exact independently sourced endpoint "+n)
        _,form=forms[fid];evidence=form.get("evidence_ids",[])
        if (form["review_state"]!="screened" or len(evidence)!=1 or evidence[0] not in observations
            or observations[evidence[0]]["locator"]!=surl or locator(meanings[target],observations)!=turl
            or phrase not in form["text"] or len(reason)<160):
            raise PipelineError("Unsubstantiated exact source phrase/target mathematical link "+n)
        links.append({"id":"rel.wave2.cross134."+n,"from_formulation":fid,
           "target_meaning":target,"relation_type":"definition_uses","review_state":"screened",
           "source_phrase":phrase,"source_locator":surl,"target_locator":turl,
           "editorial_reason":reason,
           "reviewed_by":"assistant_independent_bell_stirling_convex_degree_prerequisite_screen_2026_10_20",
           "human_verified":False})
    new={fid for fid in forms if fid.startswith(F)}
    if len(new)!=8 or len(links)!=14 or {r["from_formulation"] for r in links}!=new:
        raise PipelineError("All eight mathematical formulations must have fourteen source-screened links")
    check_cycles(meanings,{**old,**{r["id"]:r for r in links}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_632_before_cross134.jsonl"
    if len(before_rel)==855:
        if any(before_index[fid]["decision"]!="needs_review" or before_index[fid]["relation_ids"] for fid in new):
            raise PipelineError("Fresh forms not awaiting individual prerequisite review")
        content=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=content:
            raise PipelineError("Older 632 reviewed-form snapshot altered")
        archive.write_text(content,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_632_before_cross134.json",
           {"rows":632,"prior_links":855,"sha256":hashlib.sha256(content.encode()).hexdigest(),"human_peer_verified":False})
    saved=jsonl(archive);old_by={r["formulation_id"]:r for r in saved}
    if len(saved)!=632 or len(old_by)!=632:raise PipelineError("Full prior individual review snapshot missing")
    store(w.root/"wave2/cross134_individual_source_screened_links.jsonl",links)
    intake=store(w.root/"intake/cross134_links.jsonl",links)
    if len(before_rel)==855:w.ingest("relations",intake,batch_size=14)
    relations=w.records("relations")
    if len(relations)!=869 or any(relations.get(r["id"])!=r for r in links):
        raise PipelineError("Fourteen new screened links missing")
    check_cycles(meanings,relations)
    revised=[]
    for old_row in saved:
        row=dict(old_row);fid=row["formulation_id"]
        if fid in new:
            ids=[r["id"] for r in links if r["from_formulation"]==fid]
            if not ids:raise PipelineError("Accepted source formulation lacks directly screened links")
            row["relation_ids"]=ids;row["decision"]="linked"
            row["reviewed_by"]="assistant_independent_bell_stirling_convex_degree_prerequisite_screen_2026_10_20"
            row["source"]="independent_combinatorics_convex_graph_prerequisites_batch134"
            row["editorial_reason"]="Individual source phrase and target meaning reviewed; old definitions and decisions untouched."
        revised.append(row)
    if len(before_rel)==869:
        if {r["formulation_id"]:r for r in before}!={r["formulation_id"]:r for r in revised}:
            raise PipelineError("Completed individual review changes on rerun")
    else:atomic_jsonl(ledger,sorted(revised,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);index={r["formulation_id"]:r for r in final}
    if len(final)!=632 or len(index)!=632:raise PipelineError("632 individual decisions required")
    for fid,p in old_by.items():
        if fid not in new and index[fid]!=p:
            raise PipelineError("Prior unrelated review disposition mutated")
    if {i for r in final for i in r["relation_ids"]}!=set(relations):
        raise PipelineError("Missing a screened edge from individual review ledger")
    if dict(Counter(r["decision"] for r in final))!={"linked":626,"no_supported_target":6}:
        raise PipelineError("Complete review decision counts differ")
    for path in ("wave2/conv125_quarantined_source_claims.jsonl","wave2/quot118_quarantined_source_claims.jsonl","wave2/directional112_quarantined_source_claims.jsonl"):
        held=jsonl(w.root/path)
        if len(held)!=1 or held[0]["observation_id"] in {i for m in meanings.values() for f in m["formulations"] for i in f["evidence_ids"]}:
            raise PipelineError("Historical erroneous source claim promoted")
    gaps=[{"topic":"Stirling numbers as polynomial coefficients","missing_target":"falling factorial of a variable with index k","action":"independently verify direct definition before adding mathematical prerequisite"},
      {"topic":"Stirling number recurrence","missing_target":"Kronecker delta δ_(n,k)","action":"independently verify and add source-specific context if still missing"},
      {"topic":"convex hull least convex supersets","missing_target":"convex subset of a real vector space","action":"independently verify and add mathematical target before any retroactive link"}]
    store(w.root/"wave2/cross134_missing_prerequisite_targets.jsonl",gaps)
    result={"batch":134,"screened_meanings":591,"reviewed_formulations":632,"screened_relationships":869,
       "new_individual_links":14,"all_855_prior_links_preserved":True,
       "all_624_unrelated_formulation_reviews_preserved":True,
       "all_eight_new_formulations_individually_linked":True,
       "stirling_base_cases_and_bell_zero_case_preserved":True,
       "convex_hull_source_variants_equivalent":True,"vertex_degree_simple_graph_scope_retained":True,
       "missing_convex_set_falling_factorial_delta_targets_explicitly_logged":True,
       "three_source_held_issues_untouched":True,"dependency_graph_has_cycles":False,
       "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
       "next":"Batch135 independent mathematical breadth beyond recent Stirling/Bell/convex hull/degree contexts; may selectively source three logged prerequisite gaps."}
    atomic_json(w.root/"state/wave2_cross134_link_review.json",result);return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
