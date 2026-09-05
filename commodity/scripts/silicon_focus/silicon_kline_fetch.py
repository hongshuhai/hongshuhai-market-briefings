# -*- coding: utf-8 -*-
"""硅产业链 K线抓取 + 期限结构分析 - 2026-08-26"""
import json, subprocess

def http_get(url):
    r = subprocess.run(["curl", "-s", "--max-time", "15",
                        "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                        "-H", "Referer: https://quote.eastmoney.com/", url],
                       capture_output=True, text=True, timeout=25)
    return r.stdout

# 东财 push2his, 广期所 secid 前缀 225
def get_kline(code, lmt=120):
    url = ("https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=225.%s"
           "&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58"
           "&klt=101&fqt=0&end=20500101&lmt=%d" % (code, lmt))
    d = json.loads(http_get(url))
    rows = []
    for line in d["data"]["klines"]:
        f = line.split(",")
        rows.append({"date": f[0], "open": float(f[1]), "close": float(f[2]),
                     "high": float(f[3]), "low": float(f[4]),
                     "vol": float(f[5]), "oi": float(f[6]) if len(f) > 6 and f[6] else 0})
    return rows

out = {}
for code in ["SI2611", "PS2611"]:
    try:
        k = get_kline(code)
        out[code] = k
        c_now, c_20 = k[-1]["close"], k[-21]["close"]
        c_60 = k[-61]["close"] if len(k) > 60 else k[0]["close"]
        oi_now, oi_20 = k[-1]["oi"], k[-21]["oi"]
        print("=== %s (%d根) 最新%s 收%.0f ===" % (code, len(k), k[-1]["date"], c_now))
        print("  20日涨跌: %+.2f%% (%.0f -> %.0f)" % ((c_now/c_20-1)*100, c_20, c_now))
        print("  60日涨跌: %+.2f%%" % ((c_now/c_60-1)*100))
        print("  持仓: 20日前%.0f -> 现%.0f (%+.1f%%)" % (oi_20, oi_now, (oi_now/oi_20-1)*100))
        # 近10日逐日: 收盘价 + 持仓
        print("  近10日 (日期 收盘 持仓):")
        for r in k[-10:]:
            print("    %s  %8.0f  %9.0f" % (r["date"], r["close"], r["oi"]))
    except Exception as e:
        print(code, "fail:", e)

with open("/Users/shuhaihong/Documents/workbuddy/silicon_kline.json", "w") as f:
    json.dump(out, f)
print("\nsaved -> silicon_kline.json")
