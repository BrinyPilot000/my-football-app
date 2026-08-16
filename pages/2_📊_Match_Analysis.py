"""
2_📊_Match_Analysis.py
-----------------------
Passing network engine for Al-Hilal (Saudi Pro League) and Al-Ain (UAE Pro
League), built on a hardcoded spatial touch-position dataset. Includes a
Climate Heat Fatigue Toggle that simulates deeper defensive positioning
during high-temperature (38°C+) summer fixtures.

Dataset is a hardcoded, illustrative mock dataset for portfolio
demonstration purposes only — it does not represent real tracking data.
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from mplsoccer import Pitch

st.set_page_config(page_title="Match Analysis | Passing Network", page_icon="📊", layout="wide")

PRIMARY_BG = "#0d1117"
SECONDARY_BG = "#161b22"
ACCENT_BLUE = "#87CEEB"
ACCENT_TEAL = "#00F2FE"
PITCH_BG = "#0d1117"
PITCH_LINE = "#2c3745"
HEAT_COLOR = "#ff8b5c"


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
        .pfsa-heat-banner {{
            background: rgba(255, 139, 92, 0.08); border: 1px solid rgba(255, 139, 92, 0.45);
            border-left: 4px solid {HEAT_COLOR}; border-radius: 10px; padding: 0.8rem 1.1rem;
            color: #ffcbb0; font-size: 0.88rem; margin-bottom: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>📊 Match Analysis — Passing Network Engine</h1>
        <p>Al-Hilal (Saudi Pro League) &amp; Al-Ain (UAE Pro League) · Node size = touch involvement ·
        Glowing edges = pass combinations (min. 3 passes)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "⚠️ All positions, touch counts, and pass combinations below are illustrative mock values built "
    "for portfolio demonstration purposes and do not represent real tracking data."
)

# --------------------------------------------------------------------------
# HARDCODED SPATIAL TOUCH-POSITION DATASET
# --------------------------------------------------------------------------
TEAM_DATA = {
    "Al-Hilal": {
        "league": "Saudi Pro League",
        "formation": "4-3-3",
        "2024/2025 (Last Season)": {
            "lineup": [
                {"player": "Y. Bounou", "position": "GK", "x": 8, "y": 50, "touches": 30},
                {"player": "S. Abdulhamid", "position": "RB", "x": 24, "y": 78, "touches": 54},
                {"player": "K. Koulibaly", "position": "CB", "x": 18, "y": 60, "touches": 68},
                {"player": "A. Al-Bulaihi", "position": "CB", "x": 18, "y": 40, "touches": 64},
                {"player": "R. Lodi", "position": "LB", "x": 24, "y": 22, "touches": 58},
                {"player": "R. Neves", "position": "CDM", "x": 40, "y": 50, "touches": 82},
                {"player": "M. Kanno", "position": "CM", "x": 50, "y": 30, "touches": 66},
                {"player": "S. Milinković-Savić", "position": "CM", "x": 50, "y": 70, "touches": 60},
                {"player": "S. Al-Dawsari", "position": "RW", "x": 72, "y": 78, "touches": 46},
                {"player": "A. Mitrović", "position": "ST", "x": 84, "y": 50, "touches": 34},
                {"player": "M. Leonardo", "position": "LW", "x": 72, "y": 22, "touches": 38},
            ],
            "combos": [
                ("R. Neves", "K. Koulibaly", 14), ("R. Neves", "A. Al-Bulaihi", 12),
                ("R. Neves", "M. Kanno", 16), ("R. Neves", "S. Milinković-Savić", 11),
                ("K. Koulibaly", "A. Al-Bulaihi", 9), ("K. Koulibaly", "S. Abdulhamid", 8),
                ("A. Al-Bulaihi", "R. Lodi", 8), ("M. Kanno", "S. Abdulhamid", 7),
                ("S. Milinković-Savić", "R. Lodi", 6), ("M. Kanno", "S. Al-Dawsari", 5),
                ("S. Milinković-Savić", "M. Leonardo", 6), ("S. Al-Dawsari", "A. Mitrović", 4),
                ("M. Leonardo", "A. Mitrović", 4), ("S. Abdulhamid", "S. Al-Dawsari", 5),
                ("R. Lodi", "M. Leonardo", 5), ("Y. Bounou", "K. Koulibaly", 10),
                ("Y. Bounou", "A. Al-Bulaihi", 9), ("R. Neves", "Y. Bounou", 5),
                ("M. Kanno", "S. Milinković-Savić", 6), ("A. Mitrović", "S. Milinković-Savić", 3),
            ],
        },
        "2025/2026 (Current Season)": {
            "lineup": [
                {"player": "Y. Bounou", "position": "GK", "x": 8, "y": 50, "touches": 26},
                {"player": "S. Abdulhamid", "position": "RB", "x": 24, "y": 78, "touches": 48},
                {"player": "K. Koulibaly", "position": "CB", "x": 18, "y": 60, "touches": 60},
                {"player": "A. Al-Bulaihi", "position": "CB", "x": 18, "y": 40, "touches": 57},
                {"player": "R. Lodi", "position": "LB", "x": 24, "y": 22, "touches": 50},
                {"player": "R. Neves", "position": "CDM", "x": 40, "y": 50, "touches": 74},
                {"player": "M. Kanno", "position": "CM", "x": 50, "y": 30, "touches": 58},
                {"player": "S. Milinković-Savić", "position": "CM", "x": 50, "y": 70, "touches": 52},
                {"player": "S. Al-Dawsari", "position": "RW", "x": 72, "y": 78, "touches": 40},
                {"player": "A. Mitrović", "position": "ST", "x": 84, "y": 50, "touches": 27},
                {"player": "M. Leonardo", "position": "LW", "x": 72, "y": 22, "touches": 33},
            ],
            "combos": [
                ("R. Neves", "K. Koulibaly", 11), ("R. Neves", "A. Al-Bulaihi", 10),
                ("R. Neves", "M. Kanno", 13), ("R. Neves", "S. Milinković-Savić", 9),
                ("K. Koulibaly", "A. Al-Bulaihi", 8), ("K. Koulibaly", "S. Abdulhamid", 6),
                ("A. Al-Bulaihi", "R. Lodi", 7), ("M. Kanno", "S. Abdulhamid", 5),
                ("S. Milinković-Savić", "R. Lodi", 5), ("M. Kanno", "S. Al-Dawsari", 4),
                ("S. Milinković-Savić", "M. Leonardo", 5), ("S. Al-Dawsari", "A. Mitrović", 3),
                ("M. Leonardo", "A. Mitrović", 3), ("Y. Bounou", "K. Koulibaly", 8),
                ("Y. Bounou", "A. Al-Bulaihi", 7), ("M. Kanno", "S. Milinković-Savić", 5),
            ],
        },
    },
    "Al-Ain": {
        "league": "UAE Pro League",
        "formation": "4-2-3-1",
        "2024/2025 (Last Season)": {
            "lineup": [
                {"player": "K. Eisa", "position": "GK", "x": 8, "y": 50, "touches": 28},
                {"player": "Y. Al-Shamsi", "position": "RB", "x": 24, "y": 76, "touches": 50},
                {"player": "K. Laba", "position": "CB", "x": 18, "y": 60, "touches": 62},
                {"player": "M. Al-Menhali", "position": "CB", "x": 18, "y": 40, "touches": 59},
                {"player": "B. Al-Ketbi", "position": "LB", "x": 24, "y": 24, "touches": 52},
                {"player": "I. Al-Hammadi", "position": "CDM", "x": 38, "y": 40, "touches": 70},
                {"player": "Y. Ibrahim", "position": "CDM", "x": 38, "y": 60, "touches": 66},
                {"player": "M. Al-Akhbari", "position": "AM", "x": 58, "y": 50, "touches": 54},
                {"player": "K. Al-Blooshi", "position": "RW", "x": 68, "y": 76, "touches": 40},
                {"player": "Fábio Lima", "position": "LW", "x": 68, "y": 24, "touches": 42},
                {"player": "S. Rahimi", "position": "ST", "x": 84, "y": 50, "touches": 32},
            ],
            "combos": [
                ("I. Al-Hammadi", "K. Laba", 12), ("I. Al-Hammadi", "M. Al-Menhali", 11),
                ("I. Al-Hammadi", "Y. Ibrahim", 15), ("Y. Ibrahim", "M. Al-Akhbari", 13),
                ("K. Laba", "M. Al-Menhali", 9), ("K. Laba", "Y. Al-Shamsi", 7),
                ("M. Al-Menhali", "B. Al-Ketbi", 7), ("Y. Ibrahim", "K. Al-Blooshi", 6),
                ("I. Al-Hammadi", "Fábio Lima", 6), ("M. Al-Akhbari", "S. Rahimi", 5),
                ("K. Al-Blooshi", "S. Rahimi", 4), ("Fábio Lima", "S. Rahimi", 4),
                ("K. Eisa", "K. Laba", 9), ("K. Eisa", "M. Al-Menhali", 8),
                ("Y. Al-Shamsi", "K. Al-Blooshi", 5), ("B. Al-Ketbi", "Fábio Lima", 5),
                ("M. Al-Akhbari", "K. Al-Blooshi", 4), ("M. Al-Akhbari", "Fábio Lima", 4),
            ],
        },
        "2025/2026 (Current Season)": {
            "lineup": [
                {"player": "K. Eisa", "position": "GK", "x": 8, "y": 50, "touches": 25},
                {"player": "Y. Al-Shamsi", "position": "RB", "x": 24, "y": 76, "touches": 45},
                {"player": "K. Laba", "position": "CB", "x": 18, "y": 60, "touches": 56},
                {"player": "M. Al-Menhali", "position": "CB", "x": 18, "y": 40, "touches": 53},
                {"player": "B. Al-Ketbi", "position": "LB", "x": 24, "y": 24, "touches": 47},
                {"player": "I. Al-Hammadi", "position": "CDM", "x": 38, "y": 40, "touches": 64},
                {"player": "Y. Ibrahim", "position": "CDM", "x": 38, "y": 60, "touches": 60},
                {"player": "M. Al-Akhbari", "position": "AM", "x": 58, "y": 50, "touches": 48},
                {"player": "K. Al-Blooshi", "position": "RW", "x": 68, "y": 76, "touches": 35},
                {"player": "Fábio Lima", "position": "LW", "x": 68, "y": 24, "touches": 37},
                {"player": "S. Rahimi", "position": "ST", "x": 84, "y": 50, "touches": 29},
            ],
            "combos": [
                ("I. Al-Hammadi", "K. Laba", 10), ("I. Al-Hammadi", "M. Al-Menhali", 9),
                ("I. Al-Hammadi", "Y. Ibrahim", 13), ("Y. Ibrahim", "M. Al-Akhbari", 11),
                ("K. Laba", "M. Al-Menhali", 8), ("K. Laba", "Y. Al-Shamsi", 6),
                ("M. Al-Menhali", "B. Al-Ketbi", 6), ("Y. Ibrahim", "K. Al-Blooshi", 5),
                ("I. Al-Hammadi", "Fábio Lima", 5), ("M. Al-Akhbari", "S. Rahimi", 4),
                ("K. Eisa", "K. Laba", 7), ("K. Eisa", "M. Al-Menhali", 7),
                ("M. Al-Akhbari", "K. Al-Blooshi", 3), ("M. Al-Akhbari", "Fábio Lima", 3),
            ],
        },
    },
}

# --------------------------------------------------------------------------
# CONTROLS
# --------------------------------------------------------------------------
c1, c2, c3 = st.columns([1.2, 1.2, 1.6])
with c1:
    selected_team = st.selectbox("Target Team", list(TEAM_DATA.keys()))
with c2:
    selected_season = st.selectbox("Season", ["2024/2025 (Last Season)", "2025/2026 (Current Season)"])
with c3:
    min_passes = st.slider("Minimum pass-combination threshold", min_value=1, max_value=10, value=3)

heat_toggle = st.toggle(
    "🌡️ Climate Heat Fatigue Toggle — Simulate 38°C+ Summer Fixture",
    value=False,
    help="Shifts outfield players deeper to simulate reduced pressing intensity and a dropped defensive "
         "line under extreme heat conditions.",
)

team_info = TEAM_DATA[selected_team]
season_data = team_info[selected_season]
lineup_df = pd.DataFrame(season_data["lineup"])
combos = season_data["combos"]

# --------------------------------------------------------------------------
# APPLY HEAT FATIGUE ADJUSTMENT
# --------------------------------------------------------------------------
HEAT_DROP = 10  # metres-equivalent drop in average positioning under extreme heat

lineup_df["x_adj"] = lineup_df["x"]
if heat_toggle:
    non_gk_mask = lineup_df["position"] != "GK"
    lineup_df.loc[non_gk_mask, "x_adj"] = (lineup_df.loc[non_gk_mask, "x"] - HEAT_DROP).clip(lower=6)

if heat_toggle:
    st.markdown(
        f"""
        <div class="pfsa-heat-banner">
            🌡️ <strong>High Temperature Mode Active</strong> — {selected_team}'s outfield shape is sitting
            approximately {HEAT_DROP}m deeper than its baseline structure, reflecting reduced pressing
            intensity and a dropped defensive line typical of 38°C+ kickoff conditions.
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------
# KPI ROW
# --------------------------------------------------------------------------
active_edges = [c for c in combos if c[2] >= min_passes]
k1, k2, k3 = st.columns(3)
kpis = [
    ("Total Touches", int(lineup_df["touches"].sum())),
    ("Active Connections", len(active_edges)),
    ("Total Passes (est.)", sum(c[2] for c in combos)),
]
for col, (label, val) in zip([k1, k2, k3], kpis):
    with col:
        st.markdown(
            f'<div class="pfsa-card"><div class="pfsa-metric-value">{val}</div>'
            f'<div class="pfsa-metric-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")

# --------------------------------------------------------------------------
# DRAW THE PASSING NETWORK
# --------------------------------------------------------------------------
def draw_passing_network(lineup: pd.DataFrame, combos: list, threshold: int, team: str, formation: str):
    pitch = Pitch(
        pitch_type="opta",
        pitch_color=PITCH_BG,
        line_color=PITCH_LINE,
        linewidth=1.4,
        line_zorder=1,
    )
    fig, ax = pitch.draw(figsize=(11, 7.2))
    fig.patch.set_facecolor(PITCH_BG)
    ax.set_facecolor(PITCH_BG)

    pos_lookup = lineup.set_index("player")[["x_adj", "y", "touches"]]

    # --- Glowing edges (drawn first, beneath nodes) ---
    edges = [c for c in combos if c[2] >= threshold]
    if edges:
        max_p = max(c[2] for c in edges)
        for player_a, player_b, passes in edges:
            xa, ya = pos_lookup.loc[player_a, ["x_adj", "y"]]
            xb, yb = pos_lookup.loc[player_b, ["x_adj", "y"]]
            base_lw = 0.6 + 5.0 * (passes / max_p)

            # glow layers: wide + faint, then narrow + solid
            pitch.lines(xa, ya, xb, yb, lw=base_lw + 5, color=ACCENT_TEAL, alpha=0.10, zorder=2, ax=ax)
            pitch.lines(xa, ya, xb, yb, lw=base_lw + 2.5, color=ACCENT_TEAL, alpha=0.20, zorder=2, ax=ax)
            pitch.lines(xa, ya, xb, yb, lw=base_lw, color=ACCENT_TEAL, alpha=0.75, zorder=2, ax=ax)

    # --- Nodes (Sky Blue circles scaled by touches) ---
    max_touches = lineup["touches"].max()
    sizes = 260 + 1500 * (lineup["touches"] / max_touches)
    pitch.scatter(
        lineup["x_adj"], lineup["y"],
        s=sizes,
        color=SECONDARY_BG,
        edgecolors=ACCENT_BLUE,
        linewidth=2.4,
        alpha=0.95,
        zorder=3,
        ax=ax,
    )

    for _, row in lineup.iterrows():
        pitch.annotate(
            row["player"].split()[-1],
            xy=(row["x_adj"], row["y"]),
            c="#f0f6fc",
            va="center", ha="center",
            fontsize=8.5, fontweight="bold",
            zorder=4, ax=ax,
        )

    heat_tag = " · 🌡️ Heat Fatigue Mode" if lineup["x_adj"].ne(lineup["x"]).any() else ""
    ax.set_title(
        f"{team} — Passing Network ({formation}){heat_tag}",
        color="#f0f6fc", fontsize=15, fontweight="bold", pad=14,
    )
    fig.text(
        0.5, 0.02,
        f"Node size = touches · Glowing teal edges = pass frequency (≥ {threshold} passes)",
        color="#9fb3c8", ha="center", fontsize=9,
    )
    return fig


fig = draw_passing_network(lineup_df, combos, min_passes, selected_team, team_info["formation"])
st.pyplot(fig, use_container_width=True)

with st.expander("📋 View underlying touch &amp; combination data"):
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("**Player Touches**")
        st.dataframe(lineup_df[["player", "position", "touches"]].sort_values("touches", ascending=False),
                     use_container_width=True, hide_index=True)
    with t2:
        st.markdown(f"**Active Pass Combinations (≥ {min_passes})**")
        combo_df = pd.DataFrame(active_edges, columns=["Player A", "Player B", "Passes"]).sort_values(
            "Passes", ascending=False)
        st.dataframe(combo_df, use_container_width=True, hide_index=True)
