# -*- coding: utf-8 -*-
"""硅链专题晨报生成器 · 工业硅/多晶硅 主战场深挖版
用法: python3 silicon_focus_report.py [YYYY MM DD]
数据依赖: silicon_data.json
CONTEXT 从 commodity_morning_report.py 导入(单一数据源)——改价表/弱现实拆解只需改主报的 CONTEXT
输出: outputs/silicon_focus_YYYY_MM_DD.html
"""
import json, sys, os
from datetime import datetime

# 单一数据源: 从父目录的 commodity_morning_report.py 导入 CONTEXT
# 仓库目录结构: scripts/commodity_morning_report.py (主报)
#               scripts/silicon_focus/silicon_focus_report.py (本脚本)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from commodity_morning_report import CONTEXT

def load(name):
    p = os.path.join(BASE, name)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def main():
    if len(sys.argv) >= 4:
        y, m, dd = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        now = datetime.now()
        y, m, dd = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")

    sil = load("silicon_data.json") or {}
    sq = sil.get("quotes", {})

    def q(c):
        r = sq.get(c, {})
        return r.get("last", 0), r.get("settle", 0), r.get("oi", 0), r.get("volume", 0)

    si11 = q("SI2611"); si12 = q("SI2612")
    ps11 = q("PS2611"); ps12 = q("PS2612")
    si_gap = (si12[0] - si11[0]) if si11[0] and si12[0] else 0
    ps_gap = (ps12[0] - ps11[0]) if ps11[0] and ps12[0] else 0

    sf = CONTEXT["silicon_fundamental"]

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

    # 头部
    A('<div style="background:linear-gradient(135deg,#7a5c0e 0%,#b8860b 100%);border-radius:10px 10px 0 0;padding:22px 24px;color:#fff;">')
    A('<div style="font-size:12px;opacity:.85;letter-spacing:2px;">SILICON CHAIN FOCUS BRIEF · 主战场深挖</div>')
    A('<div style="font-size:24px;font-weight:700;margin:6px 0 4px;">硅链专题晨报</div>')
    wk_map = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    try:
        wd = wk_map[datetime(int(y), int(m), int(dd)).weekday()]
    except Exception:
        wd = "星期四"
    A('<div style="font-size:13px;opacity:.9;">%s年%s月%s日 · %s · 数据截至昨收盘+今日夜盘</div>' % (y, m, dd, wd))
    A('<div style="display:inline-block;margin-top:10px;background:rgba(255,255,255,.15);border-radius:20px;padding:5px 14px;font-size:13px;">⛓ 工业硅 × 多晶硅 · 期货热36°C × 实体冷25°C</div>')
    A('</div>')

    # 摘要条
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-top:none;padding:14px 24px;font-size:13px;line-height:1.7;">')
    A('<b style="color:#7a5c0e;">▎本专题定位</b><br>'
      '大宗商品晨报第六部分的独立深挖版——只看硅链。合约角色 → 为什么弱 → 现货真实价表(标准+非标15行) → 市场分割逻辑 → 价差时间窗口 → 分角色客户行动建议 → 四大验证信号。')
    A('</div>')

    # 1 合约表
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #fdcb6e;padding-left:10px;margin-bottom:12px;">一 · 合约全景(广期所)</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">合约</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">最新</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">昨结</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">持仓(手)</th><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">角色</th></tr>')
    for c, last, settle, oiv, note in [
        ("SI2611", si11[0], si11[1], si11[2], "主力·弱现实定价"),
        ("SI2612", si12[0], si12[1], si12[2], "新交割标准·制度断层+%d" % si_gap),
        ("PS2611", ps11[0], ps11[1], ps11[2], "主力·弱现实定价"),
        ("PS2612", ps12[0], ps12[1], ps12[2], "反内卷预期·政策断层+%d" % ps_gap),
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
    # 弱现实拆解
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:12px;color:#57606f;margin-top:10px;border-collapse:collapse;">')
    A('<tr><td style="padding:4px 8px 4px 0;width:88px;vertical-align:top;color:#8b949e;line-height:1.9;">弱现实拆解</td>'
      '<td style="padding:4px 0;line-height:1.5;">'
      '<table width="100%" cellpadding="3" cellspacing="0" style="font-size:12px;border-collapse:collapse;">'
      '<tr style="background:#f8f9fa;">'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;width:64px;">合约</th>'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">弱现实的具体含义(三句话脱口版)</th>'
      '</tr>')
    wr_marks = ["①", "②", "③"]
    for wr_c, wr_items in CONTEXT["weak_reality_rows"]:
        wr_body = "<br>".join("%s %s" % (wr_marks[i], s) for i, s in enumerate(wr_items))
        A('<tr><td style="padding:4px 6px;border:1px solid #e1e4e8;font-weight:700;color:#1a3a5c;">%s</td>'
          '<td style="padding:4px 6px;border:1px solid #e1e4e8;color:#57606f;line-height:1.7;">%s</td></tr>' % (wr_c, wr_body))
    A('</table>'
      '<div style="font-size:11px;color:#8b949e;margin-top:4px;">"弱现实"不是一句口号——上面每一条都对应可核实的仓单/利润/开工数据。</div>'
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
    for cat, spec, price, chg, role in CONTEXT["silicon_spot_rows"]:
        if "亏损" in chg or "-1" in chg:
            chg_col = "#d63031"; chg_w = "700"
        elif "+" in chg:
            chg_col = "#d63031"; chg_w = "700"
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
      '<b>关键提示(市场分割逻辑):</b><br>'
      '① 期货 SI 2611/PS 2611 报价 <b>通氧 553#</b>(8,830 元)与 <b>N 致密料</b>(40,250 元)只是<b>交割基准品</b>, 流通量不足现货总量 10%<br>'
      '② 实际主流走量是 <b>不通氧 553#</b>(~15 万吨/月) + <b>441#</b>(~5 万吨/月) + <b>99/97 硅等非标品</b>(~12 万吨/月), 后者基本不进入交割体系<br>'
      '③ <b style="color:#d63031;">市场分割:</b> 非标品现货市场(99硅/97硅/551#等)玩家是 <b>中小贸易商/磨粉厂/铝合金厂</b>, <b>基本不做期现套利</b>——价格随行就市, 与期货盘不直接联动; '
      '标准品期现市场(553#/421#等可交割品)由 <b>期现商/大型冶炼厂/机构</b>主导, <b>常态化期现套利</b>——这是判断盘面价格是否能传导到现货的两条不同路径<br>'
      '④ 多晶硅虽报盘 +18.75% 月, 但<b>全行业亏损</b>(单公斤 -1.4 元), <b>成交仍稀</b>——挺价没量等于"账面的"'
      '</div>')
    A('</div>')

    # 3 库存与供给
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #6c5ce7;padding-left:10px;margin-bottom:12px;">三 · 库存与供给</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:12px;color:#57606f;border-collapse:collapse;">')
    A('<tr><td style="padding:4px 8px 4px 0;width:88px;color:#8b949e;">库存</td><td style="padding:4px 0;">工业硅 %s; 多晶硅 %s — <b>涨幅最大的品种库存最重</b></td></tr>' % (sf["SI_social_inv"], sf["PS_chain_inv"]))
    A('<tr><td style="padding:4px 8px 4px 0;color:#8b949e;">供给</td><td style="padding:4px 0;">工业硅: %s; 多晶硅: %s</td></tr>' % (sf["SI_open_rate"], sf["PS_open_rate"]))
    A('</table>')
    A('</div>')

    # 4 价差时间窗口
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #2c5f8a;padding-left:10px;margin-bottom:12px;">四 · 价差时间窗口(方向 × 时点 · 可执行)</div>')
    A('<div style="background:#eef6ff;border:1px solid #b8d4f0;border-radius:6px;padding:10px 14px;font-size:13px;line-height:1.8;">')
    A('<b>价差时间窗口:</b><br>'
      '① <b>工业硅 SI2611-2612 价差 +%d 元</b>: 距正常持仓成本(~80-100 元)仍有约 <b>250 元收敛空间</b>——收敛需等 9-11 月仓单注销进度; 若老仓单大量流向现货 → 近月压力减轻 → 价差可能<b>提前收敛</b><br>'
      '② <b>多晶硅 PS2611-2612 价差 +%d 元</b>: 12 月"反内卷"政策若在行业会议后落地 → 价差可能进一步<b>走扩至 4000+</b>; 若政策不及预期 → 迅速<b>收敛至 2000 以内</b>。关键观察窗口: <b>8/31-9/5(会议后一周)</b>' % (si_gap, ps_gap))
    A('</div>')
    # Actionable 绿盒
    A('<div style="background:#e8f7ec;border:1px solid #a5d6a7;border-radius:6px;padding:10px 14px;margin-top:12px;font-size:13px;line-height:1.85;">')
    A('<b>Actionable · 分角色客户行动建议(描述性→可执行):</b><br>')
    A('<table width="100%" cellpadding="3" cellspacing="0" style="font-size:12px;border-collapse:collapse;margin-top:4px;">'
      '<tr style="background:#d4edda;">'
      '<th style="text-align:left;padding:4px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;width:88px;">客户角色</th>'
      '<th style="text-align:left;padding:4px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;width:200px;">当前价位 / 判断</th>'
      '<th style="text-align:left;padding:4px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;">可执行动作</th>'
      '</tr>'
      '<tr>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;">工业硅<br><span style="font-weight:400;font-size:11px;color:#57606f;">上游冶炼厂</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;">SI2611 当前 8,865(8/31 收盘 +0.8%)<br>'
      '<span style="color:#57606f;">机构建议"低比例卖出"窗口, 距 9,000 关口仅 135 元</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;line-height:1.7;">'
      '① <b>当前 8,865: 低比例卖出套保窗口</b>(如 30% 产量)<br>'
      '② 若价格反弹至 <b>9,000 以上</b>: <b style="color:#d63031;">加套保比例至 50%+</b>(反内卷预期 + 仓单注销双驱动下, 9,000 上方空间有限)<br>'
      '③ 若价格回落至 <b>8,500 以下</b>: <b style="color:#d63031;">平掉部分空头套保头寸</b>(如从 50% 降至 20%), 同时在现货端<b>做好低价惜售准备</b>——8,500 已跌破多数企业成本线, 继续做空的性价比下降; 释放后不是离场, 而是<b>等反弹到 8,700-8,800 再分批重建</b>头寸。⚠ <b>切忌只释放不复建:</b> 若继续阴跌到 8,200, 后悔的是 "既丢了空头、也没在低价惜售现货" 。'
      '</td></tr>'
      '<tr>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;">工业硅<br><span style="font-weight:400;font-size:11px;color:#57606f;">中游贸易商</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;">基差 +535(现 9,400 − 期 8,865)<br>'
      '<span style="color:#57606f;">现货升水, 期货估值偏低</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;line-height:1.7;">'
      '① <b>"卖现货买期货" 反套策略</b>(基差正向回归): 卖现货 9,400 / 买 SI2611 8,865<br>'
      '② <b>扣除仓储+资金成本后净利 ~300 元/吨</b>(按 11-12 价差收敛、持有至 SI2611 交割前测算, <b>约 60-90 天</b>周期)。⚠ 若价差在 1 个月内提前收敛(老仓单注销超预期), 年化收益率将显著提升——别死守合约到期, 见好就收。<br>'
      '③ <b style="color:#d63031;">关键约束:</b> 卖现货端必须有<b>真实销售渠道</b>(推荐不通氧 553# 或 441#), <b>不能依赖交割库一刀切</b>——这正是非标品市场分割的核心'
      '</td></tr>'
      '<tr>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;">多晶硅<br><span style="font-weight:400;font-size:11px;color:#57606f;">下游拉晶厂</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;">PS2611 当前 37,035(8/31 收盘 -2.0%)<br>'
      '<span style="color:#57606f;">"政策底" + 行业亏损兜底</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;line-height:1.7;">'
      '① <b>37,000-37,500 区间:</b> "政策底" 保护(反内卷政策预期 + 全行业亏损 -1.6 元/kg 兜底)<br>'
      '② <b>分批建立买入套保头寸(30%-50% 远期原料需求)</b>, 锁定远期成本<br>'
      '③ <b>场景拆解(方向相反, 动作不同):</b><br>'
      '&nbsp;&nbsp;• <b>若价格回落至 35,000 以下(政策底被击穿, 超跌窗口)</b>: <b style="color:#d63031;">套保比例加至 70%+</b>——这是 3-6 个月内的"安全垫价位", 单 kg 原料成本节省 5 元+<br>'
      '&nbsp;&nbsp;• <b>若会议超预期利好兑现、价格跳涨(突破 38,000)</b>: <b style="color:#d63031;">不建议追涨加仓</b>, 应等待回踩 36,000-37,000 后再分批建仓——历史规律: 利好兑现后常有获利回吐, 追涨被套概率 >60%'
      '</td></tr>'
      '</table>'
      '<div style="font-size:11px;color:#8b949e;margin-top:6px;line-height:1.6;">'
      '<b>使用提示:</b> 三类客户的动作方向不同——上游卖、中游反套、下游买, 这是市场结构决定的, 不是建议; 客户问"为什么"时, 可用上方的"弱现实拆解"作为说服依据, 用"价差时间窗口"作为时点依据。'
      '</div>')
    A('</div>')
    A('</div>')

    # 5 验证信号
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #e17055;padding-left:10px;margin-bottom:12px;">五 · 四大验证信号(按优先级)</div>')
    A('<div style="background:#fff8e6;border:1px solid #ffe0a3;border-radius:6px;padding:10px 14px;font-size:13px;line-height:1.8;">')
    A('<b>四大验证信号:</b><br>'
      '① <b>PS2611−PS2612 价差(当前 %s, 三档边界值跟踪口径):</b><br>'
      '&nbsp;&nbsp;• <b>收窄至 -3,000 以内</b>: 政策预期开始兑现, 近月估值修复<br>'
      '&nbsp;&nbsp;• <b>走扩至 -4,000 以上</b>: 政策预期进一步强化 或 近月仓单压力加剧<br>'
      '&nbsp;&nbsp;• <b>跌破 -4,500</b>: 警惕政策预期泡沫, 近月可能出现超跌反弹机会<br>'
      '总框架: 收敛→政策兑现; 走扩→预期发酵/弱现实加码。给客户一个<b>可量化的交易触发器</b>, 不再凭感觉。<br>'
      '② <b>工业硅仓单注销进度(9-11月)</b>: 老仓单流向现货压近月 vs 12月后可交割品骤减推远月<br>'
      '③ <b>多晶硅现货成交恢复</b>: 从零成交恢复成交, 牌价才变成真价格; 在此之前涨幅都是账面的<br>'
      '④ <b>持仓量的方向性变化(交易层面)</b>: PS2611 若在下跌过程中持仓持续减少(获利盘出清)→短期底部临近; 若持仓继续增加但价格横盘→多空分歧加大, 需等待方向选择' % format(int(ps11[0] - ps12[0]), ","))
    A('<div style="background:#fff3f3;border:1px solid #f5c6c6;border-radius:6px;padding:8px 12px;margin-top:8px;font-size:12px;line-height:1.7;color:#7a4a4a;">'
      '<b>📌 8/31 首次实测(信号④上线后第 1 个交易日):</b><br>'
      '• PS2611 <b>增仓下跌</b>(持仓 +1,034 手 / 价格 -2.01%)——<b>未触发</b>"持仓减少→底部临近"信号; 增仓下跌 = 空头主动打压 / 多空分歧加大, <b>短期底部未确认</b>, 观望等待方向选择<br>'
      '• PS2611-2612 价差 -3,940(从 -3,745 走扩 195 元)——逼近 -4,000 阈值; 本次走扩主因是<b>近月仓单压力加剧</b>(8/31 +150 手)而非政策强化(政策端反转向"保供稳价", 涨价预期降温)<br>'
      '• SI2611 <b>增仓上涨</b>(持仓 +18,395 手 / 价格 +0.8%)——多头主动进攻, 逼近 9,000 关口, 与 PS 形成双硅分化</div>')
    A('</div>')
    A('</div>')

    # 6 事件日历(硅链相关)
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #0984e3;padding-left:10px;margin-bottom:12px;">六 · 硅链事件日历(雷区地图)</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">时间</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">事件</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">影响</th></tr>')
    for t, ev, note, sym in CONTEXT["calendar"]:
        # 只保留硅链相关 + 全品种宏观事件
        if not ("工业硅" in sym or "多晶硅" in sym or "全品种" in sym):
            continue
        hot = "今日" in t or "8/31" in t or "9月上旬" in t
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
      '行情: 新浪期货(昨收盘+夜盘), 结算价口径 · 硅链现货: 百川盈孚/SMM/Mysteel/CBC/长江有色/同花顺 · 仓单: 广期所<br>'
      '姊妹报告: 大宗商品晨报(七步测温全市场版, 08:30) · 本专题为第六部分独立深挖版<br>'
      '本报告仅为个人研究参考, 不构成投资建议。')
    A('</div>')
    A('</div></body></html>')

    html = "\n".join(H)
    out = os.path.join(BASE, "outputs", "silicon_focus_%s_%s_%s.html" % (y, m, dd))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("saved ->", out, "(%.1f KB)" % (len(html.encode("utf-8")) / 1024))
    assert "硅链专题晨报" in html and "弱现实拆解" in html and "Actionable" in html
    print("tables:", html.count("<table"), "| sections:", html.count("▎") + html.count("· "))

if __name__ == "__main__":
    main()
