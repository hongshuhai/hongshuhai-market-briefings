# -*- coding: utf-8 -*-
"""国内大宗商品晨报生成器 · 基于七步测温框架
用法: python3 commodity_morning_report.py [YYYY MM DD]
数据依赖: commodity_temp_data.json / commodity_oi_data.json / silicon_data.json
静态上下文(宏观/日历/硅链基本面)在 CONTEXT 中, 每日运行前先搜索更新
"""
import json, sys, os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

CN = {"UR": "尿素", "RB": "螺纹钢", "CU": "沪铜", "AG": "沪银", "AU": "沪金", "SC": "原油",
      "MA": "甲醇", "TA": "PTA", "I": "铁矿石", "FG": "玻璃", "SA": "纯碱", "M": "豆粕",
      "JM": "焦煤", "J": "焦炭", "SI": "工业硅", "PS": "多晶硅"}

# ============ 每日更新的静态上下文(运行前先搜索更新) ============
CONTEXT = {
    # 宏观大气候（9/2 发出视角, 数据截至 9/1 收盘 + 8/31 PMI + 8/31-9/1 美联储转鹰）
    "macro": [
        ("制造业PMI(8月)", "49.8%", "8/31发布, +0.6pct 景气回升但仍处收缩区间; 产需双扩张(生产50.4/新订单50.6回扩张/新出口50.1); 购进价56.6(+3.4)/出厂价50.4(+2.6重返扩张)——上游价格回升, 工业品偏暖", "偏暖"),
        ("8月价格指数", "购进56.6 / 出厂50.4", "原油+有色上行拉动; 出厂价重返扩张区间=工业品涨价开始向下游传导, 但消费端CPI仍弱", "偏暖"),
        ("PPI同比(7月)", "+3.5%", "8/9发布, 环比-0.7%延续回落; 8月读数 9/9 发布", "偏暖转弱"),
        ("CPI同比(7月)", "+0.5%", "环比-0.1%, 核心CPI +0.9%温和; 8月读数 9/9 发布", "中性"),
        ("M2 / 社融(7月)", "M2 +7.7% / 社融+1.40万亿", "M2环比-0.3pct, 信贷转负(-3400亿), 实体融资意愿不足; 8月社融 9/10-9/15 发布", "偏冷"),
        ("美联储(9/15-16 FOMC)", "加息概率 68%", "9/3 凌晨 8 月褐皮书: 经济温和扩张但依赖 AI 数据中心、通胀顽固、消费K型分化 → CME 9月加息概率升至 68%(一周前 35%); 巴尔'若通胀未降温应果断加息'呼应沃什, 与财长贝森特相左; 9/4 非农 + 9/11 CPI 为最终变量; 决议北京时间 9/17 凌晨——若落地将抬升美元、压制全球商品定价水位", "转冷"),
        ("美元指数", "~99 反弹中", "加息预期升温推动美元走强, 对铜/油/金等全球定价商品从托底转为压制", "转冷"),
        ("美伊冲突(9/1-9/3)", "WTI 90.6 / 布油 95.4", "9/1-2 美军打击伊朗革命卫队目标, 9/2 两油轮在霍尔木兹海峡触雷爆炸, 美军已拦截 86 艘商船、特朗普威胁'随时再次打击'; SC 20日 +38.7%、9/2 夜盘再 +2.6%——能源是当前最强主线, 向化工/油服/航运传导", "偏暖(能源)"),
        ("政策信号", "反内卷+三锁+减产报备", "能耗国标+成本核算通则+盐城指导三锁成链; 8/31 硅料企业提报各基地减产方案至部委备案, 新疆大厂东疆停炉32台已执行(9/1 落地后盘面'利多兑现'连续两日走弱); 能耗测算将采用开工率关联折算系数校正", "偏暖"),
    ],
    # 今日及近期日历(9/3周四发出, 数据截至 9/2 收盘)
    "calendar": [
        ("9/3 今日", "美联储8月褐皮书(02:00已发) + 中国8月财新服务业PMI 09:45", "褐皮书: 经济温和扩张但增长依赖AI数据中心、通胀顽固、消费K型分化 → CME 9月加息概率68%(一周前35%); 财新服务业前值52.5, 关注是否延续扩张", "宏观"),
        ("9/3-4", "世界动力电池大会(四川宜宾)", "宁德时代/比亚迪/特斯拉等120余家中外龙头; 电池排产/固态电池/储能议题——碳酸锂需求侧验证窗口(9月排产~332GWh是否兑现)", "碳酸锂"),
        ("9/4 20:30", "美国8月非农就业", "FOMC前最关键数据; 9/2 ADP 仅 +3.8万(低于预期4.7万)偏弱先行, 机构对非农预期分歧大(5.6万~14万); 若大幅低于预期→9月加息概率回落, 商品喘息", "全品种"),
        ("9/7", "郑商所动力煤2609交割", "机构客户最后交易日, 持仓调整为200手整数倍", "黑色"),
        ("9/8", "上期所/能源中心个人2609持仓清零", "铜铝锌金白银螺纹等个人客户2609合约持仓须调整为0", "有色/黑色/贵金属"),
        ("9/9 09:30", "中国8月CPI/PPI", "PPI能否延续出厂价回升、CPI通缩压力是否缓解, 定调工业品需求", "全品种"),
        ("9/9 20:30", "USDA 8月供需报告", "北半球定产窗口, 美豆/玉米面积与单产", "农产品"),
        ("9/11 20:30", "美国8月CPI + 成品油调价窗口", "若CPI超预期→9月加息板上钉钉, 利空大宗; 油价调整影响化工品", "全品种"),
        ("9/12-13", "金砖国家领导人第十八次会晤(新德里)", "多边经贸合作看点, 关注大宗商品结算与资源合作议题", "宏观"),
        ("9/14", "广期所工业硅/碳酸锂/多晶硅2609交割月持仓调整", "机构客户最后交易日9/14; 2609仓单压力进入最后窗口", "硅链/锂链"),
        ("9/15", "中国8月工业增加值/固投/社零 + 70城房价", "经济三驾马车: 地产链数据决定黑色/建材方向", "黑色/建材"),
        ("9/15-16 02:00(北京9/17)", "美联储FOMC利率决议(含点阵图)", "下半年最关键会议; 加息概率68%(9/3褐皮书后), 若加息落地利空全球商品, 若意外按兵不动则利空出尽", "全品种"),
        ("9/21", "9月LPR报价", "若降息→利好地产/黑色; 维持不变中性", "黑色/建材"),
        ("9/24", "国内成品油调价窗口", "油价上调→利好化工品期货; 下调→利空", "化工/能源"),
        ("9月中旬", "尿素印度IPL标购", "出口需求唯一引擎, 上次标购已两个月", "尿素"),
        ("9月中旬", "江西枧下窝锂矿批复窗口", "宜春生态局8/26撤销原环评报告, 9月中前批复决定锂链强现实vs弱预期", "碳酸锂"),
        ("11月底", "工业硅老仓单强制注销", "16.77万吨老仓单换血, 4系品大多无法重注册, 制度断层最关键节点", "工业硅"),
        ("12/1", "美国对多晶硅加征15%关税+最低限价生效", "出口通道变化, 短期或刺激抢出口, 长期需求转移", "多晶硅"),
    ],
    # 硅链基本面快照 (9/3 发出, 9/2 收盘 + 紫金天风/百川/北方有色 9/2 口径)
    "silicon_fundamental": {
        "SI_spot": 9400,        # SMM 华东通氧553#(9/2 基本持平; 新疆通氧553# 8,700; 华东421# 9,550; 不通氧553# 华东9,200 持平; 97硅 8,600 +100)
        "PS_spot": 40660,       # SMM N型复投料均价(9/2, 40.66元/kg 持平; N型致密料 40.10元/kg 持平; 混包料 39.25; 颗粒硅 39.50)
        "PS_cost": "4.5-4.8万", # 完全成本区间(头部可压至3.8-4.3万; 百川9/1平均生产成本43,608.56元/吨)
        "SI_social_inv": "紫金天风9/1口径: 工厂34.72万吨(+1.41) + 市场20.95万吨(-0.2) = 场外55.67万吨; 叠加下游原料24.53万吨 + 注册仓单16.78万吨(33,559手), 总库存96.98万吨高位",
        "PS_chain_inv": "硅料厂库存32.79万吨(百川9/1, +1.05); 仓单23,940手=7.18万吨(9/1, +150手/+450吨); 硅片库存30.54GW(+1.73%, 大越口径); 硅片亏损/电池片盈利/组件盈利",
        "SI_open_rate": "9/2 新疆大厂东区减产已落地、西区暂未复产(综合月减3-4万吨, 影响周产~6.5万吨量级)——但减产预期已消化近两周, 9/1-9/2 连续两日'利多兑现'盘面走弱; 现货部分厂家封盘挺价, 97硅逆势+100",
        "PS_open_rate": "周产26,360吨(+1,080); 9月排产11.83-12.45万吨(环比+9.53%); 硅料厂库存超32万吨高位; 减产方案已报部委备案, 市场传闻减产计划但对盘面提振有限——政策预期与弱现实博弈",
        "PS_official_inv": "硅料厂库存32.79万吨(百川9/1); 期现商成交相对活跃、货源价与大厂高价单明显价差, 但下游硅片/电池片价续跌、主动补库意愿弱; N型致密料40.10元/kg持平, 有价无市; 毛利润-3,964.81元/吨(-10%, 紫金天风9/1)",
    },
    # 现货价表（贸易商主要成交品）—— 9/2 收盘综合报价(多数持平; 97硅 +100 为 9/2 少数上调项)
    # 数据源: 百川盈孚 / SMM / Mysteel / CBC / 长江有色 / 同花顺
    # 核心观点: 期货盘的代表品(通氧 553#、N 致密料)只是贸易商流通量的冰山一角;
    #          非通氧/非标品(99硅/97硅/551#等)的实际成交主流, 与期货盘基本脱钩
    # Frank 现场反馈(8/30 22:45):
    #   - 标准品期现市场(553#/421#可交割品): 期现商/大型冶炼厂/机构, 常态化期现套利
    #   - 非标品现货市场(99/97/551#等): 中小贸易商/磨粉厂/铝合金厂, 基本不做期现套利
    "silicon_spot_rows": [
        # ───── 标准品期现市场(可交割品)─────
        ("工业硅", "不通氧 553# (黄埔/华东/四川)", "9,000-9,400", "持稳", "贸易主流品 ~50%, 期现商套保基准; 华东9,200持平"),
        ("工业硅", "通氧 553# (华东基准)", "9,100-9,500", "持稳", "期货交割品, 流通量<10%; 华东9,400持平"),
        ("工业硅", "441# (华东/黄埔)", "9,400-9,800", "持稳", "铝合金主流, ~25-30%"),
        ("工业硅", "421# (华东/云南)", "9,300-9,700", "持稳", "化学级精品, 有机硅用; 华东9,550持平"),
        ("工业硅", "3303# (华东/福建)", "10,090-11,500", "持稳", "高品位, 出口/军工"),
        ("工业硅", "2202# (上海特级)", "14,060-14,200", "持稳", "化工/特殊钢"),
        # ───── 非标品现货市场(不可交割, 中小贸易商流通主力)─────
        ("工业硅(非标)", "99硅 (Si≥99%, 新疆/内蒙烟道灰+加工尾料)", "6,500-7,800", "持稳", "铝合金/铸造厂脱氧剂, 月流通~8-10万吨"),
        ("工业硅(非标)", "97硅 (Si≥97%, 磨粉厂烟粉)", "5,500-6,500", "持稳", "磨粉厂走量品, 月流通~3-5万吨"),
        ("工业硅(非标)", "551# (等外低品位, 通氧553边缘品)", "8,400-8,800", "持稳", "铸造+部分铝合金, 月流通~2-3万吨"),
        # ───── 多晶硅(标准品期现)─────
        ("多晶硅", "N型复投料 (棒状/东岳/大全)", "39,500-41,000", "持平", "主流料, 拉晶填充; 9/1均价40.66元/kg"),
        ("多晶硅", "N型致密料 (通威/大全)", "39,500-40,500", "持平", "期货交割品, 反内卷挺价最坚; 9/1均价40.10元/kg"),
        ("多晶硅", "N型菜花料 (二三线)", "36,000-38,000", "持稳", "低成本混包用; 混包料39.25元/kg"),
        ("多晶硅", "N型颗粒硅 (协鑫主供)", "37,000-41,000", "持平", "30%掺杂比例上限; 9/1均价39.50元/kg"),
        ("多晶硅", "P型致密料 (旧产能)", "32,000-34,000", "持稳", "PERC退场, 流通量缩减"),
        # ───── 行业利润行─────
        # 口径备注(9/1 紫金天风): 毛利润 -3,964.81元/吨(-10%); N型致密料生产成本43,608.56元/吨(百川) vs 市场均价40,100元/吨; 一线(通威/协鑫)仍微利, 二三线深度亏损
        ("利润", "多晶硅厂(全行业, 9/1紫金天风)", "净利 -1.6 元/kg", "亏损扩大", "毛利润-3,965元/吨(-10%); 生产成本43.61元/kg vs 均价40.1元/kg；一线(通威/协鑫)仍微利, 二三线深度亏损"),
    ],
    # 弱现实拆解(9/2 收盘更新)——客户问"为什么弱"时直接脱口而出的三句话
    "weak_reality_rows": [
        ("SI2611", [
            "11月老仓单集中注销压力: 33,559手 ≈ 16.78万吨(5吨/手, 9/1 口径); 总库存96.98万吨(紫金天风9/1: 场外55.67+下游24.53+仓单16.78)",
            "社会库存高位未解: 工厂34.72万吨(+1.41) + 市场20.95万吨; 东疆停炉32台虽已执行(月减3-4万吨), 但减产预期消化近两周, 9/2 盘面'利多兑现'收 8,650(-1.93%)——供给收缩滞后于价格",
            "下游多晶硅/有机硅采购疲软, 需求端无亮点; 现货分化: 97硅逆势 +100 至 8,600(非标品挺价), 华东通氧553# 9,400-9,500 持平(新疆通氧553# 8,700)",
        ]),
        ("PS2611", [
            "11月老仓单注销: 23,940手 ≈ 7.18万吨(3吨/手, 9/1 +150手/+450吨)",
            "全行业毛利润 -3,965 元/吨(-10%, 紫金天风9/1), 亏损扩大; 硅料厂库存32.79万吨(+1.05, 百川); 减产方案已报部委备案, 但 9/2 传闻减产对盘面提振有限——预期 vs 现实博弈",
            "下游硅片/电池片价格续跌(N型硅片1.11元/片持平; 组件0.73元/瓦 -0.07%), 硅片库存30.54GW仍在涨、去库困难; 期现商成交相对活跃但下游刚需补库为主, N型致密料40.10元/kg持平, 有价无市",
        ]),
    ],
    # 温度判定(六板块, 9/2 收盘后七步交叉验证 — 能源独强(美伊冲突), 双硅/锂回调, 黑色冲高回落)
    "temps": {
        "能源": 40.5, "黑色建材": 37.5, "农产品": 37.0,
        "化工": 36.5, "贵金属": 34.5, "有色": 33.0,
    },
    "headline": "9/3 视角(9/2 收盘): 能源独强——美伊冲突升级(霍尔木兹两油轮触雷、美军拦截86艘商船、特朗普威胁再打), SC 20日+38.7% 领涨、夜盘再+2.6%, WTI 90.6/布油 95.4; 黑色冲高回落(双焦9/2夜盘-2%), 双硅减产'利多兑现'连续两日走弱(SI2611 收8,650 -1.93% / PS2611 收36,900 -1.85%, 前日+3.22%反弹回吐); 碳酸锂连续第二日回调, LC2701 收154,780(-3.2%昨结口径/盘中低153,200), 减仓9,123手至39.58万, 现货跟跌3,500至15.65万, 基差走扩至+1,720; 宏观: 美联储褐皮书通胀顽固→9月加息概率68%(一周前35%), 9/4 非农 + 9/11 CPI 定乾坤",
    "overall": "37°C 结构性偏热(能源独强·硅锂降温)",
    # ============ 第七段 碳酸锂主战场 (9/3 发出, 9/2 收盘 + SMM/光大/北方有色 9/2 口径) ============
    # Frank 23:51 临时新增主战场需求. 数据来源:
    # - 期货行情: 广期所(新浪期货/东财K线), 9/2 收盘 LC2701 收 154,780(-3.2%昨结口径, 盘中低153,200), 昨结159,960, 持仓395,794(减9,123)
    # - 现货 + 库存 + 周产: SMM/百川盈孚/光大期货/北方有色 9/2 口径
    # - 事件: 9/2 电池大厂因原料短缺排产下修5%传闻打击情绪; 雅保智利9/2罢工启动; 9/3-4 世界动力电池大会(宜宾)
    # 核心叙事: 强现实 vs 弱预期的博弈窗口 — 连续两日回调(16.29万→15.48万)后进入"现货验证"阶段
    #   - 强现实: 连续17周去库 + 9月排产高位 + 缺口2.5万吨 + 矿价坚挺
    #   - 弱预期: 电池大厂排产下修传闻 + 澳矿复产到港 + 枧下窝复产 + 仓单高位 + 美联储加息预期压制
    "lithium_fundamental": {
        # (last, prev_settle, oi, volume) -- 9/2 收盘口径(新浪期货: last=收盘, prev_settle=昨结)
        "LC2701": (154780, 159960, 395794, 186331),  # 主力·收15.48万(-3.2%昨结口径/-1.95%收盘口径, 盘中低153,200), 昨结159,960, 持仓39.58万(-9,123)
        "LC2705": (150840, 154200, 65201, 11816),    # 远月·贴水走扩至-3,940(近月−远月=+3,940), 淡季预期压制
        "LC2609": (155000, 158340, 11146, 692),       # 临交割·9/14进入交割月持仓调整
        # 基本面 (9/2 SMM/光大/北方有色口径; 现货为 9/2 收盘价)
        "SMM_battery_spot": "156,500 元/吨 (9/2 -3,500, 电池级 155,000-158,000; SMM口径同跌)",
        "SMM_industrial_spot": "152,000 元/吨 (9/2 约-3,500, 工业级跟跌)",
        "baichuan_battery_spot": "15.3-15.75 万元/吨 (9/2 回落, 期货下跌带动买卖双方观望)",
        "baichuan_industrial_spot": "15.0-15.35 万元/吨 (9/2 跟跌)",
        "SMM_lithium_hydroxide": "146,000-148,000 元/吨 (粗颗粒, 9/2 高位回落)",
        "SMM_spodumene_6pct": "2,285 美元/吨 (+5 美元, 矿价坚挺; 外采锂矿点价利润仍宽裕)",
        # 库存
        "SMM_total_inv": "78,802 吨 (大样本 8/27, -7,590 吨/周, 连续 17 周去化, 年内最低)",
        "SMM_smaller_inv": "61,632 吨 (环比 -4,745), 冶炼厂 10,128 / 下游 31,098 / 其他 20,407",
        "GFEX_warrant": "45,389 吨 (9/2 -450; 9/1 曾+215至45,839), 高位小幅回落, 暂未形成新交割压力",
        # 供给
        "weekly_output": "23,808 吨/周 (+801); 9月产量预计环比+10%至12.4万吨; 检修结束+澳矿陆续到港, 供给端增量逐步兑现",
        "demand_aug": "9月锂电全市场排产~332GWh(环比+9.2%); 铁锂+6%(61.2万吨)三元-5%(86,450吨); 9月供需缺口2.5-2.6万吨, 延续去库但边际放缓",
        "demand_lfp": "9/2 传某电池大厂因原料短缺(非需求弱)排产下修5%→市场排产预期下调, 打击情绪; 铁锂周产量升至13.03万吨, 旺季未转弱",
        "spread_basis": "基差 +1,720 元/吨(基差率 1.1%; 电碳 156,500 − LC2701 154,780, 9/2收盘), 期货贴水加深——正套(买现卖期)窗口关闭, 反套(卖现买期)幅度仍不足(1.1% 低于持有成本)暂不可做",
        "spodumene_cost": "锂矿加工费 18,250 元/吨 LCE 等效成本, 完全成本约 14.9 万(电碳); 外采矿点价利润扩至9,500+"
    },
    "lithium_spot_rows": [
        # ───── 期货交割基准品(电池级, 标准化 GB/T 11075-2013 99.5%)─────
        ("电池级碳酸锂(99.5%)", "SMM 江苏/四川/江西(电碳主流)", "155,000-158,000", "-3,500", "期货交割品, 期现商套保基准, ~70%; 9/2均价156,500"),
        ("电池级碳酸锂(99.5%)", "新料/客供品(通威/赣锋长协)", "156,000-160,000", "-3,000~-3,500", "下游材料厂首选, 价高于流通货"),
        # ───── 工业级 / 准电碳(主流走量品)─────
        ("工业级碳酸锂(99.2%)", "SMM 主流(青海/盐湖)", "150,000-154,000", "-3,500", "工业润滑/玻璃/陶瓷主流, ~25%; 9/2约152,000"),
        ("准电碳(99.3%)", "市场流通货(贸易商货)", "151,000-155,000", "-3,000", "中小正极厂混包用, 价介于工碳与电碳"),
        # ───── 上游原料成本端─────
        ("氢氧化锂", "SMM 电池级(56.5%)", "144,000-149,000", "-2,000~-3,000", "高镍三元专用; 9/2粗颗粒146,000-148,000"),
        ("锂精矿(6%CIF)", "澳洲主力 + 津巴布韦", "2,285 美元/吨", "+5 美元", "矿价坚挺; 澳矿复产但发运未明显恢复; LCE 等效成本 ~8 万"),
        # ───── 行业利润行─────
        ("利润", "锂盐厂(全行业, 9/2口径)", "净利 +0.7 万元/吨", "旺季回落", "电碳均价15.65万 vs 完全成本 ~14.9万; 一线(赣锋/天齐)盈利稳定, 二三线转盈"),
    ],
    # 强现实 vs 弱预期拆解(9/2 更新)——客户问"为什么是博弈窗口"时脱口而出版
    "lithium_weak_reality_rows": [
        ("LC2701", [
            "强现实: 连续 17 周去库, SMM 大样本库存 78,800 吨(年内最低, 周降 7,600 吨), 库销比即将跌破 0.6 个月; 9/2 现货跌 3,500 后 15.6 万附近仍获买盘(15.5万以下下游逢低采购意愿回升)",
            "旺季需求: 9 月锂电排产 ~332GWh(+9.2%), 铁锂排产 +6%(61.2万吨, 有抢货), 但 9/2 传某电池大厂因原料短缺(非需求弱)排产下修 5% → 排产预期下修打击情绪, 三元端 9 月 -5%",
            "供给扰动: 雅保智利 400+ 工会成员 9/2 起合法罢工已启动(97.49% 支持) + 检修结束但澳矿复产发运未明显恢复 + 锂精矿 6% CIF 2,285 美元坚挺",
            "弱预期: 澳矿复产/扩产 + 枧下窝复产(流程慢于预期) + 仓单 45,389 吨高位 + 美联储 9 月加息概率 68% 压制商品定价水位; 9/1-9/2 连续两日回调(16.29万→15.48万) = 前期涨幅兑现",
            "枧下窝变数: 8/26 宜春生态局撤销原环评报告 → 复产节奏远慢于预期, 9 月中批复窗口仍是扳机; 短期进入'现货持续去库、远期供应增加'的拉锯, 运行区间参考 15.2-16.2 万",
        ]),
    ],
    # Actionable 三角色(9/2 收盘更新锚定价位——LC2701 收 15.48 万, 连续两日回调, 基差走扩至+1,720)
    # 数据源: 光大期货 / 国联期货 / 海证 / 北方有色 9/2 盘后综合
    "lithium_actionable": [
        ("上游锂盐厂<br><span style=\"font-weight:400;font-size:11px;color:#57606f;\">赣锋/天齐/永兴</span>",
         "LC2701 收 15.48 万(9/2, -3.2%昨结口径, 盘中低 15.32 万)<br><span style=\"color:#57606f;\">两日从 16.29 万高点回落 8,080 元, 完全成本 14.9 万; 现货 15.65 万仍保 ~0.7 万/吨利润</span>",
         "① <b>当前 15.48 万: 8/31 已兑现'16 万加至 50%+'触发, 套保头寸继续持有</b>——旺季高价窗口虽回落但现货端仍盈利, 正常出货, 不宜在 15.5 万附近恐慌减空<br>"
         "② 若反弹回补至 <b>16.3-16.5 万</b>(前高压力区): <b style=\"color:#d63031;\">可加至 60-70%</b>——16.3 上方仍是'情绪定价区', 越涨越值得卖<br>"
         "③ 若继续回落至 <b>14.5 万以下</b>: <b style=\"color:#d63031;\">释放部分空头</b>(从 50% 降至 20%), 同时<b>惜售现货</b>——14.5 万逼近'舒适区'下沿(14-15 万), 旺季去库背景下继续做空性价比下降; ⚠ <b>切忌只释放不复建</b>: 若 9 月排产终值再超预期冲回 16+, '既丢了空头、也没惜售'。等企稳再分批重建。",
         "上游卖"),
        ("中游贸易商<br><span style=\"font-weight:400;font-size:11px;color:#57606f;\">期现商/正极厂贸易部</span>",
         "基差 +1,720 (现 15.65万 − 期 15.48万)<br><span style=\"color:#57606f;\">基差率 1.1%; 期货贴水加深(9/1 +640 → 9/2 +1,720), 但幅度仍不足以覆盖持有成本</span>",
         "① <b>反套(卖现货买期货)仍不可做</b>——基差率仅 1.1%, 距覆盖仓储+资金成本(约 2-3% 年化)仍有距离, 且仓单 45,389 吨高位, 反向套利承担仓单压力<br>"
         "② <b>正套(买现货卖期货)窗口继续关闭</b>——期货贴水 1,720 无锁定空间; 持有现货者正常出货<br>"
         "③ <b>月差套利</b>: LC2701-LC2705 价差 <b>+3,940</b>(9/2收盘) 逼近 +4,000 加码阈值 → '买近卖远'持有中; <b>止损 +1,900</b>(跌破平衡区+2,000~+3,500 下沿, 弱预期占优); <b>站稳 +4,000 可加码</b>; <b>止盈 +4,500</b> 或时间止盈(10/15 前未到目标价则平仓); 持有至 10 月中 <b>别死守</b>(枧下窝 9 月中批复 → 反向回归立刻平)",
         "中游观望"),
        ("下游正极厂<br><span style=\"font-weight:400;font-size:11px;color:#57606f;\">铁锂厂/三元厂</span>",
         "LC2701 当前 15.48 万(两日 +8.4% 后回吐 8,080 元)<br><span style=\"color:#57606f;\">已回踩进入 15.2-15.5 万分批买保区(参考区间下沿 15.2 万)</span>",
         "① <b>当前 15.48 万: 进入分批建仓区</b>——两日回吐 8,080 元后利好兑现压力释放大半, 可启动买入套保(30%-50% 远期原料)<br>"
         "② <b>场景拆解:</b><br>"
         "&nbsp;&nbsp;• 若回踩 15.2-15.3 万(参考区间下沿, 大概率): 按计划继续分批买入, 锁定四季度旺季成本<br>"
         "&nbsp;&nbsp;• 若极端回落至 <b>14 万以下</b>(强现实证伪/枧下窝提前批复): <b style=\"color:#d63031;\">加至 70%+</b>, 3-6 个月'安全垫价位'<br>"
         "&nbsp;&nbsp;• 若再次冲高突破 <b>17 万</b>(逼仓): 坚决不追, 等待更极端的情绪顶回落",
         "下游买"),
    ],
    # 验证信号(9/2 更新)——LC 价差的边界值触发器 + 9/2 第三次实测
    "lithium_signals": {
        "LC2701-LC2705": 3940,  # 9/2 收盘价差 +3,940 (154780-150840), 从 9/1 +3,660 走扩 280
        "tiers": [
            ("收窄至 +1,500 以内", "近端供需全面宽松(枧下窝复产/澳矿放量), 近月估值见顶"),
            ("维持 +2,000~+3,500", "平衡区; 9/2 已走扩至 +3,940, 突破平衡区上沿逼近 +4,000 加码线"),
            ("走扩至 +4,000 以上", "近月去库继续加速 + 枧下窝延期 + 储能超预期, 多头逻辑成立——站稳可加码买近卖远"),
            ("突破 +5,000", "近月逼仓风险, 注意月差反复无常"),
        ],
    },
    # 碳酸锂专属事件 (9/3 精简)——与通用 calendar 去重后仅保留锂链独有条目
    # 已去重(通用日历均已覆盖): 动力电池大会9/3-4 / 广期所2609持仓调整9/14 / FOMC 9/15-16 / 老仓单注销11月底 / 枧下窝9月中 / 雅保罢工9/2已启动
    "lithium_events": [
        ("9/9 09:30", "8 月电池排产终值", "9 月排产 ~332GWh(+9.2%) 共识; 9/2 电池大厂下修 5% 传闻待证伪; 终值上修→近月继续走强", "碳酸锂"),
        ("9/11", "雅保智利罢工进展观察", "9/2 已启动; 若扩大至港口物流→供给实质收紧, 近月支撑增强", "碳酸锂"),
    ],
}
# =============================================================

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

    cmd = load("commodity_temp_data.json") or {}
    oi = load("commodity_oi_data.json") or {}
    sil = load("silicon_data.json") or {}

    sector = cmd.get("sector", {})
    kline = cmd.get("kline", {})
    ts = cmd.get("term_structure", {})
    dom = cmd.get("dominant", {})

    # ---- 期限结构: 展期收益率(结算价口径, 按实际月份间隔年化) ----
    # 结构判定五档(2026-09-02 Frank 口径修正): 供需平衡时市场付满额仓储+资金成本,
    # 满carry contango 约 -3%~-6%; -3%~+3% = 偏紧(不愿付全额仓储费); -6%~-3% = 正常持有成本; <=-6% = 过剩定价
    def months_between(c1, c2):
        y1, m1 = int(c1[:2]), int(c1[2:])
        y2, m2 = int(c2[:2]), int(c2[2:])
        return max((y2 - y1) * 12 + (m2 - m1), 1)

    def struct_label(roll):
        if roll > 3:
            return "贴水(现货紧)"
        if roll > -3:
            return "偏紧(近平水)"
        if roll > -6:
            return "正常持有成本(满carry)"
        return "深升水(过剩定价)"

    term_rows = []
    for prod, rows in ts.items():
        valid = [r for r in rows if r.get("settle", 0) > 0]
        if len(valid) < 2:
            continue
        rows_sorted = sorted(valid, key=lambda r: r["contract"])
        dom_c = dom.get(prod, {}).get("contract")
        prices = {r["contract"]: r for r in rows_sorted}
        keys = [r["contract"] for r in rows_sorted]
        if dom_c in keys and keys.index(dom_c) < len(keys) - 1:
            next_c = keys[keys.index(dom_c) + 1]
            p_dom = prices[dom_c]["settle"]
            p_next = prices[next_c]["settle"]
            if p_next > 0:
                spread = p_dom - p_next
                pct = spread / p_dom * 100
                roll = pct * 12.0 / months_between(dom_c[-4:], next_c[-4:])
                term_rows.append((prod, dom_c, next_c, spread, pct, roll,
                                  struct_label(roll)))
    term_rows.sort(key=lambda x: -x[5])

    # ---- 板块表现 ----
    perf = []
    for prod, k in kline.items():
        if isinstance(k, dict) and "chg_20d" in k:
            perf.append((prod, k.get("contract", ""), k.get("chg_20d", 0), k.get("chg_5d", 0), sector.get(prod, "")))
    perf.sort(key=lambda x: -x[2])
    # 加入硅链(9/2收盘20日涨跌幅, 取自东财K线 secid=225.SI2611/PS2611: 8/5收8420/35625 → 9/2收8650/36900)
    perf_silicon = [("PS(多晶硅)", "PS2611", 3.6, None, "光伏链"), ("SI(工业硅)", "SI2611", 2.7, None, "光伏链")]

    # ---- 持仓 ----
    oi_rows = []
    if isinstance(oi, dict):
        # 兼容 {合约: {...}} 与 {rows: [...]} 两种格式
        for k, v in oi.items():
            if isinstance(v, dict) and "oi_now" in v:
                r = dict(v)
                r["contract"] = k
                r["oi_chg"] = v.get("oi_chg_20d", v.get("oi_chg", 0))
                r["product"] = k.rstrip("0123456789")
                oi_rows.append(r)
    elif isinstance(oi, list):
        oi_rows = [r for r in oi if isinstance(r, dict) and "oi_now" in r]

    # ---- 硅链 ----
    sq = sil.get("quotes", {})

    def q(c):
        r = sq.get(c, {})
        return r.get("last", 0), r.get("settle", 0), r.get("oi", 0), r.get("volume", 0)

    si11 = q("SI2611"); si12 = q("SI2612")
    ps11 = q("PS2611"); ps12 = q("PS2612")
    # 价差统一口径: 近月−远月(正=back, 负=contango/远月升水), 与锂链 LC2701-LC2705、第四章 term_rows(主力−次主力)一致
    si_gap = (si11[0] - si12[0]) if si11[0] and si12[0] else 0   # SI2611-SI2612, 9/1: -320(远月升水)
    ps_gap = (ps11[0] - ps12[0]) if ps11[0] and ps12[0] else 0   # PS2611-PS2612, 9/1: -3,705(远月升水)

    RED, GREEN = "#d63031", "#00875a"
    def col(v):
        return RED if v > 0 else (GREEN if v < 0 else "#57606f")
    def sign(v, fmt="%+.1f"):
        return (fmt % v) if v is not None else "—"

    # ============ HTML ============
    H = []
    A = H.append
    A('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>')
    A('<body style="margin:0;padding:0;background:#f4f6f8;font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\',\'Microsoft YaHei\',sans-serif;color:#24292e;">')
    A('<div style="max-width:680px;margin:0 auto;padding:16px 12px;">')

    # 头部
    A('<div style="background:linear-gradient(135deg,#1a3a5c 0%,#2c5f8a 100%);border-radius:10px 10px 0 0;padding:22px 24px;color:#fff;">')
    A('<div style="font-size:12px;opacity:.85;letter-spacing:2px;">DOMESTIC COMMODITY MORNING BRIEF · 七步测温框架</div>')
    A('<div style="font-size:24px;font-weight:700;margin:6px 0 4px;">国内大宗商品晨报</div>')
    # 中文星期
    wk_map = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    try:
        wd = wk_map[datetime(int(y), int(m), int(dd)).weekday()]
    except Exception:
        wd = "星期四"
    A('<div style="font-size:13px;opacity:.9;">%s年%s月%s日 · %s · 数据截至昨收盘+今日夜盘</div>' % (y, m, dd, wd))
    A('<div style="display:inline-block;margin-top:10px;background:rgba(255,255,255,.15);border-radius:20px;padding:5px 14px;font-size:13px;">🌡 市场综合温度: <b>%s</b></div>' % CONTEXT["overall"])
    A('</div>')

    # 一句话
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-top:none;padding:14px 24px;font-size:14px;line-height:1.7;">')
    A('<b style="color:#1a3a5c;">▎今日一句话</b><br>%s' % CONTEXT["headline"])
    A('</div>')

    # 1 温度计
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #d63031;padding-left:10px;margin-bottom:12px;">一 · 六板块温度计</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;">')
    for name, t in sorted(CONTEXT["temps"].items(), key=lambda x: -x[1]):
        bar_red = min(t, 45)
        pct = int(t / 45 * 100)
        tc = "#d63031" if t >= 36 else ("#e17055" if t >= 33 else ("#57606f" if t >= 27 else "#00875a"))
        A('<tr>')
        A('<td style="padding:5px 0;width:70px;color:#57606f;">%s</td>' % name)
        A('<td style="padding:5px 8px 5px 0;"><div style="background:#eef1f4;border-radius:4px;height:14px;position:relative;">'
          '<div style="background:%s;border-radius:4px;height:14px;width:%d%%;"></div>'
          '<div style="position:absolute;left:44%%;top:-2px;width:1px;height:18px;background:#b2bec3;"></div></div></td>' % (tc, pct))
        A('<td style="width:52px;text-align:right;font-weight:700;color:%s;">%.1f°C</td></tr>' % (tc, t))
    A('</table>')
    A('<div style="font-size:12px;color:#8b949e;margin-top:8px;line-height:1.6;">刻度: 温度=动量+期限结构+持仓的交叉<b>主观读数</b>(无固定公式, 各板块不横向可比); <b>水位看绝对值</b>(当前六板块全部>33=整体偏热), <b>分化看温差</b>(最高−最低=7.5°C, 能源独强型分化); 9/2 能源升温至 40.5(美伊冲突, SC 20日+38.7%)、硅链/锂链回调降温, 关注 9/15-16 FOMC(北京时间 9/17 凌晨决议) 加息预期 68% 对全市场定价水位的压制。</div>')
    A('</div>')

    # 2 宏观
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #2c5f8a;padding-left:10px;margin-bottom:12px;">二 · 宏观大气候: 暖风仍在, 但美联储转鹰成新变量</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">指标</th><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">读数</th><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">解读</th><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">温度</th></tr>')
    for name, val, note, t in CONTEXT["macro"]:
        A('<tr><td style="padding:6px 8px;border:1px solid #e1e4e8;font-weight:600;">%s</td><td style="padding:6px 8px;border:1px solid #e1e4e8;color:#1a3a5c;font-weight:700;">%s</td><td style="padding:6px 8px;border:1px solid #e1e4e8;color:#57606f;">%s</td><td style="padding:6px 8px;border:1px solid #e1e4e8;">%s</td></tr>' % (name, val, note, t))
    A('</table>')
    A('</div>')

    # 3 板块轮动
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #d63031;padding-left:10px;margin-bottom:12px;">三 · 板块轮动(20日涨跌幅)</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">品种</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">主力</th><th style="text-align:right;padding:5px 8px;border:1px solid #e1e4e8;">20日</th><th style="text-align:right;padding:5px 8px;border:1px solid #e1e4e8;">5日</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">板块</th></tr>')
    merged = [(p, c, c20, c5, s) for (p, c, c20, c5, s) in perf] + [(p, c, c20, None, s) for (p, c, c20, _, s) in perf_silicon]
    merged.sort(key=lambda x: -x[2])
    for p, c, c20, c5, s in merged:
        c5s = sign(c5, "%+.2f") if c5 is not None else "—"
        A('<tr><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;">%s</td><td style="padding:5px 8px;border:1px solid #e1e4e8;color:#57606f;">%s</td>'
          '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:%s;">%s</td>'
          '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;color:%s;">%s</td>'
          '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#8b949e;">%s</td></tr>' % (p, c, col(c20), sign(c20), col(c5 or 0), c5s, s))
    A('</table>')
    A('<div style="font-size:12px;color:#8b949e;margin-top:8px;">9/2 领涨=能源(SC 20日+38.7%, 美伊冲突升级)与黑色(双焦20日+17~20%)、化工(MA 20日+18.2%, 能化共振); 垫底=有色(铜20日+0.8%温吞)与贵金属(白银5日-6.7%后9/2反弹)。硅链 20日 PS +3.6%/SI +2.7% 居中(但9/2当日双硅齐跌~1.9%, 减产利多兑现); 玻璃 5日+7% 但 20日仍-0.5%(地产链短反弹)。</div>')
    A('</div>')

    # 4 期限结构
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #6c5ce7;padding-left:10px;margin-bottom:12px;">四 · 期限结构(年化展期收益率) — 核心维度</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">品种</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">主力→次主</th><th style="text-align:right;padding:5px 8px;border:1px solid #e1e4e8;">价差</th><th style="text-align:right;padding:5px 8px;border:1px solid #e1e4e8;">年化</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">结构</th></tr>')
    for prod, dc, nc, sp, pct, roll, st in term_rows:
        A('<tr><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;">%s</td><td style="padding:5px 8px;border:1px solid #e1e4e8;color:#57606f;">%s→%s</td>'
          '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:%s;">%+.0f</td>'
          '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:%s;">%+.1f%%</td>'
          '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#8b949e;">%s</td></tr>' % (prod, dc[-4:], nc[-4:], col(roll), sp, col(roll), roll, st))
    # 硅链补充
    A('<tr><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;">SI(工业硅)</td><td style="padding:5px 8px;border:1px solid #e1e4e8;color:#57606f;">2611→2612</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:%s;">%+.0f</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:%s;">制度断层</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#8b949e;">新交割标准</td></tr>' % (col(si_gap), si_gap, col(si_gap)))
    A('<tr><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;">PS(多晶硅)</td><td style="padding:5px 8px;border:1px solid #e1e4e8;color:#57606f;">2611→2612</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:%s;">%+.0f</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:%s;">政策断层</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#8b949e;">反内卷预期</td></tr>' % (col(ps_gap), ps_gap, col(ps_gap)))
    A('</table>')
    A('<div style="font-size:12px;color:#8b949e;margin-top:8px;line-height:1.6;">注: 年化=近月−远月展期收益(正=back/近月升水, 负=contango/远月升水)。供需平衡时市场付满仓储+资金成本, <b>满carry contango 约 −3%~−6%</b>; <b>−3%~+3%=偏紧</b>(不愿付全额仓储费持货), <b>−6%~−3%=正常持有成本区</b>(属满carry而非过剩), <b>低于−6%=过剩定价</b>; 正值=现货真紧(SC 受美伊冲突驱动近月升水显著, 年化+50%上下; 甲醇/豆粕/TA/豆油/铁矿等); 铁矿价格弱但近月 back=仓单与交割品结构问题; 双焦远月贴水=旺季预期已计入。SC 三口径并存(日盘收盘/官方结算/夜盘结算)不矛盾, 本章用结算口径。</div>')
    A('</div>')

    # 5 持仓(四象限: 同周期 20日价格 × 20日持仓, 杜绝跨周期错配; 与第六章"9/1当日"实测是不同窗口, 不矛盾)
    si20 = next((x[2] for x in perf_silicon if "SI" in x[0]), 0.0)
    ps20 = next((x[2] for x in perf_silicon if "PS" in x[0]), 0.0)
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #00b894;padding-left:10px;margin-bottom:12px;">五 · 持仓与资金(价格×持仓四象限 · 20日窗口)</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">品种</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">合约</th><th style="text-align:right;padding:5px 8px;border:1px solid #e1e4e8;">收盘</th><th style="text-align:right;padding:5px 8px;border:1px solid #e1e4e8;">持仓(手)</th><th style="text-align:right;padding:5px 8px;border:1px solid #e1e4e8;">20日涨幅</th><th style="text-align:right;padding:5px 8px;border:1px solid #e1e4e8;">20日OI变化</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">行为解读(20日)</th></tr>')
    if oi_rows:
        items = sorted(oi_rows, key=lambda r: -abs(r.get("oi_chg_20d", 0)))
        for r in items:
            chg = r.get("oi_chg_20d", 0)
            px20r = r.get("px_chg_20d", 0)
            A('<tr><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;">%s</td>'
              '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#8b949e;">%s</td>'
              '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;">%s</td>'
              '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;color:#57606f;">%s</td>'
              '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:%s;">%s</td>'
              '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:%s;">%s</td>'
              '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#57606f;">%s</td></tr>' % (
                  CN.get(r.get("product", ""), r.get("contract", "?")), r.get("contract", ""), r.get("close", "—"),
                  "{:,.0f}".format(r.get("oi_now", 0)) if r.get("oi_now") else "—",
                  col(px20r), sign(px20r, "%+.1f%%"),
                  col(chg), sign(chg, "%+.1f%%"), r.get("combo", r.get("pattern", ""))))
    # 硅链持仓(20日口径, 与第六章9/1当日实测不同窗口)
    A('<tr><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;">SI(工业硅)</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#8b949e;">SI2611</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;">%s</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;color:#57606f;">%s</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:#d63031;">%+.1f%%</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:#d63031;">大幅增仓</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#57606f;">增仓上涨(新多入场)</td></tr>' % ("{:,.0f}".format(si11[0]), "{:,.0f}".format(si11[2]), si20))
    A('<tr><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;">PS(多晶硅)</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#8b949e;">PS2611</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;">%s</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;color:#57606f;">%s</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:#d63031;">%+.1f%%</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;text-align:right;font-weight:700;color:#d63031;">高位增仓</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#57606f;">增仓上涨(新多入场)</td></tr>' % ("{:,.0f}".format(ps11[0]), "{:,.0f}".format(ps11[2]), ps20))
    A('</table>')
    A('<div style="font-size:12px;color:#8b949e;margin-top:8px;">20日窗口(价格与持仓同周期): <b>14/14 品种全部增仓, 无减仓</b>——11 个增仓上涨(新多入场) + 3 个增仓对峙。三个对峙点: 玻璃 OI+163% 但价格 -0.5%(空头最拥挤也最危险)、尿素 OI+115% 价格仅+0.1%、沪铜 OI+55% 价格+0.8%; 增仓上涨代表: 焦炭 OI+227% 价格+17.6%(但 6.8万手小盘子易放大)、螺纹 OI+232% 价格+4.0%(移仓成分大, 见注②)。</div>')
    A('<div style="font-size:11px;color:#8b949e;margin-top:4px;">注①: 持仓=各品种<b>主力单合约</b>(见合约列), 非全品种合计——品种间持仓绝对值不可直接横向比(焦炭盘子小 vs 豆粕/玻璃盘子大, 属品种特性)。<br>'
      '注②: 9-10 月正处 2609/2610→2701 主力迁移窗口, 单合约 OI 放大含<b>移仓成分</b>, 不能直接解读为"增量资金入场"; 增量资金需看全品种总持仓或保证金沉淀, 本章不据此下结论。<br>'
      '注③: 本章为20日窗口; 第六章"9/2 当日实测"为当日窗口, 两者尺度不同(如 SI 20日增仓上涨 vs 当日减仓下跌=中期资金仍在流入、短期获利了结), 不矛盾。</div>')
    A('</div>')

    # 6 硅链主战场
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #fdcb6e;padding-left:10px;margin-bottom:12px;">六 · 主战场: 硅链(工业硅/多晶硅) — 期货热36°C × 实体冷25°C</div>')
    sf = CONTEXT["silicon_fundamental"]
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">合约</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">最新</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">昨结</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">持仓(手)</th><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">角色</th></tr>')
    def gap_note(gap, label):
        # 近月−远月口径下的升水方向说明: 负=远月升水, 正=近月升水
        if gap < 0:
            return "%s, 远月升水 %s 元" % (label, "{:,.0f}".format(-gap))
        return "%s, 近月升水 %s 元" % (label, "{:,.0f}".format(gap))

    for c, last, settle, oiv, note in [
        ("SI2611", si11[0], si11[1], si11[2], "主力·弱现实定价"),
        ("SI2612", si12[0], si12[1], si12[2], gap_note(si_gap, "新交割标准·制度断层")),
        ("PS2611", ps11[0], ps11[1], ps11[2], "主力·弱现实定价"),
        ("PS2612", ps12[0], ps12[1], ps12[2], gap_note(ps_gap, "反内卷预期·政策断层")),
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
    # 弱现实拆解(8/30 23:11 第四轮反馈①)——客户问"为什么弱"时直接脱口而出
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
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:12px;color:#57606f;margin-top:10px;border-collapse:collapse;">')
    A('<tr><td style="padding:4px 8px 4px 0;width:88px;vertical-align:top;color:#8b949e;line-height:1.9;">现货锚</td>'
      '<td style="padding:4px 0;line-height:1.5;">'
      '<table width="100%" cellpadding="3" cellspacing="0" style="font-size:12px;border-collapse:collapse;">'
      '<tr style="background:#f8f9fa;">'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">品名</th>'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">规格/产地</th>'
      '<th style="text-align:right;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">报价(元/吨)</th>'
      '<th style="text-align:right;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">变化</th>'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">贸易商角色 / 占比</th>'
      '</tr>')
    for cat, spec, price, chg, role in CONTEXT["silicon_spot_rows"]:
        # 价格/亏损/正反馈着色
        if "亏损" in chg or "-1" in chg:
            chg_col = "#d63031"; chg_w = "700"
        elif "+" in chg:
            chg_col = "#d63031"; chg_w = "700"
        elif "持稳" in chg:
            chg_col = "#57606f"; chg_w = "400"
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
      '① 期货 SI 2611/PS 2611 报价 <b>通氧 553#</b>(9,100-9,500 元)与 <b>N 致密料</b>(39,500-40,500 元)只是<b>交割基准品</b>, 流通量不足现货总量 10%<br>'
      '② 实际主流走量是 <b>不通氧 553#</b>(~15 万吨/月) + <b>441#</b>(~5 万吨/月) + <b>99/97 硅等非标品</b>(~12 万吨/月), 后者基本不进入交割体系<br>'
      '③ <b style="color:#d63031;">市场分割:</b> 非标品现货市场(99硅/97硅/551#等)玩家是 <b>中小贸易商/磨粉厂/铝合金厂</b>, <b>基本不做期现套利</b>——价格随行就市, 与期货盘不直接联动; '
      '标准品期现市场(553#/421#等可交割品)由 <b>期现商/大型冶炼厂/机构</b>主导, <b>常态化期现套利</b>——这是判断盘面价格是否能传导到现货的两条不同路径<br>'
      '④ 多晶硅现货 9/2 全线持平(N型复投料 40.66 / 致密料 40.10 元/kg), 但<b>全行业毛利润 -3,965 元/吨(-10%)</b>, <b>成交仍稀</b>——挺价没量等于"账面的"; 工业硅现货 97硅逆势 +100 至 8,600(减产挺价, 非标品与盘面脱钩)'
      '</div>'
      '</td></tr>')
    A('<tr><td style="padding:4px 8px 4px 0;color:#8b949e;">库存</td><td style="padding:4px 0;">工业硅 %s; 多晶硅 %s — <b>涨幅最大的品种库存最重</b></td></tr>' % (sf["SI_social_inv"], sf["PS_chain_inv"]))
    A('<tr><td style="padding:4px 8px 4px 0;color:#8b949e;">供给</td><td style="padding:4px 0;">工业硅: %s; 多晶硅: %s</td></tr>' % (sf["SI_open_rate"], sf["PS_open_rate"]))
    A('</table>')
    # 价差时间窗口(8/30 23:11 第四轮反馈③)——把"价差方向"和"时间窗口"结合成可执行交易计划
    A('<div style="background:#eef6ff;border:1px solid #b8d4f0;border-radius:6px;padding:10px 14px;margin-top:12px;font-size:13px;line-height:1.8;">')
    A('<b>价差时间窗口(方向 × 时点 · 可执行 · 口径=近月−远月, 负=远月升水):</b><br>'
      '① <b>工业硅 SI2611-2612 价差 %+d 元</b>: 远月升水 %d 元(新交割标准制度断层), 正常远月仓储资金成本约 80-100 元, 仍有约 <b>250 元收敛空间</b>——收敛需等 9-11 月仓单注销进度; 若老仓单大量流向现货 → 近月压力减轻 → 价差可能<b>提前收敛</b><br>'
      '② <b>多晶硅 PS2611-2612 价差 %+d 元</b>(近月−远月, 负=远月升水): 12 月"反内卷"政策若在行业会议后落地 → 远月升水可能进一步<b>走扩至 4,000 元以上</b>(绝对值更大); 若政策不及预期 → 远月升水迅速<b>收敛至 2,000 元以内</b>。关键观察窗口: <b>9/1-9/5(减产方案提报后一周)</b>' % (si_gap, -si_gap, ps_gap))
    A('</div>')
    # 客户行动建议(8/30 23:11 第五轮反馈)——描述性 → Actionable, 分上游/中游/下游三个角色
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
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;">SI2611 当前 8,650(9/2 收盘 -1.93%)<br>'
      '<span style="color:#57606f;">停炉"利多兑现"已两日(9/1 -0.4% / 9/2 -1.9%), 价格回吐至 8/14 起涨点附近, 距 9,000 关口 350 元</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;line-height:1.7;">'
      '① <b>当前 8,650: 维持低比例卖出套保</b>(如 30% 产量)——减产落地但库存 96.98 万吨高位未解, 反弹是卖保机会不是追多理由<br>'
      '② 若价格反弹至 <b>9,000 以上</b>: <b style="color:#d63031;">加套保比例至 50%+</b>(反内卷预期 + 仓单注销双驱动下, 9,000 上方空间有限)<br>'
      '③ 若价格回落至 <b>8,400 以下</b>: <b style="color:#d63031;">平掉部分空头套保头寸</b>(如从 50% 降至 20%), 同时在现货端<b>做好低价惜售准备</b>——8,400 已贴近多数企业现金流成本线(8,200-8,500), 继续做空的性价比下降; 释放后不是离场, 而是<b>等反弹到 8,500-8,600 再分批重建</b>头寸。⚠ <b>切忌只释放不复建:</b> 若减产传导后价格再度拉升, 后悔的是"既丢了空头、也没在低价惜售现货"。'
      '</td></tr>'
      '<tr>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;">工业硅<br><span style="font-weight:400;font-size:11px;color:#57606f;">中游贸易商</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;">基差 +550(现 9,200 不通氧553# − 期 8,650)<br>'
      '<span style="color:#57606f;">基差率 6.4%; 执行品=不通氧553#(真实销售渠道), 非交割基准通氧553#; 9/2 期货跌 1.93% 而现货未跟跌——非标品与盘面脱钩的典型例证</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;line-height:1.7;">'
      '① <b>"卖现货买期货" 反套策略</b>(基差正向回归): 卖不通氧553# 9,200 / 买 SI2611 8,650, 基差从 9/1 +410 走阔至 +550<br>'
      '② <b>扣除仓储+资金成本(约 310 元)后净利约 240 元/吨</b>(持有至 SI2611 交割前约 60-90 天测算)——仍略低于 250 元机会成本阈值, <b>观望为主</b>; 若基差进一步走阔至 <b>+600 以上</b>(现货 9,200+/期货回落 8,600 以下), 净利升至 ~290 元, 可小仓位(30% 库存)进场; ⚠ 若现货端实际成交低于 9,000 或持有期拉长, 净利可能归零甚至倒挂, 价差提前收敛(老仓单注销超预期)则见好就收, 别死守合约到期。<br>'
      '③ <b style="color:#d63031;">关键约束:</b> 卖现货端必须有<b>真实销售渠道</b>(不通氧 553# 或 441#), <b>不能依赖交割库一刀切</b>——这正是非标品市场分割的核心'
      '</td></tr>'
      '<tr>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;font-weight:700;color:#1a3a5c;">多晶硅<br><span style="font-weight:400;font-size:11px;color:#57606f;">下游拉晶厂</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;">PS2611 当前 36,900(9/2 收盘 -1.85%)<br>'
      '<span style="color:#57606f;">9/1 +3.22% 反弹后回吐, 已进入 36,000-37,000 分批建仓区; 现货成交仍稀</span></td>'
      '<td style="padding:6px 8px;border:1px solid #a5d6a7;line-height:1.7;">'
      '① <b>当前 36,900: 已回踩进入建仓区间, 启动分批买入套保(30%-50% 远期原料需求)</b>——前日反弹主因减产预期 + 仓单微增, 现货成交清淡、9 月排产仍环比 +9.5%, 回踩给的是成本锁定机会<br>'
      '② <b>场景拆解(方向相反, 动作不同):</b><br>'
      '&nbsp;&nbsp;• <b>若价格回落至 35,000 以下(政策底被击穿, 超跌窗口)</b>: <b style="color:#d63031;">套保比例加至 70%+</b>——这是 3-6 个月内的"安全垫价位", 单 kg 原料成本节省 5 元+<br>'
      '&nbsp;&nbsp;• <b>若反内卷政策超预期落地、价格突破 40,000</b>: <b style="color:#d63031;">不建议追涨加仓</b>, 应等待回踩 37,000-38,000 后再分批建仓——历史规律: 利好兑现后常有获利回吐(9/2 已演示), 追涨被套概率 >60%'
      '</td></tr>'
      '</table>'
      '<div style="font-size:11px;color:#8b949e;margin-top:6px;line-height:1.6;">'
      '<b>使用提示:</b> 三类客户的动作方向不同——上游卖、中游反套、下游买, 这是市场结构决定的, 不是建议; 客户问"为什么"时, 可用上方的"弱现实拆解"作为说服依据, 用"价差时间窗口"作为时点依据。'
      '</div>')
    A('</div>')
    A('<div style="background:#fff8e6;border:1px solid #ffe0a3;border-radius:6px;padding:10px 14px;margin-top:12px;font-size:13px;line-height:1.8;">')
    A('<b>四大验证信号(按优先级, PS 价差口径=近月−远月, 负号只在数据表出现, 触发器一律用绝对值表述):</b><br>'
      '① <b>PS2611−PS2612 价差(当前 %s 元, 远月升水, 三档边界值跟踪):</b><br>'
      '&nbsp;&nbsp;• <b>远月升水收窄至 3,000 元以内</b>: 政策预期开始兑现, 近月估值修复<br>'
      '&nbsp;&nbsp;• <b>远月升水走扩至 4,000 元以上</b>: 政策预期进一步强化 或 近月仓单压力加剧<br>'
      '&nbsp;&nbsp;• <b>远月升水突破 4,500 元</b>: 警惕政策预期泡沫, 近月可能出现超跌反弹机会<br>'
      '总框架: 收敛→政策兑现; 走扩→预期发酵/弱现实加码。给客户一个<b>可量化的交易触发器</b>, 不再凭感觉。<br>'
      '② <b>工业硅仓单注销进度(9-11月)</b>: 老仓单流向现货压近月 vs 12月后可交割品骤减推远月<br>'
      '③ <b>多晶硅现货成交恢复</b>: 从零成交恢复成交, 牌价才变成真价格; 在此之前涨幅都是账面的<br>'
      '④ <b>持仓量的方向性变化(交易层面)</b>: PS2611 若在下跌过程中持仓持续减少(获利盘出清)→短期底部临近; 若持仓继续增加但价格横盘→多空分歧加大, 需等待方向选择' % format(int(ps11[0] - ps12[0]), ","))
    A('<div style="background:#fff3f3;border:1px solid #f5c6c6;border-radius:6px;padding:8px 12px;margin-top:8px;font-size:12px;line-height:1.7;color:#7a4a4a;">'
      '<b>📌 9/2 实测(信号④上线后第 3 个交易日):</b><br>'
      '• PS2611 <b>冲高回落收 36,900(-1.85%)</b>——9/1 +3.22% 反弹后回吐, "利好兑现获利回吐"现场演示; 期现商成交相对活跃但下游刚需补库为主, 9 月排产 12.45 万吨仍高、反弹持续性待验<br>'
      '• PS2611-2612 价差 -3,865(从 -3,705 走扩 160 元)——前一日收敛后再度走扩, 主因近月回吐快于远月; 仍在 -3,000~-4,000 观察区内, 未触发 -4,500 超跌信号<br>'
      '• SI2611 <b>收 8,650(-1.93%)</b>——东疆停炉 32 台(8/31 落地)后第二日"利多兑现", 减产预期消化近两周、高位卖压显现; 现货 97硅逆势 +100 至 8,600(非标品不跟跌, 市场分割又一例证)</div>')
    A('</div>')
    A('</div>')

    # 7 碳酸锂主战场 (8/30 23:51 Frank 临时新增)
    lf = CONTEXT["lithium_fundamental"]
    lc_main = lf["LC2701"]; lc_far = lf["LC2705"]; lc_0909 = lf["LC2609"]
    lc_gap = lc_main[0] - lc_far[0]  # LC2701-LC2705 价差(8/27 估算 last 差)

    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #e17055;padding-left:10px;margin-bottom:12px;">七 · 主战场: 碳酸锂(电池级/工业级) — 强现实28°C × 弱预期22°C, 连续两日回调后的"现货验证"窗口</div>')
    # 合约全景
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">合约</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">最新</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">昨结</th><th style="text-align:right;padding:6px 8px;border:1px solid #e1e4e8;">持仓(手)</th><th style="text-align:left;padding:6px 8px;border:1px solid #e1e4e8;">角色</th></tr>')
    for c, last, settle, oiv, note in [
        ("LC2609", lc_0909[0], lc_0909[1], lc_0909[2], "临交割·持仓外溢到 2701"),
        ("LC2701", lc_main[0], lc_main[1], lc_main[2], "主力·反枧下窝+排产强势"),
        ("LC2705", lc_far[0], lc_far[1], lc_far[2], "新主力切换承接·淡季预期受压"),
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
    # 弱现实拆解(LC2701 一支)
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:12px;color:#57606f;margin-top:10px;border-collapse:collapse;">')
    A('<tr><td style="padding:4px 8px 4px 0;width:88px;vertical-align:top;color:#8b949e;line-height:1.9;">强现实 vs 弱预期</td>'
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
    # 现货价表
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:12px;color:#57606f;margin-top:10px;border-collapse:collapse;">')
    A('<tr><td style="padding:4px 8px 4px 0;width:88px;vertical-align:top;color:#8b949e;line-height:1.9;">现货锚</td>'
      '<td style="padding:4px 0;line-height:1.5;">'
      '<table width="100%" cellpadding="3" cellspacing="0" style="font-size:12px;border-collapse:collapse;">'
      '<tr style="background:#f8f9fa;">'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">品名</th>'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">规格/产地</th>'
      '<th style="text-align:right;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">报价</th>'
      '<th style="text-align:right;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">变化</th>'
      '<th style="text-align:left;padding:4px 6px;border:1px solid #e1e4e8;font-weight:600;color:#1a3a5c;">角色 / 占比</th>'
      '</tr>')
    for cat, spec, price, chg, role in CONTEXT["lithium_spot_rows"]:
        if "亏损" in chg or "-1" in chg:
            chg_col = "#d63031"; chg_w = "700"
        elif "+" in chg:
            chg_col = "#d63031"; chg_w = "700"
        elif "-" in chg:
            chg_col = "#00875a"; chg_w = "700"
        elif "持稳" in chg:
            chg_col = "#57606f"; chg_w = "400"
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
      '④ 9 月锂电排产 <b>~332 GWh</b>(+9.2%), 铁锂环比 <b>+6%</b>(61.2万吨)、三元 -5% — 旺季需求托底但排产上修存疑(9/2 电池大厂下修 5% 传闻); 澳矿复产到港 + 江西枧下窝 9 月中前批复窗口 + 仓单 45,389 吨高位, 远期宽松压制<br>'
      '⑤ 锂盐厂利润 <b>+0.7 万/吨</b>(转盈收窄, 售价 15.65 vs 完本 14.9), 一线(赣锋/天齐)稳定盈利, 二三线转盈; <b>"舒适区"是 14-15 万</b> — 跌破 14 万才会大面积减产'
      '</div>'
      '</td></tr>')
    A('<tr><td style="padding:4px 8px 4px 0;color:#8b949e;">库存</td><td style="padding:4px 0;">SMM %s ; GFEX 仓单 %s — <b>连续 17 周去库创年内新低, 但仓单高位流入</b></td></tr>' % (lf["SMM_total_inv"], lf["GFEX_warrant"]))
    A('<tr><td style="padding:4px 8px 4px 0;color:#8b949e;">供给</td><td style="padding:4px 0;">周产 %s ; 锂精矿 %s</td></tr>' % (lf["weekly_output"], lf["SMM_spodumene_6pct"]))
    A('<tr><td style="padding:4px 8px 4px 0;color:#8b949e;">需求</td><td style="padding:4px 0;">%s ; 铁锂/三元: %s</td></tr>' % (lf["demand_aug"], lf["demand_lfp"]))
    A('<tr><td style="padding:4px 8px 4px 0;color:#8b949e;">基差</td><td style="padding:4px 0;">%s</td></tr>' % lf["spread_basis"])
    A('</table>')
    # 价差时间窗口
    A('<div style="background:#eef6ff;border:1px solid #b8d4f0;border-radius:6px;padding:10px 14px;margin-top:12px;font-size:13px;line-height:1.8;">')
    A('<b>价差时间窗口(方向 × 时点 · 可执行):</b><br>'
      '① <b>LC2701-LC2705 价差 +%d 元</b>: 从 +2,380(8/27) → +3,660(9/1) → <b>+3,940(9/2)</b> 连续走扩, 逼近 <b>+4,000 加码阈值</b>——"走扩至 +3,500+ 是大概率方向"已兑现, 下一步看站稳 +4,000 可加码买近卖远; 若价差反向收敛至 +1,500 以内, 警惕枧下窝提前批复或澳矿放量<br>'
      '② <b>基差 +1,720 元(基差率 1.1%%</b>, 现 15.65万 − 期 15.48万): 期货贴水由 +640 加深至 +1,720(9/2 期货跌幅大于现货)——<b>正套(买现卖期)窗口继续关闭</b>(无锁定空间), 反套(卖现买期)幅度仍不足(1.1%% 低于持有成本), 暂不可做(仓单高位+远期宽松)<br>'
      '③ <b>枧下窝时间窗</b>: 8/26 宜春生态局撤销原报告 → 复产流程远慢于预期(未来 4 个月供应有限), 9 月中正式批复窗口仍是<b>强现实 vs 弱预期的最大扳机</b>; 9/5-9/10 观察为宜<br>'
      '④ <b>新供给扰动</b>: 雅保智利罢工 <b>9/2 已启动</b>(投票 97.49%% 支持) — 若扩大至港口物流则南美供给实质收紧; 叠加 9/3-4 世界动力电池大会(宜宾)需求侧验证窗口' % lc_gap)
    A('</div>')
    # Actionable 绿盒
    A('<div style="background:#e8f7ec;border:1px solid #a5d6a7;border-radius:6px;padding:10px 14px;margin-top:12px;font-size:13px;line-height:1.85;">')
    A('<b>Actionable · 碳酸锂分角色客户行动建议:</b><br>')
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
      '<b>使用提示:</b> 上游卖套保(16 万上方锁定旺季利润)、中游观望(基差转正但幅度不足: 正套窗口已随期货升水出清而关闭, 反套需基差走阔至 +1,000 以上再评估)、下游等回踩 15.5-16 万分批买保 — 与硅链方向结构<b>方向相同、幅度差一个数量级</b>: 硅链中游基差 +410(基差率 <b>4.7%</b>, 但扣除持有成本后净利仅 ~100 元/吨, 套利性价比已大幅下降); 锂链基差 +640(基差率仅 <b>0.4%</b>)——<b>跨品种比基差必须用基差率, 绝对值不可直接比</b>。两链反套窗口目前均未真正打开。<b>口径固化: 正套=买现货卖期货(买现卖期), 反套=卖现货买期货(卖现买期)</b>。客户问"为什么"时, 可用"强现实 vs 弱预期拆解"作为说服依据, 用"枧下窝时间窗"作为时点依据。'
      '</div>')
    A('</div>')
    # 验证信号黄盒(LC 价差边界值)
    cur_diff = CONTEXT["lithium_signals"]["LC2701-LC2705"]
    A('<div style="background:#fff8e6;border:1px solid #ffe0a3;border-radius:6px;padding:10px 14px;margin-top:12px;font-size:13px;line-height:1.8;">')
    A('<b>验证信号 · LC 价差边界值触发器(按优先级):</b><br>'
      '① <b>LC2701-LC2705 价差(当前 +%d 元, 四档跟踪口径):</b><br>' % cur_diff)
    for tier, meaning in CONTEXT["lithium_signals"]["tiers"]:
        A('&nbsp;&nbsp;• <b>%s</b>: %s<br>' % (tier, meaning))
    A('总框架: <b>近月强势(月差 +3,940 逼近 +4,000 加码线) → 强现实占优</b>; 月差收敛至 +2,000 以下 + 基差再度走弱 → 弱预期占优, 趋势转空。基差由期货升水 2,500 → 现货升水 640 → 1,720 = <b>期货溢价持续出清</b>, 行情从"抢跑定价"进入"现货验证"阶段。给客户一个<b>可量化的交易触发器</b>, 不再凭感觉。<br>'
      '② <b>枧下窝复产节奏(9 月中窗口)</b>: 批复延迟 → 近月继续走强; 提前批复 → 近月快速回吐 10%+<br>'
      '③ <b>SMM 周度库存去化斜率</b>: 连续 17 周去化约 -7,590 吨/周, 若去化收窄至 -3,000 吨/周以内 → 转弱信号<br>'
      '④ <b>GFEX 仓单日均增量</b>: 9/2 仓单 45,389 吨(-450, 高位小幅回落); 若再度跳增至 +3,000 吨/日 → 隐形库存显性化, 近月见顶')
    A('<div style="background:#fff3cd;border:1px solid #ffe0a3;border-radius:6px;padding:8px 12px;margin-top:8px;font-size:12px;line-height:1.7;">'
      '<b>📌 9/2 实测(信号①上线后第 3 个交易日):</b><br>'
      '&nbsp;&nbsp;• LC2701-LC2705 价差 <b>+3,940</b>(从 9/1 +3,660 走扩 280 元)——连续两日走扩逼近 +4,000 加码线, "强现实近月占优"延续; 未触发 +4,500 止盈<br>'
      '&nbsp;&nbsp;• LC2701 <b>收 154,780(-3.2%昨结口径 / -1.95%收盘口径)</b>(盘中低 153,200): 减仓 9,123 手至 395,794——价跌+减仓 = 多头获利离场而非空头打压, 两日从 16.29 万回吐 8,080 元后进入 15.2-16.2 万参考区间<br>'
      '&nbsp;&nbsp;• 基差走扩至 <b>+1,720</b>(电碳 15.65万 − 期 15.48万): 期货贴水加深、现货抗跌(15.5 万下方下游逢低采购回升)——期货溢价出清进入第二日; 9/2 电池大厂排产下修 5% 传闻打击情绪, 若现货端不能走出实质短缺, 反弹高度有限</div>')
    A('</div>')
    A('</div>')

    # 8 日历(原七改为八)
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #0984e3;padding-left:10px;margin-bottom:12px;">八 · 事件日历(雷区地图) — 通用 + 硅链 + 锂链(已去重)</div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;"><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">时间</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">事件</th><th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">影响</th></tr>')
    _seen_cal = set()
    for t, ev, note, sym in CONTEXT["calendar"] + CONTEXT["lithium_events"]:
        _k = ev[:8]  # 按事件名去重(防通用/专属日历再叠重复条目)
        if _k in _seen_cal:
            continue
        _seen_cal.add(_k)
        hot = "今日" in t or "8/31" in t or "9月上旬" in t or "8/30" in t or "9月中" in t
        A('<tr%s><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;%s">%s</td>'
          '<td style="padding:5px 8px;border:1px solid #e1e4e8;%s">%s</td>'
          '<td style="padding:5px 8px;border:1px solid #e1e4e8;color:#8b949e;">%s</td></tr>' % (
              ' bgcolor="#fff4f4"' if hot else "", "color:#d63031;" if hot else "", t,
              "font-weight:700;" if hot else "", ev, sym + " · " + note if note else sym))
    A('</table>')
    A('</div>')

    # 9 追保压力测算 (2026-09-02 Frank 第九项要求——三类客户唯一会真出事的地方)
    A('<div style="background:#fff;border:1px solid #e1e4e8;border-radius:0;margin-top:12px;padding:18px 24px;">')
    A('<div style="font-size:16px;font-weight:700;color:#1a3a5c;border-left:4px solid #d63031;padding-left:10px;margin-bottom:12px;">九 · 追保压力测算(卖保客户的风险敞口) — 三类客户里唯一会真出事的地方</div>')
    A('<div style="font-size:12px;color:#57606f;margin-bottom:8px;line-height:1.7;">'
      '<b>假设:</b> ①上游硅企月产1万吨, 按建议在 SI2611 8,650 卖保30% = 3,000吨 = 600手(5吨/手), 保证金率10%, 初始保证金259.5万; '
      '②锂盐厂月产3,000吨, 按建议在 LC2701 154,780 卖保50% = 1,500吨 = 1,500手(1吨/手), 保证金率12%, 初始保证金2,786.0万; '
      '③维持保证金=初始80%; 追保=浮亏−20%×初始(浮亏超20%保证金时触发); 授信额度=2×初始保证金。'
      '<b>逆向方向=价格继续上涨(卖保空头被套)。</b></div>')
    A('<table width="100%" cellpadding="0" cellspacing="0" style="font-size:12px;border-collapse:collapse;">')
    A('<tr style="background:#f6f8fa;">'
      '<th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">客户</th>'
      '<th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">卖保头寸</th>'
      '<th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">价格逆向 +5%</th>'
      '<th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">价格逆向 +10%</th>'
      '<th style="text-align:left;padding:5px 8px;border:1px solid #e1e4e8;">价格逆向 +15%</th></tr>')
    A('<tr><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;">工业硅<br><span style="font-weight:400;font-size:11px;color:#57606f;">上游冶炼厂</span></td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;">SI2611 600手<br><span style="color:#57606f;">初始保证金 259.5万</span></td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;">浮亏 <b>129.8万</b><br>追保 <b>77.9万</b><br>授信占用 65%</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;">浮亏 <b>259.5万</b><br>追保 <b>207.6万</b><br>授信占用 90%</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;">浮亏 <b>389.3万</b><br>追保 <b>337.4万</b><br><b style="color:#d63031;">授信占用 115% 超限 → 强平风险</b></td></tr>')
    A('<tr><td style="padding:5px 8px;border:1px solid #e1e4e8;font-weight:600;">碳酸锂<br><span style="font-weight:400;font-size:11px;color:#57606f;">上游锂盐厂</span></td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;">LC2701 1,500手<br><span style="color:#57606f;">初始保证金 2,786.0万</span></td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;">浮亏 <b>1,160.9万</b><br>追保 <b>603.6万</b><br>授信占用 61%</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;">浮亏 <b>2,321.7万</b><br>追保 <b>1,764.5万</b><br>授信占用 82%</td>'
      '<td style="padding:5px 8px;border:1px solid #e1e4e8;">浮亏 <b>3,482.6万</b><br>追保 <b>2,925.3万</b><br><b style="color:#d63031;">授信占用 103% 超限 → 强平风险</b></td></tr>')
    A('</table>')
    A('<div style="font-size:12px;color:#8b949e;margin-top:8px;line-height:1.7;">'
      '<b>关键结论:</b> ①价格逆向 <b>+10%</b> 即吃掉初始保证金并追加一倍(硅企 207.6万 / 锂盐厂 1,764.5万)——<b>卖保前必须先预留 10% 价格波动的追保资金</b>, 否则被动平仓把套保做成投机; '
      '②授信超限(115%/103%)出现在 <b>+15%</b> 逆向(SI 9,950+ / LC 17.8万+), 对应反内卷大幅超预期或锂价逼仓——概率低但一旦发生无缓冲, 期货公司会直接减仓; '
      '③<b>追保金额与保比例线性相关</b>: 硅企只卖15%(300手)对应追保减半(+5%时 77.9万→38.9万), 锂盐厂卖30%(900手)追保降至+5%时约 362万——<b>仓位越重, 追保弹性越小, 授信余量越薄</b>。</div>')
    A('</div>')

    # 尾注
    A('<div style="background:#f6f8fa;border:1px solid #e1e4e8;border-radius:0 0 10px 10px;margin-top:12px;padding:14px 24px;font-size:12px;color:#8b949e;line-height:1.7;">')
    A('<b>数据与框架说明</b><br>'
      '行情: 新浪期货(昨收盘+夜盘), 结算价口径计算展期收益 · 宏观: 国家统计局/央行 · 库存: 交易所周报/百川/隆众 · 硅链现货: 百川盈孚<br>'
      '框架: 八段结构(六板块温度计→宏观→板块轮动→期限结构→持仓资金→硅链→碳酸锂→事件日历) + 追保压力测算, 核心逻辑=获得背景而非预测涨跌。<br>'
      '本报告仅为个人研究参考, 不构成投资建议。')
    A('</div>')
    A('</div></body></html>')

    html = "\n".join(H)
    out = os.path.join(BASE, "outputs", "commodity_morning_%s_%s_%s.html" % (y, m, dd))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("saved ->", out, "(%.1f KB)" % (len(html.encode("utf-8")) / 1024))
    # 快速校验
    assert "晨报" in html and "期限结构" in html and "硅链" in html
    print("sections:", html.count("▎") + html.count("· "), "| tables:", html.count("<table"))

if __name__ == "__main__":
    main()
