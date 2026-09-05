# commodity/ — 大宗商品晨报模块

> 国内大宗商品晨报（含工业硅/多晶硅主战场 + 碳酸锂第二主战场专题），每日 07:30 GMT+8 触发。

## 包含的子模块

| 子模块 | 路径 | 状态 | 触发方式 |
|---|---|---|---|
| **commodity 晨报** | `scripts/` | ACTIVE（主报） | automation-1787706522091，07:30 |
| **silicon 专题** | `scripts/silicon_focus/` | PAUSED（合并入主报） | 手动 |
| **lithium 专题** | `scripts/lithium_focus/` | PAUSED（合并入主报） | 手动 |

## 快速开始

```bash
cd scripts/

# 1. 数据抓取（4 个 JSON 落地）
python3 commodity_temp_fetch.py
python3 commodity_oi_analyze.py
python3 commodity_term_analyze.py
python3 silicon_temp_fetch.py

# 2. 编辑 commodity_morning_report.py 顶部的 CONTEXT 字典
#    关键: macro / calendar / silicon_fundamental / silicon_spot_rows
#    关键: lithium_fundamental / lithium_spot_rows / lithium_actionable

# 3. 生成报告
python3 commodity_morning_report.py 2026 09 05
# 输出: ../examples/commodity_morning_2026_09_05.html

# 4. 发送（可选，需 macOS Keychain 配置）
python3 send_report.py --title 商品晨报 --date 2026-09-05 --html ../examples/commodity_morning_2026_09_05.html
```

## 单源架构

```
commodity_morning_report.py ← CONTEXT（14 个 key，单一数据源）
        ↓ from . import CONTEXT
silicon_focus/silicon_focus_report.py
lithium_focus/lithium_focus_report.py
```

**改价表/基本面只改主报一处，三报自动同步。**

## 文件清单

| 文件 | 行数 | 说明 |
|---|---|---|
| `commodity_morning_report.py` | 808 | **主报**，含 CONTEXT 单源 |
| `commodity_temp_fetch.py` | 174 | 抓各品种行情（新浪 nf_ 接口） |
| `commodity_oi_analyze.py` | 69 | 主力持仓 20 日趋势 |
| `commodity_term_analyze.py` | 79 | 期限结构分析（升贴水+年化展期） |
| `silicon_temp_fetch.py` | 71 | 工业硅/多晶硅行情 |
| `send_report.py` | 78 | SMTP 发送（Keychain 取授权码） |
| `silicon_focus/silicon_focus_report.py` | — | 硅链专题（已合并入主报第六段） |
| `lithium_focus/lithium_focus_report.py` | — | 锂链专题（已合并入主报第七段） |

## CONTEXT 字典字段

主报顶部 `CONTEXT = { ... }` 含 14 个 key：

| key | 内容 | 更新频率 |
|---|---|---|
| `macro` | 宏观大气候（PPI/CPI/PMI/M2社融/美元） | 每月宏观数据发布后 |
| `calendar` | 今日及近期事件日历 | 每日 |
| `silicon_fundamental` | 硅链基本面（库存/供给/需求/基差） | 每日 |
| `silicon_spot_rows` | 工业硅现货价表 15+ 行 | 每日 |
| `weak_reality_rows` | L2 咨询层"弱现实拆解" | 每日 |
| `temps` / `headline` / `overall` | 七步测温读数/一句话/综合温度 | 每日 |
| `lithium_fundamental` | 碳酸锂基本面（LC2701 行情/基差/仓单） | 每日 |
| `lithium_spot_rows` | 锂链价表 7 行 | 每日 |
| `lithium_weak_reality_rows` | 锂链"强现实 vs 弱预期"拆解 | 每日 |
| `lithium_actionable` | 锂链三角色套保建议（L3 行动层） | 每日 |
| `lithium_signals` | 锂链验证信号四档价差触发器 | 每日 |
| `lithium_events` | 锂链事件日历 | 每日 |

## 数据源

- **新浪期货接口**：`https://stock2.finance.sina.com.cn/futures/api/jsonp.php/...InnerFuturesNewService.getDailyKLine?symbol=nf_<合约>`（需 Referer 头）
- **东财 K 线接口**：`https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=225.SI2611&...&lmt=30`（兜底）
- **WebSearch / WebFetch**：宏观数据 + 突发新闻 + 碳酸锂 LC 行情（nf_LC2701 在 commodity_temp_fetch 中未覆盖）

## 输出样例

`examples/commodity_morning_2026_09_05.html`（108 KB）

## 详细文档

- 主项目文档：[docs/architecture.md](../docs/architecture.md)
- 硅链/锂链方法论：[docs/silicon-lithium-playbook.md](../docs/silicon-lithium-playbook.md)
- Actionable SOP：[docs/actionable-sop.md](../docs/actionable-sop.md)
- 自动化时间表：[docs/automation-schedule.md](../docs/automation-schedule.md)
- WorkBuddy 技能说明：[SKILL.md](./SKILL.md)

## 踩坑记录

详见 [docs/automation-schedule.md](../docs/automation-schedule.md) 的"已知踩坑记录"章节。
