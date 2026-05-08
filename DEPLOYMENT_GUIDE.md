# AgriSutra NE — Render Deployment Guide

## Final Repo Structure (target)

```
agrisutra-ne/                    ← mrinalireeti04/agrisutra-ne
├── app.py                       # Streamlit app (existing)
├── fpe_engine.py                # Core FPE logic (existing — DO NOT TOUCH)
├── nutrient_utils.py            # (existing)
├── input_enricher.py            # (existing)
├── output_enricher.py           # (existing)
├── delivery.py                  # (existing)
├── pages/                       # Streamlit pages (existing)
├── requirements.txt             # Streamlit deps (existing)
├── render.yaml                  # ← NEW: Render Blueprint
├── DEPLOYMENT_GUIDE.md          # ← NEW: this file
├── backend/                     # ← NEW: copied from Cray749/AgriNE
│   ├── __init__.py
│   ├── main.py                  # FIXED: relative imports → absolute
│   ├── fpe_engine.py            # copy from AgriNE backend
│   ├── nutrient_utils.py        # copy from AgriNE backend
│   ├── requirements.txt         # ← NEW: backend-only deps
│   ├── routers/
│   │   ├── __init__.py
│   │   └── recommend.py
│   └── models/
│       ├── __init__.py
│       └── schemas.py
└── flutter_app/                 # ← NEW: copied from Cray749/AgriNE
    ├── lib/
    ├── pubspec.yaml
    ├── web/
    └── build/
        └── web/                 # ← Built output committed to repo
```

---

## Step 1: Copy backend/ and flutter_app/ into your local repo

Open PowerShell and run:

```powershell
# Navigate to your local agrisutra-ne repo
cd "C:\Users\Hp\OneDrive\Desktop\IARI"

# Clone the AgriNE repo temporarily
git clone https://github.com/Cray749/AgriNE.git C:\Temp\AgriNE

# Copy backend folder
Copy-Item -Recurse -Force "C:\Temp\AgriNE\backend" ".\backend"

# Copy flutter_app folder
Copy-Item -Recurse -Force "C:\Temp\AgriNE\flutter_app" ".\flutter_app"
```

> **Note:** If `Cray749/AgriNE` is a collaborator's repo you can't clone privately,
> ask them to zip and send you `backend/` and `flutter_app/` folders, then copy them in.

---

## Step 2: Fix backend/main.py import (ALREADY DONE by Antigravity)

The file `backend/main.py` has been updated to use absolute imports.
**No further action needed on your part.**

Original broken line:
```python
from .routers import recommend   # ❌ relative import — crashes when run from repo root
```

Fixed to:
```python
from backend.routers import recommend   # ✅ absolute import — works with uvicorn backend.main:app
```

---

## Step 3: Build Flutter Web Locally

> **Prerequisites:** Flutter SDK must be installed.
> Check with: `flutter --version`
> Install from: https://docs.flutter.dev/get-started/install/windows

```powershell
# Navigate to the flutter_app folder inside your repo
cd "C:\Users\Hp\OneDrive\Desktop\IARI\flutter_app"

# Get dependencies
flutter pub get

# IMPORTANT: Update API base URL before building
# Open lib/services/api_client.dart (or wherever your base URL is defined)
# Change the base URL from localhost to your Render backend URL:
#   const String baseUrl = 'https://agrisutra-backend.onrender.com';
# (Use the actual Render URL after you deploy the backend service)

# Build for web
flutter build web --release

# The output will be at: flutter_app/build/web/
```

> **⚠️ Important:** The Flutter build must be committed to the repo because
> Render's Static Site service does not have Flutter SDK — it cannot build it.

---

## Step 4: Commit Everything to GitHub

```powershell
cd "C:\Users\Hp\OneDrive\Desktop\IARI"

# Stage all new files
git add backend/
git add flutter_app/
git add render.yaml
git add DEPLOYMENT_GUIDE.md

# Commit
git commit -m "feat: add FastAPI backend and Flutter web build for Render deployment"

# Push
git push origin main
```

---

## Step 5: Deploy on Render

### Option A — Automatic (Blueprint) — Recommended

1. Go to https://dashboard.render.com
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub account and select **`mrinalireeti04/agrisutra-ne`**
4. Render will detect `render.yaml` and show all 3 services automatically
5. Click **"Apply"** — Render will start deploying all 3 services

### Option B — Manual (one service at a time)

#### Backend (FastAPI)
1. **New** → **Web Service**
2. Connect repo: `mrinalireeti04/agrisutra-ne`
3. Settings:
   - **Name:** `agrisutra-backend`
   - **Root Directory:** `.` (leave blank = repo root)
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/health`

#### Streamlit App
1. **New** → **Web Service**
2. Connect same repo
3. Settings:
   - **Name:** `agrisutra-streamlit`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

#### Flutter Web
1. **New** → **Static Site**
2. Connect same repo
3. Settings:
   - **Name:** `agrisutra-flutter`
   - **Publish Directory:** `flutter_app/build/web`
   - **Build Command:** *(leave blank — build is pre-committed)*

---

## Step 6: Set Environment Variables on Render

For **both** `agrisutra-backend` and `agrisutra-streamlit`, go to:
**Dashboard → Service → Environment → Add Environment Variable**

| Variable Name | Value | Notes |
|---|---|---|
| `GOOGLE_API_KEY` | `your-gemini-api-key` | Get from https://aistudio.google.com/app/apikey |
| `PYTHON_VERSION` | `3.11` | Set in render.yaml already |

> **Do NOT set `GCP_PROJECT_ID`** unless you are using Vertex AI.
> The code falls back to direct Gemini API via `GOOGLE_API_KEY` automatically.

---

## Step 7: Verify Deployment

Once all services are live, test each URL:

```bash
# 1. Backend health check
curl https://agrisutra-backend.onrender.com/health
# Expected: {"status": "ok", "service": "AgriSutra NE API"}

# 2. Backend docs (Swagger UI)
# Open in browser: https://agrisutra-backend.onrender.com/docs

# 3. Streamlit app
# Open in browser: https://agrisutra-streamlit.onrender.com

# 4. Flutter web
# Open in browser: https://agrisutra-flutter.onrender.com
```

> **⚠️ Free tier cold starts:** Render's free tier spins down services after 15 minutes
> of inactivity. The first request after idle will take ~30 seconds to respond.
> This is expected — upgrade to Starter plan ($7/mo) to avoid this.
