import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# 1. Page Configuration & Styling
st.set_page_config(page_title="Pro Football Analytics Hub", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    h1, h2, h3 { color: #87CEEB !important; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #1f2937; color: #87CEEB; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Professional Match Performance Dashboard")
st.caption("PFSA Portfolio Standard Analytics Engine")

# 2. Generate Realistic Mock Data for Coventry City (No Paid API Required)
@st.cache_data
def load_mock_match_data():
    # Simulated average positions for a 3-2-4-1 system
    # Format: [X, Y, Involvements] on a StatsBomb 120x80 pitch
    players = {
        'Simms (9)': [95, 40, 40],           # Lone striker
        'Wright (11)': [70, 10, 35],         # Right wing
        'Sakamoto (7)': [70, 70, 33],        # Left wing
        'Rudoni (10)': [75, 35, 38],         # Right #10
        'Torp (8)': [75, 45, 36],            # Left #10
        'Sheaf (14)': [45, 32, 68],          # Primary Hub
        'Eccles (28)': [45, 48, 60],         # Secondary Hub
        'Binks (5)': [25, 20, 45],           # Right CB
        'Thomas (4)': [22, 40, 50],          # Central CB
        'Latibeaudiere (22)': [25, 60, 42],  # Left CB
        'Dovin (1)': [8, 40, 32]             # Goalkeeper
    }

    # Generate mock passing matrix lanes (Source, Target, Volume)
    passing_lanes = [
        ('Thomas (4)', 'Sheaf (14)', 18), ('Thomas (4)', 'Eccles (28)', 14),
        ('Binks (5)', 'Sheaf (14)', 15), ('Binks (5)', 'Wright (11)', 22),
        ('Latibeaudiere (22)', 'Eccles (28)', 16), ('Latibeaudiere (22)', 'Sakamoto (7)', 19),
        ('Sheaf (14)', 'Eccles (28)', 28), ('Eccles (28)', 'Sheaf (14)', 24),  # Core Pivot
        ('Sheaf (14)', 'Rudoni (10)', 14), ('Eccles (28)', 'Torp (8)', 15),
        ('Wright (11)', 'Simms (9)', 8), ('Sakamoto (7)', 'Simms (9)', 6),
        ('Rudoni (10)', 'Simms (9)', 9), ('Torp (8)', 'Simms (9)', 7)
    ]
    return players, passing_lanes

players, passing_lanes = load_mock_match_data()

# 3. Layout Control Sidebar
st.sidebar.header("🎨 Visual Options")
min_pass_threshold = st.sidebar.slider("Minimum Pass Volume Filter", 1, 10, 3)
node_color = st.sidebar.color_picker("Player Node Color", "#87CEEB")
line_color = st.sidebar.color_picker("Passing Line Color", "#00F2FE")

# 4. Canvas Creation using mplsoccer
pitch = Pitch(pitch_type='statsbomb', pitch_color='#0d1117', line_color='#212936', goal_type='line')
fig, ax = pitch.draw(figsize=(13, 8))
fig.patch.set_facecolor('#0d1117')

# Plot Lines (Passing Edges)
for source, target, volume in passing_lanes:
    if volume >= min_pass_threshold:
        x_start, y_start = players[source][0], players[source][1]
        x_end, y_end = players[target][0], players[target][1]

        # Calculate width scaling dynamically
        line_width = (volume - min_pass_threshold) / 2 + 1
        alpha_val = min(0.2 + (volume / 30), 0.9)

        pitch.lines(x_start, y_start, x_end, y_end, ax=ax, color=line_color,
                    linewidth=line_width, alpha=alpha_val, zorder=1)

# Plot Dots (Player Nodes)
for name, data in players.items():
    x, y, involvements = data[0], data[1], data[2]
    node_size = involvements * 7  # Dynamic scaling

    # Plot player position bubble
    pitch.scatter(x, y, s=node_size, color=node_color, edgecolors='#ffffff',
                  linewidth=1.5, alpha=0.95, ax=ax, zorder=2)

    # Add hyper-clean text labels slightly offset underneath
    ax.text(x, y - 3.5, name, color='#ffffff', fontsize=9,
            fontweight='bold', ha='center', va='center', zorder=3)

ax.set_title("Coventry City - Tactical Passing Network Shape", color='#ffffff',
             fontsize=16, pad=20, fontweight='bold')

# 5. Display Interface
col1, col2 = st.columns([4, 1])
with col1:
    st.pyplot(fig)
with col2:
    st.metric("Total Match Passes", "542")
    st.metric("Network Density", "68.4%")
    st.metric("Progressive Pass %", "14.2%")

    # Simple free PNG download option built right in
    fig.savefig("passing_network.png", bbox_inches='tight', facecolor='#0d1117')
    with open("passing_network.png", "rb") as file:
        st.download_button(label="📥 Download Clean PNG", data=file,
                           file_name="coventry_pass_network.png", mime="image/png")
