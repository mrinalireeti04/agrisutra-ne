import os
import requests

def get_weather_context(lat, lon):
    """
    Fetches monthly rainfall for the given coordinates using NASA POWER API.
    Uses NASA_API_KEY from Streamlit secrets / env for higher rate limits.
    Returns a dictionary with the context, or None if the call fails.
    """
    if lat is None or lon is None:
        return None

    # Read key from secrets or environment (graceful — POWER API works without key too)
    try:
        import streamlit as st
        nasa_key = st.secrets.get("NASA_API_KEY") or os.environ.get("NASA_API_KEY", "DEMO_KEY")
    except Exception:
        nasa_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")

    try:
        url = (
            f"https://power.larc.nasa.gov/api/temporal/monthly/point"
            f"?parameters=PRECTOTCORR,T2M&community=AG"
            f"&longitude={lon}&latitude={lat}&format=JSON"
            f"&start=2023&end=2023"
            f"&api_key={nasa_key}"
        )
        # Timeout is 10s so the app doesn't hang if NASA POWER is slow
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        rainfall = data["properties"]["parameter"]["PRECTOTCORR"]
        avg_rain_mm = round(sum(rainfall.values()) / 12, 1)
        return {"avg_monthly_rainfall_mm": avg_rain_mm}
    except Exception:
        return None  # graceful fallback — app continues normally
