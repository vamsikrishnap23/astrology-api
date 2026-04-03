# features/shadbala.py
import math
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

WEEKDAY_LORDS = {
    0: "Sun",
    1: "Moon",
    2: "Mars",
    3: "Mercury",
    4: "Jupiter",
    5: "Venus",
    6: "Saturn"
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
    Safely routes D-1 lookups to the base chart.
    """
    scores = {}
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    varga_keys = ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]
    
    for planet in planets:
        total_virupas = 0.0
        
        for varga in varga_keys:
            
            # --- THE FIX: Route D1 to base chart, others to vargas dict ---
            if varga == "D1":
                sign_index = chart_data[planet]["sign_index"]
            else:
                sign_index = vargas[varga][planet]["sign_index"]
            
            # Find out who rules that sign
            lord_of_sign = SIGN_LORDS[sign_index]
            
            # Calculate how the planet feels about that lord
            # Temporary relationship is ALWAYS based on D-1 physical positions
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

def calculate_ojayugma_bala(chart_data: dict, vargas: dict) -> dict:
    """
    Ojayugmarasyamsa Bala: Strength based on Odd/Even signs in D-1 and D-9.
    Returns scores up to 30 Virupas (15 for D-1, 15 for D-9).
    """
    scores = {}
    
    # 0-Indexed: Aries(0) is Odd, Taurus(1) is Even
    def is_odd(sign_index): return sign_index % 2 == 0 
    
    even_planets = ["Moon", "Venus"]
    odd_planets = ["Sun", "Mars", "Jupiter", "Mercury", "Saturn"]
    
    for planet in odd_planets + even_planets:
        if planet not in chart_data: continue
            
        d1_sign = chart_data[planet]["sign_index"]
        d9_sign = vargas["D9"][planet]["sign_index"]
        
        score = 0.0
        
        if planet in odd_planets:
            if is_odd(d1_sign): score += 15.0
            if is_odd(d9_sign): score += 15.0
        else: # even_planets
            if not is_odd(d1_sign): score += 15.0
            if not is_odd(d9_sign): score += 15.0
            
        scores[planet] = score
        
    return scores

def calculate_kendra_bala(chart_data: dict) -> dict:
    """
    Kendra Bala: Strength based on Angular houses from the Ascendant.
    """
    scores = {}
    asc_sign = chart_data["Ascendant"]["sign_index"]
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    for planet in planets:
        if planet in chart_data:
            planet_sign = chart_data[planet]["sign_index"]
            
            # Calculate House (1-based index)
            house = (planet_sign - asc_sign + 12) % 12 + 1
            
            if house in [1, 4, 7, 10]:
                scores[planet] = 60.0
            elif house in [2, 5, 8, 11]:
                scores[planet] = 30.0
            else:
                scores[planet] = 15.0
                
    return scores

def calculate_drekkana_bala(chart_data: dict) -> dict:
    """
    Drekkana Bala: Strength based on the 10-degree segment of the sign.
    """
    scores = {planet: 0.0 for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
    
    for planet in scores.keys():
        if planet in chart_data:
            # Get the exact degree within the 30-degree sign
            degree_in_sign = chart_data[planet]["longitude_360"] % 30.0
            
            if degree_in_sign < 10.0 and planet in ["Sun", "Mars", "Jupiter"]:
                scores[planet] = 15.0
            elif 10.0 <= degree_in_sign < 20.0 and planet in ["Mercury", "Saturn"]:
                scores[planet] = 15.0
            elif degree_in_sign >= 20.0 and planet in ["Moon", "Venus"]:
                scores[planet] = 15.0
                
    return scores


def calculate_dig_bala(chart_data: dict) -> dict:
    """
    Pillar 2: Dig Bala (Directional Strength).
    Calculates proximity to the planet's optimal cardinal compass point.
    Using Equal House quadrants (Ascendant + 90/180/270).
    """
    scores = {}
    
    # 1. Base the entire matrix perfectly off the Ascendant degree
    east_point = chart_data["Ascendant"]["longitude_360"]
    north_point = (east_point + 90.0) % 360.0
    west_point = (east_point + 180.0) % 360.0
    south_point = (east_point + 270.0) % 360.0
    
    # 2. Map planets to their point of MAXIMUM strength (60 Virupas)
    power_points = {
        "Sun": south_point,
        "Mars": south_point,
        "Saturn": west_point,
        "Moon": north_point,
        "Venus": north_point,
        "Mercury": east_point,
        "Jupiter": east_point
    }
    
    for planet, optimal_point in power_points.items():
        if planet in chart_data:
            planet_lon = chart_data[planet]["longitude_360"]
            
            # 3. Find the shortest angular distance on a 360-degree circle
            distance = abs(planet_lon - optimal_point)
            if distance > 180.0:
                distance = 360.0 - distance
                
            # 4. Apply the Virupa formula
            virupas = (180.0 - distance) / 3.0
            scores[planet] = round(virupas, 2)
            
    return scores


def calculate_nathonnatha_bala(hour: int, minute: int, lon: float, tz_offset: float) -> dict:
    """
    Nathonnatha Bala: Day vs Night Strength.
    Corrected to use Local Mean Time (LMT) instead of Standard Clock Time.
    """
    scores = {}
    clock_time = hour + (minute / 60.0)
    
    # 1. Convert Standard Time to Local Mean Time (LMT)
    # The standard meridian for the timezone = offset * 15 degrees
    standard_meridian = tz_offset * 15.0
    
    # Difference in degrees * 4 minutes per degree / 60 to get hours
    lmt_correction = (lon - standard_meridian) / 15.0
    decimal_time = (clock_time + lmt_correction) % 24.0
    
    # 2. Calculate distance from Midnight (00:00) and Noon (12:00)
    if decimal_time <= 12.0:
        dist_from_midnight = decimal_time
        dist_from_noon = 12.0 - decimal_time
    else:
        dist_from_midnight = 24.0 - decimal_time
        dist_from_noon = decimal_time - 12.0

    midnight_strength = (12.0 - dist_from_midnight) * 5.0
    noon_strength = (12.0 - dist_from_noon) * 5.0

    scores["Moon"] = round(midnight_strength, 2)
    scores["Mars"] = round(midnight_strength, 2)
    scores["Saturn"] = round(midnight_strength, 2)
    
    scores["Sun"] = round(noon_strength, 2)
    scores["Jupiter"] = round(noon_strength, 2)
    scores["Venus"] = round(noon_strength, 2)
    
    scores["Mercury"] = 60.0 # Mercury is always 60
    
    return scores

def calculate_paksha_bala(chart_data: dict) -> dict:
    """
    Paksha Bala: Lunar Phase Strength.
    Corrected to apply the Moon Doubling Rule and Waning/Malefic classification.
    """
    scores = {}
    sun_lon = chart_data["Sun"]["longitude_360"]
    moon_lon = chart_data["Moon"]["longitude_360"]
    
    # 1. Find the angular difference
    angle = (moon_lon - sun_lon + 360.0) % 360.0
    
    # 2. Waxing vs Waning
    is_waning = angle > 180.0
    
    if is_waning:
        distance = 360.0 - angle
    else:
        distance = angle
        
    # 3. Base scores (1 Virupa per 3 degrees)
    benefic_score = distance / 3.0
    malefic_score = 60.0 - benefic_score
    
    # 4. Assign standard scores
    # (Note: Mercury takes Malefic score if associated with Sun/Malefics. We default to Malefic if waning Moon)
    scores["Sun"] = round(malefic_score, 2)
    scores["Mars"] = round(malefic_score, 2)
    scores["Saturn"] = round(malefic_score, 2)
    
    scores["Jupiter"] = round(benefic_score, 2)
    scores["Venus"] = round(benefic_score, 2)
    
    # Mercury dynamic rule (Matching your website output)
    scores["Mercury"] = round(malefic_score if is_waning else benefic_score, 2)
    
    # 5. THE MOON DOUBLING RULE
    if is_waning:
        scores["Moon"] = round(malefic_score * 2.0, 2) # Waning Moon = Malefic doubled
    else:
        scores["Moon"] = round(benefic_score * 2.0, 2) # Waxing Moon = Benefic doubled
        
    return scores

def calculate_tribhaga_bala(hour: int, minute: int) -> dict:
    """
    Tribhaga Bala: Day/Night Thirds.
    Assigns a flat 60 Virupas to the ruler of the specific 4-hour block of time.
    Jupiter always receives 60 Virupas.
    """
    scores = {p: 0.0 for p in ["Sun", "Moon", "Mars", "Mercury", "Venus", "Saturn"]}
    scores["Jupiter"] = 60.0
    
    decimal_time = hour + (minute / 60.0)
    
    # Assuming standard 06:00 Sunrise and 18:00 Sunset for baseline math
    if 6.0 <= decimal_time < 10.0:    scores["Mercury"] = 60.0
    elif 10.0 <= decimal_time < 14.0: scores["Sun"] = 60.0
    elif 14.0 <= decimal_time < 18.0: scores["Saturn"] = 60.0
    elif 18.0 <= decimal_time < 22.0: scores["Moon"] = 60.0
    elif 22.0 <= decimal_time < 2.0 or decimal_time >= 22.0: scores["Venus"] = 60.0
    elif 2.0 <= decimal_time < 6.0:   scores["Mars"] = 60.0
    
    return scores

def calculate_time_lords_bala(jd: float, hour: int, minute: int, tz_offset: float, sunrise_hour: float = 6.0) -> dict:
    """
    Calculates Abda, Masa, Vara, and Hora Bala.
    Uses precise Julian Day weekday math to guarantee perfect Day and Hour Lords.
    """
    scores = {p: 0.0 for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
    
    decimal_time = hour + (minute / 60.0)
    
    # 1. VARA (DAY) LORD - 45 Virupas
    # Convert UTC Julian Day to Local Time Julian Day
    local_jd = jd + (tz_offset / 24.0)
    
    # Vedic days strictly change at Sunrise, not midnight!
    if decimal_time < sunrise_hour:
        local_jd -= 1.0
        
    # Standard Astronomical algorithm for Weekday from JD
    day_index = int(math.floor(local_jd + 1.5)) % 7
    day_lord = WEEKDAY_LORDS[day_index]
    scores[day_lord] += 45.0
    
    # 2. HORA (HOUR) LORD - 60 Virupas
    if decimal_time < sunrise_hour:
        hours_since_sunrise = (24.0 - sunrise_hour) + decimal_time
    else:
        hours_since_sunrise = decimal_time - sunrise_hour
        
    current_hora = int(math.floor(hours_since_sunrise))
    
    # Hora cycles backwards by 2 days every hour
    hora_index = (day_index - (2 * current_hora)) % 7
    hora_lord = WEEKDAY_LORDS[hora_index]
    scores[hora_lord] += 60.0
    
    # 3. MASA (MONTH) & ABDA (YEAR) LORDS - 30 & 15 Virupas
    # We still use Ahargana here as they are 30/360 day cyclical blocks
    ahargana = int(math.floor(local_jd - 588465.5))
    
    masa_index = ((ahargana // 30) * 30 + 4) % 7
    masa_lord = WEEKDAY_LORDS[masa_index]
    scores[masa_lord] += 30.0
    
    abda_index = ((ahargana // 360) * 360 + 4) % 7
    abda_lord = WEEKDAY_LORDS[abda_index]
    scores[abda_lord] += 15.0
    
    return scores


def calculate_chesta_bala(chart_data: dict, jd: float) -> dict:
    """
    Pillar 4: Chesta Bala (Motional Strength).
    Uses the exact Surya Siddhanta (B.V. Raman) epicycle algorithms.
    """
    scores = {"Sun": 0.0, "Moon": 0.0} 
    
    # 1. Calculate Ahargana (Days since Kali Yuga Epoch: Feb 18, 3102 BC)
    ahargana = jd - 588465.5
    
    # 2. Daily Mean Motions in Degrees (Ancient Constants)
    motions = {
        "Sun": 0.9856026,
        "Mars": 0.5240318,
        "Jupiter": 0.083087,
        "Saturn": 0.033423,
        "Mercury_Seeghrocha": 4.092305,
        "Venus_Seeghrocha": 1.602131
    }
    
    # 3. Calculate Mean Planets
    mean_sun = (ahargana * motions["Sun"]) % 360.0
    
    # Outer planets: Seeghrocha = Mean Sun. Mean Planet = Ahargana * motion
    # Inner planets: Seeghrocha = Ahargana * motion. Mean Planet = Mean Sun
    calc_data = {
        "Mars": {"mean": (ahargana * motions["Mars"]) % 360.0, "seeghrocha": mean_sun},
        "Jupiter": {"mean": (ahargana * motions["Jupiter"]) % 360.0, "seeghrocha": mean_sun},
        "Saturn": {"mean": (ahargana * motions["Saturn"]) % 360.0, "seeghrocha": mean_sun},
        "Mercury": {"mean": mean_sun, "seeghrocha": (ahargana * motions["Mercury_Seeghrocha"]) % 360.0},
        "Venus": {"mean": mean_sun, "seeghrocha": (ahargana * motions["Venus_Seeghrocha"]) % 360.0}
    }
    
    for planet in calc_data.keys():
        if planet in chart_data:
            true_lon = chart_data[planet]["longitude_360"]
            mean_lon = calc_data[planet]["mean"]
            seeghrocha = calc_data[planet]["seeghrocha"]
            
            # 4. The B.V. Raman Formula: 
            # First, find the midpoint (X) between the Mean and True Longitude
            # We must find the shortest arc to average circular angles properly
            diff = (true_lon - mean_lon) % 360.0
            if diff > 180.0: 
                diff -= 360.0
                
            x = (mean_lon + (diff / 2.0)) % 360.0
            
            # 5. Cheshta Kendra = Seeghrocha - X
            ck = (seeghrocha - x + 360.0) % 360.0
            
            # 6. Normalize and Convert to Virupas
            if ck > 180.0:
                ck = 360.0 - ck
                
            virupas = ck / 3.0
            scores[planet] = round(virupas, 2)
            
    return scores

def calculate_naisargika_bala() -> dict:
    """
    Pillar 5: Naisargika Bala (Natural Strength).
    These are static astronomical constants based on inherent planetary luminosity.
    """
    return {
        "Sun": 60.0,
        "Moon": 51.43,
        "Venus": 42.85,
        "Jupiter": 34.28,
        "Mercury": 25.70,
        "Mars": 17.14,
        "Saturn": 8.57
    }

def get_drishti_value(aspecting_lon: float, aspected_lon: float, aspecting_planet: str) -> float:
    """
    Calculates the exact Aspect Value (Drishti) from one planet to another.
    """
    # 1. Find the forward angular distance
    d = (aspected_lon - aspecting_lon + 360.0) % 360.0
    v = 0.0
    
    # 2. Standard Aspect Matrix (BPHS / B.V. Raman)
    if d <= 30.0:        v = 0.0
    elif d <= 60.0:      v = (d - 30.0) / 2.0
    elif d <= 90.0:      v = (d - 60.0) + 15.0
    elif d <= 120.0:     v = (120.0 - d) + 30.0
    elif d <= 150.0:     v = 150.0 - d
    elif d <= 180.0:     v = (d - 150.0) * 2.0
    elif d <= 300.0:     v = (300.0 - d) / 2.0
    else:                v = 0.0

    # 3. Special Planetary Aspects
    if aspecting_planet == "Mars":
        if 90.0 < d <= 120.0:  v += (d - 90.0)      # 4th House sight
        if 210.0 < d <= 240.0: v += (d - 210.0)     # 8th House sight
    elif aspecting_planet == "Jupiter":
        if 120.0 < d <= 150.0: v += (d - 120.0) / 2.0 # 5th House sight
        if 240.0 < d <= 270.0: v += (d - 240.0) / 2.0 # 9th House sight
    elif aspecting_planet == "Saturn":
        if 60.0 < d <= 90.0:   v += (d - 60.0)      # 3rd House sight
        if 270.0 < d <= 300.0: v += (d - 270.0)     # 10th House sight

    # Cap maximum sight value at 60 Virupas
    return min(v, 60.0)

def calculate_drik_bala(chart_data: dict) -> dict:
    """
    Pillar 6: Drik Bala (Aspectual Strength).
    """
    scores = {p: 0.0 for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
    planets = list(scores.keys())
    
    # Check Moon phase for Benefic/Malefic status
    sun_lon = chart_data["Sun"]["longitude_360"]
    moon_lon = chart_data["Moon"]["longitude_360"]
    moon_waning = ((moon_lon - sun_lon + 360.0) % 360.0) > 180.0
    
    # Define nature (Mercury is considered Benefic here unless heavily afflicted, keeping standard)
    malefics = ["Sun", "Mars", "Saturn"]
    if moon_waning: malefics.append("Moon")
    
    for aspected in planets:
        if aspected not in chart_data: continue
        target_lon = chart_data[aspected]["longitude_360"]
        
        net_drik_bala = 0.0
        
        for aspecting in planets:
            if aspecting == aspected or aspecting not in chart_data: 
                continue
                
            shooter_lon = chart_data[aspecting]["longitude_360"]
            
            # Get raw Drishti Value
            raw_aspect_value = get_drishti_value(shooter_lon, target_lon, aspecting)
            
            # Drik Bala is exactly 1/4th of the Drishti Value
            bala_value = raw_aspect_value / 4.0
            
            # Apply Benefic (Positive) or Malefic (Negative) filter
            if aspecting in malefics:
                net_drik_bala -= bala_value
            else:
                net_drik_bala += bala_value
                
        scores[aspected] = round(net_drik_bala, 2)
        
    return scores



def calculate_shadbala(chart_data: dict, vargas: dict, birth_time: dict) -> dict:
    """
    The Complete Shadbala Master Controller.
    Calculates and sums all 6 Pillars of Planetary Strength.
    """
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    # --- Pillar 1: Sthana Bala (Positional Strength) ---
    uchcha = calculate_uchcha_bala(chart_data)
    sapta = calculate_saptavargaja_bala(chart_data, vargas)
    ojayugma = calculate_ojayugma_bala(chart_data, vargas)
    kendra = calculate_kendra_bala(chart_data)
    drekkana = calculate_drekkana_bala(chart_data)
    
    sthana_bala_total = {}
    for p in planets:
        total = uchcha.get(p, 0) + sapta.get(p, 0) + ojayugma.get(p, 0) + kendra.get(p, 0) + drekkana.get(p, 0)
        sthana_bala_total[p] = round(total, 2)
        
    # --- Pillar 2: Dig Bala (Directional Strength) ---
    dig_bala = calculate_dig_bala(chart_data)
    
    # --- Pillar 3: Kala Bala (Temporal Strength) ---
    hour = birth_time["hour"]
    minute = birth_time["minute"]
    lon = birth_time["lon"]
    tz_offset = birth_time["tz_offset"]
    jd = birth_time["jd"]
    
    nathonnatha = calculate_nathonnatha_bala(hour, minute, lon, tz_offset)
    paksha = calculate_paksha_bala(chart_data)
    tribhaga = calculate_tribhaga_bala(hour, minute)
    time_lords = calculate_time_lords_bala(jd, hour, minute, tz_offset)
    
    kala_bala_total = {}
    for p in planets:
        total = nathonnatha.get(p, 0) + paksha.get(p, 0) + tribhaga.get(p, 0) + time_lords.get(p, 0)
        kala_bala_total[p] = round(total, 2)
        
    # --- Pillar 4: Chesta Bala (Motional Strength) ---
    chesta_bala = calculate_chesta_bala(chart_data, jd)
    
    # --- Pillar 5: Naisargika Bala (Natural Strength) ---
    naisargika_bala = calculate_naisargika_bala()
    
    # --- Pillar 6: Drik Bala (Aspectual Strength) ---
    drik_bala = calculate_drik_bala(chart_data)
    
    # --- TOTAL SHADBALA SUMMARY ---
    total_shadbala_virupas = {}
    total_shadbala_rupas = {}
    
    for p in planets:
        # Sum all 6 Pillars
        total = (
            sthana_bala_total.get(p, 0) + 
            dig_bala.get(p, 0) + 
            kala_bala_total.get(p, 0) + 
            chesta_bala.get(p, 0) + 
            naisargika_bala.get(p, 0) + 
            drik_bala.get(p, 0)
        )
        total_shadbala_virupas[p] = round(total, 2)
        
        # 60 Virupas = 1 Rupa
        total_shadbala_rupas[p] = round(total / 60.0, 2)
    
    # --- Return Final Payload ---
    return {
        "Summary": {
            "Total_Shadbala_Virupas": total_shadbala_virupas,
            "Total_Shadbala_Rupas": total_shadbala_rupas
        },
        "Sthana_Bala": {
            "Total": sthana_bala_total,
            "Breakdown": {
                "Uchcha_Bala": uchcha,
                "Saptavargaja_Bala": sapta,
                "Ojayugmarasyamsa_Bala": ojayugma,
                "Kendra_Bala": kendra,
                "Drekkana_Bala": drekkana
            }
        },
        "Dig_Bala": dig_bala,
        "Kala_Bala": {
            "Total_Partial": kala_bala_total,
            "Breakdown": {
                "Nathonnatha_Bala": nathonnatha,
                "Paksha_Bala": paksha,
                "Tribhaga_Bala": tribhaga,
                "Time_Lords_Bala": time_lords
            }
        },
        "Chesta_Bala": chesta_bala,
        "Naisargika_Bala": naisargika_bala,
        "Drik_Bala": drik_bala
    }