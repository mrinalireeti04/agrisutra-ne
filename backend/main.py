"""
AgriSutra NE — FastAPI Application Entry Point
================================================
Start command (development):
    uvicorn backend.main:app --reload --port 8000

Start command (Render / production):
    uvicorn backend.main:app --host 0.0.0.0 --port $PORT

Interactive API docs (development only):
    http://localhost:8000/docs      ← Swagger UI (best for testing)
    http://localhost:8000/redoc     ← ReDoc (clean read)

Test the health check immediately after start:
    GET http://localhost:8000/health  →  {"status": "ok", "service": "AgriSutra NE API"}
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import recommend          # absolute import — works with uvicorn backend.main:app

# ── App definition ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="AgriSutra NE API",
    description=(
        "STCR-based fertilizer recommendation engine for Northeast India. "
        "Provides scientifically-backed N / P / K prescriptions for Maize and Kholar "
        "using the Fertilizer Prescription Equation (FPE) methodology."
    ),
    version="1.0.0",
    contact={
        "name": "AgriSutra NE Dev Team",
    },
    license_info={
        "name": "MIT",
    },
)

# ── CORS — allow Flutter app and browser clients ───────────────────────────────
# During development:  allow all origins ("*") so local emulator can reach the server.
# Before production:   restrict allow_origins to your Railway domain:
#     allow_origins=["https://agrisutra-ne.up.railway.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # ← Tighten this before going live
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Router registration ────────────────────────────────────────────────────────
# /recommend  — core FPE prescription endpoint (Session 1)
app.include_router(recommend.router)

# Phase 2 placeholders — uncomment when auth.py is built
# from backend.routers import auth
# app.include_router(auth.router)


# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"], summary="Health check")
def health():
    """
    Returns a simple OK response.
    Used by:
      - Render to verify the service is running (healthCheckPath in render.yaml)
      - Flutter's api_client.dart to check connectivity before making requests
    """
    return {"status": "ok", "service": "AgriSutra NE API"}


# ── Root redirect ──────────────────────────────────────────────────────────────
@app.get("/", tags=["System"], summary="Root")
def root():
    """Redirect / to the Swagger docs during development."""
    return {
        "message": "AgriSutra NE API is running.",
        "docs": "/docs",
        "health": "/health",
    }
