"""
app.py
------
Main Hub / Landing Page for the PFSA Technical Scouting Portfolio.
Now featuring an interactive Middle Eastern League Search Engine
(Saudi Pro League & UAE Pro League) directly on the home screen.

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
            max-width: 800px;
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

        /* ---------- Search engine module ---------- */
        .pfsa-search-panel {{
            background: linear-gradient(135deg, {SECONDARY_BG} 0%, #101a24 100%);
            border: 1px solid rgba(0, 242, 254, 0.22);
            border-radius: 16px;
            padding: 1.6rem 1.8rem 0.6rem 1.8rem;
            margin-bottom: 1.2rem;
        }}
        .pfsa-search-panel h3 {{
            color: {ACCENT_TEAL} !important;
            margin-bottom: 0.1rem;
        }}
        .pfsa-search-panel p {{
            color: #9fb3c8;
            font-size: 0.88rem;
            margin-bottom: 1rem;
        }}
        .pfsa-select-label {{
            color: {ACCENT_BLUE};
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }}

        /* ---------- Confirmation / connection card ---------- */
        .pfsa-confirm-card {{
            background: rgba(0, 242, 254, 0.06);
            border: 1px solid rgba(0, 242, 254, 0.45);
            border-left: 4px solid {ACCENT_TEAL};
            border-radius: 12px;
            padding: 1.1rem 1.4rem;
            margin: 1rem 0 1.6rem 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
        }}
        .pfsa-confirm-status {{
            color: {ACCENT_TEAL};
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 0.3rem;
        }}
        .pfsa-confirm-detail {{
            color: #c9d6e3;
            font-size: 0.87rem;
        }}
        .pfsa-confirm-pill {{
            display: inline-block;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            background: rgba(135, 206, 235, 0.1);
            border: 1px solid rgba(135, 206, 235, 0.4);
            color: {ACCENT_BLUE};
            font-size: 0.75rem;
            margin: 0.15rem 0.3rem 0.15rem 0;
        }}
        .pfsa-pulse-dot {{
            display: inline-block;
            width: 0.55rem;
            height: 0.55rem;
            border-radius: 50%;
            background: {ACCENT_TEAL};
            margin-right: 0.5rem;
            box-shadow: 0 0 8px {ACCENT_TEAL};
        }}

        /* ---------- Framework deck tiles ---------- */
        .pfsa-framework-tile {{
            background-color: {SECONDARY_BG};
            border: 1px solid rgba(135, 206, 235, 0.16);
            border-radius: 14px;
            padding: 1.2rem 1.3rem;
            margin-bottom: 1rem;
            height: 100%;
            transition: 0.2s ease-in-out;
        }}
        .pfsa-framework-tile:hover {{
            border-color: {ACCENT_TEAL};
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.1);
            transform: translateY(-2px);
        }}
        .pfsa-framework-tile h4 {{
            color: #f0f6fc !important;
            margin-bottom: 0.3rem;
            font-size: 1.02rem;
        }}
        .pfsa-framework-tile p {{
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

        /* ---------- Buttons & Select widgets ---------- */
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
        div[data-baseweb="select"] > div {{
            background-color: {SECONDARY_BG};
            border-color: rgba(135, 206, 235, 0.35) !important;
        }}

        /* ---------- Footer ---------- */
        .pfsa-footer {{
            text-align: center;
            color: #56616e;
            font-size: 0.78rem;
            margin-top: 2.5rem;
            padding-top: 1.2rem;
            border-top: 1px solid rgba(135, 206, 235, 0.12);
        }}
        .pfsa-footer strong {{
            color: {ACCENT_BLUE};
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
        <span class="pfsa-badge">Middle East Market Coverage</span>
        <h1>⚽ Football Performance Scouting &amp; Analytics Portfolio</h1>
        <p>
            A data-led technical scouting workspace built for elite recruitment analysis —
            combining event-data visualization, transition tracking, and market profiling
            to support first-team recruitment, opposition analysis, and cross-market player
            identification across the Saudi Pro League and UAE Pro League.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# ANALYST CREDENTIALS GRID
# --------------------------------------------------------------------------
st.subheader("Analyst Credentials")

c1, c2, c3, c4 = st.columns(4)
credential_cards = [
    ("🎓", "PFSA Certification Level 1 &amp; 2", "Accredited technical scouting &amp; performance analysis pathway."),
    ("🌍", "Multi-League Event Tracking", "Saudi Pro League &amp; UAE Pro League focus, with cross-market coverage."),
    ("🗂️", "Standardized Club Recruitment Profiles", "Consistent scouting templates built for recruitment committees."),
    ("🧮", "Percentile Benchmarking Models", "Statistical percentile &amp; distance-based player evaluation frameworks."),
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
# PORTFOLIO SNAPSHOT METRICS
# --------------------------------------------------------------------------
st.subheader("Portfolio Snapshot")
m1, m2, m3, m4 = st.columns(4)
metrics = [
    ("Matches Analysed", "142"),
    ("Players Profiled", "538"),
    ("Competitions Monitored", "2"),
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
# NEW ENGINE MODULE — GLOBAL SCOUT DATABASE SEARCH
# --------------------------------------------------------------------------
LEAGUES_DATA = {
    "Saudi Pro League (Saudi Arabia)": {
        "seasons": ["2025/2026 (Current Season)", "2024/2025 (Last Season)"],
        "clubs": ["Al-Hilal", "Al-Nassr", "Al-Ittihad", "Al-Ahli", "Al-Shabab", "Al-Ettifaq"],
    },
    "UAE Pro League (United Arab Emirates)": {
        "seasons": ["2025/2026 (Current Season)", "2024/2025 (Last Season)"],
        "clubs": ["Al-Ain", "Al-Wasl", "Shabab Al-Ahli", "Al-Sharjah", "Al-Wahda", "Al-Jazira"],
    },
}

st.markdown(
    """
    <div class="pfsa-search-panel">
        <h3>🌐 Global Scout Database Search</h3>
        <p>Lock in a target competition, timeline, and club identity to prime every downstream scouting module.</p>
    """,
    unsafe_allow_html=True,
)

search_col1, search_col2, search_col3 = st.columns(3)

with search_col1:
    st.markdown('<div class="pfsa-select-label">Choose Target Competition</div>', unsafe_allow_html=True)
    selected_league = st.selectbox(
        "Choose Target Competition",
        options=list(LEAGUES_DATA.keys()),
        key="selected_league",
        label_visibility="collapsed",
    )

with search_col2:
    st.markdown('<div class="pfsa-select-label">Select Data Timeline</div>', unsafe_allow_html=True)
    selected_season = st.selectbox(
        "Select Data Timeline",
        options=LEAGUES_DATA[selected_league]["seasons"],
        key=f"selected_season_{selected_league}",
        label_visibility="collapsed",
    )

with search_col3:
    st.markdown('<div class="pfsa-select-label">Search Target Club Identity</div>', unsafe_allow_html=True)
    selected_club = st.selectbox(
        "Search Target Club Identity",
        options=LEAGUES_DATA[selected_league]["clubs"],
        key=f"selected_club_{selected_league}",
        label_visibility="collapsed",
    )

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# DATABASE CONFIRMATION FEEDBACK LOOP
# --------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="pfsa-confirm-card">
        <div>
            <div class="pfsa-confirm-status"><span class="pfsa-pulse-dot"></span>Secure Link Established</div>
            <div class="pfsa-confirm-detail">
                Active target parameters synced &mdash; ready for secondary page filtering across the scouting suite.
            </div>
            <div style="margin-top:0.6rem;">
                <span class="pfsa-confirm-pill">🏆 {selected_league}</span>
                <span class="pfsa-confirm-pill">🗓️ {selected_season}</span>
                <span class="pfsa-confirm-pill">🛡️ {selected_club}</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="pfsa-divider">', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# INTERACTIVE FRAMEWORK DECK (2x2)
# --------------------------------------------------------------------------
st.subheader("📂 Interactive Framework Deck")
st.caption("Every module below inherits the competition, season, and club context set above.")

framework_row1_col1, framework_row1_col2 = st.columns(2)
framework_row2_col1, framework_row2_col2 = st.columns(2)

with framework_row1_col1:
    st.markdown(
        """
        <div class="pfsa-framework-tile">
            <h4>🎯 Performance &amp; Shot Frameworks</h4>
            <p>Goals vs. xG dashboards and xG-scaled shot maps quantifying finishing quality and attacking output.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with framework_row1_col2:
    st.markdown(
        """
        <div class="pfsa-framework-tile">
            <h4>📊 Live Match Networks</h4>
            <p>Passing network visualizations mapping touch volume and pass-combination strength within a match.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with framework_row2_col1:
    st.markdown(
        """
        <div class="pfsa-framework-tile">
            <h4>🔄 Squad &amp; Recruitment Matrices</h4>
            <p>Head-to-head player comparison, statistical similarity search, and quadrant benchmarking for target identification.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with framework_row2_col2:
    st.markdown(
        """
        <div class="pfsa-framework-tile">
            <h4>🛡️ Team Scouting Profiles</h4>
            <p>Single-club deep dives and tactical style comparisons covering system, squad age curve, and seasonal form.</p>
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

# --------------------------------------------------------------------------
# PROFESSIONAL FOOTER
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="pfsa-footer">
        Built for professional club recruitment committees &middot; PFSA Technical Scouting Portfolio
        &middot; <strong>Saudi Pro League</strong> &amp; <strong>UAE Pro League</strong> Coverage &middot; © 2026
    </div>
    """,
    unsafe_allow_html=True,
)
