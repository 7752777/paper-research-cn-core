# 4.0 工作流

## 1. 研究证据

使用 `paper-research-cn-core` 建立检索协议和分层台账。期刊、学位论文、会议、标准和综述必须分开统计；期刊层级未经逐条官方目录核验时，只能称为中文文献或期刊材料，不能写成核心样本。运行 `check_literature_ledger.py`、`rebuild_evidence_ledger.py` 与 `audit_number_consistency.py`，并保存 JSON 审计结果。

## 2. 文稿与图表

用 `paper-manuscript-cn-core` 生成 `doc.json`，建立章节契约、字数预算和渲染记录。正文不得包含投稿、审稿、返修或工具过程等元话语。用 `paper-figure-cn-core` 生成图表并保存矢量源图；每个题注必须说明分母、统计口径和多重编码限制。

## 3. 参考文献

使用 `paper-reference-cn-core` 做去重、DOI 核验和 GB/T 7714 审计。无官方或可追溯元数据的条目不能进入投稿版参考文献；Zotero 导出和人工修订的差异应留在台账中。

## 4. 独立审稿与修订

`paper-review-cn-core` 必须形成中文三轮独立审稿记录。每轮重新计数 Critical、Major、Minor，并记录引文、参考文献和图表抽样。任何限制都要回写正文；零 Critical/Major 时仍须保留逐项排除记录。审计脚本会把仍在记录中的 Critical/Major 传给终审。

## 5. 投稿终审

`paper-submission-cn-core` 读取真实工件路径及九类 JSON 审计报告：数字、AI 文风、图表、参考文献、台账、文稿、目录结构、独立审稿和渲染。任一工件缺失、报告格式不合格或有 Critical/Major 时，终审以非零状态退出。实际点击期刊系统提交前仍由作者确认。

## 6. 公开发布

公开发布只同步通用 skill、脚本、合成 fixture 和公共文档。论文正文、真实台账、审稿意见、二进制稿件、图片和本地路径一律留在私库。同步后运行隐私扫描和 release gate。
