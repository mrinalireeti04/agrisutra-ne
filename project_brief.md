# 🌾 AgriSutra NE - Project Brief & Developer Handover

**Version:** 1.0
**Project Name:** AgriSutra NE (Agricultural Formula – North East)
**Target Geography:** Northeast India (Kiphire district, Assam, Nagaland, etc.)
**Platform:** Mobile-first Web Application

---

## 1. Executive Summary
**AgriSutra NE** is a hyper-personalized, AI-powered fertilizer recommendation system built exclusively for the agro-climatic realities of Northeast India. It uses the **STCR (Soil Test Crop Response)** methodology to provide scientifically backed fertilizer prescriptions. 

**One-line pitch:** *"AgriSutra NE tells every North-East farmer exactly what to put in their soil, why, and how much — in their own language."*

**Primary Crops Supported (v1):** Maize (Local & Hybrid), Kholar (region-specific legume).

---

## 2. Target Audience
- **Primary Farmer:** Smallholder (0.5–5 acres), limited literacy, local language speaker (Hindi, Assamese, Nagamese).
- **Progressive Farmer:** Medium landowner, data-aware, interested in yield optimization.
- **Agricultural Officer:** Uses aggregated data for policy and planning.

---

## 3. Core Capabilities
1. **Robust FPE Engine:** Calculates required Nitrogen (N), Phosphorus (P₂O₅), and Potassium (K₂O) based on specific soil data and target yield.
2. **Smart Fallbacks:** If a farmer doesn't have a soil test, it dynamically maps simple "Low/Medium/High" soil fertility classes to default raw values.
3. **Conversion to Real Products:** Converts scientific nutrient values directly to what farmers actually buy: Urea, SSP, MOP, and FYM.
4. **Trust-Building Explanations:** Generates plain-language breakdowns of *why* specific fertilizers are suggested.
5. **Multilingual Voice:** Supports voice inputs and outputs in local languages to assist low-literacy users.

---

## 🎨 4. For the Frontend Developer (UI/UX)

**Tech Stack:** React.js / Next.js (or Streamlit for MVP), TailwindCSS.
**Design Guidelines:** 
- Mobile-first (95% of users will be on cheap smartphones).
- Soft green, agriculture-themed design.
- High contrast, large readable text, minimal text input (use dropdowns, buttons, voice where possible).

### Landing Page Requirements
Create a visually appealing, trustworthy landing page to convert visitors (NGOs, progressive farmers, government officials):
1. **Hero Section:** Catchy headline ("Smart Farming for Northeast India"), sub-headline, and a primary Call to Action (CTA) like "Get Recommendation" or "Login via Phone". Include an image/illustration of a NE Indian farmer or green fields.
2. **Features Section:** Highlight the 4 pillars: Localized for NE, Science-backed (STCR), Voice-enabled, and Easy to understand.
3. **How It Works (3 Steps):** 
   - 1. Enter Crop & Soil Info.
   - 2. Get AI/STCR Recommendations.
   - 3. Apply exact amounts of Urea/SSP/MOP.
4. **Testimonials / Trust Badges:** Space for future farmer testimonials or agricultural institute logos.
5. **Footer:** Contact, About Us, Privacy Policy.

### App Dashboard Requirements
1. **Authentication:** Simple Phone Number + OTP login screen.
2. **Farmer Profile Setup:** Collect Name, Location (GPS auto-detect), and Land Size.
3. **Input Wizard:** 
   - Crop selection (Maize / Kholar).
   - Soil input (Radio buttons for Low/Med/High OR exact N-P-K values).
   - Target yield (optional).
   - Voice input button (Microphone icon) prominently displayed.
4. **Results Dashboard:**
   - **The Prescription:** A clear table or cards showing exact kg/ha of Urea, SSP, MOP, and FYM.
   - **Explainability Expanders:** "Why this recommendation?" showing simple bullet points (e.g., "Nitrogen is HIGH because your soil N is LOW").
   - **Historical Trends (v2):** Charts showing yield/health over past seasons.

---

## ⚙️ 5. For the Backend Developer

**Tech Stack:** Python 3.10+, FastAPI, PostgreSQL, Firebase Auth.

### Core Architecture
1. **Rule Engine (FPE Engine):** This is the heart of the app. It uses mathematical equations to convert Soil Test values and Target Yield into Nutrient Requirements (N, P, K), which are then converted into Fertilizer Amounts (Urea, SSP, MOP).
2. **APIs to Build:**
   - `POST /auth/otp`: Firebase OTP generation and verification.
   - `GET/POST /farmer/profile`: Manage user profiles (linked to phone number).
   - `POST /recommend`: Accepts crop type, soil data, and yield target -> Returns JSON with Urea, SSP, MOP, FYM amounts and explanation text.
   - `GET /geo/weather` (v2): Fetch data from NASA POWER API based on user GPS.
   - `POST /yield/predict` (v2): ML model (XGBoost) to predict target yield if the user leaves it blank.

### The FPE Logic (Example for Maize)
Your core Python class will implement these STCR equations. 
*(T = Target Yield, SN = Soil Nitrogen, SP = Soil Phosphorus, SK = Soil Potassium)*
- **Low Soil Fertility:**
  - Fertilizer N = `3.93*T - 0.26*SN`
  - Fertilizer P = `1.28*T - 0.87*SP`
  - Fertilizer K = `1.77*T - 0.09*SK`
- **Conversion to Products:**
  - `Urea (kg) = Fertilizer N / 0.46`
  - `SSP (kg) = Fertilizer P / 0.16`
  - `MOP (kg) = Fertilizer K / 0.60`

### Database Schema Overview (PostgreSQL)
- **Farmers:** `farmer_id`, `phone`, `name`, `location`, `land_size`
- **Soil Records:** `record_id`, `farmer_id`, `season`, `crop`, `soil_N`, `soil_P`, `soil_K`, `fertility_class`
- **Recommendations:** `rec_id`, `farmer_id`, `soil_record_id`, `urea_kg`, `ssp_kg`, `mop_kg`, `explanation`

---

## 6. Next Steps & Milestones
1. **Frontend:** Build the Landing Page UI and the basic input/output screens using mock data.
2. **Backend:** Setup FastAPI, create the `/recommend` endpoint with the core FPE math logic, and ensure it returns correct JSON.
3. **Integration:** Connect the React/Streamlit frontend to the FastAPI backend.
4. **Phase 2:** Add OTP Auth, Database storage, and Multilingual Voice features.
