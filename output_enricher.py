def enrich_output(FN, FP, FK, go_organic=False, fym_tonnes=None):
    """
    Takes the raw FPE engine outputs and applies post-processing.
    Clamps negative values to 0.
    Applies FYM nutrient deductions for P and K if organic pathway is chosen.
    Returns the adjusted (FN, FP, FK) and an explanation string if deductions occurred.
    """
    FN = max(0.0, FN)
    FP = max(0.0, FP)
    FK = max(0.0, FK)
    
    explanation = None
    
    if go_organic and fym_tonnes:
        original_FP = FP
        original_FK = FK
        
        # FYM provides ~2.5 kg P2O5 and ~5.0 kg K2O per tonne
        p_credit = round(fym_tonnes * 2.5, 2)
        k_credit = round(fym_tonnes * 5.0, 2)
        
        FP = max(0.0, FP - p_credit)
        FK = max(0.0, FK - k_credit)
        
        deductions = []
        if original_FP > FP:
            ssp_orig = round(original_FP / 0.16)
            ssp_new = round(FP / 0.16)
            deductions.append(f"SSP reduced from {ssp_orig} kg to {ssp_new} kg because FYM contributes ~{p_credit} kg P₂O₅/ha")
        
        if original_FK > FK:
            mop_orig = round(original_FK / 0.60)
            mop_new = round(FK / 0.60)
            deductions.append(f"MOP reduced from {mop_orig} kg to {mop_new} kg because FYM contributes ~{k_credit} kg K₂O/ha")
            
        if deductions:
            explanation = " and ".join(deductions) + "."
            
    return FN, FP, FK, explanation
