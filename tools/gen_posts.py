#!/usr/bin/env python3
"""
三平台发帖文案生成器
- V2EX: 技术硬核派 (踩坑记录: SSH/HTTP2/PAT)
- 知乎: 业务故事派 (为什么做、对客户的价值、期货经纪真实场景)
- X: 精炼版 (<280字，3 段 hook)

设计原则:
- 所有图片走 jsDelivr CDN (知乎/V2EX 通用，公网图片反盗链稳)
- 仓库链接全部用 https://github.com/hongshuhai/hongshuhai-market-briefings
- 链接都加 ?utm_source=xxx 跟踪效果（V2EX/知乎/X 各自辨识）
- 行文避免英文+中文混排太密，可读性优先
"""
import os
from datetime import date

REPO = "hongshuhai/hongshuhai-market-briefings"
CDN = f"https://cdn.jsdelivr.net/gh/{REPO}@main"

OUTPUT_DIR = "/Users/shuhaihong/Documents/workbuddy/outputs/post"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------- 共用图片 ----------

def img(name):
    return f"{CDN}/assets/screenshots/{name}.png"


# ---------- V2EX 版（技术硬核派） ----------

V2EX = f"""# 把期货经纪日常做成开源自动化，顺便聊聊 GitHub 推送踩的几个坑

我做了 8 个月期货经纪后，把每天 7:30 自动发出去的「商品晨报」、19:45 自动发的「美股日报」两个项目开源了：
**https://github.com/{REPO}?utm_source=v2ex**

MIT，纯 Python 3.10+ 标准库，5400 行+。下面快速过一下与其他研报项目的差异化，再聊聊推送到 GitHub 时撞上的几个真实坑。

## 三个不一样的点

### 1. 客户级 Actionable：报告不是给自己嗨的

一般研报停在 L1「分析层」（"价差走扩 355 元"就完事）。这套强制扩到 L2「咨询层」（"为什么弱？"三句话拆解）和 L3「行动层」（上游卖套保 / 中游反套 / 下游买套保，每个点位的精确百分比 + 重建条件 + ⚠ 切忌提示框）。

L3 不是 "建议加套保到 50%+" 这种模糊话——是「从 50% 降至 30%，现货端惜售；反弹到 X 区间再分批重建」。

### 2. 单源架构（commodity 模块的 14+ 数据源锁在三份报告上）

```
commodity_morning_report.py  ← CONTEXT (14+ key, 唯一数据源)
        ↓ from . import CONTEXT
silicon_focus_report.py      ← 工业硅 SI / 多晶硅 PS 专题
lithium_focus_report.py      ← 碳酸锂 LC 第二主战场专题
```

改一个价表 / 基本面，三份报告自动同步，长期维护不腐烂。

### 3. 零硬编码凭证 + CI 自动扫描

QQ 邮箱授权码全部从 macOS Keychain 取（`security find-generic-password -s QQMailAuthCode -w`），代码里零明文。仓库自带 GitHub Actions，每次 push 都会扫一遍硬编码凭证，守住安全基线。

## 演示

**商品晨报**（07:30 自动发送）— 七步测温框架 + 硅链/锂链两大主战场：

![commodity morning]({img('commodity_morning_full')})

**美股日报**（19:45 自动发送）— 盘前战略版 = 昨夜复盘 + 今夜开盘开关：

![us pre market]({img('us_pre_market_full')})

**单源架构数据流图：**

![workflow]({img('workflow-diagram')})

## 推送到 GitHub 时撞的真实坑

踩坑清单，献给同样撞墙的 V 友：

1. **iTerm 跑 `git push` 报"不能读取当前工作目录: Operation not permitted"** → iTerm 被 macOS TCC 拒读 `~/Documents`，换系统 Terminal.app 解决
2. **HTTP/2 framing layer 错误** → 改走 SSH 整个绕开 HTTP layer，比强制 HTTP/1.1 干净
3. **"Invalid username or token. Password authentication is not supported"** → GitHub 自 2021-08 就禁密码，HTTP/2 失败后 fallback 触发的次生错误，根因不在密码
4. **Classic PAT scopes=[] 空壳** → 重新生成时一定要勾选 permissions
5. **Fine-grained PAT propagation 失败** → 默认 No repositories，要手动选仓库
6. **Token 一旦嵌过 URL 即使没推送成功也算泄漏** → 立即去 https://github.com/settings/tokens 撤销

最后我直接走 SSH（全账号已有 `~/.ssh/id_*` key），一条命令搞定。

## 谁适合用

- 期货 / 衍生品 / 大宗商品的从业者，需要每日给客户发报告的
- 想体验「单源架构 + 客户级 Actionable」思路的研报类产品开发者
- 对 WorkBuddy / AI Agent 编排感兴趣的，可以把这套当真实业务场景看

---

🔗 **仓库**：https://github.com/{REPO}?utm_source=v2ex
📜 **License**：MIT（商用 / 改 / 闭源都可以，保留版权声明即可）
⭐ 觉得有用求个 star

> ⚠️ 免责声明：项目内容仅供参考与学习，不构成投资建议。期货交易风险极高，请独立判断。
"""


# ---------- 知乎版（业务故事派）----------

ZHIHU = f"""# 从分析师自嗨，到客户能直接行动：我把期货经纪日常做成了开源

2026 年开年，宁波。

我做期货经纪的头三个季度，经历了两次认知颠覆：

**第一次**是发现传统研报几乎全部是「自嗨」——分析师写了 8000 字深度，客户看完划走，留下来想问一句"那我到底该怎么办"，得到的回复是"风险中性"。

**第二次**是发现这个问题的根源不是"分析师不努力"，而是**报告架构本身不承载行动**。从一开始就被设计成"看完涨姿势"，而不是"看完能动手"。

于是我用 8 个月时间、迭代上百次，把 7:30 自动发出的「**大宗商品晨报**」和 19:45 自动发出的「**美股日报**」两个项目打磨出来。**今天开源：https://github.com/{REPO}?utm_source=zhihu**

## 一个真实场景：以前的报告 vs 现在的报告

**以前**（客户看完的反应）：
> 标题：《九月工业硅行情分析》
> 正文：本周工业硅 SI2611 价差走扩 355 元，市场结构分化，下游接货意愿谨慎，预计短期中性偏多震荡。
> *客户看完问题：所以呢？我要卖还是买？什么时候？*

**现在**（L1→L2→L3 三层结构）：

| 层级 | 标题 | 回答的问题 |
|---|---|---|
| L1 分析层 | SI2611 价差走扩 355 元 | 说了什么 / 为什么 |
| L2 咨询层 | 「为什么弱？」三句话拆解 + 利润分化口径备注 | 客户会怎么反问你 |
| **L3 行动层** | 上游卖套保 → 释放头寸 50%→30% / 中游反套 → 基差 +250 以上分批建仓 / 下游买套保 → 14.5 万以下加 70% | **现在怎么办** |

**现在**（客户看完的反应）：
> 哦，我下游厂这边，他这个让我们 14.5 万以下分批买远期原料对吧？反弹 16 万止盈？

> *——这才叫报告。*

### L3 行动层的 5 条铁律

这 8 个月撞出来的，是 L3 写得不好看会出大事：

1. **头寸变动要可执行**：释放套保 → 必须说「从 X% 降到 Y%」，否则客户真敢满仓干
2. **场景拆开**：一个动作对应两个相反触发场景时（如下跌/上涨），必须拆成两条分别写
3. **时间周期标注**：净利测算前必须写「持有 60-90 天」，否则客户拿着问行不行
4. **验证信号给边界值**：避免"收敛/走扩"二元模糊，给 -3000 / -4000 / -4500 三档具体触发器
5. **加 ⚠ 切忌提醒**：对冲「按建议操作却忽略前提」的风险

## 报告长这样

**商品晨报**（每天 7:30）：

![commodity morning]({img('commodity_morning_full')})

**美股日报**（每天 19:45）：

![us pre market]({img('us_pre_market_full')})

**单源架构数据流图**：改一个价表，三份报告自动同步

![workflow]({img('workflow-diagram')})

## 为什么值得开源

**写代码本身不是壁垒，研究逻辑才是**——但**「能被客户用起来的研报架构」是一种稀缺的标准**。

我希望这份开源能让同行少走 8 个月的弯路：
- 用同样的「单源架构」，你的工作流不会腐烂
- 用同样的「客户级 Actionable」，你的客户真正能行动
- 用同样的「零硬编码凭证」，你的开源仓库不会被迫改名或者改历史

## 项目信息

- **仓库**：https://github.com/{REPO}?utm_source=zhihu
- **语言**：Python 3.10+（纯标准库，Excel 用 openpyxl）
- **License**：MIT
- **5,400 行代码 / 5 篇深度文档 / 2 份真实示例报告**
- **GitHub Actions**：每次 push 跑 Python 语法校验 + 凭证扫描
- **零外部依赖**：所有数据源（新浪期货、东财、Yahoo、SMM、Mysteel）都是公开接口

---

🤝 **征求**: 期货/大宗商品/美股方向的同行，欢迎提 Issue 讨论你们行业的 Actionable 写法。

⭐ **如果觉得有用，求个 star** —— 你的支持是我继续把工作流打磨下去的最大动力。

> ⚠️ 免责声明：项目内容仅供参考与学习，不构成投资建议。期货交易风险极高，请独立判断。
"""


# ---------- X / Twitter 精炼版 ----------

X = f"""把期货经纪日常做成了开源：商品晨报 07:30 + 美股日报 19:45，5400 行 Python。

三个不一样的点：
1. 客户级 Actionable（L1 分析 → L2 咨询 → L3 行动，量化参数 + 切忌框）
2. 单源架构（硅链/锂链/主报三份报告共用 CONTEXT）
3. 零硬编码凭证（QQ 授权码从 Keychain 取 + CI 自动扫）

https://github.com/{REPO}?utm_source=x

#期货 #开源 #WorkBuddy
"""


def main():
    outputs = {
        "v2ex.md": V2EX,
        "zhihu.md": ZHIHU,
        "x.md": X,
    }
    for name, content in outputs.items():
        path = os.path.join(OUTPUT_DIR, name)
        with open(path, "w") as f:
            f.write(content)
        size = os.path.getsize(path)
        print(f"✅ {path}  ({size} bytes,  {size//1024} KB)")

    # 元信息
    meta = f"""# 发帖文案元信息

- 生成时间: {date.today().isoformat()}
- 输出目录: {OUTPUT_DIR}
- 图片床: jsDelivr CDN (https://cdn.jsdelivr.net/gh/{REPO}@main/)
- 仓库源 URL: https://github.com/{REPO}

## 文件清单

| 文件 | 目标平台 | 字数 | 风格 |
|---|---|---|---|
| v2ex.md | V2EX 技术社区 | ~1300 | 技术硬核 + 推送踩坑清单 |
| zhihu.md | 知乎 | ~1800 | 业务故事 + 客户级 Actionable 5 条铁律 |
| x.md | X / Twitter | ~280  | 3 段 hook + 标签 |

## 注意事项

1. **图片外链稳定** — jsDelivr CDN 比 raw.githubusercontent.com 命中率更高（知乎对 raw 反盗链）
2. **链接追踪** — 各平台 URL 带 ?utm_source=xxx，方便 GitHub Insights 看来源
3. **建议手工发布** — 自动发布各平台都易封号，建议每个平台复制粘贴
4. **先 star 再发帖** — 项目 star < 10 时 V2EX/知乎带仓库链接容易被踩，先内部找 3-5 个朋友点 star
"""
    meta_path = os.path.join(OUTPUT_DIR, "README.md")
    with open(meta_path, "w") as f:
        f.write(meta)
    print(f"✅ {meta_path}")


if __name__ == "__main__":
    main()
