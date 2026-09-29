
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# 1. LOAD DATASET

df = pd.read_csv(
    r"D:\python_krish_nayak\Website_Alanysis_project\website_traffic_dataset.csv"
)

df["Date"] = pd.to_datetime(df["Date"])

sns.set_theme(style="white", rc={"axes.grid": False})

# 2. KPI CALCULATIONS

total_users = df["Users"].sum()
total_sessions = df["Sessions"].sum()
total_pageviews = df["Pageviews"].sum()
total_conversions = df["Conversions"].sum()

conversion_rate = (
    total_conversions / total_sessions * 100
)

# 3. DASHBOARD SETTINGS

fig = plt.figure(
    figsize=(20, 14),
    dpi=100,
    facecolor="#B4C4D8"
)

# 10 px margin = 0.01 inch at 100 DPI
# Figure height = 14 inches
# Normalized margin = 0.01 / 14

gap = 10 / (100 * 14)
# 4. MAIN HEADING

fig.text(
    0.5, 0.965,
    "WEBSITE TRAFFIC ANALYTICS DASHBOARD",
    ha="center",
    fontsize=24,
    fontweight="bold",
    color="#172554"
)

fig.text(
    0.5, 0.93,
    "Traffic | Engagement | Conversion | Page Performance",
    ha="center",
    fontsize=11,
    color="#57667B"
)

# 5. KPI CARDS

kpis = [
    ("TOTAL USERS", f"{total_users:,}", "#2563EB"),
    ("TOTAL SESSIONS", f"{total_sessions:,}", "#7C3AED"),
    ("PAGEVIEWS", f"{total_pageviews:,}", "#0891B2"),
    ("CONVERSION RATE", f"{conversion_rate:.2f}%", "#059669")
]

for i, (title, value, color) in enumerate(kpis):

    ax = fig.add_axes([
        0.055 + i * 0.23,
        0.835,
        0.205,
        0.07
    ])

    ax.set_facecolor(color)
    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.text(
        0.5, 0.68,
        title,
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        color="white"
    )

    ax.text(
        0.5, 0.28,
        value,
        ha="center",
        va="center",
        fontsize=21,
        fontweight="bold",
        color="white"
    )

# 6. CHART POSITIONS

chart_width = 0.415
chart_height = 0.19

left_x = 0.055
right_x = 0.535

# Chart 1 and Chart 2
row1_y = 0.575

# Chart 3 and Chart 4
# Exactly 10 px gap between axes boundaries
row2_y = row1_y - chart_height - 0.100

# 7. COMMON CHART STYLE

def clean_chart(ax):

    ax.grid(False)
    ax.set_facecolor("#646F9F")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(
        axis="both",
        length=0,
        labelsize=9,
        pad=5
    )

# 8. CHART 1: SESSIONS BY TRAFFIC SOURCE

ax1 = fig.add_axes([
    left_x, row1_y,
    chart_width, chart_height
])

traffic = (
    df.groupby("TrafficSource")["Sessions"]
    .sum()
    .sort_values(ascending=False)
)

bars = ax1.bar(
    traffic.index,
    traffic.values,
    color=sns.color_palette("husl", len(traffic)),
    edgecolor="white",
    linewidth=1.2,
    width=0.65
)

for bar in bars:

    h = bar.get_height()

    ax1.annotate(
        f"{h:,.0f}",
        (bar.get_x() + bar.get_width() / 2, h),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        fontweight="bold"
    )

ax1.set_title(
    "Sessions by Traffic Source",
    fontsize=14,
    fontweight="bold",
    color="#172554",
    pad=8
)

ax1.set_ylabel("Sessions", fontsize=10)
ax1.tick_params(axis="x", rotation=20)
ax1.margins(y=0.18)

clean_chart(ax1)

# 9. CHART 2: BOUNCE RATE

ax2 = fig.add_axes([
    right_x, row1_y,
    chart_width, chart_height
])

bounce = df.groupby("TrafficSource").apply(
    lambda x: (
        (x["BounceRate"] * x["Sessions"]).sum()
        / x["Sessions"].sum()
    ),
    include_groups=False
)

if bounce.max() <= 1:
    bounce = bounce * 100

bounce = bounce.sort_values(ascending=False)

bars = ax2.bar(
    bounce.index,
    bounce.values,
    color=sns.color_palette("Spectral", len(bounce)),
    edgecolor="white",
    linewidth=1.2,
    width=0.65
)

for bar in bars:

    h = bar.get_height()

    ax2.annotate(
        f"{h:.1f}%",
        (bar.get_x() + bar.get_width() / 2, h),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        fontweight="bold"
    )

ax2.set_title(
    "Bounce Rate by Traffic Source",
    fontsize=14,
    fontweight="bold",
    color="#172554",
    pad=8
)

ax2.set_ylabel("Bounce Rate (%)", fontsize=10)
ax2.tick_params(axis="x", rotation=20)
ax2.margins(y=0.18)

clean_chart(ax2)

# 10. CHART 3: CONVERSION RATE

ax3 = fig.add_axes([
    left_x, row2_y,
    chart_width, chart_height
])

conversion = df.groupby("TrafficSource").agg(
    Sessions=("Sessions", "sum"),
    Conversions=("Conversions", "sum")
)

conversion["Rate"] = (
    conversion["Conversions"]
    / conversion["Sessions"]
    * 100
)

conversion = conversion["Rate"].sort_values(
    ascending=False
)

bars = ax3.bar(
    conversion.index,
    conversion.values,
    color=sns.color_palette("viridis", len(conversion)),
    edgecolor="white",
    linewidth=1.2,
    width=0.65
)

for bar in bars:

    h = bar.get_height()

    ax3.annotate(
        f"{h:.2f}%",
        (bar.get_x() + bar.get_width() / 2, h),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        fontweight="bold"
    )

ax3.set_title(
    "Conversion Rate by Traffic Source",
    fontsize=14,
    fontweight="bold",
    color="#172554",
    pad=8
)

ax3.set_ylabel("Conversion Rate (%)", fontsize=10)
ax3.tick_params(axis="x", rotation=20)
ax3.margins(y=0.18)

clean_chart(ax3)

# 11. CHART 4: TOP 10 PAGES

ax4 = fig.add_axes([
    right_x, row2_y,
    chart_width, chart_height
])

top_pages = (
    df.groupby("PageName")["Pageviews"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

bars = ax4.barh(
    top_pages.index,
    top_pages.values,
    color=sns.color_palette("mako", len(top_pages)),
    edgecolor="white",
    linewidth=1.2,
    height=0.65
)

for bar in bars:

    w = bar.get_width()

    ax4.annotate(
        f"{w:,.0f}",
        (w, bar.get_y() + bar.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9,
        fontweight="bold"
    )

ax4.set_title(
    "Top 10 Pages by Pageviews",
    fontsize=14,
    fontweight="bold",
    color="#172554",
    pad=8
)

ax4.set_xlabel("Pageviews", fontsize=10)
ax4.margins(x=0.18)

clean_chart(ax4)

# 12. CHART 5: DAILY TRAFFIC TREND

ax5 = fig.add_axes([
    0.070, 0.070,
    0.870, 0.12
])

daily = (
    df.groupby("Date")["Sessions"]
    .sum()
    .sort_index()
)

ax5.plot(
    daily.index,
    daily.values,
    color="#2563EB",
    linewidth=2.5
)

ax5.fill_between(
    daily.index,
    daily.values,
    color="#60A5FA",
    alpha=0.15
)

ax5.set_title(
    "Daily Website Traffic Trend",
    fontsize=14,
    fontweight="bold",
    color="#172554",
    pad=8
)

ax5.set_ylabel("Sessions", fontsize=10)

ax5.xaxis.set_major_locator(
    mdates.AutoDateLocator(minticks=5, maxticks=8)
)

ax5.xaxis.set_major_formatter(
    mdates.DateFormatter("%d %b %Y")
)

ax5.tick_params(axis="x", labelsize=9)
ax5.margins(x=0.02, y=0.15)

clean_chart(ax5)

# 13. SAVE DASHBOARD

plt.savefig(
    "website_traffic_dashboard.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="#4D6D97"
)

# 14. SHOW DASHBOARD


plt.show()