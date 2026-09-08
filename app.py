import streamlit as st
import random
import json
import os
import requests
from datetime import datetime

# ----------------- SERVER DATABASE SETUP -----------------
STATE_FILE = "master_control.json"

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

init_master_state()

# ----------------- GOOGLE SHEETS FUNCTION -----------------
def log_results_to_sheets():
    # Replace this URL with your actual Google Apps Script Web App URL
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
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #FF4B4B; color: white; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #ff3333; color: white; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden !important;}
    .stat-box { padding: 15px; border-radius: 8px; background-color: #262730; margin-bottom: 10px; border: 1px solid #454755; text-align: center; }
    .calamity-card { padding: 15px; background: linear-gradient(135deg, #FF4B4B, #9b0000); border-radius: 8px; color: white; text-align: center; font-weight: bold; margin-bottom: 10px; font-size: 20px;}
    .master-panel { background-color: #1a1c24; padding: 20px; border-radius: 10px; border: 2px solid #FF4B4B; }
</style>
""", unsafe_allow_html=True)

# ----------------- GAME DATA -----------------
ASSETS = {
    "Solar": {"cost": 150, "mw": 100, "icon": "☀️"}, #[span_0](start_span)[span_0](end_span)
    "Wind": {"cost": 150, "mw": 100, "icon": "🌬️"}, #[span_1](start_span)[span_1](end_span)
    "Hydro": {"cost": 300, "mw": 200, "icon": "💧"}, #[span_2](start_span)[span_2](end_span)
    "Coal": {"cost": 250, "mw": 150, "icon": "🔥"}, #[span_3](start_span)[span_3](end_span)
    "Gas": {"cost": 250, "mw": 150, "icon": "🔥"}, #[span_4](start_span)[span_4](end_span)
    "Nuclear": {"cost": 800, "mw": 600, "icon": "☢️"}, #[span_5](start_span)[span_5](end_span)
    "Substation": {"cost": 10, "mw": 0, "icon": "🏢"} #[span_6](start_span)[span_6](end_span)
}

CALAMITIES = {
    "Extreme Heatwave": [20, 10, -10, -5, 0, 0, 0], #[span_7](start_span)[span_7](end_span)
    "Severe Heat": [15, 5, -5, 0, 0, 5, 0], #[span_8](start_span)[span_8](end_span)
    "Heavy Monsoon": [10, -15, 5, 15, 0, 0, 0], #[span_9](start_span)[span_9](end_span)
    "Severe Thunderstorm": [10, -15, 10, 5, -5, 0, 0], #[span_10](start_span)[span_10](end_span)
    "Cyclone": [15, -20, -15, 5, -5, -5, 0], #[span_11](start_span)[span_11](end_span)
    "Dense Cloud Cover": [5, -20, 5, 0, 0, 0, 0], #[span_12](start_span)[span_12](end_span)
    "Continuous Rain": [5, -15, 10, 10, 0, 0, 0], #[span_13](start_span)[span_13](end_span)
    "Severe Drought": [10, 10, 0, -20, 0, 5, 0], #[span_14](start_span)[span_14](end_span)
    "Strong Wind Front": [5, -5, 20, 0, 0, 0, 0], #[span_15](start_span)[span_15](end_span)
    "Calm Weather": [5, 10, -20, 0, 0, 0, 0], #[span_16](start_span)[span_16](end_span)
    "Clear Sky": [5, 20, 5, 5, 0, 0, 0], #[span_17](start_span)[span_17](end_span)
    "Cold Wave": [15, -5, 5, 0, 5, 15, 0], #[span_18](start_span)[span_18](end_span)
    "Extreme Cold": [20, -10, 0, -5, 5, 15, 0], #[span_19](start_span)[span_19](end_span)
    "River Flood": [10, 0, 0, -15, -5, -5, 0], #[span_20](start_span)[span_20](end_span)
    "Foggy Weather": [5, -10, -10, 0, 0, 0, 0], #[span_21](start_span)[span_21](end_span)
    "Dry & Clear": [5, 15, 5, -5, 0, 0, 0], #[span_22](start_span)[span_22](end_span)
    "Lightning Storm": [10, -15, 5, 0, -10, -5, 0], #[span_23](start_span)[span_23](end_span)
    "Dust Storm": [10, -20, -15, 0, -5, 0, 0], #[span_24](start_span)[span_24](end_span)
    "Tropical Depression": [10, -15, 15, 10, 0, 0, 0], #[span_25](start_span)[span_25](end_span)
    "Mild Warm Spell": [5, 10, 0, 0, 0, 5, 0], #[span_26](start_span)[span_26](end_span)
    "Renewable Subsidy": [5, 20, 20, 10, -10, -10, -5], #[span_27](start_span)[span_27](end_span)
    "Nuclear Subsidy": [5, -5, -5, 0, 0, -5, 20], #[span_28](start_span)[span_28](end_span)
    "Carbon Tax Increase": [10, 10, 10, 5, -20, -15, 0], #[span_29](start_span)[span_29](end_span)
    "Fuel Tax Hike": [10, 5, 5, 5, -10, -20, 5], #[span_30](start_span)[span_30](end_span)
    "Construction Material Shortage": [5, -10, -10, -15, -5, 10, -20], #[span_31](start_span)[span_31](end_span)
    "Fuel Supply Disruption": [10, 10, 10, 5, -15, -20, 5], #[span_32](start_span)[span_32](end_span)
    "Regional War": [15, 5, 5, 10, -10, -20, -5], #[span_33](start_span)[span_33](end_span)
    "Global Fuel Price Shock": [10, 10, 10, 5, -10, -20, 5], #[span_34](start_span)[span_34](end_span)
    "Import Restrictions": [10, -15, -10, 10, -5, -10, -15], #[span_35](start_span)[span_35](end_span)
    "Infrastructure Investment": [5, 10, 10, 15, 5, 5, 20], #[span_36](start_span)[span_36](end_span)
    "Electricity Price Surge": [15, 10, 10, 5, -5, -5, 5], #[span_37](start_span)[span_37](end_span)
    "Industrial Expansion": [20, 5, 5, 10, 10, 15, 5], #[span_38](start_span)[span_38](end_span)
    "Pollution Regulation": [5, 15, 15, 10, -20, -10, 5], #[span_39](start_span)[span_39](end_span)
    "National Grid Upgrade": [5, 10, 10, 10, -5, -5, 15], #[span_40](start_span)[span_40](end_span)
    "Transmission Corridor Restriction": [5, 5, 5, -15, -10, -10, -20], #[span_41](start_span)[span_41](end_span)
    "Skilled Labour Shortage": [10, -10, -10, -15, 5, 5, -20], #[span_42](start_span)[span_42](end_span)
    "Major Industrial Accident": [10, 5, 5, 5, -15, -10, 5], #[span_43](start_span)[span_43](end_span)
    "Rapid Urban Development": [20, 10, 5, 5, 10, 15, 5], #[span_44](start_span)[span_44](end_span)
    "International Energy Agreement": [5, 15, 15, 10, -10, -10, 10], #[span_45](start_span)[span_45](end_span)
    "National Energy Emergency": [20, 5, 5, 10, 10, 10, 10] #[span_46](start_span)[span_46](end_span)
}

EASY_CALS = ["Mild Warm Spell", "Clear Sky", "Calm Weather", "Dry & Clear", "Dense Cloud Cover", "Foggy Weather", "Continuous Rain", "Renewable Subsidy", "Nuclear Subsidy"]
MOD_CALS = ["Heavy Monsoon", "Severe Thunderstorm", "Severe Heat", "Cold Wave", "River Flood", "Lightning Storm", "Strong Wind Front", "Infrastructure Investment", "National Grid Upgrade", "Construction Material Shortage"]
HARD_CALS = ["Extreme Heatwave", "Cyclone", "Severe Drought", "Extreme Cold", "Dust Storm", "Regional War", "Global Fuel Price Shock", "Rapid Urban Development", "National Energy Emergency", "Major Industrial Accident"]

# ----------------- SESSION STATE -----------------
if "role" not in st.session_state:
    st.session_state.role = None
if "team_name" not in st.session_state:
    st.session_state.points = 1800 #[span_47](start_span)[span_47](end_span)
    st.session_state.inventory = {k: 0 for k in ASSETS}
    st.session_state.stage = "playing"
    st.session_state.power_reserve = 0.0

# ----------------- UI: ROLE SELECTION -----------------
if st.session_state.role is None:
    st.title("⚡ Electri-City Server Connection")
    st.info("Please select your system role.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👑 I am the Game Master (Admin)"):
            st.session_state.role = "admin"
            st.rerun()
    with col2:
        if st.button("🎮 We are a Participating Team"):
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
        if st.button("🎲 SCRATCH & BROADCAST CALAMITIES"):
            lvl = master_data['level']
            num_calamities = lvl - 1
            
            if num_calamities <= 0:
                drawn = []
            elif num_calamities == 1:
                drawn = random.sample(EASY_CALS, 1)
            elif num_calamities == 2:
                drawn = random.sample(EASY_CALS + MOD_CALS, 2)
            else:
                safe_limit = min(num_calamities, len(MOD_CALS + HARD_CALS))
                drawn = random.sample(MOD_CALS + HARD_CALS, safe_limit)
                
            master_data['active_calamities'] = drawn
            master_data['calamities_revealed'] = True
            write_master(master_data)
            st.success("Calamities Broadcasted to all teams!")
            st.rerun()
            
    st.divider()
    st.subheader("Currently Broadcasted Calamities:")
    if not master_data['calamities_revealed']:
        st.info("Nothing broadcasted yet. Teams see 'Awaiting Game Master...'")
    elif len(master_data['active_calamities']) == 0:
        st.success("☀️ Clear Skies! No calamities for Level 1.") #[span_48](start_span)[span_48](end_span)
    else:
        for cal in master_data['active_calamities']:
            st.markdown(f"<div class='calamity-card'>⚠️ {cal}</div>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =====================================================================
#                        PARTICIPATING TEAM VIEW
# =====================================================================
if st.session_state.role == "team_reg":
    st.title("⚡ Team Registration")
    st.warning("All fields are mandatory to start the game.")
    
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
            st.session_state.p1 = p1
            st.session_state.p2 = p2
            st.session_state.p1_contact = p1_con
            st.session_state.p2_contact = p2_con
            st.session_state.role = "team_play"
            st.rerun()
        else:
            st.error("You must fill in ALL fields (including contact numbers) to initialize the game.")
    st.stop()

if st.session_state.role == "team_play":
    master_data = read_master()
    current_level = master_data['level']
    
    if st.session_state.stage == "playing":
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.title(f"🏙️ Level {current_level} - {st.session_state.team_name}")
        with c2:
            st.markdown(f"<div class='stat-box'><h4>💰 Points</h4><h3>{st.session_state.points:.1f}</h3></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-box'><h4>⚡ Base Demand</h4><h3>1100 MW</h3></div>", unsafe_allow_html=True)
            
        if st.session_state.power_reserve > 0:
            st.info(f"🔋 Carried Over Power Reserve: {st.session_state.power_reserve:.1f} MW")

        st.subheader("🛒 Market Purchases")
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
            st.error(f"❌ Insufficient Points! Cart: {total_cost} pts | Available: {st.session_state.points:.1f} pts")

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
            st.warning("⏳ Awaiting Game Master to reveal calamities for this round...")
            if st.button("🔄 Check Master Desk (Refresh)"):
                st.rerun()
        else:
            if len(master_data['active_calamities']) == 0:
                st.success("☀️ Clear Skies! No calamities are active for this round.") #[span_49](start_span)[span_49](end_span)
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
                    
                    base_gen = sum([st.session_state.inventory[k] * ASSETS[k]["mw"] * (1 + (mods[i+1] / 100)) for i, k in enumerate(["Solar", "Wind", "Hydro", "Coal", "Gas", "Nuclear"])]) #[span_50](start_span)[span_50](end_span)
                    total_gen = base_gen + st.session_state.power_reserve
                    effective_gen = total_gen - t_losses

                    st.session_state.last_demand = new_demand
                    st.session_state.last_gen = effective_gen
                    
                    if effective_gen < new_demand:
                        st.session_state.stage = "eliminated"
                    else:
                        st.session_state.last_surplus = effective_gen - new_demand
                        st.session_state.stage = "surplus_decision"
                    st.rerun()

    elif st.session_state.stage == "surplus_decision":
        st.success(f"🎉 **Round Cleared!**")
        st.write(f"**Target Demand:** {st.session_state.last_demand:.1f} MW")
        st.write(f"**Total Generation:** {st.session_state.last_gen:.1f} MW")
        st.info(f"⚡ Total Surplus Power: {st.session_state.last_surplus:.1f} MW")
        
        st.divider()
        st.subheader("⚖️ Power Conversion Decision")
        st.write("Decide how much surplus power you want to convert to points (1.5x) and how much to keep as Power Reserve for the next round.")
        
        convert_amt = st.slider("Select Power to Convert (MW):", min_value=0.0, max_value=float(st.session_state.last_surplus), value=float(st.session_state.last_surplus), step=1.0)
        keep_amt = st.session_state.last_surplus - convert_amt
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Points to Gain:**<br><span style='font-size:24px; color:#4CAF50;'>+{convert_amt * 1.5:.1f} pts</span>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**Power to Reserve:**<br><span style='font-size:24px; color:#38BDF8;'>{keep_amt:.1f} MW</span>", unsafe_allow_html=True)
            
        if st.button("✅ Confirm Decision & Proceed to Next Round"):
            st.session_state.points += (convert_amt * 1.5)
            st.session_state.power_reserve = keep_amt
            st.session_state.stage = "playing"
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
                    st.rerun()
                else:
                    st.error("Failed to transmit data. Please check connection.")
                    
    elif st.session_state.stage == "finished":
        st.subheader("🏁 Data Transmitted Successfully")
        st.write(f"Team **{st.session_state.team_name}**, your final results have been submitted to the Game Master.")
        st.write("Please return to the main assembly area.")
