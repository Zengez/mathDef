"""Deterministic, resumable stages. Never consults the existing mathDef corpus.

A run imports externally researched records into an append-only JSONL registry.
A stage can be sealed after a batch is reviewed. Progress snapshots are atomic;
idempotency checks are based on stable record IDs and full JSON content.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

STAGES = ("sources", "terms", "observations", "meanings", "relations")
ID = re.compile(r"^[a-z][a-z0-9_.-]*$")
EFFORT = {
    "sources": "Medium", "terms": "Instant", "observations": "Medium",
    "meanings": "High", "relations": "High", "publish": "High", "wave2": "Medium",
}


class PipelineError(ValueError):
    """The input must be reviewed or corrected, not silently published."""


def canonical(record):
    return json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def atomic_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)


def jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    result = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise PipelineError(f"{path}:{lineno}: bad JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise PipelineError(f"{path}:{lineno}: expected an object")
        result.append(value)
    return result


def required(record, *fields):
    for field in fields:
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise PipelineError(f"Missing/invalid {field} in {record.get('id', '<unknown>')}")


def require_id(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise PipelineError(f"Invalid stable ID: {value!r}")


class Workspace:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.config_path = self.root / "project.json"

    def init(self, config):
        if self.config_path.exists():
            raise PipelineError("Workspace already initialized; use a different directory")
        if not isinstance(config, dict) or config.get("schema_version") != 1:
            raise PipelineError("Project configuration must use schema_version: 1")
        for key in ("project", "term_kind", "content_kind", "adapter"):
            required(config, key)
        if config.get("external_reference_mode") is not True:
            raise PipelineError("Reconstruction requires external_reference_mode: true")
        atomic_json(self.config_path, config)
        (self.root / "records").mkdir(exist_ok=True)
        (self.root / "state").mkdir(exist_ok=True)
        self.checkpoint("initialized", {"project": config["project"]})

    def config(self):
        if not self.config_path.is_file():
            raise PipelineError("Workspace not initialized")
        return json.loads(self.config_path.read_text(encoding="utf-8"))

    def records(self, stage):
        if stage not in STAGES:
            raise PipelineError(f"Unknown stage: {stage}")
        values = jsonl(self.root / "records" / (stage + ".jsonl"))
        seen = {}
        for item in values:
            key = item.get("id")
            require_id(key)
            if key in seen:
                raise PipelineError(f"Duplicate record ID in {stage}: {key}")
            seen[key] = item
        return seen

    def state(self, stage):
        file = self.root / "state" / (stage + ".json")
        return json.loads(file.read_text(encoding="utf-8")) if file.exists() else {}

    def checkpoint(self, stage, details):
        atomic_json(self.root / "state" / "checkpoint.json", {
            "schema_version": 1, "latest_stage": stage,
            "details": details,
            "next_recommended_thinking": EFFORT.get(stage, "Medium"),
            "next_action": "Consult stage status and execute the next unsealed stage",
        })

    def validate(self, stage, row):
        if not isinstance(row, dict):
            raise PipelineError("All records must be JSON objects")
        required(row, "id")
        require_id(row["id"])
        if stage == "sources":
            required(row, "title", "url", "rights", "access")
            if not row["url"].startswith("https://"):
                raise PipelineError("Sources require an HTTPS URL")
            if row["rights"] not in ("permitted", "locator_only", "unknown", "disallowed"):
                raise PipelineError("Unknown source rights")
            if row["access"] not in ("free", "paid", "unknown"):
                raise PipelineError("Unknown access category")
            if row.get("authority_reviewed") not in (True, False):
                raise PipelineError("Sources require boolean authority_reviewed")
        elif stage == "terms":
            required(row, "label", "source_id", "locator")
            if row["source_id"] not in self.records("sources"):
                raise PipelineError("Unknown term source")
        elif stage == "observations":
            required(row, "term_id", "source_id", "locator", "record_kind")
            term = self.records("terms").get(row["term_id"])
            source = self.records("sources").get(row["source_id"])
            if not term or not source:
                raise PipelineError("Observation references unknown term/source")
            if row["record_kind"] not in ("locator", "paraphrase", "licensed_excerpt"):
                raise PipelineError("Bad observation record_kind")
            if row["record_kind"] != "locator":
                required(row, "text")
                if source["access"] != "free" or source["rights"] not in ("permitted", "locator_only"):
                    raise PipelineError("Do not acquire paid or unpermitted source contents")
            if row["record_kind"] == "licensed_excerpt" and source["rights"] != "permitted":
                raise PipelineError("Excerpts need affirmative reuse rights")
        elif stage == "meanings":
            required(row, "term_group_id", "display_term", "context")
            require_id(row["term_group_id"])
            if not isinstance(row.get("term_ids"), list) or not row["term_ids"]:
                raise PipelineError("Meaning requires term_ids")
            if any(t not in self.records("terms") for t in row["term_ids"]):
                raise PipelineError("Unknown meaning term_id")
            forms = row.get("formulations")
            if not isinstance(forms, list) or not forms:
                raise PipelineError("Meaning requires formulations")
            observations = self.records("observations")
            seen = set()
            for form in forms:
                required(form, "id", "text", "review_state")
                require_id(form["id"])
                if form["id"] in seen:
                    raise PipelineError("Duplicate formulation in meaning")
                seen.add(form["id"])
                if form["review_state"] not in ("candidate", "screened", "blocked"):
                    raise PipelineError("Invalid formulation review state")
                ids = form.get("evidence_ids")
                if not isinstance(ids, list) or not ids or any(i not in observations for i in ids):
                    raise PipelineError("Formulations require real observation evidence")
                if any(observations[i]["term_id"] not in row["term_ids"] for i in ids):
                    raise PipelineError("Evidence term must belong to the proposed meaning")
        elif stage == "relations":
            required(row, "from_formulation", "target_meaning", "relation_type", "review_state")
            meanings = self.records("meanings")
            forms = {f["id"] for m in meanings.values() for f in m["formulations"]}
            if row["from_formulation"] not in forms or row["target_meaning"] not in meanings:
                raise PipelineError("Unresolved relation endpoint")
            if row["review_state"] not in ("candidate", "screened", "blocked"):
                raise PipelineError("Invalid relation review state")

    def ingest(self, stage, input_path, batch_size=10, limit=None):
        self.config()
        if stage not in STAGES:
            raise PipelineError("Invalid stage")
        if self.state(stage).get("sealed"):
            raise PipelineError(f"Stage {stage} sealed; create next-wave workspace to revise")
        if batch_size < 1:
            raise PipelineError("batch_size must be positive")
        incoming = jsonl(input_path)
        target = self.root / "records" / (stage + ".jsonl")
        target.parent.mkdir(parents=True, exist_ok=True)
        existing = self.records(stage)
        added, skipped, processed = 0, 0, 0
        with target.open("a", encoding="utf-8") as out:
            for item in incoming:
                key = item.get("id")
                require_id(key)
                if key in existing:
                    if canonical(item) != canonical(existing[key]):
                        raise PipelineError(f"Record ID collision with changed content: {key}")
                    skipped += 1
                    continue
                self.validate(stage, item)
                out.write(canonical(item) + "\n")
                existing[key] = item
                added += 1
                processed += 1
                if processed % batch_size == 0:
                    out.flush()
                    os.fsync(out.fileno())
                    self._ingest_checkpoint(stage, target, added, skipped, input_path)
                if limit is not None and processed >= limit:
                    break
            out.flush()
            os.fsync(out.fileno())
        self._ingest_checkpoint(stage, target, added, skipped, input_path)
        return {"added": added, "already_present": skipped, "total": len(existing)}

    def _ingest_checkpoint(self, stage, target, added, skipped, input_path):
        state = self.state(stage)
        state.update({
            "sealed": False, "total": len(self.records(stage)),
            "last_input": str(input_path), "last_added": added,
            "last_skipped": skipped,
            "record_digest": digest(list(self.records(stage).values())),
        })
        atomic_json(self.root / "state" / (stage + ".json"), state)
        self.checkpoint(stage, state)

    def seal(self, stage):
        config = self.config()
        if stage not in STAGES:
            raise PipelineError("Invalid stage")
        # The repaired reconstruction explicitly opts into this fail-closed
        # coverage gate. Earlier immutable Stage 3/4 snapshots remain historical
        # artifacts and are NOT retroactively described as comprehensive.
        if stage in ("observations", "meanings", "relations") and config.get(
                "require_full_definition_attempts") is True:
            from .stage3_attempts import require_full_attempt_coverage
            attempt_file = self.root / "state" / "stage3_acquisition_attempts.jsonl"
            require_full_attempt_coverage(self.root, attempt_file)
        if stage in ("observations", "meanings", "relations") and config.get(
                "require_reviewed_term_dispositions") is True:
            from .stage3_review_gate import require_reviewed_term_dispositions
            require_reviewed_term_dispositions(
                self.root, self.root / "state" / "stage3_term_reviews.jsonl")
        index = STAGES.index(stage)
        if index and not self.state(STAGES[index - 1]).get("sealed"):
            raise PipelineError("Seal prior stages first, in order")
        values = self.records(stage)
        if not values:
            raise PipelineError(f"No {stage} records; nothing to seal")
        for record in values.values():
            self.validate(stage, record)
        info = {"sealed": True, "total": len(values), "record_digest": digest(list(values.values()))}
        atomic_json(self.root / "state" / (stage + ".json"), info)
        self.checkpoint(stage, info)
        return info

    def status(self):
        self.config()
        result = {}
        next_stage = None
        for stage in STAGES:
            data = self.state(stage)
            sealed = bool(data.get("sealed"))
            result[stage] = {"count": len(self.records(stage)), "sealed": sealed}
            if not sealed and next_stage is None:
                next_stage = stage
        if next_stage is None:
            published = (self.root / "state" / "publication.json").is_file()
            next_stage = "wave2" if published else "publish"
        result["handoff"] = {
            "next_stage": next_stage,
            "recommended_thinking": EFFORT.get(next_stage, "Medium"),
            "next_action": (
                "Generate the stage's research queue, review candidates, ingest batches and seal"
                if next_stage in STAGES else
                "Publish and inspect the separate experimental prototype"
                if next_stage == "publish" else
                "Inspect first-wave prototype, then generate and fork second-wave tasks"
            ),
            "checkpoint_file": str(self.root / "state" / "checkpoint.json"),
        }
        return result

    def publication(self):
        self.config()
        for stage in STAGES:
            state = self.state(stage)
            if not state.get("sealed") or state.get("record_digest") != digest(list(self.records(stage).values())):
                raise PipelineError(f"Stage {stage} not sealed against its current records")
        sources = self.records("sources")
        observations = self.records("observations")
        meanings = self.records("meanings")
        eligible, held = [], []
        all_formulation_ids = [f["id"] for m in meanings.values() for f in m["formulations"]]
        if len(all_formulation_ids) != len(set(all_formulation_ids)):
            raise PipelineError("Formulation IDs must be globally unique")
        for meaning in meanings.values():
            problem = []
            if meaning.get("_retired"):
                problem.append("meaning retired after editorial consolidation")
            for form in meaning["formulations"]:
                if form["review_state"] != "screened":
                    problem.append("formulation not screened")
                for evidence_id in form["evidence_ids"]:
                    obs = observations[evidence_id]
                    source = sources[obs["source_id"]]
                    if not source["authority_reviewed"] or source["rights"] in ("unknown", "disallowed"):
                        problem.append("unapproved/unsuitable source")
                    if source["access"] != "free" and obs["record_kind"] != "locator":
                        problem.append("paid source content")
            item = dict(meaning)
            item["verification_notice"] = "Not yet manually verified"
            item["human_verified"] = False
            (held if problem else eligible).append({**item, **({"hold_reasons": sorted(set(problem))} if problem else {})})
        eligible_meanings = {e["id"] for e in eligible}
        eligible_forms = {f["id"] for e in eligible for f in e["formulations"]}
        links = [r for r in self.records("relations").values()
                 if r["review_state"] == "screened"
                 and r["target_meaning"] in eligible_meanings
                 and r["from_formulation"] in eligible_forms]
        return {"schema_version": 1, "project": self.config()["project"],
                "meanings": eligible, "relations": links, "held": held,
                "sources": list(sources.values()), "terms": list(self.records("terms").values()),
                "observations": list(observations.values())}

    def publish(self):
        artifact = self.publication()
        path = self.root / "published" / "catalog.json"
        atomic_json(path, artifact)
        info = {"published_meanings": len(artifact["meanings"]), "held_meanings": len(artifact["held"]),
                "published_relations": len(artifact["relations"]), "sha256": digest(artifact)}
        atomic_json(self.root / "state" / "publication.json", info)
        self.checkpoint("publish", info)
        return info

    def wave2_plan(self):
        """Produce discovery tasks only; never call search engines automatically."""
        self.config()
        if not (self.root / "state" / "publication.json").exists():
            raise PipelineError("Complete first-wave publication before planning wave 2")
        sources = [s for s in self.records("sources").values() if s["authority_reviewed"]]
        terms = list(self.records("terms").values())
        meanings = list(self.records("meanings").values())
        tasks = []
        for t in terms:
            tasks.append({"id": "sources." + t["id"], "kind": "discover_sources_from_term",
                          "label": t["label"], "reason": "Search for additional authoritative collections"})
            for s in sources:
                tasks.append({"id": "variants." + t["id"] + "." + s["id"],
                              "kind": "search_variants_in_source", "term_id": t["id"],
                              "label": t["label"], "source_id": s["id"],
                              "reason": "Find synonyms, additional meanings and formulations"})
        for m in meanings:
            tasks.append({"id": "links." + m["id"], "kind": "audit_relationships",
                          "meaning_id": m["id"], "context": m["context"]})
        output = self.root / "wave2" / "tasks.jsonl"
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as f:
            for task in tasks:
                f.write(canonical(task) + "\n")
        info = {"tasks": len(tasks), "path": str(output), "next_recommended_thinking": "Medium"}
        self.checkpoint("wave2", info)
        return info

    def fork_second_wave(self, new_root):
        """Copy only isolated wave-one data to a versioned, editable wave-two workspace.

        The first-wave workspace stays sealed, allowing independent comparisons.
        Existing IDs remain immutable until an explicit revision mechanism exists.
        """
        import shutil

        self.publication()  # proves all five stages are sealed and unchanged
        dest = Workspace(new_root)
        if dest.root == self.root or dest.root.exists():
            raise PipelineError("Second-wave destination must be a new, absent directory")
        dest.init(self.config())
        for stage in STAGES:
            source_file = self.root / "records" / (stage + ".jsonl")
            target = dest.root / "records" / (stage + ".jsonl")
            shutil.copy2(source_file, target)
        frozen = {
            "origin": str(self.root),
            "first_wave_digest": digest(self.publication()),
            "mode": "second_wave",
            "note": "The original workspace remains untouched. Existing IDs cannot be revised silently."
        }
        atomic_json(dest.root / "state" / "baseline.json", frozen)
        dest.checkpoint("initialized", {"mode": "second_wave", "inherited": {
            stage: len(dest.records(stage)) for stage in STAGES
        }})
        return frozen
