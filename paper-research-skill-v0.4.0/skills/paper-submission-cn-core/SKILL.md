---
name: paper-submission-cn-core
description: Perform final submission readiness checks for Chinese journal papers by composing evidence, manuscript, figure, reference, rendering, and independent-review gates.
---

# 中文核心论文投稿终审

用于提交前的独立终审。按 `references/submission-gate.md` 汇总所有前序审计；它不替代研究、文稿、图表、参考文献或审稿 skill。

1. 收集冻结版 `doc.json`、证据台账、数字审计、图表审计、参考文献审计、渲染记录和独立审稿矩阵。
2. 用 `scripts/audit_submission_package.py` 输出结构化门禁记录。任何 Critical 或 Major 返回非零状态，禁止标记为可投稿。
3. 对剩余证据缺口给出范围化处理：删去无法支持的结论、在方法/讨论披露限制，或从投稿版移除未核验条目。

提交材料中不出现内部路径、工具日志、私人全文、审稿过程或“AI 已完成”的说明。
