"""
5_💥_Player_Maps_Shots.py
----------------------------
mplsoccer shot map with circle diameter scaled by xG value,
color-coded by outcome (Goal / Saved / Off Target / Blocked).
"""

import numpy as np
import pandas as pd
import streamlit as st
from mplsoccer import Pitch, VerticalPitch

st.set_page_config(page_title="Player Maps — Shots", page_icon="💥", layout="wide")

PRIMARY_BG = "#0d1117"
SECONDARY_BG = "#161b22"
ACCENT_BLUE = "#87CEEB"
ACCENT_TEAL = "#00F2FE"
PITCH_LINE = "#223044"
GOAL_COLOR = "#00F2FE"
MISS_COLOR = "#4b5563"
SAVED_COLOR = "#87CEEB"
BLOCKED_COLOR = "#ff6b6b"


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
        <h1>💥 Player Maps — Shot Map</h1>
        <p>Shot location plotting with circle diameter scaled to xG value (synthetic shot event data)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

PLAYERS = ["H. Sinclair", "T. Wright", "E. Ogbene", "T. Kelly", "E. Godden"]
OUTCOMES = ["Goal", "Saved", "Off Target", "Blocked"]
OUTCOME_COLORS = {"Goal": GOAL_COLOR, "Saved": SAVED_COLOR, "Off Target": MISS_COLOR, "Blocked": BLOCKED_COLOR}


@st.cache_data
def generate_shot_data(seed: int = 33, shots_per_player: int = 40):
    rng = np.random.default_rng(seed)
    records = []
    for player in PLAYERS:
        for _ in range(shots_per_player):
            # Shots cluster around the box, using Opta coordinate system (attacking → x=100)
            x = np.clip(rng.normal(88, 8), 60, 100)
            y = np.clip(rng.normal(40, 14), 5, 75)

            dist_to_goal = np.hypot(100 - x, 40 - y)
            xg = np.clip(0.55 - dist_to_goal * 0.014 + rng.normal(0, 0.05), 0.02, 0.85)

            if xg > 0.3:
                probs = np.array([min(0.55, xg + 0.05), 0.30, 0.10, 0.05])
            else:
                probs = np.array([0.10, 0.35, 0.35, 0.20])
            probs = probs / probs.sum()  # guarantee a valid probability distribution
            outcome = rng.choice(OUTCOMES, p=probs)

            records.append({"player": player, "x": x, "y": y, "xG": round(xg, 2), "outcome": outcome})

    df = pd.DataFrame(records)
    # normalise probability rounding artifacts
    return df


shots = generate_shot_data()

c1, c2 = st.columns([2, 2])
with c1:
    selected_player = st.selectbox("Select player", PLAYERS)
with c2:
    outcome_filter = st.multiselect("Filter by outcome", OUTCOMES, default=OUTCOMES)

player_shots = shots[(shots["player"] == selected_player) & (shots["outcome"].isin(outcome_filter))]

k1, k2, k3, k4 = st.columns(4)
kpis = [
    ("Total Shots", len(player_shots)),
    ("Total xG", round(player_shots["xG"].sum(), 2)),
    ("Goals", int((player_shots["outcome"] == "Goal").sum())),
    ("xG / Shot", round(player_shots["xG"].mean(), 2) if len(player_shots) else 0),
]
for col, (label, val) in zip([k1, k2, k3, k4], kpis):
    with col:
        st.markdown(
            f'<div class="pfsa-card"><div class="pfsa-metric-value">{val}</div>'
            f'<div class="pfsa-metric-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")

pitch = VerticalPitch(
    pitch_type="opta", half=True, pitch_color=PRIMARY_BG, line_color=PITCH_LINE, linewidth=1.3,
)
fig, ax = pitch.draw(figsize=(8.5, 8.5))
fig.patch.set_facecolor(PRIMARY_BG)

for outcome in outcome_filter:
    subset = player_shots[player_shots["outcome"] == outcome]
    if subset.empty:
        continue
    sizes = 60 + (subset["xG"] ** 0.9) * 2600  # diameter scales with xG
    pitch.scatter(
        subset["x"], subset["y"],
        s=sizes,
        color=OUTCOME_COLORS[outcome],
        edgecolors="#0d1117",
        linewidth=1.1,
        alpha=0.82 if outcome != "Goal" else 0.95,
        ax=ax,
        label=outcome,
        zorder=3 if outcome == "Goal" else 2,
    )

ax.set_title(f"{selected_player} — Shot Map (circle size = xG)", color="#f0f6fc",
              fontsize=13, fontweight="bold", pad=14)
legend = ax.legend(facecolor=SECONDARY_BG, edgecolor="#2a3542", labelcolor="#e6edf3",
                     loc="lower center", ncol=4, fontsize=8, bbox_to_anchor=(0.5, -0.06))

st.pyplot(fig, use_container_width=True)

st.caption("Bubble diameter reflects xG value — e.g. a 0.05 xG chance renders far smaller than a 0.65 xG chance.")

with st.expander("📋 View raw shot data"):
    st.dataframe(player_shots.sort_values("xG", ascending=False), use_container_width=True, hide_index=True)
