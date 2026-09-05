---
name: commodity-morning-report
description: 国内大宗商品晨报生成与发送（七步测温框架）。当用户要求生成/发送「商品晨报」、或 automation-1787706522091 每日 07:30 触发时使用。工作流：抓取新浪期货数据 → 更新 CONTEXT 静态上下文（宏观/日历/硅链/锂链基本面）→ 运行 commodity_morning_report.py 生成 HTML → SMTP 发送。输出 outputs/commodity_morning_YYYY_MM_DD.html，标题【商品晨报】YYYY-MM-DD。
agent_created: true
---

# 商品晨报（国内大宗商品七步测温框架）

## 定位

Frank 期货主战场的每日晨报（automation-1787706522091，07:30 GMT+8）。报告覆盖：宏观大气候 → 今日事件日历 → 工业硅/多晶硅（主战场）→ 硅链专题深挖 → 碳酸锂（第二主战场）→ 全品种事件日历。

**本技能是硅链/锂链专题的 CONTEXT 单一数据源**——`silicon_focus_report` / `lithium-focus-report` 两个技能通过 `from commodity_morning_report import CONTEXT` 复用本脚本的 CONTEXT。改价表/基本面只改本脚本一处，三报自动同步。

## 触发词

商品晨报、commodity morning report、commodity_morning_report、大宗商品晨报

## 工作流（5 步）

### 1️⃣ 数据抓取（新浪期货接口，快速）

```bash
cd <技能目录>/scripts
python3 commodity_temp_fetch.py   # → commodity_temp_data.json（各品种行情+期限结构）
python3 commodity_oi_analyze.py   # → commodity_oi_data.json（主力持仓 20 日趋势）
python3 commodity_term_analyze.py # → 期限结构分析（升贴水+年化展期）
python3 silicon_temp_fetch.py     # → silicon_data.json（工业硅 SI / 多晶硅 PS 行情）
```

数据源：`https://stock2.finance.sina.com.cn/futures/api/jsonp.php/...InnerFuturesNewService.getDailyKLine?symbol=nf_<合约>`（需 Referer 头）。失败重试 2 次，限流则用 WebFetch 抓东财 secid=225.SI2611 兜底。

### 2️⃣ 更新 CONTEXT 静态上下文（运行前必做）

`commodity_morning_report.py` 顶部 CONTEXT 字典有 14 个 key，用 WebSearch 搜索最新数据后更新（不要用旧数据）：

| key | 内容 | 更新频率 |
|---|---|---|
| `macro` | 宏观大气候（PPI/CPI/PMI/M2社融/美元/政策信号） | 每月宏观数据发布后 |
| `calendar` | 今日及近期事件日历（每行: 日期/事件/说明/涉及品种） | 每日 |
| `silicon_fundamental` | 硅链基本面（库存/供给/需求/基差） | 每日 |
| `silicon_spot_rows` | 工业硅现货价表 15+ 行（6 类硅+3 类非标+5 类多晶硅+利润行） | 每日 |
| `weak_reality_rows` | L2 咨询层"弱现实拆解" | 每日 |
| `temps` / `headline` / `overall` | 七步测温读数/一句话/综合温度 | 每日 |
| `lithium_fundamental` | 碳酸锂基本面（LC2701 行情/基差/仓单） | 每日 |
| `lithium_spot_rows` | 锂链价表 7 行（电碳/工业级/氢氧化锂/锂精矿/利润） | 每日 |
| `lithium_weak_reality_rows` | 锂链"强现实 vs 弱预期"拆解 | 每日 |
| `lithium_actionable` | 锂链三角色套保建议（L3 行动层） | 每日 |
| `lithium_signals` | 锂链验证信号四档价差触发器 | 每日 |
| `lithium_events` | 锂链事件日历 | 每日 |

**关键内容规范（Frank 沉淀，缺一不算客户可执行）**：
- 硅链价表必须含：不通氧 553#/通氧 553#/441#/421#/3303#/2202# + 非标品 99硅/97硅/551# + N 复投料/N 致密料/N 菜花料/N 颗粒硅/P 致密料 + 多晶硅厂利润行（1.6 元/kg 亏损口径）
- 市场分割逻辑：标准品期现市场 vs 非标品现货市场两条平行路径，判断盘面传导的关键判据
- Actionable 精细化五条：① 头寸变动可执行（X%→Y%+现货端动作+复建条件）② 相反场景拆两条 ③ 标注持有周期（60-90 天）④ 验证信号给三档边界值 ⑤ 动作末尾加 ⚠"切忌"警示框
- 三层升级 SOP：L1 分析层（蓝盒）→ L2 咨询层（黄盒）→ L3 行动层（绿盒）

### 3️⃣ 生成报告 HTML

```bash
python3 commodity_morning_report.py YYYY MM DD
# 例: python3 commodity_morning_report.py 2026 09 02
# 输出: outputs/commodity_morning_2026_09_02.html（相对技能目录）
```

脚本会自动读同目录 JSON 数据文件，找不到时跳过对应块但保留 CONTEXT 静态内容。

### 4️⃣ 校验

- 文件存在且非空
- 大小：20-50 KB 为合理（含硅链+锂链完整专题）；< 20 KB = 内容被砍；> 50 KB = 有冗余
- 样式：内联、浅色背景、纯表格无 JS；涨红 #C0392B / 跌绿 #1E8449（中国惯例）

### 5️⃣ SMTP 发送

```bash
python3 send_report.py --title 商品晨报 --date YYYY-MM-DD --html outputs/commodity_morning_YYYY_MM_DD.html
```

- 标题格式（Frank 2026-08-26 确认统一）：`【商品晨报】YYYY-MM-DD`，只一段不加后缀
- 链路：smtp.qq.com:465 SSL，授权码 `security find-generic-password -s QQMailAuthCode -w` 后 **必须 .strip('<>')**
- 收件人 hongshuhai@foxmail.com，不抄送不 BCC
- 失败回退：SMTP 失败 → mcp__qq-mail__SendMessage（to 用 `[{"email":"hongshuhai@foxmail.com","name":"Frank"}]` 数组，注意 DeferExecuteTool 包装 bug）→ 再失败把 HTML 留 outputs/ 备份交付

## 注意事项

- **数据时效**：CONTEXT 是"发出视角"，每次运行前必须搜索更新，禁止复用上一日未更新的宏观/日历数据
- **临时增量未确认不发邮件**：Frank 临时修改报告内容时，改完先生成 HTML 给他预览确认，确认"可以发了"再走 send_report.py
- **涨红跌绿**：所有涨跌幅配色按中国惯例，勿用欧美惯例
- **盘后合并**：2026-09-01 起商品晨报是硅链+锂链专题内容唯一出口（硅链 20:00 / 锂链 20:30 专题自动化已 PAUSED）
- **双份脚本必须同步**：`commodity_morning_report.py` 存在两份——主工作目录 `/Users/shuhaihong/Documents/workbuddy/` 与技能目录 `scripts/`。编辑任意一份后必须 `cp` 覆盖另一份（硅链/锂链专题从主报 `import CONTEXT`，单一数据源失效会导致专题用旧数据）。9/2 踩坑记录。
- **% 格式化转义坑**：脚本里有 `A('...' % 变量)` 的旧式 % 格式化模板（如"价差时间窗口"段），**在模板字符串内新增含 % 的文本（如 "97.49% 支持"）必须写成 `%%`**，否则报 `TypeError: not enough arguments for format string`。9/2 踩坑记录。
- **perf_silicon 20 日涨跌幅重算**（脚本约 255 行硬编码 `perf_silicon` 行）：本机直接请求东财 K 线接口（secid=225.SI2611 / 225.PS2611）通常被限流，改用 **WebFetch 访问** `https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=225.SI2611&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58&klt=101&fqt=1&end=YYYYMMDD&lmt=30`，取"最新收盘 vs 往前第 20 根收盘"计算（20 根口径）。9/2 实测：SI +4.4% / PS +6.7%。注意：此值用于"板块轮动"表排序与展示，忘记更新不影响生成但数据失真。
- **碳酸锂 LC 行情不在这两个抓取脚本内**（commodity_temp_fetch / silicon_temp_fetch 均无 LC）：需用 `https://hq.sinajs.cn/list=nf_LC2701,nf_LC2705,nf_LC2609`（带 Referer 头）单独抓，或 WebSearch 确认收盘价后手写进 `lithium_fundamental`。9/1 实测：LC2701 收 157,860(-1.64%) 冲高 162,860 回落。
- **价差口径全表统一"近月−远月"**（9/2 Frank 反馈①）：正=back/近月升水，负=contango/远月升水。si_gap/ps_gap 用 `近月−远月`（勿用远月−近月），第四章 SI/PS 行、第六章验证信号、第七章 LC 价差全部同口径；"制度断层/政策断层"这类远月升水描述用 `gap_note()` 输出"远月升水 X 元"。改完自检：SI2611(8,790)−SI2612(9,110)=−320；PS=−3,705；LC2701−LC2705=+3,660。
- **四象限必须同周期**（9/2 Frank 反馈②）：价格×持仓用同一时间窗口——第五章固定为 20日×20日（`px_chg_20d`/`oi_chg_20d`，读 JSON 键名勿错写 `oi_chg`），SI/PS 行也用 20 日口径（`perf_silicon` 值），并在章节注明"20日窗口"；第六章实测是 9/1 当日窗口，两章尺度不同需在脚注说明不矛盾。分类规则：|px|≤1% 时 OI>20% = 增仓对峙(巨量加仓·价格滞涨)、OI<-20% = 减仓撤离，中性只留给量价双平（否则玻璃 OI+187.7% 会被误标中性）。
- **基差/正反套口径固化**（9/2 Frank 反馈③）：`基差 = 现货 − 期货`（+ = 现货升水/期货贴水，− = 期货升水）。**正套=买现货卖期货(买现卖期)**，期货升水时窗口开；**反套=卖现货买期货(卖现买期)**，现货升水时窗口开。基差叙事全文只许一种表述（如"期货由升水 2,500 转为现货升水 640"），禁止"快速回吐/转升水回吐"等歧义词混用，禁止一处写"窗口打开"另一处写"窗口关闭"。
- **期限结构五档分类**（9/2 第二轮深度审查新增，`struct_label()` 实现）：年化 = 价差÷近月价×12÷间隔月数（**近月做分母**，Frank 确认正确）。五档：`>+3%` 贴水(现货紧) / `−3%~+3%` 偏紧(近平水) / `−6%~−3%` 正常持有成本(满carry) / `≤−6%` 深升水(过剩定价)。零轴注释必须自洽：满carry contango 约 −3%~−6%（不是 ±3%）；9/2 校验基线：贴水 7 行(SC/MA/M/TA/Y/I/CU)、偏紧 4 行(AL/AG/AU/RB)、满carry 1 行(C −4.7%)、过剩 4 行(UR/P/SA/FG)，共 16 行。
- **跨品种比基差必须用基差率**（9/2 第二轮新增）：基差率 = 基差绝对值 ÷ 标的价，禁止直接用基差绝对值跨品种比较（SI +410 = 4.7% vs LC +640 = 0.4%，差一个数量级——硅链反套"净利~100 元/吨"仍有空间 vs 锂链 0.4% 远低于持有成本不可做）。硅链中游基差**计价品=期货基准品，执行品=实际流通品**：SI 期货基准是通氧 553# 但月流通主力是不通氧 553#（9,200），基差用执行品算（+410 而非 +610），净利扣除仓储+资金成本约 310 元/吨后 ~100 元/吨。
- **主力合约统一口径**（9/2 第二轮新增）：第五章 `commodity_oi_analyze.py` 的 TARGETS 必须与第三章板块轮动/第四章期限结构**同合约**（如 RB 用 RB2701 非 RB2610），否则 20 日涨跌幅两章打架（+4.69% vs +5.24% 实测案例）。改合约后重跑 oi_analyze 并核对两章数值一致。
- **PS/SI 触发器一律绝对值表述**（9/2 第二轮新增）：负号只在数据表出现；验证信号/价差时间窗口写"远月升水收窄至 3,000 元以内 / 走扩至 4,000 元以上 / 突破 4,500 元"，禁止"−4,000 以上/跌破 −4,500"这类方向词打架写法。
- **主力迁移窗口的 OI 解读**（9/2 第二轮新增）：9-10 月 2609/2610→2701 移仓期单合约 OI 翻倍是机械结果（RB 40.4万→129万手 +219.7%），**禁止据此写"增量资金持续入场"**；无全品种总持仓数据时删该结论，改注"单合约口径+移仓成分"。第五章必须标注"单合约非全品种合计"。
- **温度计刻度**（9/2 第二轮新增）：温度 = 主观读数（**无固定权重公式，六板块不横向可比**）；水位看绝对值（全>33 = 整体偏热非分化）、分化看温差（如 5.0°C）。禁止写"27-33 正常区间"之类伪量化刻度。
- **SC 三套价格口径**（9/2 第二轮核实）：日盘 K 线收盘（第五章 20 日涨跌用，9/1=637.8）/ 官方结算价（新浪 f[10]，9/1=637.2）/ **夜盘结算价**（term_structure settle 快照，9/1=687.5——第四章 +55.2% 来源）。三口径并存不矛盾，第四章注释需标注"SC 夜盘结算 687.5"防读者误读。
- **追保压力表公式**（9/2 第二轮新增，第九段）：初始保证金 = 价格×手数×乘数×保证金率（硅 SI2611 10% / 锂 LC2701 12%）；维持保证金 = 初始×80%；追保 = 浮亏 − 20%×初始；授信占用 = (初始+追保) ÷ (2×初始)。硅企卖保 30%(600手) +5%/+10%/+15% → 追保 79.3/211.0/343.0万、授信 65%/90%/**115%超限**；锂盐厂卖保 50%(1,500手) → 追保 615.6/1,799.6/2,983.6万、授信 61%/82%/**103%超限**。结论：价格逆向 +10% 即吃掉初始保证金并追加一倍；+15% 授信超限有强平风险。
