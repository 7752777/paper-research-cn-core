---
name: paper-manuscript-cn-core
description: Draft, structure, render, and audit Chinese core-journal manuscripts with a shared doc.json contract, word budgets, AI-style checks, and Word/PDF regression checks.
---

# 中文核心论文文稿与排版

用于把经核验的证据写成论文并生成稳定稿件。以 `references/section-contracts.md` 约束章节功能，以 `references/doc-json-schema.md` 维护统一文档接口。

1. 先从冻结证据台账写方法、结果和图表，再写摘要与结论；正文每个数字、结论和引文必须可追溯。
2. 用 `scripts/build_doc_json.py` 生成或校验 `doc.json`；用 `scripts/word_budget.py` 检查章节预算。
3. 用 `scripts/audit_ai_style.py` 阻断投稿元话语、密集模板化转折和工程化残留。限制、单人编码与 AI 辅助边界应明确披露。
4. 用 `scripts/render_cn_journal_docx.py` 和 `scripts/render_pdf.py` 生成可审查稿；按 `references/render-regression-checklist.md` 抽检渲染结果。

没有 LibreOffice 时，安装 `python-docx` 与 `reportlab`：`python -m pip install python-docx reportlab`。本地 PDF fallback 还需要可用中文字体；必要时设置 `CN_CORE_CJK_FONT` 为字体文件路径。依赖或字体缺失时，渲染器必须报错，不能生成空白或替代性 PDF。

不把缺失元数据、待核验期刊层级或无法闭合的统计量写成确定性结论。图表和参考文献分别交由对应 skill 审计。
