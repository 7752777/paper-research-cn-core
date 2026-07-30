# 中文核心论文 Skill 5.0

`paper-research-skill-v0.5.0` 将 4.0 的六个工作阶段合并为唯一的 `paper-research-cn-core` skill。它仍覆盖 CNKI 证据、文稿渲染、图表、GB/T 7714、中文审稿和投稿终审，但只需安装和维护一个目录。

```powershell
python .\validate_package.py
python .\install.py --target codex --dry-run --prune-legacy
python .\install.py --target codex --force --prune-legacy
python .\verify_install.py --installed-root $env:USERPROFILE\.codex\skills
```

安装后调用：

```text
使用 $paper-research-cn-core 从检索与证据台账开始，完成中文核心论文的写作、图表、题录核验、中文三轮审稿和投稿终审。
```

公共发布只能包含此包、合成 fixture 和通用工具；真实论文、全文、台账、审稿意见、本地路径和账户信息必须留在私有工作区。
