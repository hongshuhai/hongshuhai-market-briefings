"""更新 Excel · 每日数据 R11 = 2026-08-25 现金收盘完整版

数据来源：8/25 收盘 · 多源交叉验证（中金、新华社、StreetStats、NextFin、新浪、华尔街见闻、Tencent）
注意：R10 已是 8/25 盘前快照（沿用 8/24 settled），R11 = 8/25 cash close 真实收盘版
公式列（E/F/G/H/L/Q/S/U/W/Y/AA/AC/AE/AH）保留不覆盖
"""
import openpyxl

XLSX = '/Users/shuhaihong/Documents/workbuddy/市场温度7步扫描.xlsx'
ROW = 11

wb = openpyxl.load_workbook(XLSX, data_only=False)
ws = wb['每日数据']

# === 数据列（按 R3 表头列名写）===
ws.cell(row=ROW, column=1, value='2026-08-25')                    # A 日期
ws.cell(row=ROW, column=2, value=0.04181)                         # B 2Y（多源均值）
ws.cell(row=ROW, column=3, value=0.04630)                         # C 10Y
ws.cell(row=ROW, column=4, value=0.05167)                         # D 30Y
# E/F/G/H 是公式列（bp 变动），不要覆盖
ws.cell(row=ROW, column=9, value='整体下移+微熊平(10Y领跌-6.6bp/30Y-5.8bp/2Y-5.2bp;2s10s -1.7bp至44.15bp收窄走平)')   # I 曲线变动
ws.cell(row=ROW, column=10, value=7677.28)                        # J 标普500
ws.cell(row=ROW, column=11, value=0.0030)                         # K 道指日涨跌
# L 公式列
ws.cell(row=ROW, column=13, value=0.0066)                         # M 纳指日涨跌
ws.cell(row=ROW, column=14, value=0.0050)                         # N 罗素日涨跌
ws.cell(row=ROW, column=15, value='纳指领涨(+0.66%);科技XLK +0.96%/通信服务XLC +0.77%/医疗XLV +0.34%;半导体/光通信/存储暴涨(Lumentum+6.67%/AMD+4.91%/MRVL+4.84%/NVDA+2.19%止七连跌/MU+2.48%/SK+2.68%/费半+1.44%);能源XLE -1.65% / 必消XLP -1.06%领跌（地缘缓和+油价暴跌驱动）')   # O 领涨指数
ws.cell(row=ROW, column=16, value=82.36)                          # P WTI收盘
# Q 公式列
ws.cell(row=ROW, column=18, value=88.58)                          # R 布伦特收盘
# S 公式列
ws.cell(row=ROW, column=20, value=4715.90)                        # T COMEX金
# U 公式列
ws.cell(row=ROW, column=22, value=68.63)                          # V COMEX银
# W 公式列
ws.cell(row=ROW, column=24, value=14324.5)                        # X LME铜(美元/吨)
# Y 公式列
ws.cell(row=ROW, column=26, value=524.25)                         # Z CBOT玉米(美分/蒲)
# AA 公式列
ws.cell(row=ROW, column=28, value=1238.75)                        # AB CBOT大豆
# AC 公式列
ws.cell(row=ROW, column=30, value=704.50)                         # AD CBOT小麦
# AE 公式列
ws.cell(row=ROW, column=32, value='谷物全线上行(+1.70%/+1.18%/+0.71%);玉米连续5日创3年新高(Pro Farmer巡查产量低于USDA预期)+豆-玉背离收敛;最大单日+1.70%未超3%阈值')   # AF 谷物异动
ws.cell(row=ROW, column=33, value=15.46)                          # AG VIX
# AH 公式列
ws.cell(row=ROW, column=35, value=13.45)                          # AI VIX9D
ws.cell(row=ROW, column=36, value=18.21)                          # AJ VIX3M
ws.cell(row=ROW, column=37, value=22.61)                          # AK VIX1Y
ws.cell(row=ROW, column=38, value='contango(9D13.45<现15.46<3M18.21<6M20.84<1Y22.61);8/24 +11.84%异动已大幅unwind(-4.41%);曲线整体位移方向：前端下/后端稳(1Y -0.35%几乎没动),事件对冲在前端撤、远端hedge仍在')  # AL VIX曲线形态
ws.cell(row=ROW, column=39, value='8/26(三)8:30 ET Q2 GDP二次估值+7月PCE/核心PCE(决定降息空间)+耐用品订单+个人收支;盘后 NVDA Q2 FY27(共识rev $91.9B/EPS $2.08/隐含$324.5B市值波动)+CRM+CRWD+HPQ;DKS 8/25盘前已大涨带动零售;8/27(四)Jackson Hole开幕+初请失业金+Pending Home Sales;盘后 MRVL/ADSK/BILI/DG/DLTR/WDAY;8/28(五)10AM ET Warsh Jackson Hole首秀+非农基准修正初值+密歇根信心终值+东京 8月CPI')   # AM 未来一周关键事件
ws.cell(row=ROW, column=40, value='部分(现15.46/9D13.45大幅unwind/1Y 22.61 仍高出中位19.5=+3.1pts;前端hedge撤了、后端hedge留着)')   # AN 对冲状态

# === AO 综合温度·一句话（100-200字战略评语）===
ws.cell(row=ROW, column=41, value=(
    '昨夜主轴=地缘缓和+鸽派重定价+risk-on三连击:'
    '双油暴跌 WTI -3.12%/Brent -3.89%(年内最大单日、地缘溢价回吐+库存三连增+获利了结)、'
    '美债全线走低 10Y -6.6bp/30Y -5.8bp/2Y -5.2bp(10Y领跌、2s10s 44.15bp微熊平)→'
    '风险偏好全开、纳指 +0.66%领涨、芯片股(AMD+4.91%/MRVL+4.84%/Lumentum+6.67%/NVDA+2.19%止七连跌)/光通信/storage/AI全线反弹、'
    '板块从8/24防御领涨反转成成长领涨;'
    '信用端温和配合:JNK 96.20 +0.26%/盘后96.14 -0.06%量稀/HYG +0.28%/TLT +1.10%=risk-on+主权鸽派同现的carry trade环境;'
    'VIX曲线整体位移:现15.46 -2.46%/9D13.45 -4.41%大幅unwind/1Y22.61 -0.35%几乎没动=前端hedge撤、后端hedge还在,留有二次对冲余地;'
    '明日亚盘3条绕路:①避免追高NVDA财报前抢筹 ②Brent 8/25盘后已破86(累计-6.6%)→亚盘能源股进一步回落空间 ③黄金4715.9/现货4658.9接近花旗$4800目标位、不追高但事件hedge价值上升;'
    '底仓逻辑:carry trade+期权sweep重置的反弹、不是趋势性risk-off setup,但8/26 PCE+8/28 Warsh三连事件未到、仓位上限7成。'
))

# === TLT 信用补充信息放在 AF 后，但模板没有此列，跳过；用 AO 已含 ===

wb.save(XLSX)
print(f"Excel R11 已写入 8/25 cash close 数据: {XLSX}")

# 校验
wb2 = openpyxl.load_workbook(XLSX, data_only=False)
ws2 = wb2['每日数据']
print("\n=== 校验 R11 数据 ===")
for col, label in [(1,'A日期'),(2,'B 2Y'),(3,'C 10Y'),(4,'D 30Y'),(10,'J SPX'),
                   (11,'K DJI'),(13,'M NDX'),(14,'N RUT'),(15,'O 领涨'),
                   (16,'P WTI'),(18,'R Brent'),(20,'T Gold'),(22,'V Silver'),(24,'X Copper'),
                   (26,'Z Corn'),(28,'AB Bean'),(30,'AD Wheat'),(32,'AF 异动'),
                   (33,'AG VIX'),(35,'AI VIX9D'),(36,'AJ VIX3M'),(37,'AK VIX1Y'),
                   (38,'AL 曲线'),(39,'AM 事件'),(40,'AN 对冲'),(41,'AO 总结')]:
    v = ws2.cell(row=ROW, column=col).value
    print(f"  {label}: {str(v)[:120] if v else 'EMPTY'}")
