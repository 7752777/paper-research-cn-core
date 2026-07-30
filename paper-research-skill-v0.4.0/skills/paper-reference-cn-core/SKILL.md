---
name: paper-reference-cn-core
description: Verify, deduplicate, format, and audit Chinese journal references under GB/T 7714-2015 with DOI and metadata provenance requirements.
---

# 中文核心论文参考文献

用于题录清理、DOI 核验、去重和 GB/T 7714—2015 终稿审计。遵循 `references/gbt7714-rules.md` 与 `references/zotero-protocol.md`。

1. 先建立可追溯题录台账，区分已核验、待核验和不可获得；未核验条目不得进入投稿版。
2. 用 `scripts/deduplicate_records.py` 产生候选重复项；用 `scripts/verify_dois.py` 并传入 `--metadata metadata.json` 核验 DOI 语法与官方元数据状态，自动匹配必须人工确认。
3. 用 `scripts/format_refs_gbt7714.py` 生成候选格式，再用 `scripts/audit_refs.py` 并传入参考文献文件与 `--metadata metadata.json` 检查期刊卷期页码、学位论文信息、DOI 与逐条官方元数据核验。
4. 逐条核对正文引文和参考文献，确保没有悬空条目或无法定位的主张。

审计的 Major 表示书目信息不适合投稿，不能以“后续补齐”绕过终审。
