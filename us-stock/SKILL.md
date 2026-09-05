---
name: us-stock-daily-report
description: 美股日报生成与发送（美股盘前战略版，automation-1787700114240）。当用户要求生成/发送「美股日报」「美股盘前」「美股盘后」或需美股 7 步测温/开盘开关/战略复盘报告时使用。2026-09-01 起盘前报告已合并盘后战略复盘——一份报告 = 昨夜 X-1 完整战略复盘 + 今夜 X 开盘开关。工作流：新浪 hf_ 外盘期货 + WebSearch 采集 → 更新模板 D 字典 → 生成 市场温度_盘前_YYYY-MM-DD.html → 更新 市场温度7步扫描.xlsx（X-1 行完整收盘 + X 行盘前指向）→ SMTP 发送【美股盘前】YYYY-MM-DD。
---

# 美股日报（盘前战略版 · 合并盘后复盘）

## 触发与时间
- 每日 19:45 GMT+8（美东 07:45 EDT），automation-1787700114240
- 主键日期 X = 今夜美股交易日；报告标题与文件名都用 X 日
- 2026-09-01 起**合并盘后战略版**：盘后任务已 PAUSED（automation-1787490867965 保留未删可恢复），盘前报告承担前一日完整复盘

## 报告结构（合并版，45-60 KB，越详细越好）
输出 `outputs/市场温度_盘前_YYYY-MM-DD.html`：
1. **顶头条**：一句话今日美股开盘背景（隔夜外盘 + 事件基调）
2. **昨夜 X-1 完整战略复盘（详细版）**：
   - 三大指数收盘 + 涨跌归因（SPX/IXIC/DJI/RTY）
   - 利率曲线：10Y/2Y/30Y 收盘 + bp 变动 + 曲线形态
   - 商品链：WTI/布伦特/COMEX金/白银/LME铜/谷物（小麦玉米大豆）
   - 信用端：JNK/HYG/TLT
   - 亚欧市场：恒指/日经/欧股
   - **对账表**：盘前预期 vs 实际（✅/❌）
   - **7 步完整温度表**（利率/指数/商品/黄金/VIX/信用/日历，每步一句话）
3. **今夜 X 开盘开关（战术版）**：
   - **3 触发器**：① VIX9D（9 日到期期权 IV，CBOE 独立指标）② US30Y（30Y 收益率方向）③ RTY vs SPX 期货相对强弱（RUT/SPX 比值，判断小盘 vs 大盘）
   - **7 步速览迷你版**：每步 1 行（10Y/期指/原油/金银铜/谷物/VIX/今夜日历）
   - **战术指令**：AO 列 30-50 字战术版（基调 + 开/关 + 一句话指令）
   - **今夜日历**：数据/事件（如 Dallas Fed、非农、财报映射）
   - **亚盘建议**：今晨亚太市场关注点

## 数据采集
1. **新浪 hf_ 外盘期货**（快）：`python3 fetch_us_market.py`，符号 hf_CL/hf_GC/hf_SI/hf_HG/hf_NQ/hf_ES/hf_YM/hf_VX（WTI/金/银/铜/纳指/标普/道指/VIX 期货），需 Referer: finance.sina.com.cn，GBK 解码
2. **WebSearch 综合**（慢但全）：美股三大指数收盘、金龙指数、RTY 期货（新浪无源，用 squawknews/Benzinga 新闻源）、VIX9D（盘前用估值——参考 Excel AI 列 + VIX 期货方向）、宏观数据（PCE/CPI/非农/ISM/Dallas Fed）、突发地缘事件
3. 数据基准时间戳：美东盘前 ~07:45 EDT；昨夜 = X-1 收盘

## 七步测温框架（Excel 列映射）
| 步 | 指标 | Excel 收盘列 | Excel 盘前列 |
|---|---|---|---|
| 1 | 利率曲线 2Y/10Y/30Y | B/C/D（E/F/G/H bp 公式） | — |
| 2 | 指数结构 SPX/DJI/IXIC/RTY | J/K/M/N/O（领涨板块文字） | K/M/N/O（期货方向） |
| 3 | 原油 WTI/布伦特 | P/R | — |
| 4 | 黄金/白银/铜 | T/U/V/X | — |
| 5 | VIX 衍生品 | Z/AA/AC/AE/AH | — |
| 6 | 估值 | AG | — |
| 7 | 日历/事件 | AI/AL/AM/AN/AO | AI/AL/AM/AN/AO |

**Excel 更新规则（市场温度7步扫描.xlsx · Sheet「每日数据」）**：
- 盘前任务只写盘前列：A/I/K/M/N/O/P/AI/AL/AM/AN/AO
- **绝对不覆盖**收盘列 B/C/D/J/R/T/V/X/Z/AG（留给次日盘后职责——合并后盘前任务直接补写 X-1 行完整收盘 + X 行盘前指向）
- 公式列 E/F/G/H/L/Q/S/U/W/Y/AA/AC/AE/AH 不覆盖，openpyxl 自动保留
- 找行：A 列 = X 日期；无则加新行（用第一个 A 列为 None 的行，勿用 max_row+1，公式模板行也算 max_row）
- 参考脚本：`update_excel_pre_market_2026_08_26.py`（盘前更新）、`update_xlsx_r11_2026_08_25.py`（收盘完整版）

## 邮件发送
- SMTP 直连 smtp.qq.com:465 SSL；授权码 Keychain `security find-generic-password -s QQMailAuthCode -w`，**必须 .strip('<>')**
- 用户名 hongshuhai@foxmail.com；收件人 hongshuhai@foxmail.com（不抄送不 BCC）
- 标题：`【美股盘前】YYYY-MM-DD`（只一段，不加后缀，Frank 2026-08-26 确认）
- 正文：HTML 直接嵌入（不附件）
- 命令：`python3 send_report.py --title 美股盘前 --date YYYY-MM-DD --html outputs/市场温度_盘前_YYYY-MM-DD.html`
- 失败回退：SMTP 失败则 HTML 留 outputs/ 备份交付，不报错结束

## HTML 样式规范
- 中国惯例：涨红 #C0392B / 跌绿 #1E8449
- 浅色背景 BG #FAF8F2 / 面板 #FFFFFF / 高亮 #FFF7D6 / 边框 #D6CFA8 / 墨色 #1B2631 / 弱化 #7F8C8D
- 内联样式、纯表格无 JS；七步表用红绿箭头（▲/▼）标方向
- **篇幅判定（合并后）**：< 25 KB = 内容被砍（复盘/对账不全），> 80 KB = 有冗余；自然 45-60 KB

## 执行步骤（每日）
1. `python3 fetch_us_market.py` 抓外盘期货快照（夜盘/盘前现价）
2. WebSearch：三大指数昨夜收盘、RTY 期货、VIX9D 估值、今夜日历、地缘/政策突发
3. 按当日数据填充模板（参考 `generate_pre_market_2026_08_31.py` 的 T/STEP 字典结构；盘后复盘参考 `generate_market_post_2026_08_26.py` 的 D 字典结构）生成 HTML
4. 更新 Excel：X-1 行完整收盘（如 X-1 是 X 的上一交易日）+ X 行盘前指向（A/I/K/M/N/O/P/AI/AL/AM/AN/AO）
5. `python3 send_report.py --title 美股盘前 --date X --html ...` 发送
6. 大小自检（25-80 KB 区间）

## 基调判定模板
- ⚡ event-drive（地缘/政策突发事件主导，如美伊冲突：油价 +3.8%、全线低开、大票领跌）
- 🔥 risk-on / 🧊 risk-off / 中性震荡——由 3 触发器交叉判定：
  - VIX9D 走扩 = 前端恐慌；持平 = 事件驱动非典型 risk-off
  - US30Y 跳升（鹰派）vs 企稳（中性）
  - RTY < SPX（小盘抗跌）= 风险偏好尚可；RTY 领跌 = 真 risk-off
