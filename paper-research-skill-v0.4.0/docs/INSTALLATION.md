# 安装与验证

## 依赖

Python 3.10 或更高版本。DOCX/PDF 渲染需要 `python-docx` 与 `reportlab`；优先使用本机 LibreOffice，缺失时才使用本地 fallback。安装依赖：

```powershell
python -m pip install -r .\requirements.txt
```

当本机没有可用的中文字体时，为 fallback 设置一个 TrueType/OpenType 字体路径：

```powershell
$env:CN_CORE_CJK_FONT = "C:\\path\\to\\NotoSansCJKsc-Regular.otf"
```

## 安装到 Codex

在包根目录执行。先显示影响范围，再明确替换六个 4.0 skill：

```powershell
python .\install.py --target codex --dry-run
python .\install.py --target codex --force
python .\verify_install.py --installed-root "$env:USERPROFILE\.codex\skills"
```

安装器只会替换 `paper-research-cn-core` 与 `paper-review-cn-core`，并新增 manuscript、figure、reference 与 submission 四个 skill；不会修改其他已安装 skill。

## 包校验

```powershell
python .\validate_package.py
python -m unittest discover -s .\tests -v
```

发布前还应按 `RELEASE_GATE.md` 运行隐私扫描和公共发布门禁。
