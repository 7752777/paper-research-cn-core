from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for relative in (
    "skills/paper-review-cn-core/scripts",
    "skills/paper-submission-cn-core/scripts",
):
    sys.path.insert(0, str(ROOT / relative))


FINDING_FIELDS = {"rule_id", "severity", "file", "evidence", "remediation"}


class ReleaseGateTests(unittest.TestCase):
    def test_public_package_contains_no_private_project_marker(self) -> None:
        private_marker = "\u5317\u6597"
        for path in ROOT.rglob("*"):
            if path.suffix.lower() not in {".md", ".py", ".json", ".yaml", ".yml", ".txt"}:
                continue
            self.assertNotIn(private_marker, path.read_text(encoding="utf-8"), path.relative_to(ROOT).as_posix())

    def test_submission_gate_rejects_missing_artifacts_and_reports(self) -> None:
        import audit_submission_package as submission

        findings = submission.audit(
            {
                "artifacts": {name: "placeholder" for name in submission.required_artifacts()},
                "audit_reports": {},
            },
            Path("."),
        )
        self.assertTrue(any(item["rule_id"] == "SUB-PACK-ARTIFACT-001" for item in findings))
        self.assertTrue(any(item["rule_id"] == "SUB-PACK-AUDIT-001" for item in findings))

    def test_submission_gate_reads_reports_and_blocks_major(self) -> None:
        import audit_submission_package as submission

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact_paths: dict[str, str] = {}
            for name in submission.required_artifacts():
                path = root / f"{name}.json"
                path.write_text(json.dumps({"blocks": []}), encoding="utf-8")
                artifact_paths[name] = path.name

            report_paths: dict[str, str] = {}
            for name in submission.required_audits():
                path = root / f"{name}.json"
                payload: object = []
                if name == "review":
                    payload = [{
                        "rule_id": "REVIEW-UNRESOLVED-MAJOR",
                        "severity": "major",
                        "file": "review.md",
                        "evidence": "unresolved evidence gap",
                        "remediation": "verify the source metadata",
                    }]
                path.write_text(json.dumps(payload), encoding="utf-8")
                report_paths[name] = path.name

            findings = submission.audit({"artifacts": artifact_paths, "audit_reports": report_paths}, root)
        self.assertTrue(any(item["rule_id"] == "SUB-PACK-002" for item in findings))

    def test_review_audit_requires_real_per_round_evidence(self) -> None:
        from audit_review_output import audit_review

        shell = """
# 中文独立审稿记录
## 第一轮：问题与贡献
- 轮次计数：Critical 0；Major 0；Minor 0。
- 严重度：Minor
- 位置：摘要。
- 证据：论证已核验。
- 建议：保持现有表达。
- 验证：逐项复核。
- 引文抽样：1/1。
- 参考文献抽样：1/1。
- 图表抽样：1/1。
- 逐项排除：问题、证据、方法、统计、主张、图表、参考文献和文风均已复核。
- 限制回写位置：正文方法部分。
## 第二轮：方法与证据
- 轮次计数：Critical 0；Major 0；Minor 0。
- 严重度：Minor
- 位置：方法。
- 证据：编码规则已核验。
- 建议：保持披露。
- 验证：逐项复核。
- 引文抽样：1/1。
- 参考文献抽样：1/1。
- 图表抽样：1/1。
- 逐项排除：问题、证据、方法、统计、主张、图表、参考文献和文风均已复核。
- 限制回写位置：正文方法部分。
## 第三轮：表达与图表
- 轮次计数：Critical 0；Major 0；Minor 0。
- 严重度：Minor
- 位置：结论。
- 证据：版式已核验。
- 建议：保持清晰。
- 验证：逐项复核。
- 引文抽样：1/1。
- 参考文献抽样：1/1。
- 图表抽样：1/1。
- 逐项排除：问题、证据、方法、统计、主张、图表、参考文献和文风均已复核。
- 限制回写位置：正文结论部分。
"""
        self.assertEqual(audit_review(shell), [])
        hollow = shell.replace("- 引文抽样：1/1。\n", "", 1)
        self.assertTrue(any(item["rule_id"] == "REVIEW-SAMPLE-001" for item in audit_review(hollow)))

    def test_legacy_audits_emit_structured_findings(self) -> None:
        scripts = {
            "check_literature_ledger.py": ["ledger.csv"],
            "audit_manuscript.py": ["manuscript.md"],
            "deep_structure_audit.py": ["project"],
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "ledger.csv").write_text("id,title\n1,example\n", encoding="utf-8")
            (root / "manuscript.md").write_text(r"C:\\private\\artifact.csv", encoding="utf-8")
            project = root / "project"
            project.mkdir()
            (project / "unsafe.zip").write_bytes(b"fixture")
            for script_name, argument in scripts.items():
                command = [sys.executable, str(ROOT / "skills" / "paper-research-cn-core" / "scripts" / script_name), str(root / argument[0])]
                result = subprocess.run(command, capture_output=True, text=True, check=False)
                payload = json.loads(result.stdout)
                self.assertIn("findings", payload)
                self.assertTrue(payload["findings"])
                self.assertTrue(FINDING_FIELDS.issubset(payload["findings"][0]))

    def test_privacy_audit_emits_structured_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            private_path = "C:" + "\\" + "Users" + "\\" + "private-user" + "\\" + "draft"
            (root / "note.md").write_text(private_path, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "skills" / "paper-research-cn-core" / "scripts" / "privacy_scan.py"), str(root), "--public"],
                capture_output=True,
                text=True,
                check=False,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(FINDING_FIELDS.issubset(payload["findings"][0]))


if __name__ == "__main__":
    unittest.main()
