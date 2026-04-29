class FPEEngine:
    # Approximate soil nutrient values (kg/ha) if raw data is missing
    DEFAULT_SOIL_VALUES = {
        "low": {"SN": 150.0, "SP": 10.0, "SK": 100.0},
        "medium": {"SN": 280.0, "SP": 20.0, "SK": 150.0},
        "high": {"SN": 400.0, "SP": 35.0, "SK": 300.0}
    }

    @classmethod
    def compute(cls, crop: str, soil_class: str = None, SN: float = None, SP: float = None, SK: float = None, target_yield: float = None) -> dict:
        """
        Computes Fertilizer Prescription Equation (FPE) for given crop.
        Returns N, P2O5, K2O in kg/ha.
        """
        if not target_yield:
            raise ValueError("target_yield is required from the system.")

        crop = crop.lower()
        if soil_class:
            soil_class = soil_class.lower()

        # Auto-map soil class to approximate values if SN, SP, SK are not provided
        if SN is None or SP is None or SK is None:
            if not soil_class or soil_class not in cls.DEFAULT_SOIL_VALUES:
                raise ValueError("Must provide either raw soil values (SN, SP, SK) or a valid soil_class (low, medium, high).")
            
            defaults = cls.DEFAULT_SOIL_VALUES[soil_class]
            SN = SN if SN is not None else defaults["SN"]
            SP = SP if SP is not None else defaults["SP"]
            SK = SK if SK is not None else defaults["SK"]

        # Determine which soil class equation to use if only values are provided
        if not soil_class:
            if SN < 280:
                calc_class = "low"
            elif SN > 400:
                calc_class = "high"
            else:
                calc_class = "medium"
        else:
            calc_class = soil_class

        if "maize" in crop:
            return cls._compute_maize(calc_class, SN, SP, SK, target_yield)
        elif "kholar" in crop:
            return cls._compute_kholar(calc_class, SN, SP, SK, target_yield)
        else:
            raise ValueError(f"Crop '{crop}' is not currently supported.")

    @classmethod
    def _compute_maize(cls, calc_class: str, SN: float, SP: float, SK: float, T: float) -> dict:
        if calc_class == "low":
            FN = 3.93 * T - 0.26 * SN
            FP = 1.28 * T - 0.87 * SP
            FK = 1.77 * T - 0.09 * SK
        elif calc_class == "medium":
            FN = 4.11 * T - 0.36 * SN
            FP = 1.97 * T - 1.66 * SP
            FK = 2.09 * T - 0.22 * SK
        else: # high
            FN = 4.87 * T - 0.41 * SN
            FP = 3.86 * T - 2.81 * SP
            FK = 2.98 * T - 0.34 * SK

        return {
            "N": min(300.0, max(0.0, round(FN, 2))),
            "P2O5": min(300.0, max(0.0, round(FP, 2))),
            "K2O": min(300.0, max(0.0, round(FK, 2)))
        }

    @classmethod
    def _compute_kholar(cls, calc_class: str, SN: float, SP: float, SK: float, T: float) -> dict:
        if calc_class == "low":
            FN = 23.76 * T - 0.52 * SN
            FP = 11.45 * T - 1.89 * SP
            FK = 9.65 * T - 0.21 * SK
        elif calc_class == "medium":
            FN = 25.26 * T - 0.57 * SN
            FP = 12.37 * T - 1.88 * SP
            FK = 11.42 * T - 0.31 * SK
        else: # high
            FN = 26.45 * T - 0.63 * SN
            FP = 14.11 * T - 1.97 * SP
            FK = 12.17 * T - 0.33 * SK

        return {
            "N": min(300.0, max(0.0, round(FN, 2))),
            "P2O5": min(300.0, max(0.0, round(FP, 2))),
            "K2O": min(300.0, max(0.0, round(FK, 2)))
        }

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    print("--- FPE Engine Example ---")
    
    # Example 1: Using only soil class
    print("Maize (Medium Soil, Target Yield 40 q/ha):")
    res1 = FPEEngine.compute(crop="maize", soil_class="medium", target_yield=40)
    print(res1)
    
    # Example 2: Using raw soil test values
    print("\\nKholar (Raw Values: SN=160, SP=15, SK=110, Target Yield 12 q/ha):")
    res2 = FPEEngine.compute(crop="kholar", soil_class="low", SN=160, SP=15, SK=110, target_yield=12)
    print(res2)

# ==========================================
# FastAPI Integration Snippet
# ==========================================
\"\"\"
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class FPERequest(BaseModel):
    crop: str
    soil_class: Optional[str] = None
    SN: Optional[float] = None
    SP: Optional[float] = None
    SK: Optional[float] = None
    target_yield: float

@app.post("/api/v1/fpe/compute")
def compute_fpe(req: FPERequest):
    try:
        result = FPEEngine.compute(
            crop=req.crop,
            soil_class=req.soil_class,
            SN=req.SN,
            SP=req.SP,
            SK=req.SK,
            target_yield=req.target_yield
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
\"\"\"
