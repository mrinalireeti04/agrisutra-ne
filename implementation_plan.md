# Project Addition Plan: Pre/Post Processing and Delivery Layers

The goal is to cleanly integrate new features around the core FPE engine without modifying its logic. This involves adding pre-processing (input enrichment), post-processing (output enrichment), and delivery mechanisms (PDF, History, Dashboard).

## User Review Required
> [!IMPORTANT]
> - **Dependencies**: I will add `requests`, `fpdf2`, `pandas`, and `plotly` to `requirements.txt`. Are there any version constraints I should be aware of?
> - **NASA POWER API**: Fetching live data requires latitude and longitude. I will add mock lat/lon inputs or a simple location selector to test the API call. Does this align with your vision for the MVP?

## Proposed Changes

### Pre-processing Layer
#### [NEW] [input_enricher.py](file:///c:/Users/Hp/OneDrive/Desktop/IARI/input_enricher.py)
- Create `get_weather_context(lat, lon)` to fetch monthly rainfall from NASA POWER API.
- Create `evaluate_ph(ph_value)` to return a `lime_needed` boolean flag.

---

### Post-processing Layer
#### [NEW] [output_enricher.py](file:///c:/Users/Hp/OneDrive/Desktop/IARI/output_enricher.py)
- Create `enrich_output(FN, FP, FK, go_organic=False, fym_tonnes=0)` to clamp negative values to 0 and apply FYM nutrient deductions (P credit = 2.5 * FYM, K credit = 5.0 * FYM).

---

### Delivery Layer & History
#### [NEW] [delivery.py](file:///c:/Users/Hp/OneDrive/Desktop/IARI/delivery.py)
- Create `generate_pdf_report(...)` using `fpdf2` to export prescription cards.
- Create `save_to_history(...)` using `sqlite3` to store recommendations locally.
- Create `get_whatsapp_link(...)` to format a `wa.me` URL with the final recommendation.

#### [NEW] [pages/dashboard.py](file:///c:/Users/Hp/OneDrive/Desktop/IARI/pages/dashboard.py)
- Create a new Streamlit page to read the SQLite database.
- Visualize historical data (Yield vs Target, Fertilizer Usage) using Plotly charts.

---

### Frontend Integration
#### [MODIFY] [app.py](file:///c:/Users/Hp/OneDrive/Desktop/IARI/app.py)
- **Step 1**: Replace target yield dropdown with a flexible `st.number_input`. Add a land area input (hectares/acres).
- **Step 3/4**: Add a pH input field. Pass this through `input_enricher.py` to get the `lime_needed` flag.
- **Step 4**: Multiply the final kg/ha values by the land area to show the total required for the farmer's plot.
- **Step 4**: Pass the FPE engine outputs through `output_enricher.py` before converting to Urea/SSP/MOP.
- **Step 4**: Call `save_to_history` when the recommendation is complete.
- **Step 4**: Display "Download PDF" and "Share on WhatsApp" buttons.
- **Step 4**: Append the NASA weather context and `lime_needed` flag to the Gemini AI explainability prompt.

#### [MODIFY] [requirements.txt](file:///c:/Users/Hp/OneDrive/Desktop/IARI/requirements.txt)
- Add `fpdf2`, `plotly`, `pandas`, and `requests`.

## Verification Plan
### Automated Tests
- N/A (Rule-based features)

### Manual Verification
1. Run `streamlit run app.py` and input custom yield targets and land sizes. Verify the total kg scales correctly.
2. Enter a pH < 5.5 and confirm the AI summary mentions lime application.
3. Select the Organic pathway and verify that P and K requirements decrease based on FYM credits.
4. Click the "Download PDF" button and inspect the generated file.
5. Click the "Share on WhatsApp" link and verify the message text.
6. Navigate to the new Dashboard page and verify the history charts reflect recent calculations.
