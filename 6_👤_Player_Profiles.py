"""
6_👤_Player_Profiles.py
--------------------------
Biographical scouting template: player attributes, strengths, weaknesses,
and a PFSA-style role description box.
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Player Profiles", page_icon="👤", layout="wide")

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
        .pfsa-profile-card {{
            background-color: {SECONDARY_BG}; border: 1px solid rgba(135, 206, 235, 0.2);
            border-radius: 16px; padding: 1.4rem 1.6rem;
        }}
        .pfsa-tag {{
            display: inline-block; padding: 0.2rem 0.65rem; border-radius: 999px;
            background: rgba(135, 206, 235, 0.12); border: 1px solid rgba(135, 206, 235, 0.4);
            color: {ACCENT_BLUE}; font-size: 0.72rem; margin: 0.15rem 0.25rem 0.15rem 0;
        }}
        .pfsa-strength {{ color: {ACCENT_TEAL}; }}
        .pfsa-weakness {{ color: #ff8b8b; }}
        .pfsa-role-box {{
            background: rgba(0, 242, 254, 0.06); border-left: 3px solid {ACCENT_TEAL};
            border-radius: 8px; padding: 1rem 1.2rem; margin-top: 0.8rem;
            color: #d5e2ee; font-size: 0.92rem; line-height: 1.5;
        }}
        .pfsa-attr-label {{ color: #9fb3c8; font-size: 0.8rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>👤 Player Profiles — Scouting Template</h1>
        <p>Biographical &amp; technical scouting card with role fit assessment (synthetic profile data)</p>
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def generate_profiles(seed: int = 5):
    rng = np.random.default_rng(seed)
    profiles = [
        {"player": "H. Sinclair", "position": "Striker", "age": 24, "nationality": "England",
         "foot": "Right", "height_cm": 183, "club": "Coventry City", "value_gbp": "£4.2M",
         "strengths": ["Movement in behind", "Aerial threat", "Clinical finishing", "Hold-up play"],
         "weaknesses": ["Link-up under pressure", "Off-ball pressing intensity"],
         "role": "Primary out-ball in transition; occupies the last line to stretch defences and "
                 "attacks crosses with strong aerial timing. Best deployed as a lone #9 in a mid-block "
                 "system where he can exploit space in behind."},
        {"player": "T. Wright", "position": "Winger", "age": 22, "nationality": "England",
         "foot": "Left", "height_cm": 176, "club": "Coventry City", "value_gbp": "£3.1M",
         "strengths": ["1v1 dribbling", "Cutting inside to shoot", "Acceleration"],
         "weaknesses": ["End product consistency", "Defensive tracking"],
         "role": "Inverted wide forward who thrives cutting onto his stronger foot. Fits a possession-based "
                 "system with underlapping full-back support and licence to roam centrally."},
        {"player": "J. Allen", "position": "Defensive Midfielder", "age": 27, "nationality": "Wales",
         "foot": "Right", "height_cm": 180, "club": "Coventry City", "value_gbp": "£2.6M",
         "strengths": ["Tempo control", "Positional discipline", "Progressive passing range"],
         "weaknesses": ["Recovery pace vs. transitions", "Aerial duels"],
         "role": "Deep-lying pivot who dictates rhythm from base of midfield. Best suited to a double-pivot "
                 "or single #6 role in a possession-dominant build-up structure."},
        {"player": "L. Kyriakou", "position": "Centre-Back", "age": 25, "nationality": "Cyprus",
         "foot": "Left", "height_cm": 188, "club": "Coventry City", "value_gbp": "£3.8M",
         "strengths": ["Aerial dominance", "Front-foot defending", "Composure in build-up"],
         "weaknesses": ["Recovery speed 1v1", "Occasional rash challenges"],
         "role": "Left-sided centre-back for a back three or four, comfortable stepping into midfield to "
                 "press and confident carrying the ball out from deep."},
    ]
    return profiles


profiles = generate_profiles()
names = [p["player"] for p in profiles]

selected_name = st.selectbox("Select a player profile", names)
profile = next(p for p in profiles if p["player"] == selected_name)

left, right = st.columns([1, 1.6])

with left:
    st.markdown(
        f"""
        <div class="pfsa-profile-card">
            <h2 style="margin-bottom:0.1rem;">{profile['player']}</h2>
            <p style="color:{ACCENT_BLUE}; margin-top:0; font-weight:600;">{profile['position']} · {profile['club']}</p>
            <div style="margin: 0.6rem 0;">
                <span class="pfsa-tag">🎂 Age {profile['age']}</span>
                <span class="pfsa-tag">🌍 {profile['nationality']}</span>
                <span class="pfsa-tag">🦶 {profile['foot']}-footed</span>
                <span class="pfsa-tag">📏 {profile['height_cm']} cm</span>
                <span class="pfsa-tag">💰 Est. {profile['value_gbp']}</span>
            </div>
            <hr style="border-color:#2a3542;">
            <p class="pfsa-attr-label">STRENGTHS</p>
            <ul>
                {''.join(f'<li class="pfsa-strength">{s}</li>' for s in profile['strengths'])}
            </ul>
            <p class="pfsa-attr-label">AREAS TO DEVELOP</p>
            <ul>
                {''.join(f'<li class="pfsa-weakness">{w}</li>' for w in profile['weaknesses'])}
            </ul>
            <p class="pfsa-attr-label">ROLE DESCRIPTION</p>
            <div class="pfsa-role-box">{profile['role']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.subheader("Attribute Radar Snapshot")
    rng = np.random.default_rng(hash(profile["player"]) % (2**31))
    attrs = ["Pace", "Finishing", "Passing", "Dribbling", "Defending", "Physicality", "Vision", "Work Rate"]
    values = np.clip(rng.normal(65, 15, size=len(attrs)), 20, 98)

    angles = np.linspace(0, 2 * np.pi, len(attrs), endpoint=False).tolist()
    values_closed = np.concatenate([values, [values[0]]])
    angles_closed = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(6.5, 6.5), subplot_kw={"projection": "polar"})
    fig.patch.set_facecolor(PRIMARY_BG)
    ax.set_facecolor(PRIMARY_BG)

    ax.plot(angles_closed, values_closed, color=ACCENT_TEAL, linewidth=2.2)
    ax.fill(angles_closed, values_closed, color=ACCENT_TEAL, alpha=0.22)
    ax.set_ylim(0, 100)
    ax.set_xticks(angles)
    ax.set_xticklabels(attrs, color="#e6edf3", fontsize=9)
    ax.set_yticklabels([])
    ax.spines["polar"].set_visible(False)
    ax.grid(color="#2a3542", alpha=0.45)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    st.pyplot(fig, use_container_width=True)

    st.subheader("Season Summary (synthetic)")
    season_stats = pd.DataFrame(
        {
            "Metric": ["Appearances", "Minutes Played", "Goals", "Assists", "Avg. Rating"],
            "Value": [
                int(rng.integers(20, 42)),
                int(rng.integers(1400, 3600)),
                int(rng.integers(0, 18)),
                int(rng.integers(0, 12)),
                round(float(rng.uniform(6.4, 7.8)), 2),
            ],
        }
    )
    st.dataframe(season_stats, use_container_width=True, hide_index=True)
