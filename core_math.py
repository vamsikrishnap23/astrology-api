import swisseph as swe
from models import BirthDetails
from utils import format_longitude, get_utc_decimal_hour

def calculate_base_positions(birth: BirthDetails) -> dict:
    
    utc_year, utc_month, utc_day, utc_decimal_hour = get_utc_decimal_hour(
        birth.year, birth.month, birth.day, birth.hour, birth.minute, birth.tz
    )

    julian_day = swe.julday(utc_year, utc_month, utc_day, utc_decimal_hour)
    
    # 1. Apply Dynamic Ayanamsa
    if birth.ayanamsa == "kp":
        swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    else:
        swe.set_sid_mode(swe.SIDM_LAHIRI)

    # Use Geocentric for standard astrological compatibility
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    chart_data = {"Julian_Day": julian_day}

    # 2. Apply Dynamic Node Type
    rahu_flag = swe.TRUE_NODE if birth.node_type == "true" else swe.MEAN_NODE

    planets = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS,
        "Saturn": swe.SATURN, "Rahu": rahu_flag 
    }

    # 2. Standard Planets
    for name, planet_id in planets.items():
        data, _ = swe.calc_ut(julian_day, planet_id, flags)
        # data[3] will now contain the actual speed!
        chart_data[name] = format_longitude(data[0], data[3])

    # 3. Ketu Fix
    # Ketu is exactly opposite Rahu and moves in the exact same direction.
    ketu_longitude = (chart_data["Rahu"]["longitude_360"] + 180.0) % 360.0
    chart_data["Ketu"] = format_longitude(ketu_longitude)
    
    # Directly copy the exact retrograde boolean from Rahu
    chart_data["Ketu"]["is_retrograde"] = chart_data["Rahu"].get("is_retrograde", False)

    # 4. Calculate Ascendant AND 12 House Cusps
    # 'P' stands for Placidus, standard for KP and Advanced tables
    cusps, ascmc = swe.houses_ex(julian_day, birth.lat, birth.lon, b'P', flags)
    
    chart_data["Ascendant"] = format_longitude(ascmc[0])
    
    # Store all 12 house cusps
    chart_data["Houses"] = {}
    # Python tuples are 0-indexed (0 to 11 represents House 1 to House 12)
    for i in range(12):
        chart_data["Houses"][f"House_{i+1}"] = format_longitude(cusps[i])

    return chart_data