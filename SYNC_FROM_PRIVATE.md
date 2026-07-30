# Sync From Private Maintenance Source

本公开仓库由维护者的私有工作区生成。公开仓库只保留可复用 skill、agent 描述和公开文档；不保留私人论文、全文证据、投稿材料或账号痕迹。

推荐维护流程：

```powershell
# 在私有维护源中：
$env:PYTHONUTF8='1'
python .\00_project_control\tools\write_skill_files.py
python .\00_project_control\tools\sync_public_release.py

# 在公开镜像中：
python .\scripts\release_gate.py --public-root .
git status --short
git add .
git commit -m "Sync public skill release"
git push origin main
```

如果公开仓库已有人工改动，先在公开仓库内运行 `git status` 和 `git diff`。同步脚本会重建公开镜像目录中的非 `.git` 内容，因此需要长期保留的公开文档改动应先写回维护源。
