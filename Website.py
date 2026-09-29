
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. LOAD DATASET

df = pd.read_csv(
    r"D:\python_krish_nayak\Website_Alanysis_project\website_traffic_dataset.csv"
)

df["Date"] = pd.to_datetime(df["Date"])

# Professional chart theme (without gridlines)
sns.set_theme(style="white", rc={"axes.grid": False})

# 2. OVERALL KPI SUMMARY

total_users = df["Users"].sum()
total_sessions = df["Sessions"].sum()
total_pageviews = df["Pageviews"].sum()
total_conversions = df["Conversions"].sum()
total_goals = df["GoalCompletions"].sum()

bounce_rate = (
    (df["BounceRate"] * df["Sessions"]).sum()
    / df["Sessions"].sum()
) * 100

conversion_rate = (
    total_conversions / total_sessions
) * 100

avg_duration = (
    (df["AvgSessionDurationSec"] * df["Sessions"]).sum()
    / df["Sessions"].sum()
)

avg_pages = (
    (df["PagesPerSession"] * df["Sessions"]).sum()
    / df["Sessions"].sum()
)

print("\n========== WEBSITE TRAFFIC SUMMARY ==========")
print("Total Users:", f"{total_users:,}")
print("Total Sessions:", f"{total_sessions:,}")
print("Total Pageviews:", f"{total_pageviews:,}")
print("Bounce Rate:", round(bounce_rate, 2), "%")
print("Average Session Duration:", round(avg_duration, 2), "seconds")
print("Pages Per Session:", round(avg_pages, 2))
print("Total Conversions:", f"{total_conversions:,}")
print("Conversion Rate:", round(conversion_rate, 2), "%")
print("Goal Completions:", f"{total_goals:,}")



# 3. TRAFFIC SOURCE ANALYSIS

source_summary = df.groupby("TrafficSource").agg({
    "Users": "sum",
    "Sessions": "sum",
    "Pageviews": "sum",
    "Conversions": "sum",
    "GoalCompletions": "sum"
}).reset_index()

source_summary["ConversionRate"] = (
    source_summary["Conversions"]
    / source_summary["Sessions"] * 100
)

print("\n========== TRAFFIC SOURCE ANALYSIS ==========")

print(
    source_summary.sort_values(
        "Sessions", ascending=False
    ).round(2).to_string(index=False)
)

# 4. PAGE PERFORMANCE ANALYSIS

page_summary = df.groupby(
    ["PageName", "PagePath"]
).agg({
    "Users": "sum",
    "Sessions": "sum",
    "Pageviews": "sum",
    "Conversions": "sum",
    "GoalCompletions": "sum"
}).reset_index()

print("\n========== TOP 5 PAGES BY PAGEVIEWS ==========")

print(
    page_summary.sort_values(
        "Pageviews", ascending=False
    ).head(5).to_string(index=False)
)

print("\n========== LOWEST 5 PAGES BY PAGEVIEWS ==========")

print(
    page_summary.sort_values(
        "Pageviews", ascending=True
    ).head(5).to_string(index=False)
)

# 5. CHART 1: WEBSITE SESSIONS BY TRAFFIC SOURCE

traffic = (
    df.groupby("TrafficSource")["Sessions"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 4))

colors = sns.color_palette("husl", len(traffic))

bars = ax.bar(
    traffic.index,
    traffic.values,
    color=colors,
    edgecolor="white",
    linewidth=1.5,
    width=0.65
)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{int(height):,}",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold"
    )

ax.set_title(
    "Website Sessions by Traffic Source",
    fontsize=18,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Traffic Source", fontsize=12)
ax.set_ylabel("Total Sessions", fontsize=12)
ax.tick_params(axis="x", rotation=20)
ax.grid(False)

plt.tight_layout()
plt.show()

# 6. CHART 2: BOUNCE RATE BY TRAFFIC SOURCE

bounce = df.groupby("TrafficSource")["BounceRate"].mean()

if bounce.max() <= 1:
    bounce = bounce * 100

bounce = bounce.sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 4))

colors = sns.color_palette("Spectral", len(bounce))

bars = ax.bar(
    bounce.index,
    bounce.values,
    color=colors,
    edgecolor="white",
    linewidth=1.5,
    width=0.65
)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.1f}%",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold"
    )

ax.set_title(
    "Bounce Rate by Traffic Source",
    fontsize=18,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Traffic Source", fontsize=12)
ax.set_ylabel("Bounce Rate (%)", fontsize=12)
ax.tick_params(axis="x", rotation=20)
ax.set_ylim(0, bounce.max() * 1.15)
ax.grid(False)

plt.tight_layout()
plt.show()

# 7. CHART 3: CONVERSION RATE BY TRAFFIC SOURCE

conversion = df.groupby("TrafficSource").agg({
    "Sessions": "sum",
    "Conversions": "sum"
})

conversion["ConversionRate"] = (
    conversion["Conversions"]
    / conversion["Sessions"]
) * 100

conversion = conversion["ConversionRate"].sort_values(
    ascending=False
)

fig, ax = plt.subplots(figsize=(8, 4))

colors = sns.color_palette("viridis", len(conversion))

bars = ax.bar(
    conversion.index,
    conversion.values,
    color=colors,
    edgecolor="white",
    linewidth=1.5,
    width=0.65
)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.2f}%",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold"
    )

ax.set_title(
    "Conversion Rate by Traffic Source",
    fontsize=18,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Traffic Source", fontsize=12)
ax.set_ylabel("Conversion Rate (%)", fontsize=12)
ax.tick_params(axis="x", rotation=20)
ax.set_ylim(0, conversion.max() * 1.2)
ax.grid(False)

plt.tight_layout()
plt.show()

# 8. CHART 4: TOP 10 PAGES BY PAGEVIEWS

top_pages = (
    df.groupby("PageName")["Pageviews"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values(ascending=True)
)

fig, ax = plt.subplots(figsize=(8, 5))

colors = sns.color_palette("mako", len(top_pages))

bars = ax.barh(
    top_pages.index,
    top_pages.values,
    color=colors,
    edgecolor="white",
    linewidth=1.5,
    height=0.65
)

for bar in bars:
    width = bar.get_width()
    ax.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        f" {int(width):,}",
        va="center",
        fontsize=10,
        fontweight="bold"
    )

ax.set_title(
    "Top 10 Pages by Pageviews",
    fontsize=18,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Total Pageviews", fontsize=12)
ax.set_ylabel("Website Pages", fontsize=12)
ax.grid(False)

plt.tight_layout()
plt.show()

# 9. CHART 5: DAILY WEBSITE TRAFFIC TREND

daily_traffic = (
    df.groupby("Date")["Sessions"]
    .sum()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(11,5))

ax.plot(
    daily_traffic.index,
    daily_traffic.values,
    color="#6C63FF",
    linewidth=2.5,
    marker="o",
    markersize=4,
    markerfacecolor="#FF6B6B",
    markeredgecolor="white",
    label="Daily Sessions"
)

ax.fill_between(
    daily_traffic.index,
    daily_traffic.values,
    color="#6C63FF",
    alpha=0.15
)

ax.set_title(
    "Daily Website Traffic Trend",
    fontsize=18,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Total Sessions", fontsize=12)
ax.tick_params(axis="x", rotation=45)
ax.legend()
ax.grid(False)

plt.tight_layout()
plt.show()