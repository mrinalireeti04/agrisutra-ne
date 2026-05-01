def calculate_fertilizers(n_req, p_req, k_req):
    urea = n_req / 0.46 if n_req else 0
    ssp = p_req / 0.16 if p_req else 0
    mop = k_req / 0.60 if k_req else 0
    return round(urea, 1), round(ssp, 1), round(mop, 1)

def get_nitrogen_details(n_req, urea):
    return {
        "required": n_req,
        "fertilizer": "Urea",
        "fertilizer_amount": urea,
        "conversion": "Urea = N / 0.46",
        "schedule": f"Basal: {round(urea*0.5, 1)} kg, 30 days: {round(urea*0.25, 1)} kg, 60 days: {round(urea*0.25, 1)} kg",
        "why": "Nitrogen is essential for vegetative growth, forming amino acids and proteins. It drives the green color and vigorous growth of leaves.",
        "improvement": "Split applications of Nitrogen (as suggested in the schedule) prevent leaching and ensure the plant gets nutrients precisely when needed during rapid growth phases."
    }

def get_phosphorus_details(p_req, ssp):
    return {
        "required": p_req,
        "fertilizer": "SSP (Single Super Phosphate)",
        "fertilizer_amount": ssp,
        "conversion": "SSP = P2O5 / 0.16",
        "schedule": f"Basal: {round(ssp, 1)} kg (Apply completely before or at sowing)",
        "why": "Phosphorus plays a crucial role in root development, energy transfer (ATP), and early plant establishment.",
        "improvement": "Always apply Phosphorus as a basal dose because it is immobile in the soil. Placing it near the root zone improves uptake efficiency."
    }

def get_potassium_details(k_req, mop):
    return {
        "required": k_req,
        "fertilizer": "MOP (Muriate of Potash)",
        "fertilizer_amount": mop,
        "conversion": "MOP = K2O / 0.60",
        "schedule": f"Basal: {round(mop, 1)} kg",
        "why": "Potassium enhances stress resistance (drought, disease), water regulation (stomata opening/closing), and grain quality.",
        "improvement": "Adequate Potassium ensures sturdy stems to prevent lodging. In sandy soils, a split application can be considered if heavy rainfall occurs."
    }
