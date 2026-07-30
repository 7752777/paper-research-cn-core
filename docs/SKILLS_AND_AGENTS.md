# Skills And Agents

本仓库公开六个可组合的 4.0 skill。它们不含私人论文材料、全文或审稿记录，只提供可复用 workflow、脚本与合成 fixture。

## Skill Reference

| 名称 | 触发场景 | 主要产出 |
| --- | --- | --- |
| `paper-research-cn-core` | 选题、CNKI 检索规划、分层文献台账与研究证据 | 检索协议、证据台账、纳排与分层审计 |
| `paper-manuscript-cn-core` | 中文核心文稿撰写、版式与渲染检查 | 文稿、`doc.json`、Word/PDF 渲染记录 |
| `paper-figures-cn-core` | 图表、题注、分母和多重编码限制核验 | 图表清单、题注审计、适配报告 |
| `paper-references-cn-core` | GB/T 7714 与期刊/DOI 官方元数据核验 | 参考文献表、元数据核验结果 |
| `paper-review-cn-core` | 三轮中文独立审稿、重大修改后复审 | 审稿意见、严重度分级、修订矩阵 |
| `paper-submission-cn-core` | 投稿终审、结构化审计聚合与发布门禁 | 门禁报告、阻断项和可追溯修复建议 |

## 推荐协作方式

1. 用写作 skill 建立检索协议、文献台账和论文草稿。
2. 每个阶段结束时整理项目结构，刷新 `00_项目总览.md` 和 tidy manifest。
3. 冻结文稿和证据材料。
4. 新开任务或 agent 调用审稿 skill，避免前面对话记忆影响审稿独立性。
5. 将审稿结果整理成修订矩阵，由作者或主写作 agent 决定采纳、部分采纳、反驳或延后。
6. 修改后再次运行去工程化审计、结构 checkpoint、隐私扫描和发布 gate。
