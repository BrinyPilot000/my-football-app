"""
app.py
------
Main Hub / Landing Page for the PFSA Technical Scouting Portfolio.
Run with:  streamlit run app.py
"""

import streamlit as st

# --------------------------------------------------------------------------
# PAGE CONFIG (must be the first Streamlit command)
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="PFSA Scouting Portfolio | Home",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# GLOBAL THEME (Matte Black / Dark Slate / Sky Blue / Neon Teal)
# --------------------------------------------------------------------------
PRIMARY_BG = "#0d1117"
SECONDARY_BG = "#161b22"
ACCENT_BLUE = "#87CEEB"
ACCENT_TEAL = "#00F2FE"


def inject_global_css():
    st.markdown(
        f"""
        <style>
        /* ---------- App-wide backdrop ---------- */
        .stApp {{
            background: linear-gradient(180deg, {PRIMARY_BG} 0%, {SECONDARY_BG} 100%);
            color: #e6edf3;
        }}

        section[data-testid="stSidebar"] {{
            background-color: {SECONDARY_BG};
            border-right: 1px solid rgba(0, 242, 254, 0.15);
        }}

        /* ---------- Headers ---------- */
        h1, h2, h3, h4 {{
            color: #f0f6fc !important;
            font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
        }}

        /* ---------- Hero banner ---------- */
        .pfsa-hero {{
            background: linear-gradient(135deg, {SECONDARY_BG} 0%, #0f1a24 100%);
            border: 1px solid rgba(135, 206, 235, 0.25);
            border-radius: 18px;
            padding: 2.2rem 2.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 0 35px rgba(0, 242, 254, 0.06);
        }}
        .pfsa-hero h1 {{
            font-size: 2.4rem;
            margin-bottom: 0.2rem;
            background: linear-gradient(90deg, {ACCENT_BLUE}, {ACCENT_TEAL});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .pfsa-hero p {{
            color: #9fb3c8;
            font-size: 1.05rem;
            max-width: 780px;
        }}
        .pfsa-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            background: rgba(0, 242, 254, 0.1);
            border: 1px solid rgba(0, 242, 254, 0.4);
            color: {ACCENT_TEAL};
            font-size: 0.75rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-right: 0.5rem;
            margin-bottom: 0.6rem;
        }}

        /* ---------- Credential / metric cards ---------- */
        .pfsa-card {{
            background-color: {SECONDARY_BG};
            border: 1px solid rgba(135, 206, 235, 0.18);
            border-radius: 14px;
            padding: 1.3rem 1.4rem;
            height: 100%;
            transition: 0.2s ease-in-out;
        }}
        .pfsa-card:hover {{
            border-color: {ACCENT_TEAL};
            box-shadow: 0 0 22px rgba(0, 242, 254, 0.12);
            transform: translateY(-2px);
        }}
        .pfsa-card h3 {{
            color: {ACCENT_BLUE} !important;
            font-size: 1.05rem;
            margin-bottom: 0.4rem;
        }}
        .pfsa-card p {{
            color: #9fb3c8;
            font-size: 0.9rem;
            margin-bottom: 0;
        }}
        .pfsa-metric-value {{
            font-size: 1.9rem;
            font-weight: 700;
            color: {ACCENT_TEAL};
        }}
        .pfsa-metric-label {{
            color: #9fb3c8;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* ---------- Nav deck tiles ---------- */
        .pfsa-tile {{
            background-color: {SECONDARY_BG};
            border: 1px solid rgba(135, 206, 235, 0.15);
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            margin-bottom: 0.9rem;
        }}
        .pfsa-tile h4 {{
            color: #f0f6fc !important;
            margin-bottom: 0.15rem;
            font-size: 1rem;
        }}
        .pfsa-tile p {{
            color: #8b9cb0;
            font-size: 0.85rem;
            margin-bottom: 0;
        }}

        /* ---------- Divider ---------- */
        .pfsa-divider {{
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0,242,254,0.4), transparent);
            margin: 1.6rem 0;
            border: none;
        }}

        /* ---------- Buttons ---------- */
        div.stButton > button {{
            background: linear-gradient(90deg, {ACCENT_BLUE}, {ACCENT_TEAL});
            color: #0d1117;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
        }}
        div.stButton > button:hover {{
            opacity: 0.85;
            color: #0d1117;
        }}

        /* ---------- Footer ---------- */
        .pfsa-footer {{
            text-align: center;
            color: #56616e;
            font-size: 0.78rem;
            margin-top: 2.5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_global_css()

# --------------------------------------------------------------------------
# HERO SECTION
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="pfsa-hero">
        <span class="pfsa-badge">PFSA Certified</span>
        <span class="pfsa-badge">Technical Scouting</span>
        <span class="pfsa-badge">Data-Driven Recruitment</span>
        <h1>⚽ Football Performance Scouting &amp; Analytics Portfolio</h1>
        <p>
            A data-led technical scouting workspace built for elite recruitment analysis —
            combining event-data visualization, biomechanical and tactical profiling, and
            statistical similarity modelling to support first-team recruitment, opposition
            analysis, and academy player development decisions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# ANALYST CREDENTIALS CARD
# --------------------------------------------------------------------------
st.subheader("Analyst Credentials")

c1, c2, c3, c4 = st.columns(4)
credential_cards = [
    ("🎓", "PFSA Level 3 Diploma", "Performance Analysis in Football — Technical Scouting pathway."),
    ("📈", "5+ Seasons Tracked", "Multi-competition event data coverage across the EFL &amp; Premier League."),
    ("🗂️", "500+ Player Profiles", "Standardised scouting templates built for recruitment committees."),
    ("🧮", "Custom Similarity Models", "Percentile &amp; distance-based statistical player-matching engine."),
]
for col, (icon, title, desc) in zip([c1, c2, c3, c4], credential_cards):
    with col:
        st.markdown(
            f"""
            <div class="pfsa-card">
                <h3>{icon} {title}</h3>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr class="pfsa-divider">', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# HEADLINE METRICS
# --------------------------------------------------------------------------
st.subheader("Portfolio Snapshot")
m1, m2, m3, m4 = st.columns(4)
metrics = [
    ("Matches Analysed", "142"),
    ("Players Profiled", "538"),
    ("Leagues Covered", "4"),
    ("Reports Delivered", "63"),
]
for col, (label, value) in zip([m1, m2, m3, m4], metrics):
    with col:
        st.markdown(
            f"""
            <div class="pfsa-card" style="text-align:center;">
                <div class="pfsa-metric-value">{value}</div>
                <div class="pfsa-metric-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr class="pfsa-divider">', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# NAVIGATION DECK
# --------------------------------------------------------------------------
st.subheader("📂 Explore the Scouting Suite")
st.caption("Use the sidebar navigation, or jump straight to a module below.")

deck = [
    ("🎯", "Finishing Dashboards", "Goals vs. xG output and shot conversion efficiency."),
    ("📊", "Match Analysis", "Passing network map with touch volume &amp; connection strength."),
    ("🔄", "Player Comparison", "Head-to-head radar / pizza chart across key metrics."),
    ("🗺️", "Player Maps — Passing", "Progressive passes &amp; cutback direction mapping."),
    ("💥", "Player Maps — Shots", "xG-scaled shot map with outcome markers."),
    ("👤", "Player Profiles", "Biographical scouting card with strengths &amp; role fit."),
    ("🕵️", "Player Similarity Search", "Statistical nearest-neighbour player matching."),
    ("📉", "Scatter Plot Beta", "Adjustable X/Y quadrant benchmarking tool."),
    ("👥", "Team Comparison", "Tactical style sliders across two squads."),
    ("🛡️", "Team Profiles", "Single-club deep dive: system, age curve, form."),
]

cols = st.columns(2)
for i, (icon, title, desc) in enumerate(deck):
    with cols[i % 2]:
        st.markdown(
            f"""
            <div class="pfsa-tile">
                <h4>{icon} {title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr class="pfsa-divider">', unsafe_allow_html=True)

st.info(
    "👈 Select a module from the sidebar to begin. All data on synthetic pages is "
    "randomly generated for demonstration and does not represent real player performance.",
    icon="ℹ️",
)

st.markdown(
    """
    <div class="pfsa-footer">
        Built with Streamlit &amp; mplsoccer · PFSA Technical Scouting Portfolio · © 2026
    </div>
    """,
    unsafe_allow_html=True,
)
