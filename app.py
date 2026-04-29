import streamlit as st
from fpe_engine import FPEEngine

st.set_page_config(page_title="AgriSutra NE", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for soft green theme
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 15px;
        font-size: 18px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1, h2, h3 {
        color: #81c784;
    }
    .card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        text-align: center;
        border-top: 4px solid #4CAF50;
        margin-bottom: 20px;
        color: white;
    }
    .voice-box {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 2px dashed #4CAF50;
        margin-top: 30px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def estimate_yield(crop, soil):
    if crop == "Maize (Local)":
        return {"Low": 25, "Medium": 35, "High": 45}.get(soil, 30)
    elif crop == "Maize (Hybrid)":
        return {"Low": 30, "Medium": 45, "High": 55}.get(soil, 40)
    elif crop == "Kholar":
        return {"Low": 8, "Medium": 14, "High": 20}.get(soil, 12)
    return 30

def get_explanation(crop, soil_class, yield_target):
    soil_text = soil_class.lower() if soil_class else "unknown"
    yield_text = "high" if yield_target > 30 else ("moderate" if yield_target > 15 else "low")
    
    explanation = f"- **Soil fertility:** {soil_class}\\n"
    explanation += f"- **Crop:** {crop}\\n"
    explanation += f"- **Estimated yield:** {yield_target} q/ha\\n\\n"
    
    explanation += f"Because soil fertility is **{soil_text}** and the target yield is **{yield_text}**, "
    if soil_text == "low":
        explanation += "the system recommends higher fertilizer inputs to compensate for the poor soil and meet the yield goal."
    elif soil_text == "high":
        explanation += "the system recommends lower fertilizer inputs since the soil is already rich, saving you money while meeting the yield goal."
    else:
        explanation += "the system recommends a balanced fertilizer input to maintain soil health and achieve the yield goal."
        
    return explanation

def reset_form():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.title("🌾 Fertilizer Recommendation System")
st.subheader("For Maize and Kholar (Kiphire Region)")

if "recommendation_done" not in st.session_state:
    st.session_state.recommendation_done = False

if not st.session_state.recommendation_done:
    st.markdown("### 📋 Field Information")
    
    crop = st.selectbox("Select Crop 🌽🌿", ["Maize (Local)", "Maize (Hybrid)", "Kholar"])
    
    input_mode = st.radio("Soil Input Method", ["Use Soil Fertility Class (Default)", "Use Soil Test Values"], horizontal=True)
    
    soil_class = "Medium"
    sn, sp, sk = None, None, None
    
    if input_mode == "Use Soil Fertility Class (Default)":
        soil_class = st.selectbox("Soil Fertility 🧪", ["Low", "Medium", "High"])
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            sn = st.number_input("Nitrogen (SN)", min_value=0.0, step=1.0, format="%.1f", value=None)
        with col2:
            sp = st.number_input("Phosphorus (SP)", min_value=0.0, step=1.0, format="%.1f", value=None)
        with col3:
            sk = st.number_input("Potassium (SK)", min_value=0.0, step=1.0, format="%.1f", value=None)
        
        # Deduce a rough soil class for yield estimation if raw values are used
        if sn is not None:
            if sn < 280: soil_class = "Low"
            elif sn > 400: soil_class = "High"
            else: soil_class = "Medium"
            
    land_type = st.selectbox("Land Type 🏔️", ["Upland", "Lowland", "Terrace"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Get Recommendation"):
        if input_mode == "Use Soil Test Values" and (sn is None or sp is None or sk is None):
            st.error("Please enter all soil test values (Nitrogen, Phosphorus, and Potassium).")
        else:
            target_yield = estimate_yield(crop, soil_class)
            
            # Map crop names for the engine
            engine_crop = crop.split()[0].lower()
            if "Maize" in crop:
                engine_crop = "maize"
            
            try:
                result = FPEEngine.compute(
                    crop=engine_crop,
                    soil_class=soil_class.lower() if input_mode == "Use Soil Fertility Class (Default)" else None,
                    SN=sn,
                    SP=sp,
                    SK=sk,
                    target_yield=target_yield
                )
                
                st.session_state.result = result
                st.session_state.target_yield = target_yield
                st.session_state.crop = crop
                st.session_state.soil_class = soil_class
                st.session_state.recommendation_done = True
                st.rerun()
            except Exception as e:
                st.error("Something went wrong. Please check your inputs and try again.")
                
    st.markdown("""
    <div class="voice-box">
        <h4>🎤 Voice Input (Coming Soon)</h4>
        <p>Speak to enter your farm details in Assamese or Hindi.</p>
        <span style="font-size: 2em;">🔊</span>
    </div>
    """, unsafe_allow_html=True)

else:
    # Result Screen
    st.success("✅ Recommendation generated successfully!")
    
    res = st.session_state.result
    
    # Conversion
    urea = res['N'] / 0.46
    ssp = res['P2O5'] / 0.16
    mop = res['K2O'] / 0.60
    fym = 10 if st.session_state.soil_class == "Low" else (5 if st.session_state.soil_class == "Medium" else 2)
    
    st.markdown("### 📦 Recommended Fertilizer Plan")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="card"><h4>Urea</h4><h2>{urea:.1f} kg/ha</h2><p>For Nitrogen</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><h4>MOP</h4><h2>{mop:.1f} kg/ha</h2><p>For Potassium</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="card"><h4>SSP</h4><h2>{ssp:.1f} kg/ha</h2><p>For Phosphorus</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><h4>FYM</h4><h2>{fym} tonnes/ha</h2><p>Organic Matter</p></div>', unsafe_allow_html=True)
        
    st.markdown("### 📅 Application Schedule")
    st.info(f"**At Sowing (Basal):** All {ssp:.1f}kg SSP + All {mop:.1f}kg MOP + {urea*0.5:.1f}kg Urea")
    st.info(f"**30 Days After Sowing:** {urea*0.25:.1f}kg Urea")
    st.info(f"**60 Days After Sowing:** {urea*0.25:.1f}kg Urea")
    
    st.markdown("### 🔍 Why this recommendation?")
    explanation = get_explanation(st.session_state.crop, st.session_state.soil_class, st.session_state.target_yield)
    st.markdown(explanation)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start New Recommendation"):
        reset_form()
