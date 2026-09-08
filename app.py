import streamlit as st
import random

# ----------------- CONFIGURATION & STYLING -----------------
st.set_page_config(page_title="Electri-City Game Master", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #FF4B4B; color: white; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #ff3333; color: white; }
    .stButton.keep-btn>button { background-color: #4CAF50; }
    .stButton.keep-btn>button:hover { background-color: #45a049; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden !important;}
    .stat-box { padding: 15px; border-radius: 8px; background-color: #262730; margin-bottom: 10px; border: 1px solid #454755; text-align: center; }
    .calamity-card { padding: 15px; background: linear-gradient(135deg, #FF4B4B, #9b0000); border-radius: 8px; color: white; text-align: center; font-weight: bold; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
</style>
""", unsafe_allow_html=True)

# ----------------- GAME DATA -----------------
ASSETS = {
    "Solar": {"cost": 150, "mw": 100, "icon": "☀️"}, #[span_1](start_span)[span_1](end_span)
    "Wind": {"cost": 150, "mw": 100, "icon": "🌬️"}, #[span_2](start_span)[span_2](end_span)
    "Hydro": {"cost": 300, "mw": 200, "icon": "💧"}, #[span_3](start_span)[span_3](end_span)
    "Coal": {"cost": 250, "mw": 150, "icon": "🔥"}, #[span_4](start_span)[span_4](end_span)
    "Gas": {"cost": 250, "mw": 150, "icon": "🔥"}, #[span_5](start_span)[span_5](end_span)
    "Nuclear": {"cost": 800, "mw": 600, "icon": "☢️"}, #[span_6](start_span)[span_6](end_span)
    "Substation": {"cost": 10, "mw": 0, "icon": "🏢"} #[span_7](start_span)[span_7](end_span)
}

# Full Calamity Database[span_8](start_span)[span_8](end_span)
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

# Difficulty Pools
EASY_CALS = ["Mild Warm Spell", "Clear Sky", "Calm Weather", "Dry & Clear", "Dense Cloud Cover", "Foggy Weather", "Continuous Rain", "Renewable Subsidy", "Nuclear Subsidy"]
MOD_CALS = ["Heavy Monsoon", "Severe Thunderstorm", "Severe Heat", "Cold Wave", "River Flood", "Lightning Storm", "Strong Wind Front", "Infrastructure Investment", "National Grid Upgrade", "Construction Material Shortage"]
HARD_CALS = ["Extreme Heatwave", "Cyclone", "Severe Drought", "Extreme Cold", "Dust Storm", "Regional War", "Global Fuel Price Shock", "Rapid Urban Development", "National Energy Emergency", "Major Industrial Accident"]

# ----------------- SESSION STATE -----------------
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.points = 1800 #[span_9](start_span)[span_9](end_span)
    st.session_state.level = 1
    st.session_state.inventory = {k: 0 for k in ASSETS}
    st.session_state.stage = "playing"
    st.session_state.active_calamities = []
    st.session_state.calamities_revealed = False

# ----------------- UI: REGISTRATION -----------------
if not st.session_state.started:
    st.title("⚡ Electri-City: Team Registration")
    
    t_name = st.text_input("Duo / Team Name:")
    col1, col2 = st.columns(2)
    
    with col1:
        p1_name = st.text_input("Player 1 Name:")
        p1_contact = st.text_input("Player 1 Contact Number:")
        
    with col2:
        p2_name = st.text_input("Player 2 Name:")
        p2_contact = st.text_input("Player 2 Contact Number:")

    if st.button("🚀 Initialize Game"):
        if t_name.strip() and p1_name.strip() and p2_name.strip():
            st.session_state.team_name = t_name.strip()
            st.session_state.p1 = p1_name.strip()
            st.session_state.p2 = p2_name.strip()
            st.session_state.started = True
            st.rerun()
        else:
            st.warning("Please fill in Team Name and Player Names to continue.")
    st.stop()

# ----------------- UI: GAMEPLAY -----------------
if st.session_state.stage == "playing":
    # Header: Base Demand is now hidden
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title(f"🏙️ Level {st.session_state.level}")
        st.caption(f"**Team:** {st.session_state.team_name} | {st.session_state.p1} & {st.session_state.p2}")
    with c2:
        st.markdown(f"<div class='stat-box'><h4>💰 Points</h4><h3>{st.session_state.points:.1f}</h3></div>", unsafe_allow_html=True)

    st.divider()

    # --- MARKET SECTION ---
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
    else:
        st.success(f"✅ Cart Total: {total_cost} pts (Remaining: {st.session_state.points - total_cost:.1f} pts)")

    st.divider()
    
    # --- ZONING SECTION ---
    st.subheader("🗺️ Substation Zoning")
    st.info("Assign your substations to zones. Minimum 2 substations required per zone.")
    
    total_subs_owned = st.session_state.inventory["Substation"] + buys["Substation"]
    st.write(f"**Total Substations Available to Place:** {total_subs_owned}")
    
    zone_cols = st.columns(4)
    z1 = zone_cols[0].number_input("Zone 1", min_value=0, value=0)
    z2 = zone_cols[1].number_input("Zone 2", min_value=0, value=0)
    z3 = zone_cols[2].number_input("Zone 3", min_value=0, value=0)
    z4 = zone_cols[3].number_input("Zone 4", min_value=0, value=0)
    assigned_subs = z1 + z2 + z3 + z4

    st.divider()
    
    # --- CALAMITY REVEAL (LUCK BASED) ---
    st.subheader("🌪️ Calamity Draw")
    
    num_calamities = st.session_state.level - 1
    
    if num_calamities == 0:
        st.success("☀️ Clear Skies! No calamities are active for Level 1.") #[span_10](start_span)[span_10](end_span)
        st.session_state.calamities_revealed = True
        st.session_state.active_calamities = []
    else:
        if not st.session_state.calamities_revealed:
            st.warning(f"Level {st.session_state.level} requires you to draw {num_calamities} calamity card(s).")
            if st.button("🎲 Scratch & Reveal Calamities"):
                st.session_state.calamities_revealed = True
                
                drawn = []
                if num_calamities == 1:
                    drawn = random.sample(EASY_CALS, 1)
                elif num_calamities == 2:
                    drawn = random.sample(EASY_CALS + MOD_CALS, 2)
                else:
                    safe_limit = min(num_calamities, len(MOD_CALS + HARD_CALS))
                    drawn = random.sample(MOD_CALS + HARD_CALS, safe_limit)
                    
                st.session_state.active_calamities = drawn
                st.rerun()
        else:
            cal_cols = st.columns(len(st.session_state.active_calamities))
            for i, cal in enumerate(st.session_state.active_calamities):
                with cal_cols[i]:
                    st.markdown(f"<div class='calamity-card'>⚠️ {cal}</div>", unsafe_allow_html=True)
                
    st.divider()
    
    # --- TRANSMISSION LOSSES ---
    st.subheader("📉 Transmission & Grid Factors")
    t_losses = st.number_input("Enter Transmission Losses (in MW) assigned by Game Master:", min_value=0.0, value=0.0, step=10.0)

    # --- EXECUTION ---
    if st.button("⚙️ Execute Grid Calculation"):
        if total_cost > st.session_state.points:
            st.error("Cannot execute: Over budget.")
        elif assigned_subs > total_subs_owned:
            st.error(f"Cannot execute: You assigned {assigned_subs} substations, but only have {total_subs_owned}.")
        elif z1 < 2 or z2 < 2 or z3 < 2 or z4 < 2:
            st.error(f"Cannot execute: Disqualified! You must maintain at least 2 substations in every zone.")
        elif not st.session_state.calamities_revealed:
            st.error("Cannot execute: You must reveal your calamities first!")
        else:
            # Deduct points & update inventory
            st.session_state.points -= total_cost
            for a in ASSETS:
                st.session_state.inventory[a] += buys[a]

            # Calculate Calamity Impacts
            base_peak = 1100 #[span_11](start_span)[span_11](end_span)
            mods = [0, 0, 0, 0, 0, 0, 0] # Load, Sol, Win, Hyd, Coa, Gas, Nuc
            
            for c in st.session_state.active_calamities:
                for i in range(7):
                    mods[i] += CALAMITIES[c][i]

            # Finalize Numbers
            new_demand = base_peak * (1 + (mods[0] / 100))
            
            gen = 0
            gen += st.session_state.inventory["Solar"] * ASSETS["Solar"]["mw"] * (1 + (mods[1] / 100)) #[span_12](start_span)[span_12](end_span)
            gen += st.session_state.inventory["Wind"] * ASSETS["Wind"]["mw"] * (1 + (mods[2] / 100)) #[span_13](start_span)[span_13](end_span)
            gen += st.session_state.inventory["Hydro"] * ASSETS["Hydro"]["mw"] * (1 + (mods[3] / 100)) #[span_14](start_span)[span_14](end_span)
            gen += st.session_state.inventory["Coal"] * ASSETS["Coal"]["mw"] * (1 + (mods[4] / 100)) #[span_15](start_span)[span_15](end_span)
            gen += st.session_state.inventory["Gas"] * ASSETS["Gas"]["mw"] * (1 + (mods[5] / 100)) #[span_16](start_span)[span_16](end_span)
            gen += st.session_state.inventory["Nuclear"] * ASSETS["Nuclear"]["mw"] * (1 + (mods[6] / 100)) #[span_17](start_span)[span_17](end_span)

            # Apply Transmission Losses
            effective_gen = gen - t_losses

            st.session_state.last_demand = new_demand
            st.session_state.last_gen = effective_gen
            st.session_state.losses_applied = t_losses
            
            if effective_gen < new_demand:
                st.session_state.stage = "eliminated"
            else:
                st.session_state.last_surplus = effective_gen - new_demand
                st.session_state.stage = "surplus_decision"
            
            st.rerun()

# ----------------- UI: SURPLUS DECISION -----------------
elif st.session_state.stage == "surplus_decision":
    st.balloons()
    st.success(f"🎉 **Level {st.session_state.level} Cleared!** The city grid held stable against the calamities.")
    
    st.write(f"**Target Peak Demand:** {st.session_state.last_demand:.1f} MW")
    st.write(f"**Total Generation (After {st.session_state.losses_applied:.1f} MW Losses):** {st.session_state.last_gen:.1f} MW")
    
    st.subheader(f"⚡ Surplus Power Generated: {st.session_state.last_surplus:.1f} MW")
    st.info("You have excess power. You can either convert it to bonus points (1.5x rate) to buy more assets next round, or keep it as unspent power reserve.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💰 Convert to Points (1.5x)"):
            bonus = st.session_state.last_surplus * 1.5
            st.session_state.points += bonus
            st.success(f"Converted! Added {bonus:.1f} pts to your budget.")
            st.session_state.level += 1
            st.session_state.calamities_revealed = False
            st.session_state.active_calamities = []
            st.session_state.stage = "playing"
            st.rerun()
            
    with col2:
        if st.button("⚡ Keep as Power"):
            st.success("Surplus power retained. Moving to next round.")
            st.session_state.level += 1
            st.session_state.calamities_revealed = False
            st.session_state.active_calamities = []
            st.session_state.stage = "playing"
            st.rerun()

# ----------------- UI: ELIMINATED -----------------
elif st.session_state.stage == "eliminated":
    st.error(f"🚨 **GRID COLLAPSE!** Team {st.session_state.team_name} has been eliminated.")
    st.write(f"**Target Peak Demand:** {st.session_state.last_demand:.1f} MW")
    st.write(f"**Total Generation (After {st.session_state.losses_applied:.1f} MW Losses):** {st.session_state.last_gen:.1f} MW")
    st.warning("Your power fell below the required threshold. The city has blacked out.")
    
    if st.button("🔄 Return to Registration"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()