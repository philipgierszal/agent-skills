from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "skills"
    / "architecture-hygiene-audit"
    / "scripts"
    / "validate_ledger.py"
)


def load_validator_module():
    spec = importlib.util.spec_from_file_location("architecture_hygiene_ledger", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load ledger validator at {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_inventory() -> dict[str, object]:
    return {
        "inventory_version": 1,
        "revision": "abc123",
        "files": [
            {"path": "README.md"},
            {"path": "src/main.py"},
        ],
    }


def valid_ledger() -> dict[str, object]:
    return {
        "ledger_version": 1,
        "inventory_revision": "abc123",
        "variants_analyzed": ["default"],
        "unresolved_channels": [],
        "files": [
            {
                "path": "README.md",
                "review_status": "metadata-only",
                "review_rationale": "Documentation contract and installation entrypoint",
                "role": "repository documentation",
                "reachability": "not-applicable",
                "evidence": ["manual:README headings and links"],
                "unresolved_dynamic_references": [],
                "findings": [],
            },
            {
                "path": "src/main.py",
                "review_status": "content-reviewed",
                "role": "production entrypoint",
                "reachability": "root",
                "evidence": ["pyproject.toml:project.scripts"],
                "unresolved_dynamic_references": [],
                "findings": [],
            },
        ],
    }


class LedgerValidationTests(unittest.TestCase):
    def test_accepts_a_reconciled_ledger(self) -> None:
        validator = load_validator_module()
        self.assertIsNone(validator.validate(valid_inventory(), valid_ledger()))

    def test_rejects_missing_duplicate_and_unexpected_paths(self) -> None:
        validator = load_validator_module()
        ledger = valid_ledger()
        ledger["files"] = [
            copy.deepcopy(ledger["files"][0]),
            copy.deepcopy(ledger["files"][0]),
            {
                **copy.deepcopy(ledger["files"][1]),
                "path": "src/unexpected.py",
            },
        ]

        with self.assertRaises(validator.LedgerValidationError) as raised:
            validator.validate(valid_inventory(), ledger)

        message = str(raised.exception)
        self.assertIn("duplicate path: README.md", message)
        self.assertIn("missing inventory path: src/main.py", message)
        self.assertIn("unexpected ledger path: src/unexpected.py", message)

    def test_rejects_invalid_status_reachability_and_empty_evidence(self) -> None:
        validator = load_validator_module()
        ledger = valid_ledger()
        record = ledger["files"][1]
        record["review_status"] = "skimmed"
        record["reachability"] = "probably-live"
        record["evidence"] = []

        with self.assertRaises(validator.LedgerValidationError) as raised:
            validator.validate(valid_inventory(), ledger)

        message = str(raised.exception)
        self.assertIn("invalid review_status", message)
        self.assertIn("invalid reachability", message)
        self.assertIn("requires evidence", message)

    def test_metadata_only_and_excluded_records_require_rationale(self) -> None:
        validator = load_validator_module()
        ledger = valid_ledger()
        del ledger["files"][0]["review_rationale"]

        with self.assertRaisesRegex(
            validator.LedgerValidationError,
            "metadata-only requires review_rationale",
        ):
            validator.validate(valid_inventory(), ledger)

    def test_high_certainty_finding_requires_closed_dynamic_channels(self) -> None:
        validator = load_validator_module()
        ledger = valid_ledger()
        record = ledger["files"][1]
        record["reachability"] = "unreachable"
        record["unresolved_dynamic_references"] = ["plugin registry not inspected"]
        record["findings"] = [
            {
                "class": "confirmed-unreachable",
                "summary": "Entrypoint appears unused",
                "evidence": ["vulture:src/main.py:1"],
                "counter_evidence_checked": [],
                "confidence_rationale": "No static callers",
                "action": "Review plugin registry before proposing removal",
            }
        ]

        with self.assertRaises(validator.LedgerValidationError) as raised:
            validator.validate(valid_inventory(), ledger)

        message = str(raised.exception)
        self.assertIn("confirmed-unreachable cannot retain unresolved dynamic references", message)
        self.assertIn("confirmed-unreachable requires counter_evidence_checked", message)

    def test_rejects_unknown_finding_class_and_incomplete_finding(self) -> None:
        validator = load_validator_module()
        ledger = valid_ledger()
        ledger["files"][1]["findings"] = [
            {
                "class": "definitely-dead",
                "summary": "No callers",
                "evidence": [],
                "counter_evidence_checked": [],
                "confidence_rationale": "",
                "action": "",
            }
        ]

        with self.assertRaises(validator.LedgerValidationError) as raised:
            validator.validate(valid_inventory(), ledger)

        message = str(raised.exception)
        self.assertIn("invalid finding class", message)
        self.assertIn("finding requires evidence", message)
        self.assertIn("finding requires confidence_rationale", message)
        self.assertIn("finding requires action", message)


if __name__ == "__main__":
    unittest.main()
