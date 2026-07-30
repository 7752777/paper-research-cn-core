---
name: paper-figure-cn-core
description: Design, generate, and audit publication-ready evidence maps, mechanisms, and three-line tables for Chinese journal papers with traceable captions and vector-source checks.
---

# 中文核心论文图表

用于证据图谱、机制图和三线表。先读 `references/figure-hard-rules.md` 与 `references/caption-template.md`，再开始制图。

- 图表数量由论证需要决定；证据图谱型论文通常保留闭合筛选流程图、机制图以及 3 至 4 张信息表。
- 题注必须报告分母、统计口径和多重编码限制。任何图表数字均从冻结台账生成并可重算。
- 用 `scripts/make_three_line_table.py` 输出无装饰三线表；用 `scripts/figure_style.py` 建立统一字体、色板和导出格式。
- 用 `scripts/audit_figures.py` 检查缺失资产、缺失 SVG 源图和不完整题注。Critical 或 Major 阻断投稿终审。

不将流程记录、私有文件路径或“为投稿制作”之类过程说明写入图表正文和题注。
