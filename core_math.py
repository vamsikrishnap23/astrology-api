import swisseph as swe
from models import BirthDetails
from utils import format_longitude, get_utc_decimal_hour
from features.translator import translate # <-- ADDED IMPORT

def calculate_base_positions(birth: BirthDetails) -> dict:
    lang = getattr(birth, 'lang', 'en') # <-- Extract Lang Safely
    
    utc_year, utc_month, utc_day, utc_decimal_hour = get_utc_decimal_hour(
        birth.year, birth.month, birth.day, birth.hour, birth.minute, birth.tz
    )

    julian_day = swe.julday(utc_year, utc_month, utc_day, utc_decimal_hour)
    
    if birth.ayanamsa == "kp":
        swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    else:
        swe.set_sid_mode(swe.SIDM_LAHIRI)

    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    chart_data = {"Julian_Day": julian_day}
    rahu_flag = swe.TRUE_NODE if birth.node_type == "true" else swe.MEAN_NODE

    planets = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS,
        "Saturn": swe.SATURN, "Rahu": rahu_flag 
    }

    # Standard Planets
    for name, planet_id in planets.items():
        data, _ = swe.calc_ut(julian_day, planet_id, flags)
        chart_data[name] = format_longitude(data[0], data[3], lang) 
        chart_data[name]["name"] = translate(name, "planet", lang)  
        chart_data[name]["short_name"] = translate(name, "planet_short", lang) # <-- NEW

    # 2. Ketu Fix
    ketu_longitude = (chart_data["Rahu"]["longitude_360"] + 180.0) % 360.0
    chart_data["Ketu"] = format_longitude(ketu_longitude, lang=lang) 
    chart_data["Ketu"]["is_retrograde"] = chart_data["Rahu"].get("is_retrograde", False)
    chart_data["Ketu"]["name"] = translate("Ketu", "planet", lang)   
    chart_data["Ketu"]["short_name"] = translate("Ketu", "planet_short", lang) # <-- NEW

    # 3. Ascendant
    cusps, ascmc = swe.houses_ex(julian_day, birth.lat, birth.lon, b'P', flags)
    chart_data["Ascendant"] = format_longitude(ascmc[0], lang=lang) 
    chart_data["Ascendant"]["name"] = translate("Ascendant", "planet", lang) 
    chart_data["Ascendant"]["short_name"] = translate("Ascendant", "planet_short", lang) # <-- NEW
    
    chart_data["Houses"] = {}
    for i in range(12):
        chart_data["Houses"][f"House_{i+1}"] = format_longitude(cusps[i], lang=lang)

    return chart_data