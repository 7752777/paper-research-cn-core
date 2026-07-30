# Maintainer Guide

本公开仓库不直接维护私人论文项目。所有可公开内容都应先在私有维护源中更新，再由同步脚本生成公开镜像。

## 同步前检查

```powershell
git status --short
$env:PYTHONUTF8='1'
python .\00_project_control\tools\write_skill_files.py
```

完整私人工作区出现 private blocker 是正常现象，因为那里可能有论文全文、投稿材料和私有项目。公开同步的关键是白名单是否仍然只包含可复用 skill 包和公开文档。

## 生成公开镜像

```powershell
python .\00_project_control\tools\sync_public_release.py
```

同步脚本会清空公开镜像目录中的非 `.git` 内容，然后复制白名单目录并写入公开 README、policy、docs 和 scripts。

## 公开仓库提交

```powershell
python .\scripts\release_gate.py --public-root .
git status --short
git diff
git add .
git commit -m "Sync public skill release"
git push origin main
```

## 不要这样做

- 不要把完整私人工作区直接切成 public。
- 不要把论文全文、下载清单、审稿材料或投稿包复制进公开仓库。
- 不要在公开仓库里长期手动维护会被同步脚本覆盖的核心文档。
- 不要把本地 memory、期刊账号、机构授权信息或私人偏好同步到公开仓库。
