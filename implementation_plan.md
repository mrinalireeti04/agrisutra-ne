# Streamlit App Implementation & Deployment Plan for AgriSutra NE

This document outlines the end-to-end implementation and deployment plan for the AgriSutra NE frontend using Streamlit. It incorporates the requested UI/UX guidelines and integrates the newly built `FPEEngine`.

## User Review Required

> [!IMPORTANT]
> **Architecture Decision:** For an immediate and smooth deployment to **Streamlit Cloud**, it is highly recommended to run the application as a monolith. This means the Streamlit app (`app.py`) will directly import and use the `FPEEngine` from `fpe_engine.py`, bypassing the need for a separate FastAPI backend in this MVP. Streamlit Cloud is designed for running standalone Python web apps from a GitHub repository. Does this approach work for you for the initial deployment?

> [!IMPORTANT]
> **Deployment Capability:** I can initialize a local Git repository, create all the necessary files, and commit them. However, you will need to push this repository to your personal GitHub account and link it to your Streamlit Cloud dashboard. I will provide the exact steps to do this.

## Open Questions

> [!TIP]
> 1. Do you want me to automatically initialize the Git repository and make the initial commit on your machine as part of the execution?
> 2. Are you okay with me writing a simple rule-based yield estimator inside the app to provide the `target_yield` to the FPE Engine (based on the tables in the Project Idea document)?

## Proposed Changes

### Application Files

#### [NEW] [app.py](file:///c:/Users/Hp/OneDrive/Desktop/IARI/app.py)
This will be the main Streamlit application file.
- **UI Design**: Implementation of the clean, mobile-first, soft green theme using `st.markdown` with custom CSS.
- **Form Layout**: Header, Crop dropdown, Toggle for Soil Input (Fertility vs Raw Values), Land Type dropdown, and a large "Get Recommendation" button.
- **Voice Placeholder**: A visual section indicating "🎤 Voice Input (Coming Soon)".
- **Integration**: Importing `FPEEngine` and mapping form inputs to the `compute` function.
- **Helper Functions**: 
  - `estimate_yield()`: A simple rule-based fallback to calculate the target yield based on crop and soil class.
  - `convert_to_fertilizers()`: Converts raw N, P, K output into Urea, SSP, MOP, and FYM quantities.
- **Results Display**: Large metric cards showing the required fertilizers, the application schedule, and a simple textual explanation.

#### [NEW] [requirements.txt](file:///c:/Users/Hp/OneDrive/Desktop/IARI/requirements.txt)
Dependencies required for Streamlit Cloud deployment:
- `streamlit`
- `fastapi` (if needed for the backend snippet in fpe_engine, though not strictly required for the Streamlit MVP)
- `pydantic`

#### [NEW] [.gitignore](file:///c:/Users/Hp/OneDrive/Desktop/IARI/.gitignore)
Standard Python `.gitignore` to prevent committing unnecessary files (e.g., `__pycache__`, virtual environments).

## Verification Plan

### Automated Tests
- Run `streamlit run app.py` locally.
- Use the Browser tool to visually inspect the Streamlit UI, ensuring it matches the design requirements (soft green theme, large buttons, responsive layout).
- Verify the form submission correctly triggers the FPE Engine and displays the expected fertilizer output without errors.

### Manual Verification
- The user will be asked to run the app locally, confirm the design, and then follow the provided instructions to deploy the code to Streamlit Cloud.
