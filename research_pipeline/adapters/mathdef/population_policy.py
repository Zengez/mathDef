"""Fast mathDef-only intake policy; not an automated mathematical proof."""
from pathlib import Path
from research_pipeline.engine.core import PipelineError, Workspace

def validate_package(package: dict, workspace: Path):
    config = Workspace(workspace).config()
    if config.get("independent_second_wave") is not True:
        raise PipelineError("mathDef population requires independent unsealed Wave 2")
    for meaning in package.get("meanings", []):
        for form in meaning.get("formulations", []):
            rationale = form.get("mathematical_rationale", "")
            if len(rationale.strip()) < 60:
                raise PipelineError("New formulation requires an explicit mathematical rationale: " + form.get("id", "?"))
    for rel in package.get("relations", []):
        if rel.get("relation_type") == "definition_uses" and not rel.get("source_phrase") and not rel.get("target_query"):
            raise PipelineError("Prerequisite needs a source phrase or unresolved-target query")
    if package.get("production_corpus_consulted", False):
        raise PipelineError("Production mathematical corpus may not seed independent research")
    return {"mathdef_intake_policy": "passed", "human_peer_verified": False}
