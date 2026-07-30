---
name: paper-review-cn-core
description: Run independent Chinese-language peer review and revision for Chinese core-journal manuscripts, with anti-rubber-stamp checks, evidence sampling, and revision-matrix closure.
---

# 中文核心论文审稿修订

用于有完整草稿后的独立审稿、重大修订和终审复核。审稿依据稿件、台账、图表和参考文献，而不是对话中的乐观判断；先读 `references/review-rubric.md`、`references/revision-matrix-schema.md` 和 `references/anti-rubber-stamp.md`。

1. 第一轮检验问题、贡献、理论和中文议题适配；第二轮检验检索、样本、编码、统计和结论强度；第三轮以退稿风险审计格式、图表、引文和文风。
2. 每项意见以中文给出位置、严重度、证据、理由、修订动作和验证方式，写入修订矩阵。
3. 每轮重新计数并抽查引文、参考文献、图表和分母。若审稿发现限制，必须回写正文。
4. 用 `scripts/audit_review_output.py` 阻止“全部已解决”之类无证据结论。零 Critical/Major 必须逐项排除并保留审计记录。

不以削弱全部贡献来处理问题；修订应缩小不受支持的推论，同时保留被证据支持的学术贡献。
