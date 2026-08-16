"""
1_🎯_Finishing_Dashboards.py
------------------------------
Finishing output dashboard for Saudi Pro League & UAE Pro League forwards.
Dataset is a hardcoded, illustrative mock dataset for portfolio demonstration
purposes only — it does not represent real statistical records.
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Finishing Dashboards", page_icon="🎯", layout="wide")

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
            border-radius: 12px; padding: 1rem 1.2rem; text-align: center; transition: 0.2s ease-in-out;
        }}
        .pfsa-card:hover {{ border-color: {ACCENT_TEAL}; box-shadow: 0 0 20px rgba(0, 242, 254, 0.12); }}
        .pfsa-metric-value {{ font-size: 1.6rem; font-weight: 700; color: {ACCENT_TEAL}; }}
        .pfsa-metric-label {{ color: #9fb3c8; font-size: 0.78rem; text-transform: uppercase; }}
        .pfsa-u23-tag {{
            display:inline-block; padding:0.15rem 0.55rem; border-radius:6px;
            background: rgba(0,242,254,0.12); border:1px solid rgba(0,242,254,0.5);
            color:{ACCENT_TEAL}; font-size:0.68rem; letter-spacing:0.04em; text-transform:uppercase;
            margin-left:0.4rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>🎯 Finishing Dashboards</h1>
        <p>Goal output vs. Expected Goals (xG), shot conversion, and press-resistant progression —
        Saudi Pro League &amp; UAE Pro League forwards</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "⚠️ All figures below are illustrative mock values built for portfolio demonstration purposes "
    "and do not represent real recorded statistics."
)

# --------------------------------------------------------------------------
# HARDCODED MODULAR DATA MATRIX — ARAB LEAGUE FORWARDS
# --------------------------------------------------------------------------
FORWARDS_DATA = [
    # Saudi Pro League — Al-Hilal
    {"player": "Aleksandar Mitrović", "club": "Al-Hilal", "league": "Saudi Pro League", "season": "2024/2025 (Last Season)",
     "age": 30, "nationality": "Serbia", "goals": 24, "xG": 20.8, "shots": 96,
     "line_breaking_passes_under_press": 34, "u23_resale_asset": False},
    {"player": "Aleksandar Mitrović", "club": "Al-Hilal", "league": "Saudi Pro League", "season": "2025/2026 (Current Season)",
     "age": 31, "nationality": "Serbia", "goals": 11, "xG": 10.1, "shots": 44,
     "line_breaking_passes_under_press": 16, "u23_resale_asset": False},
    {"player": "Marcos Leonardo", "club": "Al-Hilal", "league": "Saudi Pro League", "season": "2024/2025 (Last Season)",
     "age": 21, "nationality": "Brazil", "goals": 9, "xG": 10.4, "shots": 58,
     "line_breaking_passes_under_press": 41, "u23_resale_asset": True},
    {"player": "Marcos Leonardo", "club": "Al-Hilal", "league": "Saudi Pro League", "season": "2025/2026 (Current Season)",
     "age": 22, "nationality": "Brazil", "goals": 6, "xG": 6.9, "shots": 29,
     "line_breaking_passes_under_press": 22, "u23_resale_asset": True},

    # Saudi Pro League — Al-Nassr
    {"player": "Cristiano Ronaldo", "club": "Al-Nassr", "league": "Saudi Pro League", "season": "2024/2025 (Last Season)",
     "age": 39, "nationality": "Portugal", "goals": 35, "xG": 29.6, "shots": 132,
     "line_breaking_passes_under_press": 18, "u23_resale_asset": False},
    {"player": "Cristiano Ronaldo", "club": "Al-Nassr", "league": "Saudi Pro League", "season": "2025/2026 (Current Season)",
     "age": 40, "nationality": "Portugal", "goals": 14, "xG": 12.9, "shots": 61,
     "line_breaking_passes_under_press": 9, "u23_resale_asset": False},

    # Saudi Pro League — Al-Ittihad
    {"player": "Karim Benzema", "club": "Al-Ittihad", "league": "Saudi Pro League", "season": "2024/2025 (Last Season)",
     "age": 36, "nationality": "France", "goals": 22, "xG": 19.3, "shots": 88,
     "line_breaking_passes_under_press": 27, "u23_resale_asset": False},
    {"player": "Karim Benzema", "club": "Al-Ittihad", "league": "Saudi Pro League", "season": "2025/2026 (Current Season)",
     "age": 37, "nationality": "France", "goals": 9, "xG": 8.7, "shots": 39,
     "line_breaking_passes_under_press": 13, "u23_resale_asset": False},

    # Saudi Pro League — Al-Ahli
    {"player": "Ivan Toney", "club": "Al-Ahli", "league": "Saudi Pro League", "season": "2024/2025 (Last Season)",
     "age": 28, "nationality": "England", "goals": 18, "xG": 16.5, "shots": 79,
     "line_breaking_passes_under_press": 31, "u23_resale_asset": False},
    {"player": "Ivan Toney", "club": "Al-Ahli", "league": "Saudi Pro League", "season": "2025/2026 (Current Season)",
     "age": 29, "nationality": "England", "goals": 8, "xG": 7.5, "shots": 34,
     "line_breaking_passes_under_press": 14, "u23_resale_asset": False},

    # UAE Pro League — Al-Ain
    {"player": "Soufiane Rahimi", "club": "Al-Ain", "league": "UAE Pro League", "season": "2024/2025 (Last Season)",
     "age": 28, "nationality": "Morocco", "goals": 26, "xG": 21.7, "shots": 91,
     "line_breaking_passes_under_press": 29, "u23_resale_asset": False},
    {"player": "Soufiane Rahimi", "club": "Al-Ain", "league": "UAE Pro League", "season": "2025/2026 (Current Season)",
     "age": 29, "nationality": "Morocco", "goals": 12, "xG": 10.6, "shots": 47,
     "line_breaking_passes_under_press": 15, "u23_resale_asset": False},
    {"player": "Fábio Lima", "club": "Al-Ain", "league": "UAE Pro League", "season": "2024/2025 (Last Season)",
     "age": 25, "nationality": "Brazil", "goals": 15, "xG": 13.2, "shots": 66,
     "line_breaking_passes_under_press": 23, "u23_resale_asset": False},
    {"player": "Fábio Lima", "club": "Al-Ain", "league": "UAE Pro League", "season": "2025/2026 (Current Season)",
     "age": 26, "nationality": "Brazil", "goals": 7, "xG": 6.4, "shots": 30,
     "line_breaking_passes_under_press": 11, "u23_resale_asset": False},

    # UAE Pro League — Al-Wasl
    {"player": "Kaku", "club": "Al-Wasl", "league": "UAE Pro League", "season": "2024/2025 (Last Season)",
     "age": 30, "nationality": "Paraguay", "goals": 11, "xG": 9.8, "shots": 61,
     "line_breaking_passes_under_press": 38, "u23_resale_asset": False},
    {"player": "Kaku", "club": "Al-Wasl", "league": "UAE Pro League", "season": "2025/2026 (Current Season)",
     "age": 31, "nationality": "Paraguay", "goals": 5, "xG": 5.1, "shots": 27,
     "line_breaking_passes_under_press": 17, "u23_resale_asset": False},
    {"player": "Caio Lucas", "club": "Al-Wasl", "league": "UAE Pro League", "season": "2024/2025 (Last Season)",
     "age": 22, "nationality": "Brazil", "goals": 8, "xG": 9.1, "shots": 49,
     "line_breaking_passes_under_press": 33, "u23_resale_asset": True},
    {"player": "Caio Lucas", "club": "Al-Wasl", "league": "UAE Pro League", "season": "2025/2026 (Current Season)",
     "age": 23, "nationality": "Brazil", "goals": 4, "xG": 5.0, "shots": 24,
     "line_breaking_passes_under_press": 18, "u23_resale_asset": True},

    # UAE Pro League — Shabab Al-Ahli
    {"player": "Igor Coronado", "club": "Shabab Al-Ahli", "league": "UAE Pro League", "season": "2024/2025 (Last Season)",
     "age": 30, "nationality": "Brazil", "goals": 13, "xG": 11.4, "shots": 70,
     "line_breaking_passes_under_press": 42, "u23_resale_asset": False},
    {"player": "Igor Coronado", "club": "Shabab Al-Ahli", "league": "UAE Pro League", "season": "2025/2026 (Current Season)",
     "age": 31, "nationality": "Brazil", "goals": 6, "xG": 5.9, "shots": 33,
     "line_breaking_passes_under_press": 20, "u23_resale_asset": False},

    # UAE Pro League — Al-Sharjah
    {"player": "Ali Saleh", "club": "Al-Sharjah", "league": "UAE Pro League", "season": "2024/2025 (Last Season)",
     "age": 22, "nationality": "UAE", "goals": 7, "xG": 8.3, "shots": 44,
     "line_breaking_passes_under_press": 25, "u23_resale_asset": True},
    {"player": "Ali Saleh", "club": "Al-Sharjah", "league": "UAE Pro League", "season": "2025/2026 (Current Season)",
     "age": 23, "nationality": "UAE", "goals": 4, "xG": 4.6, "shots": 21,
     "line_breaking_passes_under_press": 12, "u23_resale_asset": True},
]

df = pd.DataFrame(FORWARDS_DATA)
df["conversion_rate"] = (df["goals"] / df["shots"] * 100).round(1)
df["xg_diff"] = (df["goals"] - df["xG"]).round(2)

# --------------------------------------------------------------------------
# LEAGUE & SEASON FILTERS
# --------------------------------------------------------------------------
f1, f2 = st.columns(2)
with f1:
    league_choice = st.selectbox("League", sorted(df["league"].unique()))
with f2:
    season_choice = st.selectbox("Season", sorted(df["season"].unique(), reverse=True))

view = df[(df["league"] == league_choice) & (df["season"] == season_choice)].copy()

# --------------------------------------------------------------------------
# METRIC GRID
# --------------------------------------------------------------------------
k1, k2, k3 = st.columns(3)
kpis = [
    ("Total Goals", int(view["goals"].sum()) if len(view) else 0),
    ("Total xG", round(view["xG"].sum(), 1) if len(view) else 0),
    ("Avg. Shot Conversion %", f'{view["conversion_rate"].mean():.1f}%' if len(view) else "0%"),
]
for col, (label, val) in zip([k1, k2, k3], kpis):
    with col:
        st.markdown(
            f'<div class="pfsa-card"><div class="pfsa-metric-value">{val}</div>'
            f'<div class="pfsa-metric-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")

if view.empty:
    st.warning("No forwards recorded for this league/season combination in the mock dataset.")
    st.stop()

# --------------------------------------------------------------------------
# SCATTER — GOALS VS xG
# --------------------------------------------------------------------------
st.subheader("Goals vs. Expected Goals (xG)")

fig1, ax1 = plt.subplots(figsize=(9, 6))
fig1.patch.set_facecolor(PRIMARY_BG)
ax1.set_facecolor(PRIMARY_BG)

max_val = max(view["xG"].max(), view["goals"].max()) + 3
ax1.plot([0, max_val], [0, max_val], linestyle="--", color="#3a4552", linewidth=1, label="Expected (Goals = xG)")

colors = ["#00F2FE" if diff >= 0 else "#ff6b6b" for diff in view["xg_diff"]]
ax1.scatter(view["xG"], view["goals"], s=view["shots"] * 3.4, c=colors, alpha=0.8,
            edgecolors="#0d1117", linewidth=0.7)

for _, row in view.iterrows():
    ax1.annotate(row["player"], (row["xG"], row["goals"]), fontsize=8, color="#c9d6e3",
                 xytext=(5, 4), textcoords="offset points")

ax1.set_xlabel("Expected Goals (xG)", color="#9fb3c8")
ax1.set_ylabel("Goals Scored", color="#9fb3c8")
ax1.tick_params(colors="#9fb3c8")
for spine in ax1.spines.values():
    spine.set_color("#2a3542")
ax1.grid(alpha=0.15, color="#3a4552")
ax1.legend(facecolor=SECONDARY_BG, edgecolor="#2a3542", labelcolor="#c9d6e3", fontsize=8)
ax1.set_title("Bubble size = shot volume · Teal = overperforming xG · Red = underperforming",
              color="#f0f6fc", fontsize=10)

st.pyplot(fig1, use_container_width=True)

# --------------------------------------------------------------------------
# HORIZONTAL BAR — CONVERSION RATE RANKING
# --------------------------------------------------------------------------
st.subheader("Shot Conversion Rate Ranking")

u23_only = st.checkbox("🔷 Show only U23 Resale Assets", value=False)

rank_view = view.copy()
if u23_only:
    rank_view = rank_view[rank_view["u23_resale_asset"]]

if rank_view.empty:
    st.info("No U23 resale assets found for this league/season selection.")
else:
    rank_view = rank_view.sort_values("conversion_rate", ascending=False)

    fig2, ax2 = plt.subplots(figsize=(9, max(3, len(rank_view) * 0.65)))
    fig2.patch.set_facecolor(PRIMARY_BG)
    ax2.set_facecolor(PRIMARY_BG)

    bar_colors = [ACCENT_TEAL if u23 else ACCENT_BLUE for u23 in rank_view["u23_resale_asset"]]
    labels = [f"{p} (U23)" if u23 else p for p, u23 in zip(rank_view["player"], rank_view["u23_resale_asset"])]

    bars = ax2.barh(labels, rank_view["conversion_rate"], color=bar_colors, alpha=0.88)
    for bar, rate in zip(bars, rank_view["conversion_rate"]):
        ax2.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2, f"{rate:.1f}%",
                  va="center", color="#e6edf3", fontsize=8)

    ax2.invert_yaxis()
    ax2.set_xlabel("Conversion Rate (%)", color="#9fb3c8")
    ax2.tick_params(colors="#9fb3c8")
    for spine in ax2.spines.values():
        spine.set_color("#2a3542")
    ax2.grid(axis="x", alpha=0.15, color="#3a4552")

    st.pyplot(fig2, use_container_width=True)

with st.expander("📋 View full finishing dataset"):
    display_cols = ["player", "club", "goals", "xG", "shots", "conversion_rate",
                     "line_breaking_passes_under_press", "u23_resale_asset"]
    st.dataframe(view[display_cols].sort_values("goals", ascending=False),
                 use_container_width=True, hide_index=True)
