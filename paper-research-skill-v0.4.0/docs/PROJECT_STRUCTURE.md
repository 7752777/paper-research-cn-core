# 论文项目目录

```text
paper-project/
├── .agents/skills/                   # 本套 Skills
├── .paper-project/
│   └── state.json                    # 跨会话唯一状态源
├── 00_admin/
│   ├── DECISIONS.md                  # 人工关卡与重大决策
│   ├── NEXT_ACTIONS.md
│   ├── PROVENANCE.md                 # 外部工具、Skill、来源与版本
│   ├── risks.md
│   └── external-skills/              # 只读参考，不自动执行
├── 01_venue/
│   ├── venue-dossier.md
│   ├── requirements-checklist.md
│   └── source-snapshots/
├── 02_topics/
│   ├── candidates/
│   ├── concept-map.yaml
│   ├── search-saturation.csv
│   ├── nearest-neighbors.csv
│   ├── novelty-audit.md
│   └── topic-scorecard.md
├── 03_protocol/
│   ├── research-plan.md
│   ├── search-protocol.md
│   ├── preregistration-style-plan.md
│   └── ethics-and-compliance.md
├── 04_literature/
│   ├── searches/
│   ├── metadata/
│   ├── pdfs/
│   ├── notes/
│   ├── screening/
│   ├── raw-exports/
│   ├── fulltext-requests/
│   ├── search-queries.csv
│   ├── work-records.jsonl
│   ├── screening-decisions.csv
│   ├── fulltext-manifest.csv
│   ├── evidence-ledger.csv
│   └── references.bib
├── 05_design/
│   ├── conceptual-model.md
│   ├── hypotheses.md
│   ├── instruments/
│   ├── sampling-plan.md
│   ├── design-comparison.md
│   ├── method-decision.md
│   └── analysis-plan.md
├── 06_data/
│   ├── raw/                           # 不覆盖、不手改
│   ├── interim/
│   ├── processed/
│   ├── external/
│   ├── metadata/
│   │   ├── source-manifest.csv
│   │   ├── data-dictionary.csv
│   │   └── quality-report.md
│   └── README.md
├── 07_analysis/
│   ├── code/
│   ├── notebooks/
│   ├── outputs/
│   ├── figures/
│   ├── tables/
│   ├── logs/
│   ├── results-manifest.csv
│   └── deviations.md
├── 08_manuscript/
│   ├── outline/
│   ├── sections/
│   ├── figures/
│   ├── tables/
│   ├── supplements/
│   ├── styles/
│   ├── build/
│   ├── claims.yaml
│   ├── evidence.yaml
│   ├── terminology.csv
│   ├── word-budget.json
│   ├── claim-ledger.csv
│   ├── manuscript.qmd
│   └── manuscript.md
├── 09_review/
│   ├── round-1-developmental/
│   ├── round-2-methods/
│   ├── round-3-hostile-editorial/
│   └── revision-matrix.csv
├── 10_submission/
│   ├── final/
│   ├── cover-letter/
│   ├── declarations/
│   └── submission-checklist.md
└── 99_archive/
```

## 状态规则

- `.paper-project/state.json` 是阶段、关卡和当前版本的唯一机器可读来源。
- 聊天内容不是状态源；新会话必须从文件恢复。
- 每次完成阶段后更新 `state.json`、`DECISIONS.md`、`NEXT_ACTIONS.md`。
- 原始材料、原始数据和已冻结结果只追加版本，不原地覆盖。
- 文件名使用 ISO 日期或版本号，例如 `2026-07-14-search-openalex-v1.json`。
