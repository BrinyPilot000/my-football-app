"""
7_🕵️‍♂️_Player_Similarity_Search.py
--------------------------------------
Statistical similarity engine: standardises a synthetic player-metric matrix
and returns the top-5 nearest neighbours (Euclidean distance on z-scores)
for a targeted player, with adjustable metric weighting.
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Player Similarity Search", page_icon="🕵️‍♂️", layout="wide")

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
        .pfsa-match-card {{
            background-color: {SECONDARY_BG}; border: 1px solid rgba(135, 206, 235, 0.18);
            border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.7rem;
        }}
        .pfsa-match-score {{ color: {ACCENT_TEAL}; font-weight: 700; font-size: 1.2rem; }}
        .pfsa-rank-badge {{
            display:inline-block; width:1.6rem; height:1.6rem; border-radius:50%;
            background: rgba(0,242,254,0.12); border:1px solid {ACCENT_TEAL};
            color:{ACCENT_TEAL}; text-align:center; line-height:1.6rem; font-size:0.8rem; margin-right:0.5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="pfsa-header">
        <h1>🕵️‍♂️ Player Similarity Search</h1>
        <p>Percentile-standardised distance model returning the top statistical matches for a target player</p>
    </div>
    """,
    unsafe_allow_html=True,
)

METRICS = [
    "Goals /90", "xG /90", "Progressive Passes /90", "Progressive Carries /90",
    "Dribbles Completed /90", "Key Passes /90", "Tackles /90", "Interceptions /90",
    "Aerial Win %", "Pass Completion %",
]


@st.cache_data
def generate_similarity_pool(seed: int = 88):
    rng = np.random.default_rng(seed)
    surnames = [
        "Sinclair", "Wright", "Ogbene", "Godden", "Kelly", "Bidwell", "Allen", "Doyle",
        "Latibeaudiere", "Sakamoto", "Kyriakou", "Simms", "Torfason", "Bushiri", "Rudoni",
        "Norwood", "Palmer", "Iheanacho", "Awoniyi", "Eze", "Mitoma", "Gordon", "Mbeumo",
        "Semenyo", "Diaby", "Solanke", "Watkins", "Isak", "Cunha", "Wissa",
    ]
    n = len(surnames)
    data = {"player": surnames}
    for m in METRICS:
        data[m] = np.clip(rng.normal(50, 20, size=n), 1, 99).round(1)
    df = pd.DataFrame(data)
    df["age"] = rng.integers(18, 33, size=n)
    df["position"] = rng.choice(["FW", "MF", "DF"], size=n, p=[0.4, 0.4, 0.2])
    return df


pool = generate_similarity_pool()

c1, c2, c3 = st.columns([1.5, 1.5, 1])
with c1:
    target_player = st.selectbox("Target player", pool["player"])
with c2:
    weighted_metrics = st.multiselect("Metrics to include in similarity model", METRICS, default=METRICS)
with c3:
    top_n = st.slider("Number of matches", 3, 10, 5)

if len(weighted_metrics) < 2:
    st.warning("Select at least 2 metrics to run the similarity model.")
    st.stop()

# --------------------------------------------------------------------------
# STANDARDISE (z-score) & COMPUTE EUCLIDEAN DISTANCE
# --------------------------------------------------------------------------
matrix = pool[weighted_metrics].to_numpy(dtype=float)
z = (matrix - matrix.mean(axis=0)) / matrix.std(axis=0)

target_idx = pool.index[pool["player"] == target_player][0]
target_vec = z[pool.index.get_loc(target_idx)]

distances = np.linalg.norm(z - target_vec, axis=1)
max_dist = distances.max() if distances.max() > 0 else 1
similarity_pct = (1 - distances / max_dist) * 100

results = pool.copy()
results["distance"] = distances
results["similarity"] = similarity_pct.round(1)
results = results[results["player"] != target_player].sort_values("distance").head(top_n)

st.subheader(f"Top {top_n} Statistical Matches for {target_player}")

for rank, (_, row) in enumerate(results.iterrows(), start=1):
    st.markdown(
        f"""
        <div class="pfsa-match-card">
            <span class="pfsa-rank-badge">{rank}</span>
            <strong style="font-size:1.05rem;">{row['player']}</strong>
            &nbsp;·&nbsp; {row['position']} &nbsp;·&nbsp; Age {row['age']}
            <span class="pfsa-match-score" style="float:right;">{row['similarity']}% match</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# --------------------------------------------------------------------------
# VISUAL: similarity bar chart
# --------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, max(3, len(results) * 0.6)))
fig.patch.set_facecolor(PRIMARY_BG)
ax.set_facecolor(PRIMARY_BG)

bars = ax.barh(results["player"][::-1], results["similarity"][::-1], color=ACCENT_TEAL, alpha=0.85)
for bar, val in zip(bars, results["similarity"][::-1]):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f"{val}%",
              va="center", color="#e6edf3", fontsize=8)

ax.set_xlim(0, 105)
ax.set_xlabel("Similarity Score (%)", color="#9fb3c8")
ax.tick_params(colors="#9fb3c8")
for spine in ax.spines.values():
    spine.set_color("#2a3542")
ax.grid(axis="x", alpha=0.15, color="#3a4552")

st.pyplot(fig, use_container_width=True)

with st.expander("📋 View full similarity matrix &amp; metrics used"):
    st.dataframe(
        results[["player", "position", "age", "similarity", "distance"] + weighted_metrics],
        use_container_width=True, hide_index=True,
    )
    st.caption("Similarity computed as 1 − (normalised Euclidean distance) across z-scored metrics.")
