#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""美股日报 · 外盘期货数据抓取（新浪 hf_ 接口）

用法:
  python3 fetch_us_market.py            # 抓全部符号
  python3 fetch_us_market.py hf_ES hf_NQ  # 指定符号

字段（新浪 hf_ 顺序）: 0现价 1买价 2卖价 3今开 4最高 5最低 6时间 7昨结 8昨收 9持仓 10成交量 11日期 12名称 13涨跌额
返回: 名称 / 现价 / 昨结 / 涨跌额 / 涨跌幅%
"""
import sys
import urllib.request

SYMBOLS = ['hf_CL', 'hf_GC', 'hf_SI', 'hf_HG', 'hf_NQ', 'hf_ES', 'hf_YM', 'hf_VX']
BASE = 'https://hq.sinajs.cn/list='


def fetch(symbols):
    url = BASE + ','.join(symbols)
    req = urllib.request.Request(url, headers={'Referer': 'https://finance.sina.com.cn'})
    raw = urllib.request.urlopen(req, timeout=10).read().decode('gbk', errors='ignore')
    for line in raw.strip().splitlines():
        if '=' not in line or '"' not in line:
            continue
        sym = line.split('=')[0].replace('var hq_str_', '').strip()
        body = line.split('"')[1]
        f = body.split(',')
        if len(f) < 13 or not f[0]:
            print(f'{sym:8s} 无数据')
            continue
        name = f[12]
        last = float(f[0])
        prev = float(f[8]) if f[8] else float(f[7])
        chg = last - prev
        pct = chg / prev * 100 if prev else 0.0
        arrow = '▲' if chg > 0 else ('▼' if chg < 0 else '=')
        print(f'{name:12s} {sym:6s} 现价 {last:>10.2f}  昨结 {prev:>10.2f}  {arrow} {chg:+.2f} ({pct:+.2f}%)  {f[6]}')


if __name__ == '__main__':
    syms = sys.argv[1:] or SYMBOLS
    fetch(syms)
