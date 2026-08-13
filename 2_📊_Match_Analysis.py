"""
2_📊_Match_Analysis.py
-----------------------
Coventry City passing network: node size = touch volume,
edge width = pass-combination frequency (min threshold = 3 passes).
Includes a PNG export/download feature.

NOTE: This conversation began fresh, so there was no earlier passing-network
code to re-use. This page reconstructs that functionality from scratch using
a synthetic (but structurally realistic) Coventry City event dataset.
"""

import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from mplsoccer import Pitch

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(page_title="Match Analysis | Passing Network", page_icon="📊", layout="wide")

PRIMARY_BG = "#0d1117"
SECONDARY_BG = "#161b22"
ACCENT_BLUE = "#87CEEB"
ACCENT_TEAL = "#00F2FE"
PITCH_BG = "#0d1117"
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
        div.stButton > button, div.stDownloadButton > button {{
            background: linear-gradient(90deg, {ACCENT_BLUE}, {ACCENT_TEAL});
            color: #0d1117; font-weight: 700; border: none; border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>📊 Match Analysis — Passing Network</h1>
        <p>Coventry City FC · Node size = touch volume · Edge width = combination frequency (min. 3 passes)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# SYNTHETIC EVENT DATA GENERATION
# --------------------------------------------------------------------------
@st.cache_data
def generate_match_data(seed: int = 42):
    """Builds a synthetic Coventry City starting XI with average positions,
    touch counts, and a pass-combination matrix."""
    rng = np.random.default_rng(seed)

    # Starting XI in a 4-3-3, average (x, y) positions on a 100x100 pitch
    lineup = pd.DataFrame(
        [
            {"player": "B. Hamer", "position": "GK", "x": 6, "y": 40},
            {"player": "J. Bidwell", "position": "LB", "x": 22, "y": 12},
            {"player": "L. Kyriakou", "position": "CB", "x": 18, "y": 32},
            {"player": "B. Sakamoto", "position": "CB", "x": 18, "y": 48},
            {"player": "J. Latibeaudiere", "position": "RB", "x": 22, "y": 68},
            {"player": "J. Allen", "position": "CDM", "x": 38, "y": 40},
            {"player": "E. Godden", "position": "CM", "x": 48, "y": 26},
            {"player": "T. Kelly", "position": "CM", "x": 48, "y": 54},
            {"player": "T. Wright", "position": "LW", "x": 68, "y": 14},
            {"player": "H. Sinclair", "position": "ST", "x": 78, "y": 40},
            {"player": "E. Ogbene", "position": "RW", "x": 68, "y": 66},
        ]
    )

    # Touches: higher volume for midfielders/build-up players
    base_touches = {
        "GK": 32, "CB": 58, "LB": 46, "RB": 46, "CDM": 72, "CM": 66, "LW": 34, "RW": 34, "ST": 28,
    }
    lineup["touches"] = lineup["position"].map(base_touches) + rng.integers(-6, 8, size=len(lineup))

    # Build a plausible pass-combination matrix weighted by pitch proximity
    players = lineup["player"].tolist()
    n = len(players)
    coords = lineup[["x", "y"]].to_numpy()
    dist = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=-1)
    proximity_weight = np.clip(45 - dist, 1, None)

    combo_counts = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            lam = proximity_weight[i, j] * 0.28
            combo_counts[i, j] = rng.poisson(lam)

    pass_records = []
    for i in range(n):
        for j in range(i + 1, n):
            total = combo_counts[i, j] + combo_counts[j, i]
            if total > 0:
                pass_records.append({"player_a": players[i], "player_b": players[j], "passes": total})

    combos = pd.DataFrame(pass_records)
    return lineup, combos


lineup_df, combos_df = generate_match_data()

# --------------------------------------------------------------------------
# CONTROLS
# --------------------------------------------------------------------------
ctrl_col, meta_col1, meta_col2, meta_col3 = st.columns([2, 1, 1, 1])
with ctrl_col:
    min_passes = st.slider("Minimum pass-combination threshold", min_value=1, max_value=10, value=3)
with meta_col1:
    st.markdown(
        f'<div class="pfsa-card"><div class="pfsa-metric-value">{int(lineup_df["touches"].sum())}</div>'
        f'<div class="pfsa-metric-label">Total Touches</div></div>',
        unsafe_allow_html=True,
    )
with meta_col2:
    active_edges = combos_df[combos_df["passes"] >= min_passes]
    st.markdown(
        f'<div class="pfsa-card"><div class="pfsa-metric-value">{len(active_edges)}</div>'
        f'<div class="pfsa-metric-label">Active Connections</div></div>',
        unsafe_allow_html=True,
    )
with meta_col3:
    st.markdown(
        f'<div class="pfsa-card"><div class="pfsa-metric-value">{int(combos_df["passes"].sum())}</div>'
        f'<div class="pfsa-metric-label">Total Passes (est.)</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# --------------------------------------------------------------------------
# DRAW THE PASSING NETWORK
# --------------------------------------------------------------------------
def draw_passing_network(lineup: pd.DataFrame, combos: pd.DataFrame, threshold: int):
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

    pos_lookup = lineup.set_index("player")[["x", "y", "touches"]]

    # --- Edges (drawn first, beneath nodes) ---
    edges = combos[combos["passes"] >= threshold]
    if not edges.empty:
        max_p = edges["passes"].max()
        for _, row in edges.iterrows():
            xa, ya = pos_lookup.loc[row["player_a"], ["x", "y"]]
            xb, yb = pos_lookup.loc[row["player_b"], ["x", "y"]]
            lw = 0.6 + 5.5 * (row["passes"] / max_p)
            pitch.lines(
                xa, ya, xb, yb,
                lw=lw,
                color=ACCENT_TEAL,
                alpha=0.55,
                zorder=2,
                ax=ax,
            )

    # --- Nodes ---
    max_touches = lineup["touches"].max()
    sizes = 260 + 1500 * (lineup["touches"] / max_touches)
    pitch.scatter(
        lineup["x"], lineup["y"],
        s=sizes,
        color=SECONDARY_BG,
        edgecolors=ACCENT_BLUE,
        linewidth=2.2,
        alpha=0.95,
        zorder=3,
        ax=ax,
    )

    for _, row in lineup.iterrows():
        pitch.annotate(
            row["player"].split()[-1],
            xy=(row["x"], row["y"]),
            c="#f0f6fc",
            va="center", ha="center",
            fontsize=9, fontweight="bold",
            zorder=4, ax=ax,
        )

    ax.set_title(
        "Coventry City FC — Passing Network",
        color="#f0f6fc", fontsize=15, fontweight="bold", pad=14,
    )
    fig.text(
        0.5, 0.02,
        f"Node size = touches · Edge width = pass frequency (≥ {threshold} passes)",
        color="#9fb3c8", ha="center", fontsize=9,
    )
    return fig


fig = draw_passing_network(lineup_df, combos_df, min_passes)
st.pyplot(fig, use_container_width=True)

# --------------------------------------------------------------------------
# PNG DOWNLOAD
# --------------------------------------------------------------------------
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=250, facecolor=fig.get_facecolor(), bbox_inches="tight")
buf.seek(0)

dl_col, _ = st.columns([1, 3])
with dl_col:
    st.download_button(
        label="⬇️ Download Passing Network (PNG)",
        data=buf,
        file_name="coventry_city_passing_network.png",
        mime="image/png",
        use_container_width=True,
    )

with st.expander("📋 View underlying touch &amp; combination data"):
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("**Player Touches**")
        st.dataframe(lineup_df[["player", "position", "touches"]].sort_values("touches", ascending=False),
                     use_container_width=True, hide_index=True)
    with t2:
        st.markdown(f"**Active Pass Combinations (≥ {min_passes})**")
        st.dataframe(active_edges.sort_values("passes", ascending=False),
                     use_container_width=True, hide_index=True)
