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

# 2. Generate Fixed Dataset for Coventry City
@st.cache_data
def load_mock_match_data():
    # Format: [X coordinate, Y coordinate, Total Match Involvements]
    players = {
        'Simms (9)':,           # Lone striker
        'Wright (11)':,         # Left wing
        'Sakamoto (7)':,        # Right wing
        'Rudoni (10)':,         # Attacking Mid Left
        'Torp (8)':,            # Attacking Mid Right
        'Sheaf (14)':,          # Midfield Anchor Hub
        'Eccles (28)':,         # Midfield Anchor Support
        'Binks (5)':,           # Left CB
        'Thomas (4)':,          # Central CB
        'Latibeaudiere (22)':,  # Right CB
        'Dovin (1)': [10, 40, 30]            # Goalkeeper
    }
    
    # Generate match passing matrix lanes (Source, Target, Volume of passes)
    passing_lanes = [
        ('Thomas (4)', 'Sheaf (14)', 18), ('Thomas (4)', 'Eccles (28)', 14),
        ('Binks (5)', 'Sheaf (14)', 15), ('Binks (5)', 'Wright (11)', 22),
        ('Latibeaudiere (22)', 'Eccles (28)', 16), ('Latibeaudiere (22)', 'Sakamoto (7)', 19),
        ('Sheaf (14)', 'Eccles (28)', 28), ('Eccles (28)', 'Sheaf (14)', 24), 
        ('Sheaf (14)', 'Rudoni (10)', 14), ('Eccles (28)', 'Torp (8)', 15),
        ('Wright (11)', 'Simms (9)', 8), ('Sakamoto (7)', 'Simms (9)', 6),
        ('Rudoni (10)', 'Simms (9)', 9), ('Torp (8)', 'Simms (9)', 7)
    ]
    return players, passing_lanes

players, passing_lanes = load_mock_match_data()

# 3. Layout Control Sidebar Settings
st.sidebar.header("🎨 Visual Options")
min_pass_threshold = st.sidebar.slider("Minimum Pass Volume Filter", 1, 10, 3)
node_color = st.sidebar.color_picker("Player Node Color", "#87CEEB")
line_color = st.sidebar.color_picker("Passing Line Color", "#00F2FE")

# 4. Canvas Plotting Engine using mplsoccer
pitch = Pitch(pitch_type='statsbomb', pitch_color='#0d1117', line_color='#212936', goal_type='line')
fig, ax = pitch.draw(figsize=(13, 8))
fig.patch.set_facecolor('#0d1117')

# Plot Lines (Passing Links)
for source, target, volume in passing_lanes:
    if volume >= min_pass_threshold:
        x_start, y_start = players[source][0], players[source][1]
        x_end, y_end = players[target][0], players[target][1]
        
        # Calculate width scaling dynamically
        line_width = (volume - min_pass_threshold) / 2 + 1
        alpha_val = min(0.2 + (volume / 30), 0.9)
        
        pitch.lines(x_start, y_start, x_end, y_end, ax=ax, color=line_color, 
                    linewidth=line_width, alpha=alpha_val, zorder=1)

# Plot Circles (Player Nodes)
for name, data in players.items():
    x, y, involvements = data[0], data[1], data[2]
    node_size = involvements * 7.5  # Dynamic size mapping
    
    # Plot bubble shape
    pitch.scatter(x, y, s=node_size, color=node_color, edgecolors='#ffffff', 
                  linewidth=1.5, alpha=0.95, ax=ax, zorder=2)
    
    # Add text label placement
    ax.text(x, y - 3.5, name, color='#ffffff', fontsize=9, 
            fontweight='bold', ha='center', va='center', zorder=3)

ax.set_title("Coventry City - Tactical Passing Network Shape", color='#ffffff', 
             fontsize=16, pad=20, fontweight='bold')

# 5. Display Interface Columns
col1, col2 = st.columns([4, 1])
with col1:
    st.pyplot(fig)
with col2:
    st.metric("Total Match Passes", "542")
    st.metric("Network Density", "68.4%")
    st.metric("Progressive Pass %", "14.2%")
    
    # Save chart configuration as image asset
    fig.savefig("passing_network.png", bbox_inches='tight', facecolor='#0d1117')
    with open("passing_network.png", "rb") as file:
        st.download_button(label="📥 Download Clean PNG", data=file, 
                           file_name="coventry_pass_network.png", mime="image/png")
