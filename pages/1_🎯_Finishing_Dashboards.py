"""
1_🎯_Finishing_Dashboards.py
------------------------------
Goals vs. Expected Goals (xG) and shot-conversion efficiency dashboards
built on a synthetic Championship-style dataset.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Finishing Dashboards", page_icon="🎯", layout="wide")

PRIMARY_BG = "#0d1117"
SECONDARY_BG = "#161b22"
ACCENT_BLUE = "#87CEEB"
ACCENT_TEAL = "#00F2FE"


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{ background: linear-gradient(180deg, {PRIMARY_BG} 0%, {SECONDARY_BG} 100%); color: #e6edf3; }}
        section[data-testid="stSidebar"] {{ background-color: {SECONDARY_BG}; }}
        h1, h2, h3, h4 {{ color: #f0f6fc !important; }}
        .pfsa-header {{
            background: linear-gradient(135deg, {SECONDARY_BG} 0%, #0f1a24 100%);
            border: 1px solid rgba(135, 206, 235, 0.25);
            border-radius: 16px; padding: 1.6rem 2rem; margin-bottom: 1.2rem;
        }}
        .pfsa-header h1 {{
            font-size: 1.9rem; margin-bottom: 0.2rem;
            background: linear-gradient(90deg, {ACCENT_BLUE}, {ACCENT_TEAL});
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .pfsa-header p {{ color: #9fb3c8; margin-bottom: 0; }}
        .pfsa-card {{
            background-color: {SECONDARY_BG}; border: 1px solid rgba(135, 206, 235, 0.18);
            border-radius: 12px; padding: 1rem 1.2rem; text-align: center;
        }}
        .pfsa-metric-value {{ font-size: 1.6rem; font-weight: 700; color: {ACCENT_TEAL}; }}
        .pfsa-metric-label {{ color: #9fb3c8; font-size: 0.78rem; text-transform: uppercase; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>🎯 Finishing Dashboards</h1>
        <p>Goal output vs. Expected Goals (xG) &amp; shot conversion efficiency — synthetic Championship dataset</p>
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def generate_finishing_data(seed: int = 7):
    rng = np.random.default_rng(seed)
    first_names = ["H", "T", "E", "J", "L", "B", "C", "M", "R", "D", "A", "S", "K", "P", "N"]
    surnames = [
        "Sinclair", "Wright", "Ogbene", "Godden", "Kelly", "Bidwell", "Allen", "Doyle",
        "Latibeaudiere", "Hamer", "Sakamoto", "Kyriakou", "Simms", "Torfason", "Bushiri",
        "Rudoni", "Norwood", "Palmer", "Iheanacho", "Awoniyi",
    ]
    n = 20
    players = [f"{rng.choice(first_names)}. {surnames[i]}" for i in range(n)]
    positions = rng.choice(["ST", "LW", "RW", "AM", "CM"], size=n, p=[0.25, 0.2, 0.2, 0.2, 0.15])

    shots = rng.integers(15, 95, size=n)
    xg_per_shot = rng.uniform(0.07, 0.18, size=n)
    xg = np.round(shots * xg_per_shot * rng.uniform(0.8, 1.2, size=n), 2)
    finishing_skill = rng.normal(1.0, 0.28, size=n)
    goals = np.maximum(0, np.round(xg * finishing_skill).astype(int))
    conversion = np.round(np.divide(goals, shots, out=np.zeros_like(goals, dtype=float), where=shots != 0) * 100, 1)

    df = pd.DataFrame(
        {
            "player": players,
            "position": positions,
            "shots": shots,
            "xG": xg,
            "goals": goals,
            "xG_diff": np.round(goals - xg, 2),
            "conversion_rate": conversion,
        }
    )
    return df


df = generate_finishing_data()

# --------------------------------------------------------------------------
# FILTERS
# --------------------------------------------------------------------------
f1, f2, f3 = st.columns([2, 1, 1])
with f1:
    pos_filter = st.multiselect("Filter by position", sorted(df["position"].unique()),
                                 default=sorted(df["position"].unique()))
with f2:
    min_shots = st.slider("Minimum shots", 0, int(df["shots"].max()), 10)
with f3:
    sort_by = st.selectbox("Sort table by", ["goals", "xG", "xG_diff", "conversion_rate", "shots"], index=2)

view = df[(df["position"].isin(pos_filter)) & (df["shots"] >= min_shots)].sort_values(sort_by, ascending=False)

# --------------------------------------------------------------------------
# KPI ROW
# --------------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
kpis = [
    ("Total Goals", int(view["goals"].sum())),
    ("Total xG", round(view["xG"].sum(), 1)),
    ("Avg. Conversion Rate", f'{view["conversion_rate"].mean():.1f}%' if len(view) else "0%"),
    ("Players Shown", len(view)),
]
for col, (label, val) in zip([k1, k2, k3, k4], kpis):
    with col:
        st.markdown(
            f'<div class="pfsa-card"><div class="pfsa-metric-value">{val}</div>'
            f'<div class="pfsa-metric-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")

# --------------------------------------------------------------------------
# CHART 1 — Goals vs xG scatter (over/under-performance)
# --------------------------------------------------------------------------
st.subheader("Goals vs. Expected Goals (xG)")

fig1, ax1 = plt.subplots(figsize=(9, 6))
fig1.patch.set_facecolor(PRIMARY_BG)
ax1.set_facecolor(PRIMARY_BG)

max_val = max(view["xG"].max(), view["goals"].max()) + 2 if len(view) else 10
ax1.plot([0, max_val], [0, max_val], linestyle="--", color="#3a4552", linewidth=1, label="Expected (Goals = xG)")

colors = np.where(view["xG_diff"] >= 0, ACCENT_TEAL, "#ff6b6b")
ax1.scatter(view["xG"], view["goals"], s=view["shots"] * 3.2, c=colors, alpha=0.75, edgecolors="#0d1117", linewidth=0.6)

for _, row in view.iterrows():
    ax1.annotate(row["player"].split()[-1], (row["xG"], row["goals"]),
                 fontsize=7.5, color="#c9d6e3", xytext=(4, 3), textcoords="offset points")

ax1.set_xlabel("Expected Goals (xG)", color="#9fb3c8")
ax1.set_ylabel("Goals Scored", color="#9fb3c8")
ax1.tick_params(colors="#9fb3c8")
for spine in ax1.spines.values():
    spine.set_color("#2a3542")
ax1.grid(alpha=0.15, color="#3a4552")
ax1.legend(facecolor=SECONDARY_BG, edgecolor="#2a3542", labelcolor="#c9d6e3", fontsize=8)
ax1.set_title("Bubble size = shot volume · Teal = overperforming xG · Red = underperforming",
              color="#f0f6fc", fontsize=10)

st.pyplot(fig1, use_container_width=True)

# --------------------------------------------------------------------------
# CHART 2 — Shot conversion rate bar chart
# --------------------------------------------------------------------------
st.subheader("Shot Conversion Rate by Player")

top_n = st.slider("Show top N players by conversion rate", 5, min(20, len(df)), 10)
bar_view = view.sort_values("conversion_rate", ascending=False).head(top_n)

fig2, ax2 = plt.subplots(figsize=(9, max(3.5, top_n * 0.42)))
fig2.patch.set_facecolor(PRIMARY_BG)
ax2.set_facecolor(PRIMARY_BG)

bars = ax2.barh(bar_view["player"], bar_view["conversion_rate"], color=ACCENT_BLUE, alpha=0.85)
for bar, rate in zip(bars, bar_view["conversion_rate"]):
    ax2.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2, f"{rate:.1f}%",
              va="center", color="#e6edf3", fontsize=8)

ax2.invert_yaxis()
ax2.set_xlabel("Conversion Rate (%)", color="#9fb3c8")
ax2.tick_params(colors="#9fb3c8")
for spine in ax2.spines.values():
    spine.set_color("#2a3542")
ax2.grid(axis="x", alpha=0.15, color="#3a4552")

st.pyplot(fig2, use_container_width=True)

with st.expander("📋 View full finishing dataset"):
    st.dataframe(view, use_container_width=True, hide_index=True)
