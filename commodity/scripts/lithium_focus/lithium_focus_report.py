# -*- coding: utf-8 -*-
"""锂链专题晨报生成器 · 碳酸锂 主战场深挖版
用法: python3 lithium_focus_report.py [YYYY MM DD]
CONTEXT 从 commodity_morning_report.py 导入(单一数据源)——改价表/弱预期拆解/Actionable 只需改主报的 CONTEXT
输出: outputs/lithium_focus_YYYY_MM_DD.html
"""
import sys, os
from datetime import datetime

# 单一数据源: 从父目录的 commodity_morning_report.py 导入 CONTEXT
# 仓库目录结构: scripts/commodity_morning_report.py (主报)
#               scripts/lithium_focus/lithium_focus_report.py (本脚本)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from commodity_morning_report import CONTEXT

def main():
    if len(sys.argv) >= 4:
        y, m, dd = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        now = datetime.now()
        y, m, dd = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")

    lf = CONTEXT["lithium_fundamental"]
    lc_main = lf["LC2701"]; lc_far = lf["LC2705"]; lc_0909 = lf["LC2609"]
    lc_gap = lc_main[0] - lc_far[0]  # LC2701-LC2705 价差
    cur_diff = CONTEXT["lithium_signals"]["LC2701-LC2705"]

    RED, GREEN = "#d63031", "#00875a"
    def col(v):
        return RED if v > 0 else (GREEN if v < 0 else "#57606f")
    def sign(v, fmt="%+.1f"):
        return (fmt % v) if v is not None else "—"

    H = []
    A = H.append
    A('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>')
    A('<body style="margin:0;padding:0;background:#f4f6f8;font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\',\'Microsoft YaHei\',sans-serif;color:#24292e;">')
    A('<div style="max-width:680px;margin:0 auto;padding:16px 12px;">')

    # 头部(锂链主题色: 青绿, 区别于硅链金色)
    A('<div style="background:linear-gradient(135deg,#0b5e4a 0%,#1a9d7a 100%);border-radius:10px 10px 0 0;padding:22px 24px;color:#fff;">')
    A('<div style="font-size:12px;opacity:.85;letter-spacing:2px;">LITHIUM CHAIN FOCUS BRIEF · 主战场深挖</div>')
    A('<div style="font-size:24px;font-weight:700;margin:6px 0 4px;">锂链专题晨报</div>')
    wk_map = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    try:
        wd = wk_map[datetime(int(y), int(m), int(dd)).weekday()]
    except Exception:
        wd = "星期一"
    A('<div style="font-size:13px;opacity:.9;">%s年%s月%s日 · %s · 数据截至昨收盘+今日夜盘</div>' % (y, m, dd, wd))
    A('<div style="display:inline-block;margin-top:10px;background:rgba(255,255,255,.15);border-radius:20px;padding:5px 14px;font-size:13px;">🔋 碳酸锂(电池级/工业级) · 强现实28°C × 弱预期22°C — 强现实开始主导</div>')
    A('</div>')

    # 摘要条
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-top:none;padding:14px 24px;font-size:13px;line-height:1.7;">')
    A('<b style="color:#0b5e4a;">▎本专题定位</b><br>'
      '大宗商品晨报第七部分的独立深挖版——只看锂链。合约角色 → 强现实 vs 弱预期拆解 → 现货真实价表(7行) → 市场分割逻辑 → 价差时间窗口 → 分角色客户行动建议 → 四大验证信号(价差四档边界值)。')
    A('</div>')

    # 1 合约表
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #1a9d7a;padding-left:10px;margin-bottom:12px;">一 · 合约全景(广期所)</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">合约</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">最新</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">昨结</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">持仓(手)</th><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">角色</th></tr>')
    for c, last, settle, oiv, note in [
        ("LC2609", lc_0909[0], lc_0909[1], lc_0909[2], "临交割·持仓外溢到 2701"),
        ("LC2701", lc_main[0], lc_main[1], lc_main[2], "主力·反枧下窝+排产强势"),
        ("LC2705", lc_far[0], lc_far[1], lc_far[2], "远月承接·淡季预期受压, 价差 +%d" % lc_gap),
    ]:
        if last:
            chg = (last - settle) / settle * 100 if settle else 0
            A('<tr><td style="padding:6px 8px;border:1px solid #e1e4e8;font-weight:600;">%s</td>'
              '<td style="padding:6px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;">%s</td>'
              '<td style="padding:6px 8px;border:1px solid #e1e4e8;text-align:right;color:%s;">%s</td>'
              '<td style="padding:6px 8px;border:1px solid #e1e4e8;text-align:right;color:#57606f;">%s</td>'
              '<td style="padding:6px 8px;border:1px solid #e1e4e8;color:#57606f;">%s</td></tr>' % (
                  c, "{:,.0f}".format(last), col(chg), sign(chg), "{:,.0f}".format(oiv), note))
    A('</table>')
    # 强现实 vs 弱预期拆解
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:12px;color:#57606f;margin-top:10px;border-collapse:collapse;">')
    A('<tr><td style="padding:4px 8px 4px 0;width:100px;vertical-align:top;color:#8b949e;line-height:1.9;">强现实 vs 弱预期</td>'
      '<td style="padding:4px 0;line-height:1.5;">'
      '<table width="100%" cellpadding="3" cellspacing="0" style="font-size:12px;border-collapse:collapse;">'
      '<tr style="background:#fff5f0;">'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;width:64px;">合约</th>'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">两条逻辑各占一半的具体含义(脱口版)</th>'
      '</tr>')
    wr_marks = ["①", "②", "③", "④", "⑤"]
    for wr_c, wr_items in CONTEXT["lithium_weak_reality_rows"]:
        wr_body = "<br>".join("%s %s" % (wr_marks[i], s) for i, s in enumerate(wr_items))
        A('<tr><td style="padding:4px 6px;border:1px solid #e1e4e8;font-weight:700;color:#1a3a5c;">%s</td>'
          '<td style="padding:4px 6px;border:1px solid #e1e4e8;color:#57606f;line-height:1.7;">%s</td></tr>' % (wr_c, wr_body))
    A('</table>'
      '<div style="font-size:11px;color:#8b949e;margin-top:4px;">"博弈窗口"不是形容词 — 上面 5 条各对应可核实的库存/排产/事件数据。强现实(①②③)决定近月, 弱预期(④⑤)决定远月; 枧下窝复产是这两个逻辑谁占优的扳机。</div>'
      '</td></tr>')
    A('</table>')
    A('</div>')

    # 2 现货价表
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #0984e3;padding-left:10px;margin-bottom:12px;">二 · 现货价表(贸易商主要流通规格)</div>')
    A('<table width="100%" cellpadding="3" cellspacing="0" style="font-size:12px;border-collapse:collapse;">')
    A('<tr style="background:#f8f9fa;">'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">品名</th>'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">规格/产地</th>'
      '<th style="text-align:right;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">报价(元/吨)</th>'
      '<th style="text-align:right;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">变化</th>'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">贸易商角色 / 占比</th>'
      '</tr>')
    for cat, spec, price, chg, role in CONTEXT["lithium_spot_rows"]:
        if "亏损" in chg or "-1" in chg:
            chg_col = "#d63031"; chg_w = "700"
        elif "+" in chg:
            chg_col = "#d63031"; chg_w = "700"
        elif "-" in chg:
            chg_col = "#00875a"; chg_w = "700"
        else:
            chg_col = "#57606f"; chg_w = "400"
        A('<tr>'
          '<td style="padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;">%s</td>'
          '<td style="padding:4px 6px;border:1px solid #e1e4e8;color:#57606f;">%s</td>'
          '<td style="padding:4px 6px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:#1a3a5c;">%s</td>'
          '<td style="padding:4px 6px;border:1px solid #e1e4e8;text-align:right;color:%s;font-weight:%s;">%s</td>'
          '<td style="padding:4px 6px;border:1px solid #e1e4e8;color:#57606f;">%s</td>'
          '</tr>' % (cat, spec, price, chg_col, chg_w, chg, role))
    A('</table>'
      '<div style="font-size:11px;color:#8b949e;margin-top:6px;line-height:1.7;">'
      '<b>关键提示(博弈窗口的市场分割):</b><br>'
      '① 期货 LC2701/LC2705 报价是 <b>电池级(99.5%)主流电碳</b>(15.1-15.5 万) — 标准化 GB/T 11075, 是<b>交割基准品</b>; 期现商和大型正极厂主导, 常态化期现套利<br>'
      '② 实际下游材料厂的<b>工业级(99.2%)+ 准电碳(99.3%)</b>是主流走量品(占贸易流通 ~60%), 价格 <b>14.5-15.2 万</b>, 对 LC 期货是 <b>"贴近但独立"</b> 的另一条价格曲线<br>'
      '③ 中小正极厂混包用准电碳(<b>148,000-152,000</b>), 通过长协 + 客供绑定, <b>散户视角很少</b> — 这正是非标品市场分割的核心<br>'
      '④ 8 月电池排产 <b>311.85 GWh</b>(+5.71%), <b>储能首次反超动力(41.1%)</b> — 旺季需求托底; 但津巴布韦锂矿陆续到港 + 江西枧下窝 9 月中前批复窗口, 远期宽松压制<br>'
      '⑤ 锂盐厂利润 <b>+0.3 万/吨</b>(转盈边缘, 售价 15.3 vs 完本 14.9), 一线(赣锋/天齐)稳定盈利, 二三线微利; <b>"舒适区"是 14-15 万</b> — 跌破 14 万才会大面积减产'
      '</div>')
    A('</div>')

    # 3 库存与供给
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #6c5ce7;padding-left:10px;margin-bottom:12px;">三 · 库存与供给</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:12px;color:#57606f;border-collapse:collapse;">')
    A('<tr><td style="padding:4px 8px 4px 0;width:88px;color:#8b949e;">库存</td><td style="padding:4px 0;">SMM %s ; GFEX 仓单 %s — <b>连续 9 周加速去库创年内新低</b></td></tr>' % (lf["SMM_total_inv"], lf["GFEX_warrant"]))
    A('<tr><td style="padding:4px 8px 4px 0;color:#8b949e;">供给</td><td style="padding:4px 0;">周产 %s ; 锂精矿 %s</td></tr>' % (lf["weekly_output"], lf["SMM_spodumene_6pct"]))
    A('<tr><td style="padding:4px 8px 4px 0;color:#8b949e;">需求</td><td style="padding:4px 0;">%s ; 铁锂/三元: %s</td></tr>' % (lf["demand_aug"], lf["demand_lfp"]))
    A('<tr><td style="padding:4px 8px 4px 0;color:#8b949e;">基差</td><td style="padding:4px 0;">%s</td></tr>' % lf["spread_basis"])
    A('</table>')
    A('</div>')

    # 4 价差时间窗口 + Actionable
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #2c5f8a;padding-left:10px;margin-bottom:12px;">四 · 价差时间窗口(方向 × 时点 · 可执行)</div>')
    A('<div style="background:#eef6ff;border:1px solid #b8d4f0;border-radius:6px;padding:10px 14px;font-size:13px;line-height:1.8;">')
    A('<b>价差时间窗口:</b><br>'
      '① <b>LC2701-LC2705 价差 +%d 元</b>: 从 +2,380 走扩 1,040 元, 已逼近 <b>+3,500 上沿阈值</b>——"走扩至 +3,500+ 是大概率方向"的判断正在兑现; 若价差反向收敛至 +1,500 以内, 警惕枧下窝提前批复或津巴布韦矿放量<br>'
      '② <b>基差约 -6,500 元</b>(现 15.45万 − 期 16.1万): 期货升水大幅走阔, <b>传统反套(卖现买期)不可做</b>; 反向看, <b>正向套利(卖期买现)窗口打开</b>——基差 -6,500 已远超持有成本, 有现货货源者可锁基差; 但现货流动性缺口大、贸易商补库困难, 正套需真实货源<br>'
      '③ <b>枧下窝时间窗</b>: 8/26 宜春生态局撤销原报告 → 复产流程远慢于预期(未来 4 个月供应有限), 9 月中正式批复窗口仍是<b>强现实 vs 弱预期的最大扳机</b>; 9/5-9/10 观察为宜<br>'
      '④ <b>新供给扰动</b>: 雅保智利 400+ 工会成员 9/2 起合法罢工 — 南美锂盐供给收紧, 叠加澳矿发运未明显恢复' % lc_gap)
    A('</div>')
    # Actionable 绿盒
    A('<div style="background:#e8f7ec;border:1px solid #a5d6a7;border-radius:6px;padding:10px 14px;margin-top:12px;font-size:13px;line-height:1.85;">')
    A('<b>Actionable · 碳酸锂分角色客户行动建议(描述性→可执行):</b><br>')
    A('<table width="100%" cellpadding="3" cellspacing="0" style="font-size:12px;border-collapse:collapse;margin-top:4px;">'
      '<tr style="background:#d4edda;">'
      '<th style="text-align:left;padding:4px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;width:88px;">客户角色</th>'
      '<th style="text-align:left;padding:4px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;width:200px;">当前价位 / 判断</th>'
      '<th style="text-align:left;padding:4px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;">可执行动作</th>'
      '</tr>')
    for role, position, action, _ in CONTEXT["lithium_actionable"]:
        A('<tr>'
          '<td style="padding:6px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;">%s</td>'
          '<td style="padding:6px 8px;border:1px solid #a5d6a7;">%s</td>'
          '<td style="padding:6px 8px;border:1px solid #a5d6a7;line-height:1.7;">%s</td>'
          '</tr>' % (role, position, action))
    A('</table>'
      '<div style="font-size:11px;color:#8b949e;margin-top:6px;line-height:1.6;">'
      '<b>使用提示:</b> 上游卖、中游转正套(需真实货源)、下游等回踩 — 与硅链方向结构一致(中游因基差为负做不了传统反套, 但基差大幅走阔后正套窗口打开); 客户问"为什么"时, 可用"强现实 vs 弱预期拆解"作为说服依据, 用"枧下窝时间窗"作为时点依据。'
      '</div>')
    A('</div>')
    A('</div>')

    # 5 验证信号
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #e17055;padding-left:10px;margin-bottom:12px;">五 · 四大验证信号(按优先级)</div>')
    A('<div style="background:#fff8e6;border:1px solid #ffe0a3;border-radius:6px;padding:10px 14px;font-size:13px;line-height:1.8;">')
    A('<b>验证信号 · LC 价差边界值触发器:</b><br>'
      '① <b>LC2701-LC2705 价差(当前 +%d 元, 四档跟踪口径):</b><br>' % cur_diff)
    for tier, meaning in CONTEXT["lithium_signals"]["tiers"]:
        A('&nbsp;&nbsp;• <b>%s</b>: %s<br>' % (tier, meaning))
    A('总框架: <b>近月强势(月差走扩) + 基差负值持续 → 强现实占优</b>; 月差收敛 + 基差转正 → 弱预期占优, 趋势转空。给客户一个<b>可量化的交易触发器</b>, 不再凭感觉。<br>'
      '② <b>枧下窝复产节奏(9 月中窗口)</b>: 批复延迟 → 近月继续走强; 提前批复 → 近月快速回吐 10%+<br>'
      '③ <b>SMM 周度库存去化斜率</b>: 连续 9 周去化约 -7,600 吨/周, 若去化收窄至 -3,000 吨/周以内 → 转弱信号<br>'
      '④ <b>GFEX 仓单日均增量</b>: 8/31 单日 +1,600 手至 45,600 手(高位), 若跳增至 +3,000 手/日 → 隐形库存显性化, 近月见顶')
    A('<div style="background:#fff3cd;border:1px solid #ffe0a3;border-radius:6px;padding:8px 12px;margin-top:8px;font-size:12px;line-height:1.7;">'
      '<b>📌 8/31 首次实测(信号①上线后首个交易日):</b><br>'
      '&nbsp;&nbsp;• LC2701-LC2705 价差 <b>+3,420</b>(从 +2,380 走扩 1,040 元)——已穿越平衡区上沿, 验证"走扩 +3,500+ 是大概率方向", 下一步看 <b>+4,000</b><br>'
      '&nbsp;&nbsp;• LC2701 <b>增仓上涨</b>(持仓 403,032, 日增约 1.1 万手): 多头主动进攻, 强现实(9 周去库+旺季备货+雅保罢工)开始主导定价<br>'
      '&nbsp;&nbsp;• 仓单高位(45,600 手)未阻止上行——隐性库存显性化被多头忽略, 若仓单见顶回落, 碳酸锂或继续被炒作(中金财富提示追高风险)</div>')
    A('</div>')
    A('</div>')

    # 6 事件日历(锂链相关)
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #0984e3;padding-left:10px;margin-bottom:12px;">六 · 锂链事件日历(雷区地图)</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">时间</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">事件</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">影响</th></tr>')
    for t, ev, note, sym in CONTEXT["calendar"] + CONTEXT["lithium_events"]:
        # 只保留锂链相关 + 全品种宏观事件
        if not ("碳酸锂" in sym or "锂" in sym or "全品种" in sym):
            continue
        hot = "今日" in t or "8/31" in t or "9月上旬" in t or "8/30" in t or "9月中" in t
        A('<tr%s><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;%s">%s</td>'
          '<td style="padding:5px 8px;border:1px solid #e1e4e8;%s">%s</td>'
          '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#8b949e;">%s</td></tr>' % (
              ' bgcolor="#fff4f4"' if hot else "", "color:#d63031;" if hot else "", t,
              "font-weight:700;" if hot else "", ev, sym + " · " + note if note else sym))
    A('</table>')
    A('</div>')

    # 尾注
    A('<div style="background:#f6f8fa;border:1px solid #e1e4e8;border-radius:0 0 10px 10px;margin-top:12px;padding:14px 24px;font-size:12px;color:#8b949e;line-height:1.7;">')
    A('<b>数据与框架说明</b><br>'
      '行情: 广期所(新浪期货, 昨收盘+夜盘), 结算价口径 · 锂链现货/库存/排产: SMM/百川盈孚 8/27 周报口径 · 仓单: 广期所<br>'
      '姊妹报告: 大宗商品晨报(七步测温全市场版, 08:30) · 硅链专题(08:45) · 本专题为第七部分独立深挖版<br>'
      '本报告仅为个人研究参考, 不构成投资建议。')
    A('</div>')
    A('</div></body></html>')

    html = "\n".join(H)
    out = os.path.join(BASE, "outputs", "lithium_focus_%s_%s_%s.html" % (y, m, dd))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("saved ->", out, "(%.1f KB)" % (len(html.encode("utf-8")) / 1024))
    assert "锂链专题晨报" in html and "强现实" in html and "Actionable" in html
    print("tables:", html.count("<table"), "| sections:", html.count("▎") + html.count("· "))

if __name__ == "__main__":
    main()
