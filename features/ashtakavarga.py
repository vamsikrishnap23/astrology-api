# The Master Rulebook for Bhinna Ashtakavarga (BAV)
# Standard Parashari rules: 1-based indexing (1st house, 2nd house)
# The Master Rulebook for Bhinna Ashtakavarga (BAV)
# Standard Parashari rules: 1-based indexing (1st house, 2nd house)
# The Master Rulebook for Bhinna Ashtakavarga (BAV)
# Strict BPHS (Parashari) rules: 1-based indexing
from features.translator import translate

ASHTAKAVARGA_RULES = {
    "Sun": {
        "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon": [3, 6, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [5, 6, 9, 11],
        "Venus": [6, 7, 12],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Ascendant": [3, 4, 6, 10, 11, 12]
    },
    "Moon": {
        "Sun": [3, 6, 7, 8, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [2, 3, 5, 6, 9, 10, 11],
        "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter": [1, 4, 7, 8, 10, 11, 12],
        "Venus": [3, 4, 5, 7, 9, 10, 11],
        "Saturn": [3, 5, 6, 11],
        "Ascendant": [3, 6, 10, 11]
    },
    "Mars": {
        "Sun": [3, 5, 6, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [3, 5, 6, 11],
        "Jupiter": [6, 10, 11, 12],
        "Venus": [6, 8, 11, 12],
        "Saturn": [1, 4, 7, 8, 9, 10, 11],
        "Ascendant": [1, 3, 6, 10, 11]
    },
    "Mercury": {
        "Sun": [5, 6, 9, 11, 12],
        "Moon": [2, 4, 6, 8, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [6, 8, 11, 12],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Ascendant": [1, 2, 4, 6, 8, 10, 11]
    },
    "Jupiter": {
        "Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon": [2, 5, 7, 9, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "Venus": [2, 5, 6, 9, 10, 11],
        "Saturn": [3, 5, 6, 12],
        "Ascendant": [1, 2, 4, 5, 6, 7, 9, 10, 11]
    },
    "Venus": {
        "Sun": [8, 11, 12],
        "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Mars": [3, 5, 6, 9, 11, 12], # FIXED: 4 changed to 5
        "Mercury": [3, 5, 6, 9, 11],
        "Jupiter": [5, 8, 9, 10, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Saturn": [3, 4, 5, 8, 9, 10, 11],
        "Ascendant": [1, 2, 3, 4, 5, 8, 9, 11]
    },
    "Saturn": {
        "Sun": [1, 2, 4, 7, 8, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [3, 5, 6, 10, 11, 12],
        "Mercury": [6, 8, 9, 10, 11, 12],
        "Jupiter": [5, 6, 11, 12],
        "Venus": [6, 11, 12],
        "Saturn": [3, 5, 6, 11],
        "Ascendant": [1, 3, 4, 6, 10, 11]
    }
}

def calculate_single_bav(chart_data: dict, target_planet: str) -> list:
    """
    Calculates the 12-sign Bindu array for ANY given planet.
    Index 0 = Aries, Index 11 = Pisces.
    """
    bav_array = [0] * 12
    rules = ASHTAKAVARGA_RULES.get(target_planet, {})
    
    for reference_point, rule_houses in rules.items():
        ref_sign_index = chart_data[reference_point]["sign_index"]
        
        for house_offset in rule_houses:
            target_sign = (ref_sign_index + (house_offset - 1)) % 12
            bav_array[target_sign] += 1
            
    return bav_array

def get_all_bavs(chart_data: dict, lang: str = "en") -> dict:
    """
    Generates a dictionary containing the BAV arrays for all 7 standard planets.
    """
    all_bavs = {}
    
    # Must include all 7 planets to accurately calculate the SAV
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    for planet in planets:
        translated_key = translate(planet, "planet", lang)
        all_bavs[translated_key] = calculate_single_bav(chart_data, planet)
        
    return all_bavs

def calculate_sav(all_bavs: dict) -> list:
    """
    Calculates the Sarvashtakavarga (master chart) by summing all 7 planetary BAVs.
    Returns a single array of 12 integers representing the total Bindus per sign.
    """
    # Initialize a master array for the 12 signs (Aries to Pisces)
    sav_array = [0] * 12
    
    # Iterate through each planet's individual 12-point array
    for planet, bav_array in all_bavs.items():
        
        # Add the planet's points to the master SAV array
        for sign_index in range(12):
            sav_array[sign_index] += bav_array[sign_index]
            
    return sav_array

def calculate_trikona_shodhana(bav_array: list) -> list:
    """
    Applies Trikona Shodhana (Triangular Reduction) to a single BAV array.
    Groups are: Fire (0,4,8), Earth (1,5,9), Air (2,6,10), Water (3,7,11).
    """
    # Create a copy so we do not overwrite the raw BAV data
    reduced_array = bav_array.copy()
    
    # Iterate through the 4 elemental groups
    for i in range(4):
        # Find the minimum Bindus among the three signs in this specific trine
        min_bindus = min(reduced_array[i], reduced_array[i+4], reduced_array[i+8])
        
        # Subtract that minimum from all three signs
        reduced_array[i] -= min_bindus
        reduced_array[i+4] -= min_bindus
        reduced_array[i+8] -= min_bindus
        
    return reduced_array

def get_all_trikona(all_bavs: dict) -> dict:
    """
    Applies Trikona Shodhana to every planet's BAV array.
    """
    all_trikona = {}
    for planet, bav_array in all_bavs.items():
        all_trikona[planet] = calculate_trikona_shodhana(bav_array)
        
    return all_trikona

def get_planet_counts(chart_data: dict) -> list:
    """
    Counts how many physical planets (Sun to Saturn) occupy each of the 12 signs.
    Rahu, Ketu, and Ascendant are ignored for this specific rule.
    """
    counts = [0] * 12
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    for planet in planets:
        if planet in chart_data:
            counts[chart_data[planet]["sign_index"]] += 1
            
    return counts

def calculate_ekadhipatya_shodhana(trikona_array: list, planet_counts: list) -> list:
    """
    Applies the 7 rules of Ekadhipatya Shodhana to a Trikona-reduced array.
    """
    # Create a copy so we do not overwrite the Trikona data
    ekadhi = trikona_array.copy()

    # The 5 planet pairs (Aries/Sco, Taurus/Lib, Gemini/Vir, Sag/Pis, Cap/Aqu)
    pairs = [(0, 7), (1, 6), (2, 5), (8, 11), (9, 10)]

    for r1, r2 in pairs:
        t1 = trikona_array[r1]
        t2 = trikona_array[r2]

        p1 = planet_counts[r1] > 0
        p2 = planet_counts[r2] > 0

        # Rule 0: If one has points and the other is 0 -> No reduction
        if (t1 > 0 and t2 == 0) or (t1 == 0 and t2 > 0):
            continue

        # Rule 1: Both empty, points are different -> Both become the smaller number
        elif not p1 and not p2 and t1 != t2:
            ekadhi[r1] = ekadhi[r2] = min(t1, t2)

        # Rule 2: Both occupied -> No reduction
        elif p1 and p2:
            continue

        # Rule 3: One occupied, one empty, occupied is SMALLER -> Deduct smaller from the empty one
        elif p1 and not p2 and t1 < t2:
            ekadhi[r2] -= t1
        elif p2 and not p1 and t2 < t1:
            ekadhi[r1] -= t2

        # Rule 4: One occupied, one empty, occupied is BIGGER -> Empty one becomes 0
        elif p1 and not p2 and t1 > t2:
            ekadhi[r2] = 0
        elif p2 and not p1 and t2 > t1:
            ekadhi[r1] = 0

        # Rule 5: Both empty, points are equal -> Both become 0
        elif not p1 and not p2 and t1 == t2:
            ekadhi[r1] = 0
            ekadhi[r2] = 0

        # Rule 6: One occupied, one empty, points are equal -> Empty one becomes 0
        elif p1 and not p2 and t1 == t2:
            ekadhi[r2] = 0
        elif p2 and not p1 and t2 == t1:
            ekadhi[r1] = 0

    return ekadhi

def get_all_ekadhipatya(trikona_data: dict, chart_data: dict) -> dict:
    """
    Applies Ekadhipatya Shodhana to every planet's Trikona array.
    """
    # We only count the planets once for the entire chart
    planet_counts = get_planet_counts(chart_data)
    
    all_ekadhi = {}
    for planet, trikona_array in trikona_data.items():
        all_ekadhi[planet] = calculate_ekadhipatya_shodhana(trikona_array, planet_counts)
        
    return all_ekadhi