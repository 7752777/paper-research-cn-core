# Local Usage

这份指南面向希望把公开仓库中的两个 skill 安装到本机 Codex skills 目录的用户。

## 一键安装

```powershell
git clone https://github.com/7752777/paper-research-cn-core.git
cd paper-research-cn-core
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1
```

安装目标：

- `paper-research-cn-core` -> `%USERPROFILE%\.codex\skills\paper-research-cn-core`
- `paper-review-cn-core` -> `%USERPROFILE%\.codex\skills\paper-review-cn-core`

## 在 Codex 中调用

写作流水线：

```text
使用 $paper-research-cn-core 帮我从选题开始，先设计 CNKI 检索式、关键词同义词表、核心期刊清单、纳排标准和全文下载清单，并在每个阶段结束时运行项目结构整理 checkpoint。
```

审稿流水线：

```text
使用 $paper-review-cn-core 对这篇论文做三轮独立审稿，输出问题清单、严重度、证据、修订建议和修订矩阵。
```

## 阶段整理

```powershell
python .\paper-research-skill-v0.3.0\skills\paper-research-cn-core\scripts\tidy_project_structure.py C:\path\to\paper-project
python .\paper-research-skill-v0.3.0\skills\paper-research-cn-core\scripts\deep_structure_audit.py C:\path\to\paper-project
```

确认目标路径无误后再执行：

```powershell
python .\paper-research-skill-v0.3.0\skills\paper-research-cn-core\scripts\tidy_project_structure.py C:\path\to\paper-project --apply
```

## 本地私有记忆

记忆目录默认在 `%USERPROFILE%\.codex\paper-research-cn-core\memory`。公开仓库不保存任何个人记忆。

```powershell
python .\paper-research-skill-v0.3.0\skills\paper-research-cn-core\scripts\memory_update.py --review
```
