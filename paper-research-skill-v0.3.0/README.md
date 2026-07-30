# paper-research-skill-v0.3.0

这是 `paper-research-cn-core` 与 `paper-review-cn-core` 的可移植 skill 包，面向中文核心期刊论文的 CNKI-first、证据门控、去工程化写作与三轮审稿流程。

| Skill | 用途 |
| --- | --- |
| `skills/paper-research-cn-core` | 选题、CNKI 检索规划、文献台账、全文证据、项目整理、研究设计、正文写作、投稿前审计、公开发布 gate 与本地私有记忆。 |
| `skills/paper-review-cn-core` | 独立三轮审稿、修订矩阵、贡献保护、方法/证据复核、去工程化检查与反过度道歉。 |

## 安装

```powershell
$skillsRoot = Join-Path $env:USERPROFILE ".codex\skills"
New-Item -ItemType Directory -Force $skillsRoot | Out-Null
Copy-Item -Recurse -Force .\skills\paper-research-cn-core (Join-Path $skillsRoot "paper-research-cn-core")
Copy-Item -Recurse -Force .\skills\paper-review-cn-core (Join-Path $skillsRoot "paper-review-cn-core")
```

## 核心流程

1. 项目结构 checkpoint 与规范命名。
2. 目标期刊和研究对象 gate。
3. CNKI 检索协议、核心期刊清单和全文下载清单。
4. 用户授权下载全文后建立文献台账。
5. 证据、编码、方法和 claim ledger 冻结。
6. 中文核心期刊语体写作。
7. 去工程化审计。
8. 三轮独立审稿和修订矩阵。
9. 投稿前复核、项目整理、私库/公开库分流。
10. 本地私有记忆候选复盘与晋升。
