import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.font_manager as fm
import pandas as pd

# ====================== 全局配置（统一管理，消除硬编码） ======================
CFG = {
    "DPI": 300,
    "BG": "white",
    "GRID": "#E5E7EB",
    "BLUE": "#2C5F8A",      # 主蓝色：规模、核心指标
    "RED": "#E74C3C",       # 珊瑚红：增速、风险
    "TEAL": "#1ABC9C",      # 青绿色：预测、专利
    "GRAY": "#95A5A6",      # 灰色：保守情景、辅助线
    "GOLD": "#F39C12",      # 金色：芯片、重点
    "LIGHT_BLUE": "#3498DB",
    "ORANGE": "#E67E22",
    "PURPLE": "#9B59B6"
}

out = Path("./charts")
out.mkdir(exist_ok=True)

# ====================== 数据字典（集中维护，便于更新） ======================
DATA = {
    # ---------- 图1、图2：市场规模 ----------
    "years_size": np.arange(2019, 2026),
    "size": np.array([710, 3031, 4041, 5080, 5784, 6964, 10457]),  # 宽口径(2020起)
    "growth": np.array([38.7, 327.0, 33.3, 25.7, 13.9, 20.4, 50.2]),
    "years_growth_bar": np.arange(2020, 2026),
    "growth_bar": np.array([327.0, 33.3, 25.7, 13.9, 20.4, 50.2]),

    # ---------- 图3：核心企业数量 ----------
    "years_ent": np.arange(2018, 2026),
    "enterprises": np.array([1011, 1200, 1454, 1800, 2200, 3000, 4500, 5300]),

    # ---------- 图4：技术领域市场结构 ----------
    "tech_pct": [37.5, 25.2, 15.8, 12.6, 8.9],
    "tech_labels": ["计算机视觉", "NLP与语音", "AI芯片", "机器学习平台", "智能机器人"],

    # ---------- 图5：骨干企业城市分布 ----------
    "city_labels": ["北京", "上海", "深圳", "杭州", "广州", "成都", "南京", "武汉"],
    "city_pct": np.array([28.1, 14.2, 13.4, 7.7, 5.2, 4.8, 3.9, 3.5]),

    # ---------- 图6：三大经济圈AI企业占比 ----------
    "region_circle_labels": ["京津冀", "长三角", "珠三角", "成渝", "其他地区"],
    "region_circle_pct": [29.4, 31.0, 26.5, 7.2, 5.9],

    # ---------- 图7：区域综合指数热力图 ----------
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

    # ---------- 图8：专利申请量 ----------
    "years_patent": np.arange(2018, 2025),
    "patent_count": np.array([3000, 6000, 10900, 15600, 16800, 18400, 22400]),

    # ---------- 图9：投融资金额 ----------
    "years_invest": np.arange(2015, 2025),  # 2015-2024 每年一个柱子
    "invest_amount": np.array([391, 560, 2105, 1000, 1000, 1500, 2252, 1500, 1200, 1052]),

    # ---------- 图10：情景预测 ----------
    "years_history": np.arange(2019, 2026),
    "years_forecast": np.arange(2025, 2031),
    "forecast_conservative": np.array([10457, 11500, 12800, 14200, 15800, 17500]),
    "forecast_neutral": np.array([10457, 12200, 14500, 17200, 20500, 24000]),
    "forecast_optimistic": np.array([10457, 13200, 16800, 21500, 27000, 33500]),

    # ---------- 图11：细分赛道趋势 ----------
    "years_tech_trend": np.arange(2019, 2025),
    "trend_cv": np.array([820, 1100, 1450, 1720, 1980, 2200]),       # 计算机视觉
    "trend_nlp": np.array([320, 450, 680, 950, 1280, 1520]),        # NLP与语音
    "trend_chip": np.array([280, 380, 520, 780, 960, 1150]),        # AI芯片
    "trend_ml": np.array([220, 310, 420, 550, 680, 800]),           # 机器学习平台
    "trend_robot": np.array([150, 210, 290, 370, 440, 500])         # 智能机器人
}

# ====================== 字体自适应（跨平台回退机制） ======================
def get_chinese_font():
    for name in ["Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei"]:
        if any(name in f.name for f in fm.fontManager.ttflist):
            return name
    return "sans-serif"  # 最终回退

FONT = get_chinese_font()
plt.rcParams.update({
    "font.sans-serif": [FONT],
    "axes.unicode_minus": False,
    "figure.facecolor": CFG["BG"],
    "axes.facecolor": CFG["BG"]
})

# ====================== 通用函数（消除重复代码） ======================
def setup_ax(ax, ylabel=""):
    ax.set_xlabel("年份", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(axis="y", color=CFG["GRID"], alpha=0.6, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

def save(fig, name):
    try:
        fig.tight_layout()
        fig.savefig(out / f"{name}.png", dpi=CFG["DPI"], bbox_inches="tight")
    except Exception as e:
        print(f"Save {name} failed: {e}")
    finally:
        plt.close(fig)

# ==============================================================================
# ====================== 11张图表绘图函数（对应正文图3-1至3-11） ======================
# ==============================================================================

# ===== 图1: 规模与增长率双轴图（正文图3-1） =====
def fig01():
    y, s, g = DATA["years_size"], DATA["size"], DATA["growth"]
    fig, ax1 = plt.subplots(figsize=(13, 7.5))
    ax2 = ax1.twinx()

    # 柱状图：产业规模
    ax1.bar(y, s, width=0.52, color=CFG["BLUE"], edgecolor="white", zorder=3)
    # 折线图：增长率
    ax2.plot(y, g, color=CFG["RED"], lw=2.8, marker="o", ms=8,
             mfc="white", mec=CFG["RED"], mew=2, zorder=5)

    # 数值标注
    for b, v in zip(ax1.patches, s):
        ax1.text(b.get_x() + b.get_width() / 2, v + 180, str(v),
                 ha="center", fontsize=9, fontweight="bold", color=CFG["BLUE"])

    ax1.set_ylim(0, 13500)
    ax2.set_ylim(0, 420)
    ax1.set_ylabel("产业规模(亿元)", fontsize=12, color=CFG["BLUE"])
    ax2.set_ylabel("同比增长率(%)", fontsize=12, color=CFG["RED"])

    setup_ax(ax1)
    ax2.spines["top"].set_visible(False)
    ax1.set_title("2019—2025年中国AI核心产业规模与增长率", fontsize=14, pad=15)
    save(fig, "fig01_规模双轴图")

# ===== 图2: 同比增长率柱状图（正文图3-2） =====
def fig02():
    y, g = DATA["years_growth_bar"], DATA["growth_bar"]
    fig, ax = plt.subplots(figsize=(11, 7))

    bars = ax.bar(y, g, width=0.55, color=CFG["BLUE"], edgecolor="white", zorder=3)
    # 高亮最高值
    bars[0].set_color(CFG["RED"])

    # 数值标注
    for bar, val in zip(bars, g):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 5, f"{val}%",
                ha="center", fontsize=10, fontweight="bold")

    ax.set_ylim(0, 380)
    setup_ax(ax, ylabel="同比增长率(%)")
    ax.set_title("2020—2025年AI核心产业规模同比增长率", fontsize=14, pad=15)
    save(fig, "fig02_增长率柱状图")

# ===== 图3: 核心企业数量面积图（正文图3-3） =====
def fig03():
    y, ent = DATA["years_ent"], DATA["enterprises"]
    fig, ax = plt.subplots(figsize=(13, 7.5))

    ax.fill_between(y, ent, color=CFG["TEAL"], alpha=0.25, zorder=2)
    ax.plot(y, ent, color=CFG["TEAL"], lw=3, marker="o", ms=8,
            mfc="white", mec=CFG["TEAL"], mew=2, zorder=3)

    # 数值标注
    for x, v in zip(y, ent):
        ax.text(x, v + 150, str(v), ha="center", fontsize=10, fontweight="bold", color=CFG["TEAL"])

    ax.set_ylim(0, 6000)
    setup_ax(ax, ylabel="核心企业数量(家)")
    ax.set_title("2018—2025年中国AI核心企业数量增长趋势", fontsize=14, pad=15)
    save(fig, "fig03_企业数量面积图")

# ===== 图4: 技术领域市场结构环形图（正文图3-4） =====
def fig04():
    fig, ax = plt.subplots(figsize=(11, 9))
    colors = [CFG["BLUE"], CFG["TEAL"], CFG["GOLD"], CFG["LIGHT_BLUE"], CFG["ORANGE"]]

    wedges, _ = ax.pie(DATA["tech_pct"], startangle=90, colors=colors,
                       wedgeprops={"width": 0.4, "edgecolor": "white", "linewidth": 3})

    lgnd_text = [f"{l}  {v:.1f}%" for l, v in zip(DATA["tech_labels"], DATA["tech_pct"])]
    ax.legend(wedges, lgnd_text, loc="center left", bbox_to_anchor=(1, 0.5),
              fontsize=11, frameon=False)

    ax.set_title("AI技术领域市场结构(2024年)", fontsize=14, pad=15)
    save(fig, "fig04_技术结构环形图")

# ===== 图5: 骨干企业城市分布横向条形图（正文图3-5，匹配论文样式） =====
def fig05():
    labels = DATA["city_labels"]
    values = DATA["city_pct"]
    # 倒序排列，让数值最高的城市显示在最上方
    labels_rev = labels[::-1]
    values_rev = values[::-1]

    # 蓝色渐变：北上深最深，后续逐级变浅，匹配论文配色
    colors = [
        "#2C5F8A", "#2C5F8A", "#2C5F8A",  # 北京、上海、深圳（第一梯队）
        "#3A72A6", "#4A85BC", "#5D97CA",  # 杭州、广州、成都（第二梯队）
        "#7BAAD6", "#9CBDE0"               # 南京、武汉（第三梯队）
    ]
    colors_rev = colors[::-1]  # 对应倒序的城市顺序

    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(labels_rev, values_rev, color=colors_rev, 
                   edgecolor="white", height=0.65, zorder=3)

    # 数值标签：条形右侧标注百分比
    for bar, val in zip(bars, values_rev):
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2, f"{val}%",
                va="center", fontsize=10, color="#2A2A2A")

    # 坐标轴与网格
    ax.set_xlim(0, 35)  # 与论文X轴范围一致
    ax.set_xlabel("占全国AI骨干企业比例(%)", fontsize=11)
    ax.grid(axis="x", color=CFG["GRID"], alpha=0.6, zorder=0)  # 垂直网格线
    
    # 隐藏上、右边框
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    save(fig, "fig05_城市分布条形图")

# ===== 图6: 三大经济圈AI企业占比环形图（正文图3-6，匹配论文样式） =====
def fig06():
    fig, ax = plt.subplots(figsize=(11, 9))
    # 颜色严格匹配论文：京津冀深蓝、长三角青绿、珠三角橙、成渝红、其他灰
    colors = [CFG["BLUE"], CFG["TEAL"], CFG["GOLD"], CFG["RED"], CFG["GRAY"]]

    wedges, _ = ax.pie(
        DATA["region_circle_pct"],
        startangle=90,
        colors=colors,
        wedgeprops={"width": 0.4, "edgecolor": "white", "linewidth": 2}
    )

    # 图例样式匹配论文：右侧排列，带百分比
    lgnd_text = [f"{l}  {v:.1f}%" for l, v in zip(DATA["region_circle_labels"], DATA["region_circle_pct"])]
    ax.legend(wedges, lgnd_text, loc="center left", bbox_to_anchor=(1, 0.5),
              fontsize=10, frameon=False)

    ax.set_title("AI企业经济圈分布(2025年)", fontsize=10, pad=10)
    save(fig, "fig06_经济圈环形图")

# ===== 图7: 区域AI综合指数热力图（正文图3-7） =====
def fig07():
    rgn = DATA["region_names"]
    mtr = DATA["region_metrics"]
    data = DATA["region_matrix"]

    fig, ax = plt.subplots(figsize=(13, 7.5))
    cmap = LinearSegmentedColormap.from_list("ai_blue", ["#EDF3F8", "#8FB1CA", CFG["BLUE"]])

    im = ax.imshow(data, cmap=cmap, vmin=0, vmax=100, aspect="auto")

    ax.set_xticks(range(len(mtr)))
    ax.set_xticklabels(mtr, fontsize=11)
    ax.set_yticks(range(len(rgn)))
    ax.set_yticklabels(rgn, fontsize=11)

    # 单元格数值标注
    for i in range(len(rgn)):
        for j in range(len(mtr)):
            ax.text(j, i, str(data[i, j]), ha="center", va="center",
                    fontweight="bold", fontsize=10,
                    color="white" if data[i, j] >= 78 else "#2A2A2A")

    [s.set_visible(False) for s in ax.spines.values()]
    ax.set_title("区域AI综合指数热力图(2025年)", fontsize=14, pad=15)
    save(fig, "fig07_区域热力图")

# ===== 图8: AI专利申请量面积图（正文图3-8） =====
def fig08():
    y, p = DATA["years_patent"], DATA["patent_count"]
    fig, ax = plt.subplots(figsize=(13, 7.5))

    ax.fill_between(y, p, color=CFG["TEAL"], alpha=0.25, zorder=2)
    ax.plot(y, p, color=CFG["TEAL"], lw=3, marker="o", ms=8,
            mfc="white", mec=CFG["TEAL"], mew=2, zorder=3)

    for x, v in zip(y, p):
        ax.text(x, v + 600, str(v), ha="center", fontsize=10, fontweight="bold", color=CFG["TEAL"])

    ax.set_ylim(0, 26000)
    setup_ax(ax, ylabel="AI相关专利申请量(件)")
    ax.set_title("2018—2024年中国AI相关专利申请量趋势", fontsize=14, pad=15)
    save(fig, "fig08_专利面积图")

# ===== 图9: AI产业投融资金额柱状图（正文图3-9） =====
def fig09():
    y, inv = DATA["years_invest"], DATA["invest_amount"]
    fig, ax = plt.subplots(figsize=(13, 7.5))

    # 配色：高峰年(2017、2021)深蓝，其余浅蓝
    bar_colors = []
    for i in range(len(inv)):
        if i == 2 or i == 6:  # 第3个=2017，第7个=2021
            bar_colors.append(CFG["BLUE"])
        else:
            bar_colors.append("#6A95C2")

    bars = ax.bar(y, inv, width=0.6, color=bar_colors, edgecolor="white", zorder=3)

    # 每个柱子顶部标注数值
    for bar, val in zip(bars, inv):
        ax.text(
            bar.get_x() + bar.get_width() / 2, val + 30,
            f"{val}亿", ha="center", fontsize=8.5, color="#2A2A2A"
        )

    # 2017 政策驱动高峰
    ax.annotate(
        "政策驱动高峰\n(2105亿)",
        xy=(2017, 2105), xytext=(2016.3, 2400),
        fontsize=8.5, color=CFG["RED"],
        arrowprops=dict(arrowstyle="->", color=CFG["RED"], lw=1)
    )
    # 2021 AI芯片/自动驾驶
    ax.annotate(
        "AI芯片/自动驾驶\n(2252亿)",
        xy=(2021, 2252), xytext=(2020.3, 2500),
        fontsize=8.5, color=CFG["RED"],
        arrowprops=dict(arrowstyle="->", color=CFG["RED"], lw=1)
    )

    # 坐标轴设置
    ax.set_ylim(0, 2700)
    ax.set_yticks([0, 500, 1000, 1500, 2000, 2500])
    ax.set_xticks(y)  # 显示所有年份
    ax.set_ylabel("投融资金额(亿元)", fontsize=10)
    ax.set_xlabel("年份", fontsize=10)

    # 去掉网格线（论文原图无网格）
    ax.grid(False)
    # 隐藏上、右边框
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_title("2015—2024年中国AI产业投融资金额趋势", fontsize=10, pad=10)
    save(fig, "fig09_投融资柱状图")

# ===== 图10: 情景预测区间图（正文图3-10） =====
def fig10():
    hy = DATA["years_history"]
    fy = DATA["years_forecast"]
    con = DATA["forecast_conservative"]
    neu = DATA["forecast_neutral"]
    opt = DATA["forecast_optimistic"]

    fig, ax = plt.subplots(figsize=(13, 7.5))

    # 不确定性填充区间
    ax.fill_between(fy, con, opt, color=CFG["TEAL"], alpha=0.10)
    # 三条情景线
    ax.plot(fy, con, color=CFG["GRAY"], lw=2, ls="--", label="保守情景")
    ax.plot(fy, neu, color=CFG["TEAL"], lw=3, marker="o", ms=8,
            mfc="white", mec=CFG["TEAL"], mew=2, label="中性情景")
    ax.plot(fy, opt, color=CFG["RED"], lw=2, ls="--", label="积极情景")
    # 历史数据
    ax.plot(hy, DATA["size"], color=CFG["BLUE"], lw=3, marker="o", ms=8,
            mfc="white", mec=CFG["BLUE"], mew=2, label="历史数据")

    # 预测分割线
    ax.axvline(2025, color="#CBD5E1", lw=1.5, ls="--")
    ax.text(2025.1, 35000, "预测起点", fontsize=10, color="#64748B")

    # 中性情景数值标注
    for x, v in zip(fy, neu):
        ax.annotate(f"{v}亿", (x, v), textcoords="offset points", xytext=(0, 14),
                    ha="center", fontsize=9, color=CFG["TEAL"], fontweight="bold")

    ax.legend(fontsize=11, frameon=False, loc="upper left")
    ax.set_ylim(0, 38000)
    setup_ax(ax, ylabel="产业规模(亿元)")
    ax.set_title("2026—2030年中国AI核心产业规模情景预测", fontsize=14, pad=15)
    save(fig, "fig10_情景预测区间图")

# ===== 图11: 细分领域发展趋势多线折线图（正文图3-11） =====
def fig11():
    y = DATA["years_tech_trend"]
    fig, ax = plt.subplots(figsize=(13, 7.5))

    # 五条赛道折线
    lines_config = [
        ("计算机视觉", DATA["trend_cv"], CFG["BLUE"], 3),
        ("NLP与语音", DATA["trend_nlp"], CFG["RED"], 3),
        ("AI芯片", DATA["trend_chip"], CFG["GOLD"], 2.5),
        ("机器学习平台", DATA["trend_ml"], CFG["PURPLE"], 2),
        ("智能机器人", DATA["trend_robot"], CFG["TEAL"], 2)
    ]

    for name, data, color, lw in lines_config:
        ax.plot(y, data, color=color, lw=lw, marker="o", ms=6,
                mfc="white", mec=color, mew=1.5, label=name)

    ax.legend(fontsize=11, frameon=False, loc="upper left")
    ax.set_ylim(0, 2500)
    setup_ax(ax, ylabel="市场规模(亿元)")
    ax.set_title("2019—2024年AI细分领域市场规模发展趋势", fontsize=14, pad=15)
    save(fig, "fig11_细分赛道折线图")

# ====================== 批量运行（异常保护） ======================
if __name__ == "__main__":
    all_figs = [
        fig01, fig02, fig03, fig04, fig05,
        fig06, fig07, fig08, fig09, fig10, fig11
    ]

    print("开始生成11张图表...")
    for fn in all_figs:
        try:
            fn()
            print(f"  ✅ {fn.__name__} 生成成功")
        except Exception as e:
            print(f"  ❌ {fn.__name__} 生成失败: {e}")

    # 导出核心数据CSV
    pd.DataFrame({
        "年份": DATA["years_size"],
        "产业规模(亿元)": DATA["size"],
        "同比增长率(%)": DATA["growth"]
    }).to_csv(out / "市场规模数据.csv", index=False, encoding="utf-8-sig")

    print("\n全部完成！图表与数据文件已保存至 ./charts/ 目录")