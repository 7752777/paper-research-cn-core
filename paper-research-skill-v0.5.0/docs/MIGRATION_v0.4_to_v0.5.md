# 从 4.0 到 5.0

5.0 将六个拆分目录合并为 `paper-research-cn-core`。调用名称保持不变，但原先需分别调用的文稿、图表、参考文献、审稿和终审能力改由同一 skill 的阶段路由调用。

先运行 `validate_package.py`，再运行安装器的 `--dry-run --prune-legacy`。确认动作只包含一个主 skill 和五个精确命名的拆分目录后，使用 `--force --prune-legacy`。正式论文仍须保存分层证据、数字审计、`doc.json`、图表/题注清单、参考文献审计、渲染记录和审稿矩阵。
