# paper-research-cn-core

[![Public release](https://img.shields.io/badge/release-public-2ea44f)](https://github.com/7752777/paper-research-cn-core)
[![Codex Skills](https://img.shields.io/badge/Codex-skills-2563eb)](#包含什么)
[![CNKI-first](https://img.shields.io/badge/workflow-CNKI--first-b45309)](#工作流)
[![Evidence gated](https://img.shields.io/badge/evidence-gated-0f766e)](#设计原则)
[![License](https://img.shields.io/badge/license-not%20specified-lightgrey)](#许可证)

面向中文核心期刊写作的 **CNKI-first evidence-gated Codex skill** 工具包。

它把中文论文写作中最容易失控的环节做成硬门槛：先完成可复核的中文核心文献检索、全文获取清单、证据台账和研究设计，再进入写作、去工程化审计、三轮独立审稿与投稿前复核。

这个公开仓库只发布通用 workflow、skill、agent 描述、空模板和辅助脚本；不包含私人论文项目、CNKI 下载全文、投稿材料、审稿记录、机构信息、账号信息或任何凭据。

## 适合谁

- 需要写中文核心、CSSCI、北大核心、AMI 或高水平中文期刊论文的研究者。
- 希望 AI 参与选题、检索、综述、编码、写作和审稿，但不接受虚构文献、数据拼接和工作报告式正文的人。
- 希望把个人论文项目维护成“可复查、可续写、可审稿、可投稿”的长期研究工作流的人。

## 包含什么

| 模块 | 路径 | 作用 |
| --- | --- | --- |
| 写作 skill | `paper-research-skill-v0.3.0/skills/paper-research-cn-core` | 选题、CNKI 检索规划、文献台账、研究设计、项目整理、正文写作、投稿前审计、发布 gate 与本地记忆规则 |
| 审稿 skill | `paper-research-skill-v0.3.0/skills/paper-review-cn-core` | 三轮独立审稿、修订矩阵、方法/证据复核、去工程化检查、反过度道歉 |
| 写作 agent 描述 | `paper-research-skill-v0.3.0/skills/paper-research-cn-core/agents/openai.yaml` | 面向中文核心论文写作流水线的默认 agent 名称与启动提示 |
| 审稿 agent 描述 | `paper-research-skill-v0.3.0/skills/paper-review-cn-core/agents/openai.yaml` | 面向中文核心三轮审稿的默认 agent 名称与启动提示 |
| 项目整理脚本 | `paper-research-skill-v0.3.0/skills/paper-research-cn-core/scripts/tidy_project_structure.py` | 对论文项目做 dry-run/apply 式结构归位、规范命名和整理 manifest |
| 深层结构审计 | `paper-research-skill-v0.3.0/skills/paper-research-cn-core/scripts/deep_structure_audit.py` | 扫描活跃区压缩包、缓存、虚拟环境和过深嵌套 |
| 记忆更新脚本 | `paper-research-skill-v0.3.0/skills/paper-research-cn-core/scripts/memory_update.py` | 管理本地私有偏好、失败模式和可复用经验候选 |
| 发布审计脚本 | `scripts/privacy_scan.py`, `scripts/release_gate.py` | 检查公开仓库是否混入本地路径、凭据、二进制论文材料或发布禁区内容 |

## 工作流

```mermaid
flowchart LR
    A["选题与期刊定位"] --> B["CNKI 检索规划"]
    B --> C["用户授权下载全文"]
    C --> D["文献台账与证据编码"]
    D --> E["方法与数据冻结"]
    E --> F["中文核心论文写作"]
    F --> G["去工程化审计"]
    G --> H["三轮独立审稿"]
    H --> I["修订矩阵与投稿前复核"]
    I --> J["项目整理与发布审计"]
    J --> K["本地记忆候选复盘"]
```

## 快速开始

```powershell
git clone https://github.com/7752777/paper-research-cn-core.git
cd paper-research-cn-core
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1
```

安装后在 Codex 中调用：

```text
使用 $paper-research-cn-core 帮我为“高校数字治理能力建设”这个选题设计中文核心期刊论文的 CNKI 检索方案、纳排标准、全文下载清单和项目结构 checkpoint。
```

```text
使用 $paper-review-cn-core 对这篇中文论文做三轮独立审稿，输出修订矩阵，重点检查贡献、文献、方法、证据、图表、引用和去工程化表达。
```

## 设计原则

| 原则 | 含义 |
| --- | --- |
| 真实优先 | 不虚构文献、数据、访谈、编码结果、统计结论或期刊规则 |
| CNKI 优先 | 中国议题先以中文核心和高水平中文文献为主，英文文献作为补充 |
| 全文证据优先 | 先有检索式、纳排标准、下载清单、文献台账和全文状态，再进入综述与正文 |
| 方法严谨 | 样本、编码、模型、统计、伦理和可复现边界必须可说明 |
| 论文语体优先 | 摘要、图注、表注、结论只保留学术表达，不把文件路径、CSV、脚本日志和内部轮次写进论文 |
| 审稿不夺权 | 审稿 agent 提批评、证据和修订建议，最终由作者或主写作 agent 决定采纳、反驳或降级 |
| 本地记忆私有 | 个性化偏好和失败复盘只进入本地私有 memory，不进入公开仓库 |
| 公开最小化 | 公开仓库只放通用 workflow，不传播论文全文、私有数据、投稿材料和账号凭据 |

## 公开边界

请不要把以下材料提交到这个仓库：

- 数据库、出版平台或机构授权渠道下载的 PDF、CAJ、HTML、TXT 全文及其抽取文本。
- 私人论文项目、阶段稿、终稿、投稿稿、审稿意见、通讯作者审阅记录和修订历史。
- 文献管理导出、全文下载清单、带本地路径的数据表、压缩包、浏览器配置、cookie、token、账号截图或授权机构信息。

详细规则见 [PUBLIC_RELEASE_POLICY.md](PUBLIC_RELEASE_POLICY.md)。

## 维护方式

公开仓库是从维护者的私有工作区生成的发布镜像。公开同步前必须运行隐私扫描和发布 gate；任何需要长期保留的公开文档改动，都应先写回私有维护源，再重新生成公开镜像。

```powershell
python .\scripts\release_gate.py --public-root .
git status --short
```

维护细节见 [docs/MAINTAINER_GUIDE.md](docs/MAINTAINER_GUIDE.md)。

## 外部参考

本项目吸收了公开 agent skills 生态的结构经验，包括自包含 skill 组织、精选 skill 列表的可发现性、科研工作流的证据门槛，以及 agent memory/self-improvement 的评估回路。外部项目只作为结构参考，本仓库不复制其私有内容或许可证文本。

## 许可证

暂未声明开源许可证。公开可见不等于自动授权再分发、商用或再许可；后续如需开放许可证，应由仓库所有者单独添加 `LICENSE`。
