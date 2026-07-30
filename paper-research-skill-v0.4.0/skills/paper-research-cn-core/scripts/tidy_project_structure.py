from __future__ import annotations

import argparse
import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


STANDARD_DIRS = {
    "00_项目总览": "索引、审计报告、canonical 清单、整理 manifest、交接说明",
    "01_论文正文": "终稿、源稿、导出稿、投稿文本",
    "02_文献证据": "全文、元数据、检索协议、文献台账、综述笔记",
    "03_数据编码": "数据、codebook、编码台账、统计输出",
    "04_图表附件": "图表源文件、导出图片、补充材料",
    "05_审稿修订": "审稿意见、修订矩阵、作者回复",
    "06_投稿期刊": "目标期刊、格式规则、投稿包",
    "07_过程记录": "阶段日志、执行记录、交接说明",
    "08_工作区_旧结构": "历史工作区和旧目录镜像",
    "09_压缩包与备份": "必要压缩包和备份包",
}
ARCHIVE_SUFFIXES = {".zip", ".rar", ".7z"}
DATA_SUFFIXES = {".csv", ".xlsx", ".xls", ".json", ".sav", ".dta"}
MANUSCRIPT_SUFFIXES = {".doc", ".docx", ".md", ".qmd", ".pdf"}


@dataclass
class MoveRow:
    source: str
    target: str
    kind: str
    reason: str
    size_bytes: int
    action: str = "planned"


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def path_size(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def normalize(name: str) -> str:
    cleaned = " ".join(name.replace("　", " ").split())
    for char in '<>:"|?*':
        cleaned = cleaned.replace(char, "_")
    return cleaned or "未命名"


def classify(entry: Path, date: str) -> tuple[str | None, str]:
    name = entry.name
    low = name.casefold()
    suffix = entry.suffix.casefold()
    if name in STANDARD_DIRS or name == "99_archive" or name == ".git":
        return None, "standard"
    if low in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "node_modules"}:
        return f"99_archive/_cleanup_{date}/环境缓存/{name}", "cache/environment"
    if suffix in ARCHIVE_SUFFIXES:
        return f"09_压缩包与备份/{normalize(name)}", "archive/backup package"
    if any(term in name for term in ("审稿", "复审", "修订", "意见", "回复")):
        return f"05_审稿修订/{normalize(name)}", "review/revision"
    if any(term in name for term in ("投稿", "期刊", "格式", "封面信", "cover")):
        return f"06_投稿期刊/{normalize(name)}", "venue/submission"
    if any(term in name for term in ("图", "表", "figure", "table", "附件")) and suffix not in DATA_SUFFIXES:
        return f"04_图表附件/{normalize(name)}", "figure/table"
    if suffix in DATA_SUFFIXES or any(term in name for term in ("数据", "编码", "台账", "ledger", "codebook")):
        return f"03_数据编码/{normalize(name)}", "data/coding"
    if any(term in name for term in ("文献", "证据", "检索", "全文", "CNKI", "知网", "综述")):
        return f"02_文献证据/{normalize(name)}", "literature/evidence"
    if suffix in MANUSCRIPT_SUFFIXES and any(term in name for term in ("论文", "正文", "初稿", "终稿", "稿件", "manuscript", "draft")):
        return f"01_论文正文/{normalize(name)}", "manuscript"
    if low.startswith("readme") or any(term in name for term in ("说明", "记录", "计划", "日志", "交接")):
        return f"07_过程记录/{normalize(name)}", "process note"
    return f"08_工作区_旧结构/散落文件/{normalize(name)}", "unclassified active-root item"


def unique_target(root: Path, target_rel: str) -> Path:
    target = root / target_rel
    if not target.exists():
        return target
    for index in range(2, 10000):
        candidate = target.with_name(f"{target.stem}__dup{index}{target.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"cannot allocate target for {target}")


def collect(root: Path, date: str) -> list[MoveRow]:
    rows: list[MoveRow] = []
    for entry in sorted(root.iterdir(), key=lambda item: item.name):
        target_rel, reason = classify(entry, date)
        if target_rel is None:
            continue
        target = unique_target(root, target_rel)
        rows.append(MoveRow(rel(entry, root), rel(target, root), "dir" if entry.is_dir() else "file", reason, path_size(entry)))
    return rows


def ensure_dirs(root: Path) -> None:
    for dirname in STANDARD_DIRS:
        (root / dirname).mkdir(parents=True, exist_ok=True)
    (root / "99_archive").mkdir(parents=True, exist_ok=True)


def apply(root: Path, rows: list[MoveRow]) -> None:
    for row in rows:
        source = root / row.source
        target = root / row.target
        if not source.exists():
            row.action = "missing"
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            target = unique_target(root, row.target)
            row.target = rel(target, root)
        shutil.move(str(source), str(target))
        row.action = "moved"


def write_outputs(root: Path, rows: list[MoveRow], date: str) -> None:
    overview = root / "00_项目总览"
    overview.mkdir(parents=True, exist_ok=True)
    manifest = overview / f"PROJECT_TIDY_MANIFEST_{date}.csv"
    with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(MoveRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)
    dirs = "\n".join(f"| `{name}` | {purpose} |" for name, purpose in STANDARD_DIRS.items())
    moved = "\n".join(f"- `{row.source}` -> `{row.target}` ({row.reason}, {row.action})" for row in rows) or "- 本轮没有需要移动的顶层项目。"
    (root / "00_项目总览.md").write_text(
        f"# {root.name}\n\n本项目按统一论文工作区结构维护。整理策略为只归档、不删除、可追溯。\n\n## 标准目录\n\n| 目录 | 用途 |\n| --- | --- |\n{dirs}\n| `99_archive` | 过时、重复、临时、缓存、环境、探针材料 |\n\n## 本轮整理\n\n{moved}\n\n## 追溯\n\n- 整理日期：{date}\n- 清单：`00_项目总览/PROJECT_TIDY_MANIFEST_{date}.csv`\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--date", default=datetime.now().strftime("%Y%m%d"))
    args = parser.parse_args()

    root = args.project_root.resolve()
    if not root.exists() or not root.is_dir() or root.anchor == str(root):
        print(f"ERROR: unsafe project root: {root}")
        return 2
    rows = collect(root, args.date)
    if args.apply:
        ensure_dirs(root)
        apply(root, rows)
        write_outputs(root, rows, args.date)
    else:
        for row in rows:
            print(f"{row.source} -> {row.target} | {row.reason}")
    print(f"mode={'apply' if args.apply else 'dry-run'} entries={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
