"""
8_📉_Scatter_Plot_Beta.py
----------------------------
Interactive quadrant scatter plot with adjustable X/Y axis dropdowns
to benchmark players across a synthetic league dataset.
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Scatter Plot Beta", page_icon="📉", layout="wide")

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
        .pfsa-beta-tag {{
            display:inline-block; padding:0.15rem 0.55rem; border-radius:6px;
            background: rgba(255,139,139,0.12); border:1px solid rgba(255,139,139,0.5);
            color:#ff8b8b; font-size:0.7rem; letter-spacing:0.05em; text-transform:uppercase;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>📉 Scatter Plot Beta <span class="pfsa-beta-tag">Beta Module</span></h1>
        <p>Adjustable-axis quadrant benchmarking across the synthetic league sample</p>
    </div>
    """,
    unsafe_allow_html=True,
)

METRICS = {
    "Aerial Wins /90": (0.5, 6.5),
    "Defensive Duels Won /90": (1.0, 9.0),
    "Progressive Carries /90": (0.5, 8.0),
    "Key Passes /90": (0.2, 4.5),
    "Shots /90": (0.5, 5.5),
    "xG /90": (0.02, 0.85),
    "Tackles /90": (0.5, 5.5),
    "Interceptions /90": (0.3, 4.0),
    "Dribbles Completed /90": (0.3, 5.0),
    "Pass Completion %": (55, 94),
}


@st.cache_data
def generate_league_sample(seed: int = 60):
    rng = np.random.default_rng(seed)
    surnames = [
        "Sinclair", "Wright", "Ogbene", "Godden", "Kelly", "Bidwell", "Allen", "Doyle",
        "Latibeaudiere", "Sakamoto", "Kyriakou", "Simms", "Torfason", "Bushiri", "Rudoni",
        "Norwood", "Palmer", "Iheanacho", "Awoniyi", "Eze", "Mitoma", "Gordon", "Mbeumo",
        "Semenyo", "Diaby", "Solanke", "Watkins", "Isak", "Cunha", "Wissa", "Bowen",
        "Maddison", "Gibbs-White", "Ward-Prowse", "McNeil",
    ]
    n = len(surnames)
    data = {"player": surnames}
    data["position"] = rng.choice(["FW", "MF", "DF"], size=n, p=[0.35, 0.4, 0.25])
    for metric, (lo, hi) in METRICS.items():
        data[metric] = np.round(rng.uniform(lo, hi, size=n), 2)
    return pd.DataFrame(data)


df = generate_league_sample()

c1, c2, c3, c4 = st.columns([1.3, 1.3, 1, 1])
with c1:
    x_metric = st.selectbox("X-axis metric", list(METRICS.keys()), index=list(METRICS.keys()).index("Aerial Wins /90"))
with c2:
    y_metric = st.selectbox("Y-axis metric", list(METRICS.keys()), index=list(METRICS.keys()).index("Defensive Duels Won /90"))
with c3:
    pos_filter = st.multiselect("Position", ["FW", "MF", "DF"], default=["FW", "MF", "DF"])
with c4:
    label_points = st.checkbox("Show player labels", value=True)

view = df[df["position"].isin(pos_filter)]

x_mean, y_mean = view[x_metric].mean(), view[y_metric].mean()
pos_colors = {"FW": ACCENT_TEAL, "MF": ACCENT_BLUE, "DF": "#c9a7ff"}

fig, ax = plt.subplots(figsize=(10, 7.5))
fig.patch.set_facecolor(PRIMARY_BG)
ax.set_facecolor(PRIMARY_BG)

for pos in pos_filter:
    subset = view[view["position"] == pos]
    ax.scatter(subset[x_metric], subset[y_metric], s=95, color=pos_colors[pos],
               alpha=0.82, edgecolors="#0d1117", linewidth=0.6, label=pos)

if label_points:
    for _, row in view.iterrows():
        ax.annotate(row["player"], (row[x_metric], row[y_metric]), fontsize=7.5,
                     color="#c9d6e3", xytext=(4, 3), textcoords="offset points")

ax.axvline(x_mean, color="#3a4552", linestyle="--", linewidth=1)
ax.axhline(y_mean, color="#3a4552", linestyle="--", linewidth=1)

ax.set_xlabel(x_metric, color="#9fb3c8")
ax.set_ylabel(y_metric, color="#9fb3c8")
ax.tick_params(colors="#9fb3c8")
for spine in ax.spines.values():
    spine.set_color("#2a3542")
ax.grid(alpha=0.15, color="#3a4552")
ax.legend(facecolor=SECONDARY_BG, edgecolor="#2a3542", labelcolor="#e6edf3", fontsize=8)
ax.set_title(f"{x_metric} vs. {y_metric} — Quadrant Benchmark", color="#f0f6fc", fontsize=12, fontweight="bold")

st.pyplot(fig, use_container_width=True)

st.caption("Dashed lines mark the sample mean for each axis, dividing the plot into four benchmarking quadrants.")

with st.expander("📋 View underlying data"):
    st.dataframe(view[["player", "position", x_metric, y_metric]], use_container_width=True, hide_index=True)
