---
name: paper-research-cn-core
description: Use when planning, writing, reviewing, revising, rendering, or finalizing a Chinese core-journal paper, especially when CNKI evidence, figures, GB/T 7714 references, Chinese peer review, or submission readiness must be checked together.
---

# 中文核心论文全流程

用一个工作流完成证据、文稿、图表、参考文献、审稿和投稿终审。先核验真实材料，再允许更强的论文主张；任何 Critical 或 Major 都阻断投稿。

## 阶段路由

| 阶段 | 先读 | 运行 |
| --- | --- | --- |
| 检索、台账、编码、样本分层 | `references/cnki-search-playbook.md`、`references/evidence-ledger-schema.md`、`references/journal-tier-lists.md`、`references/statistical-audit.md` | `scripts/check_literature_ledger.py`、`scripts/audit_number_consistency.py`、`scripts/rebuild_evidence_ledger.py` |
| 写作、结构、字数、渲染 | `references/section-contracts.md`、`references/doc-json-schema.md`、`references/render-regression-checklist.md` | `scripts/build_doc_json.py`、`scripts/word_budget.py`、`scripts/render_cn_journal_docx.py`、`scripts/render_pdf.py` |
| 图表与三线表 | `references/figure-hard-rules.md`、`references/caption-template.md` | `scripts/audit_figures.py`、`scripts/make_three_line_table.py` |
| 参考文献 | `references/gbt7714-rules.md`、`references/zotero-protocol.md` | `scripts/deduplicate_records.py`、`scripts/verify_dois.py`、`scripts/audit_refs.py` |
| 中文独立审稿与修订 | `references/review-rubric.md`、`references/anti-rubber-stamp.md`、`references/revision-matrix-schema.md` | `scripts/audit_review_output.py` |
| 投稿与公开发布 | `references/submission-gate.md`、`references/privacy-release.md` | `scripts/audit_submission_package.py`、`scripts/privacy_scan.py`、`scripts/release_gate.py` |

## 不可跳过的门槛

- 期刊、学位论文、会议、标准、政策与综述必须分层；没有官方目录和版本证据时，不得称为核心期刊样本。
- 筛选流、正文、图表和表格的分母必须闭合；多重编码必须披露。
- AI 只能辅助候选提取、标签归并和一致性检查；人工复核边界、单人编码和限制必须进入方法。
- 图表必须有编号、题注、分母、统计口径、数据来源和可编辑/矢量源；正式参考文献必须有官方或可追溯元数据。
- 审稿必须中文完成、分三轮独立记录；每轮统计 Critical/Major/Minor，抽样核对引文、参考文献和图表，并把限制回写文稿。
- 终审只读取真实工件和结构化审计结果。未关闭 Critical/Major、缺失报告、个人路径、全文、账号或凭据均会阻断投稿或公开发布。

## 使用顺序

1. 建立检索协议、分层台账和编码规则，先运行台账与数字审计。
2. 冻结可追溯证据后起草文稿，生成 `doc.json`，完成 Word/PDF 渲染检查。
3. 同步审计图表、题注、GB/T 7714、DOI 和官方元数据。
4. 完成三轮中文独立审稿和修订矩阵；将每项限制回写正文。
5. 以投稿终审聚合全部审计；公开发布额外运行隐私扫描与发布门禁。

真实论文、下载全文、审稿意见、台账、个人信息、本地路径和凭据只能留在私有工作区，不能作为公开 fixture 或提交内容。
