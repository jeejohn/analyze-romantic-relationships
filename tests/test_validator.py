from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from relationship_case_validator import validate_case


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "examples" / "cases"


class ValidatorTests(unittest.TestCase):
    def load(self, name: str):
        return json.loads((CASES / name).read_text(encoding="utf-8"))

    def test_public_synthetic_cases_are_strictly_valid(self):
        for name in ("synthetic-conflict-valid.json", "synthetic-safety-valid.json"):
            with self.subTest(name=name):
                errors, warnings = validate_case(self.load(name))
                self.assertEqual(errors, [])
                self.assertEqual(warnings, [])

    def test_private_case_produces_publication_and_privacy_warnings(self):
        errors, warnings = validate_case(self.load("invalid-private.json"))
        self.assertEqual(errors, [])
        self.assertTrue(any("allow_publication" in item for item in warnings))
        self.assertTrue(any("email address" in item for item in warnings))

    def test_risk_flag_requires_safety_context(self):
        case = self.load("synthetic-safety-valid.json")
        case.pop("safety_context")
        errors, _ = validate_case(case)
        self.assertTrue(any("safety_context" in item for item in errors))

    def test_duplicate_event_ids_fail(self):
        case = self.load("synthetic-conflict-valid.json")
        case["events"][1]["id"] = case["events"][0]["id"]
        errors, _ = validate_case(case)
        self.assertTrue(any("event ids must be unique" in item for item in errors))

    def test_strict_cli_rejects_warnings(self):
        command = [
            sys.executable,
            str(ROOT / "relationship_case_validator.py"),
            "--strict",
            str(CASES / "invalid-private.json"),
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("INVALID", result.stdout)


if __name__ == "__main__":
    unittest.main()
