---
name: paper-review-cn-core
description: Independent three-round peer-review and revision workflow for Chinese core journal papers. Use after a manuscript draft exists, before submission, after major revisions, or when a fresh review agent/subtask is needed to audit contribution, theory, methods, evidence, style, figures/tables, citations, de-engineering residue, and apology-drift without taking over the author's argument.
---

# 中文核心论文三轮审稿

## 审稿契约

审稿对象是冻结文稿和本地证据材料，不是对话记忆。找不到文稿、台账、方法附件或审稿历史时，先在项目目录中检索；确实缺失再向用户说明。

- 三轮审稿保持独立，不让第二轮复读第一轮，也不让第三轮继承未经验证的乐观判断。
- 发现问题优先于礼貌性总结。每条问题需要位置、严重度、证据、理由、建议和验证方式。
- 不擅自重写全文。默认输出定位明确的修改建议和修订矩阵。
- 保护论文主贡献。局限应具体、有边界、有用，不把论文压扁成局限说明。
- 方法、证据和数据同步问题不能只靠降调措辞解决。

## 三轮结构

1. **第一轮：贡献、理论与期刊适配**
   - 检查题名、摘要、问题意识、文献缺口、概念和贡献是否匹配目标中文期刊。
   - 检查中国议题是否以中文核心与领域权威文献为主。
   - 标出过度声称、贡献不足、对象边界不稳和国内锚点缺失。

2. **第二轮：方法、证据与可复现性**
   - 核对语料构建、CNKI/全文状态、抽样、编码、编码者一致性、模型提示词/版本、统计、伦理和表文一致性。
   - 证据图谱重点查分母、记录/家族区分、证据层级、时间范围和“未知不等于零”。
   - 实证研究重点查效度、信度、操纵检验、匹配、混杂与结论强度。

3. **第三轮：敌意编辑与投稿前审计**
   - 以可能退稿的编辑视角阅读。
   - 审计摘要、结论、图表、注释、引用、字数、期刊规则、中文表达和工程化残留。
   - 有文稿文本时运行或请求 `$paper-research-cn-core` 中的 `audit_manuscript.py`。

## 严重度

- **Critical**：导致不可投稿、主结论不成立、伦理/版权/隐私风险，或正文有明显 AI/过程痕迹。
- **Major**：明显削弱贡献、方法、证据、期刊适配或可复现性，投稿前必须修改。
- **Minor**：改善清晰度、格式、表注、引文精度或语体，不改变核心论证。
- **Note**：可选润色或未来研究建议。

## 反“过度道歉”规则

先读 `references/review-rubric.md` 和 `references/anti-apology-drift.md`。审稿的目标是让论文更强、更稳、更像期刊论文，而不是让作者不断撤回自己的贡献。
