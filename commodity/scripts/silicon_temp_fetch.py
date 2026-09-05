# -*- coding: utf-8 -*-
"""硅产业链（工业硅SI/多晶硅PS）七步测温数据抓取 - 2026-08-26"""
import json, time, urllib.request

def http_get(url):
    req = urllib.request.Request(url, headers={
        "Referer": "https://finance.sina.com.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("gbk", errors="ignore")

# 广期所: 工业硅SI 多晶硅PS (2609-2706)
months = ["2609","2610","2611","2612","2701","2702","2703","2704","2705","2706","2707","2708"]
contracts = ["SI"+m for m in months] + ["PS"+m for m in months]

# 1. 全合约实时行情 (新浪, 每批20个)
quotes = {}
for i in range(0, len(contracts), 20):
    batch = contracts[i:i+20]
    url = "https://hq.sinajs.cn/list=" + ",".join("nf_"+c for c in batch)
    try:
        text = http_get(url)
        for line in text.strip().split("\n"):
            if '="' not in line: continue
            code = line.split("=")[0].split("_")[-1]
            f = line.split('="')[1].rstrip('";').split(",")
            if len(f) < 15 or float(f[8] or 0) == 0: continue
            quotes[code] = {
                "name": f[0], "time": f[1],
                "open": float(f[2]), "high": float(f[3]), "low": float(f[4]),
                "prev_close": float(f[5]),
                "last": float(f[8]),
                "settle": float(f[9] or 0),          # 今结算(盘中为0)
                "prev_settle": float(f[10] or 0),    # 昨结算
                "oi": float(f[13] or 0),             # 持仓量
                "volume": float(f[14] or 0),         # 成交量
                "date": f[17] if len(f) > 17 else ""
            }
    except Exception as e:
        print("batch fail:", e)
    time.sleep(0.5)

print("=== 行情 (%d 个有效合约) ===" % len(quotes))
for prod in ["SI","PS"]:
    print("\n--- %s ---" % ("工业硅" if prod=="SI" else "多晶硅"))
    rows = [(c, q) for c, q in quotes.items() if c.startswith(prod)]
    rows.sort(key=lambda x: -x[1]["oi"])
    for c, q in rows:
        print("  %-7s 持仓%8.0f  成交%8.0f  最新%9.0f  昨结%9.0f" % (
            c, q["oi"], q["volume"], q["last"], q["prev_settle"]))

# 2. 主力合约日K线(含持仓) - 取持仓量最大的合约
klines = {}
for prod in ["SI","PS"]:
    dom = max([c for c in quotes if c.startswith(prod)], key=lambda c: quotes[c]["oi"])
    url = ("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20t=/"
           "InnerFuturesNewService.getDailyKLine?symbol=" + dom)
    try:
        text = http_get(url)
        raw = text.split("=",1)[1].strip().rstrip(";")
        data = json.loads(raw)
        klines[prod] = {"dominant": dom, "kline": data}
        print("\n%s 主力=%s, K线%d根, 最新: %s 收%s 持仓%s" % (
            prod, dom, len(data), data[-1]["d"], data[-1]["c"], data[-1]["p"]))
    except Exception as e:
        print(prod, "kline fail:", e)

with open("/Users/shuhaihong/Documents/workbuddy/silicon_data.json","w") as f:
    json.dump({"quotes": quotes, "klines": klines, "fetched": "2026-08-26"}, f, ensure_ascii=False, indent=1)
print("\nsaved -> silicon_data.json")
