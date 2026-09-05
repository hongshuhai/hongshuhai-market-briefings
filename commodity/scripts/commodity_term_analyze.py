# -*- coding: utf-8 -*-
# 期限结构分析: 升贴水 + 年化展期收益率
import json

with open("/Users/shuhaihong/Documents/workbuddy/commodity_temp_data.json") as fp:
    data = json.load(fp)

ts = data["term_structure"]
dom = data["dominant"]

# 合约到期月份差(用于年化)
def month_diff(m1, m2):
    y1, mm1 = int(m1[:2]), int(m1[2:])
    y2, mm2 = int(m2[:2]), int(m2[2:])
    return (y2 - y1) * 12 + (mm2 - mm1)

print("=" * 88)
print("%-4s %-8s %-26s %-10s %-12s %s" % ("品种", "主力", "合约链(价格)", "近远月差", "年化展期收益", "结构"))
print("=" * 88)

summary = {}
for prod, rows in ts.items():
    # 价格口径: 优先last(最新价), 上期所品种夜盘后last=0则用settle(昨结算价)
    for r in rows:
        r["px"] = r["last"] if r["last"] > 0 else r["settle"]
    rows = [r for r in rows if r["px"] > 0]
    if len(rows) < 2:
        continue
    # 按合约月份排序
    rows_sorted = sorted(rows, key=lambda r: r["contract"])
    chain = " | ".join("%s:%.0f" % (r["contract"][-4:], r["px"]) for r in rows_sorted)
    # 主力 vs 下一合约(展期收益)
    dom_c = dom.get(prod, {}).get("contract")
    prices = {r["contract"]: r for r in rows_sorted}
    keys = [r["contract"] for r in rows_sorted]
    if dom_c in keys and keys.index(dom_c) < len(keys) - 1:
        next_c = keys[keys.index(dom_c) + 1]
        p_dom = prices[dom_c]["px"]
        p_next = prices[next_c]["px"]
        spread = p_dom - p_next
        md = month_diff(dom_c[-4:], next_c[-4:])
        roll_yield = (p_dom / p_next - 1) * 100 * (12.0 / md) if md > 0 else None
        structure = "贴水Back" if spread > 0 else "升水Contango"
        summary[prod] = {
            "dominant": dom_c, "next": next_c, "spread": round(spread, 1),
            "roll_yield": round(roll_yield, 2) if roll_yield is not None else None,
            "structure": structure, "chain": chain,
        }
        print("%-4s %-8s %-26s %-10s %-12s %s" % (
            prod, dom_c, chain[:26], "%+.1f" % spread,
            "%+.2f%%" % roll_yield if roll_yield is not None else "N/A", structure))

print()
print("=" * 88)
print("尿素(UR)期限结构明细:")
print("=" * 88)
for r in sorted(ts.get("UR", []), key=lambda x: x["contract"]):
    print("  UR%s  最新:%8.1f  昨结算:%8.1f  持仓:%8.0f  %s" % (
        r["contract"][-4:], r["last"], r["settle"], r["oi"],
        "<== 主力" if r["is_dominant"] else ""))

print()
print("重点品种近月贴水/升水幅度(主力-次主力, 相对%):")
focus = ["UR", "RB", "CU", "AU", "AG", "SC", "I", "MA", "TA", "M", "FG", "SA", "JM", "J"]
for p in focus:
    if p in summary:
        s = summary[p]
        base_px = None
        for r in ts.get(p, []):
            if r["contract"] == s["dominant"]:
                base_px = r["last"] if r["last"] > 0 else r["settle"]
        if base_px:
            pct = s["spread"] / base_px * 100
            print("  %-3s 主力%-7s → 次主%-7s 价差%+8.1f (%+.2f%%)  年化%+.2f%%  %s" % (
                p, s["dominant"], s["next"], s["spread"], pct, s["roll_yield"], s["structure"]))

with open("/Users/shuhaihong/Documents/workbuddy/commodity_term_structure.json", "w") as fp:
    json.dump(summary, fp, ensure_ascii=False, indent=1)
print("\nsaved: commodity_term_structure.json")
