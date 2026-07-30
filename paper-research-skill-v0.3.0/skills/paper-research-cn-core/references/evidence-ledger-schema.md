# 文献与证据台账字段

推荐用 CSV/XLSX 管理大语料，用 Markdown 表格展示小清单。

## 文献台账

- `id`
- `title`
- `authors`
- `year`
- `journal`
- `source_database`
- `journal_tier`
- `search_query`
- `retrieval_date`
- `fulltext_status`
- `local_path`
- `inclusion_decision`
- `exclusion_reason`
- `study_family_id`
- `topic_tags`
- `method_tags`
- `evidence_tier`
- `notes`

## 编码台账

- `source_id`
- `unit_of_analysis`
- `code_family`
- `code`
- `value`
- `evidence_quote_or_page`
- `coder`
- `coding_date`
- `confidence`
- `disagreement_note`

## 观点台账

- `claim_id`
- `claim_text`
- `section`
- `supporting_source_ids`
- `supporting_data`
- `claim_strength`
- `limits`
- `allowed_wording`
- `forbidden_wording`

## 全文状态

只使用：`downloaded`、`metadata-only`、`abstract-only`、`unavailable`、`excluded`。

中文核心文献若为 `metadata-only`，不能支撑正文中的实质性判断。
