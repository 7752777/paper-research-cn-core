---
name: paper-research-cn-core
description: Build and audit evidence-led Chinese social-science journal research, including CNKI-first search plans, literature ledgers, journal-tier verification, coding, and closed evidence maps.
---

# 中文核心论文研究证据

用于选题、检索协议、中文文献台账、全文编码、证据图谱和研究方法审计。先处理真实证据，再写任何结论；不能访问或未核验的元数据必须明确标注，不得补造。

## 不可跳过的边界

- “核心期刊”仅可由官方目录及版本逐条核验；未核验时使用“中文文献样本”或“期刊层级待核验”。详见 `references/journal-tier-lists.md`。
- 期刊、学位论文、会议论文、标准、政策和综述必须分层。它们可以解释研究背景，但不得混入期刊核心样本分母。
- 一条主张必须能回溯到全文、可核验元数据或明确标为背景材料。AI 仅可辅助提取候选关键词、归并标签和检查一致性，人工复核边界必须写进方法。
- 筛选流、分母、图表频数与正文数字必须闭合；多重编码不能伪装成互斥比例。规则见 `references/statistical-audit.md`。

## 工作流

1. 制定检索协议：主题词、同义词、数据库、时段、来源类型、纳排标准和全文状态。
2. 建立证据台账：每条记录包含材料类型、期刊层级、全文状态、纳排理由、方法、主题、治理环节、主张强度与出处。
3. 用 `scripts/check_literature_ledger.py` 检查台账字段；必要时用 `scripts/rebuild_evidence_ledger.py` 将历史编码重建为分层台账。
4. 用 `scripts/audit_number_consistency.py` 检查筛选流和多重编码；再以抽样方式复核编码和引用。
5. 进入正文前运行 `scripts/deep_structure_audit.py` 与 `scripts/audit_manuscript.py`；发现的限制必须进入方法或讨论，而不是仅写在项目记录中。

公开发布前还要遵守 `references/privacy-release.md`，运行 `scripts/privacy_scan.py` 和 `scripts/release_gate.py`。私有论文、全文、审稿意见、真实台账及路径永不作为公开 fixture。
