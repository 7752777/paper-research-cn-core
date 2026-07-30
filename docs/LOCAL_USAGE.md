# Local Usage

这份指南面向希望把公开仓库中的六个 4.0 skill 安装到本机 Codex skills 目录的用户。

## 一键安装

```powershell
git clone https://github.com/7752777/paper-research-cn-core.git
cd paper-research-cn-core
powershell -ExecutionPolicy Bypass -File .\scripts\install_skills.ps1
```

安装目标：

- `paper-research-cn-core`：研究证据与文献分层
- `paper-manuscript-cn-core`：中文核心文稿、排版与渲染
- `paper-figures-cn-core`：图表、题注与图文一致性
- `paper-references-cn-core`：GB/T 7714 与官方元数据核验
- `paper-review-cn-core`：三轮独立审稿与修订闭环
- `paper-submission-cn-core`：投稿终审与发布门禁

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
python .\paper-research-skill-v0.4.0\install.py --target codex --dry-run
python .\paper-research-skill-v0.4.0\install.py --target codex --force
```

首先审阅 dry-run；只有确认六个目标 skill 正确后再使用 `--force` 覆盖同名旧版本。公开仓库不保存任何个人记忆、论文材料或下载全文。
