# -*- coding: utf-8 -*-
"""美股盘前战略版 2026-09-04 (automation-1787700114240) — 详细版（合并盘后战略复盘）
X = 9/4 周五（今夜交易日，20:30 非农开盘前落地 → event-drive）；X-1 = 9/3 周四（昨夜交易日，完整收盘复盘）
数据基准：9/3 美东收盘（新华社/新华财经/中国金融信息网/华尔街见闻/东财/每经/Vista/Investrade 多源交叉验证）+ 9/4 盘前实时（新浪外盘期货 19:46 GMT+8）
"""
import os

OUT_DIR = '/Users/shuhaihong/Documents/workbuddy/outputs'
os.makedirs(OUT_DIR, exist_ok=True)
X_DATE = '2026-09-04'
X1_DATE = '2026-09-03'
OUT = os.path.join(OUT_DIR, f'市场温度_盘前_{X_DATE}.html')

UP = '#C0392B'    # 涨-红（中国惯例）
DOWN = '#1E8449'  # 跌-绿

CSS_BASE = "font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;"

# ---------------- 顶头条 ----------------
hero = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="background:linear-gradient(135deg,#1a2a4a 0%,#2c3e6b 100%);border-radius:12px 12px 0 0;">
<tr><td style="padding:22px 28px 10px 28px;{CSS_BASE}">
  <div style="color:#9fb4d8;font-size:13px;letter-spacing:2px;">美股盘前战略版 · 详细版（已合并盘后复盘）</div>
  <div style="color:#ffffff;font-size:26px;font-weight:700;margin-top:6px;">【美股盘前】{X_DATE} 周五</div>
  <div style="color:#c8d6ee;font-size:13px;margin-top:4px;">昨夜 X-1 = {X1_DATE} 周四（美东收盘）完整复盘 ｜ 今夜 X = {X_DATE}（ET 09:30 开盘；20:30 GMT+8 非农先行）</div>
</td></tr>
<tr><td style="padding:0 28px 22px 28px;{CSS_BASE}">
  <div style="background:rgba(255,255,255,0.08);border-radius:10px;padding:14px 16px;margin-top:8px;">
    <div style="color:#ffd97a;font-size:15px;font-weight:700;">🌡️ 核心温度计：沃勒「给反通胀一个机会」+ 加息概率腰斩 + 金银双爆 → 🟢 risk-on 修复，但今夜 <b>⚡ event-drive</b>（非农开盘前 1 小时落地）</div>
    <div style="color:#e8eef8;font-size:13px;margin-top:8px;line-height:1.7;">
      昨夜主逻辑一句话：<b style="color:#ffd97a;">沃勒一句「给反通胀一个机会」把 9 月加息概率从 63.2% 打到 50.4%，2Y -3.5bp 领跌、美元破 99，标普 +1.06% 创 8/4 以来最大单日涨幅、距历史收盘高点不足 0.7%；金银暴涨（金 +2.39% 创近月最大涨幅）、VIX -5.9% 破 15——但 ISM 支付价格 72.6 创 2022/10 来最高，反弹地基是「利率缓解」而非「通胀解决」。</b>
    </div>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:12px;">
      <tr style="{CSS_BASE}font-size:13px;text-align:center;color:#fff;">
        <td style="background:rgba(255,255,255,0.10);border-radius:8px;padding:8px 4px;">🇺🇸 SPX<br><b style="color:{UP};">7747.71 +1.06%</b></td>
        <td style="width:8px;"></td>
        <td style="background:rgba(255,255,255,0.10);border-radius:8px;padding:8px 4px;">💻 纳指<br><b style="color:{UP};">26584.06 +1.40%</b></td>
        <td style="width:8px;"></td>
        <td style="background:rgba(255,255,255,0.10);border-radius:8px;padding:8px 4px;">🏭 道指<br><b style="color:{UP};">53686.11 +1.18%</b></td>
        <td style="width:8px;"></td>
        <td style="background:rgba(255,255,255,0.10);border-radius:8px;padding:8px 4px;">🔬 罗素<br><b style="color:{UP};">2968.27 +0.51%</b></td>
        <td style="width:8px;"></td>
        <td style="background:rgba(255,255,255,0.10);border-radius:8px;padding:8px 4px;">🛢️ WTI<br><b style="color:{UP};">91.67 +0.73%</b></td>
      </tr>
      <tr><td colspan="9" style="height:8px;"></td></tr>
      <tr style="{CSS_BASE}font-size:13px;text-align:center;color:#fff;">
        <td style="background:rgba(255,255,255,0.10);border-radius:8px;padding:8px 4px;">🥇 COMEX金<br><b style="color:{UP};">4520.2 +2.39%</b></td>
        <td></td>
        <td style="background:rgba(255,255,255,0.10);border-radius:8px;padding:8px 4px;">🪙 银<br><b style="color:{UP};">67.59 +3.24%</b></td>
        <td></td>
        <td style="background:rgba(255,255,255,0.10);border-radius:8px;padding:8px 4px;">🔩 铜<br><b style="color:{UP};">6.66 +0.8%</b></td>
        <td></td>
        <td style="background:rgba(255,255,255,0.10);border-radius:8px;padding:8px 4px;">📈 10Y<br><b style="color:{DOWN};">4.766% -1.2bp</b></td>
        <td></td>
        <td style="background:rgba(255,255,255,0.10);border-radius:8px;padding:8px 4px;">😱 VIX<br><b style="color:{DOWN};">14.30 -5.92%</b></td>
      </tr>
    </table>
    <div style="color:#e8eef8;font-size:13px;margin-top:12px;line-height:1.7;">
      今夜开盘倾向：<b style="color:#ffd97a;">⚡ event-drive（非农 20:30 GMT+8 开盘前 1 小时落地，全场胜负手）</b>——①VIX9D ~13.5 无恐慌（但=对冲薄）②US30Y ~5.245% 持平、利率端已定价「鸽」③NQ 期货 +0.50% 领涨 / RTY 温和（高贝塔科技惯性、小盘掉队）。<b style="color:#ffb0a0;">盘前注意：油 90.71 / 金 4515 / 银 67.5 同步小幅回吐——昨夜大涨后的获利盘在非农前了结；对冲薄 + 双向数据风险 = 波动放大器。</b>
    </div>
  </div>
</td></tr>
</table>
"""

# ---------------- 综合温度 ----------------
temp_box = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px;{CSS_BASE}">
<tr><td style="background:#fff8dc;border:1px solid #f0dfa8;border-radius:10px;padding:16px 20px;">
  <div style="font-size:15px;font-weight:700;color:#8a6d1a;">☀️ 昨夜综合温度（{X1_DATE} 美东收盘）</div>
  <div style="font-size:13px;color:#4a4a3a;line-height:1.8;margin-top:8px;">
    ① 沃勒「有条件鸽派」主导全场：若 8 月通胀延续放缓，倾向支持 9 月维持 3.50%-3.75% 不变（但「通胀可能不需要大幅加速就促使我支持收紧」）→ <b>9 月加息概率一日 63.2%→50.4%，几乎成抛硬币</b>；2Y -3.5bp 连续两日回撤、短端领跌 = 加息溢价加速回吐，DXY 破 99（-0.58%）、USDJPY -1.83% 至 155.8（BOJ 加息预期共振）。<br>
    ② 三大指数两连涨：标普 +1.06%（8/4 以来最大单日涨幅、距历史收盘高点不足 0.7%）、纳指 +1.40%、道指 +1.18%（+624 点）；<b>高贝塔接管行情</b>——七巨头 +2.0%，特斯拉 +5.42%（Cybercab 无人出租车发布会）、SNOW +16.55%（AI 编程代理拉动销售）、SpaceX +6.42%、NVDA +1.8%（130 亿美元收购 Hugging Face）。<br>
    ③ 反弹地基不牢的三个证据：ISM 服务业 55.4 超预期强劲、<b>支付价格分项 72.6 创 2022/10 以来最高</b>（通胀黏性未解）；小盘 RUT 仅 +0.51% 掉队（前日领涨惯性未续）；能源板块 -0.72% 领跌。<b>这是「利率缓解估值修复」而非「盈利上修」——今晚非农 + 9/11 CPI 才是裁决者。</b><br>
    ④ 金银双爆：COMEX 金 +2.39% 至 4520.2（近一月最大单日涨幅，现货盘中 4511）、银 +3.24% 至 67.59，金矿股两三倍弹性（金田 +7%）——收益率回落 + 美元走软 + 央行 7 月净购金 23 吨三重共振；中信建投：金价第二轮趋势性上涨仍需等实质性宽松确认。<br>
    ⑤ 暗流未消：黑石与 Cliffwater 同日将私募信贷基金赎回上限砍至 5%（赎回请求至少超额度两倍）=<b>「排队挤兑」信号</b>；30Y 固定房贷利率 6.71% 创一年多新高；比特币 +5.3% 破 81000——高利率裂缝处的风险并没有被昨夜反弹解决。
  </div>
</td></tr>
</table>
"""

# ---------------- 战略复盘 5 节 ----------------
def sec(title, body):
    return f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:12px;{CSS_BASE}">
<tr><td style="background:#f7f9fc;border:1px solid #e2e8f2;border-radius:10px;padding:14px 20px;">
  <div style="font-size:14px;font-weight:700;color:#1a2a4a;">{title}</div>
  <div style="font-size:13px;color:#333;line-height:1.8;margin-top:6px;">{body}</div>
</td></tr>
</table>"""

review = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;{CSS_BASE}">
<tr><td>
  <div style="font-size:17px;font-weight:700;color:#1a2a4a;border-left:4px solid #2c5fa8;padding-left:10px;">🔍 昨夜战略复盘（X-1 = {X1_DATE}，五项深度对比）</div>
</td></tr>
</table>
""" + sec(
    "（A）板块轮动确认：「小盘惯性」失败，「高贝塔科技接管」❌",
    f"11 板块 <b style='color:{UP};'>8 涨 3 跌</b>：非必需消费 +1.58%、金融 +1.55% 领涨（特斯拉 +5.42% + 高盛 +3%/花旗 +3%/摩士丹利 +2%），能源 -0.72%、材料 -0.46% 领跌——<b>金矿材料股暴涨但材料板块整体下跌</b>（金田 +7% 被工业金属链拖累对冲），结构分裂。罗素 2000 +0.51% 明显落后 SPX +1.06%（RUT/SPX = 0.48）——9/2 盘前预期「小盘领涨惯性」<b>失败</b>：沃勒鸽派直接点燃的是成长/高贝塔（七巨头 +2.0%），而非 9/2 的「利率见顶交易」（小盘/银行/材料）。<b>教训：非农前哨信号驱动的反弹，资金先回补流动性最好的大盘成长，小盘补涨要等数据确认后的第二棒。</b>银行股普涨（+1~3%）倒是延续了利率回落逻辑——轮动不是反转，是「两条利率交易线并行」。"
) + sec(
    "（B）VIX 曲线整体位移：整体下移、破 15 关键位 ✅",
    f"VIX 15.38 → 14.30（<b style='color:{DOWN};'>-5.92%</b>，回吐 9/1 全部涨幅、跌破 15）；前端 9D ~14.0 → ~13.5（估）同步回落，3M ~18.0（估）微降，1Y ~22.3（估）纹丝未动。<b>曲线整体下移 + 1Y 完全平坦位移 = 市场把昨夜反弹定性为「加息恐慌降温」而非「系统性转向」</b>；contango 维持、前端无倒挂。VIX 期货 15.95（昨结 16.14，-1.2%）确认期货端同步降温。关键提示：14.3 的 VIX 在非农前夜偏低——<b>「无恐慌」与「无对冲」只有一线之隔</b>，今晚双向波动风险大于表面读数。今夜盯 VIX 能否守住 14：跌破 = 鸽派定价加深；跳回 15.5 上方 = 非农意外触发对冲回补。"
) + sec(
    "（C）信用-主权协调：JNK 终于跟涨，信用确认但「里子」有裂缝 ⚠️",
    f"9/2「JNK 95.21 持平 vs 股票涨」的滞后，昨夜以 <b>JNK 95.30 +0.09%</b> 的温和跟涨方式完成确认（9/1 -0.88% → 9/2 持平 → 9/3 转涨，信用修复三部曲走完）；HYG（估 +0.05~0.1%）同向 = HY 内部 BB/B dispersion 低、无选择性抛售。主权端 2Y -3.5bp/10Y -1.2bp/30Y -1.37bp 全线回落配合，2s10s +43.0bp（+2.7bp）连续第二日陡峭化 = 信用与主权定价重新同步向「鸽」。<b>但「里子」有裂缝：黑石/Cliffwater 私募信贷限赎 5%（请求超 2 倍）</b>——公募 HY ETF 的平静与私募信贷的挤兑红灯并存，30Y 房贷 6.71% 一年新高说明实体融资端并未感受到「鸽派」。AI 数据中心发债潮挤压信用市场的结构性问题依旧悬而未决。"
) + sec(
    "（D）量价结构：放量长阳、收在区间 87% 分位，真突破倾向 ✅",
    f"SPX 日内区间 7686.71-7756.76，收盘 7747.71 位于区间约 <b>87% 分位（接近日高）</b>，且为 <b>8/4 以来最大单日涨幅</b>——开盘即涨、全天强势、无尾盘跳水，量价结构优于 9/2 的深 V（那日是「低位反包」，昨日是「放量推进」）。上方缺口参照：7756.76（昨夜高点）→ 7800（历史高点 7816.70 下方的心理位，距历史收盘高点仅 0.7%）；下方 7686.71（昨夜低点）为第一止损参照，7666（9/2 收盘）为趋势分界。<b>警示项：SPX 已连续 26 个交易日无 1% 单日跌幅（9/2 截止口径）+ 高盛警告 9 月季节性最弱时段（SPX 9 月负收益概率 55%、平均回撤 -4.7%）</b>——「低波 + 高位 + 事件日」组合下，真突破与空头陷阱只有非农一个变量的距离。"
) + sec(
    "（E）财报 / 事件 digest：沃勒定调「抛硬币」，数据面「分裂」",
    "① <b>沃勒讲话是全场唯一主角</b>：通胀「终于看到放缓迹象」+ 若数据延续则支持 9 月按兵不动，但保留加息选项——本质是给数据留窗口而非政策转向。② <b>ISM 服务业 55.4</b>（前 54.1、预期 54.2-54.3）：业务活动 61.7、新订单 60.9（3.5 年新高）= 需求强；但<b>支付价格 72.6 创 2022/10 来最高</b>（前 70.3）+ 就业分项 47.8 仍在收缩 = 滞胀式分裂，恰好是「好坏参半、非农裁决」的格局。③ <b>初请 20.6 万</b>（预期 20.5 万、前值 20.4 万）连续微升 + Challenger 裁员 5.3 万（2022 年来最低 8 月值）=「低招低裁」温和降温，与 ADP 走弱同向，为非农下行风险背书。④ <b>7 月贸易逆差 886 亿美元（+24.4%，一年多最高）</b>——出口下滑进口增加，对 GDP 与再通胀均是边际利空。⑤ NVDA 130 亿美元收购 Hugging Face（从「卖铲子」卡位 AI 平台层）、微软/Meta/谷歌事件面平静——AI 叙事无利空。⑥ <b>私募信贷黑石/Cliffwater 限赎</b>是昨夜最被低估的信用头条。"
)

# ---------------- 对账表 ----------------
def row3(exp, act, ok, color):
    bg = '#eaf7ee' if ok else '#fdeeee'
    return f"""<tr>
<td style="border:1px solid #dde5ef;padding:8px 12px;font-size:12.5px;color:#333;width:34%;">{exp}</td>
<td style="border:1px solid #dde5ef;padding:8px 12px;font-size:12.5px;color:#333;width:48%;">{act}</td>
<td style="border:1px solid #dde5ef;padding:8px 12px;font-size:13px;font-weight:700;text-align:center;background:{bg};color:{color};width:18%;">{ok}</td>
</tr>"""

recon = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;{CSS_BASE}">
<tr><td>
  <div style="font-size:17px;font-weight:700;color:#1a2a4a;border-left:4px solid #2c5fa8;padding-left:10px;">⚡ 与 9/3 盘前报告对账</div>
  <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:10px;border-collapse:collapse;">
    <tr style="background:#2c3e6b;color:#fff;{CSS_BASE}font-size:13px;">
      <td style="padding:8px 12px;border:1px solid #2c3e6b;">盘前预期（9/3 19:45）</td>
      <td style="padding:8px 12px;border:1px solid #2c3e6b;">昨夜实际</td>
      <td style="padding:8px 12px;border:1px solid #2c3e6b;text-align:center;">判定</td>
    </tr>
    {row3("基调 🟢 偏 risk-on（弱确认）", "三大指数大涨两连涨、标普创 8/4 来最大单日涨幅——risk-on 不仅延续而且强化", "✅", UP)}
    {row3("① VIX9D ~14.0 前端未再抬升", "VIX 14.30 -5.92% 破 15、9D ~13.5 前端同步回落——「反弹持续性第一道闸门通过」如预期兑现", "✅", UP)}
    {row3("② US30Y 5.245% (-1.5bp) 鸽派延续", "30Y 收 5.2455% (-1.37bp)——与预期分毫不差；10Y 4.766% (-1.2bp) 鸽派延续", "✅", UP)}
    {row3("③ RTY/ES≈1.0 小盘领涨惯性延续", "RUT 仅 +0.51% 掉队（RUT/SPX = 0.48），高贝塔科技接管——「利率见顶交易」第二棒没有轮到小盘，资金直接回补大盘成长", "❌", DOWN)}
    {row3("「AVGO 盘前 -2.2% 拖累半导体」兑现", "AVGO 收 -2.74%、ASML -2%，SOX 全天仅 +0.11% 大幅跑输——AI 链 high bar 精准命中", "✅", UP)}
    {row3("伊朗袭击 → 油价地缘溢价维持", "WTI 盘中 93.13 冲高（+2.5%）后大幅回吐、收 +0.73% 至 91.67；溢价边际钝化第三日，方向对但弹性递减", "🟡 半对", '#b8860b')}
  </table>
  <div style="font-size:12.5px;color:#666;margin-top:8px;line-height:1.7;">对账结论：<b style="color:{UP};">4.5/6 正确</b>（4✅ + 1 半对 + 1 ❌）。核心失误模式：连续第三次对「小盘轮动」的时点判断失准——9/1 误判「小盘抗跌」、9/2 正确、9/3 又误判「惯性延续」。<b>教训：数据事件（非农/讲话）驱动的反弹中，第一棒永远是流动性最好的大盘成长，小盘是第二棒（需数据确认后），把「板块惯性」默认成「延续」不如把「事件性质」作为轮动的第一变量。</b></div>
</td></tr>
</table>
"""

# ---------------- 7 步完整表 ----------------
def step_table(no, title, rows):
    trs = ""
    for label, val, arrow, note in rows:
        color = UP if arrow == '↑' else (DOWN if arrow == '↓' else '#555')
        trs += f"""<tr style="{CSS_BASE}font-size:12.5px;">
<td style="border:1px solid #dde5ef;padding:7px 12px;color:#555;width:22%;background:#f7f9fc;">{label}</td>
<td style="border:1px solid #dde5ef;padding:7px 12px;font-weight:700;color:{color};width:26%;">{val} {arrow}</td>
<td style="border:1px solid #dde5ef;padding:7px 12px;color:#333;line-height:1.6;">{note}</td>
</tr>"""
    return f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:12px;{CSS_BASE}">
<tr><td>
  <div style="font-size:14.5px;font-weight:700;color:#1a2a4a;background:#eef3fa;border-radius:8px 8px 0 0;padding:9px 14px;border:1px solid #dde5ef;">{no} {title}</div>
  <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">{trs}</table>
</td></tr>
</table>"""

steps = step_table("①", "利率与债券（9/3 收盘）", [
    ("2Y / 10Y / 30Y", "4.334% / 4.766% / 5.245%", "↓", "2Y -3.5bp（连续两日回撤）/ 10Y -1.2bp（盘中 20:54 GMT+8 刷日低 4.73%）/ 30Y -1.37bp——沃勒表态后收益率全线下行"),
    ("曲线形态", "2s10s 43.0bp 陡峭化 (+2.7bp)", "→", "2Y 降更多 = 加息溢价加速回吐主导；短端对政策预期最敏感，连续两日领跌"),
    ("当日利率大事", "沃勒「有条件鸽派」+ ISM 支付价格 72.6", "→", "加息概率 63.2%→50.4%（抛硬币）；但 ISM 支付价格创 2022/10 来最高 = 通胀黏性未解，9/11 CPI 是第二裁决者"),
    ("全球共振", "DXY 破 99（-0.58%）；日债全线回落", "↓", "USDJPY -1.83% 至 155.8（BOJ 加息预期）；法债 -4.8bp/德债 -3.3bp/英债 -9.6bp，全球发达国家长端抛售潮显著缓和"),
]) + step_table("②", "指数与板块（9/3 收盘）", [
    ("SPX / 纳指 / 道指", "7747.71 / 26584.06 / 53686.11", "↑", "+1.06% / +1.40% / +1.18%（+624 点），两连涨；SPX 收在日内区间 87% 分位、距历史收盘高点不足 0.7%"),
    ("罗素2000", "2968.27", "↑", "仅 +0.51% 明显掉队（前日 +1.13% 领涨）——高贝塔科技接管，小盘是「第二棒」"),
    ("板块前三", "非必需消费 +1.58% / 金融 +1.55% / 通信科技", "↑", "特斯拉 +5.42%（Cybercab 发布会）、SNOW +16.55%、SpaceX +6.42%、META +3%、高盛 +3%、花旗 +3%、摩士丹利 +2%"),
    ("板块后三", "能源 -0.72% / 材料 -0.46%", "↓", "能源股全线走低（XOM -1%+、斯伦贝谢 -1%+）= 油价冲高回落 + 通胀溢价钝化；金矿股逆势暴涨（金田 +7%/哈莫尼 +6%）造成材料板块内部分裂"),
    ("个股焦点", "AVGO -2.74% / ASML -2% / Ciena -10.36%", "↓", "SOX 仅 +0.11% 大幅跑输 = AI 硬件链 high bar（AVGO 指引 in-line 后仍在定价）；NVDA +1.8%（130 亿美元收购 Hugging Face）、ARM +3%、中概金龙 -0.81%"),
]) + step_table("③", "石油（9/3 收盘）", [
    ("WTI / Brent", "91.67 / 95.92", "↑", "+0.73% / +0.30%；WTI 盘中 93.13 冲高 → 89.60 回踩 → 收 91.67，日内 3.8 美元宽幅震荡 = 地缘溢价定价高度分歧"),
    ("供需面", "OPEC+ 周日会议临近", "→", "核心成员或坚持 10 月配额不变、闲置产能恢复推迟至明年初（诺瓦克：不会讨论下调配额）；全球炼油几无闲置产能 + 俄延长柴油出口限制"),
    ("异常判定", "无 &gt;3% 收盘异动（盘中曾 +2.5%）", "→", "地缘溢价边际钝化第三日；花旗上调 Q3 布油预测至 86 美元（市价调整后）——机构与现货价差仍大"),
]) + step_table("④", "黄金·白银·铜（9/3 收盘）", [
    ("COMEX 金 / 银", "4520.2 / 67.585", "↑", "+2.39%（+105.7 美元，近一月最大单日涨幅）/ +3.24%；现货金 4473.3 +1.94%（盘中 4511.7，自 4281.7 一个月低点 V 形修复）"),
    ("铜（COMEX / LME）", "6.66 美元/磅 / 14334 美元", "↑", "+0.8% / +118 美元——跟随「利率回落+风偏回升」温和修复，弹性远小于贵金属"),
    ("金铜比判定", "金涨银涨铜小涨", "↑", "贵金属领涨 + 铜温和跟随 = 「利率回落驱动的全面商品修复」而非典型滞胀背离；央行 7 月净购金 23 吨 + 筹码出清是额外催化"),
]) + step_table("⑤", "谷物（9/3 收盘）", [
    ("小麦 / 玉米 / 大豆", "752.25 / 539.25 / 1314.50", "↓", "-2.81% / -0.78% / +0.32%；小麦领跌（盘中 730.5，全天 V 形）、接近 3% 剧烈波动阈值——供应担忧缓解后的获利回吐"),
    ("结构分化", "大豆逆势收涨（豆粕 +1.25%）", "→", "彭博谷物指数 -0.85% V 形走势（22:00 曾刷日低 34.49）；粮油共振消退——油价冲高回落 + 谷物回吐同步发生"),
]) + step_table("⑥", "VIX 期限结构（9/3 收盘）", [
    ("VIX 现货", "14.30", "↓", "-5.92%，回吐 9/1 全部涨幅、跌破 15 关键位——9/1 恐慌脉冲完全消化"),
    ("9D / 3M / 1Y", "~13.5 / ~18.0 / ~22.3（估）", "↓", "前端同步回落、1Y 未动；VIX 期货 15.95（-1.2%）确认——contango 维持、整体下移 = 恐慌消退而非扩散"),
    ("非农前夜判定", "对冲薄是最大暗风险", "⚠", "14.3 的 VIX 在非农前夜偏低——「无恐慌」≠「无风险」；今夜 VIX 守 14 = 鸽派定价加深，跳回 15.5 上方 = 意外触发对冲回补"),
]) + step_table("⑦", "信用·高收益债（9/3 收盘 + 盘后）", [
    ("JNK 收盘", "95.30 +0.09%", "↑", "9/1 -0.88% → 9/2 持平 95.21 → 9/3 转涨 95.30——「信用修复三部曲」走完，终于跟上股票反弹"),
    ("HYG 对比", "~79.2（估 +0.1%）", "→", "JNK（BB 偏多）与 HYG（B 偏多）同向微涨 = HY 内部 BB/B dispersion 低，无选择性抛售"),
    ("YTM / 52 周", "~6.6% / 94.49-97.24", "→", "票息缓冲仍厚；利率回落后 HY 收益率吸引力边际下降但信用利差未走扩"),
    ("⚠️ 私募信贷暗流", "黑石/Cliffwater 限赎至 5%", "↓", "赎回请求至少超上限两倍 =「排队挤兑」信号——公募 HY ETF 平静 vs 私募信贷红灯并存；数万亿级市场从未走完完整信用周期，是比商业地产更难拆的雷")
])

# ---------------- JNK 附段 ----------------
jnk = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px;{CSS_BASE}">
<tr><td style="background:#f4f9f6;border:1px solid #cfe6d8;border-radius:10px;padding:14px 20px;">
  <div style="font-size:14px;font-weight:700;color:#1a2a4a;">🛡️ JNK 信用附段（盘后跟踪）</div>
  <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:8px;border-collapse:collapse;{CSS_BASE}font-size:12.5px;">
    <tr style="background:#eef3fa;color:#1a2a4a;font-weight:700;">
      <td style="border:1px solid #dde5ef;padding:6px 10px;">指标</td><td style="border:1px solid #dde5ef;padding:6px 10px;">读数</td><td style="border:1px solid #dde5ef;padding:6px 10px;">解读</td>
    </tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">JNK 收盘（9/3）</td><td style="border:1px solid #dde5ef;padding:6px 10px;color:{UP};font-weight:700;">95.30 +0.09%</td><td style="border:1px solid #dde5ef;padding:6px 10px;">连续三日「独跌→持平→跟涨」，信用与股票重新同步 = 鸽派定价获得信用端确认</td></tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">盘后（~18:30 EDT）</td><td style="border:1px solid #dde5ef;padding:6px 10px;">~95.30（估，流动性 ~1K 手量级）</td><td style="border:1px solid #dde5ef;padding:6px 10px;">盘后无异动；HY 流动性薄，真实信号以收盘为准</td></tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">NAV / YTM</td><td style="border:1px solid #dde5ef;padding:6px 10px;">~95.2-95.3 / ~6.6%</td><td style="border:1px solid #dde5ef;padding:6px 10px;">溢价交易收窄至接近平价；YTM 在利率回落后对「票息猎人」吸引力边际下降</td></tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">52 周区间</td><td style="border:1px solid #dde5ef;padding:6px 10px;">94.49 - 97.24</td><td style="border:1px solid #dde5ef;padding:6px 10px;">现价处于区间 18% 分位（偏低）——若非农鸽派确认，向上空间 &gt; 向下</td></tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">HYG vs JNK</td><td style="border:1px solid #dde5ef;padding:6px 10px;">同向微涨（估 +0.1%）</td><td style="border:1px solid #dde5ef;padding:6px 10px;">BB/B dispersion 低 = 无「以质换质」抛售；但黑石/Cliffwater 私募限赎提醒：ETF 平静 ≠ 信用健康</td></tr>
  </table>
</td></tr>
</table>
"""

# ---------------- 亚欧夜盘 ----------------
asia = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px;{CSS_BASE}">
<tr><td style="background:#f7f9fc;border:1px solid #e2e8f2;border-radius:10px;padding:14px 20px;">
  <div style="font-size:14px;font-weight:700;color:#1a2a4a;">🌏 亚欧接续（欧股 9/3 收盘 + 亚太 9/4 今日收盘）</div>
  <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:8px;border-collapse:collapse;{CSS_BASE}font-size:12.5px;">
    <tr style="background:#eef3fa;color:#1a2a4a;font-weight:700;">
      <td style="border:1px solid #dde5ef;padding:6px 10px;">市场</td><td style="border:1px solid #dde5ef;padding:6px 10px;">收盘</td><td style="border:1px solid #dde5ef;padding:6px 10px;">涨跌</td><td style="border:1px solid #dde5ef;padding:6px 10px;">解读</td>
    </tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">英国 FTSE100（9/3）</td><td style="border:1px solid #dde5ef;padding:6px 10px;">10831.52</td><td style="border:1px solid #dde5ef;padding:6px 10px;color:{UP};font-weight:700;">+0.70%</td><td style="border:1px solid #dde5ef;padding:6px 10px;">英债 10Y -9.6bp（5.134%）领跌全球 = 抛售潮缓和最猛；跟随美股风偏修复</td></tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">德国 DAX（9/3）</td><td style="border:1px solid #dde5ef;padding:6px 10px;">26003.32</td><td style="border:1px solid #dde5ef;padding:6px 10px;color:{UP};font-weight:700;">+0.63%</td><td style="border:1px solid #dde5ef;padding:6px 10px;">德债 10Y -3.3bp；STOXX600 +0.49% 全线走高</td></tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">法国 CAC40（9/3）</td><td style="border:1px solid #dde5ef;padding:6px 10px;">8286.40</td><td style="border:1px solid #dde5ef;padding:6px 10px;color:{UP};font-weight:700;">+0.07%</td><td style="border:1px solid #dde5ef;padding:6px 10px;">法债 -4.8bp；欧股昨日整体温和修复</td></tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">日经225（9/4 今日）</td><td style="border:1px solid #dde5ef;padding:6px 10px;">65020.94</td><td style="border:1px solid #dde5ef;padding:6px 10px;color:{UP};font-weight:700;">+1.26%</td><td style="border:1px solid #dde5ef;padding:6px 10px;">昨日 -0.17% 后补涨；日元 155.8 高位震荡（BOJ 加息预期未再升温）</td></tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">韩国 KOSPI（9/4）</td><td style="border:1px solid #dde5ef;padding:6px 10px;">6687.21</td><td style="border:1px solid #dde5ef;padding:6px 10px;color:{UP};font-weight:700;">+1.64%</td><td style="border:1px solid #dde5ef;padding:6px 10px;">台加权 +1.51%——亚太科技链强势跟随美股成长风偏</td></tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">恒生指数（9/4）</td><td style="border:1px solid #dde5ef;padding:6px 10px;">25650.87</td><td style="border:1px solid #dde5ef;padding:6px 10px;color:{UP};font-weight:700;">+1.74%</td><td style="border:1px solid #dde5ef;padding:6px 10px;">国企指数 +2.02%、恒科 +2.27% 领涨——中概修复但与昨夜金龙 -0.81% 背离，周五空头回补成分大</td></tr>
    <tr><td style="border:1px solid #dde5ef;padding:6px 10px;">上证指数（9/4）</td><td style="border:1px solid #dde5ef;padding:6px 10px;">3930.12</td><td style="border:1px solid #dde5ef;padding:6px 10px;color:{DOWN};font-weight:700;">-0.30%</td><td style="border:1px solid #dde5ef;padding:6px 10px;">A股独立行情：深成 -0.79%/创业板 -0.78%/科创50 -2%+——亚太普涨中唯一收跌，资金切向金融/贵金属（沪金沪银 +2%）</td></tr>
  </table>
  <div style="font-size:12.5px;color:#666;margin-top:8px;line-height:1.7;">接续判定：欧股昨夜「债市抛售缓和」型修复 → 亚太今日科技链普涨（韩/台/日/港），唯 A 股独跌（内因主导：科创 50 -2%+、资金切向防御与贵金属）。<b>今夜美股开盘前，全球风偏处于「修复已扩散至亚太、等非农盖章」状态；A 股的独立防御行情提示内资风险偏好与全球脱钩。</b></div>
</td></tr>
</table>
"""

# ---------------- 3 触发器 ----------------
def trig_row(name, val, judge, meaning, color):
    return f"""<tr style="{CSS_BASE}font-size:12.5px;">
<td style="border:1px solid #dde5ef;padding:8px 12px;font-weight:700;color:#1a2a4a;width:16%;background:#f7f9fc;">{name}</td>
<td style="border:1px solid #dde5ef;padding:8px 12px;width:24%;font-weight:700;color:{color};">{val}</td>
<td style="border:1px solid #dde5ef;padding:8px 12px;width:14%;text-align:center;font-weight:700;color:{color};">{judge}</td>
<td style="border:1px solid #dde5ef;padding:8px 12px;line-height:1.6;">{meaning}</td>
</tr>"""

triggers = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;{CSS_BASE}">
<tr><td>
  <div style="font-size:17px;font-weight:700;color:#1a2a4a;border-left:4px solid #2c5fa8;padding-left:10px;">🎯 今夜 3 个触发器（9/4 盘前 07:45 EDT 快照）</div>
  <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:10px;border-collapse:collapse;">
    <tr style="background:#2c3e6b;color:#fff;{CSS_BASE}font-size:13px;">
      <td style="padding:8px 12px;border:1px solid #2c3e6b;">触发器</td><td style="padding:8px 12px;border:1px solid #2c3e6b;">盘前读数</td><td style="padding:8px 12px;border:1px solid #2c3e6b;text-align:center;">方向</td><td style="padding:8px 12px;border:1px solid #2c3e6b;">含义</td>
    </tr>
    {trig_row("① VIX9D", "~13.5（VIX 期货 15.95 -1.2%）", "↓ 无恐慌", "前端连续第三日回落、无事件恐慌；但 14.3 的 VIX 在非农前夜 = 对冲薄——双向波动放大器，非农意外时保护不足", DOWN)}
    {trig_row("② US30Y", "~5.245% 持平（10Y 4.766% 持平）", "→ 已定价鸽", "利率端已把「沃勒鸽派」定价完毕，盘前无增量；非农强（&gt;10 万）→ 2Y 跳升 + 30Y 重上 5.27 = 鸽派定价一夜回吐", '#555')}
    {trig_row("③ NQ / ES", "NQ +0.50% 领涨 / ES +0.08% / YM -0.04%；RTY ~+0.15%（估）", "↑ 科技强", "高贝塔科技惯性延续（昨夜 NQ 现货 +1.40% 主导）；小盘温和掉队——「科技第一棒、小盘第二棒」结构未变", UP)}
    <tr style="{CSS_BASE}font-size:13px;background:#fff8dc;">
      <td colspan="4" style="border:1px solid #dde5ef;padding:10px 12px;"><b>总基调：⚡ event-drive（非农 20:30 GMT+8 开盘前 1 小时落地）</b>——三个触发器全部「偏多但无增量」：对冲薄 + 利率已定价鸽 + 科技惯性。今夜开盘基调 100% 由非农决定：数据符合预期（+3~9 万）→ risk-on 延续；强于预期（&gt;10 万）→ 加息重燃 risk-off；远弱于预期（&lt;3 万）→ 衰退 swap 转防御（注意「好消息=好消息、坏消息=坏消息」的模式切换风险）。<b>非农后 09:30 开盘前有 1 小时消化窗口——等定价完成再动手，不吃头 15 分钟的假突破。</b></td>
    </tr>
  </table>
</td></tr>
</table>
"""

# ---------------- 7 步速览 ----------------
quick = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px;{CSS_BASE}">
<tr><td style="background:#f7f9fc;border:1px solid #e2e8f2;border-radius:10px;padding:14px 20px;">
  <div style="font-size:14px;font-weight:700;color:#1a2a4a;">📊 今夜 7 步速览（单行版）</div>
  <div style="font-size:14px;line-height:2.0;margin-top:8px;color:#333;">
    ① 利率 <b>→</b>（10Y 4.766% / 30Y 5.245% 盘前持平，等非农）→
    ② 指数 <b style="color:{UP};">↑</b>（NQ +0.50% 领涨 / ES +0.08% / YM -0.04% / RTY ~+0.15% 弱；高贝塔科技惯性）→
    ③ 油 <b style="color:{DOWN};">↓</b>（WTI 90.71 -0.64%，昨夜 93.13 冲高后获利回吐）→
    ④ 金银铜 <b style="color:{DOWN};">↓→</b>（金 4515 -0.55% / 银 67.5 -0.31% 回吐、铜 666 → 持平——大涨后非农前了结）→
    ⑤ 谷物 →（豆 1314.75 平；麦昨夜 -2.81% 后夜盘平静）→
    ⑥ VIX <b style="color:{DOWN};">↓</b>（现货 14.30 昨收、VIX 期货 15.95 -1.2%、9D ~13.5——对冲薄）→
    ⑦ 日历 <b>⚡</b>（20:30 非农 +5.8 万预期 = 开盘前落地；9/7 劳工节休市、9/10 PPI、9/11 CPI、9/16 FOMC ~50%）
  </div>
</td></tr>
</table>
"""

# ---------------- 战术指令 ----------------
tactics = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px;{CSS_BASE}">
<tr><td style="background:#eaf7ee;border:1px solid #bfe3cc;border-radius:10px;padding:16px 20px;">
  <div style="font-size:15px;font-weight:700;color:#1e6b3a;">🔧 战术指令（今夜开盘开关）</div>
  <div style="font-size:13.5px;color:#1a3a26;line-height:1.8;margin-top:8px;background:#ffffff;border-radius:8px;padding:12px 14px;border:1px solid #d5ead8;">
    <b>⚡ event-drive（20:30 非农先行）：①VIX9D ~13.5↓ ②US30Y ~5.245%平 ③NQ +0.5%领涨/RTY弱。</b>非农 5-9 万 → risk-on 延续买科技/金融；&gt;10 万 → 加息重燃减仓；&lt;3 万 → 衰退 swap 转防御。开盘前等 1 小时消化窗口，不吃头 15 分钟假突破。
  </div>
  <div style="font-size:13px;color:#1a3a26;line-height:1.8;margin-top:10px;">
    <b>Actionable（非农三剧本）：</b>
    <ul style="margin:6px 0 0 18px;padding:0;">
      <li><b>剧本一「金发女孩」（+3~9 万、失业率 ≤4.3%、时薪 ≤0.3%）</b>：加息概率跌破 45% → risk-on 延续——科技（QQQ）、金融（KRE/WFC）、工业顺势加仓；SPX 突破 7756.76（昨夜高点）后看 7800 → 7816 历史高点；VIX &lt; 14 确认。</li>
      <li><b>剧本二「过热」（&gt;12 万 或时薪 &gt;0.4%）</b>：2Y 跳升 &gt;8bp + 30Y 重上 5.27 → 加息定价一夜回吐——减科技/小盘/高贝塔（昨夜涨最猛的 SNOW/特斯拉类回吐最快），9/1-9/2 的「利率冲击」剧本重演；防御 swap：必需消费 + 医疗。</li>
      <li><b>剧本三「熄火」（&lt;3 万 或失业率跳升）</b>：模式切换为「坏消息=坏消息」——衰退 swap：金/美债/防御优先，周期股与小盘先砍；但警惕「数据越差、降息预期越强」的对冲性反弹，等 10:00 后二次定价。</li>
      <li><b>⚠️ 切忌</b>：①对冲薄（VIX 14.3）+ 周一劳工节休市 + OPEC+ 周日会议——今夜不留重隔夜仓，杠杆减半；②非农公布后头 15 分钟的跳空多为假突破，09:45-10:00 二次定价后再执行。</li>
    </ul>
  </div>
</td></tr>
</table>
"""

# ---------------- 日历 ----------------
def cal_row(d, ev, imp, hedge):
    return f"""<tr style="{CSS_BASE}font-size:12.5px;">
<td style="border:1px solid #dde5ef;padding:7px 12px;font-weight:700;color:#1a2a4a;width:20%;background:#f7f9fc;">{d}</td>
<td style="border:1px solid #dde5ef;padding:7px 12px;line-height:1.6;">{ev}</td>
<td style="border:1px solid #dde5ef;padding:7px 12px;text-align:center;width:12%;color:{imp};font-weight:700;">{'高' if imp==UP else ('中' if imp=='#b8860b' else '低')}</td>
<td style="border:1px solid #dde5ef;padding:7px 12px;width:30%;">{hedge}</td>
</tr>"""

calendar = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;{CSS_BASE}">
<tr><td>
  <div style="font-size:17px;font-weight:700;color:#1a2a4a;border-left:4px solid #2c5fa8;padding-left:10px;">📅 未来一周日历（GMT+8）</div>
  <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:10px;border-collapse:collapse;">
    <tr style="background:#2c3e6b;color:#fff;{CSS_BASE}font-size:13px;">
      <td style="padding:8px 12px;border:1px solid #2c3e6b;">日期</td><td style="padding:8px 12px;border:1px solid #2c3e6b;">事件</td><td style="padding:8px 12px;border:1px solid #2c3e6b;text-align:center;">重要性</td><td style="padding:8px 12px;border:1px solid #2c3e6b;">对冲状态</td>
    </tr>
    {cal_row("9/4（今夜）", "20:30 8 月非农（预期 +5.8 万）+ 失业率 + 时薪——9 月 FOMC 前最重磅数据，开盘前 1 小时落地", UP, "VIX 14.3 对冲薄 = 意外时保护不足；非农前隔夜仓减半")}
    {cal_row("9/6（周日）", "OPEC+ 会议：核心成员或坚持 10 月配额不变、闲置产能恢复推迟至明年初", '#b8860b', "油价地缘溢价的周末变量；若意外增产 → 周一能化承压、WBI 回吐 90 下沿")}
    {cal_row("9/7（周一）", "美国劳工节休市（美股/美债休市）", '#b8860b', "流动性真空日：亚欧正常交易但无美盘接力，隔周末风险（OPEC+ + 非农余波）不宜重仓")}
    {cal_row("9/8（周二）", "NFIB 小企业信心", '#888', "低影响")}
    {cal_row("9/10（周四）", "8 月 PPI", UP, "再通胀叙事二次校准，油价传导首轮验证；ISM 支付价格 72.6 的映照")}
    {cal_row("9/11（周五）", "8 月 CPI——加息叙事的第二裁决者（沃勒条件的数据兑现窗口）", UP, "若 CPI 环比 ≥0.3% → 9 月加息概率重回 60%+，金银回吐 + 利率冲击二次探底")}
    {cal_row("9/16（周二）", "FOMC 决议——9 月加息概率 ~50%（抛硬币），沃勒已给「条件」，等 CPI 盖章", UP, "1Y VIX ~22.3 未动 = 长期对冲未建立，FOMC 前一周需回补")}
    {cal_row("持续跟踪", "美伊冲突（美军封锁 vs 伊朗基地袭击）；私募信贷赎回限制扩散风险（黑石/Cliffwater 之后有无跟风）", UP, "油价地缘溢价钝化中；私募信贷是信用端最大尾部")}
  </table>
</td></tr>
</table>
"""

# ---------------- 亚盘建议 ----------------
advice = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px;{CSS_BASE}">
<tr><td style="background:#f0f4fb;border:1px solid #c9d8ef;border-radius:10px;padding:16px 20px;">
  <div style="font-size:15px;font-weight:700;color:#1a2a4a;">🎯 周末 / 下周初亚盘·欧盘建议（可执行）</div>
  <ul style="font-size:13px;color:#333;line-height:1.9;margin:8px 0 0 18px;padding:0;">
    <li><b>非农剧本 → 下周一亚盘映射</b>：剧本一金发女孩 → 下周一亚太（日/韩/港）高开，但美股休市无接力，<b>冲高勿追</b>，等周二美盘确认；剧本二/三 → 下周一亚太直接承接美债/美元变动，科技链（韩存储/台半导体/港股恒科）首当其冲。</li>
    <li><b>OPEC+ 周日会议定周一能化基调</b>：维持配额不变 → 油价地缘溢价维持、周一能化/航运高开但注意「溢价钝化第三日」的追高刀口；意外增产 → 油价下探 90 → 周一石化/能化避开、航空/运输修复。</li>
    <li><b>金银回踩低吸而非追高</b>：金 4520/银 67.6 隔夜已回吐（盘前 4515/67.5），黄金股弹性两三倍回吐风险同步放大；非农鸽派确认前，回踩金 4450-4470 区间低吸优于 4500 上方追涨；下周一沪金沪银（今日 +2%）跟随外盘节奏，警惕高开低走。</li>
    <li><b>A 股独立防御行情延续观察</b>：今日亚太普涨唯 A 股独跌（科创 50 -2%+、资金切向金融/贵金属）——若非农 risk-on、A 股仍未跟涨，则确认内资风偏脱钩，下周配置端避开高位科技连板、关注证券/保险/贵金属低位承接（沪金沪银 +2% 已在交易「全球宽松+避险」双逻辑）。</li>
    <li><b>私募信用警报列入周末检查项</b>：黑石/Cliffwater 限赎之后，周末若有同类产品跟风限制赎回的新闻 → 下周信用端（JNK/HYG/地产债）降杠杆优先级提到最高，这是比非农更结构性的尾部风险。</li>
    <li><b>劳工节流动性纪律</b>：9/7 美股休市 = 全球市场「真空日」，日内波动被放大且无美盘修正——下周一无论多强的方向信号，仓位上限打七折。</li>
  </ul>
</td></tr>
</table>
"""

# ---------------- 落款 ----------------
footer = f"""
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;{CSS_BASE}">
<tr><td style="border-top:1px solid #dde5ef;padding:14px 4px;font-size:12px;color:#888;line-height:1.8;">
  数据来源：新华社 / 新华财经 / 中国金融信息网 / 华尔街见闻 / 东方财富 / 每日经济新闻 / 中新经纬 / Vista Partners / Investrade / SKN / 新浪外盘期货实时（19:46 GMT+8）/ WSJ-DJN（多源交叉验证，弃单源孤证）。VIX9D/VIX3M/VIX1Y/RTY 盘前及 HYG/NAV/YTM 为估值口径（标「估」）。<br>
  数字着色遵循中国惯例：涨/红、跌/绿。本报告为自动化生成（automation-1787700114240），仅供参考，不构成投资建议。<br>
  落款：{X_DATE} 19:45 GMT+8 ｜ 宁波 ｜ 波动率实验室 · 美股盘前战略版（合并盘后复盘详细版）
</td></tr>
</table>
"""

html_doc = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>【美股盘前】{X_DATE} · 详细版</title></head>
<body style="margin:0;padding:0;background:#eef1f5;{CSS_BASE}">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
<table width="1500" cellpadding="0" cellspacing="0" style="max-width:1500px;width:100%;background:#ffffff;margin:10px auto;border-radius:12px;box-shadow:0 1px 4px rgba(0,0,0,0.08);">
<tr><td style="padding:6px;">
{hero}
{temp_box}
{review}
{recon}
{steps}
{jnk}
{asia}
{triggers}
{quick}
{tactics}
{calendar}
{advice}
{footer}
</td></tr>
</table>
</td></tr></table>
</body></html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html_doc)
size = os.path.getsize(OUT)
print(f'HTML written: {OUT} ({size} bytes, {size/1024:.1f} KB)')
