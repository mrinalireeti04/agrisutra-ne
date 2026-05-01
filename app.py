import streamlit as st
import pandas as pd
from fpe_engine import FPEEngine
import anthropic

st.set_page_config(page_title="AgriSutra NE", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp {
        background-color: #f9fafb;
    }
    h1, h2, h3 {
        color: #2e7d32;
        font-family: 'Inter', sans-serif;
    }
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2e7d32;
    }
    .metric-label {
        font-size: 1rem;
        color: #555;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        color: white;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .badge-low { background-color: #e53935; }
    .badge-medium { background-color: #fb8c00; }
    .badge-high { background-color: #43a047; }
</style>
""", unsafe_allow_html=True)

def estimate_yield(crop, land_type):
    if "Maize" in crop:
        return {"Upland": 3.5, "Medium": 4.5, "Lowland": 5.5}.get(land_type, 4.5)
    else:
        return {"Upland": 1.5, "Medium": 2.0, "Lowland": 2.5}.get(land_type, 2.0)

def render_badge(fertility_class):
    fc = fertility_class.lower()
    color_class = {"low": "badge-low", "medium": "badge-medium", "high": "badge-high"}.get(fc, "badge-medium")
    return f'<span class="badge {color_class}">{fertility_class.upper()}</span>'

# Header
st.markdown("<h1 style='text-align: center;'>🌾 AgriSutra NE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Smart Fertilizer Prescriptions for Northeast India</p>", unsafe_allow_html=True)
st.divider()

# Sidebar
with st.sidebar:
    st.header("Settings")
    crop = st.selectbox("Crop", ["Maize", "Kholar"])
    land_type = st.selectbox("Land Type", ["Upland", "Medium", "Lowland"])
    
    auto_estimate = st.checkbox("Auto-estimate Yield", value=True)
    if auto_estimate:
        T = estimate_yield(crop, land_type)
        st.info(f"Estimated Yield: {T} t/ha")
    else:
        T = st.slider("Target Yield (t/ha)", 1.0, 10.0, 4.5, 0.5)
        
    with st.expander("How to use"):
        st.write("""
        1. Select your crop and land type.
        2. Set target yield or auto-estimate.
        3. Enter the soil information for N, P, and K.
        4. Click '⚡ Get Prescription' to compute results.
        """)

# Main Content
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 📋 Soil Inputs")
    input_mode = st.radio("Input Method", ["Fertility Class", "Direct Soil Test Value"], horizontal=True)
    
    # N Input
    st.markdown("**Nitrogen (N)**")
    if input_mode == "Fertility Class":
        fc_N = st.selectbox("N Fertility Class", ["Low", "Medium", "High"])
        SN = None
    else:
        fc_N = None
        SN = st.number_input("Soil Test N (kg/ha)", min_value=0.0, value=280.0)
        
    # P Input
    st.markdown("**Phosphorus (P)**")
    if input_mode == "Fertility Class":
        fc_P = st.selectbox("P Fertility Class", ["Low", "Medium", "High"])
        SP = None
    else:
        fc_P = None
        SP = st.number_input("Soil Test P (kg/ha)", min_value=0.0, value=20.0)
        
    # K Input
    st.markdown("**Potassium (K)**")
    if input_mode == "Fertility Class":
        fc_K = st.selectbox("K Fertility Class", ["Low", "Medium", "High"])
        SK = None
    else:
        fc_K = None
        SK = st.number_input("Soil Test K (kg/ha)", min_value=0.0, value=150.0)
        
    st.markdown("<div style='color: grey;'>🎤 Voice Input (Coming Soon)</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    compute_clicked = st.button("⚡ Get Prescription", type="primary", use_container_width=True)

if compute_clicked:
    try:
        res_N = FPEEngine.compute_N(crop, T, fertility_class=fc_N, SN=SN)
        res_P = FPEEngine.compute_P(crop, T, fertility_class=fc_P, SP=SP)
        res_K = FPEEngine.compute_K(crop, T, fertility_class=fc_K, SK=SK)
        
        # Deduce classes if raw values were provided for the prompt
        display_fc_N = fc_N if fc_N else FPEEngine._resolve_class_from_value(SN, "N").capitalize()
        display_fc_P = fc_P if fc_P else FPEEngine._resolve_class_from_value(SP, "P").capitalize()
        display_fc_K = fc_K if fc_K else FPEEngine._resolve_class_from_value(SK, "K").capitalize()

        with col2:
            st.markdown("### 📊 Prescription Results")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class='card'>
                    <div class='metric-label'>Nitrogen (FN)</div>
                    <div class='metric-value'>{res_N['FN']} <span style='font-size:1rem'>kg/ha</span></div>
                    <div style='color: #666;'>Urea: {res_N['urea_kg_ha']} kg/ha</div>
                    <div style='margin-top: 10px;'>Soil: {render_badge(display_fc_N)}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class='card'>
                    <div class='metric-label'>Phosphorus (FP)</div>
                    <div class='metric-value'>{res_P['FP']} <span style='font-size:1rem'>kg/ha</span></div>
                    <div style='color: #666;'>SSP: {res_P['ssp_kg_ha']} kg/ha</div>
                    <div style='margin-top: 10px;'>Soil: {render_badge(display_fc_P)}</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class='card'>
                    <div class='metric-label'>Potassium (FK)</div>
                    <div class='metric-value'>{res_K['FK']} <span style='font-size:1rem'>kg/ha</span></div>
                    <div style='color: #666;'>MOP: {res_K['mop_kg_ha']} kg/ha</div>
                    <div style='margin-top: 10px;'>Soil: {render_badge(display_fc_K)}</div>
                </div>
                """, unsafe_allow_html=True)
                
            df = pd.DataFrame({
                "Nutrient": ["Nitrogen", "Phosphorus", "Potassium"],
                "Fertility Class": [display_fc_N, display_fc_P, display_fc_K],
                "Requirement (kg/ha)": [res_N['FN'], res_P['FP'], res_K['FK']],
                "Fertilizer": ["Urea", "SSP", "MOP"],
                "Amount (kg/ha)": [res_N['urea_kg_ha'], res_P['ssp_kg_ha'], res_K['mop_kg_ha']]
            })
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            with st.expander("Show Equation Details"):
                st.code(f"{res_N['equation']}\n{res_P['equation']}\n{res_K['equation']}")

        # LLM Explanation Section
        st.divider()
        with st.expander("🧠 AgriSutra AI Explanation", expanded=True):
            with st.spinner("Generating agronomic explanation..."):
                try:
                    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                    
                    system_prompt = """You are AgriSutra AI, an expert agricultural scientist and soil 
fertility advisor for Northeast India. When given a fertilizer 
prescription, explain it in clear, logical, farmer-friendly language.

Always structure your response exactly as follows:

**Why these amounts?**
Explain the agronomic logic behind FN, FP, FK. Reference target yield 
and soil fertility class. No raw equations — conceptual reasoning only.

**Soil fertility interpretation**
What does the farmer's fertility class mean for their field? 
What are the risks if left untreated?

**Application advice**
When and how to apply (split doses, timing relative to sowing, method).

**Caution flags**
If any value is 0 or unusually high, flag it and explain why.

**Farmer takeaway**
One plain-language actionable sentence.

Be specific to the crop and fertility class. Never give generic advice. 
200–300 words total."""

                    user_message = f"""Crop: {crop}, Target Yield: {T} t/ha, Land Type: {land_type}
N — Class: {display_fc_N}, FN={res_N['FN']} kg/ha, Urea={res_N['urea_kg_ha']} kg/ha
P — Class: {display_fc_P}, FP={res_P['FP']} kg/ha, SSP={res_P['ssp_kg_ha']} kg/ha
K — Class: {display_fc_K}, FK={res_K['FK']} kg/ha, MOP={res_K['mop_kg_ha']} kg/ha
Explain this prescription agronomically."""

                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=600,
                        system=system_prompt,
                        messages=[
                            {"role": "user", "content": user_message}
                        ]
                    )
                    
                    st.markdown(response.content[0].text)
                    
                except Exception as e:
                    st.error(f"Error connecting to AgriSutra AI: {str(e)}")
                    st.info("Make sure your ANTHROPIC_API_KEY is set in .streamlit/secrets.toml")
    except Exception as e:
        st.error(f"Computation Error: {str(e)}")
