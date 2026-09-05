# -*- coding: utf-8 -*-
# 国内大宗商品七步测温框架 - 数据抓取脚本
# 数据源: 新浪期货接口 (实时行情 + 日K线)
import urllib.request
import json
import re
import time
import sys

HEADERS = {"Referer": "https://finance.sina.com.cn", "User-Agent": "Mozilla/5.0"}

# 各板块代表品种: 期限结构合约清单
CONTRACTS = {
    "UR":  ["2609", "2701", "2705", "2709"],   # 尿素(郑)
    "RB":  ["2610", "2701", "2705"],           # 螺纹钢(上)
    "CU":  ["2609", "2610", "2611", "2612", "2701", "2702"],  # 铜(上)
    "AL":  ["2610", "2611", "2612", "2701"],   # 铝(上)
    "AU":  ["2612", "2702", "2704", "2706"],   # 黄金(上)
    "AG":  ["2612", "2702", "2704", "2706"],   # 白银(上)
    "SC":  ["2609", "2610", "2611", "2612", "2701"],  # 原油(INE)
    "I":   ["2609", "2701", "2705"],           # 铁矿石(大)
    "M":   ["2609", "2701", "2703", "2705"],   # 豆粕(大)
    "C":   ["2611", "2701", "2703", "2705"],   # 玉米(大)
    "MA":  ["2609", "2701", "2705", "2709"],   # 甲醇(郑)
    "TA":  ["2609", "2701", "2705"],           # PTA(郑)
    "FG":  ["2609", "2701", "2705"],           # 玻璃(郑)
    "SA":  ["2609", "2701", "2705"],           # 纯碱(郑)
    "JM":  ["2609", "2701"],                   # 焦煤(大)
    "J":   ["2609", "2701"],                   # 焦炭(大)
    "Y":   ["2701", "2705"],                   # 豆油(大)
    "P":   ["2701", "2705"],                   # 棕榈油(大)
}

# 板块归属
SECTOR = {
    "UR": "化工", "MA": "化工", "TA": "化工", "FG": "建材(地产链)", "SA": "建材(地产链)",
    "RB": "黑色", "I": "黑色", "JM": "黑色", "J": "黑色",
    "CU": "有色", "AL": "有色",
    "AU": "贵金属", "AG": "贵金属",
    "SC": "能源",
    "M": "农产品", "C": "农产品", "Y": "农产品", "P": "农产品",
}


def fetch_quotes(codes):
    """批量获取实时行情"""
    out = {}
    for i in range(0, len(codes), 25):
        batch = codes[i:i + 25]
        url = "https://hq.sinajs.cn/list=" + ",".join("nf_" + c for c in batch)
        req = urllib.request.Request(url, headers=HEADERS)
        raw = urllib.request.urlopen(req, timeout=15).read().decode("gbk", "ignore")
        for line in raw.strip().split("\n"):
            m = re.match(r'var hq_str_nf_(\w+)="(.*)";', line.strip())
            if not m:
                continue
            code, payload = m.group(1), m.group(2)
            f = payload.split(",")
            if len(f) < 18 or not f[2]:
                continue
            try:
                out[code] = {
                    "name": f[0],
                    "open": float(f[2]), "high": float(f[3]), "low": float(f[4]),
                    "close": float(f[5]), "prev_settle": float(f[6]),
                    "last": float(f[9]),
                    "oi": float(f[13]), "vol": float(f[14]),
                    "date": f[17],
                }
            except (ValueError, IndexError):
                pass
        time.sleep(0.4)
    return out


def fetch_kline(code):
    """获取日K线(全部历史)"""
    url = ("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20t=/"
           "InnerFuturesNewService.getDailyKLine?symbol=" + code)
    req = urllib.request.Request(url, headers=HEADERS)
    raw = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
    m = re.search(r'\[.*\]', raw, re.S)
    if not m:
        return []
    data = json.loads(m.group(0))
    return [{"d": k["d"], "c": float(k["c"]), "s": float(k["s"]),
             "o": float(k["o"]), "h": float(k["h"]), "l": float(k["l"]),
             "p": float(k["p"])} for k in data]


def main():
    # 1. 实时行情: 全部合约
    all_codes = []
    for prod, months in CONTRACTS.items():
        for mo in months:
            all_codes.append(prod + mo)
    print("fetching quotes for %d contracts..." % len(all_codes))
    quotes = fetch_quotes(all_codes)
    print("got %d quotes" % len(quotes))

    # 2. 判断主力合约(持仓量最大)
    dominant = {}
    for prod, months in CONTRACTS.items():
        best, best_oi = None, -1
        for mo in months:
            c = prod + mo
            if c in quotes and quotes[c]["oi"] > best_oi:
                best, best_oi = c, quotes[c]["oi"]
        if best:
            dominant[prod] = {"contract": best, "oi": best_oi}

    # 3. 主力日K线 -> 20日涨跌幅
    print("fetching klines for dominant contracts...")
    kline_result = {}
    for prod, info in dominant.items():
        code = info["contract"]
        try:
            kl = fetch_kline(code)
            if len(kl) >= 22:
                last = kl[-1]
                base = kl[-21]
                chg20 = (last["c"] / base["c"] - 1) * 100
                chg5 = (last["c"] / kl[-6]["c"] - 1) * 100 if len(kl) >= 6 else None
                kline_result[prod] = {
                    "contract": code, "last_date": last["d"], "last_close": last["c"],
                    "chg_20d": round(chg20, 2), "chg_5d": round(chg5, 2),
                    "high_60d": max(k["h"] for k in kl[-60:]) if len(kl) >= 60 else None,
                    "low_60d": min(k["l"] for k in kl[-60:]) if len(kl) >= 60 else None,
                }
            elif kl:
                kline_result[prod] = {"contract": code, "last_date": kl[-1]["d"],
                                      "last_close": kl[-1]["c"], "note": "insufficient history"}
            print("  %s %s ok" % (prod, code))
        except Exception as e:
            print("  %s %s FAIL: %s" % (prod, code, e))
        time.sleep(0.3)

    # 4. 期限结构: 各合约最新价 vs 主力
    term_structure = {}
    for prod, months in CONTRACTS.items():
        rows = []
        dom = dominant.get(prod, {}).get("contract")
        for mo in months:
            c = prod + mo
            if c in quotes:
                q = quotes[c]
                rows.append({"contract": c, "last": q["last"], "settle": q["prev_settle"],
                             "oi": q["oi"], "date": q["date"],
                             "is_dominant": c == dom})
        if rows:
            term_structure[prod] = rows

    result = {
        "fetch_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "quotes": quotes,
        "dominant": dominant,
        "kline": kline_result,
        "term_structure": term_structure,
        "sector": SECTOR,
    }
    with open("/Users/shuhaihong/Documents/workbuddy/commodity_temp_data.json", "w") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=1)
    print("saved to commodity_temp_data.json")

    # 摘要打印
    print("\n=== 板块轮动(20日涨跌幅) ===")
    for prod, k in sorted(kline_result.items(), key=lambda x: -(x[1].get("chg_20d") or -999)):
        print("%-3s %-7s %-10s 20d: %6.2f%%  5d: %6.2f%%  [%s]" % (
            prod, k["contract"], k["last_date"], k.get("chg_20d", 0), k.get("chg_5d", 0),
            SECTOR.get(prod, "")))


if __name__ == "__main__":
    main()
