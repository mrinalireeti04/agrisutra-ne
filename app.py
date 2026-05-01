import streamlit as st
from fpe_engine import FPEEngine
from utils import calculate_fertilizers, get_nitrogen_details, get_phosphorus_details, get_potassium_details

st.set_page_config(page_title="AgriSutra NE", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    h1, h2, h3, h4 {
        color: #69f0ae;
        font-family: 'Inter', sans-serif;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        text-align: center;
        border-top: 4px solid #00e676;
        margin-bottom: 20px;
        color: #e0e0e0;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #69f0ae;
    }
    .metric-label {
        font-size: 16px;
        color: #b0bec5;
    }
    .input-card {
        background-color: #1e1e1e;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        color: #e0e0e0;
    }
    .detail-card {
        background-color: #1e1e1e;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        margin-top: 20px;
        color: #e0e0e0;
    }
    hr {
        border-color: #333333;
    }
    p, strong, em {
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "main"
if "has_result" not in st.session_state:
    st.session_state.has_result = False

def navigate(page_name):
    st.session_state.page = page_name

def render_main_page():
    st.markdown("<h1 style='text-align: center;'>🌾 Fertilizer Recommendation System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Kiphire Region | Maize & Kholar</h3><br>", unsafe_allow_html=True)

    with st.container():
        # Input Card Area (Styled visually with container but Streamlit native elements)
        st.markdown("### 📋 Field Information")
        
        col1, col2 = st.columns(2)
        with col1:
            crop = st.selectbox("Select Crop 🌽🌿", ["Maize (Local)", "Maize (Hybrid)", "Kholar"])
        
        with col2:
            if "Maize" in crop:
                yield_options = [40, 50]
            else:
                yield_options = [8, 10]
            target_yield = st.selectbox("Target Yield (q/ha) 🎯", yield_options)
            
        st.markdown("---")
        input_mode = st.radio("Soil Input Method", ["Use Soil Fertility Class", "Use Raw Soil Test Values"], horizontal=True)
        st.markdown("#### Soil Fertility Inputs 🧪")
        
        col_n, col_p, col_k = st.columns(3)
        
        n_class, p_class, k_class = None, None, None
        sn, sp, sk = None, None, None
        
        if input_mode == "Use Soil Fertility Class":
            with col_n:
                n_class = st.selectbox("Nitrogen (N) Fertility", ["Low", "Medium", "High"])
            with col_p:
                p_class = st.selectbox("Phosphorus (P) Fertility", ["Low", "Medium", "High"])
            with col_k:
                k_class = st.selectbox("Potassium (K) Fertility", ["Low", "Medium", "High"])
        else:
            with col_n:
                sn = st.number_input("Nitrogen (SN) kg/ha", min_value=0.0, step=1.0, value=280.0)
            with col_p:
                sp = st.number_input("Phosphorus (SP) kg/ha", min_value=0.0, step=1.0, value=20.0)
            with col_k:
                sk = st.number_input("Potassium (SK) kg/ha", min_value=0.0, step=1.0, value=150.0)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Compute Recommendations", type="primary", use_container_width=True):
            engine_crop = "maize" if "Maize" in crop else "kholar"
            try:
                result = FPEEngine.compute(
                    crop=engine_crop,
                    target_yield=float(target_yield),
                    soil_n_class=n_class,
                    soil_p_class=p_class,
                    soil_k_class=k_class,
                    SN=sn,
                    SP=sp,
                    SK=sk
                )
                st.session_state.result = result
                st.session_state.has_result = True
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.has_result:
        st.markdown("<hr>### 📊 Result Summary", unsafe_allow_html=True)
        res = st.session_state.result
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Nitrogen (N)</div>
                <div class="metric-value">{res['N']} kg/ha</div>
            </div>
            ''', unsafe_allow_html=True)
            if st.button("View Nitrogen Details 🌿", use_container_width=True):
                navigate("nitrogen")
                st.rerun()
                
        with c2:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Phosphorus (P₂O₅)</div>
                <div class="metric-value">{res['P2O5']} kg/ha</div>
            </div>
            ''', unsafe_allow_html=True)
            if st.button("View Phosphorus Details 🌱", use_container_width=True):
                navigate("phosphorus")
                st.rerun()
                
        with c3:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Potassium (K₂O)</div>
                <div class="metric-value">{res['K2O']} kg/ha</div>
            </div>
            ''', unsafe_allow_html=True)
            if st.button("View Potassium Details 🌾", use_container_width=True):
                navigate("potassium")
                st.rerun()

def render_nitrogen_page():
    res = st.session_state.result
    urea, ssp, mop = calculate_fertilizers(res['N'], res['P2O5'], res['K2O'])
    details = get_nitrogen_details(res['N'], urea)
    
    st.markdown("## 🌿 Nitrogen Details")
    if st.button("← Back to Summary"):
        navigate("main")
        st.rerun()
        
    st.markdown(f'''
    <div class="detail-card">
        <h3>Requirement: {details['required']} kg/ha N</h3>
        <p><strong>Fertilizer Form:</strong> {details['fertilizer']} ({details['fertilizer_amount']} kg/ha)</p>
        <p><em>Conversion Logic: {details['conversion']}</em></p>
        <hr>
        <h4>📅 Application Schedule</h4>
        <p>{details['schedule']}</p>
        <hr>
        <h4>💡 Why is Nitrogen needed?</h4>
        <p>{details['why']}</p>
        <hr>
        <h4>🚀 Improvement Suggestions</h4>
        <p>{details['improvement']}</p>
    </div>
    ''', unsafe_allow_html=True)

def render_phosphorus_page():
    res = st.session_state.result
    urea, ssp, mop = calculate_fertilizers(res['N'], res['P2O5'], res['K2O'])
    details = get_phosphorus_details(res['P2O5'], ssp)
    
    st.markdown("## 🌱 Phosphorus Details")
    if st.button("← Back to Summary"):
        navigate("main")
        st.rerun()
        
    st.markdown(f'''
    <div class="detail-card">
        <h3>Requirement: {details['required']} kg/ha P₂O₅</h3>
        <p><strong>Fertilizer Form:</strong> {details['fertilizer']} ({details['fertilizer_amount']} kg/ha)</p>
        <p><em>Conversion Logic: {details['conversion']}</em></p>
        <hr>
        <h4>📅 Application Schedule</h4>
        <p>{details['schedule']}</p>
        <hr>
        <h4>💡 Why is Phosphorus needed?</h4>
        <p>{details['why']}</p>
        <hr>
        <h4>🚀 Improvement Suggestions</h4>
        <p>{details['improvement']}</p>
    </div>
    ''', unsafe_allow_html=True)

def render_potassium_page():
    res = st.session_state.result
    urea, ssp, mop = calculate_fertilizers(res['N'], res['P2O5'], res['K2O'])
    details = get_potassium_details(res['K2O'], mop)
    
    st.markdown("## 🌾 Potassium Details")
    if st.button("← Back to Summary"):
        navigate("main")
        st.rerun()
        
    st.markdown(f'''
    <div class="detail-card">
        <h3>Requirement: {details['required']} kg/ha K₂O</h3>
        <p><strong>Fertilizer Form:</strong> {details['fertilizer']} ({details['fertilizer_amount']} kg/ha)</p>
        <p><em>Conversion Logic: {details['conversion']}</em></p>
        <hr>
        <h4>📅 Application Schedule</h4>
        <p>{details['schedule']}</p>
        <hr>
        <h4>💡 Why is Potassium needed?</h4>
        <p>{details['why']}</p>
        <hr>
        <h4>🚀 Improvement Suggestions</h4>
        <p>{details['improvement']}</p>
    </div>
    ''', unsafe_allow_html=True)

if st.session_state.page == "main":
    render_main_page()
elif st.session_state.page == "nitrogen":
    render_nitrogen_page()
elif st.session_state.page == "phosphorus":
    render_phosphorus_page()
elif st.session_state.page == "potassium":
    render_potassium_page()
