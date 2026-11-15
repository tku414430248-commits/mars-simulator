import streamlit as st
import math

G_MARS = 590.0          # 火星表面平均日照常數 (W/m^2)
EFFICIENCY = 0.20       # 太陽能板轉換效率 (20%)
PANEL_DENSITY = 5.0     # 太陽能板單位面積質量 (kg/m^2)
SHIELDING_DENSITY = 20.0 # 輻射防護層單位面積質量 (kg/m^2) - 假設使用高密度聚乙烯(HDPE)
MAX_PAYLOAD = 8000.0    # 火箭最大酬載限制 (kg) - 基於 Delta-V 計算出的上限
BASE_POWER_REQ = 4000.0 # 基地基本維生系統所需功率 (W)

def calculate_mission_parameters(area: float, life_support_mass: float, shielding_area: float) -> dict:
    """

    """
    try:
   
        if area < 0 or life_support_mass < 0 or shielding_area < 0:
            raise ValueError("物理參數不能為負數 (Negative values are not allowed).")

        power_generated = area * EFFICIENCY * G_MARS
        panel_mass = area * PANEL_DENSITY
        shielding_mass = shielding_area * SHIELDING_DENSITY
        
        total_mass = panel_mass + life_support_mass + shielding_mass
        
        # 3. 狀態判定 (State Determination)
        power_ok = power_generated >= BASE_POWER_REQ
        mass_ok = total_mass <= MAX_PAYLOAD
        shielding_ok = shielding_mass >= 1000.0 
        return {
            "power": power_generated,
            "total_mass": total_mass,
            "shielding_mass": shielding_mass,
            "power_ok": power_ok,
            "mass_ok": mass_ok,
            "shielding_ok": shielding_ok,
            "success": power_ok and mass_ok and shielding_ok
        }
    except Exception as e:
       
        return {"error": str(e)}


st.set_page_config(page_title="Mars Outpost Simulator", layout="wide")
st.title("🚀 Junior Astronaut Mission Trainer")
st.markdown("### Mission: Mars Outpost Engineering Trade-off")
st.markdown("Adjust the parameters below. You must balance **Power**, **Mass**, and **Radiation Shielding** based on real orbital mechanics and thermodynamic constraints.")

col1, col2 = st.columns(2)

with col1:
    st.header("⚙️ Engineering Inputs")
    area_input = st.slider("Solar Panel Area (m^2)", min_value=10.0, max_value=150.0, value=50.0, step=1.0)
    life_support_mass = st.slider("Life Support Mass (kg)", min_value=1000.0, max_value=5000.0, value=2500.0, step=100.0)
    shielding_area = st.slider("Radiation Shielding Area (m^2)", min_value=10.0, max_value=100.0, value=30.0, step=1.0)

with col2:
    st.header("📊 Telemetry & Status")
    results = calculate_mission_parameters(area_input, life_support_mass, shielding_area)
    
    if "error" in results:
        st.error(f"System Error: {results['error']}")
    else:
        
        st.metric(label="Total Payload Mass (Limit: 8000 kg)", value=f"{results['total_mass']:.1f} kg", delta=f"{8000 - results['total_mass']:.1f} kg remaining" if results['mass_ok'] else "OVERLOAD", delta_color="normal" if results['mass_ok'] else "inverse")
        st.metric(label="Power Generated (Req: 4000 W)", value=f"{results['power']:.1f} W")
        st.metric(label="Shielding Mass (Req: >1000 kg)", value=f"{results['shielding_mass']:.1f} kg")
        
        st.markdown("---")
     
        if results['success']:
            st.success("✅ MISSION GO! All physical and engineering constraints are met.")
            st.balloons()
        else:
            st.error("❌ MISSION ABORT! Constraints violated.")
            if not results['power_ok']:
                st.warning("⚠️ Insufficient Power: Astronauts will freeze.")
            if not results['mass_ok']:
                st.warning("⚠️ Mass Overload: Rocket cannot achieve escape velocity.")
            if not results['shielding_ok']:
                st.warning("⚠️ Insufficient Shielding: Lethal radiation exposure.")