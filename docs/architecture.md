# 项目架构说明

> 单源架构是本项目的核心设计——commodity 模块的 `CONTEXT` 字典被三个报告共享，改一处自动同步三处。

## 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                  数据采集层（每日 06:00-07:30）                │
├─────────────────────────────────────────────────────────────┤
│  commodity_temp_fetch.py   → commodity_temp_data.json       │
│  commodity_oi_analyze.py   → commodity_oi_data.json          │
│  commodity_term_analyze.py → commodity_term_structure.json   │
│  silicon_temp_fetch.py     → silicon_data.json               │
│  fetch_us_market.py        → us_market_snapshot.json         │
│  WebSearch / WebFetch      → 宏观数据 / 突发新闻             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│            CONTEXT 静态上下文（人工编辑，单一数据源）           │
├─────────────────────────────────────────────────────────────┤
│  commodity_morning_report.py 顶部的 CONTEXT 字典              │
│  - macro / calendar / silicon_fundamental / silicon_spot_rows│
│  - weak_reality_rows / temps / headline / overall            │
│  - lithium_fundamental / lithium_spot_rows                   │
│  - lithium_weak_reality_rows / lithium_actionable             │
│  - lithium_signals / lithium_events                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓ from . import CONTEXT
┌─────────────────────────────────────────────────────────────┐
│              报告生成层（HTML 直产，邮件正文嵌入）             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌──────────────────────────┐  │
│  │ commodity_morning_report │  │ generate_pre_market.py   │  │
│  │ → commodity_morning.html │  │ → 市场温度_盘前.html     │  │
│  └──────────────────────────┘  └──────────────────────────┘  │
│  ┌──────────────────────────┐  ┌──────────────────────────┐  │
│  │ silicon_focus_report.py  │  │ generate_market_post.py  │  │
│  │ → silicon_focus.html     │  │ → 市场温度_盘后.html     │  │
│  └──────────────────────────┘  └──────────────────────────┘  │
│  ┌──────────────────────────┐                                │
│  │ lithium_focus_report.py  │                                │
│  │ → lithium_focus.html     │                                │
│  └──────────────────────────┘                                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Excel 更新层（仅 us-stock）                       │
├─────────────────────────────────────────────────────────────┤
│  update_excel_pre_market.py → 盘前指向列（X-1 收盘 + X 盘前）│
│  update_xlsx_r11.py         → 收盘完整版（盘后补全）         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              邮件发送层（SMTP via Keychain）                    │
├─────────────────────────────────────────────────────────────┤
│  send_report.py → smtp.qq.com:465 SSL → hongshuhai@foxmail  │
└─────────────────────────────────────────────────────────────┘
```

## 数据流时序

### commodity 模块（07:30 GMT+8 触发）

```
T-30min:  commodity_temp_fetch.py        (4 个 JSON 落地)
T-15min:  commodity_oi_analyze.py        (持仓趋势 JSON)
T-10min:  commodity_term_analyze.py      (期限结构 JSON)
T-5min:   silicon_temp_fetch.py          (硅链行情 JSON)

T+0:      编辑 CONTEXT 字典（宏观/日历/基本面）

T+5min:   commodity_morning_report.py    → commodity_morning_YYYY_MM_DD.html
T+10min:  send_report.py                 → 邮件发送
```

### us-stock 模块（19:45 GMT+8 触发）

```
T-30min:  fetch_us_market.py             (隔夜外盘快照)
T-15min:  WebSearch 三指数收盘 + 突发新闻
T-10min:  编辑 T / STEP 字典（昨夜 X-1 完整收盘数据）

T+0:      generate_pre_market.py         → 市场温度_盘前_YYYY-MM-DD.html
T+5min:   update_excel_pre_market.py     → Excel X-1 行完整 + X 行盘前
T+10min:  send_report.py                 → 邮件发送
```

## 单源架构的关键约束

### ⚠️ 双份脚本必须同步

`commodity_morning_report.py` 在两个地方存在：

1. `commodity/scripts/commodity_morning_report.py`（本仓库）
2. `~/.workbuddy/skills/commodity-morning-report/scripts/commodity_morning_report.py`（WorkBuddy 技能目录）

**编辑任何一份后必须 `cp` 覆盖另一份**——因为硅链/锂链专题从主报 `import CONTEXT`，单源失效会导致专题用旧数据。

### ⚠️ import 路径兼容

专题脚本的 import 写法：

```python
# silicon_focus_report.py / lithium_focus_report.py 顶部
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from commodity_morning_report import CONTEXT
```

专题脚本放在 `scripts/silicon_focus/` 或 `scripts/lithium_focus/` 子目录时，**`__file__` 的相对路径要正确解析到上一级的 `commodity_morning_report.py`**。

### ⚠️ CONTEXT 字段类型约束

| key | 类型 | 说明 |
|---|---|---|
| `macro` | list[dict] | 宏观大气候条目 |
| `calendar` | list[dict] | 事件日历 |
| `silicon_spot_rows` | list[list] | 二维列表（每行 5 列） |
| `weak_reality_rows` | list[str] | L2 咨询层条目 |
| `temps` | list[float] | 七步测温读数（无固定权重） |
| `lithium_actionable` | list[str] | L3 行动层条目（按角色分组） |
| `lithium_signals` | list[dict] | 验证信号触发器 |

## 自动化触发链路

| 模块 | automation_id | 触发时间 | 状态 |
|---|---|---|---|
| commodity 晨报 | 1787706522091 | 07:30 GMT+8 | ACTIVE |
| us-stock 盘前 | 1787700114240 | 19:45 GMT+8 | ACTIVE |
| ~~us-stock 盘后~~ | ~~1787490867965~~ | ~~07:45 GMT+8~~ | PAUSED (2026-09-01) |
| ~~silicon 专题~~ | ~~1788103353019~~ | ~~20:00 GMT+8~~ | PAUSED (2026-09-01) |
| ~~lithium 专题~~ | ~~1788105988743~~ | ~~20:30 GMT+8~~ | PAUSED (2026-09-01) |

**2026-09-01 起合并策略**：
- commodity 晨报承担硅链/锂链专题完整深度内容
- us-stock 盘前承担昨夜完整复盘（原盘后职责）

详见 [automation-schedule.md](./automation-schedule.md)。
