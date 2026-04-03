# features/shadbala.py

# Deep Exaltation Points (in 360-degree continuous format)
# Sun: Aries 10°, Moon: Taurus 3°, Mars: Capricorn 28°, 
# Mercury: Virgo 15°, Jupiter: Cancer 5°, Venus: Pisces 27°, Saturn: Libra 20°
DEEP_EXALTATION = {
    "Sun": 10.0,
    "Moon": 33.0,
    "Mars": 298.0,
    "Mercury": 165.0,
    "Jupiter": 95.0,
    "Venus": 357.0,
    "Saturn": 200.0
}

from features.relationships import get_compound_relationship

# Virupa scoring matrix for dignities
DIGNITY_SCORES = {
    "Moolatrikona": 45.0, # Handled separately via degree checks
    "Own": 30.0,
    "Great_Friend": 22.5,
    "Friend": 15.0,
    "Neutral": 7.5,
    "Enemy": 3.75,
    "Great_Enemy": 1.875
}

# The lords of the 12 Zodiac signs (0=Aries, 11=Pisces)
SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", 
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
]

def calculate_saptavargaja_bala(chart_data: dict, vargas: dict) -> dict:
    """
    Calculates the dignity strength across the 7 specific Vargas.
    (Requires your pre-calculated Varga dictionaries: D1, D2, D3, D7, D9, D12, D30)
    """
    scores = {}
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    varga_keys = ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]
    
    for planet in planets:
        total_virupas = 0.0
        
        for varga in varga_keys:
            # Get the sign index the planet sits in for this specific Varga
            sign_index = vargas[varga][planet]["sign_index"]
            
            # Find out who rules that sign
            lord_of_sign = SIGN_LORDS[sign_index]
            
            # Calculate how the planet feels about that lord
            # Note: Temporary relationship is ALWAYS based on D-1 physical positions!
            relationship = get_compound_relationship(planet, lord_of_sign, chart_data)
            
            # Add the score
            total_virupas += DIGNITY_SCORES[relationship]
            
        scores[planet] = round(total_virupas, 2)
        
    return scores

def calculate_uchcha_bala(chart_data: dict) -> dict:
    """
    Calculates Uchcha Bala (Exaltation Strength) for the 7 physical planets.
    Returns the strength in Virupas (Max: 60, Min: 0).
    """
    uchcha_scores = {}
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    for planet in planets:
        if planet in chart_data:
            planet_lon = chart_data[planet]["longitude_360"]
            exaltation_point = DEEP_EXALTATION[planet]
            
            # The debilitation point is exactly 180 degrees away from exaltation
            debilitation_point = (exaltation_point + 180.0) % 360.0
            
            # Find the absolute angular distance from the debilitation point
            distance = abs(planet_lon - debilitation_point)
            
            # The shortest path on a circle cannot exceed 180 degrees
            if distance > 180.0:
                distance = 360.0 - distance
                
            # Rule: 1 Virupa for every 3 degrees of distance from debilitation
            virupas = distance / 3.0
            
            uchcha_scores[planet] = round(virupas, 2)
            
    return uchcha_scores

def calculate_shadbala(chart_data: dict) -> dict:
    """
    The master controller that will eventually run all 6 Balas.
    """
    # 1. Sthana Bala calculations
    uchcha = calculate_uchcha_bala(chart_data)
    
    # We will bundle everything neatly for the UI
    return {
        "Sthana_Bala": {
            "Uchcha_Bala": uchcha
        }
    }