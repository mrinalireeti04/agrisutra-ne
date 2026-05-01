class FPEEngine:
    """
    Fertilizer Prescription Equation (FPE) Engine.
    Each nutrient (N, P, K) is computed INDEPENDENTLY.
    Never mix fertility inputs across nutrients.
    """

    # Default soil nutrient values (kg/ha) for each fertility class
    DEFAULT_SN = {"low": 150.0, "medium": 280.0, "high": 400.0}
    DEFAULT_SP = {"low": 10.0,  "medium": 20.0,  "high": 35.0}
    DEFAULT_SK = {"low": 100.0, "medium": 150.0, "high": 300.0}

    @staticmethod
    def _resolve_class_from_value(crop: str, val: float, nutrient: str) -> str:
        crop = crop.lower()
        if "maize" in crop:
            if nutrient == "N":
                return "low" if val < 225 else ("high" if val > 500 else "medium")
            elif nutrient == "P":
                return "low" if val < 22 else ("high" if val > 55 else "medium")
            elif nutrient == "K":
                return "low" if val < 137 else ("high" if val > 337 else "medium")
        elif "kholar" in crop:
            if nutrient == "N":
                return "low" if val < 225 else ("high" if val > 450 else "medium")
            elif nutrient == "P":
                return "low" if val < 22.5 else ("high" if val > 55 else "medium")
            elif nutrient == "K":
                return "low" if val < 137 else ("high" if val > 337 else "medium")
        return "medium"

    # ─────────────────────────────────────────────
    # NITROGEN (FN) — Independent
    # ─────────────────────────────────────────────
    @classmethod
    def compute_N(cls, crop: str, T: float, fertility_class: str = None, SN: float = None) -> dict:
        """
        Compute Nitrogen requirement (FN) independently.
        Either fertility_class OR SN must be provided.
        """
        crop = crop.lower()

        if SN is None:
            if fertility_class is None:
                raise ValueError("Provide either fertility_class or SN for Nitrogen.")
            fc = fertility_class.lower()
            SN = cls.DEFAULT_SN[fc]
        else:
            fc = cls._resolve_class_from_value(crop, SN, "N")

        if "maize" in crop:
            if fc == "low":
                FN = 3.93 * T - 0.26 * SN
            elif fc == "medium":
                FN = 4.11 * T - 0.36 * SN
            else:
                FN = 4.87 * T - 0.41 * SN
        elif "kholar" in crop:
            if fc == "low":
                FN = 23.76 * T - 0.52 * SN
            elif fc == "medium":
                FN = 25.26 * T - 0.57 * SN
            else:
                FN = 26.45 * T - 0.63 * SN
        else:
            raise ValueError(f"Unsupported crop: {crop}")

        FN = round(FN, 2)
        return {
            "FN": FN,
            "urea_kg_ha": round(FN / 0.46, 2),
            "equation": f"FN = {FN} kg/ha   [SN={SN}, T={T}, Class={fc}]"
        }

    # ─────────────────────────────────────────────
    # PHOSPHORUS (FP) — Independent
    # ─────────────────────────────────────────────
    @classmethod
    def compute_P(cls, crop: str, T: float, fertility_class: str = None, SP: float = None) -> dict:
        """
        Compute Phosphorus requirement (FP2O5) independently.
        Either fertility_class OR SP must be provided.
        """
        crop = crop.lower()

        if SP is None:
            if fertility_class is None:
                raise ValueError("Provide either fertility_class or SP for Phosphorus.")
            fc = fertility_class.lower()
            SP = cls.DEFAULT_SP[fc]
        else:
            fc = cls._resolve_class_from_value(crop, SP, "P")

        if "maize" in crop:
            if fc == "low":
                FP = 1.28 * T - 0.87 * SP
            elif fc == "medium":
                FP = 1.97 * T - 1.66 * SP
            else:
                FP = 3.86 * T - 2.81 * SP
        elif "kholar" in crop:
            if fc == "low":
                FP = 11.45 * T - 1.89 * SP
            elif fc == "medium":
                FP = 12.37 * T - 1.88 * SP
            else:
                FP = 14.11 * T - 1.97 * SP
        else:
            raise ValueError(f"Unsupported crop: {crop}")

        FP = round(FP, 2)
        return {
            "FP": FP,
            "ssp_kg_ha": round(FP / 0.16, 2),
            "equation": f"FP = {FP} kg/ha   [SP={SP}, T={T}, Class={fc}]"
        }

    # ─────────────────────────────────────────────
    # POTASSIUM (FK) — Independent
    # ─────────────────────────────────────────────
    @classmethod
    def compute_K(cls, crop: str, T: float, fertility_class: str = None, SK: float = None) -> dict:
        """
        Compute Potassium requirement (FK2O) independently.
        Either fertility_class OR SK must be provided.
        """
        crop = crop.lower()

        if SK is None:
            if fertility_class is None:
                raise ValueError("Provide either fertility_class or SK for Potassium.")
            fc = fertility_class.lower()
            SK = cls.DEFAULT_SK[fc]
        else:
            fc = cls._resolve_class_from_value(crop, SK, "K")

        if "maize" in crop:
            if fc == "low":
                FK = 1.77 * T - 0.09 * SK
            elif fc == "medium":
                FK = 2.09 * T - 0.22 * SK
            else:
                FK = 2.98 * T - 0.34 * SK
        elif "kholar" in crop:
            if fc == "low":
                FK = 9.65 * T - 0.21 * SK
            elif fc == "medium":
                FK = 11.42 * T - 0.31 * SK
            else:
                FK = 12.17 * T - 0.33 * SK
        else:
            raise ValueError(f"Unsupported crop: {crop}")

        FK = round(FK, 2)
        return {
            "FK": FK,
            "mop_kg_ha": round(FK / 0.60, 2),
            "equation": f"FK = {FK} kg/ha   [SK={SK}, T={T}, Class={fc}]"
        }


if __name__ == "__main__":
    print(FPEEngine.compute_N("maize", T=40, fertility_class="low"))
    print(FPEEngine.compute_P("maize", T=40, fertility_class="medium"))
    print(FPEEngine.compute_K("maize", T=40, fertility_class="high"))
