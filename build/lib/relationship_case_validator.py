#!/usr/bin/env python3
"""Validate relationship-evidence case JSON using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SOURCE_TYPES = {"synthetic", "user-submitted-anonymized", "public-with-permission"}
EVENT_SOURCE_TYPES = {"chat", "screenshot", "self-report", "behavior-record", "third-party"}
RISK_FLAGS = {
    "violence",
    "sexual-coercion",
    "stalking",
    "threats",
    "coercive-control",
    "self-harm",
    "harm-to-others",
}
CASE_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
PRIVACY_PATTERNS = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone-like number": re.compile(r"(?<!\d)(?:\+?\d[\d ()-]{7,}\d)(?!\d)"),
    "social handle": re.compile(r"(?<!\w)@[A-Za-z0-9_]{2,}"),
    "web address": re.compile(r"https?://\S+", re.I),
}


def _is_object(value: Any) -> bool:
    return isinstance(value, dict)


def _is_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_case(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not _is_object(data):
        return ["root: expected a JSON object"], warnings

    required = {
        "schema_version",
        "case_id",
        "title",
        "source",
        "consent",
        "relationship",
        "events",
        "questions",
        "risk_flags",
    }
    for field in sorted(required - data.keys()):
        errors.append(f"{field}: required field is missing")

    if data.get("schema_version") != "1.0":
        errors.append("schema_version: expected '1.0'")

    case_id = data.get("case_id")
    if not _is_string(case_id) or not CASE_ID_RE.fullmatch(case_id):
        errors.append("case_id: use letters, digits, dots, underscores, or hyphens only")

    if not _is_string(data.get("title")):
        errors.append("title: expected a non-empty string")

    source = data.get("source")
    if not _is_object(source):
        errors.append("source: expected an object")
        source = {}
    if source.get("type") not in SOURCE_TYPES:
        errors.append(f"source.type: expected one of {sorted(SOURCE_TYPES)}")
    if source.get("deidentified") is not True:
        errors.append("source.deidentified: must be true before a case is shared or published")

    consent = data.get("consent")
    if not _is_object(consent):
        errors.append("consent: expected an object")
        consent = {}
    if consent.get("allow_analysis") is not True:
        errors.append("consent.allow_analysis: explicit true is required")
    if consent.get("allow_publication") is not True:
        warnings.append("consent.allow_publication: case must not be committed to a public repository")

    relationship = data.get("relationship")
    if not _is_object(relationship):
        errors.append("relationship: expected an object")
        relationship = {}
    if not _is_string(relationship.get("stage")):
        errors.append("relationship.stage: expected a non-empty string")
    agreements = relationship.get("agreements")
    if not isinstance(agreements, list) or any(not _is_string(item) for item in agreements):
        errors.append("relationship.agreements: expected an array of non-empty strings")

    participants = relationship.get("participants")
    participant_ids: list[str] = []
    if not isinstance(participants, list) or len(participants) < 2:
        errors.append("relationship.participants: expected at least two participant objects")
    else:
        for index, participant in enumerate(participants):
            path = f"relationship.participants[{index}]"
            if not _is_object(participant):
                errors.append(f"{path}: expected an object")
                continue
            participant_id = participant.get("id")
            if not _is_string(participant_id):
                errors.append(f"{path}.id: expected a non-empty alias")
            else:
                participant_ids.append(participant_id)
            if not _is_string(participant.get("role")):
                errors.append(f"{path}.role: expected a non-empty string")
    if len(participant_ids) != len(set(participant_ids)):
        errors.append("relationship.participants: participant ids must be unique")

    events = data.get("events")
    event_ids: list[str] = []
    if not isinstance(events, list) or not events:
        errors.append("events: expected at least one event object")
    else:
        for index, event in enumerate(events):
            path = f"events[{index}]"
            if not _is_object(event):
                errors.append(f"{path}: expected an object")
                continue
            event_id = event.get("id")
            if not _is_string(event_id):
                errors.append(f"{path}.id: expected a non-empty string")
            else:
                event_ids.append(event_id)
            if event.get("source_type") not in EVENT_SOURCE_TYPES:
                errors.append(f"{path}.source_type: expected one of {sorted(EVENT_SOURCE_TYPES)}")
            if not _is_string(event.get("reporter")):
                errors.append(f"{path}.reporter: expected a source alias")
            if not _is_string(event.get("summary")):
                errors.append(f"{path}.summary: expected a non-empty string")
            actions = event.get("observable_actions")
            if not isinstance(actions, list) or not actions:
                errors.append(f"{path}.observable_actions: expected at least one action")
            else:
                for action_index, action in enumerate(actions):
                    action_path = f"{path}.observable_actions[{action_index}]"
                    if not _is_object(action):
                        errors.append(f"{action_path}: expected an object")
                        continue
                    if not _is_string(action.get("actor")):
                        errors.append(f"{action_path}.actor: expected a non-empty alias")
                    if not _is_string(action.get("action")):
                        errors.append(f"{action_path}.action: expected a non-empty string")
    if len(event_ids) != len(set(event_ids)):
        errors.append("events: event ids must be unique")

    questions = data.get("questions")
    if not isinstance(questions, list) or not questions or any(not _is_string(item) for item in questions):
        errors.append("questions: expected at least one non-empty string")

    risk_flags = data.get("risk_flags")
    if not isinstance(risk_flags, list):
        errors.append("risk_flags: expected an array")
        risk_flags = []
    else:
        unknown_flags = sorted(set(risk_flags) - RISK_FLAGS)
        if unknown_flags:
            errors.append(f"risk_flags: unknown values {unknown_flags}")
    if risk_flags and not _is_object(data.get("safety_context")):
        errors.append("safety_context: required when risk_flags is not empty")

    serialized = json.dumps(data, ensure_ascii=False)
    for label, pattern in PRIVACY_PATTERNS.items():
        if pattern.search(serialized):
            warnings.append(f"privacy scan: possible {label}; review and remove identifying data")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_file", type=Path)
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = parser.parse_args()

    try:
        data = json.loads(args.case_file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors, warnings = [f"file not found: {args.case_file}"], []
    except json.JSONDecodeError as exc:
        errors, warnings = [f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"], []
    else:
        errors, warnings = validate_case(data)

    passed = not errors and not (args.strict and warnings)
    result = {"valid": passed, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("VALID" if passed else "INVALID")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARNING: {item}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

