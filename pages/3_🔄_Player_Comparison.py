"""
3_🔄_Player_Comparison.py
---------------------------
Side-by-side polar radar comparison for Saudi Pro League & UAE Pro League
midfielders/attackers across five core tactical traits.

Dataset is a hardcoded, illustrative mock dataset for portfolio
demonstration purposes only — it does not represent real percentile data.
"""

import numpy as np
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
        .pfsa-player-card {{
            background-color: {SECONDARY_BG}; border: 1px solid rgba(135, 206, 235, 0.18);
            border-radius: 12px; padding: 0.9rem 1.1rem; text-align: center; margin-bottom: 0.8rem;
        }}
        table.pfsa-compare-table {{
            width: 100%; border-collapse: collapse; margin-top: 0.8rem; font-size: 0.92rem;
        }}
        table.pfsa-compare-table th {{
            background-color: {SECONDARY_BG}; color: {ACCENT_BLUE}; text-align: left;
            padding: 0.6rem 0.8rem; border-bottom: 2px solid rgba(135, 206, 235, 0.3);
        }}
        table.pfsa-compare-table td {{
            padding: 0.55rem 0.8rem; border-bottom: 1px solid rgba(135, 206, 235, 0.12); color: #e6edf3;
        }}
        table.pfsa-compare-table tr:nth-child(even) {{ background-color: rgba(135, 206, 235, 0.03); }}
        .pfsa-winner {{ color: {ACCENT_TEAL}; font-weight: 700; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>🔄 Player Comparison — Tactical Radar</h1>
        <p>Head-to-head comparison of Saudi Pro League &amp; UAE Pro League midfielders and attackers
        across five core tactical traits</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "⚠️ Trait scores below are illustrative mock percentile values built for portfolio demonstration "
    "purposes and do not represent real performance data."
)

# --------------------------------------------------------------------------
# HARDCODED PLAYER PROFILE MATRIX
# --------------------------------------------------------------------------
TRAITS = ["Passing Accuracy", "Progressive Carries", "Defensive Interceptions",
          "Key Chance Creation", "Press Resistance"]

PLAYER_PROFILES = {
    "Rúben Neves": {
        "club": "Al-Hilal", "league": "Saudi Pro League", "position": "CDM",
        "traits": {"Passing Accuracy": 92, "Progressive Carries": 74, "Defensive Interceptions": 68,
                   "Key Chance Creation": 62, "Press Resistance": 88},
    },
    "Sergej Milinković-Savić": {
        "club": "Al-Hilal", "league": "Saudi Pro League", "position": "CM / AM",
        "traits": {"Passing Accuracy": 85, "Progressive Carries": 78, "Defensive Interceptions": 58,
                   "Key Chance Creation": 80, "Press Resistance": 82},
    },
    "Kaku": {
        "club": "Al-Wasl", "league": "UAE Pro League", "position": "AM",
        "traits": {"Passing Accuracy": 81, "Progressive Carries": 70, "Defensive Interceptions": 40,
                   "Key Chance Creation": 88, "Press Resistance": 65},
    },
    "N'Golo Kanté": {
        "club": "Al-Ittihad", "league": "Saudi Pro League", "position": "CDM",
        "traits": {"Passing Accuracy": 87, "Progressive Carries": 60, "Defensive Interceptions": 91,
                   "Key Chance Creation": 48, "Press Resistance": 90},
    },
}

PLAYER_NAMES = list(PLAYER_PROFILES.keys())

# --------------------------------------------------------------------------
# SIDE-BY-SIDE SELECTORS
# --------------------------------------------------------------------------
c1, c2 = st.columns(2)
with c1:
    player_alpha = st.selectbox("Player Alpha", PLAYER_NAMES, index=0)
with c2:
    default_beta_idx = 3 if len(PLAYER_NAMES) > 3 else (1 if len(PLAYER_NAMES) > 1 else 0)
    player_beta = st.selectbox("Player Beta", PLAYER_NAMES, index=default_beta_idx)

profile_a = PLAYER_PROFILES[player_alpha]
profile_b = PLAYER_PROFILES[player_beta]

card_col1, card_col2 = st.columns(2)
with card_col1:
    st.markdown(
        f"""
        <div class="pfsa-player-card">
            <strong style="color:{ACCENT_BLUE}; font-size:1.05rem;">{player_alpha}</strong><br>
            <span style="color:#9fb3c8; font-size:0.85rem;">{profile_a['position']} · {profile_a['club']}
            ({profile_a['league']})</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with card_col2:
    st.markdown(
        f"""
        <div class="pfsa-player-card">
            <strong style="color:{ACCENT_TEAL}; font-size:1.05rem;">{player_beta}</strong><br>
            <span style="color:#9fb3c8; font-size:0.85rem;">{profile_b['position']} · {profile_b['club']}
            ({profile_b['league']})</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------
# POLAR RADAR CHART
# --------------------------------------------------------------------------
values_a = [profile_a["traits"][t] for t in TRAITS]
values_b = [profile_b["traits"][t] for t in TRAITS]

angles = np.linspace(0, 2 * np.pi, len(TRAITS), endpoint=False).tolist()
values_a_closed = values_a + [values_a[0]]
values_b_closed = values_b + [values_b[0]]
angles_closed = angles + [angles[0]]

fig, ax = plt.subplots(figsize=(8.5, 8.5), subplot_kw={"projection": "polar"})
fig.patch.set_facecolor(PRIMARY_BG)
ax.set_facecolor(PRIMARY_BG)

ax.plot(angles_closed, values_a_closed, color=ACCENT_BLUE, linewidth=2.4, label=player_alpha)
ax.fill(angles_closed, values_a_closed, color=ACCENT_BLUE, alpha=0.18)

ax.plot(angles_closed, values_b_closed, color=ACCENT_TEAL, linewidth=2.4, label=player_beta)
ax.fill(angles_closed, values_b_closed, color=ACCENT_TEAL, alpha=0.18)

ax.set_ylim(0, 100)
ax.set_xticks(angles)
ax.set_xticklabels(TRAITS, color="#e6edf3", fontsize=10)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"], color="#6b7684", fontsize=7)
ax.spines["polar"].set_visible(False)
ax.grid(color="#2a3542", alpha=0.45)
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.12), facecolor=SECONDARY_BG,
          edgecolor="#2a3542", labelcolor="#e6edf3", fontsize=10)
ax.set_title(f"{player_alpha} vs. {player_beta}", color="#f0f6fc", fontsize=14, fontweight="bold", pad=24)

st.pyplot(fig, use_container_width=True)

# --------------------------------------------------------------------------
# COMPARISON TABLE — WINNER HIGHLIGHTED IN NEON TEAL
# --------------------------------------------------------------------------
st.subheader("Metric-by-Metric Breakdown")

table_rows = []
for trait in TRAITS:
    val_a = profile_a["traits"][trait]
    val_b = profile_b["traits"][trait]

    if val_a > val_b:
        cell_a = f'<span class="pfsa-winner">{val_a}</span>'
        cell_b = f"{val_b}"
    elif val_b > val_a:
        cell_a = f"{val_a}"
        cell_b = f'<span class="pfsa-winner">{val_b}</span>'
    else:
        cell_a = f"{val_a}"
        cell_b = f"{val_b}"

    table_rows.append(f"<tr><td>{trait}</td><td>{cell_a}</td><td>{cell_b}</td></tr>")

table_html = f"""
<table class="pfsa-compare-table">
    <thead>
        <tr>
            <th>Tactical Trait</th>
            <th>{player_alpha}</th>
            <th>{player_beta}</th>
        </tr>
    </thead>
    <tbody>
        {''.join(table_rows)}
    </tbody>
</table>
"""

st.markdown(table_html, unsafe_allow_html=True)

wins_a = sum(1 for t in TRAITS if profile_a["traits"][t] > profile_b["traits"][t])
wins_b = sum(1 for t in TRAITS if profile_b["traits"][t] > profile_a["traits"][t])

st.write("")
summary_col1, summary_col2, summary_col3 = st.columns(3)
with summary_col1:
    st.markdown(
        f'<div class="pfsa-player-card"><div style="color:{ACCENT_BLUE}; font-size:1.4rem; font-weight:700;">'
        f'{wins_a}</div><div style="color:#9fb3c8; font-size:0.78rem; text-transform:uppercase;">'
        f'{player_alpha} — Traits Won</div></div>',
        unsafe_allow_html=True,
    )
with summary_col2:
    st.markdown(
        f'<div class="pfsa-player-card"><div style="color:#9fb3c8; font-size:1.4rem; font-weight:700;">'
        f'{len(TRAITS) - wins_a - wins_b}</div><div style="color:#9fb3c8; font-size:0.78rem; '
        f'text-transform:uppercase;">Traits Tied</div></div>',
        unsafe_allow_html=True,
    )
with summary_col3:
    st.markdown(
        f'<div class="pfsa-player-card"><div style="color:{ACCENT_TEAL}; font-size:1.4rem; font-weight:700;">'
        f'{wins_b}</div><div style="color:#9fb3c8; font-size:0.78rem; text-transform:uppercase;">'
        f'{player_beta} — Traits Won</div></div>',
        unsafe_allow_html=True,
    )
