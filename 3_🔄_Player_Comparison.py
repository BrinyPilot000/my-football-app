"""
3_🔄_Player_Comparison.py
---------------------------
Side-by-side pizza-style comparison chart (matplotlib polar bar chart)
for two selected players across a synthetic percentile-metric matrix.
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Player Comparison", page_icon="🔄", layout="wide")

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
        .pfsa-legend-a {{ color: {ACCENT_BLUE}; font-weight: 700; }}
        .pfsa-legend-b {{ color: {ACCENT_TEAL}; font-weight: 700; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>🔄 Player Comparison — Pizza Chart</h1>
        <p>Head-to-head percentile comparison across key performance metrics (synthetic league dataset)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

METRICS = [
    "Goals /90", "xG /90", "Shots /90", "Key Passes /90", "Dribbles /90",
    "Progressive Carries /90", "Pass Completion %", "Aerial Win %",
    "Tackles /90", "Interceptions /90", "Pressures /90", "Defensive Duels Won %",
]


@st.cache_data
def generate_player_pool(seed: int = 21):
    rng = np.random.default_rng(seed)
    surnames = [
        "Sinclair", "Wright", "Ogbene", "Godden", "Kelly", "Bidwell", "Allen", "Doyle",
        "Latibeaudiere", "Sakamoto", "Kyriakou", "Simms", "Torfason", "Bushiri", "Rudoni",
        "Norwood", "Palmer", "Iheanacho", "Awoniyi", "Eze", "Mitoma", "Gordon",
    ]
    n = len(surnames)
    data = {"player": surnames}
    for m in METRICS:
        data[m] = np.clip(rng.normal(50, 22, size=n), 1, 99).round(1)
    return pd.DataFrame(data)


pool = generate_player_pool()

c1, c2 = st.columns(2)
with c1:
    player_a = st.selectbox("Select Player A", pool["player"], index=0)
with c2:
    default_b_idx = 1 if len(pool) > 1 else 0
    player_b = st.selectbox("Select Player B", pool["player"], index=default_b_idx)

row_a = pool[pool["player"] == player_a].iloc[0]
row_b = pool[pool["player"] == player_b].iloc[0]

values_a = [row_a[m] for m in METRICS]
values_b = [row_b[m] for m in METRICS]

# --------------------------------------------------------------------------
# PIZZA / POLAR BAR CHART
# --------------------------------------------------------------------------
def draw_pizza(ax, values, color, label):
    n = len(METRICS)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    width = (2 * np.pi / n) * 0.92

    ax.set_facecolor(PRIMARY_BG)
    bars = ax.bar(angles, values, width=width, color=color, alpha=0.85,
                   edgecolor=PRIMARY_BG, linewidth=1.5, zorder=3)

    ax.set_ylim(0, 100)
    ax.set_yticklabels([])
    ax.set_xticks(angles)
    ax.set_xticklabels(METRICS, fontsize=8, color="#e6edf3")
    ax.spines["polar"].set_visible(False)
    ax.grid(color="#2a3542", alpha=0.4)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    for angle, val in zip(angles, values):
        ax.text(angle, val + 6, f"{val:.0f}", ha="center", va="center",
                 fontsize=7.5, color="#f0f6fc", fontweight="bold", zorder=4)

    ax.set_title(label, color=color, fontsize=13, fontweight="bold", pad=18)


fig, axes = plt.subplots(1, 2, subplot_kw={"projection": "polar"}, figsize=(13, 6.5))
fig.patch.set_facecolor(PRIMARY_BG)

draw_pizza(axes[0], values_a, ACCENT_BLUE, f"{player_a}")
draw_pizza(axes[1], values_b, ACCENT_TEAL, f"{player_b}")

fig.suptitle("Percentile Rank vs. League Sample (0–100)", color="#9fb3c8", fontsize=10, y=0.02)
st.pyplot(fig, use_container_width=True)

# --------------------------------------------------------------------------
# HEAD-TO-HEAD TABLE
# --------------------------------------------------------------------------
st.subheader("Metric-by-Metric Breakdown")
compare_df = pd.DataFrame(
    {
        "Metric": METRICS,
        player_a: values_a,
        player_b: values_b,
        "Edge": [player_a if a > b else (player_b if b > a else "Tie") for a, b in zip(values_a, values_b)],
    }
)
st.dataframe(compare_df, use_container_width=True, hide_index=True)
