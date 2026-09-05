# us-stock/ — 美股日报模块

> 美股盘前战略版（含昨夜 X-1 完整复盘 + 今夜 X 开盘开关），每日 19:45 GMT+8 触发。

## 快速开始

```bash
cd scripts/

# 1. 抓隔夜外盘期货
python3 fetch_us_market.py
# → us_market_snapshot.json

# 2. 编辑 generate_pre_market.py 顶部的 T / STEP 字典
#    T 字典: 昨夜 X-1 三指数收盘 + 利率 + VIX + 商品 + 信用
#    STEP 字典: 七步速览迷你版

# 3. 生成报告
python3 generate_pre_market.py
# 输出: ../examples/us_pre_market_2026-09-04.html

# 4. 更新 Excel 模板（市场温度7步扫描.xlsx）
python3 update_excel_pre_market.py

# 5. 发送（可选）
python3 send_report.py --title 美股盘前 --date 2026-09-04 --html ../examples/us_pre_market_2026-09-04.html
```

## 报告结构（合并版，45-60 KB）

1. **顶头条**：一句话今日美股开盘背景
2. **昨夜 X-1 完整战略复盘**：
   - 三大指数收盘 + 涨跌归因
   - 利率曲线：10Y/2Y/30Y 收盘 + bp 变动
   - 商品链：WTI/布伦特/COMEX金/白银/LME铜/谷物
   - 信用端：JNK/HYG/TLT
   - 亚欧市场：恒指/日经/欧股
   - **对账表**：盘前预期 vs 实际
   - **7 步完整温度表**
3. **今夜 X 开盘开关**：
   - **3 触发器**：① VIX9D ② US30Y ③ RTY vs SPX 期货相对强弱
   - **7 步速览迷你版**
   - **战术指令**：AO 列 30-50 字
   - **今夜日历**：数据/事件
   - **亚盘建议**

## 文件清单

| 文件 | 行数 | 说明 |
|---|---|---|
| `fetch_us_market.py` | 43 | 抓隔夜外盘期货（hf_CL/hf_GC/hf_SI/hf_HG 等） |
| `generate_pre_market.py` | ~420 | **盘前报告生成**（主脚本） |
| `generate_market_post.py` | ~330 | 盘后复盘脚本（PAUSED 状态保留） |
| `update_excel_pre_market.py` | 93 | 更新 Excel 盘前列 |
| `update_xlsx_r11.py` | 83 | Excel 收盘完整版（盘后补全） |
| `send_report.py` | 78 | SMTP 发送（Keychain 取授权码） |
| `templates/market_temp_7step_template.xlsx` | — | 7 步扫描 Excel 模板 |

## 七步 Excel 列映射

| 步 | 指标 | Excel 收盘列 | Excel 盘前列 |
|---|---|---|---|
| 1 | 利率曲线 2Y/10Y/30Y | B/C/D | — |
| 2 | 指数结构 SPX/DJI/IXIC/RTY | J/K/M/N/O | K/M/N/O |
| 3 | 原油 WTI/布伦特 | P/R | — |
| 4 | 黄金/白银/铜 | T/U/V/X | — |
| 5 | VIX 衍生品 | Z/AA/AC/AE/AH | — |
| 6 | 估值 | AG | — |
| 7 | 日历/事件 | AI/AL/AM/AN/AO | AI/AL/AM/AN/AO |

## Excel 更新规则

- 盘前任务只写盘前列：`A/I/K/M/N/O/P/AI/AL/AM/AN/AO`
- **绝对不覆盖**收盘列 `B/C/D/J/R/T/V/X/Z/AG`（留给次日盘后职责——合并后盘前任务直接补写 X-1 行完整收盘 + X 行盘前指向）
- 公式列 `E/F/G/H/L/Q/S/U/W/Y/AA/AC/AE/AH` 不覆盖，openpyxl 自动保留
- 找行：A 列 = X 日期；无则加新行（用第一个 A 列为 None 的行，勿用 max_row+1）

## 数据源

- **新浪 hf_ 外盘期货**：`https://hq.sinajs.cn/list=hf_CL,hf_GC,hf_SI,hf_HG,hf_NQ,hf_ES,hf_YM,hf_VX`（需 Referer 头，GBK 解码）
- **WebSearch 综合**：美股三大指数收盘、金龙指数、RTY 期货、VIX9D 估值、宏观数据

## 3 触发器（盘前核心判定）

| 触发器 | 指标 | 阈值 |
|---|---|---|
| ① VIX9D 走扩 | 9 日到期期权 IV（CBOE 独立指标） | > 20 = 前端恐慌 |
| ② US30Y 跳升 | 30Y 收益率方向 | > +5 bp = 鹰派 |
| ③ RTY vs SPX 期货相对强弱 | RUT/SPX 比值 | < -1% = 小盘领跌 = 真 risk-off |

**基调判定**：

- ⚡ event-drive：地缘/政策突发事件主导
- 🔥 risk-on：VIX9D 持平 + RTY 抗跌
- 🧊 risk-off：VIX9D 走扩 + RTY 领跌
- 中性震荡：触发器无明确信号

## 输出样例

`examples/us_pre_market_2026-09-04.html`（60 KB）

## 详细文档

- 主项目文档：[docs/architecture.md](../docs/architecture.md)
- 七步测温方法论：[docs/seven-step-framework.md](../docs/seven-step-framework.md)
- 自动化时间表：[docs/automation-schedule.md](../docs/automation-schedule.md)
- WorkBuddy 技能说明：[SKILL.md](./SKILL.md)
