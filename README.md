# WorkBuddy Market Briefings

> 基于 [WorkBuddy](https://www.workbuddy.cn/) 自动化框架的 **大宗商品晨报 + 美股日报** 双场景开源项目，由期货经纪实战沉淀而来。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![WorkBuddy Skill](https://img.shields.io/badge/WorkBuddy-Skill-green.svg)](https://www.workbuddy.cn/)
[![CI](https://github.com/hongshuhai/hongshuhai-market-briefings/actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)

---

## 📌 项目定位

这是洪树海在做期货经纪业务时沉淀的两个日常自动化项目，经过 8 个月多轮迭代稳定下来后开源：

| 模块 | 场景 | 触发时间 | 一句话定位 |
|---|---|---|---|
| **commodity/** | 国内大宗商品晨报（工业硅/多晶硅/碳酸锂等） | 每日 07:30 GMT+8 | 七步测温 + 主战场深挖 + 客户级 Actionable |
| **us-stock/** | 美股日报（盘前战略版 = 昨夜复盘 + 今夜开盘开关） | 每日 19:45 GMT+8 | 隔夜外盘 + 7 步 Excel + 3 触发器判定 |

**核心理念**：报告既是给自己看的，也是给客户群用的——给自己看要能快速锁定决策点，给客户看要能直接行动、可复用。所以每一份报告都做了 L1→L2→L3 三层升级：分析层（说了什么 / 为什么）→ 咨询层（关键问题拆解）→ 行动层（具体动作 + 量化参数 + 复建条件）。

---

## 🎯 核心特性

### 1. 七步市场温度扫描框架（双场景共用）

| 步 | 指标 | 美股映射 | 商品映射 |
|---|---|---|---|
| 1 | 利率曲线 | 2Y / 10Y / 30Y | — |
| 2 | 指数结构 | SPX / DJI / IXIC / RTY | 板块轮动 16 品种 |
| 3 | 原油链 | WTI / Brent | SC / 沥青 / 燃油 |
| 4 | 贵金属+工业金属 | 黄金 / 白银 / 铜 | 沪金 / 沪银 / 沪铜 |
| 5 | 波动率 | VIX / VIX9D / VVIX | — |
| 6 | 信用 | JNK / HYG / TLT | — |
| 7 | 日历/事件 | 财报 + 宏观数据 | 持仓 + 基差 + 价差窗口 |

### 2. 单源架构（commodity 模块）

```
commodity_morning_report.py  ← CONTEXT（14 个 key，单一数据源）
        ↓ from . import CONTEXT
silicon_focus_report.py      ← 工业硅 SI / 多晶硅 PS 主战场专题
lithium_focus_report.py      ← 碳酸锂 LC 第二主战场专题
```

**好处**：改一个价表 / 基本面，三份报告自动同步。**踩坑**：编辑主报后必须同步覆盖所有专题脚本。

### 3. 客户级 Actionable 精细化（5 条铁律）

1. **头寸变动要可执行**：`释放套保头寸 50% → 30%`，附现货端动作 + 复建条件
2. **场景拆开**：一个动作条款对应两个相反触发场景，必须拆成两条分别写
3. **时间周期要标注**：净利测算前必须注明持有周期（60-90 天）
4. **验证信号给边界值**：避免"收敛/走扩"二元模糊，给具体 -3000/-4000/-4500 三档数值触发器
5. **加 ⚠ 警示框**：动作末尾加"切忌"提醒，对冲"按建议操作却没注意前提"风险

### 4. 中国市场惯例

- 涨红跌绿（#C0392B / #1E8449）—— 与欧美相反
- 浅色背景 HTML 邮件模板（无 JS、无外部资源）
- 7 步温度表用 ▲/▼ 方向符号

---

## 🚀 快速开始

### 前置条件

- **Python 3.10+**（推荐 3.13）
- macOS / Linux（macOS 用于从 Keychain 取 QQ 邮箱授权码）
- 邮件发送依赖 QQ 邮箱 SMTP（其他邮箱可改 `send_report.py` 的 `SMTP_HOST`）

### 安装

```bash
git clone https://github.com/hongshuhai/hongshuhai-market-briefings.git
cd hongshuhai-market-briefings
```

无需 pip install，**纯标准库**（`smtplib` / `urllib` / `json` / `openpyxl` 仅 Excel 模块需要）。

### 配置 QQ 邮箱授权码（仅 macOS）

```bash
# 把 QQ 邮箱授权码存到 Keychain（一次性）
security add-generic-password -s QQMailAuthCode -a hongshuhai@foxmail.com -w '<你的授权码>'

# 验证可读取
security find-generic-password -s QQMailAuthCode -w
```

> ⚠️ **安全提示**：授权码等价于密码，不要硬编码到任何脚本里。本项目所有 `send_report.py` 都从 Keychain 取，开源即用。

### 运行 commodity 晨报

```bash
cd commodity/scripts
python3 commodity_temp_fetch.py   # 抓取各品种行情（→ commodity_temp_data.json）
python3 commodity_oi_analyze.py   # 主力持仓 20 日趋势（→ commodity_oi_data.json）
python3 commodity_term_analyze.py # 期限结构分析（→ commodity_term_structure.json）
python3 silicon_temp_fetch.py     # 工业硅/多晶硅行情（→ silicon_data.json）

# 编辑 commodity_morning_report.py 顶部的 CONTEXT 字典（宏观/日历/硅链/锂链基本面）
# 关键：CONTEXT 是"发出视角"，每次运行前必须搜索更新

python3 commodity_morning_report.py 2026 09 05
# 输出: ../examples/commodity_morning_2026_09_05.html

# 发送（可选）
python3 send_report.py --title 商品晨报 --date 2026-09-05 --html ../examples/commodity_morning_2026_09_05.html
```

### 运行 us-stock 盘前报告

```bash
cd us-stock/scripts
python3 fetch_us_market.py        # 抓取隔夜外盘期货（→ us_market_snapshot.json）

# 编辑 generate_pre_market.py 顶部的 T / STEP 字典（三指数收盘 + 利率 + VIX + 触发器）

python3 generate_pre_market.py
# 输出: ../examples/us_pre_market_2026-09-04.html

python3 update_excel_pre_market.py  # 更新 Excel 模板（市场温度7步扫描.xlsx）

# 发送（可选）
python3 send_report.py --title 美股盘前 --date 2026-09-04 --html ../examples/us_pre_market_2026-09-04.html
```

### 在 WorkBuddy 中使用

每个模块根目录都有 `SKILL.md`：

```
commodity/SKILL.md       # 商品晨报 + 硅链/锂链专题（合并版）
us-stock/SKILL.md        # 美股盘前/盘后（合并版）
```

把 `SKILL.md` 和 `scripts/` 复制到 `~/.workbuddy/skills/<name>/` 即可作为 WorkBuddy 技能加载。

---

## 📁 项目结构

```
hongshuhai-market-briefings/
├── README.md
├── LICENSE
├── .gitignore
├── docs/                         # 深度文档
│   ├── project-intro.md          # 📣 项目介绍（图文版，含截图 + 数据流图）
│   ├── architecture.md           # 单源架构图 + 数据流
│   ├── seven-step-framework.md   # 七步测温方法论
│   ├── silicon-lithium-playbook.md
│   ├── actionable-sop.md
│   └── automation-schedule.md
├── commodity/                    # 大宗商品晨报（含硅链/锂链专题）
│   ├── README.md
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── commodity_morning_report.py     # 主报（单源 CONTEXT）
│   │   ├── commodity_temp_fetch.py
│   │   ├── commodity_oi_analyze.py
│   │   ├── commodity_term_analyze.py
│   │   ├── silicon_temp_fetch.py
│   │   ├── send_report.py
│   │   ├── silicon_focus/                  # 硅链专题子模块
│   │   │   ├── silicon_focus_report.py
│   │   │   ├── silicon_kline_fetch.py
│   │   │   ├── silicon_temp_fetch.py
│   │   │   └── send_report.py
│   │   └── lithium_focus/                  # 锂链专题子模块
│   │       ├── lithium_focus_report.py
│   │       └── send_report.py
│   └── examples/                          # 真实示例报告
│       ├── commodity_morning_2026_09_05.html
│       ├── silicon_focus_2026_09_01.html
│       └── lithium_focus_2026_09_01.html
└── us-stock/                     # 美股日报
    ├── README.md
    ├── SKILL.md
    ├── scripts/
    │   ├── fetch_us_market.py
    │   ├── generate_pre_market.py
    │   ├── generate_market_post.py
    │   ├── update_excel_pre_market.py
    │   ├── update_xlsx_r11.py
    │   └── send_report.py
    ├── templates/
    │   └── market_temp_7step_template.xlsx   # 7 步扫描 Excel 模板
    └── examples/
        └── us_pre_market_2026-09-04.html
```

---

## 🛠️ 技术栈

- **Python 3.13**（managed 运行时，隔离环境）
- **WorkBuddy Skills** —— 自动化触发与邮件发送
- **macOS Keychain** —— 凭证安全存储
- **新浪期货接口** —— 国内行情（nf_SI2611 / nf_LC2701 等）+ 隔夜外盘（hf_CL / hf_GC）
- **东财 K 线接口** —— 兜底（secid=225.SI2611）
- **WebSearch / WebFetch** —— 宏观数据 + 突发新闻
- **openpyxl** —— Excel 7 步温度表

---

## 🤝 贡献指南

我们欢迎以下方向的贡献：

1. **新数据源接入**：akshare / tushare / wind / 同花顺 iFinD 等
2. **新场景适配**：A 股盘前/盘后（参考已沉淀的 HTML 报告）
3. **Actionable 框架增强**：更多角色 + 触发器
4. **可视化增强**：把 HTML 报告转 PNG 长图（参考 `html_to_long_png.py` 思路）
5. **国际化**：英文版报告模板

提交 PR 前请：

- 保留 `send_report.py` 的 Keychain 取值逻辑（不要硬编码授权码）
- 跑一遍 `commodity_morning_report.py` 自检（输出 20-50 KB 视为合格）
- 更新对应模块的 SKILL.md

---

## 📜 许可证

本项目采用 **MIT 许可证**——可自由商用、修改、闭源衍生，只需保留版权声明。详见 [LICENSE](./LICENSE)。

---

## 👤 作者

**洪树海（Frank）** —— 期货经纪 / 波动率实验室
📧 hongshuhai@foxmail.com
📍 宁波，中国

> 选定单一积累路径，深度优先于广度。

---

## ⚠️ 免责声明

本项目的所有报告内容**仅供参考与学习**，不构成任何投资建议。期货交易风险极高，请独立判断并自负盈亏。
