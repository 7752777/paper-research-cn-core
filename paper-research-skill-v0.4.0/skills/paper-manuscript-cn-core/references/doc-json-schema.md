# 统一 doc.json 契约

`doc.json` 是写作与渲染之间的中间表示。至少包含 `title`、`sections`、`blocks`、`tables`、`figures`、`references` 和 `audit_inputs`。`blocks` 是按文稿出现顺序排列的 `heading`、`paragraph`、`table` 与 `figure`；渲染器必须优先消费它，不能把图表集中到文末。每个表图条目应有稳定编号、题注、数据来源、分母、统计口径和资产路径。

文件应为 UTF-8 JSON。缺字段必须报出结构化审计结果，而不能默默生成空白表格或省略参考文献。
