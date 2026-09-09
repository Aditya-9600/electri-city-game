import streamlit as st
import streamlit.components.v1 as components
import json
import os
import requests
from datetime import datetime

# --- ADMIN PASSWORD ---
ADMIN_PASSWORD = "eesa"

# ----------------- SERVER DATABASE SETUP -----------------
STATE_FILE = "master_control.json"
TEAM_FILE = "teams_database.json"

def init_master_state():
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w") as f:
            json.dump({"level": 1, "calamities_revealed": False, "active_calamities": []}, f)

def read_master():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def write_master(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def load_teams():
    if os.path.exists(TEAM_FILE):
        with open(TEAM_FILE, "r") as f:
            return json.load(f)
    return {}

def save_team_state():
    if "team_name" in st.session_state:
        teams = load_teams()
        keys_to_save = ["points", "level", "inventory", "stage", "power_reserve", "last_demand", "last_gen", "last_surplus", "losses_applied", "p1", "p2", "p1_contact", "p2_contact"]
        teams[st.session_state.team_name] = {k: st.session_state[k] for k in keys_to_save if k in st.session_state}
        with open(TEAM_FILE, "w") as f:
            json.dump(teams, f)

init_master_state()

# ----------------- GOOGLE SHEETS FUNCTION -----------------
def log_results_to_sheets():
    url = "https://script.google.com/macros/s/AKfycbwLnXW4LZfjLfxiMA7RCnRxEikOlN6yiV12PXHN5w1y0Fk43AH8h0qOxlanVg2sJzzD/exec"
    payload = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Team_Name": st.session_state.team_name,
        "Player_1": st.session_state.p1,
        "P1_Contact": st.session_state.p1_contact, 
        "Player_2": st.session_state.p2,
        "P2_Contact": st.session_state.p2_contact, 
        "Final_Points": st.session_state.points,
        "Level_Reached": st.session_state.level
    }
    try:
        requests.post(url, json=payload, timeout=10)
        return True
    except Exception:
        return False

# ----------------- CONFIGURATION & STYLING -----------------
st.set_page_config(page_title="Electri-City Server", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    /* Animated Dynamic Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #0b0f19, #1a1025, #001122, #0d0208);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Hide defaults */
    #MainMenu, footer, header, [data-testid="stHeader"] { visibility: hidden !important; display: none !important; }

    /* Glowing Neon Buttons */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        font-weight: bold; 
        background: transparent;
        color: #00e5ff; 
        border: 2px solid #00e5ff; 
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.4), inset 0 0 10px rgba(0, 229, 255, 0.2);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 12px;
    }
    .stButton>button:hover { 
        background: #00e5ff; 
        color: #000; 
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.8), inset 0 0 20px rgba(0, 229, 255, 0.8);
    }

    /* Glassmorphism Stat Boxes */
    .stat-box { 
        padding: 15px; 
        border-radius: 8px; 
        background: rgba(30, 34, 45, 0.6); 
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        margin-bottom: 10px; 
        border: 1px solid rgba(255,255,255,0.1); 
        text-align: center; 
        border-bottom: 3px solid #00e5ff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }

    /* Pulsing Calamity Warning Cards */
    .calamity-card { 
        padding: 15px; 
        background: rgba(255, 0, 60, 0.15); 
        border: 1px solid #ff003c;
        border-radius: 8px; 
        color: #fff; 
        text-align: center; 
        font-weight: bold; 
        margin-bottom: 10px; 
        animation: pulseRed 1.5s infinite;
    }
    @keyframes pulseRed {
        0% { box-shadow: 0 0 10px rgba(255, 0, 60, 0.3); }
        50% { box-shadow: 0 0 25px rgba(255, 0, 60, 0.7); }
        100% { box-shadow: 0 0 10px rgba(255, 0, 60, 0.3); }
    }

    /* Master Panel Styling */
    .master-panel { 
        background-color: rgba(26, 28, 36, 0.85); 
        backdrop-filter: blur(15px);
        padding: 20px; 
        border-radius: 10px; 
        border: 2px solid #ff003c; 
        box-shadow: 0 0 25px rgba(255, 0, 60, 0.3);
    }
    
    /* Floating Sparks (Background Elements) */
    .spark {
        position: fixed;
        bottom: -50px;
        width: 4px;
        height: 4px;
        background: #ffea00;
        border-radius: 50%;
        box-shadow: 0 0 10px #ffea00, 0 0 20px #ffea00, 0 0 30px #00e5ff;
        animation: sparkRise 5s linear infinite;
        z-index: 0;
        opacity: 0;
    }
    
    /* Randomize Spark Positions & Speeds */
    .spark:nth-child(1) { left: 10%; animation-duration: 4s; animation-delay: 1s; }
    .spark:nth-child(2) { left: 20%; animation-duration: 6s; animation-delay: 2s; }
    .spark:nth-child(3) { left: 30%; animation-duration: 3s; animation-delay: 0.5s; }
    .spark:nth-child(4) { left: 40%; animation-duration: 5s; animation-delay: 3s; }
    .spark:nth-child(5) { left: 50%; animation-duration: 4.5s; animation-delay: 0s; }
    .spark:nth-child(6) { left: 60%; animation-duration: 7s; animation-delay: 1.5s; background: #00e5ff; box-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff;}
    .spark:nth-child(7) { left: 70%; animation-duration: 3.5s; animation-delay: 4s; }
    .spark:nth-child(8) { left: 80%; animation-duration: 5.5s; animation-delay: 2.5s; }
    .spark:nth-child(9) { left: 90%; animation-duration: 4s; animation-delay: 1s; background: #00e5ff; box-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff;}
    .spark:nth-child(10) { left: 15%; animation-duration: 6s; animation-delay: 4.5s; }
    .spark:nth-child(11) { left: 85%; animation-duration: 4.2s; animation-delay: 2.1s; }
    .spark:nth-child(12) { left: 45%; animation-duration: 5.8s; animation-delay: 0.8s; }

    @keyframes sparkRise {
        0% { transform: translateY(0) scale(1); opacity: 0; }
        10% { opacity: 1; }
        50% { transform: translateY(-50vh) scale(1.5); }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) scale(0); opacity: 0; }
    }
    
    /* Keep Main Content Above Sparks */
    .block-container { z-index: 2; position: relative; }
</style>

<!-- Inject Floating Sparks into Background -->
<div class="spark"></div><div class="spark"></div><div class="spark"></div><div class="spark"></div>
<div class="spark"></div><div class="spark"></div><div class="spark"></div><div class="spark"></div>
<div class="spark"></div><div class="spark"></div><div class="spark"></div><div class="spark"></div>
""", unsafe_allow_html=True)

# ----------------- GAME DATA -----------------
ASSETS = {
    "Solar": {"cost": 150, "mw": 100, "icon": "☀️"},
    "Wind": {"cost": 150, "mw": 100, "icon": "🌬️"},
    "Hydro": {"cost": 300, "mw": 200, "icon": "💧"},
    "Coal": {"cost": 250, "mw": 170, "icon": "🔥"},
    "Gas": {"cost": 250, "mw": 170, "icon": "🔥"},
    "Nuclear": {"cost": 800, "mw": 600, "icon": "☢️"},
    "Substation": {"cost": 10, "mw": 0, "icon": "🏢"}
}

CALAMITIES = {
    "Extreme Heatwave": [20, 10, -10, -5, 0, 0, 0],
    "Severe Heat": [15, 5, -5, 0, 0, 5, 0],
    "Heavy Monsoon": [10, -15, 5, 15, 0, 0, 0],
    "Severe Thunderstorm": [10, -15, 10, 5, -5, 0, 0],
    "Cyclone": [15, -20, -15, 5, -5, -5, 0],
    "Dense Cloud Cover": [5, -20, 5, 0, 0, 0, 0],
    "Continuous Rain": [5, -15, 10, 10, 0, 0, 0],
    "Severe Drought": [10, 10, 0, -20, 0, 5, 0],
    "Strong Wind Front": [5, -5, 20, 0, 0, 0, 0],
    "Calm Weather": [5, 10, -20, 0, 0, 0, 0],
    "Clear Sky": [5, 20, 5, 5, 0, 0, 0],
    "Cold Wave": [15, -5, 5, 0, 5, 15, 0],
    "Extreme Cold": [20, -10, 0, -5, 5, 15, 0],
    "River Flood": [10, 0, 0, -15, -5, -5, 0],
    "Foggy Weather": [5, -10, -10, 0, 0, 0, 0],
    "Dry & Clear": [5, 15, 5, -5, 0, 0, 0],
    "Lightning Storm": [10, -15, 5, 0, -10, -5, 0],
    "Dust Storm": [10, -20, -15, 0, -5, 0, 0],
    "Tropical Depression": [10, -15, 15, 10, 0, 0, 0],
    "Mild Warm Spell": [5, 10, 0, 0, 0, 5, 0],
    "Renewable Subsidy": [5, 20, 20, 10, -10, -10, -5],
    "Nuclear Subsidy": [5, -5, -5, 0, 0, -5, 20],
    "Carbon Tax Increase": [10, 10, 10, 5, -20, -15, 0],
    "Fuel Tax Hike": [10, 5, 5, 5, -10, -20, 5],
    "Construction Material Shortage": [5, -10, -10, -15, -5, 10, -20],
    "Fuel Supply Disruption": [10, 10, 10, 5, -15, -20, 5],
    "Regional War": [15, 5, 5, 10, -10, -20, -5],
    "Global Fuel Price Shock": [10, 10, 10, 5, -10, -20, 5],
    "Import Restrictions": [10, -15, -10, 10, -5, -10, -15],
    "Infrastructure Investment": [5, 10, 10, 15, 5, 5, 20],
    "Electricity Price Surge": [15, 10, 10, 5, -5, -5, 5],
    "Industrial Expansion": [20, 5, 5, 10, 10, 15, 5],
    "Pollution Regulation": [5, 15, 15, 10, -20, -10, 5],
    "National Grid Upgrade": [5, 10, 10, 10, -5, -5, 15],
    "Transmission Corridor Restriction": [5, 5, 5, -15, -10, -10, -20],
    "Skilled Labour Shortage": [10, -10, -10, -15, 5, 5, -20],
    "Major Industrial Accident": [10, 5, 5, 5, -15, -10, 5],
    "Rapid Urban Development": [20, 10, 5, 5, 10, 15, 5],
    "International Energy Agreement": [5, 15, 15, 10, -10, -10, 10],
    "National Energy Emergency": [20, 5, 5, 10, 10, 10, 10]
}

# ----------------- SESSION STATE -----------------
if "role" not in st.session_state:
    st.session_state.role = None

# ----------------- UI: ROLE SELECTION -----------------
if st.session_state.role is None:
    st.title("⚡ Electri-City Server Connection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='stat-box'><h3>👑 Game Master (Admin)</h3></div>", unsafe_allow_html=True)
        pwd = st.text_input("Enter Admin Password:", type="password")
        if st.button("Login as Admin"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.role = "admin"
                st.rerun()
            else:
                st.error("Incorrect Password!")
                
    with col2:
        st.markdown("<div class='stat-box'><h3>🎮 Participating Team</h3></div>", unsafe_allow_html=True)
        st.write("Teams competing in Electri-City enter here.")
        if st.button("Go to Team Registration"):
            st.session_state.role = "team_reg"
            st.rerun()
            
    st.stop()

# =====================================================================
#                        GAME MASTER (ADMIN) VIEW
# =====================================================================
if st.session_state.role == "admin":
    st.markdown("<div class='master-panel'>", unsafe_allow_html=True)
    st.title("👑 Game Master Control Desk")
    st.error("⚠️ ONLY ONE COMPUTER SHOULD HAVE THIS SCREEN OPEN.")
    
    master_data = read_master()
    st.subheader(f"Current Global Round: Level {master_data['level']}")
    
    col1, col2 = st.columns(2)
    with col1:
        new_lvl = st.number_input("Change Level Number:", min_value=1, value=master_data['level'])
        if st.button("Update Level"):
            master_data['level'] = new_lvl
            master_data['calamities_revealed'] = False
            master_data['active_calamities'] = []
            write_master(master_data)
            st.success("Level Updated Globally!")
            st.rerun()
            
    with col2:
        st.write("---")
        st.write("**Manual Calamity Selection:**")
        
        all_cals = list(CALAMITIES.keys())
        selected_cals = st.multiselect("Select Calamities to Broadcast:", all_cals, default=master_data['active_calamities'])
        
        if st.button("📢 BROADCAST SELECTED CALAMITIES"):
            master_data['active_calamities'] = selected_cals
            master_data['calamities_revealed'] = True
            write_master(master_data)
            st.success("Calamities Broadcasted to all teams!")
            st.rerun()
            
    st.divider()
    st.subheader("Currently Broadcasted Calamities:")
    if not master_data['calamities_revealed']:
        st.info("Nothing broadcasted yet. Teams see 'Awaiting Game Master...'")
    elif len(master_data['active_calamities']) == 0:
        st.success("☀️ Clear Skies! No calamities active.")
    else:
        for cal in master_data['active_calamities']:
            st.markdown(f"<div class='calamity-card'>⚠️ {cal}</div>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =====================================================================
#                        PARTICIPATING TEAM VIEW
# =====================================================================
if st.session_state.role == "team_reg":
    st.title("⚡ Team Registration / Login")
    st.warning("Enter your exact Team Name. If you accidentally refreshed, typing your exact Team Name will restore your progress.")
    
    t_name = st.text_input("Duo / Team Name:")
    c1, c2 = st.columns(2)
    with c1:
        p1 = st.text_input("Player 1 Name:")
        p1_con = st.text_input("Player 1 Contact Number:")
    with c2:
        p2 = st.text_input("Player 2 Name:")
        p2_con = st.text_input("Player 2 Contact Number:")
        
    if st.button("🚀 Enter Lobby"):
        if t_name.strip() and p1.strip() and p2.strip() and p1_con.strip() and p2_con.strip():
            st.session_state.team_name = t_name
            
            teams = load_teams()
            if t_name in teams:
                for k, v in teams[t_name].items():
                    st.session_state[k] = v
                    
                if st.session_state.stage in ["finished", "eliminated"]:
                    st.warning("Session restored. This team has already concluded their run.")
                else:
                    st.success("Previous session found! Resuming game...")
            else:
                st.session_state.points = 1800
                st.session_state.level = 1
                st.session_state.inventory = {k: 0 for k in ASSETS}
                st.session_state.stage = "playing"
                st.session_state.power_reserve = 0.0
                st.session_state.p1 = p1
                st.session_state.p2 = p2
                st.session_state.p1_contact = p1_con
                st.session_state.p2_contact = p2_con
                save_team_state()
                
            st.session_state.role = "team_play"
            st.rerun()
        else:
            st.error("You must fill in ALL fields to initialize the game.")
    st.stop()

if st.session_state.role == "team_play":
    components.html("""
    <script>
    document.addEventListener("visibilitychange", () => {
        if (document.hidden) { alert("⚠️ WARNING: TAB SWITCH OR MINIMIZE DETECTED! DO NOT LEAVE THE BROWSER."); }
    });
    </script>
    """, height=0)

    master_data = read_master()
    current_level = master_data['level']
    
    if st.session_state.stage == "playing":
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.title(f"🏙️ Level {current_level} - {st.session_state.team_name}")
        with c2:
            st.markdown(f"<div class='stat-box'><h4 style='margin:0'>💰 Budget</h4><h3 style='margin:0;color:#00e5ff;'>{st.session_state.points:.1f} pts</h3></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-box'><h4 style='margin:0'>⚡ Base Demand</h4><h3 style='margin:0;color:#00e5ff;'>1100 MW</h3></div>", unsafe_allow_html=True)
            
        if st.session_state.power_reserve > 0:
            st.info(f"🔋 Carried Over Power Reserve: {st.session_state.power_reserve:.1f} MW")

        st.subheader("🛒 Market Purchases")
        cart_display = st.empty()
        
        buy_cols = st.columns(7)
        buys = {}
        total_cost = 0

        for idx, (asset, details) in enumerate(ASSETS.items()):
            with buy_cols[idx]:
                if asset == "Substation":
                    st.markdown(f"**{details['icon']} {asset}**<br>Cost: {details['cost']} pts<br>Node", unsafe_allow_html=True)
                else:
                    st.markdown(f"**{details['icon']} {asset}**<br>Cost: {details['cost']} pts<br>Gen: {details['mw']} MW", unsafe_allow_html=True)
                qty = st.number_input(f"Buy {asset}", min_value=0, value=0, key=f"buy_{asset}", label_visibility="collapsed")
                buys[asset] = qty
                total_cost += qty * details['cost']

        if total_cost > st.session_state.points:
            cart_display.error(f"❌ OVER BUDGET! Cart: {total_cost} pts | Available: {st.session_state.points:.1f} pts")
        elif total_cost > 0:
            cart_display.success(f"🛒 Live Cart Total: {total_cost} pts | Remaining Points: {st.session_state.points - total_cost:.1f} pts")
        else:
            cart_display.info("Cart is empty. Add sources below.")

        st.divider()
        st.subheader("🗺️ Substation Zoning")
        total_subs = st.session_state.inventory["Substation"] + buys.get("Substation", 0)
        st.write(f"**Total Substations Available:** {total_subs}")
        
        zone_cols = st.columns(4)
        z1 = zone_cols[0].number_input("Zone 1", min_value=0, value=0)
        z2 = zone_cols[1].number_input("Zone 2", min_value=0, value=0)
        z3 = zone_cols[2].number_input("Zone 3", min_value=0, value=0)
        z4 = zone_cols[3].number_input("Zone 4", min_value=0, value=0)
        assigned_subs = z1 + z2 + z3 + z4

        st.divider()
        st.subheader("🌪️ Live Calamity Feed")
        
        if not master_data['calamities_revealed']:
            st.warning("⏳ Awaiting Game Master to broadcast calamities for this round...")
            if st.button("🔄 Check Master Desk (Refresh)"):
                st.rerun()
        else:
            if len(master_data['active_calamities']) == 0:
                st.success("☀️ Clear Skies! No calamities are active for this round.")
            else:
                cal_cols = st.columns(len(master_data['active_calamities']))
                for i, cal in enumerate(master_data['active_calamities']):
                    with cal_cols[i]:
                        st.markdown(f"<div class='calamity-card'>⚠️ {cal}</div>", unsafe_allow_html=True)
                        
            st.divider()
            st.subheader("📉 Transmission & Grid Factors")
            t_losses = st.number_input("Enter Transmission Losses (in MW) assigned by Master:", min_value=0.0, value=0.0, step=10.0)

            if st.button("⚙️ Execute Grid Calculation"):
                if total_cost > st.session_state.points:
                    st.error("Over budget.")
                elif assigned_subs > total_subs:
                    st.error("Too many substations assigned.")
                elif z1 < 2 or z2 < 2 or z3 < 2 or z4 < 2:
                    st.error("Disqualified! Must maintain at least 2 substations per zone.")
                else:
                    st.session_state.points -= total_cost
                    for a in ASSETS: st.session_state.inventory[a] += buys[a]

                    base_demand = 1100
                    mods = [0]*7 
                    for c in master_data['active_calamities']:
                        for i in range(7): mods[i] += CALAMITIES[c][i]

                    new_demand = base_demand * (1 + (mods[0] / 100))
                    
                    base_gen = 0
                    generators = ["Solar", "Wind", "Hydro", "Coal", "Gas", "Nuclear"]
                    for i, k in enumerate(generators):
                        base_gen += st.session_state.inventory[k] * ASSETS[k]["mw"] * (1 + (mods[i+1] / 100))
                    
                    total_gen = base_gen + st.session_state.power_reserve
                    effective_gen = total_gen - t_losses

                    st.session_state.last_demand = new_demand
                    st.session_state.last_gen = effective_gen
                    
                    if effective_gen < new_demand:
                        st.session_state.stage = "eliminated"
                    else:
                        st.session_state.last_surplus = effective_gen - new_demand
                        st.session_state.stage = "surplus_decision"
                        
                    save_team_state()
                    st.rerun()

    elif st.session_state.stage == "surplus_decision":
        st.success(f"🎉 **Round Cleared!**")
        st.write(f"**Target Demand:** {st.session_state.last_demand:.1f} MW")
        st.write(f"**Total Generation:** {st.session_state.last_gen:.1f} MW")
        st.info(f"⚡ Total Surplus Power: {st.session_state.last_surplus:.1f} MW")
        
        st.divider()
        st.subheader("⚖️ Power Conversion Decision")
        st.write("Decide how much surplus power you want to convert to points (1.3x rate) and how much to keep as Power Reserve for the next round.")
        
        convert_amt = st.slider("Select Power to Convert (MW):", min_value=0.0, max_value=float(st.session_state.last_surplus), value=float(st.session_state.last_surplus), step=0.1)
        keep_amt = st.session_state.last_surplus - convert_amt
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='stat-box'>**Points to Gain:**<br><span style='font-size:24px; color:#00e5ff;'>+{convert_amt:.1f} pts</span></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-box'>**Power to Reserve:**<br><span style='font-size:24px; color:#ffea00;'>{keep_amt:.1f} MW</span></div>", unsafe_allow_html=True)
            
        if st.button("✅ Confirm Decision & Proceed to Next Round"):
            st.session_state.points += convert_amt*1.3
            st.session_state.power_reserve = keep_amt
            st.session_state.stage = "playing"
            save_team_state()
            st.rerun()

    elif st.session_state.stage == "eliminated":
        st.error("🚨 **GRID COLLAPSE!** Your power fell below the required threshold.")
        st.write(f"**Final Level Reached:** {current_level}")
        st.write(f"**Target Demand:** {st.session_state.last_demand:.1f} MW")
        st.write(f"**Total Generation:** {st.session_state.last_gen:.1f} MW")
        
        if st.button("📤 Submit Final Log"):
            with st.spinner("Transmitting data to Google Sheets..."):
                success = log_results_to_sheets()
                if success:
                    st.session_state.stage = "finished"
                    save_team_state()
                    st.rerun()
                else:
                    st.error("Failed to transmit data. Please check connection.")
                    
    elif st.session_state.stage == "finished":
        st.subheader("🏁 Data Transmitted Successfully")
        st.write(f"Team **{st.session_state.team_name}**, your final results have been submitted to the Game Master.")
        st.write("Please return to the main assembly area.")
        st.error("Your game session has concluded and is now locked.")
