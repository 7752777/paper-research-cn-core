# Changelog

## 0.4.0 - 2026-07-31

- 从两个混合职责 skill 升级为研究证据、文稿排版、图表、参考文献、审稿修订和投稿终审六个 skill。
- 引入统一审计 finding 接口：`rule_id`、`severity`、`file`、`evidence`、`remediation`；Critical/Major 返回非零状态。
- 增加数字闭合、期刊层级、AI 文风、GB/T 7714、图表题注与矢量源图、反橡皮图章和投稿包审计。
- 引入 `doc.json` 契约、DOCX/PDF 渲染检查、可执行正负 fixture 及安装/包验证器。
- 保留 3.0 为私库历史版本；公开同步只允许通用 4.0 包。
