from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "paper-research-cn-core" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from rebuild_evidence_ledger import build_summary, transform_record


class EvidenceLedgerTests(unittest.TestCase):
    def test_marks_non_periodical_records_as_not_applicable_to_journal_tier(self) -> None:
        record = {
            "evidence_id": "T-01",
            "corpus": "cnki",
            "corpus_role": "中文核心",
            "include_in_core_denominator": "true",
            "analysis_status": "included",
            "doc_type": "硕士论文",
            "title": "测试论文",
            "method_type": "公共管理案例/政策分析",
            "claim_strength": "机制解释",
        }

        result = transform_record(record)

        self.assertEqual(result["analysis_role"], "主分析中文研究材料")
        self.assertEqual(result["material_category"], "学位论文")
        self.assertEqual(result["journal_tier"], "不适用")
        self.assertEqual(result["claim_strength_revised"], "机制解释")

    def test_reclassifies_standard_interpretation_and_closes_summary(self) -> None:
        records = [
            {
                "evidence_id": "T-01",
                "corpus": "cnki",
                "corpus_role": "中文核心",
                "include_in_core_denominator": "true",
                "analysis_status": "included",
                "doc_type": "期刊",
                "title": "国家标准《测试》解读",
                "primary_theme": "标准制度",
                "method_type": "标准/规范解读",
                "claim_strength": "报告性效能指标",
                "governance_stage": "制度协同",
            },
            {
                "evidence_id": "T-02",
                "corpus": "cnki",
                "corpus_role": "中文补充",
                "include_in_core_denominator": "false",
                "analysis_status": "included",
                "doc_type": "补充材料",
                "title": "补充材料",
                "primary_theme": "",
                "method_type": "",
                "claim_strength": "",
                "governance_stage": "",
            },
            {
                "evidence_id": "T-03",
                "corpus": "cnki",
                "corpus_role": "中文补充",
                "include_in_core_denominator": "false",
                "analysis_status": "manual_review_encrypted",
                "doc_type": "补充材料",
                "title": "受限标准",
                "primary_theme": "",
                "method_type": "",
                "claim_strength": "",
                "governance_stage": "",
            },
            {
                "evidence_id": "T-04",
                "corpus": "oa",
                "corpus_role": "英文补充",
                "include_in_core_denominator": "false",
                "analysis_status": "included",
                "doc_type": "article",
                "title": "English comparison",
                "primary_theme": "",
                "method_type": "",
                "claim_strength": "",
                "governance_stage": "",
            },
            {
                "evidence_id": "T-05",
                "corpus": "cnki",
                "corpus_role": "中文核心",
                "include_in_core_denominator": "false",
                "analysis_status": "included",
                "doc_type": "会议论文",
                "title": "背景材料",
                "primary_theme": "背景技术",
                "method_type": "技术测试/性能评估",
                "claim_strength": "报告性效能指标",
                "governance_stage": "未明确",
            },
            {
                "evidence_id": "T-06",
                "corpus": "cnki",
                "corpus_role": "中文核心",
                "include_in_core_denominator": "false",
                "analysis_status": "duplicate_excluded",
                "doc_type": "期刊",
                "title": "重复材料",
                "primary_theme": "",
                "method_type": "",
                "claim_strength": "",
                "governance_stage": "",
            },
        ]

        summary = build_summary(records)

        self.assertEqual(summary["flow"]["identified"], 6)
        self.assertEqual(sum(summary["flow"]["outputs"].values()), 5)
        self.assertEqual(sum(summary["flow"]["excluded"].values()), 1)
        self.assertEqual(summary["claim_strength"]["制度解释"], 1)


if __name__ == "__main__":
    unittest.main()
