# 🌾 AgriSutra NE
### *A Rule-Based, AI-Assisted Fertilizer Recommendation System for Kiphire District and Similar Hill Agro-Climatic Regions of Northeast India*

---

> **Design Philosophy:**
> *"The system is designed to start as a rule-based expert system and progressively evolve into a data-driven adaptive model as localized farmer data is collected."*

---

## What Is This Project?

**AgriSutra NE** is a smart agricultural advisory tool designed for smallholder farmers in the hill agro-climatic zones of Northeast India — beginning with **Kiphire district, Nagaland**, and expanding to similar regions as the system matures.

It tells each farmer — in their own language — exactly **which fertilizers to apply, in what quantity, and in what sequence** — based on their crop, soil condition, land type, and farming history.

The name "AgriSutra" means *agricultural formula* — a precise, science-backed recipe tailored to each farmer's field.

> **Current Scope (v1):** Kiphire district and agro-climatically similar hill regions of Northeast India.
> **Planned Expansion:** Broader NE India as localized data is collected season over season.

---

## The Problem We Are Solving

Farmers in Kiphire and similar NE hill districts face a set of deeply interconnected challenges that no existing agricultural tool addresses:

### 1. Fertilizer decisions are guesswork
Most farmers apply fertilizer based on habit, neighbour advice, or what the local shop stocks — not science. This leads to:
- **Overuse of nitrogen** → soil acidification, money wasted
- **Underuse of phosphorus** → stunted root development
- **Wrong ratios** → crops that cannot reach their natural yield potential

### 2. Every existing tool ignores this region
Agricultural apps are built for Punjab, Haryana, or AP. Their data, their rules, and their assumptions have **no validity** in Kiphire's:
- Acidic, nutrient-deficient hill soils
- Extreme and uneven rainfall patterns
- Shifting cultivation and terrace farming systems
- Local crops like **Kholar** that don't appear in any national database

### 3. Language is a real barrier
Primary farmers in Kiphire speak Nagamese or Hindi. Existing tools are in English and require literacy and digital fluency that most farmers do not have. A voice interface in the local language is not an add-on feature — it is fundamental to usability.

### 4. No system remembers anything
Every season, every farmer starts from scratch. There is no record of:
- What fertilizers were applied last season
- What soil condition looked like
- What yield was achieved
- Whether soil health is getting better or worse

Every mistake gets repeated. Every hard-won learning is lost.

---

## Design Approach — How AgriSutra NE Works

AgriSutra NE is built in **three progressive phases**. What gets built first is lean, deployable, and scientifically grounded. What comes later is added only after real data exists to justify it.

```
Phase 1 → Rule-based recommendation engine + farmer identity + basic storage
Phase 2 → Rule-based yield estimation + history insights + simple personalization
Phase 3 → ML yield prediction + adaptive personalization + voice AI
```

This is not a limitation — it is the correct engineering approach.

---

## Stage-by-Stage Explanation

---

### Stage 1: Farmer Identity — Login and Profile

The farmer creates an account using their **phone number and OTP** — no passwords, no complicated forms. Once registered, the system retains their identity permanently across seasons.

**What gets stored:**
- Name, village, block, district
- Location (GPS auto-detected, editable)
- Land size (acres or hectares)
- Land type (Upland / Lowland / Terrace field)
- Crops grown in past seasons (filled in over time)

This identity layer is the foundation of everything. Without knowing who the farmer is, no personalization, no history, and no long-term learning is possible.

---

### Stage 2: Input — What the Farmer Tells the System

The system asks for only what a real farmer in Kiphire can actually provide. Inputs are split into two levels:

#### Level 1 — Default (covers ~80% of farmers)

| Input | Options |
|---|---|
| Crop | Maize (Local) / Maize (Hybrid) / Kholar |
| Soil fertility | Low / Medium / High |
| Previous crop (optional) | Fallow / Maize / Kholar / Other |
| Land type | Upland / Lowland / Terrace |

This is enough. A recommendation can be generated from only these four fields.

#### Level 2 — Advanced (for officers or farmers with soil test results)

| Input | Notes |
|---|---|
| Nitrogen (N) in kg/ha | From soil test report |
| Phosphorus (P₂O₅) in kg/ha | From soil test report |
| Potassium (K₂O) in kg/ha | From soil test report |
| Soil pH | 4.0–9.0 range |

**Important design decision:** The system does **not** ask the farmer for a target yield. Farmers in this region don't think in quintals per hectare — they think in terms of whether last season was good or bad. The system estimates yield internally. The farmer is never asked to do maths.

**Voice input is available for all Level 1 fields** in Phase 1 (Hindi and Assamese), with Nagamese added in Phase 3 as the language dataset matures.

---

### Stage 3: The System Reviews Farmer History

Before generating a recommendation, the system checks whether this farmer has any past records:

- **If this is Season 1:** Use regional defaults for Kiphire hill soils. No history adjustment.
- **If Season 2+:** Review what was applied last season, what yield was reported, and whether soil condition has changed.

This history check is read-only in Phase 1 — it surfaces information but does not yet automatically adjust recommendations. That adjustment logic begins in Phase 2 once there is enough real data to validate it.

---

### Stage 4: Geo-Intelligence — Keeping It Realistic

In Phase 1, the system uses **hardcoded block-level rainfall and temperature averages** for Kiphire district. These are derived from publicly available IMD and district agriculture office data, not live APIs.

This is intentional: live API calls add complexity, latency, and failure points that are unnecessary when the system covers a single district where climate patterns are relatively consistent.

**Phase 2 addition:** Block-level averages refined using historical NASA POWER data.  
**Phase 3 addition:** Live NASA POWER API calls for precise, real-time geo-intelligence.

---

### Stage 5: Yield Estimation

The system always generates a yield estimate — the farmer never has to provide one.

#### Phase 1 — Rule-Based Yield Range

Simple lookup table based on crop, variety, and soil fertility:

| Crop | Variety | Soil Fertility | Estimated Yield Range |
|---|---|---|---|
| Maize | Local | Low | 18–25 q/ha |
| Maize | Local | Medium | 26–35 q/ha |
| Maize | Local | High | 36–45 q/ha |
| Maize | Hybrid | Low | 25–35 q/ha |
| Maize | Hybrid | Medium | 36–48 q/ha |
| Maize | Hybrid | High | 49–60 q/ha |
| Kholar | — | Low | 6–10 q/ha |
| Kholar | — | Medium | 11–16 q/ha |
| Kholar | — | High | 17–22 q/ha |

The system picks the midpoint of the range as the working estimate and uses this to drive the fertilizer calculation.

**The output to the farmer is simple:**
> *"For your field conditions, we are targeting a yield of around 30 quintals per hectare."*

#### Phase 3 — ML-Based Yield Prediction
Once at least 2–3 seasons of real farmer data from Kiphire is collected, an XGBoost regression model will be trained on this localized dataset. National datasets (Kaggle, etc.) will not be used as primary training data — they are not valid proxies for Kiphire hill conditions.

---

### Stage 6: The Core Decision Engine — The Science (FPE Engine)

This is the scientific heart of the system. It is based on the **STCR (Soil Test Crop Response) methodology** established by ICAR — India's standard framework for fertilizer prescription.

We have designed a clean, modular `FPEEngine` that easily plugs into our FastAPI backend. 

**Backend Pipeline Integration:**
`Input Layer → Yield Estimation → FPE Engine → Fertilizer Conversion`

The rule engine takes:
- Crop type
- Soil fertility class (Low / Medium / High) or actual N, P, K values (SN, SP, SK)
- Estimated yield target (T) — generated internally, never asked of the farmer.

And outputs the **Fertilizer Prescription Equation (FPE)** — the quantities of N, P₂O₅, and K₂O in kg/ha, strictly clamping any negative unrealistic outputs to zero. 

**The Equations:**

**Maize:**
- **Low Soil:** FN = 3.93T - 0.26SN | FP₂O₅ = 1.28T - 0.87SP | FK₂O = 1.77T - 0.09SK
- **Medium Soil:** FN = 4.11T - 0.36SN | FP₂O₅ = 1.97T - 1.66SP | FK₂O = 2.09T - 0.22SK
- **High Soil:** FN = 4.87T - 0.41SN | FP₂O₅ = 3.86T - 2.81SP | FK₂O = 2.98T - 0.34SK

**Kholar:**
- **Low Soil:** FN = 23.76T - 0.52SN | FP₂O₅ = 11.45T - 1.89SP | FK₂O = 9.65T - 0.21SK
- **Medium Soil:** FN = 25.26T - 0.57SN | FP₂O₅ = 12.37T - 1.88SP | FK₂O = 11.42T - 0.31SK
- **High Soil:** FN = 26.45T - 0.63SN | FP₂O₅ = 14.11T - 1.97SP | FK₂O = 12.17T - 0.33SK

If the farmer only inputs their soil class (Low/Medium/High) without raw values, the `FPEEngine` intelligently maps them to approximate values to complete the calculations.

---

### Stage 7: Converting Nutrients into Fertilizer Products

Farmers buy products from shops — not abstract nutrients. The system converts:

| Nutrient Required | Fertilizer Product | Conversion |
|---|---|---|
| Nitrogen (N) | Urea | Urea kg = N ÷ 0.46 |
| Phosphorus (P₂O₅) | SSP (Single Super Phosphate) | SSP kg = P₂O₅ ÷ 0.16 |
| Potassium (K₂O) | MOP (Muriate of Potash) | MOP kg = K₂O ÷ 0.60 |
| Organic matter | FYM (Farm Yard Manure) | 5–10 tonnes/ha based on soil class |

The output also includes an **application schedule** — the farmer is told exactly when to apply each product:
- **At sowing (Basal dose):** 100% P + 100% K + 50% N
- **30 days after sowing:** 25% N
- **60 days after sowing:** 25% N

---

### Stage 8: Personalization — Phased and Honest

Personalization requires data. It cannot be applied from Day 1.

#### Phase 1 — History storage only
The system stores this season's inputs, recommendation, and (later) the actual yield. No automatic adjustments are made yet.

#### Phase 2 — Simple rule-based adjustments
Once a farmer has at least one past season on record, simple checks apply:

| What the System Finds | What It Does |
|---|---|
| Last season yield was significantly below estimate | Suggest increasing FYM application |
| Farmer reported very poor crop | Flag for KVK officer review |
| Same soil class for 3+ seasons with no soil test | Prompt farmer to get a soil health card |

#### Phase 3 — Data-driven personalization
Trend detection (soil degradation, nutrient imbalance) and automatic nutrient adjustments based on multi-season patterns. This requires 3+ seasons of data per farmer.

---

### Stage 9: Explaining the Recommendation

The system does not output blind numbers. Every recommendation comes with a plain-language explanation written in simple, farmer-facing terms:

> *"Your soil has low nitrogen. Maize needs a lot of nitrogen to grow well. Because your target yield is medium, we recommend 100 kg of Urea per hectare. Apply half at sowing and the rest in two equal doses later."*

This explanation is **rule-generated** — not AI-computed. Each output is assembled from templated sentences based on the inputs. This is more reliable, more auditable, and more easily translatable than any model-generated text.

**SHAP visualizations** (technical feature importance charts) will be available in the admin/researcher dashboard for internal analysis — but are intentionally kept off the farmer-facing interface.

---

### Stage 10: Voice Interface — Realistic Rollout

#### Phase 1 (Launch)
- **Languages:** Hindi, Assamese
- **Input:** Farmer speaks crop name and soil condition; system parses using OpenAI Whisper
- **Output:** Recommendation read aloud using AI4Bharat TTS

#### Phase 3 (After data collection)
- **Nagamese added** via custom speech dataset collection and Whisper fine-tuning
- This requires real Nagamese audio data — it cannot be assumed to work out of the box

Nagamese has limited digital text and audio corpora. Claiming Phase 1 Nagamese support would be technically dishonest and would be questioned in any serious evaluation.

---

### Stage 11: Farmer Dashboard

Each farmer has a personal record-keeping view that shows:

- **This season:** Current recommendation and application schedule
- **Last season:** What was recommended, what was reported as yield
- **Soil trend:** Simple Low/Medium/High classification across recorded seasons
- **History table:** Every season's crop, recommendation, and yield

The dashboard grows in richness as more seasons are recorded. In Season 1 it shows only the current recommendation. By Season 4 it shows meaningful trends.

---

### Stage 12: Feedback Loop — The System Learns Over Time

After the harvest, the system prompts the farmer with one simple question:

> *"How did your crop do this season? Better than usual / Same as usual / Worse than usual"*

For farmers working with field officers who can provide exact numbers:

> *"Actual yield: ___ quintals per hectare"*

The system:
1. Stores the response against this season's recommendation
2. Computes the gap between estimated yield and reported yield
3. Flags large discrepancies for manual review by KVK officer
4. Feeds clean data into the ML training pipeline (Phase 3)

Over multiple seasons, the system accumulates a localized Kiphire-specific dataset — something that has never existed before and cannot be replicated from any national data source.

---

## What Makes This System Defensible

| Claim | Why It Holds Up |
|---|---|
| "Designed for Kiphire hill conditions" | Rules, yield tables, and soil classes are calibrated to Kiphire — not national averages |
| "Expert-derived Kholar rules" | Derived from qualified agronomist consultation — clearly stated as baselines |
| "Phase 1 is deployable now" | Core engine requires only crop + soil fertility as inputs — available without lab tests |
| "ML comes later, when data exists" | Prevents the circular logic of training on synthetic data generated by the same rules |
| "Grows smarter each season" | Feedback loop architecture is in place from Day 1, even if ML isn't |

---

## Competitive Comparison

| Feature | AgriSutra NE | Generic Agricultural Apps |
|---|---|---|
| Designed for Kiphire hill soils | ✅ Yes | ❌ No |
| Kholar crop included | ✅ Yes | ❌ Not anywhere |
| Works without a soil test | ✅ Yes (Level 1 input) | ❌ Usually requires test |
| STCR-based rule engine | ✅ Yes | ❌ Rarely |
| Farmer history and memory | ✅ Yes | ❌ No |
| Voice in Hindi / Assamese | ✅ Phase 1 | ❌ No |
| Voice in Nagamese | ✅ Phase 3 | ❌ No |
| Explains every recommendation | ✅ Plain language | ❌ Rarely |
| Feedback loop for learning | ✅ Yes | ❌ No |
| Honest about ML limitations | ✅ Yes | — |

---

## Crops Supported

### 🌽 Maize

Two varieties:
- **Local Maize** — traditional, lower input requirements, resilient to hill conditions
- **Hybrid Maize** — improved varieties requiring higher, more precisely calibrated inputs

Both calibrated to Kiphire district soil and rainfall conditions.

### 🌿 Kholar

A pulse/legume crop central to the food and farming systems of Nagaland and similar NE hill districts. No national fertilizer recommendation tool covers Kholar. AgriSutra NE provides the first structured, expert-derived fertilizer baseline for this crop — a genuine and verifiable contribution to the regional agricultural knowledge base.

---

## Data Sources

| Data Type | Source | Use in System |
|---|---|---|
| Soil health baseline | Soil Health Card portal (soilhealth.dac.gov.in) | Soil fertility classification |
| Crop yield — NE states | State agriculture department reports | Yield range calibration |
| Rainfall and temperature | IMD district-level averages + NASA POWER (Phase 2) | Geo-intelligence layer |
| Agronomic FPE tables | Krishikosh (ICAR research repository) | Rule engine tables |
| Kholar-specific rules | Expert agronomist consultation | Kholar FPE baseline |
| Multilingual NLP | AI4Bharat (IIT Madras) | Voice output |
| Voice understanding | OpenAI Whisper | Voice input |

Synthetic data generation (running the rule engine across parameter combinations) is used to supplement training data in Phase 3 — but is clearly distinguished from real field observations.

---

## Technology Stack

| Component | Technology | Phase |
|---|---|---|
| Core rule engine | Python 3.11 | 1 |
| Backend API | FastAPI | 1 |
| Frontend UI | Streamlit | 1 |
| Database | PostgreSQL | 1 |
| Authentication | Firebase OTP | 1 |
| Rule-based yield estimation | Python lookup tables | 1–2 |
| Geo-intelligence (static) | Hardcoded district averages | 1 |
| Geo-intelligence (dynamic) | NASA POWER API | 2 |
| Voice input | OpenAI Whisper | 2 |
| Voice output | AI4Bharat TTS | 2 |
| ML yield model | XGBoost / Scikit-learn | 3 |
| Personalization engine | Rule-based → data-driven | 2–3 |
| Nagamese voice | Whisper fine-tuned | 3 |
| Deployment | Render + Streamlit Cloud | 1 |

---

## Who Will Use This

**Primary Users:**
- Smallholder farmers (0.5–5 acres) in Kiphire district and similar NE hill areas
- Block-level agriculture officers conducting farm visits
- Krishi Vigyan Kendra (KVK) extension workers

**Secondary Users:**
- State agriculture departments tracking crop-wise fertilizer consumption
- ICAR researchers needing field-level soil and yield data from NE hill regions

---

## The Bigger Vision

AgriSutra NE begins small and specific — Kiphire, two crops, rule-based logic. This is intentional.

Each season it operates:
- The farmer database grows
- The feedback dataset grows
- The yield model becomes trainable on real local data
- The recommendations become empirically validated, not just theoretically derived

After 3–5 seasons of operation, AgriSutra NE will hold the **only structured, farmer-level soil and yield dataset for Kiphire district** — data that has never existed before and cannot be downloaded from any public repository.

That dataset is the real long-term asset. The algorithm is the vehicle. **The data is the moat.**

This positions AgriSutra NE for meaningful expansion:
- District by district across Nagaland
- Then into Manipur, Mizoram, and Meghalaya hill belts
- Eventually covering all NE hill agro-climatic regions

Each expansion uses the same architecture with locally calibrated rule tables — making scale systematic, not speculative.

---

## Development Roadmap

| Phase | Timeline | Deliverables |
|---|---|---|
| Phase 1 | Weeks 1–4 | Rule engine, fertilizer output, farmer login, PostgreSQL storage, Streamlit UI |
| Phase 2 | Weeks 5–8 | History insights, simple personalization, NASA API, Hindi + Assamese voice |
| Phase 3 | Post-deployment | ML yield model (on real data), advanced personalization, Nagamese voice |

---

## Summary

AgriSutra NE is a **science-backed, farmer-first fertilizer recommendation system** built for the hill agro-climatic conditions of Kiphire district, Nagaland — with a clear architecture for scaling across Northeast India.

It starts with what can be built reliably and used today: STCR-based expert rules, a two-level input system that works without lab tests, farmer identity and seasonal records, and plain-language explanations in Hindi and Assamese.

It grows into what the data will eventually justify: machine learning yield prediction, adaptive personalization, and multilingual voice AI — built on real local observations, not national generalizations.

It is not a generic tool retrofitted to NE India. It is a system **designed from the ground up for this soil, this climate, and this farmer.**

> *"The right fertilizer. The right amount. The right reason. In your language."*

---

*Document prepared as part of the AgriSutra NE project proposal — IARI Incubation.*
*Primary crops: Maize (Local & Hybrid), Kholar | Initial region: Kiphire district, Nagaland*
*Version 2.0 — Revised for field realism and incubation evaluation*
