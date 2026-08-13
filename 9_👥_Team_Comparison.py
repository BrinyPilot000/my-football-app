"""
9_👥_Team_Comparison.py
--------------------------
Side-by-side squad comparison board with interactive sliders visualising
tactical style dimensions (Pressing Intensity, Build-up Speed, Directness, etc.)
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Team Comparison", page_icon="👥", layout="wide")

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
        .pfsa-team-card {{
            background-color: {SECONDARY_BG}; border: 1px solid rgba(135, 206, 235, 0.18);
            border-radius: 14px; padding: 1.1rem 1.3rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>👥 Team Comparison — Tactical Style Board</h1>
        <p>Interactive squad-vs-squad comparison across core tactical style dimensions</p>
    </div>
    """,
    unsafe_allow_html=True,
)

TEAMS = ["Coventry City", "Leeds United", "West Brom", "Sunderland", "Middlesbrough", "Norwich City"]
DIMENSIONS = ["Pressing Intensity", "Build-up Speed", "Directness", "Width", "Possession Share", "Defensive Line Height"]


@st.cache_data
def generate_team_styles(seed: int = 14):
    rng = np.random.default_rng(seed)
    data = {}
    for team in TEAMS:
        data[team] = {dim: int(rng.integers(25, 96)) for dim in DIMENSIONS}
    return data


team_styles = generate_team_styles()

c1, c2 = st.columns(2)
with c1:
    team_a = st.selectbox("Team A", TEAMS, index=0)
with c2:
    team_b = st.selectbox("Team B", TEAMS, index=1)

st.subheader("Adjust Tactical Style Sliders")
st.caption("Defaults are drawn from the synthetic season model — override to run 'what-if' tactical scenarios.")

col_a, col_b = st.columns(2)
values_a, values_b = {}, {}

with col_a:
    st.markdown(f"##### 🔵 {team_a}")
    for dim in DIMENSIONS:
        values_a[dim] = st.slider(f"{dim} — {team_a}", 0, 100, team_styles[team_a][dim], key=f"a_{dim}")

with col_b:
    st.markdown(f"##### 🟢 {team_b}")
    for dim in DIMENSIONS:
        values_b[dim] = st.slider(f"{dim} — {team_b}", 0, 100, team_styles[team_b][dim], key=f"b_{dim}")

st.write("")
st.subheader("Tactical Style Comparison")

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(PRIMARY_BG)
ax.set_facecolor(PRIMARY_BG)

y_pos = np.arange(len(DIMENSIONS))
bar_h = 0.35

ax.barh(y_pos + bar_h / 2, [values_a[d] for d in DIMENSIONS], height=bar_h, color=ACCENT_BLUE, alpha=0.88, label=team_a)
ax.barh(y_pos - bar_h / 2, [values_b[d] for d in DIMENSIONS], height=bar_h, color=ACCENT_TEAL, alpha=0.88, label=team_b)

ax.set_yticks(y_pos)
ax.set_yticklabels(DIMENSIONS, color="#e6edf3")
ax.set_xlim(0, 100)
ax.set_xlabel("Style Index (0–100)", color="#9fb3c8")
ax.tick_params(colors="#9fb3c8")
for spine in ax.spines.values():
    spine.set_color("#2a3542")
ax.grid(axis="x", alpha=0.15, color="#3a4552")
ax.legend(facecolor=SECONDARY_BG, edgecolor="#2a3542", labelcolor="#e6edf3", fontsize=9)
ax.invert_yaxis()

st.pyplot(fig, use_container_width=True)

st.write("")
st.subheader("Squad Snapshot")

s1, s2 = st.columns(2)
for col, team, values in [(s1, team_a, values_a), (s2, team_b, values_b)]:
    with col:
        dominant_trait = max(values, key=values.get)
        st.markdown(
            f"""
            <div class="pfsa-team-card">
                <h4>{team}</h4>
                <p style="color:#9fb3c8; font-size:0.88rem;">
                    Dominant tactical trait: <strong style="color:{ACCENT_TEAL};">{dominant_trait}</strong>
                    ({values[dominant_trait]}/100)
                </p>
                <p style="color:#9fb3c8; font-size:0.88rem;">
                    Average style index: <strong style="color:#e6edf3;">{np.mean(list(values.values())):.1f}</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with st.expander("📋 View comparison table"):
    table = pd.DataFrame({"Dimension": DIMENSIONS, team_a: [values_a[d] for d in DIMENSIONS],
                           team_b: [values_b[d] for d in DIMENSIONS]})
    table["Gap"] = table[team_a] - table[team_b]
    st.dataframe(table, use_container_width=True, hide_index=True)
