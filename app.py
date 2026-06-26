import matplotlib
matplotlib.use("Agg")

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap

# 强制刷新字体缓存，加载系统安装的文泉驿中文字体
fm._load_fontmanager(try_read_cache=False)

def get_chinese_font():
    candidate_fonts = [
        "WenQuanYi Zen Hei",
        "WenQuanYi Micro Hei",
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "DejaVu Sans"
    ]
    installed = {f.name for f in fm.fontManager.ttflist}
    for font in candidate_fonts:
        if font in installed:
            return font
    return "sans-serif"

FONT = get_chinese_font()
plt.rcParams.update({
    "font.sans-serif": [FONT],
    "font.family": "sans-serif",
    "axes.unicode_minus": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white"
})

# ====================== 全局配置 ======================
st.set_page_config(page_title="中国AI产业发展态势可视化平台", layout="wide")

# 配色
CFG = {
    "BLUE": "#2C5F8A",
    "RED": "#E74C3C",
    "TEAL": "#1ABC9C",
    "GRAY": "#95A5A6",
    "GOLD": "#F39C12",
    "GRID": "#E5E7EB"
}

# ====================== 数据字典 ======================
DATA = {
    "years_size": np.arange(2019, 2026),
    "size": np.array([710, 3031, 4041, 5080, 5784, 6964, 10457]),
    "growth": np.array([38.7, 327.0, 33.3, 25.7, 13.9, 20.4, 50.2]),
    "years_ent": np.arange(2018, 2026),
    "enterprises": np.array([1011, 1200, 1454, 1800, 2200, 3000, 4500, 5300]),
    "tech_pct": [37.5, 25.2, 15.8, 12.6, 8.9],
    "tech_labels": ["计算机视觉", "NLP与语音", "AI芯片", "机器学习平台", "智能机器人"],
    "city_labels": ["北京", "上海", "深圳", "杭州", "广州", "成都", "南京", "武汉"],
    "city_pct": np.array([28.1, 14.2, 13.4, 7.7, 5.2, 4.8, 3.9, 3.5]),
    "region_circle_labels": ["京津冀", "长三角", "珠三角", "成渝", "其他地区"],
    "region_circle_pct": [29.4, 31.0, 26.5, 7.2, 5.9],
    "region_names": ["长三角", "珠三角", "京津冀", "成渝", "中部", "西北", "东北"],
    "region_metrics": ["企业规模", "投融资", "人才储备", "专利产出", "政策支持"],
    "region_matrix": np.array([
        [92, 90, 95, 88, 93],
        [90, 86, 88, 85, 91],
        [85, 88, 92, 82, 90],
        [76, 72, 74, 68, 78],
        [69, 65, 67, 62, 72],
        [54, 48, 51, 45, 58],
        [50, 43, 46, 40, 52]
    ]),
    "years_patent": np.arange(2018, 2025),
    "patent_count": np.array([3000, 6000, 10900, 15600, 16800, 18400, 22400]),
    "years_invest": np.arange(2015, 2025),
    "invest_amount": np.array([391, 560, 2105, 1000, 1000, 1500, 2252, 1500, 1200, 1052]),
    "years_history": np.arange(2019, 2026),
    "years_forecast": np.arange(2025, 2031),
    "forecast_conservative": np.array([10457, 11500, 12800, 14200, 15800, 17500]),
    "forecast_neutral": np.array([10457, 12200, 14500, 17200, 20500, 24000]),
    "forecast_optimistic": np.array([10457, 13200, 16800, 21500, 27000, 33500]),
    "years_tech_trend": np.arange(2019, 2025),
    "trend_cv": np.array([820, 1100, 1450, 1720, 1980, 2200]),
    "trend_nlp": np.array([320, 450, 680, 950, 1280, 1520]),
    "trend_chip": np.array([280, 380, 520, 780, 960, 1150]),
    "trend_ml": np.array([220, 310, 420, 550, 680, 800]),
    "trend_robot": np.array([150, 210, 290, 370, 440, 500])
}

def setup_ax(ax, ylabel=""):
    ax.set_xlabel("年份", fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(axis="y", color=CFG["GRID"], alpha=0.6, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# ====================== 侧边栏导航 ======================
with st.sidebar:
    st.title("📊 导航菜单")
    page = st.radio("选择分析模块", [
        "🏠 首页概览",
        "📈 市场规模分析",
        "🏢 企业竞争格局",
        "🗺️ 区域分布分析",
        "💡 专利与技术趋势",
        "💰 投融资分析",
        "🔮 发展趋势预测"
    ])

# ====================== 页面1：首页概览 ======================
if page == "🏠 首页概览":
    st.title("中国人工智能产业发展态势可视化分析平台")
    st.markdown("基于多源公开数据 | 覆盖市场、企业、区域、技术、资本、预测六大维度")
    
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("2025核心产业规模", "10457 亿元", "+50.2%")
    with col2:
        st.metric("核心企业数量", "5300 家", "年均增长25%")
    with col3:
        st.metric("专利全球占比", "38.58%", "全球第一")
    with col4:
        st.metric("三大经济圈集聚度", "86.9%", "区域高度集中")

    st.divider()
    st.subheader("核心结论速览")
    st.markdown("""
    1. **产业规模**：2019-2025年从710亿元增长至10457亿元，进入「AI+」战略加速期
    2. **竞争格局**：计算机视觉与NLP双轮驱动，AI芯片赛道国产替代加速
    3. **区域分布**：京津冀、长三角、珠三角三大经济圈集聚全国近87%的骨干企业
    4. **技术创新**：专利申请量全球第一，但海外申请率仅7.3%，量质矛盾突出
    5. **资本周期**：投融资呈现「双峰」周期，当前处于理性回归阶段
    6. **趋势预测**：中性情景下2030年核心产业规模预计达24000亿元
    """)

# ====================== 页面2：市场规模分析 ======================
elif page == "📈 市场规模分析":
    st.header("一、AI产业市场规模分析")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("产业规模与增长率双轴图")
        y, s, g = DATA["years_size"], DATA["size"], DATA["growth"]
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax2 = ax1.twinx()
        ax1.bar(y, s, width=0.52, color=CFG["BLUE"], edgecolor="white", zorder=3)
        ax2.plot(y, g, color=CFG["RED"], lw=2.5, marker="o", ms=7,
                 mfc="white", mec=CFG["RED"], mew=2, zorder=5)
        ax1.set_ylim(0, 13500)
        ax2.set_ylim(0, 420)
        ax1.set_ylabel("规模(亿元)", color=CFG["BLUE"])
        ax2.set_ylabel("增长率(%)", color=CFG["RED"])
        setup_ax(ax1)
        ax2.spines["top"].set_visible(False)
        st.pyplot(fig1, use_container_width=True)

    with col2:
        st.subheader("同比增长率柱状图")
        y_g = DATA["years_size"][1:]
        g_val = DATA["growth"][1:]
        fig2, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(y_g, g_val, width=0.55, color=CFG["BLUE"], edgecolor="white", zorder=3)
        bars[0].set_color(CFG["RED"])
        for bar, val in zip(bars, g_val):
            ax.text(bar.get_x()+bar.get_width()/2, val+5, f"{val}%", ha="center", fontsize=9)
        ax.set_ylim(0, 380)
        setup_ax(ax, ylabel="同比增长率(%)")
        st.pyplot(fig2, use_container_width=True)

    st.info("💡 分析要点：2020年327%的高增速包含口径扩展效应；2025年增速反弹受大模型与「AI+」政策双重驱动。")

# ====================== 页面3：企业竞争格局 ======================
elif page == "🏢 企业竞争格局":
    st.header("二、AI企业竞争格局分析")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("核心企业数量增长趋势")
        y, ent = DATA["years_ent"], DATA["enterprises"]
        fig3, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(y, ent, color=CFG["TEAL"], alpha=0.25, zorder=2)
        ax.plot(y, ent, color=CFG["TEAL"], lw=2.5, marker="o", ms=7,
                mfc="white", mec=CFG["TEAL"], mew=2, zorder=3)
        ax.set_ylim(0, 6000)
        setup_ax(ax, ylabel="核心企业数量(家)")
        st.pyplot(fig3, use_container_width=True)

    with col2:
        st.subheader("技术领域市场结构")
        fig4, ax = plt.subplots(figsize=(10, 6))
        colors = [CFG["BLUE"], CFG["TEAL"], CFG["GOLD"], "#3498DB", "#E67E22"]
        wedges, _ = ax.pie(DATA["tech_pct"], startangle=90, colors=colors,
                           wedgeprops={"width":0.4, "edgecolor":"white", "linewidth":2})
        lgnd = [f"{l}  {v:.1f}%" for l,v in zip(DATA["tech_labels"], DATA["tech_pct"])]
        ax.legend(wedges, lgnd, loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)
        st.pyplot(fig4, use_container_width=True)

    st.divider()
    st.subheader("细分赛道发展趋势对比")
    fig11, ax = plt.subplots(figsize=(12, 6))
    y = DATA["years_tech_trend"]
    lines = [
        ("计算机视觉", DATA["trend_cv"], CFG["BLUE"], 3),
        ("NLP与语音", DATA["trend_nlp"], CFG["RED"], 3),
        ("AI芯片", DATA["trend_chip"], CFG["GOLD"], 2.5),
        ("机器学习平台", DATA["trend_ml"], "#9B59B6", 2),
        ("智能机器人", DATA["trend_robot"], CFG["TEAL"], 2)
    ]
    for name, data, color, lw in lines:
        ax.plot(y, data, color=color, lw=lw, marker="o", ms=6,
                mfc="white", mec=color, mew=1.5, label=name)
    ax.legend(frameon=False, loc="upper left")
    ax.set_ylim(0, 2500)
    setup_ax(ax, ylabel="市场规模(亿元)")
    st.pyplot(fig11, use_container_width=True)

    st.info("💡 分析要点：产业正从「视觉一家独大」向「视觉+语言双轮驱动」演进，AI芯片赛道增长强劲。")

# ====================== 页面4：区域分布分析 ======================
elif page == "🗺️ 区域分布分析":
    st.header("三、AI产业区域分布分析")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("骨干企业城市分布")
        labels = DATA["city_labels"][::-1]
        values = DATA["city_pct"][::-1]
        colors = ["#9CBDE0","#7BAAD6","#5D97CA","#4A85BC","#3A72A6","#2C5F8A","#2C5F8A","#2C5F8A"]
        fig5, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(labels, values, color=colors, edgecolor="white", height=0.65, zorder=3)
        for bar, val in zip(bars, values):
            ax.text(val+0.3, bar.get_y()+bar.get_height()/2, f"{val}%", va="center", fontsize=9)
        ax.set_xlim(0, 35)
        ax.set_xlabel("占全国骨干企业比例(%)")
        ax.grid(axis="x", color=CFG["GRID"], alpha=0.6, zorder=0)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        st.pyplot(fig5, use_container_width=True)

    with col2:
        st.subheader("三大经济圈占比")
        fig6, ax = plt.subplots(figsize=(10, 6))
        colors = [CFG["BLUE"], CFG["TEAL"], CFG["GOLD"], CFG["RED"], CFG["GRAY"]]
        wedges, _ = ax.pie(DATA["region_circle_pct"], startangle=90, colors=colors,
                           wedgeprops={"width":0.4, "edgecolor":"white", "linewidth":2})
        lgnd = [f"{l}  {v:.1f}%" for l,v in zip(DATA["region_circle_labels"], DATA["region_circle_pct"])]
        ax.legend(wedges, lgnd, loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)
        st.pyplot(fig6, use_container_width=True)

    st.divider()
    st.subheader("区域AI综合指数热力图")
    fig7, ax = plt.subplots(figsize=(12, 6))
    cmap = LinearSegmentedColormap.from_list("b",["#EDF3F8","#8FB1CA",CFG["BLUE"]])
    data = DATA["region_matrix"]
    ax.imshow(data, cmap=cmap, vmin=0, vmax=100, aspect="auto")
    ax.set_xticks(range(5))
    ax.set_xticklabels(DATA["region_metrics"])
    ax.set_yticks(range(7))
    ax.set_yticklabels(DATA["region_names"])
    for i in range(7):
        for j in range(5):
            ax.text(j,i,str(data[i,j]),ha="center",va="center",
                    fontweight="bold",fontsize=9,
                    color="white" if data[i,j]>=78 else "#2A2A2A")
    [s.set_visible(False) for s in ax.spines.values()]
    st.pyplot(fig7, use_container_width=True)

    st.info("💡 分析要点：三大经济圈合计集聚86.9%企业，领先区域形成「人才-资本-专利-产业-政策」正向循环。")

# ====================== 页面5：专利与技术趋势 ======================
elif page == "💡 专利与技术趋势":
    st.header("四、AI专利与技术趋势分析")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("AI专利申请量趋势")
        y, p = DATA["years_patent"], DATA["patent_count"]
        fig8, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(y, p, color=CFG["TEAL"], alpha=0.25, zorder=2)
        ax.plot(y, p, color=CFG["TEAL"], lw=2.5, marker="o", ms=7,
                mfc="white", mec=CFG["TEAL"], mew=2, zorder=3)
        ax.set_ylim(0, 26000)
        setup_ax(ax, ylabel="专利申请量(件)")
        st.pyplot(fig8, use_container_width=True)

    with col2:
        st.subheader("专利质量核心指标")
        st.metric("全球占比", "38.58%", "全球第一")
        st.metric("海外申请率", "7.3%", "远低于日本70%+")
        st.metric("专利授权率", "约32%", "质量提升空间大")
        st.markdown("""
        **核心问题**：「量大质弱」结构性矛盾突出
        **突破方向**：国际布局、高价值培育、商业化转化
        """)

# ====================== 页面6：投融资分析 ======================
elif page == "💰 投融资分析":
    st.header("五、AI投融资分析")
    
    fig9, ax = plt.subplots(figsize=(12, 6))
    y, inv = DATA["years_invest"], DATA["invest_amount"]
    bar_colors = [CFG["BLUE"] if i in [2,6] else "#6A95C2" for i in range(len(inv))]
    bars = ax.bar(y, inv, width=0.6, color=bar_colors, edgecolor="white", zorder=3)
    
    for bar, val in zip(bars, inv):
        ax.text(bar.get_x()+bar.get_width()/2, val+30, f"{val}亿", ha="center", fontsize=8.5)
    
    ax.annotate("政策驱动高峰\n(2105亿)", xy=(2017, 2105), xytext=(2016.2, 2400),
                fontsize=9, color=CFG["RED"], arrowprops=dict(arrowstyle="->", color=CFG["RED"], lw=1))
    ax.annotate("AI芯片/自动驾驶\n(2252亿)", xy=(2021, 2252), xytext=(2020.2, 2500),
                fontsize=9, color=CFG["RED"], arrowprops=dict(arrowstyle="->", color=CFG["RED"], lw=1))
    
    ax.set_ylim(0, 2700)
    ax.set_yticks([0, 500, 1000, 1500, 2000, 2500])
    setup_ax(ax, ylabel="投融资金额(亿元)")
    st.pyplot(fig9, use_container_width=True)

    st.info("💡 分析要点：两轮高峰均遵循「政策信号→资本涌入→估值泡沫→优胜劣汰→理性回归」的周期规律。")

# ====================== 页面7：趋势预测 ======================
elif page == "🔮 发展趋势预测":
    st.header("六、AI产业发展趋势预测")
    
    fig10, ax = plt.subplots(figsize=(12, 6))
    hy = DATA["years_history"]
    fy = DATA["years_forecast"]
    con = DATA["forecast_conservative"]
    neu = DATA["forecast_neutral"]
    opt = DATA["forecast_optimistic"]
    
    ax.fill_between(fy, con, opt, color=CFG["TEAL"], alpha=0.10)
    ax.plot(fy, con, color=CFG["GRAY"], lw=2, ls="--", label="保守情景")
    ax.plot(fy, neu, color=CFG["TEAL"], lw=3, marker="o", ms=7,
            mfc="white", mec=CFG["TEAL"], mew=2, label="中性情景")
    ax.plot(fy, opt, color=CFG["RED"], lw=2, ls="--", label="积极情景")
    ax.plot(hy, DATA["size"], color=CFG["BLUE"], lw=3, marker="o", ms=7,
            mfc="white", mec=CFG["BLUE"], mew=2, label="历史数据")
    
    ax.axvline(2025, color="#CBD5E1", lw=1.5, ls="--")
    ax.text(2025.1, 35000, "预测起点", fontsize=9, color="#64748B")
    
    for x, v in zip(fy, neu):
        ax.annotate(f"{v}亿", (x, v), textcoords="offset points", xytext=(0,12),
                    ha="center", fontsize=8.5, color=CFG["TEAL"], fontweight="bold")
    
    ax.legend(frameon=False, loc="upper left")
    ax.set_ylim(0, 38000)
    setup_ax(ax, ylabel="产业规模(亿元)")
    st.pyplot(fig10, use_container_width=True)

    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("保守情景")
        st.metric("2030年规模", "约17500亿元", "增速10%-12%")
        st.caption("假设：出口管制加剧，资本退潮，推广放缓")
    with col2:
        st.subheader("中性情景")
        st.metric("2030年规模", "约24000亿元", "增速16%-20%")
        st.caption("假设：技术稳步迭代，「AI+」行动持续推进")
    with col3:
        st.subheader("积极情景")
        st.metric("2030年规模", "约33500亿元", "增速24%-28%")
        st.caption("假设：大模型突破，国产替代加速，海外拓展顺利")
