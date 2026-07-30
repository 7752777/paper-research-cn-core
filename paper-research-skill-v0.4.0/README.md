# paper-research-skill-v0.4.0

可移植的中文核心期刊论文工作流包。4.0 将研究证据、文稿排版、图表、参考文献、审稿修订和投稿终审拆为六个可独立调用的 skill，并通过统一的结构化审计结果接口连接。

| Skill | 作用 |
| --- | --- |
| `paper-research-cn-core` | 检索协议、分层证据台账、期刊层级与数字一致性审计 |
| `paper-manuscript-cn-core` | 文稿章节契约、`doc.json`、AI 文风、DOCX/PDF 渲染 |
| `paper-figure-cn-core` | 筛选流、机制图、三线表、题注与资产审计 |
| `paper-reference-cn-core` | GB/T 7714、DOI、元数据和重复项审计 |
| `paper-review-cn-core` | 三轮中文审稿、反橡皮图章和修订矩阵 |
| `paper-submission-cn-core` | 汇总前述结果并阻断未解决的 Critical/Major |

## 安装

先验证包和安装计划：

```powershell
python .\validate_package.py
python .\install.py --target codex --dry-run
```

确认只有六个同名 skill 会被更新后再执行：

```powershell
python .\install.py --target codex --force
```

安装器只操作上述六个目录，忽略 `__pycache__` 与 `.pyc`，不会触碰其他已安装 skill。

## 发布门禁

```powershell
python -m unittest discover -s .\tests -v
python .\validate_package.py
```

私有论文可以作为集成测试，但不得进入公开 package、fixture、文档、截图或发布仓库。公开镜像只同步本目录、通用安装工具和文档；同步前运行隐私和发布门禁。
