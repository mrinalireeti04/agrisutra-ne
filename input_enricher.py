import requests

def evaluate_ph(ph_value):
    """
    Evaluates the soil pH and determines if lime application is needed.
    Returns a boolean flag. The FPE engine does not see this.
    """
    if ph_value is None:
        return False
    return ph_value < 5.5

def get_weather_context(lat, lon):
    """
    Fetches monthly rainfall for the given coordinates using NASA POWER API.
    Returns a dictionary with the context, or None if the call fails.
    """
    if lat is None or lon is None:
        return None
        
    try:
        url = (
            f"https://power.larc.nasa.gov/api/temporal/monthly/point"
            f"?parameters=PRECTOTCORR,T2M&community=AG"
            f"&longitude={lon}&latitude={lat}&format=JSON"
            f"&start=2023&end=2023"
        )
        # Timeout is 8s so the app doesn't hang if NASA POWER is slow
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        data = r.json()
        rainfall = data["properties"]["parameter"]["PRECTOTCORR"]
        avg_rain_mm = round(sum(rainfall.values()) / 12, 1)
        return {"avg_monthly_rainfall_mm": avg_rain_mm}
    except Exception:
        return None  # graceful fallback — app continues normally
