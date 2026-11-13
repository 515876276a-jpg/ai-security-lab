import re, sys
from pathlib import Path
EXTS, SKIP, OUT = {".py", ".md"}, {"__pycache__", ".git", ".codebuddy", ".venv", "venv", "node_modules"}, "汇总表.md"

def read_text(p):  # UTF-8(BOM) 优先，回退 GBK，换行统一为 LF
    b = p.read_bytes()
    for e in ("utf-8-sig", "gbk"):
        try: return b.decode(e).replace("\r\n", "\n").replace("\r", "\n")
        except UnicodeDecodeError: continue
    return None

def week(rel):  # 路径里的 W2 / C1 等周目录，找不到归「未分周」
    return next((x.upper() for x in rel.parts[:-1] if re.fullmatch(r"[A-Za-z]?\d+", x)), "未分周")

def scan(root, exclude):  # 返回 (周, 文件, 行数, 字符数)
    rows = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EXTS: continue
        if any(x in SKIP for x in p.parts) or p.resolve() == exclude: continue
        t = read_text(p)
        if t is None: continue
        rel = p.relative_to(root)
        rows.append((week(rel), rel.as_posix(), len(t.splitlines()), len(t)))
    return rows

def render(rows, root, out):
    groups = {}
    for r in rows: groups.setdefault(r[0], []).append(r)
    key = lambda n: (0, int(re.sub(r"\D", "", n)), n) if re.fullmatch(r"[A-Za-z]?\d+", n) else (1, 0, n)
    groups = {k: groups[k] for k in sorted(groups, key=key)}
    L = ["# 目录统计汇总", "", f"- 扫描根目录：`{root.as_posix()}`",
         "- 范围：`.py`、`.md`，跳过缓存目录；口径：换行统一 LF，行数 splitlines，字符数含换行不含 BOM",
         f"- 结果文件 `{out.name}` 自身不计入统计", "", "## 按周汇总", "",
         "| 周/分组 | 文件数 | 行数合计 | 字符数合计 |", "| --- | ---: | ---: | ---: |"]
    for k, v in groups.items(): L.append(f"| {k} | {len(v)} | {sum(r[2] for r in v)} | {sum(r[3] for r in v)} |")
    L.append(f"| **总计** | **{len(rows)}** | **{sum(r[2] for r in rows)}** | **{sum(r[3] for r in rows)}** |")
    L += ["", "## 文件明细", "", "| 周/分组 | 文件 | 行数 | 字符数 |", "| --- | --- | ---: | ---: |"]
    for k, v in groups.items(): L += [f"| {k} | `{r[1]}` | {r[2]} | {r[3]} |" for r in v]
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    root = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else here.parent.parent
    if not root.is_dir(): raise SystemExit(f"目录不存在：{root}")
    out = here / OUT
    rows = scan(root, out.resolve())
    out.write_text(render(rows, root, out), encoding="utf-8")
    print(f"已统计 {len(rows)} 个文件，结果写入 {out}")
