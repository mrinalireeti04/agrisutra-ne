# 🌾 AgriSutra NE

**A Rule-Based Fertilizer Recommendation System for Kiphire District and Similar Hill Agro-Climatic Regions of Northeast India.**

## Overview

AgriSutra NE is a smart agricultural advisory tool designed for smallholder farmers. It provides scientifically backed, hyper-personalized fertilizer prescriptions based on the **STCR (Soil Test Crop Response)** methodology. The system tells farmers exactly which fertilizers to apply, in what quantities, and when—all through a highly accessible, mobile-first interface.

### Current Scope (MVP)
- **Target Geography:** Kiphire district, Nagaland.
- **Supported Crops:** Maize (Local), Maize (Hybrid), Kholar (legume).
- **Primary Mechanism:** Rule-based Core Decision Engine (FPE Engine) that dynamically adapts to Soil Classes (Low/Medium/High) or raw soil test values.

---

## 🚀 Features

- **Robust FPE Engine:** Calculates required Nitrogen, Phosphorus, and Potassium (N, P₂O₅, K₂O) precisely clamped to realistic biological limits.
- **Smart Fallbacks:** Dynamically Maps Soil Fertility classes to exact raw values if soil tests are unavailable.
- **Farmer-First UI:** Built on Streamlit with a soft green, agriculture-themed design featuring minimal inputs and large, readable results.
- **Trust-Building Explanations:** Every recommendation includes an auto-generated, plain-language breakdown of *why* the inputs are suggested.
- **Conversion to Products:** Output is converted directly to what farmers buy: Urea, SSP (Single Super Phosphate), MOP (Muriate of Potash), and FYM (Farm Yard Manure).

---

## 🛠️ Technology Stack

- **Frontend / UI Layer:** [Streamlit](https://streamlit.io/)
- **Core Engine:** Python (Vanilla classes, zero ML overhead for MVP)
- **Validation:** Pydantic

---

## 💻 Running the Project Locally

### Prerequisites
Make sure you have Python 3.10+ installed.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/agrisutra-ne.git
   cd agrisutra-ne
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```
   The application will automatically open in your web browser at `http://localhost:8501`.

---

## ☁️ Deployment (Streamlit Cloud)

AgriSutra NE is designed to be instantly deployable to Streamlit Community Cloud.

1. Push your local code to a public or private GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in.
3. Click **New app**, select your repository, choose `main` as the branch, and set `app.py` as the Main file path.
4. Click **Deploy!**

---

*AgriSutra NE — Built for the soil, by the science, for the farmer.*
