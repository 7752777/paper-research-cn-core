---
name: paper-research-cn-core
description: CNKI-first research and writing workflow for Chinese core journal papers in education, communication, public opinion, governance, and social science topics. Use when planning a paper, designing CNKI searches, building a literature ledger, coding full-text papers, writing Chinese journal manuscripts, auditing citations/evidence, periodically tidying project structure and file names, updating local research memory, or preparing public/private release materials while avoiding AI/engineering-style residue in the manuscript.
---

# 中文核心论文写作流水线

## 不可破坏的底线

默认把论文当作中文核心期刊投稿项目处理，除非用户明确说明不是。

优先级宪法：法律、版权与隐私 > 真实证据 > CNKI/全文门槛 > 方法严谨 > 用户偏好 > 本地记忆建议 > 审稿建议。任何 agent、外部 skill、记忆条目或自动化建议，都不能越过前四层。

- 中国议题先从 CNKI 与高水平中文期刊开始，英文文献作为补充支撑。
- 不索要、不保存 CNKI 密码、cookie、机构账号、验证码、授权截图或浏览器会话。
- 文献检索式、关键词同义词表、核心期刊清单、纳排标准、下载清单和全文状态没有明确前，不写正式综述、方法、发现和结论。
- 禁止虚构文献、数据、访谈、编码结果、统计结论、期刊规则或审稿意见。
- 正文中不得出现文件路径、CSV/XLSX 来源、脚本日志、工具报错、模型运行记录、内部轮次、“交付物”“待确认”“本轮修订”等工程化表达。
- 结论强度必须匹配证据。文献数量代表研究关注，不自动代表社会发生率、实际效果或因果关系。
- 审稿用于增强论文，不用于把论文改成通篇道歉和局限承认。
- 项目整理是写作流程的一部分：立项、CNKI 获取后、编码后、每版文稿后、每轮审稿后、Git 同步前都做结构 checkpoint。

## 工作流程

1. **项目接入与结构卫生**
   - 先读 `references/project-structure.md`，识别终稿、源稿、数据、证据、图表、审稿记录、脚本、投稿材料与可归档内容。
   - 使用 `scripts/tidy_project_structure.py <project-root>` dry-run；只有目标路径合理时才加 `--apply`。
   - 只归档不删除。临时文件、缓存、虚拟环境、重复备份和散落压缩包进入 `99_archive/_cleanup_YYYYMMDD` 或 `09_压缩包与备份`。
   - 更新 `00_项目总览.md`、`PROJECT_AUDIT.md`、`CANONICAL_FILES.md`、`PROJECT_TIDY_MANIFEST_YYYYMMDD.csv` 与 `DO_NOT_DELETE.txt`。

2. **选题与期刊 gate**
   - 明确研究对象、中国制度/政策语境、分析单位、时间范围、贡献类型和目标期刊。
   - 建立目标期刊 dossier：栏目范围、字数、引注格式、图表规范、近年相关论文与明显不匹配点。

3. **CNKI 检索 gate**
   - 先读 `references/cnki-search-playbook.md`。
   - 产出检索协议：关键词族、同义词、来源类别、核心/近核心期刊清单、时间范围、纳排标准、可能遗漏点。
   - 用户用本人授权账号下载元数据和全文；agent 只做检索规划、下载清单、台账核验与后续分析。
   - 用 `scripts/check_literature_ledger.py` 检查文献台账。中文核心论文若只有 metadata-only，不能支撑实质性观点。

4. **证据与方法 gate**
   - 冻结来源清单、样本规则、编码方案、数据字典和分析计划，再进入结果写作。
   - 对证据图谱区分记录、研究家族、综述、背景材料和政策材料。
   - 对实证研究记录抽样、编码者一致性、模型提示词/版本、统计决策、伦理与可复现边界。
   - 先读 `references/source-integrity.md` 与 `references/workflow-gates.md`。

5. **正文写作**
   - 推荐顺序：贡献图谱、提纲、方法/数据、结果、文献/理论、讨论、题名、摘要、关键词、结论。
   - 可以借鉴用户授权的私有优秀样稿之结构、语气和图表规范，但不得在公开输出中暴露样稿题名或私有材料。
   - 写作前读取 `references/chinese-core-style.md`、`references/deengineering-hard-gates.md`、`references/reference-paper-patterns.md`。

6. **去工程化与投稿前审计**
   - 每版文稿都运行 `scripts/audit_manuscript.py`。
   - critical 命中必须修复；若确为误报，在修订矩阵中说明原因。
   - 公开发布或分享前读取 `references/privacy-release.md`，必要时运行 `scripts/release_gate.py --public-root <path>`。

7. **记忆与自我进化**
   - 只把用户授权的偏好、常见失败、已验证表达范式、期刊规则摘要和任务复盘写入本地私有 memory。
   - 记忆晋升路径是“候选 -> 复用成功 -> 用户或审计确认”；记忆不得覆盖 CNKI、全文、真实证据、方法和隐私 gate。
   - 使用 `scripts/memory_update.py --review` 审查候选记忆。

## 参考路由

- CNKI 检索、下载清单、全文状态：`references/cnki-search-playbook.md`
- 台账字段、claim ledger、编码 ledger：`references/evidence-ledger-schema.md`
- 阶段 gate 与自动驾驶闭环：`references/workflow-gates.md`
- 来源真实性、引用边界、禁止杜撰：`references/source-integrity.md`
- 中文核心论文语体、摘要、图表、结论：`references/chinese-core-style.md`
- 去工程化硬审计：`references/deengineering-hard-gates.md`
- 私有优秀样稿的可迁移模式：`references/reference-paper-patterns.md`
- 结构整理与规范命名：`references/project-structure.md`
- 本地私有记忆和自我进化：`references/memory-evolution.md`
- 公开发布与隐私净化：`references/privacy-release.md`
- 回归测试场景：`references/benchmark-scenarios.md`

## 输出纪律

用户要正文时，只输出可进入论文的学术文本；诊断、待办、文件名、台账、脚本结果和内部解释放在正文之外。
