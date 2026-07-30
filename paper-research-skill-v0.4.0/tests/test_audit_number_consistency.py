from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "paper-research-cn-core" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from audit_number_consistency import audit_payload


class NumberConsistencyTests(unittest.TestCase):
    def test_reports_unclosed_flow_as_critical(self) -> None:
        findings = audit_payload(
            {
                "flow": {
                    "identified": 118,
                    "excluded": {"duplicates": 1, "restricted_standard": 2},
                    "outputs": {"main": 100, "supplement": 7, "english": 9},
                }
            }
        )

        self.assertEqual(findings[0]["rule_id"], "NUM-FLOW-001")
        self.assertEqual(findings[0]["severity"], "critical")

    def test_accepts_closed_flow_and_declared_multi_coding(self) -> None:
        findings = audit_payload(
            {
                "flow": {
                    "identified": 118,
                    "excluded": {"duplicates": 1},
                    "outputs": {"main": 100, "supplement": 7, "english": 9, "restricted_standard": 1},
                },
                "dimensions": [
                    {"name": "治理环节", "total": 345, "denominator": 100, "multiple": True}
                ],
            }
        )

        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
