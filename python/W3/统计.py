import csv, io, re, sys
HINTS = ("费用", "合计", "总额", "amount", "value")
def _num(v):
    t = re.sub(r"[,\s，元￥¥]", "", str("" if v is None else v))
    return float(t) if re.fullmatch(r"-?\d+(\.\d+)?", t) else None
def _dict_rows(rows):
    buf = io.StringIO(); csv.writer(buf).writerows(rows); buf.seek(0)
    return list(csv.DictReader(buf))
def _load(path, group_col, amount_col):
    """兼容普通明细表与 Excel 分区块报销单，先拍平再交给 DictReader。"""
    with open(path, encoding="utf-8-sig", newline="") as f:
        raw = list(csv.reader(f))
    hints = (amount_col,) + HINTS
    out, cat, amt, gidx, didx, ncols = [[group_col, "项目", "日期", amount_col]], "", None, None, 0, 0
    for row in raw:
        c = [x.strip() for x in row]
        if not any(c): continue                                # 空行
        if any("金额" in x or x in hints for x in c):          # 表头行：定位金额 / 分组 / 日期列
            amt = next(j for j, x in enumerate(c) if "金额" in x or x in hints)
            gidx = next((j for j, x in enumerate(c) if x and (group_col in x or x in group_col)), None)
            didx, ncols, cat = c.index("日期") if "日期" in c else 0, len(c), cat or c[0]
            continue
        if amt is None: continue                             # 表名、部门、出差事由等说明行
        if sum(bool(x) for x in c) == 1 and gidx is None:
            cat = c[0].replace(" ", ""); continue            # 区块标题：住 宿 费 / 餐 费
        extra = max(0, len(c) - ncols)                       # 无引号的 "1,234元" 被拆列
        v = ",".join(c[amt:amt + 1 + extra]) if extra else (c[amt:] or [""])[0]
        if _num(v) is None: continue
        key = ((c[gidx:] or [cat])[0] if gidx is not None else cat) or "未填写"
        out.append([key, (c[:1] or [""])[0], (c[didx:] or [""])[0], v])
    return _dict_rows(out)
def summarize(path, group_col="类别", amount_col="金额"):
    """按 group_col 分组，返回按合计降序的列表；函数内不 print。"""
    groups = {}
    for r in _load(path, group_col, amount_col):
        v = _num(r.get(amount_col))
        if v is not None:
            groups.setdefault(r.get(group_col) or "未填写", []).append(v)
    total = sum(sum(v) for v in groups.values())
    return sorted([{"分组": k, "笔数": len(v), "合计": round(sum(v), 2), "均值": round(sum(v)/len(v), 2),
                    "最大单笔": max(v), "占比": round(sum(v)/total*100, 2) if total else 0.0}
                   for k, v in groups.items()], key=lambda g: g["合计"], reverse=True)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else input("请输入 CSV 文件路径：").strip().strip('"')
    if not path: raise SystemExit("用法：python 统计.py <CSV路径> [分组列名] [金额列名]")
    data = summarize(path, sys.argv[2] if len(sys.argv) > 2 else "类别", sys.argv[3] if len(sys.argv) > 3 else "金额")
    for g in data: print(f"{g['分组']} {g['笔数']} 笔、合计 {g['合计']:,.2f} 元、均值 {g['均值']:,.2f} 元、最大单笔 {g['最大单笔']:,.2f} 元、占比 {g['占比']}%")
    print(f"总计 {sum(g['笔数'] for g in data)} 笔、合计 {sum(g['合计'] for g in data):,.2f} 元")
    if data: print(f"占比最高：{data[0]['分组']}（{data[0]['占比']}%）")
