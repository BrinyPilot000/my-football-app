"""
10_🛡️_Team_Profiles.py
--------------------------
Single-club deep dive: tactical system overview, squad age distribution
(histogram), and seasonal form trend, built on synthetic club data.
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Team Profiles", page_icon="🛡️", layout="wide")

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
        .pfsa-system-box {{
            background: rgba(135, 206, 235, 0.06); border-left: 3px solid {ACCENT_BLUE};
            border-radius: 8px; padding: 1rem 1.2rem; color: #d5e2ee; font-size: 0.92rem; line-height: 1.5;
        }}
        .pfsa-form-win {{ background: {ACCENT_TEAL}; }}
        .pfsa-form-draw {{ background: #6b7684; }}
        .pfsa-form-loss {{ background: #ff6b6b; }}
        .pfsa-form-pill {{
            display:inline-block; width:1.7rem; height:1.7rem; border-radius:50%;
            color:#0d1117; font-weight:700; text-align:center; line-height:1.7rem;
            font-size:0.8rem; margin-right:0.35rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>🛡️ Team Profiles — Club Deep Dive</h1>
        <p>Tactical system, squad age curve &amp; seasonal form trend (synthetic club dataset)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

CLUBS = {
    "Coventry City": {
        "system": "4-2-3-1",
        "manager": "F. Lampard",
        "style_summary": (
            "Coventry set up in a flexible 4-2-3-1 that morphs into a 3-2-5 in possession, "
            "with the double pivot rotating to create passing lanes through the half-spaces. "
            "Out of possession, the side presses in a mid-block, using the wide forwards to "
            "trigger pressure and force play down the touchline."
        ),
    },
    "Leeds United": {
        "system": "4-3-3",
        "manager": "D. Farke",
        "style_summary": (
            "Leeds build patiently through a back three in possession, with full-backs inverting "
            "into midfield to overload central zones. High defensive line supported by aggressive "
            "counter-press within 5 seconds of losing the ball."
        ),
    },
    "West Brom": {
        "system": "4-4-2",
        "manager": "C. Corberán",
        "style_summary": (
            "A compact mid-block 4-4-2 that prioritises defensive solidity and transitions through "
            "direct forward passing to two mobile strikers."
        ),
    },
}

selected_club = st.selectbox("Select club", list(CLUBS.keys()))
club = CLUBS[selected_club]


@st.cache_data
def generate_club_data(club_name: str, seed_offset: int = 0):
    seed = (hash(club_name) % 10000) + seed_offset
    rng = np.random.default_rng(seed)

    # Squad ages
    ages = np.clip(rng.normal(25.5, 4.2, size=26), 17, 36).astype(int)

    # Seasonal form (last 15 matches): W / D / L
    form = rng.choice(["W", "D", "L"], size=15, p=[0.42, 0.28, 0.30])

    # Points progression across the season (38 games)
    match_points = np.where(
        rng.random(38) < 0.42, 3, np.where(rng.random(38) < 0.6, 1, 0)
    )
    cumulative_points = np.cumsum(match_points)

    return ages, form, cumulative_points


ages, form, cumulative_points = generate_club_data(selected_club)

# --------------------------------------------------------------------------
# SYSTEM OVERVIEW
# --------------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
kpis = [
    ("Formation", club["system"]),
    ("Manager", club["manager"]),
    ("Avg. Squad Age", f"{ages.mean():.1f}"),
    ("Current Points", int(cumulative_points[-1])),
]
for col, (label, val) in zip([k1, k2, k3, k4], kpis):
    with col:
        st.markdown(
            f'<div class="pfsa-card"><div class="pfsa-metric-value">{val}</div>'
            f'<div class="pfsa-metric-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")
st.subheader("Tactical System")
st.markdown(f'<div class="pfsa-system-box">{club["style_summary"]}</div>', unsafe_allow_html=True)

st.write("")

# --------------------------------------------------------------------------
# FORM STRIP
# --------------------------------------------------------------------------
st.subheader("Last 15 Matches — Form Trend")
form_class = {"W": "pfsa-form-win", "D": "pfsa-form-draw", "L": "pfsa-form-loss"}
form_html = "".join(f'<span class="pfsa-form-pill {form_class[r]}">{r}</span>' for r in form)
st.markdown(form_html, unsafe_allow_html=True)

st.write("")
chart_col1, chart_col2 = st.columns(2)

# --------------------------------------------------------------------------
# AGE HISTOGRAM
# --------------------------------------------------------------------------
with chart_col1:
    st.subheader("Squad Age Distribution")
    fig1, ax1 = plt.subplots(figsize=(6, 5))
    fig1.patch.set_facecolor(PRIMARY_BG)
    ax1.set_facecolor(PRIMARY_BG)

    ax1.hist(ages, bins=range(int(ages.min()), int(ages.max()) + 2), color=ACCENT_BLUE,
              alpha=0.85, edgecolor=PRIMARY_BG)
    ax1.axvline(ages.mean(), color=ACCENT_TEAL, linestyle="--", linewidth=1.6,
                 label=f"Mean age: {ages.mean():.1f}")

    ax1.set_xlabel("Age", color="#9fb3c8")
    ax1.set_ylabel("Number of Players", color="#9fb3c8")
    ax1.tick_params(colors="#9fb3c8")
    for spine in ax1.spines.values():
        spine.set_color("#2a3542")
    ax1.grid(axis="y", alpha=0.15, color="#3a4552")
    ax1.legend(facecolor=SECONDARY_BG, edgecolor="#2a3542", labelcolor="#e6edf3", fontsize=8)

    st.pyplot(fig1, use_container_width=True)

# --------------------------------------------------------------------------
# SEASONAL FORM (CUMULATIVE POINTS)
# --------------------------------------------------------------------------
with chart_col2:
    st.subheader("Seasonal Points Progression")
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    fig2.patch.set_facecolor(PRIMARY_BG)
    ax2.set_facecolor(PRIMARY_BG)

    matches = np.arange(1, len(cumulative_points) + 1)
    ax2.plot(matches, cumulative_points, color=ACCENT_TEAL, linewidth=2.2)
    ax2.fill_between(matches, cumulative_points, color=ACCENT_TEAL, alpha=0.12)

    ax2.set_xlabel("Matchday", color="#9fb3c8")
    ax2.set_ylabel("Cumulative Points", color="#9fb3c8")
    ax2.tick_params(colors="#9fb3c8")
    for spine in ax2.spines.values():
        spine.set_color("#2a3542")
    ax2.grid(alpha=0.15, color="#3a4552")

    st.pyplot(fig2, use_container_width=True)

with st.expander("📋 View squad age data"):
    age_df = pd.DataFrame({"Player #": range(1, len(ages) + 1), "Age": ages}).sort_values("Age")
    st.dataframe(age_df, use_container_width=True, hide_index=True)
