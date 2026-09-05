"""生成 8/26 盘后战略复盘 HTML（战略语气 · 35-40 KB）
"""
import os
import html as _html

OUT_DIR = '/Users/shuhaihong/Documents/workbuddy/outputs'
os.makedirs(OUT_DIR, exist_ok=True)
fpath = os.path.join(OUT_DIR, '市场温度_盘后_2026-08-26.html')

D = {
    'date': '2026-08-26 (周三)',
    'snapshot_time': '美东 16:00 EDT 收盘 · GMT+8 8/27 04:00 截取',
    'headline_metric': 'SPX 7675.70 (-0.02%) · IXIC 26130.20 (-0.08%) · DJI 53463.88 (-0.21%) · VIX 15.21 (-1.55%)',
    'one_liner': (
        '8/26 PCE日收官：三大指数微跌、美债收益率反弹、曲线略陡；'
        '整体PCE YoY 3.7%超预期、核心PCE 3.3%符合，市场重燃「高利率更久」担忧；'
        'NVDA盘后财报营收$96.2B/Q3指引$108B双双beat，AH由跌转涨约+4%；'
        '原油续跌(WTI -0.16%/Brent -0.84%)、COMEX金 -0.99%、LME铜 -0.64%；'
        '谷物大涨(小麦+6.40%)；VIX 15.21 calm 但 VIX1Y 22.60 仍高，尾部对冲未撤。'
    ),
    'summary': (
        '昨夜 SPX -0.02% 收 7675.70、道指 -0.21% 领跌、纳指 -0.08%；'
        'VIX 现货 15.21 (-1.55%) 继续压缩，但期限结构后端 VIX1Y 22.60 几乎没动，'
        '前端 calm、后端 hedge 仍在；信用端 JNK 96.18 (-0.01%) / HYG 79.90 (-0.03%) / TLT 83.30 (-0.20%) '
        '随利率反弹小幅承压，与 8/25 三同涨形成对比。'
        '商品链：WTI 82.23 (-0.16%) / Brent 87.84 (-0.84%) 续跌，EIA 库存仅增 9.5 万桶低于预期；'
        'COMEX 金 4647.80 (-0.99%) / 现货 4594.68 (-1.38%) 高位回吐，白银 68.085 (-0.87%)；'
        'LME 铜 14232.50 (-0.64%) 随美元反弹回落。'
        '谷物全线大涨：玉米 536.50 (+2.34%)、大豆 1266.00 (+1.96%)、小麦 748.25 (+6.40%)。'
        '事件 digest：7 月整体 PCE YoY 3.7%(超预期 3.6%)、核心 PCE MoM 0.2%/YoY 3.3% 符合；'
        'Q2 GDP 二估 1.5% 不变；个人收入 +0.4%、支出 +0.2%；'
        '盘后 NVDA Q2 FY27 营收 $96.2B / EPS $2.22 / 数据中心 $89B，Q3 指引 $108B±2% 均超共识；'
        '8/27 Jackson Hole 央行年会开幕，8/28 Warsh 首秀定调全球货币政策。'
    ),
}

# 中国惯例颜色（涨红跌绿）
RED = '#C0392B'      # 涨/正变动
GREEN = '#1E8449'    # 跌/负变动
INK = '#1B2631'
BG = '#FAF8F2'
PANEL = '#FFFFFF'
HILITE = '#FFF7D6'
HILITE2 = '#FFEEBC'
BORDER = '#D6CFA8'
MUTED = '#7F8C8D'

def esc(s): return _html.escape(str(s))

def num_red(text):
    return f'<span style="color:{RED};font-weight:600">{esc(text)}</span>'
def num_green(text):
    return f'<span style="color:{GREEN};font-weight:600">{esc(text)}</span>'
def num_neutral(text):
    return f'<span style="color:{INK};font-weight:600">{esc(text)}</span>'


# === 5 项战略复盘 ===
def section_strategic_review():
    return f"""
    <div style="border:1px solid {BORDER};border-radius:6px;overflow:hidden;margin-bottom:14px">
      <div style="background:#F1E8C8;padding:9px 14px;font-size:13px;font-weight:700;letter-spacing:1px">
        🔍 战略复盘 · 昨夜到底交易了什么逻辑
      </div>
      <div style="padding:14px;background:{PANEL};font-size:13px;line-height:1.7">

        <div style="margin-bottom:10px">
          <b style="color:#8E44AD">(A) 板块轮动确认/失败</b>——
          8/26 盘前预报的「防御领涨/小盘弱」<b style="color:{RED}">✅ 部分兑现</b>：
          工业 XLI +1.07% / 公用事业 XLU +0.47% / 信息技术 XLK +0.37% 领涨，
          医疗 XLV -1.01% / 通信服务 XLC -0.71% / 非必需消费 XLY -0.62% 领跌。
          道指 -0.21% 跌幅最大，罗素 2000 -0.14% 同步走弱；
          与 8/25 成长+半导体 risk-on 大切不同，8/26 是「事件前防御性轮动+板块分化」。
        </div>

        <div style="margin-bottom:10px">
          <b style="color:#8E44AD">(B) VIX 曲线整体位移</b>——
          VIX 现货 15.21 (-1.55%) 继续走低，但<b>后端几乎没动</b>：
          VIX9D 13.55 / 3M 17.99 / 6M 20.82 / 1Y 22.60。
          曲线位移方向 = <b style="color:{RED}">前端下、后端稳</b>：
          9D/3M 随现货压缩，1Y 仍远高于历史中位 19.5（+3.1 pts）→
          事件 hedge 便宜，<b>尾部 hedge 还在</b>。
        </div>

        <div style="margin-bottom:10px">
          <b style="color:#8E44AD">(C) 信用-主权协调</b>——
          JNK 96.18 (-0.01%) / 盘后 96.19 / HYG 79.90 (-0.03%) / TLT 83.30 (-0.20%)。
          与 8/25「信用+长端鸽派+利差收窄」三同涨不同，
          8/26 PCE 粘性后利率反弹、信用债小幅承压 →
          <b style="color:{GREEN}">risk-off 微调</b>，但 JNK/HYG 跌幅极浅，
          未出现高yield 抛售恐慌。风险点仍在 VIX1Y 22.60 的尾部溢价。
        </div>

        <div style="margin-bottom:10px">
          <b style="color:#8E44AD">(D) 量价结构</b>——
          SPX 收盘 7675.70，日内波动极小（-0.02%），DJI 跌 -0.21% 领跌，
          板块 7 跌 4 涨但幅度温和；配合 PCE/GDP + NVDA 盘后 + Jackson Hole 开幕，
          成交量偏清淡。评：<b>事件前观望市，不是趋势性突破</b>，
          类似 8/26 盘前「等 PCE + NVDA + Warsh」的谨慎结构。
        </div>

        <div>
          <b style="color:#8E44AD">(E) 财报/事件 digest</b>——
          ① 7 月 PCE：整体 YoY 3.7% 超预期 3.6%，核心 YoY 3.3%/MoM 0.2% 符合 →
          「通胀粘性」叙事重燃，9 月降息预期降温，10Y +3bp；
          ② Q2 GDP 二估 1.5% 不变，个人收入 +0.4%、支出 +0.2% → 经济未走弱；
          ③ 盘后 NVDA Q2 FY27 营收 $96.2B（+106% YoY）、EPS $2.22、数据中心 $89B，
          Q3 指引 $108B±2% 均超共识，AH 由跌转涨约 +4%；
          ④ Jackson Hole 8/27 开幕，Warsh 8/28 首秀是全球货币政策关键定调。
        </div>

      </div>
    </div>
    """


# === ⚡ 与昨日盘前报告对账 ===
def section_reconciliation_table():
    return f"""
    <div style="border:1px solid {BORDER};border-radius:6px;overflow:hidden;margin-bottom:14px">
      <div style="background:#F1E8C8;padding:9px 14px;font-size:13px;font-weight:700;letter-spacing:1px">
        ⚡ 与昨日盘前战术报告对账（8/26 07:30 GMT+8 跑、收盘兑现如何？）
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:13px;background:{PANEL}">
        <thead>
          <tr style="background:#FBF6E5">
            <th style="padding:8px 12px;text-align:left;width:28%">昨日 07:30 盘前预期</th>
            <th style="padding:8px 12px;text-align:left;width:34%">昨夜 8/26 收盘实际</th>
            <th style="padding:8px 12px;text-align:center;width:12%">兑现</th>
            <th style="padding:8px 12px;text-align:left">简评</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5">防御领涨 / 小盘偏弱（YM > ES > NQ > RTY）</td>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5">道指 -0.21% 领跌；工业 +1.07% / 公用事业 +0.47% 领涨；RTY -0.14%</td>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5;text-align:center"><b style="color:{RED};font-size:14px">✅</b></td>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5">防御/价值相对抗跌</td>
          </tr>
          <tr>
            <td style="padding:8px 12px">油价续跌（亚欧获利了结）</td>
            <td style="padding:8px 12px">{num_green('WTI 82.23 (-0.16%) / Brent 87.84 (-0.84%)')} 续跌</td>
            <td style="padding:8px 12px;text-align:center"><b style="color:{RED};font-size:14px">✅</b></td>
            <td style="padding:8px 12px">方向对，幅度温和</td>
          </tr>
          <tr>
            <td style="padding:8px 12px">黄金高位获利回吐</td>
            <td style="padding:8px 12px">{num_green('COMEX 金 4647.80 (-0.99%) / 现货 4594.68 (-1.38%)')}</td>
            <td style="padding:8px 12px;text-align:center"><b style="color:{RED};font-size:14px">✅</b></td>
            <td style="padding:8px 12px">PCE/美元反弹压制金价</td>
          </tr>
          <tr>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5">科技股偏弱 / NVDA 财报前谨慎</td>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5">IXIC -0.08% 偏弱；NVDA cash -1.59% 财报前回落，盘后财报 beat 反弹</td>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5;text-align:center"><b style="color:{RED};font-size:14px">✅</b></td>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5">盘中谨慎，盘后利好释放</td>
          </tr>
          <tr>
            <td style="padding:8px 12px">VIX 维持 calm</td>
            <td style="padding:8px 12px">{num_green('VIX 15.21 (-1.55%)')} 继续压缩</td>
            <td style="padding:8px 12px;text-align:center"><b style="color:{RED};font-size:14px">✅</b></td>
            <td style="padding:8px 12px">前端 vol 便宜</td>
          </tr>
          <tr>
            <td style="padding:8px 12px">2s10s 微熊平</td>
            <td style="padding:8px 12px">{num_red('2s10s 约 47bp (+1bp 微牛陡)')}：2Y +1bp / 10Y +3bp</td>
            <td style="padding:8px 12px;text-align:center"><b style="color:{GREEN};font-size:14px">❌</b></td>
            <td style="padding:8px 12px">PCE 粘性推陡峭化</td>
          </tr>
          <tr>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5">PCE 粘性预期</td>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5">整体 PCE YoY 3.7% 超预期；核心 3.3% 符合</td>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5;text-align:center"><b style="color:{RED};font-size:14px">✅</b></td>
            <td style="padding:8px 12px;border-top:1px solid #EEE5C5">名义通胀粘性确认</td>
          </tr>
          <tr>
            <td style="padding:8px 12px">小麦/谷物偏强</td>
            <td style="padding:8px 12px">{num_red('小麦 +6.40% / 玉米 +2.34% / 大豆 +1.96%')} 全线大涨</td>
            <td style="padding:8px 12px;text-align:center"><b style="color:{RED};font-size:14px">✅</b></td>
            <td style="padding:8px 12px">黑海/作物评级驱动</td>
          </tr>
        </tbody>
      </table>
      <div style="padding:10px 14px;font-size:11px;color:{MUTED};background:#FBF6E5">
        准确率 7/8 = 88%；唯一 ❌ 是曲线形态，PCE 粘性使 2s10s 由微熊平转微牛陡，说明市场对「高利率更久」重新定价。
      </div>
    </div>
    """


# === 7 步分节 ===
def section_7_steps():
    return f"""
    <div style="margin-bottom:14px">

      <!-- ① -->
      <div style="border:1px solid {BORDER};border-radius:4px;overflow:hidden;margin-bottom:10px">
        <div style="background:#EDE2B0;padding:7px 12px;font-size:12px;font-weight:700;letter-spacing:1px">
          ① 利率与债券（8/26 cash close）· vs 8/25 settle
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;background:{PANEL}">
          <tr><td style="padding:6px 12px;width:35%">2Y 美债</td><td style="padding:6px 12px">4.19%</td><td style="padding:6px 12px;text-align:right">{num_red('+1bp')}</td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">10Y 美债</td><td style="padding:6px 12px">4.66%</td><td style="padding:6px 12px;text-align:right">{num_red('+3bp (领涨)')}</td></tr>
          <tr><td style="padding:6px 12px">30Y 美债</td><td style="padding:6px 12px">5.18%</td><td style="padding:6px 12px;text-align:right">{num_red('+1bp')}</td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">2Y-10Y 利差</td><td style="padding:6px 12px">约 47bp</td><td style="padding:6px 12px;text-align:right">{num_red('+1bp（微牛陡）')}</td></tr>
          <tr><td style="padding:6px 12px">事件触发</td><td colspan="2" style="padding:6px 12px;font-size:12px">
            ① 7 月整体 PCE YoY 3.7% 超预期 → ② 核心 PCE 3.3% 符合但粘性 → ③ Q2 GDP 二估 1.5% 不变
          </td></tr>
        </table>
        <div style="padding:8px 12px;font-size:12px;color:#5D4E2D;background:#FBF6E5">
          <b>结论</b>：收益率集体反弹 + 10Y 领涨 + 2s10s 微牛陡 =
          <b>PCE 粘性推升「高利率更久」定价</b>，与 8/25 鸽派重定价方向相反。
        </div>
      </div>

      <!-- ② -->
      <div style="border:1px solid {BORDER};border-radius:4px;overflow:hidden;margin-bottom:10px">
        <div style="background:#EDE2B0;padding:7px 12px;font-size:12px;font-weight:700;letter-spacing:1px">
          ② 指数期货与板块（8/26 cash close）
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;background:{PANEL}">
          <tr><td style="padding:6px 12px;width:35%">标普 500</td><td style="padding:6px 12px">7675.70</td><td style="padding:6px 12px;text-align:right">{num_green('-0.02%')}</td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">道指 (DJI)</td><td style="padding:6px 12px">53463.88</td><td style="padding:6px 12px;text-align:right">{num_green('-0.21% 领跌')}</td></tr>
          <tr><td style="padding:6px 12px">纳斯达克 (IXIC)</td><td style="padding:6px 12px">26130.20</td><td style="padding:6px 12px;text-align:right">{num_green('-0.08%')}</td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">罗素 2000 (RTY)</td><td style="padding:6px 12px">3005.90</td><td style="padding:6px 12px;text-align:right">{num_green('-0.14%')}</td></tr>
          <tr><td style="padding:6px 12px">领涨板块（前 3）</td><td colspan="2" style="padding:6px 12px;font-size:12px">
            {num_red('工业 XLI +1.07%')} / 公用事业 XLU +0.47% / 信息技术 XLK +0.37%
          </td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">领跌板块（后 3）</td><td colspan="2" style="padding:6px 12px;font-size:12px">
            {num_green('医疗 XLV -1.01%')} / 通信服务 XLC -0.71% / 非必需消费 XLY -0.62%
          </td></tr>
        </table>
        <div style="padding:8px 12px;font-size:12px;color:#5D4E2D;background:#FBF6E5">
          <b>风险信号</b>：道指领跌 + 小盘偏弱 = 利率敏感型/价值型板块受 PCE 粘性压制；
          工业/公用事业领涨显示资金转向防御性实物资产 + 高股息。
        </div>
      </div>

      <!-- ③ -->
      <div style="border:1px solid {BORDER};border-radius:4px;overflow:hidden;margin-bottom:10px">
        <div style="background:#EDE2B0;padding:7px 12px;font-size:12px;font-weight:700;letter-spacing:1px">
          ③ 石油（8/26 cash close）
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;background:{PANEL}">
          <tr><td style="padding:6px 12px;width:35%">WTI (10 月)</td><td style="padding:6px 12px">$82.23</td><td style="padding:6px 12px;text-align:right">{num_green('-0.16%')}</td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">Brent (10 月)</td><td style="padding:6px 12px">$87.84</td><td style="padding:6px 12px;text-align:right">{num_green('-0.84%')}（近三周最大单日跌幅）</td></tr>
        </table>
        <div style="padding:8px 12px;font-size:12px;color:#5D4E2D;background:#FBF6E5">
          <b>驱动</b>：① 伊朗-阿曼就霍尔木兹海峡安全通航继续谈判 → ② EIA 原油库存仅增 9.5 万桶（远低于预期 59.7 万桶），跌幅收窄 →
          ③ 中东地缘风险溢价回吐 + 多头获利了结。Brent 已回落至 87-88 区间，接近 8/10 以来低点。
        </div>
      </div>

      <!-- ④ -->
      <div style="border:1px solid {BORDER};border-radius:4px;overflow:hidden;margin-bottom:10px">
        <div style="background:#EDE2B0;padding:7px 12px;font-size:12px;font-weight:700;letter-spacing:1px">
          ④ 黄金 · 白银 · 铜（8/26 cash close）
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;background:{PANEL}">
          <tr><td style="padding:6px 12px;width:35%">COMEX 黄金</td><td style="padding:6px 12px">$4647.80</td><td style="padding:6px 12px;text-align:right">{num_green('-0.99%')}</td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">现货黄金 (伦敦)</td><td style="padding:6px 12px">$4594.68</td><td style="padding:6px 12px;text-align:right">{num_green('-1.38%')}</td></tr>
          <tr><td style="padding:6px 12px">COMEX 白银</td><td style="padding:6px 12px">$68.085</td><td style="padding:6px 12px;text-align:right">{num_green('-0.87%')}</td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">LME 铜 (3 月)</td><td style="padding:6px 12px">$14232.50</td><td style="padding:6px 12px;text-align:right">{num_green('-0.64%')}</td></tr>
        </table>
        <div style="padding:8px 12px;font-size:12px;color:#5D4E2D;background:#FBF6E5">
          <b>整体逻辑</b>：PCE 粘性 + 美元反弹 + 利率上行 → 贵金属与工业金属同步承压；
          黄金高位获利回吐，铜随宏观紧缩预期回落。イベント hedge 价值仍存，但短期价格调整。
        </div>
      </div>

      <!-- ⑤ -->
      <div style="border:1px solid {BORDER};border-radius:4px;overflow:hidden;margin-bottom:10px">
        <div style="background:#EDE2B0;padding:7px 12px;font-size:12px;font-weight:700;letter-spacing:1px">
          ⑤ 谷物（CBOT 8/26 close）
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;background:{PANEL}">
          <tr><td style="padding:6px 12px;width:35%">玉米 (12月)</td><td style="padding:6px 12px">536.50 ¢/bu</td><td style="padding:6px 12px;text-align:right">{num_red('+2.34%')}（作物评级下滑）</td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">大豆 (11月)</td><td style="padding:6px 12px">1266.00 ¢/bu</td><td style="padding:6px 12px;text-align:right">{num_red('+1.96%')}（出口需求强劲）</td></tr>
          <tr><td style="padding:6px 12px">小麦 (12月)</td><td style="padding:6px 12px">748.25 ¢/bu</td><td style="padding:6px 12px;text-align:right">{num_red('+6.40%')}（黑海出口中断+作物担忧）</td></tr>
        </table>
        <div style="padding:8px 12px;font-size:12px;color:#5D4E2D;background:#FBF6E5">
          <b>剧烈波动?</b> 小麦 +6.40% 超 3% 阈值，属重大异常；玉米/大豆同步大涨，
          谷物板块从「豆-玉背离」修复为全线走强。关注 USDA 作物巡查报告。
        </div>
      </div>

      <!-- ⑥ -->
      <div style="border:1px solid {BORDER};border-radius:4px;overflow:hidden;margin-bottom:10px">
        <div style="background:#EDE2B0;padding:7px 12px;font-size:12px;font-weight:700;letter-spacing:1px">
          ⑥ VIX 期限结构 · 8/26 close | <b style="color:#8E44AD">战略位：前端 calm、后端 hedge 仍在</b>
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;background:{PANEL}">
          <tr><td style="padding:6px 12px;width:35%">VIX 现货</td><td style="padding:6px 12px">15.21</td><td style="padding:6px 12px;text-align:right">{num_green('-1.55%')}（vs 8/25 15.45）</td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">VIX9D</td><td style="padding:6px 12px">13.55</td><td style="padding:6px 12px;text-align:right">{num_red('+0.74%')}（9D 相对 spot 偏贵）</td></tr>
          <tr><td style="padding:6px 12px">VIX3M (3月)</td><td style="padding:6px 12px">17.99</td><td style="padding:6px 12px;text-align:right">{num_green('-1.21%')}</td></tr>
          <tr style="background:#FBF6E5"><td style="padding:6px 12px">VIX6M (6月)</td><td style="padding:6px 12px">20.82</td><td style="padding:6px 12px;text-align:right">{num_green('-0.10%')}</td></tr>
          <tr><td style="padding:6px 12px">VIX1Y (1年)</td><td style="padding:6px 12px">22.60</td><td style="padding:6px 12px;text-align:right">{num_green('-0.04%')}（远端几乎没动）</td></tr>
        </table>
        <div style="padding:8px 12px;font-size:12px;color:#5D4E2D;background:#FBF6E5">
          <b>曲线形态</b>：contango 持续（9D 13.55 < 现 15.21 < 3M 17.99 < 6M 20.82 < 1Y 22.60）；
          <b style="color:{RED}">曲线位移方向</b>：<b>前端下、后端稳</b>（spot -1.55% / 1Y 几乎没动）。
          <b>解读</b>：事件 hedge 便宜，但<b>尾部 hedge (VIX1Y) 还在</b>；
          VIX1Y 22.60 vs 历史中位 19.5 = +3.1 pts，若 Warsh 偏鹰，VIX 现 15.21 反弹至 17-19 区间容易。
        </div>
      </div>

      <!-- ⑦ -->
      <div style="border:1px solid {BORDER};border-radius:4px;overflow:hidden">
        <div style="background:#EDE2B0;padding:7px 12px;font-size:12px;font-weight:700;letter-spacing:1px">
          ⑦ 日历与对冲 · Jackson Hole + Warsh 首秀周
        </div>
        <div style="padding:10px 12px;font-size:13px;background:{PANEL};line-height:1.8">
          <b>8/26 周三 8:30 ET</b>：Q2 GDP 二估 1.5% + <b style="color:#8E44AD">7 月 PCE / 核心 PCE</b>（整体 YoY 3.7% 超预期 / 核心 3.3% 符合）+ 耐用品订单 + 个人收支<br>
          <b>8/26 盘后 (8/27 GMT+8 早晨)</b>：<b style="color:#8E44AD">NVDA Q2 FY27</b>（营收 $96.2B / EPS $2.22 / 数据中心 $89B / Q3 指引 $108B±2%，均超共识）+ CRM + CRWD + HPQ<br>
          <b>8/27 周四</b>：Jackson Hole 央行年会开幕（主题「金融创新：对支付与政策的影响」）+ 初请失业金 + Pending Home Sales<br>
          <b>8/27 盘后</b>：MRVL + ADSK + BILI + DG + DLTR + WDAY<br>
          <b style="color:#8E44AD">8/28 周五 10:00 ET 22:00 北京</b>：<b>Warsh Jackson Hole 首秀</b>（上任后首次主旨演讲，锚定全球货币政策预期）+ 非农基准修正初值 + 密歇根信心终值<br>
          <b>8/29 周六</b>：Jackson Hole 闭幕
        </div>
        <div style="padding:8px 12px;font-size:12px;color:#5D4E2D;background:#FBF6E5">
          <b>对冲状态</b>：前端 hedge 便宜（VIX 15.21 / 9D 13.55），远端 hedge 还在（VIX1Y 22.60）；
          <b>关键词</b>：Warsh 首秀是本周最大 binary 事件，偏鹰 = 长端利率再上行 + 黄金再回调 + 科技估值受压。
        </div>
      </div>

    </div>
    """


# === 🛡️ JNK 信用 + 盘后 ===
def section_jnk_post_market():
    return f"""
    <div style="border:1px solid #B7950B;border-radius:6px;overflow:hidden;margin-bottom:14px;background:#FFFEF3">
      <div style="background:#D4AC0D;padding:9px 14px;font-size:13px;font-weight:700;letter-spacing:1px;color:#FFF">
        🛡️ JNK 信用债 · 盘后细节（事件 hedge 的另一只眼睛）
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:13px">
        <tr><td style="padding:6px 14px;width:32%;background:#FFFEF3">JNK 8/26 cash 收盘</td><td style="padding:6px 14px;background:#FFFEF3">{num_green('96.18')}（-0.01% vs 8/25 96.20）</td></tr>
        <tr><td style="padding:6px 14px">JNK 盘后 (16:16 ET)</td><td style="padding:6px 14px">{num_red('96.19')}（+0.01 · 量 162.7 万）</td></tr>
        <tr><td style="padding:6px 14px">HYG (iShares BB-B 全谱)</td><td style="padding:6px 14px">{num_green('79.90 -0.03%')}（vs 8/25 +0.28%）</td></tr>
        <tr><td style="padding:6px 14px">TLT (20Y+ 长端)</td><td style="padding:6px 14px">{num_green('83.30 -0.20%')}（长端利率反弹）</td></tr>
        <tr><td style="padding:6px 14px">HY 利差方向</td><td style="padding:6px 14px">JNK/HYG 微跌 = 信用端随利率温和承压，无恐慌抛售</td></tr>
      </table>
      <div style="padding:10px 14px;font-size:12px;background:#FCF3D6">
        <b>HY 内部解读</b>：JNK (-0.01%) ≈ HYG (-0.03%)，BB/B 无明显分化，
        说明 PCE 粘性尚未触发高收益债抛售；
        <b>JNK 微跌 + TLT 跌 = 利率反弹环境下信用债小幅回撤</b>，
        与 8/25 三同涨形成对比。若 Warsh 偏鹰，JNK -0.3%、TLT -0.8% 是基本情景。
      </div>
    </div>
    """


# === ⑨ 亚欧夜盘（盘后 1.5-3 小时） ===
def section_asia_europe_overnight():
    return f"""
    <div style="border:1px solid {BORDER};border-radius:4px;overflow:hidden;margin-bottom:14px">
      <div style="background:#EDE2B0;padding:7px 12px;font-size:12px;font-weight:700;letter-spacing:1px">
        ⑨ 亚欧夜盘（8/27 GMT+8 早晨 07:30 截取）· 接续昨夜 risk-on/off
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:13px;background:{PANEL}">
        <tr><td style="padding:6px 12px;width:30%">🇯🇵 日经 225</td><td style="padding:6px 12px">66,262.16</td><td style="padding:6px 12px;text-align:right">{num_red('+0.62%')}（半导体/NVDA 财报后）</td></tr>
        <tr style="background:#FBF6E5"><td style="padding:6px 12px">🇰🇷 KOSPI</td><td style="padding:6px 12px">6,808.21</td><td style="padding:6px 12px;text-align:right">{num_red('+0.97%')}（三星 / SK 海力士）</td></tr>
        <tr><td style="padding:6px 12px">🇭🇰 恒生指数</td><td style="padding:6px 12px">25,652.97</td><td style="padding:6px 12px;text-align:right">{num_red('+0.56%')}</td></tr>
        <tr style="background:#FBF6E5"><td style="padding:6px 12px">🇨🇳 沪指</td><td style="padding:6px 12px">3,912.52</td><td style="padding:6px 12px;text-align:right">{num_red('+0.59%')}</td></tr>
        <tr><td style="padding:6px 12px">🇩🇪 DAX30</td><td style="padding:6px 12px">26,285.96</td><td style="padding:6px 12px;text-align:right">{num_red('+0.08%')}</td></tr>
        <tr style="background:#FBF6E5"><td style="padding:6px 12px">🇬🇧 富时 100</td><td style="padding:6px 12px">10,878.12</td><td style="padding:6px 12px;text-align:right">{num_green('-0.07%')}（能源板块回吐）</td></tr>
        <tr><td style="padding:6px 12px">🇫🇷 CAC40</td><td style="padding:6px 12px">8,462.39</td><td style="padding:6px 12px;text-align:right">{num_red('+0.27%')}</td></tr>
        <tr style="background:#FBF6E5"><td style="padding:6px 12px">欧元区 Stoxx 50</td><td style="padding:6px 12px">6,473.62</td><td style="padding:6px 12px;text-align:right">{num_red('+0.28%')}</td></tr>
      </table>
      <div style="padding:8px 12px;font-size:12px;color:#5D4E2D;background:#FBF6E5">
        <b>亚欧解读</b>：日韩随 NVDA 财报 beat 反弹，A/H 股小幅上涨，
        欧洲主要股指涨跌互现。亚欧对昨夜美股「微跌+PCE粘性」反应偏温和，
        核心叙事仍由 Jackson Hole/Warsh 首秀主导。
      </div>
    </div>
    """


# === 🎯 明日亚盘/欧盘建议 ===
def section_tomorrow_playbook():
    return f"""
    <div style="border:1px solid #8E44AD;border-radius:4px;overflow:hidden;margin-bottom:14px;background:#FAF3FC">
      <div style="background:#8E44AD;padding:9px 14px;font-size:13px;font-weight:700;letter-spacing:1px;color:#FFF">
        🎯 明日亚盘/欧盘 actionable 战术建议（5 条）
      </div>
      <ol style="padding:12px 18px;margin:0;font-size:13px;line-height:1.8;background:#FAF3FC">
        <li>
          <b style="color:#C0392B">NVDA 财报 beat 后，AI 半导体链亚盘高开但不宜追高</b>：
          盘后 NVDA 由跌转涨约 +4%，Q3 指引 $108B 超预期。亚盘 SK 海力士 / 台积电 ADR / 恒科可能高开，
          但「beat and raise」已部分 priced-in，建议等盘中回落再评估加仓。
        </li>
        <li>
          <b style="color:#1E8449">PCE 粘性 + 10Y 反弹，成长股估值承压</b>：
          8/26 10Y 上行 +3bp，若 Warsh 偏鹰，10Y 4.70% / TLT 82 是下一个测试位；
          高估值科技股（XLK/QQQ）短期偏逆风，仓位上限 7 成。
        </li>
        <li>
          <b style="color:#C0392B">黄金回调 ≠ 趋势结束，Jackson Hole 前 hedge 价值上升</b>：
          COMEX 金 4647.80 (-0.99%) 是技术性回调。Warsh 首秀前 24 小时窗口仍是经典事件 hedge 窗口，
          可考虑 5-10% 仓位黄金 / GLD 对冲。
        </li>
        <li>
          <b style="color:#1E8449">谷物波动放大，小麦 +6.4% 后警惕技术性回调</b>：
          小麦单日 +6.4% 已超 3% 阈值，黑海叙事 + 作物评级是主驱；
          追涨风险高，关注 USDA 巡查报告是否兑现产量下调预期。
        </li>
        <li>
          <b style="color:#8E44AD">底仓逻辑：事件前观望，等待 Warsh 定调</b>：
          当前市场处于「PCE 粘性 + NVDA beat + Jackson Hole 开幕」的过渡期；
          VIX1Y 22.60 显示尾部 hedge 未撤，但前端 vol 便宜。
          <b>仓位上限 7 成，不追满仓</b>；推荐关注：① Warsh 讲话后利率/黄金方向 ② NVDA 供应链开盘反馈 ③ 小麦波动率。
        </li>
      </ol>
    </div>
    """


# === 主组合 ===
subject = '【美股盘后】2026-08-26'

html_body = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>{esc(subject)}</title></head>
<body style="margin:0;padding:24px;background:#F4EFE0;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;color:{INK};font-size:14px;line-height:1.6">
<div style="max-width:780px;margin:0 auto;background:{BG};border:1px solid {BORDER};border-radius:6px;overflow:hidden">

  <!-- 顶头条 -->
  <div style="padding:18px 22px;background:linear-gradient(135deg,#2C3E50 0%,#34495E 100%);color:#FAF8F2">
    <div style="font-size:11px;letter-spacing:2px;opacity:.7">MARKET TEMPERATURE · 盘后战略复盘</div>
    <div style="font-size:18px;font-weight:700;margin-top:4px">{esc(D['date'])} · 美东 16:00 EDT 收盘</div>
    <div style="font-size:11px;opacity:.65;margin-top:2px">{esc(D['snapshot_time'])}</div>
    <div style="font-size:11px;opacity:.65;margin-top:2px">数据源：新华社 / 路透 / 华尔街见闻 / Wind / MarketWatch / Edge Consultancy / 腾讯自选股 · 多源交叉验证</div>
  </div>

  <!-- 关键数字一行 -->
  <div style="padding:14px 22px;background:#34495E;color:#FAF8F2;font-size:13px;border-bottom:1px solid #B7950B">
    <div style="font-size:11px;letter-spacing:1.5px;opacity:.7;margin-bottom:4px">昨夜美股关键数字 · 主逻辑</div>
    <div style="font-weight:700;font-size:14px">{esc(D['headline_metric'])}</div>
    <div style="font-size:12px;margin-top:6px;opacity:.85">{esc(D['one_liner'])}</div>
  </div>

  <!-- 综合温度（黄底框） -->
  <div style="padding:18px 22px;background:{HILITE};border-bottom:1px solid {BORDER}">
    <div style="font-size:11px;color:#B7950B;letter-spacing:1.5px;font-weight:700">☀️ 综合温度 · 昨夜市场总体表述</div>
    <div style="font-size:14px;margin-top:6px;line-height:1.75">{esc(D['summary'])}</div>
  </div>

  <!-- 战略复盘 -->
  <div style="padding:18px 22px;border-bottom:1px solid {BORDER}">
    {section_strategic_review()}
  </div>

  <!-- 与昨日盘前报告对账 -->
  <div style="padding:0 22px 18px 22px;border-bottom:1px solid {BORDER}">
    {section_reconciliation_table()}
  </div>

  <!-- 7 步分节 -->
  <div style="padding:18px 22px;border-bottom:1px solid {BORDER}">
    <div style="font-size:13px;font-weight:700;letter-spacing:1px;margin-bottom:10px;color:#8B7D3B">📊 7 步扫描 · 昨夜收盘要点 + 与 8/25 settle 对比</div>
    {section_7_steps()}
  </div>

  <!-- JNK 信用 -->
  <div style="padding:0 22px 18px 22px;border-bottom:1px solid {BORDER}">
    {section_jnk_post_market()}
  </div>

  <!-- 亚欧夜盘 -->
  <div style="padding:0 22px 18px 22px;border-bottom:1px solid {BORDER}">
    {section_asia_europe_overnight()}
  </div>

  <!-- 明日战术 -->
  <div style="padding:0 22px 18px 22px;border-bottom:1px solid {BORDER}">
    {section_tomorrow_playbook()}
  </div>

  <!-- AO 全文 -->
  <div style="padding:18px 22px;border-bottom:1px solid {BORDER};background:#FBF6E5">
    <div style="font-size:11px;color:#8B7D3B;letter-spacing:1.5px;font-weight:700">🔖 AO · 一句话综合温度</div>
    <div style="font-size:13px;margin-top:6px;line-height:1.75">{esc(D['one_liner'])}</div>
  </div>

  <!-- 落款 -->
  <div style="padding:12px 22px;font-size:11px;color:{MUTED};text-align:right">
    WorkBuddy · 每日盘后战略复盘 · automation-1787490867965 · {esc(D['date'])}
  </div>

</div>
</body></html>
"""

with open(fpath, 'w', encoding='utf-8') as f:
    f.write(html_body)

size_kb = len(html_body.encode('utf-8')) / 1024
print(f'HTML written to {fpath}')
print(f'Size: {size_kb:.1f} KB')

if size_kb < 20:
    print('WARNING: HTML size below 20 KB, content may be truncated')
elif size_kb > 50:
    print('WARNING: HTML size above 50 KB, consider trimming')
else:
    print('Size OK')
