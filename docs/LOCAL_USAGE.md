# Local Usage

这份指南面向希望把公开仓库中的单体 5.0 skill 安装到本机 Codex skills 目录的用户。

## 一键安装

```powershell
git clone https://github.com/7752777/paper-research-cn-core.git
cd paper-research-cn-core
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1
```

安装目标：

- `paper-research-cn-core`：检索、证据、写作、图表、题录、审稿与投稿终审。

## 在 Codex 中调用

写作流水线：

```text
使用 $paper-research-cn-core 帮我从选题开始，先设计 CNKI 检索式、关键词同义词表、核心期刊清单、纳排标准和全文下载清单，并在每个阶段结束时运行项目结构整理 checkpoint。
```

审稿流水线：

```text
使用 $paper-research-cn-core 对这篇论文做三轮独立审稿和投稿终审，输出问题清单、严重度、证据、修订建议和修订矩阵。
```

## 阶段整理

```powershell
python .\paper-research-skill-v0.5.0\install.py --target codex --dry-run --prune-legacy
python .\paper-research-skill-v0.5.0\install.py --target codex --force --prune-legacy
```

首先审阅 dry-run；只有确认一个主 skill 和五个精确旧目录正确后再使用 `--force`。公开仓库不保存任何个人记忆、论文材料或下载全文。
