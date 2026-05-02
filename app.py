import os
import streamlit as st
import importlib
import fpe_engine
import google.generativeai as genai
importlib.reload(fpe_engine)
from fpe_engine import FPEEngine

@st.cache_data
def get_explainable_summary_table(crop, yield_target, urea, ssp, mop):
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "API Key not found. Please set GEMINI_API_KEY in Streamlit secrets or environment variables."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    prompt = f"""
    We are recommending fertilizers for {crop} with a target yield of {yield_target} q/ha.
    The recommended amounts are: {urea} kg/ha Urea, {ssp} kg/ha SSP, and {mop} kg/ha MOP.
    Please provide a detailed, explainable, technical summary writeup.
    The writeup should include a clear table breaking down the recommendations and a detailed explanation 
    of the agronomic reasoning behind these specific fertilizer quantities. 
    Format the response nicely using markdown.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not generate summary: {e}"

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="AgriSutra NE | FPE Advisor", layout="wide", initial_sidebar_state="collapsed")

# ─────────────────────────────────────────────────────────────────────────────
# CSS — DARK MODE PREMIUM THEME
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background-color: #0f1117;
    color: #e0e0e0;
}

/* ── Header ── */
.app-header {
    text-align: center;
    padding: 1.5rem 0 0.5rem 0;
    border-bottom: 1px solid #1e2a1e;
    margin-bottom: 1.5rem;
}
.app-header h1 {
    color: #69f0ae;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0;
}
.app-header p {
    color: #78909c;
    font-size: 1rem;
    margin: 0.25rem 0 0 0;
}

/* ── Step Indicator ── */
.step-bar {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.step-chip {
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    border: 2px solid #2a3a2a;
    color: #546e4a;
    background: #141a14;
}
.step-chip.active {
    border-color: #69f0ae;
    color: #69f0ae;
    background: #0d1f0d;
}
.step-chip.done {
    border-color: #388e3c;
    color: #388e3c;
    background: #0d1a0d;
}

/* ── Panel Card ── */
.panel {
    background: #1a1d27;
    border: 1px solid #252d25;
    border-radius: 14px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.panel h3 {
    color: #69f0ae;
    margin-top: 0;
}

/* ── Nutrient Badge Cards (hub) ── */
.nutrient-card {
    background: #141a14;
    border: 2px solid #1e2d1e;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: border-color 0.2s;
}
.nutrient-card.done-card {
    border-color: #388e3c;
    background: #0d1a0d;
}
.nutrient-card .nut-icon { font-size: 2rem; margin-bottom: 0.4rem; }
.nutrient-card .nut-name { font-size: 1rem; font-weight: 700; color: #cfd8dc; }
.nutrient-card .nut-val  { font-size: 1.4rem; font-weight: 700; color: #69f0ae; margin-top: 0.3rem; }
.nutrient-card .nut-pend { font-size: 0.85rem; color: #546e4a; margin-top: 0.3rem; }

/* ── Result card inside nutrient page ── */
.result-box {
    background: #0d1a0d;
    border: 1px solid #2e7d32;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
}
.result-box .big-val {
    font-size: 2rem;
    font-weight: 700;
    color: #69f0ae;
}
.result-box .eq-text {
    font-size: 0.8rem;
    color: #78909c;
    font-family: monospace;
    margin-top: 0.4rem;
}

/* ── Summary card ── */
.summary-card {
    background: #141a14;
    border: 2px solid #2e7d32;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
}
.summary-card .s-label { color: #90a4ae; font-size: 0.9rem; }
.summary-card .s-val   { font-size: 2.2rem; font-weight: 700; color: #69f0ae; }
.summary-card .s-conv  { font-size: 0.85rem; color: #78909c; margin-top: 0.3rem; }

/* ── Divider ── */
.divider { border-top: 1px solid #252d25; margin: 1.5rem 0; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.15s;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS = {
    "step": 1,          # 1=setup, 2=hub, 3=nutrient_page, 4=summary
    "crop": None,
    "target_yield": None,
    "active_nutrient": None,   # "N", "P", or "K"

    "N_done": False, "P_done": False, "K_done": False,
    "FN": None,      "FP": None,      "FK": None,
    "N_urea": None,  "P_ssp": None,   "K_mop": None,
    "N_eq": "",      "P_eq": "",      "K_eq": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def go(step, **kwargs):
    st.session_state.step = step
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.rerun()

def all_done():
    return st.session_state.N_done and st.session_state.P_done and st.session_state.K_done

NUTRIENT_META = {
    "N":  {"icon": "🌿", "label": "Nitrogen",    "unit": "FN",   "fert": "Urea",  "conv_label": "Urea",  "color": "#69f0ae"},
    "P":  {"icon": "🌱", "label": "Phosphorus",  "unit": "FP₂O₅","fert": "SSP",   "conv_label": "SSP",   "color": "#81d4fa"},
    "K":  {"icon": "🌾", "label": "Potassium",   "unit": "FK₂O", "fert": "MOP",   "conv_label": "MOP",   "color": "#ffcc80"},
}

# ─────────────────────────────────────────────────────────────────────────────
# SHARED HEADER
# ─────────────────────────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class="app-header">
        <h1>🌾 AgriSutra NE — Fertilizer Advisor</h1>
        <p>Kiphire Region &nbsp;|&nbsp; STCR-Based FPE System &nbsp;|&nbsp; Maize &amp; Kholar</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP INDICATOR
# ─────────────────────────────────────────────────────────────────────────────
def render_step_bar():
    steps = ["1. Crop & Yield", "2. Select Nutrient", "3. Compute", "4. Summary"]
    cur = st.session_state.step
    chips = ""
    for i, label in enumerate(steps, start=1):
        cls = "active" if i == cur else ("done" if i < cur else "")
        chips += f'<div class="step-chip {cls}">{label}</div>'
    st.markdown(f'<div class="step-bar">{chips}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — CROP & TARGET YIELD
# ─────────────────────────────────────────────────────────────────────────────
def step1_setup():
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### 📋 Step 1 — Select Crop & Target Yield")
    st.markdown("These values will be used in all three nutrient equations.")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        crop = st.selectbox("🌽 Crop", ["Maize (Local)", "Maize (Hybrid)", "Kholar"], key="sel_crop")
    with col2:
        if "Maize" in crop:
            yield_opts = [40, 50]
        else:
            yield_opts = [8, 10]
        T = st.selectbox("🎯 Target Yield (q/ha)", yield_opts, key="sel_yield")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✅ Confirm & Proceed to Nutrient Selection", type="primary", use_container_width=True):
        engine_crop = "maize" if "Maize" in crop else "kholar"
        go(2, crop=engine_crop, target_yield=float(T),
           N_done=False, P_done=False, K_done=False,
           FN=None, FP=None, FK=None,
           N_urea=None, P_ssp=None, K_mop=None)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — NUTRIENT HUB / SELECTION
# ─────────────────────────────────────────────────────────────────────────────
def step2_hub():
    crop_label = "Maize" if "maize" in st.session_state.crop else "Kholar"
    T = st.session_state.target_yield

    st.markdown(f"""
    <div class="panel">
        <h3>🧭 Step 2 — Nutrient Selection Hub</h3>
        <p style="color:#78909c">Crop: <strong style="color:#cfd8dc">{crop_label}</strong>
        &nbsp;|&nbsp; Target Yield: <strong style="color:#cfd8dc">{T} q/ha</strong></p>
        <p>Select one nutrient at a time. Compute each independently.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Nutrient status cards ──
    c1, c2, c3 = st.columns(3)
    for col, nut_key in zip([c1, c2, c3], ["N", "P", "K"]):
        meta = NUTRIENT_META[nut_key]
        done = st.session_state[f"{nut_key}_done"]
        val_key = {"N": "FN", "P": "FP", "K": "FK"}[nut_key]
        val = st.session_state[val_key]

        card_cls = "nutrient-card done-card" if done else "nutrient-card"
        badge = f'<div class="nut-val">{val} kg/ha</div>' if done else '<div class="nut-pend">⏳ Pending</div>'
        status_icon = "✅" if done else "○"

        col.markdown(f"""
        <div class="{card_cls}">
            <div class="nut-icon">{meta['icon']}</div>
            <div class="nut-name">{status_icon} {meta['label']}</div>
            {badge}
        </div>
        """, unsafe_allow_html=True)

        with col:
            btn_label = "✏️ Recompute" if done else "▶ Compute"
            if st.button(btn_label, key=f"btn_hub_{nut_key}", use_container_width=True):
                go(3, active_nutrient=nut_key)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Navigation row ──
    bcol, fcol = st.columns([1, 3])
    with bcol:
        if st.button("← Back to Setup"):
            go(1)
    with fcol:
        if all_done():
            if st.button("🏁 View Final Summary →", type="primary", use_container_width=True):
                go(4)
        else:
            remaining = [NUTRIENT_META[n]["label"] for n in ["N","P","K"] if not st.session_state[f"{n}_done"]]
            st.info(f"Still pending: **{', '.join(remaining)}**. Compute all to unlock the summary.")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — INDIVIDUAL NUTRIENT PAGE
# ─────────────────────────────────────────────────────────────────────────────
def step3_nutrient():
    nut = st.session_state.active_nutrient   # "N", "P", or "K"
    meta = NUTRIENT_META[nut]
    crop = st.session_state.crop
    T    = st.session_state.target_yield

    crop_label = "Maize" if "maize" in crop else "Kholar"

    st.markdown(f"""
    <div class="panel">
        <h3>{meta['icon']} Step 3 — {meta['label']} ({meta['unit']})</h3>
        <p style="color:#78909c">Crop: <strong style="color:#cfd8dc">{crop_label}</strong>
        &nbsp;|&nbsp; T = <strong style="color:#cfd8dc">{T} q/ha</strong></p>
        <p>This page computes <strong>{meta['label']}</strong> ONLY. No other nutrient is touched.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input mode ──
    input_mode = st.radio(
        "Input method for this nutrient:",
        ["Fertility Class (Low / Medium / High)", "Direct Soil Test Value"],
        horizontal=True,
        key=f"imode_{nut}"
    )

    fc, raw_val = None, None
    soil_key = {"N": "SN (kg/ha)", "P": "SP (kg/ha)", "K": "SK (kg/ha)"}[nut]
    default_raw = {"N": 280.0, "P": 20.0, "K": 150.0}[nut]

    col_in = st.container()

    with col_in:
        if input_mode.startswith("Fertility"):
            fc = st.selectbox(f"{meta['label']} Soil Fertility", ["Low", "Medium", "High"], key=f"fc_{nut}")
            fc_display = fc.lower()
        else:
            raw_val = st.number_input(f"{soil_key}", min_value=0.0, step=1.0, value=default_raw, key=f"raw_{nut}")
            fc_display = FPEEngine._resolve_class_from_value(crop, raw_val, nut)
            st.info(f"**Detected Fertility Level:** {fc_display.capitalize()}")
            
            # Warnings logic
            if "maize" in crop:
                if nut == "N" and (raw_val < 225 or raw_val > 500):
                    st.warning("Value is outside typical Maize N bounds (225-500). Proceeding with extreme category.")
                elif nut == "P" and (raw_val < 22 or raw_val > 55):
                    st.warning("Value is outside typical Maize P bounds (22-55).")
                elif nut == "K" and (raw_val < 137 or raw_val > 337):
                    st.warning("Value is outside typical Maize K bounds (137-337).")
            elif "kholar" in crop:
                if nut == "N" and (raw_val < 100 or raw_val > 500):
                    st.warning("Value is outside typical Kholar N bounds (100-500).")
                elif nut == "P" and (raw_val < 10 or raw_val > 90):
                    st.warning("Value is outside typical Kholar P bounds (10-90).")
                elif nut == "K" and (raw_val < 90 or raw_val > 400):
                    st.warning("Value is outside typical Kholar K bounds (90-400).")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Compute button ──
    if st.button(f"⚡ Compute {meta['label']}", type="primary", use_container_width=True, key=f"cmp_{nut}"):
        try:
            if nut == "N":
                res = FPEEngine.compute_N(crop, T, fertility_class=fc, SN=raw_val)
                st.session_state.FN    = res["FN"]
                st.session_state.N_urea = res["urea_kg_ha"]
                st.session_state.N_eq  = res["equation"]
                st.session_state.N_done = True
            elif nut == "P":
                res = FPEEngine.compute_P(crop, T, fertility_class=fc, SP=raw_val)
                st.session_state.FP    = res["FP"]
                st.session_state.P_ssp = res["ssp_kg_ha"]
                st.session_state.P_eq  = res["equation"]
                st.session_state.P_done = True
            else:
                res = FPEEngine.compute_K(crop, T, fertility_class=fc, SK=raw_val)
                st.session_state.FK    = res["FK"]
                st.session_state.K_mop = res["mop_kg_ha"]
                st.session_state.K_eq  = res["equation"]
                st.session_state.K_done = True
            st.rerun()
        except Exception as e:
            st.error(f"Calculation error: {e}")

    # ── Show result if already computed ──
    done_key  = f"{nut}_done"
    val_map   = {"N": "FN",    "P": "FP",    "K": "FK"}
    conv_map  = {"N": "N_urea","P": "P_ssp", "K": "K_mop"}
    conv_lbls = {"N": "Urea",  "P": "SSP",   "K": "MOP"}
    eq_map    = {"N": "N_eq",  "P": "P_eq",  "K": "K_eq"}

    if st.session_state[done_key]:
        val  = st.session_state[val_map[nut]]
        conv = st.session_state[conv_map[nut]]
        clbl = conv_lbls[nut]
        st.markdown(f"""
        <div class="result-box">
            <div class="big-val">{val} kg/ha &nbsp;<span style="font-size:1rem;color:#78909c">({meta['unit']})</span></div>
            <div style="margin-top:0.5rem; color:#b0bec5;">→ {clbl}: <strong style="color:#fff">{conv} kg/ha</strong></div>
        </div>
        """, unsafe_allow_html=True)

    # ── Navigation ──
    st.markdown("<br>", unsafe_allow_html=True)
    n1, n2 = st.columns([1, 1])
    with n1:
        if st.button("← Back to Nutrient Hub"):
            go(2)
    with n2:
        if all_done():
            if st.button("🏁 View Final Summary →", type="primary", use_container_width=True):
                go(4)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — FINAL SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
def step4_summary():
    crop_label = "Maize" if "maize" in st.session_state.crop else "Kholar"
    T = st.session_state.target_yield

    st.markdown(f"""
    <div class="panel">
        <h3>🏁 Step 4 — Final Fertilizer Summary</h3>
        <p style="color:#78909c">Crop: <strong style="color:#cfd8dc">{crop_label}</strong>
        &nbsp;|&nbsp; Target Yield: <strong style="color:#cfd8dc">{T} q/ha</strong></p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    for col, nut, val_key, conv_key, conv_lbl, unit in [
        (c1, "N", "FN",  "N_urea","Urea",  "kg/ha N"),
        (c2, "P", "FP",  "P_ssp", "SSP",   "kg/ha P₂O₅"),
        (c3, "K", "FK",  "K_mop", "MOP",   "kg/ha K₂O"),
    ]:
        meta = NUTRIENT_META[nut]
        val  = st.session_state[val_key]
        conv = st.session_state[conv_key]
        col.markdown(f"""
        <div class="summary-card">
            <div style="font-size:2rem">{meta['icon']}</div>
            <div class="s-label">{meta['label']}</div>
            <div class="s-val">{val}</div>
            <div class="s-label" style="margin-top:0.1rem">{unit}</div>
            <div class="s-conv">→ {conv_lbl}: <strong>{conv} kg/ha</strong></div>
        </div>
        """, unsafe_allow_html=True)

    # ── Application schedule ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📅 Recommended Application Schedule")
    urea = st.session_state.N_urea
    ssp  = st.session_state.P_ssp
    mop  = st.session_state.K_mop

    sch_cols = st.columns(3)
    schedules = [
        ("At Sowing (Basal)", f"All SSP ({ssp} kg) + All MOP ({mop} kg) + {round(urea*0.5,1)} kg Urea"),
        ("30 Days After Sowing", f"{round(urea*0.25,1)} kg Urea"),
        ("60 Days After Sowing", f"{round(urea*0.25,1)} kg Urea"),
    ]
    for col, (timing, dose) in zip(sch_cols, schedules):
        col.markdown(f"""
        <div class="panel" style="text-align:center">
            <div style="font-size:0.8rem;color:#78909c">{timing}</div>
            <div style="font-size:0.95rem;color:#e0e0e0;margin-top:0.4rem;font-weight:600">{dose}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 AI-Driven Explainable Summary")
    with st.spinner("Generating detailed technical summary from AI..."):
        summary_table = get_explainable_summary_table(crop_label, T, urea, ssp, mop)
        st.markdown(summary_table)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Start New Recommendation", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────────────
render_header()
render_step_bar()

step = st.session_state.step
if   step == 1: step1_setup()
elif step == 2: step2_hub()
elif step == 3: step3_nutrient()
elif step == 4: step4_summary()
