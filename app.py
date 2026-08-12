import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# 1. Page Configuration & Professional Styling Layout
st.set_page_config(page_title="Next-Gen Performance Hub", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    h1, h2, h3, h4 { color: #87CEEB !important; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #1f2937; color: #87CEEB; border-radius: 5px; width: 100%; border: 1px solid #212936; }
    .stButton>button:hover { background-color: #87CEEB; color: #0d1117; }
    div[data-testid="stExpander"] { background-color: #161b22; border: 1px solid #212936; border-radius: 6px; }
    div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #212936; padding: 15px; border-radius: 8px; text-align: center; }
    label[data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 14px !important; }
    div[data-testid="stMetricValue"] { color: #00F2FE !important; font-size: 24px !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Next-Gen Football Analytics Hub")
st.caption("Advanced Custom Match Engine, Scouting Matrix & Deep Analytics Text Generator — PFSA Standards")

# 2. Advanced Dynamic Team & Player Generation Datasets
@st.cache_data
def get_preset_teams():
    return {
        "Coventry City": {
            "formation": "3-2-4-1 (Inverted Box Pivot)",
            "color1": "#87CEEB", "color2": "#00F2FE",
            "players": {
                "Simms (9)": [95, 40, 41, 78, 85, 30],         # X, Y, Touches, Pass%, xG Rating, Def%
                "Wright (11)": [72, 12, 38, 82, 74, 45],
                "Sakamoto (7)": [74, 68, 35, 85, 62, 50],
                "Rudoni (10)": [76, 33, 45, 79, 88, 55],
                "Torp (8)": [75, 47, 42, 84, 80, 58],
                "Sheaf (14)": [48, 30, 72, 91, 70, 78],        # Central Hub
                "Eccles (28)": [46, 50, 64, 88, 72, 72],
                "Binks (5)": [28, 18, 48, 85, 40, 82],
                "Thomas (4)": [24, 40, 55, 89, 35, 86],
                "Latibeaudiere (22)": [28, 62, 44, 83, 42, 80],
                "Dovin (1)": [8, 40, 34, 75, 20, 10]
            },
            "lanes": [
                ("Thomas (4)", "Sheaf (14)", 18), ("Thomas (4)", "Eccles (28)", 14),
                ("Binks (5)", "Sheaf (14)", 15), ("Binks (5)", "Wright (11)", 22),
                ("Latibeaudiere (22)", "Eccles (28)", 16), ("Latibeaudiere (22)", "Sakamoto (7)", 19),
                ("Sheaf (14)", "Eccles (28)", 28), ("Eccles (28)", "Sheaf (14)", 24),
                ("Sheaf (14)", "Rudoni (10)", 14), ("Eccles (28)", "Torp (8)", 15),
                ("Wright (11)", "Simms (9)", 8), ("Sakamoto (7)", "Simms (9)", 6)
            ],
            "stats": {"passes": "542", "density": "68.4%", "prog": "14.2%"}
        },
        "Custom Template Team": {
            "formation": "4-3-3 Attacking Shape",
            "color1": "#FF4B4B", "color2": "#FFD700",
            "players": {
                "Center Forward (9)": [92, 40, 35, 72, 88, 22],
                "Winger Left (11)": [75, 14, 42, 80, 81, 36],
                "Winger Right (7)": [75, 66, 39, 81, 79, 40],
                "Attacking Mid (10)": [66, 40, 55, 86, 89, 44],
                "Central Mid (8)": [56, 26, 50, 85, 75, 61],
                "Defensive Mid (6)": [44, 40, 68, 93, 60, 82],
                "Fullback Left (3)": [42, 12, 45, 84, 68, 74],
                "Fullback Right (2)": [42, 68, 47, 81, 71, 75],
                "Centerback Left (5)": [26, 24, 52, 88, 32, 84],
                "Centerback Right (4)": [26, 56, 50, 87, 30, 87],
                "Goalkeeper (1)": [8, 40, 31, 76, 12, 15]
            },
            "lanes": [
                ("Centerback Right (4)", "Defensive Mid (6)", 15), ("Centerback Left (5)", "Defensive Mid (6)", 13),
                ("Defensive Mid (6)", "Central Mid (8)", 20), ("Defensive Mid (6)", "Attacking Mid (10)", 18),
                ("Central Mid (8)", "Winger Left (11)", 16), ("Attacking Mid (10)", "Winger Right (7)", 14),
                ("Winger Left (11)", "Center Forward (9)", 10), ("Winger Right (7)", "Center Forward (9)", 7)
            ],
            "stats": {"passes": "495", "density": "58.1%", "prog": "11.5%"}
        }
    }

# 3. Interactive Data Processing Configuration Sidebar
st.sidebar.header("🕹️ Team Setup & Engine Controls")
team_presets = get_preset_teams()
selected_team = st.sidebar.selectbox("Select Target Team Identity", list(team_presets.keys()))

team_data = team_presets[selected_team]
formation_label = st.sidebar.text_input("Tactical Formation System Label", team_data["formation"])
primary_node_color = st.sidebar.color_picker("Custom Primary Club Theme", team_data["color1"])
secondary_line_color = st.sidebar.color_picker("Custom Passing Edge Accent", team_data["color2"])
min_pass_val = st.sidebar.slider("Minimum Pass Volume Filter", 1, 10, 4)

# 4. Modifiable Tactical Matrix Grid Layout
st.subheader(f"📋 Tactical Matrix Panel: {selected_team} ({formation_label})")
with st.expander("📝 Open to Modify Live Player Grid Values (Coordinates & Performance Stats)"):
    modified_players = {}
    cols = st.columns(3)
    for index, (p_name, p_vals) in enumerate(team_data["players"].items()):
        col_target = cols[index % 3]
        with col_target:
            st.markdown(f"**Player: {p_name}**")
            mod_x = st.slider(f"X (Depth) - {p_name}", 0, 120, p_vals[0], key=f"x_{p_name}")
            mod_y = st.slider(f"Y (Width) - {p_name}", 0, 80, p_vals[1], key=f"y_{p_name}")
            mod_tou = st.slider(f"Match Involvements - {p_name}", 5, 100, p_vals[2], key=f"tou_{p_name}")
            
            # Hidden stats injected dynamically into the next generation layer
            modified_players[p_name] = [mod_x, mod_y, mod_tou, p_vals[3], p_vals[4], p_vals[5]]

# 5. Canvas Generation Section via Canvas Layout
pitch = Pitch(pitch_type='statsbomb', pitch_color='#0d1117', line_color='#223044', goal_type='line', line_zorder=1)
fig, ax = pitch.draw(figsize=(14, 8.5))
fig.patch.set_facecolor('#0d1117')

# Drawing Networks lanes
for source, target, volume in team_data["lanes"]:
    if volume >= min_pass_val and source in modified_players and target in modified_players:
        x1, y1 = modified_players[source][0], modified_players[source][1]
        x2, y2 = modified_players[target][0], modified_players[target][1]
        line_w = (volume - min_pass_val) / 1.8 + 1.2
        alpha_v = min(0.3 + (volume / 28), 0.95)
        pitch.lines(x1, y1, x2, y2, ax=ax, color=secondary_line_color, linewidth=line_w, alpha=alpha_v, zorder=2)

# Drawing Player Node Bubbles
for p_name, p_vals in modified_players.items():
    x, y, touches = p_vals[0], p_vals[1], p_vals[2]
    pitch.scatter(x, y, s=touches * 7.5, color=primary_node_color, edgecolors='#ffffff', linewidth=1.8, alpha=0.95, ax=ax, zorder=3)
    ax.text(x, y - 3.8, p_name, color='#ffffff', fontsize=9.5, fontweight='bold', ha='center', va='center', zorder=4)

ax.set_title(f"{selected_team} — Modern Tactical Passing Network Grid Shape", color='#ffffff', fontsize=17, pad=22, fontweight='bold')

# Display Graphical Layout
col1, col2 = st.columns([3.5, 1.2])
with col1:
    st.pyplot(fig)
    fig.savefig("scout_network_export.png", bbox_inches='tight', facecolor='#0d1117')
    with open("scout_network_export.png", "rb") as f_img:
        st.download_button(label="📥 Download Portfolio High-Res PNG File", data=f_img, file_name=f"{selected_team.lower().replace(' ','_')}_network.png", mime="image/png")

with col2:
    st.markdown("#### 📊 Metric Analytics Panel")
    st.metric("Total Executed Passes", team_data["stats"]["passes"])
    st.metric("Overall Spatial Density", team_data["stats"]["density"])
    st.metric("Vertical Progression %", team_data["stats"]["prog"])

# 6. Next-Gen Tactical Automated Text Generation Engine
st.markdown("---")
st.subheader("🔮 Next-Gen Automated Scout Profile Report Generator")
st.caption("Select any player node inside your active grid matrix to generate immediate PFSA-standard textual scouting assessments.")

selected_scout_target = st.selectbox("Choose Profile Node for Text Extraction Analysis", list(modified_players.keys()))
p_stats = modified_players[selected_scout_target]

# Parsing performance indicators to auto-generate the professional analytical text layout
pass_acc, xg_val, def_val = p_stats[3], p_stats[4], p_stats[5]

# Simple algorithmic narrative assignment block
if pass_acc >= 88:
    pass_text = f"demonstrates exceptional press-resistant distribution traits, sitting comfortably in the upper tier percentile. Acting as a critical technical hub, their selection choice under heavy transition locks down possession loops effectively."
else:
    pass_text = f"operates as a direct, high-risk progressive passer, actively trading safety variables to crack open low defensive blocks. While their total turnover percentage rises, their intent creates immediate front line adjustments."

if xg_val >= 75:
    attack_text = f"Their vertical off-ball movement maps directly into prime shot creation parameters, presenting high underlying expected threat metrics (xT) that destabilise central structural tracking chains."
else:
    attack_text = f"Maintains a conservative attacking stance, prioritizing spatial structural recovery runs over aggressive zone penetrations, keeping the team's balance secure during deep transition phases."

if def_val >= 70:
    def_text = f"Defensively, they offer profound utility. Their aggressive counter-pressing metrics and successful tracking duels lock down their flank, converting loose territorial balls into safe rest-defense configurations."
else:
