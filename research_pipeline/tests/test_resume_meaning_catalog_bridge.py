"""Fail-closed synthetic regression coverage for approved Wave2 meaning-text bridge.

No production definitions or frozen Wave1 records are loaded in these tests.
"""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.adapters.mathdef.resume_validation import (
    _validate_meaning_catalog_review_bridge,
)
from research_pipeline.engine.core import digest
from research_pipeline.engine.resume_checkpoint import ResumeError


class ApprovedSourceTextRevisionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "events").mkdir()
        self.before = (
            "Equivalently, X is compact if every family of closed subsets of X "
            "that has the finite intersection property has nonempty total intersection."
        )
        self.after = (
            "Equivalently, X is compact if every nonempty family of closed subsets "
            "of X that has the finite intersection property has nonempty total intersection."
        )
        self.mid = "meaning.wave2.broad67.compact-topological-space"
        self.fid = "form.wave2.broad67.compact-closed-fip"
        self.old = {
            "meaning.synthetic.unchanged": {
                "id": "meaning.synthetic.unchanged",
                "context": "Synthetic placeholder",
                "formulations": [{"id": "form.synthetic.unchanged", "text": "Unchanged text"}],
            },
            self.mid: {
                "id": self.mid,
                "context": "General topology",
                "formulations": [
                    {"id": "form.synthetic.open-cover", "text": "Open cover criterion"},
                    {"id": self.fid, "text": self.before},
                ],
            },
        }
        self.live = copy.deepcopy(self.old)
        self.live[self.mid]["formulations"][1]["text"] = self.after
        self.old_digest = digest(list(self.old.values()))
        self.reviews = [
            {"meaning_catalog_digest": self.old_digest, "formulation_id": "form.synthetic.unchanged"},
            {"meaning_catalog_digest": self.old_digest, "formulation_id": "form.synthetic.open-cover"},
            {"meaning_catalog_digest": self.old_digest, "formulation_id": self.fid},
        ]
        self.event = {
            "schema_version": 1,
            "event_id": "wave2.fip-compactness-nonempty-family.2026-10-24",
            "stage": "meanings",
            "meaning_id": self.mid,
            "formulation_id": self.fid,
            "prior_reviewed_meaning_catalog_digest": self.old_digest,
            "before_text": self.before,
            "after_text": self.after,
            "authorization": "User explicitly approved the scoped mathematical revision.",
            "reviewed_by": "Mathematical reviewer",
            "reason": "Text-only change to qualify nonempty families; previous catalog is exactly reconstructed.",
        }
        self.events_path = self.root / "events" / "meaning_text_revision_attestations.jsonl"
        self.write_event()

    def write_event(self):
        self.events_path.write_text(json.dumps(self.event) + "\n", encoding="utf-8")

    def validate(self):
        return _validate_meaning_catalog_review_bridge(self.live, self.reviews, self.root)

    def test_approved_text_only_change_reconciles_without_editing_reviews(self):
        original_review_rows = copy.deepcopy(self.reviews)
        evidence = self.validate()
        self.assertEqual(evidence["authorized_text_revisions"], 1)
        self.assertEqual(evidence["revised_formulation"], self.fid)
        self.assertEqual(self.reviews, original_review_rows)

    def test_missing_attestation_fails_closed(self):
        self.events_path.unlink()
        with self.assertRaises(ResumeError):
            self.validate()

    def test_other_meaning_change_is_not_approved(self):
        self.live["meaning.synthetic.unchanged"]["context"] = "Unrelated tampering"
        with self.assertRaises(ResumeError):
            self.validate()

    def test_other_formulation_on_same_meaning_is_not_approved(self):
        self.live[self.mid]["formulations"][0]["text"] = "Unsupported edit"
        with self.assertRaises(ResumeError):
            self.validate()

    def test_source_text_must_match_approved_version(self):
        self.live[self.mid]["formulations"][1]["text"] += " Unauthorized sentence."
        with self.assertRaises(ResumeError):
            self.validate()

    def test_prior_digest_must_match_historical_reviews(self):
        self.event["prior_reviewed_meaning_catalog_digest"] = "0" * 64
        self.write_event()
        with self.assertRaises(ResumeError):
            self.validate()

    def test_multiple_attestations_do_not_silently_extend_scope(self):
        with self.events_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(self.event) + "\n")
        with self.assertRaises(ResumeError):
            self.validate()

    def test_unchanged_catalog_without_event_is_still_valid(self):
        self.events_path.unlink()
        self.live = copy.deepcopy(self.old)
        evidence = self.validate()
        self.assertEqual(evidence["authorized_text_revisions"], 0)


if __name__ == "__main__":
    unittest.main()
