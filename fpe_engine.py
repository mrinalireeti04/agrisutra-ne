from pydantic import BaseModel
from typing import Optional

class FPEEngine:
    # Approximate soil nutrient values (kg/ha) if raw data is missing
    DEFAULT_SOIL_VALUES = {
        "low": {"SN": 150.0, "SP": 10.0, "SK": 100.0},
        "medium": {"SN": 280.0, "SP": 20.0, "SK": 150.0},
        "high": {"SN": 400.0, "SP": 35.0, "SK": 300.0}
    }

    @classmethod
    def compute(cls, 
                crop: str, 
                target_yield: float,
                soil_n_class: str = None, 
                soil_p_class: str = None, 
                soil_k_class: str = None, 
                SN: float = None, 
                SP: float = None, 
                SK: float = None) -> dict:
        """
        Computes Fertilizer Prescription Equation (FPE) for given crop.
        Calculates N, P2O5, K2O independently based on separate N, P, K classes/values.
        """
        if not target_yield:
            raise ValueError("target_yield is required from the system.")

        crop = crop.lower()
        
        # Determine actual classes and values for each nutrient
        n_class, sn_val = cls._resolve_nutrient("N", soil_n_class, SN)
        p_class, sp_val = cls._resolve_nutrient("P", soil_p_class, SP)
        k_class, sk_val = cls._resolve_nutrient("K", soil_k_class, SK)

        if "maize" in crop:
            return cls._compute_maize(n_class, p_class, k_class, sn_val, sp_val, sk_val, target_yield)
        elif "kholar" in crop:
            return cls._compute_kholar(n_class, p_class, k_class, sn_val, sp_val, sk_val, target_yield)
        else:
            raise ValueError(f"Crop '{crop}' is not currently supported.")

    @classmethod
    def _resolve_nutrient(cls, nutrient_type: str, soil_class: str, val: float):
        if soil_class:
            soil_class = soil_class.lower()
            
        if val is None:
            if not soil_class or soil_class not in cls.DEFAULT_SOIL_VALUES:
                raise ValueError(f"Must provide either raw soil value or a valid class for {nutrient_type}.")
            val = cls.DEFAULT_SOIL_VALUES[soil_class][f"S{nutrient_type}"]
            calc_class = soil_class
        else:
            if not soil_class:
                if nutrient_type == "N":
                    calc_class = "low" if val < 280 else ("high" if val > 400 else "medium")
                elif nutrient_type == "P":
                    calc_class = "low" if val < 20 else ("high" if val > 35 else "medium")
                elif nutrient_type == "K":
                    calc_class = "low" if val < 150 else ("high" if val > 300 else "medium")
            else:
                calc_class = soil_class

        return calc_class, val

    @classmethod
    def _compute_maize(cls, n_class: str, p_class: str, k_class: str, SN: float, SP: float, SK: float, T: float) -> dict:
        # Nitrogen
        if n_class == "low":
            FN = 3.93 * T - 0.26 * SN
        elif n_class == "medium":
            FN = 4.11 * T - 0.36 * SN
        else:
            FN = 4.87 * T - 0.41 * SN

        # Phosphorus
        if p_class == "low":
            FP = 1.28 * T - 0.87 * SP
        elif p_class == "medium":
            FP = 1.97 * T - 1.66 * SP
        else:
            FP = 3.86 * T - 2.81 * SP

        # Potassium
        if k_class == "low":
            FK = 1.77 * T - 0.09 * SK
        elif k_class == "medium":
            FK = 2.09 * T - 0.22 * SK
        else:
            FK = 2.98 * T - 0.34 * SK

        return {
            "N": min(300.0, max(0.0, round(FN, 2))),
            "P2O5": min(300.0, max(0.0, round(FP, 2))),
            "K2O": min(300.0, max(0.0, round(FK, 2)))
        }

    @classmethod
    def _compute_kholar(cls, n_class: str, p_class: str, k_class: str, SN: float, SP: float, SK: float, T: float) -> dict:
        # Nitrogen
        if n_class == "low":
            FN = 23.76 * T - 0.52 * SN
        elif n_class == "medium":
            FN = 25.26 * T - 0.57 * SN
        else:
            FN = 26.45 * T - 0.63 * SN

        # Phosphorus
        if p_class == "low":
            FP = 11.45 * T - 1.89 * SP
        elif p_class == "medium":
            FP = 12.37 * T - 1.88 * SP
        else:
            FP = 14.11 * T - 1.97 * SP

        # Potassium
        if k_class == "low":
            FK = 9.65 * T - 0.21 * SK
        elif k_class == "medium":
            FK = 11.42 * T - 0.31 * SK
        else:
            FK = 12.17 * T - 0.33 * SK

        return {
            "N": min(300.0, max(0.0, round(FN, 2))),
            "P2O5": min(300.0, max(0.0, round(FP, 2))),
            "K2O": min(300.0, max(0.0, round(FK, 2)))
        }

if __name__ == "__main__":
    res = FPEEngine.compute(crop="maize", target_yield=40, soil_n_class="low", soil_p_class="medium", soil_k_class="high")
    print(res)
