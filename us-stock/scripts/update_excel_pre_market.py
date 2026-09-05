"""市场温度7步扫描 Excel — R12 (X=2026-08-26) 最小化更新
本盘前任务仅覆盖: A/I/K/M/N/O/P/AI/AL/AM/AN/AO 列
绝对不覆盖:B/C/D/J/R/T/V/X/Z/AG 等昨夜 close 数据列（留给 8/27 07:30 盘后任务写 X 日 close）
公式列(E/F/G/H/L/Q/S/U/W/Y/AA/AC/AE/AH) 不覆盖, 由 openpyxl 自动保留
"""
import openpyxl
from openpyxl import load_workbook

XLSX = '/Users/shuhaihong/Documents/workbuddy/市场温度7步扫描.xlsx'
SHEET = '每日数据'

wb = load_workbook(XLSX, data_only=False)
ws = wb[SHEET]

# 找到 X=2026-08-26 对应行;不存在则新加
x_date = '2026-08-26'
target_row = None
for r in range(4, ws.max_row + 1):
    if ws.cell(row=r, column=1).value == x_date:
        target_row = r
        break

if target_row is None:
    # 新加一行: 找 A 列为 None 的第一空行(不要用 max_row+1,因为公式模板行也算 max_row)
    target_row = None
    for r in range(4, ws.max_row + 1):
        if ws.cell(row=r, column=1).value is None:
            target_row = r
            break
    if target_row is None:
        target_row = ws.max_row + 1
    print(f'R12-区域无 X 行,新增 R{target_row} for X={x_date}')
else:
    print(f'找到现成行 R{target_row} for X={x_date}')

r = target_row

# ---- 强制覆盖列 ----
# A: 日期
ws.cell(row=r, column=1).value = x_date

# I: 曲线变动（盘前曲线评论）
ws.cell(row=r, column=9).value = (
    '8/26 7:30AM EDT 盘前:30Y -4bp 至5.181% 领跌,长端鸽派 term premium unwind;2s10s微熊平'
)

# K: 道指日涨跌(盘前期货变化) — YM +0.07%
ws.cell(row=r, column=11).value = 0.0007

# M: 纳指日涨跌(盘前期货变化) — NQ -0.20%
ws.cell(row=r, column=13).value = -0.0020

# N: 罗素日涨跌(盘前期货变化) — RTY ≈0 (-0.01%)
ws.cell(row=r, column=14).value = -0.0001

# O: 领涨指数(盘前 leader)
ws.cell(row=r, column=15).value = (
    '8/26盘前防御领涨:YM+0.07% > ES-0.07% > NQ-0.20% > RTY≈0;油价续-2.7%鸽小盘+金高位获利兑现'
)

# P: WTI收盘(盘前期货值) — 改为盘前方向
ws.cell(row=r, column=16).value = 80.15

# AI: VIX9D(盘前估算)
ws.cell(row=r, column=35).value = 13.0

# AL: VIX曲线形态(盘前观察)
ws.cell(row=r, column=38).value = (
    'contango(9D 13.0<现 15.49<3M~18.2<1Y 22.61);9D 较昨13.45再unwind(前端hedge再撤光),远端1Y仍溢价'
)

# AM: 未来一周关键事件(盘前已知)
ws.cell(row=r, column=39).value = (
    '今晚(8/26)8:30ET:7月PCE/核心PCE+Q2 GDP二次估值+耐用品(主菜事件,核心PCE预期2.9%YoY);'
    '盘后NVIDIA/CRM/CRWD/HPQ/WDAY/OKTA财报;'
    '8/28(五)22:00 GMT+8 Warsh Jackson Hole首秀(上任后首次主旨演讲)'
)

# AN: 事件是否被对冲(盘前观察)
ws.cell(row=r, column=40).value = (
    '部分(VIX9D由昨13.45再unwind至13.0=前端hedge再撤;1Y 22.61远端仍高位=尾部hedge留)'
)

# AO: 综合温度·一句话(30-50字 战术版,07:30 盘后任务会用 100-200 字战略版覆盖)
ws.cell(row=r, column=41).value = (
    '🟡mixed(鸽cost/small-cap防御):①VIX9D≈13.0低位延续 ②US30Y-4bp至5.18% ③RTY/SPX~0.86。'
    'PCE≤2.9%则上膛NQ多,否则空仓等闭市再看NVDA。'
)

# 保存
wb.save(XLSX)
print(f'✅ 已更新 R{r}: A/I/K/M/N/O/P/AI/AL/AM/AN/AO ({x_date})')
print(f'公式列自动保留: E/F/G/H/L/Q/S/U/W/Y/AA/AC/AE/AH = 11 个公式, 盘后任务会写 X close 时一并触发更新')
