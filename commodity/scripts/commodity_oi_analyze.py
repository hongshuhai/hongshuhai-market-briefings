# -*- coding: utf-8 -*-
# 持仓量变化分析: 主力合约持仓量20日趋势(框架第5步: 资金流入/流出)
import urllib.request
import json
import re
import time

HEADERS = {"Referer": "https://finance.sina.com.cn", "User-Agent": "Mozilla/5.0"}

# 统一取各品种主力合约(与第三章板块轮动/第四章期限结构同合约, 避免 RB2610 vs RB2701 20日涨幅打架)
TARGETS = ["UR2701", "RB2701", "CU2610", "AG2612", "AU2612", "SC2610",
           "MA2701", "TA2701", "I2701", "FG2701", "SA2701", "M2701", "JM2701", "J2701"]


def fetch_kline(code):
    url = ("https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20t=/"
           "InnerFuturesNewService.getDailyKLine?symbol=" + code)
    req = urllib.request.Request(url, headers=HEADERS)
    raw = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
    m = re.search(r'\[.*\]', raw, re.S)
    if not m:
        return []
    return json.loads(m.group(0))


result = {}
print("%-8s %-11s %10s %10s %10s %8s   %s" % ("合约", "日期", "收盘", "持仓now", "持仓20d前", "OI变化", "价格-持仓组合"))
print("-" * 95)
for code in TARGETS:
    try:
        kl = fetch_kline(code)
        if len(kl) < 22:
            continue
        last, base = kl[-1], kl[-21]
        px_chg = (float(last["c"]) / float(base["c"]) - 1) * 100
        oi_now, oi_base = float(last["p"]), float(base["p"])
        oi_chg = (oi_now / oi_base - 1) * 100 if oi_base > 0 else 0
        # 组合判断(同周期: 20日价格 × 20日持仓, 杜绝跨周期错配——禁止拿20日OI配单日涨跌)
        if px_chg > 1 and oi_chg > 5:
            combo = "增仓上涨(新多入场)"
        elif px_chg < -1 and oi_chg > 5:
            combo = "增仓下跌(新空入场)"
        elif px_chg > 1 and oi_chg < -5:
            combo = "减仓上涨(空头回补)"
        elif px_chg < -1 and oi_chg < -5:
            combo = "减仓下跌(多头离场)"
        elif abs(px_chg) <= 1 and oi_chg > 20:
            combo = "增仓对峙(巨量加仓·价格滞涨)"
        elif abs(px_chg) <= 1 and oi_chg < -20:
            combo = "减仓撤离(资金大幅离场·价格横盘)"
        elif abs(px_chg) <= 1 and oi_chg > 5:
            combo = "增仓滞涨(多空加码·价格未动)"
        elif abs(px_chg) <= 1 and oi_chg < -5:
            combo = "减仓观望(资金离场·价格未动)"
        else:
            combo = "中性(量价平稳)"
        result[code] = {"date": last["d"], "close": float(last["c"]),
                        "oi_now": oi_now, "oi_base": oi_base,
                        "px_chg_20d": round(px_chg, 2), "oi_chg_20d": round(oi_chg, 2),
                        "combo": combo}
        print("%-8s %-11s %10.0f %10.0f %10.0f %+7.1f%%   %s" % (
            code, last["d"], float(last["c"]), oi_now, oi_base, oi_chg, combo))
        time.sleep(0.3)
    except Exception as e:
        print("%-8s FAIL: %s" % (code, e))

with open("/Users/shuhaihong/Documents/workbuddy/commodity_oi_data.json", "w") as fp:
    json.dump(result, fp, ensure_ascii=False, indent=1)
print("\nsaved: commodity_oi_data.json")
