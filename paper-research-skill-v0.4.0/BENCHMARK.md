# 4.0 基准记录

| 场景 | 输入 | 预期结果 | 自动化位置 |
| --- | --- | --- | --- |
| 未闭合筛选流 | 合成 12 条记录、仅 10 条去向 | `NUM-FLOW-001` Critical，非零退出 | `tests/test_audit_number_consistency.py` |
| 未声明多重编码 | 频数总和高于分母、`multiple=false` | `NUM-MULTI-001` Major，非零退出 | `tests/test_audit_number_consistency.py` |
| 投稿元话语 | 含“投稿”“评审”正文 | `AI-STYLE-001` Major | `tests/test_package_contracts.py` |
| 缺失卷期页码 | 不完整期刊条目 | `REF-GBT-001` Major | `tests/test_package_contracts.py` |
| 图表不可复用 | PNG 无 SVG 且题注无分母 | `FIG-VECTOR-001` 与 `FIG-CAPTION-001` Major | `tests/test_package_contracts.py` |
| 安装完整性 | 同一 skill 树 | 哈希一致、无 findings | `tests/test_package_contracts.py` |

基准只验证工作流规则。真实论文的完整审计另存于私库，不作为公开测试样本。
