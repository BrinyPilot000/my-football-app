"""
4_🗺️_Player_Maps_Passing.py
------------------------------
mplsoccer pitch plotting a selected player's progressive passes and
cutbacks using directional arrows, built on synthetic event coordinates.
"""

import numpy as np
import pandas as pd
import streamlit as st
from mplsoccer import Pitch

st.set_page_config(page_title="Player Maps — Passing", page_icon="🗺️", layout="wide")

PRIMARY_BG = "#0d1117"
SECONDARY_BG = "#161b22"
ACCENT_BLUE = "#87CEEB"
ACCENT_TEAL = "#00F2FE"
PITCH_LINE = "#223044"


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
        <h1>🗺️ Player Maps — Progressive Passing</h1>
        <p>Progressive passes &amp; cutbacks mapped with directional arrows (synthetic event data)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

PLAYERS = ["T. Kelly", "J. Allen", "E. Godden", "J. Bidwell", "E. Ogbene", "T. Wright"]


@st.cache_data
def generate_pass_events(seed: int = 11, n_per_player: int = 55):
    rng = np.random.default_rng(seed)
    records = []
    for player in PLAYERS:
        for _ in range(n_per_player):
            x_start = rng.uniform(15, 75)
            y_start = rng.uniform(5, 75)
            # bias forward progression
            x_end = np.clip(x_start + rng.uniform(5, 40), 0, 100)
            y_end = np.clip(y_start + rng.uniform(-25, 25), 0, 80)

            forward_progress = x_end - x_start
            is_cutback = (x_end > 82) and (y_end < y_start) and (rng.random() > 0.5)
            is_progressive = forward_progress >= 12 or is_cutback

            outcome = rng.choice(["Complete", "Incomplete"], p=[0.78, 0.22])

            records.append(
                {
                    "player": player,
                    "x": x_start, "y": y_start,
                    "end_x": x_end, "end_y": y_end,
                    "is_progressive": is_progressive,
                    "is_cutback": is_cutback,
                    "outcome": outcome,
                }
            )
    return pd.DataFrame(records)


events = generate_pass_events()

c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    selected_player = st.selectbox("Select player", PLAYERS)
with c2:
    show_cutbacks = st.checkbox("Highlight cutbacks", value=True)
with c3:
    completed_only = st.checkbox("Completed passes only", value=False)

player_events = events[events["player"] == selected_player]
if completed_only:
    player_events = player_events[player_events["outcome"] == "Complete"]

prog_passes = player_events[player_events["is_progressive"] & ~player_events["is_cutback"]]
cutbacks = player_events[player_events["is_cutback"]]

k1, k2, k3, k4 = st.columns(4)
kpis = [
    ("Total Passes", len(player_events)),
    ("Progressive Passes", len(prog_passes)),
    ("Cutbacks", len(cutbacks)),
    ("Completion %", f'{(player_events["outcome"].eq("Complete").mean() * 100):.1f}%' if len(player_events) else "0%"),
]
for col, (label, val) in zip([k1, k2, k3, k4], kpis):
    with col:
        st.markdown(
            f'<div class="pfsa-card"><div class="pfsa-metric-value">{val}</div>'
            f'<div class="pfsa-metric-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")

pitch = Pitch(pitch_type="opta", pitch_color=PRIMARY_BG, line_color=PITCH_LINE, linewidth=1.3)
fig, ax = pitch.draw(figsize=(11, 7.2))
fig.patch.set_facecolor(PRIMARY_BG)

if not prog_passes.empty:
    pitch.arrows(
        prog_passes["x"], prog_passes["y"], prog_passes["end_x"], prog_passes["end_y"],
        color=ACCENT_BLUE, width=1.8, headwidth=6, headlength=6, alpha=0.8,
        ax=ax, label="Progressive Pass",
    )

if show_cutbacks and not cutbacks.empty:
    pitch.arrows(
        cutbacks["x"], cutbacks["y"], cutbacks["end_x"], cutbacks["end_y"],
        color=ACCENT_TEAL, width=2.4, headwidth=7, headlength=7, alpha=0.95,
        ax=ax, label="Cutback",
    )

ax.set_title(f"{selected_player} — Progressive Passes &amp; Cutbacks".replace("&amp;", "&"),
              color="#f0f6fc", fontsize=14, fontweight="bold", pad=12)

legend = ax.legend(facecolor=SECONDARY_BG, edgecolor="#2a3542", labelcolor="#e6edf3",
                     loc="upper left", fontsize=9)

st.pyplot(fig, use_container_width=True)

with st.expander("📋 View raw pass event data"):
    st.dataframe(player_events, use_container_width=True, hide_index=True)
