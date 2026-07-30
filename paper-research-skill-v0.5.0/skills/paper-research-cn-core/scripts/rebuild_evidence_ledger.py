#!/usr/bin/env python3
"""Rebuild an evidence ledger without inheriting unverified journal-tier claims."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from collections.abc import Iterable
from pathlib import Path


LEDGER_FIELDS = [
    "evidence_id",
    "corpus",
    "analysis_status",
    "analysis_role",
    "analysis_included",
    "material_category",
    "journal_tier",
    "tier_verification_basis",
    "title",
    "authors",
    "year",
    "source",
    "primary_theme",
    "themes",
    "governance_stage",
    "method_type",
    "claim_strength_original",
    "claim_strength_revised",
    "fulltext_pages",
    "text_path",
    "support_note",
    "limitations",
]


def value(record: dict[str, str], field: str) -> str:
    return (record.get(field) or "").strip()


def material_category(record: dict[str, str]) -> str:
    doc_type = value(record, "doc_type").casefold()
    if record.get("corpus") == "oa":
        return "英文期刊论文"
    if "学位" in doc_type or "硕士" in doc_type or "博士" in doc_type:
        return "学位论文"
    if "会议" in doc_type or "conference" in doc_type:
        return "会议论文"
    if "标准" in doc_type:
        return "标准/标准解读"
    if "期刊" in doc_type or "journal" in doc_type:
        return "期刊论文"
    if "补充" in doc_type:
        return "补充材料"
    return "其他材料"


def analysis_role(record: dict[str, str]) -> str:
    status = value(record, "analysis_status")
    if status == "duplicate_excluded":
        return "重复剔除"
    if status == "manual_review_encrypted":
        return "受限标准旁证"
    if record.get("corpus") == "oa":
        return "英文比较材料"
    if value(record, "include_in_core_denominator").casefold() == "true" and status == "included":
        return "主分析中文研究材料"
    if value(record, "corpus_role") == "中文补充":
        return "中文补充材料"
    return "技术背景，不入主分析"


def revised_claim_strength(record: dict[str, str]) -> str:
    original = value(record, "claim_strength")
    title = value(record, "title")
    method = value(record, "method_type")
    if method == "标准/规范解读" and title.startswith("国家标准") and "解读" in title:
        return "制度解释"
    return original


def transform_record(record: dict[str, str]) -> dict[str, str]:
    category = material_category(record)
    role = analysis_role(record)
    journal_tier = "期刊层级待官方目录核验" if category == "期刊论文" else "不适用"
    return {
        "evidence_id": value(record, "evidence_id"),
        "corpus": value(record, "corpus"),
        "analysis_status": value(record, "analysis_status"),
        "analysis_role": role,
        "analysis_included": "是" if role == "主分析中文研究材料" else "否",
        "material_category": category,
        "journal_tier": journal_tier,
        "tier_verification_basis": "待以北大核心/CSSCI等官方目录逐刊核验" if journal_tier != "不适用" else "材料类型不适用期刊分层",
        "title": value(record, "title"),
        "authors": value(record, "authors"),
        "year": value(record, "year"),
        "source": value(record, "source"),
        "primary_theme": value(record, "primary_theme"),
        "themes": value(record, "themes"),
        "governance_stage": value(record, "governance_stage"),
        "method_type": value(record, "method_type"),
        "claim_strength_original": value(record, "claim_strength"),
        "claim_strength_revised": revised_claim_strength(record),
        "fulltext_pages": value(record, "fulltext_pages"),
        "text_path": value(record, "text_path"),
        "support_note": value(record, "support_note"),
        "limitations": value(record, "limitations"),
    }


def counter_dict(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def build_summary(records: list[dict[str, str]]) -> dict[str, object]:
    transformed = [transform_record(record) for record in records]
    role_counts = Counter(row["analysis_role"] for row in transformed)
    main = [row for row in transformed if row["analysis_role"] == "主分析中文研究材料"]
    primary_theme = Counter(row["primary_theme"] for row in main if row["primary_theme"])
    method_type = Counter(row["method_type"] for row in main if row["method_type"])
    claim_strength = Counter(row["claim_strength_revised"] for row in main if row["claim_strength_revised"])
    governance_stage: Counter[str] = Counter()
    for row in main:
        governance_stage.update(
            stage for stage in row["governance_stage"].split(";") if stage and stage != "未明确"
        )
    excluded = {"duplicates": role_counts["重复剔除"]}
    outputs = {
        "main_chinese": role_counts["主分析中文研究材料"],
        "chinese_supplement": role_counts["中文补充材料"],
        "english_comparison": role_counts["英文比较材料"],
        "restricted_standard": role_counts["受限标准旁证"],
        "technical_background": role_counts["技术背景，不入主分析"],
    }
    return {
        "flow": {"identified": len(records), "excluded": excluded, "outputs": outputs},
        "main_sample_material_categories": counter_dict(Counter(row["material_category"] for row in main)),
        "primary_theme": counter_dict(primary_theme),
        "method_type": counter_dict(method_type),
        "claim_strength": counter_dict(claim_strength),
        "governance_stage": counter_dict(governance_stage),
        "tier_rule": "期刊条目均待以官方目录逐刊核验；非期刊材料不适用期刊层级。",
    }


def read_records(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_ledger(path: Path, records: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS)
        writer.writeheader()
        writer.writerows(transform_record(record) for record in records)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="coded-corpus.csv")
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args(list(argv) if argv is not None else None)
    records = read_records(args.source)
    summary = build_summary(records)
    write_ledger(args.ledger, records)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
