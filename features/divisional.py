from utils import ZODIAC_SIGNS
from features.translator import translate

def get_varga_sign_index(varga_type: int, base_sign: int, degree_in_sign: float) -> int:
    """
    Applies the strict Parashari mapping rules for all 16 divisional charts.
    """
    is_odd_sign = (base_sign % 2 == 0) # 0=Aries (Odd), 1=Taurus (Even)
    modality = base_sign % 3           # 0=Movable, 1=Fixed, 2=Dual
    
    # Calculate equal part index (Ignored for D-30)
    part = int(degree_in_sign / (30.0 / varga_type)) if varga_type != 30 else 0

    if varga_type == 2:   # Hora
        if is_odd_sign: return 4 if part == 0 else 3
        else: return 3 if part == 0 else 4
        
    elif varga_type == 3: # Drekkana
        return (base_sign + (part * 4)) % 12
        
    elif varga_type == 4: # Chaturthamsha
        return (base_sign + (part * 3)) % 12
        
    elif varga_type == 7: # Saptamsha
        start = base_sign if is_odd_sign else (base_sign + 6) % 12
        return (start + part) % 12
        
    elif varga_type == 9: # Navamsa
        start = (base_sign % 4) * 9 % 12
        return (start + part) % 12
        
    elif varga_type == 10: # Dashamsha
        start = base_sign if is_odd_sign else (base_sign + 8) % 12
        return (start + part) % 12
        
    elif varga_type == 12: # Dwadashamsha
        return (base_sign + part) % 12
        
    elif varga_type == 16: # Shodashamsha (Starts Movable=Aries, Fixed=Leo, Dual=Sag)
        start = modality * 4
        return (start + part) % 12
        
    elif varga_type == 20: # Vimshamsha (Starts Movable=Aries, Dual=Leo, Fixed=Sag)
        if modality == 0: start = 0
        elif modality == 1: start = 8
        else: start = 4
        return (start + part) % 12
        
    elif varga_type == 24: # Chaturvimshamsha (Odd starts Leo, Even starts Cancer)
        start = 4 if is_odd_sign else 3
        return (start + part) % 12
        
    elif varga_type == 27: # Saptavimshamsha / Bhamsha (Starts from Elemental signs)
        start = (base_sign % 4) * 3
        return (start + part) % 12
        
    elif varga_type == 30: # Trimshamsha (Unequal Parts Rule)
        deg = degree_in_sign
        if is_odd_sign:
            if deg <= 5.0: return 0     # Aries
            elif deg <= 10.0: return 10 # Aquarius
            elif deg <= 18.0: return 8  # Sagittarius
            elif deg <= 25.0: return 2  # Gemini
            else: return 6              # Libra
        else:
            if deg <= 5.0: return 1     # Taurus
            elif deg <= 12.0: return 5  # Virgo
            elif deg <= 20.0: return 11 # Pisces
            elif deg <= 25.0: return 9  # Capricorn
            else: return 7              # Scorpio
            
    elif varga_type == 40: # Khavedamsha (Odd starts Aries, Even starts Libra)
        start = 0 if is_odd_sign else 6
        return (start + part) % 12
        
    elif varga_type == 45: # Akshavedamsha (Starts Movable=Aries, Fixed=Leo, Dual=Sag)
        start = modality * 4
        return (start + part) % 12
        
    elif varga_type == 60: # Shashtiamsha
        return (base_sign + part) % 12
        
    else:
        return (base_sign + part) % 12

def calculate_single_varga(chart_data: dict, varga_type: int, lang: str = "en") -> dict:
    varga_chart = {}
    
    for key, data in chart_data.items():
        if key in ("Julian_Day", "Houses"):  # Houses is a nested dict, not a planet-like entry
            continue

        if not isinstance(data, dict) or "longitude_360" not in data:
            # Skip entries that are not convertible planetary/ascendant bodies
            continue

        longitude = data["longitude_360"]
        base_sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        is_odd_sign = (base_sign % 2 == 0)
        
        # 1. Get Destination Sign
        varga_sign_index = get_varga_sign_index(varga_type, base_sign, degree_in_sign)
        
        # 2. Expand Degrees to 0-30 scale
        if varga_type == 30:
            # Custom Degree Expansion for Unequal Trimshamsha slices
            deg = degree_in_sign
            if is_odd_sign:
                if deg <= 5.0:   s_start, s_len = 0.0, 5.0
                elif deg <= 10.0: s_start, s_len = 5.0, 5.0
                elif deg <= 18.0: s_start, s_len = 10.0, 8.0
                elif deg <= 25.0: s_start, s_len = 18.0, 7.0
                else:             s_start, s_len = 25.0, 5.0
            else:
                if deg <= 5.0:    s_start, s_len = 0.0, 5.0
                elif deg <= 12.0: s_start, s_len = 5.0, 7.0
                elif deg <= 20.0: s_start, s_len = 12.0, 8.0
                elif deg <= 25.0: s_start, s_len = 20.0, 5.0
                else:             s_start, s_len = 25.0, 5.0
                
            expanded_degree = ((deg - s_start) / s_len) * 30.0
        else:
            # Standard equal division expansion
            varga_slice = 30.0 / varga_type
            fraction_in_part = degree_in_sign % varga_slice
            expanded_degree = fraction_in_part * varga_type
            
        d = int(expanded_degree)
        m_decimal = (expanded_degree - d) * 60
        m = int(m_decimal)
        s = (m_decimal - m) * 60
        
        varga_chart[key] = {
            "name": translate(key, "planet", lang), 
            "short_name": translate(key, "planet_short", lang), # <-- NEW
            "sign_index": varga_sign_index,
            "sign_name": translate(ZODIAC_SIGNS[varga_sign_index], "zodiac", lang), 
            "degree": d,
            "minute": m,
            "second": round(s, 2)
        }
        
        # NEW: Carry over the retrograde status from the D-1 chart
        if "is_retrograde" in data:
            varga_chart[key]["is_retrograde"] = data["is_retrograde"]
        
    return varga_chart

def calculate_all_vargas(chart_data: dict, lang: str = "en") -> dict:
    """
    Generates the complete Shodashavarga array (All 16 charts).
    """
    # Includes all 15 divisional charts + D1 Rasi
    vargas_to_calculate = [2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60]
    
    all_charts = {"D1_Rasi": chart_data}
    
    for v_num in vargas_to_calculate:
        chart_name = f"D{v_num}"
        all_charts[chart_name] = calculate_single_varga(chart_data, v_num, lang)
        
    return all_charts