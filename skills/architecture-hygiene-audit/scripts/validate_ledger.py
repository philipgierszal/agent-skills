#!/usr/bin/env python3
"""Validate an architecture-hygiene ledger against its repository inventory."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence


REVIEW_STATUSES = {"content-reviewed", "tool-reviewed", "metadata-only", "excluded"}
REACHABILITY = {"root", "reachable", "unreachable", "candidate", "unknown", "not-applicable"}
FINDING_CLASSES = {
    "confirmed-unreachable",
    "high-confidence-unused",
    "probable-unused",
    "orphan-path",
    "architecture-violation",
    "design-smell",
    "unknown-or-exempt",
}
HIGH_CERTAINTY = {
    "confirmed-unreachable",
    "high-confidence-unused",
    "architecture-violation",
}
RELATION_TARGET_TYPES = {"file", "symbol", "external", "pattern"}
RELATION_CONFIDENCE = {"direct", "declared", "inferred", "observed"}


class LedgerValidationError(ValueError):
    """Raised with every discovered ledger-contract violation."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("\n".join(errors))


def _nonempty_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def _string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _paths(document: dict[str, object], label: str, errors: list[str]) -> list[str]:
    records = document.get("files")
    if not isinstance(records, list):
        errors.append(f"{label}.files must be a list")
        return []

    paths: list[str] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"{label}.files[{index}] must be an object")
            continue
        path = record.get("path")
        if not isinstance(path, str) or not path:
            errors.append(f"{label}.files[{index}] requires a non-empty path")
            continue
        paths.append(path)
    return paths


def _validate_finding(
    finding: object,
    path: str,
    index: int,
    unresolved: list[str],
    relation_ids: set[str],
    analyzed_variants: set[str],
    unresolved_channels: list[dict[str, object]],
    errors: list[str],
) -> None:
    prefix = f"{path} finding[{index}]"
    if not isinstance(finding, dict):
        errors.append(f"{prefix} must be an object")
        return

    finding_class = finding.get("class")
    if finding_class not in FINDING_CLASSES:
        errors.append(f"{prefix} has invalid finding class: {finding_class!r}")

    for key in ("subject", "location", "summary", "confidence_rationale", "action"):
        value = finding.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{prefix} finding requires {key}")

    if not _nonempty_strings(finding.get("evidence")):
        errors.append(f"{prefix} finding requires evidence")

    scopes_value = finding.get("scopes")
    if not _nonempty_strings(scopes_value):
        errors.append(f"{prefix} finding requires scopes")
        scopes: list[str] = []
    else:
        scopes = scopes_value

    variants_value = finding.get("variants")
    if not _nonempty_strings(variants_value):
        errors.append(f"{prefix} finding requires variants")
        variants: list[str] = []
    else:
        variants = variants_value

    counter_evidence = finding.get("counter_evidence_checked")
    if not _string_list(counter_evidence):
        errors.append(f"{prefix} counter_evidence_checked must be a list of strings")
        counter_evidence = []

    if finding_class in HIGH_CERTAINTY:
        if unresolved:
            errors.append(
                f"{path} {finding_class} cannot retain unresolved dynamic references"
            )
        if not counter_evidence:
            errors.append(f"{path} {finding_class} requires counter_evidence_checked")
        for variant in sorted(set(variants) - analyzed_variants):
            errors.append(f"{path} {finding_class} uses unanalyzed variant: {variant}")
        for gap in unresolved_channels:
            gap_scopes = set(gap["scopes"])
            gap_variants = set(gap["variants"])
            scopes_overlap = "all" in gap_scopes or bool(gap_scopes.intersection(scopes))
            variants_overlap = "all" in gap_variants or bool(gap_variants.intersection(variants))
            if scopes_overlap and variants_overlap:
                errors.append(
                    f"{path} {finding_class} overlaps unresolved channel: {gap['channel']}"
                )

    if finding_class == "architecture-violation":
        rule = finding.get("policy_rule")
        if not isinstance(rule, str) or not rule.strip():
            errors.append(f"{prefix} architecture-violation requires policy_rule")
        relation_refs = finding.get("relation_refs")
        if not _nonempty_strings(relation_refs):
            errors.append(f"{prefix} architecture-violation requires relation_refs")
        else:
            for relation_ref in relation_refs:
                if relation_ref not in relation_ids:
                    errors.append(f"{prefix} references unknown relation id: {relation_ref}")


def _validate_relation(
    relation: object,
    path: str,
    index: int,
    inventory_paths: set[str],
    relation_ids: set[str],
    errors: list[str],
) -> None:
    prefix = f"{path} relation[{index}]"
    if not isinstance(relation, dict):
        errors.append(f"{prefix} must be an object")
        return

    relation_id = relation.get("id")
    if not isinstance(relation_id, str) or not relation_id.strip():
        errors.append(f"{prefix} requires id")
    elif relation_id in relation_ids:
        errors.append(f"{prefix} duplicates relation id: {relation_id}")
    else:
        relation_ids.add(relation_id)

    kind = relation.get("kind")
    if not isinstance(kind, str) or not kind.strip():
        errors.append(f"{prefix} requires kind")

    target = relation.get("target")
    if not isinstance(target, str) or not target.strip():
        errors.append(f"{prefix} requires target")

    target_type = relation.get("target_type")
    if target_type not in RELATION_TARGET_TYPES:
        errors.append(f"{prefix} has invalid target_type: {target_type!r}")
    elif target_type == "file" and isinstance(target, str) and target not in inventory_paths:
        errors.append(f"{prefix} references missing inventory path: {target}")

    if not _nonempty_strings(relation.get("evidence")):
        errors.append(f"{prefix} requires evidence")

    confidence = relation.get("confidence")
    if confidence not in RELATION_CONFIDENCE:
        errors.append(f"{prefix} has invalid confidence: {confidence!r}")

    if not _nonempty_strings(relation.get("scopes")):
        errors.append(f"{prefix} requires scopes")


def _validate_file(
    record: object,
    index: int,
    inventory_paths: set[str],
    analyzed_variants: set[str],
    unresolved_channels: list[dict[str, object]],
    errors: list[str],
) -> None:
    if not isinstance(record, dict):
        return

    path = record.get("path")
    if not isinstance(path, str) or not path:
        return

    review_status = record.get("review_status")
    if review_status not in REVIEW_STATUSES:
        errors.append(f"{path} has invalid review_status: {review_status!r}")

    reachability = record.get("reachability")
    if reachability not in REACHABILITY:
        errors.append(f"{path} has invalid reachability: {reachability!r}")

    role = record.get("role")
    if not isinstance(role, str) or not role.strip():
        errors.append(f"{path} requires role")

    if not _nonempty_strings(record.get("evidence")):
        errors.append(f"{path} requires evidence")

    relations = record.get("relations")
    relation_ids: set[str] = set()
    if not isinstance(relations, list):
        errors.append(f"{path} relations must be a list")
    else:
        for relation_index, relation in enumerate(relations):
            _validate_relation(
                relation,
                path,
                relation_index,
                inventory_paths,
                relation_ids,
                errors,
            )

    if review_status in {"metadata-only", "excluded"}:
        rationale = record.get("review_rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            errors.append(f"{path} {review_status} requires review_rationale")

    unresolved_value = record.get("unresolved_dynamic_references")
    if not _string_list(unresolved_value):
        errors.append(f"{path} unresolved_dynamic_references must be a list of strings")
        unresolved: list[str] = []
    else:
        unresolved = unresolved_value

    findings = record.get("findings")
    if not isinstance(findings, list):
        errors.append(f"{path} findings must be a list")
        return
    for finding_index, finding in enumerate(findings):
        _validate_finding(
            finding,
            path,
            finding_index,
            unresolved,
            relation_ids,
            analyzed_variants,
            unresolved_channels,
            errors,
        )


def _validate_unresolved_channels(
    value: object,
    errors: list[str],
) -> list[dict[str, object]]:
    if not isinstance(value, list):
        errors.append("unresolved_channels must be a list")
        return []

    valid_channels: list[dict[str, object]] = []
    for index, channel in enumerate(value):
        prefix = f"unresolved_channels[{index}]"
        if not isinstance(channel, dict):
            errors.append(f"{prefix} must be an object")
            continue
        name = channel.get("channel")
        scopes = channel.get("scopes")
        variants = channel.get("variants")
        valid = True
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{prefix} requires channel")
            valid = False
        if not _nonempty_strings(scopes):
            errors.append(f"{prefix} requires scopes")
            valid = False
        if not _nonempty_strings(variants):
            errors.append(f"{prefix} requires variants")
            valid = False
        if valid:
            valid_channels.append(channel)
    return valid_channels


def validate(inventory: dict[str, object], ledger: dict[str, object]) -> None:
    """Raise LedgerValidationError with all discovered contract violations."""

    errors: list[str] = []
    if inventory.get("inventory_version") != 1:
        errors.append("inventory_version must be 1")
    if ledger.get("ledger_version") != 1:
        errors.append("ledger_version must be 1")

    inventory_revision = inventory.get("revision")
    ledger_revision = ledger.get("inventory_revision")
    if inventory_revision != ledger_revision:
        errors.append(
            f"inventory revision mismatch: inventory={inventory_revision!r}, ledger={ledger_revision!r}"
        )

    inventory_digest = inventory.get("inventory_digest")
    ledger_digest = ledger.get("inventory_digest")
    if not isinstance(inventory_digest, str) or not inventory_digest:
        errors.append("inventory requires inventory_digest")
    if inventory_digest != ledger_digest:
        errors.append(
            f"inventory digest mismatch: inventory={inventory_digest!r}, ledger={ledger_digest!r}"
        )

    variants = ledger.get("variants_analyzed")
    if not _nonempty_strings(variants):
        errors.append("variants_analyzed must contain at least one named variant")
        analyzed_variants: set[str] = set()
    else:
        analyzed_variants = set(variants)
    unresolved_channels = _validate_unresolved_channels(
        ledger.get("unresolved_channels"),
        errors,
    )

    inventory_paths = _paths(inventory, "inventory", errors)
    ledger_paths = _paths(ledger, "ledger", errors)

    for path, count in Counter(inventory_paths).items():
        if count > 1:
            errors.append(f"duplicate inventory path: {path}")
    for path, count in Counter(ledger_paths).items():
        if count > 1:
            errors.append(f"duplicate path: {path}")

    inventory_set = set(inventory_paths)
    ledger_set = set(ledger_paths)
    for path in sorted(inventory_set - ledger_set):
        errors.append(f"missing inventory path: {path}")
    for path in sorted(ledger_set - inventory_set):
        errors.append(f"unexpected ledger path: {path}")

    records = ledger.get("files")
    if isinstance(records, list):
        for index, record in enumerate(records):
            _validate_file(
                record,
                index,
                inventory_set,
                analyzed_variants,
                unresolved_channels,
                errors,
            )

    if errors:
        raise LedgerValidationError(errors)


def _read_json(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LedgerValidationError([f"Cannot read {path}: {error}"]) from error
    if not isinstance(value, dict):
        raise LedgerValidationError([f"{path} must contain a JSON object"])
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        inventory = _read_json(args.inventory)
        ledger = _read_json(args.ledger)
        validate(inventory, ledger)
    except LedgerValidationError as error:
        for message in error.errors:
            print(f"ledger error: {message}", file=sys.stderr)
        return 2

    count = len(inventory["files"])
    print(f"Ledger valid: {count}/{count} paths reconciled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
