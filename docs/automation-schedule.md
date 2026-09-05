# 自动化触发时间表

> 两个模块的自动化触发链路、合并策略、暂停/恢复记录。

## 活跃自动化（2026-09 起）

| automation_id | 模块 | 触发时间（GMT+8） | 报告标题 | 输出文件 |
|---|---|---|---|---|
| 1787706522091 | commodity 晨报 | **07:30** | 【商品晨报】YYYY-MM-DD | `outputs/commodity_morning_YYYY_MM_DD.html` |
| 1787700114240 | us-stock 盘前 | **19:45** | 【美股盘前】YYYY-MM-DD | `outputs/市场温度_盘前_YYYY-MM-DD.html` |

## 已暂停自动化

| automation_id | 原模块 | 原触发时间 | 暂停日期 | 原因 |
|---|---|---|---|---|
| 1787490867965 | us-stock 盘后 | 07:45 | 2026-09-01 | 合并入盘前报告（盘前承担前一日完整复盘） |
| 1788103353019 | silicon 专题 | 20:00 | 2026-09-01 | 合并入 commodity 晨报第六段 |
| 1788105988743 | lithium 专题 | 20:30 | 2026-09-01 | 合并入 commodity 晨报第七段 |

**所有 PAUSED 自动化保留未删**，可手动恢复。

## 邮件标题统一规范

所有报告类邮件标题统一格式 = `【前缀】YYYY-MM-DD`，**只一段**，不附加关键词/基调/结论后缀。

| 前缀 | 对应模块 |
|---|---|
| 【商品晨报】 | commodity 晨报 |
| 【美股盘前】 | us-stock 盘前（含盘后复盘） |

## 报告篇幅规范

| 模块 | 正常区间 | 判定 |
|---|---|---|
| commodity 晨报（含硅链+锂链专题） | 20-50 KB | < 20 KB = 内容被砍；> 50 KB = 有冗余 |
| us-stock 盘前（合并盘后复盘） | 45-60 KB | < 25 KB = 复盘/对账不全；> 80 KB = 有冗余 |

## 数据采集时序

### commodity 模块（07:30 触发）

```
T-30 min   commodity_temp_fetch.py        → commodity_temp_data.json
T-15 min   commodity_oi_analyze.py        → commodity_oi_data.json
T-10 min   commodity_term_analyze.py      → commodity_term_structure.json
T-5 min    silicon_temp_fetch.py          → silicon_data.json
T-3 min    WebSearch 宏观数据（手动）
T+0        编辑 CONTEXT 字典（手动）
T+5 min    commodity_morning_report.py    → HTML
T+10 min   send_report.py                 → SMTP 发送
```

### us-stock 模块（19:45 触发）

```
T-30 min   fetch_us_market.py             → us_market_snapshot.json
T-15 min   WebSearch 三指数收盘（手动）
T-10 min   编辑 T / STEP 字典（手动）
T+0        generate_pre_market.py         → HTML
T+5 min    update_excel_pre_market.py     → Excel X-1 行完整 + X 行盘前
T+10 min   send_report.py                 → SMTP 发送
```

## 凭证管理

### macOS Keychain

```bash
# 一次性配置
security add-generic-password -s QQMailAuthCode -a hongshuhai@foxmail.com -w '<你的授权码>'

# 所有 send_report.py 都用这一行取：
auth_raw = subprocess.check_output(['security', 'find-generic-password', '-s', 'QQMailAuthCode', '-w'], text=True).strip()
password = auth_raw.strip('<>')   # ⚠ 必须 strip('<>')
```

### 跨平台注意

- **Linux / Windows**：Keychain 不可用，需修改 `send_report.py` 用环境变量：
  ```python
  password = os.environ['QQ_MAIL_AUTH_CODE']
  ```
- **Docker / CI**：用 secrets 注入

## WorkBuddy 自动化配置参考

### commodity 晨报（automation-1787706522091）

- **scheduleType**: recurring
- **rrule**: `FREQ=DAILY;BYHOUR=7;BYMINUTE=30`
- **status**: ACTIVE

### us-stock 盘前（automation-1787700114240）

- **scheduleType**: recurring
- **rrule**: `FREQ=DAILY;BYHOUR=19;BYMINUTE=45`
- **status**: ACTIVE

## 已知踩坑记录

### 1. 双份脚本同步（2026-09-02 踩坑）

`commodity_morning_report.py` 在两个地方存在：
1. `~/.workbuddy/skills/commodity-morning-report/scripts/`
2. `/Users/shuhaihong/Documents/workbuddy/`（工作目录）

编辑任意一份后必须 `cp` 覆盖另一份——硅链/锂链专题从主报 `import CONTEXT`，单一数据源失效会导致专题用旧数据。

**解决**：本项目仓库的 `commodity/scripts/commodity_morning_report.py` 是唯一权威源，工作时只需改这一份。

### 2. % 格式化转义（2026-09-02 踩坑）

脚本里有 `A('...' % 变量)` 的旧式 % 格式化模板（如"价差时间窗口"段），**在模板字符串内新增含 % 的文本（如 "97.49% 支持"）必须写成 `%%`**，否则报 `TypeError: not enough arguments for format string`。

### 3. PS/SI 触发器方向词打架（2026-09-02 反馈）

负号只在数据表出现；验证信号/价差时间窗口写"远月升水收窄至 3,000 元以内 / 走扩至 4,000 元以上 / 突破 4,500 元"，禁止"−4,000 以上/跌破 −4,500"这类方向词打架写法。

### 4. 主力迁移窗口的 OI 解读（2026-09-02 反馈）

9-10 月 2609/2610→2701 移仓期单合约 OI 翻倍是机械结果，**禁止据此写"增量资金持续入场"**；第五章必须标注"单合约非全品种合计"。

### 5. WebFetch 替代东财 K 线接口（2026-09-02 实测）

`perf_silicon` 行 20 日涨跌幅：本机直接请求东财 K 线接口通常被限流，改用 WebFetch 访问 `https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=225.SI2611&...&lmt=30`，取"最新收盘 vs 往前第 20 根收盘"计算。
