# ADR-001: Skill 文件统一 UTF-8

4.0 的 SKILL、参考文档、脚本和 `agents/openai.yaml` 一律使用 UTF-8。这样可保证中文说明、审计证据与题注在跨平台环境中保持稳定。

当前 Windows 环境中的 `generate_openai_yaml.py` 未显式指定 UTF-8，因而会以默认 GBK 读取包含中文的 SKILL 文件并失败。包不以该行为作为校验门槛：YAML 由同一前端契约手工生成，`validate_package.py` 以 UTF-8 验证包内容。生成器修复后可重新生成 YAML，但不得把文件改回本地代码页。
