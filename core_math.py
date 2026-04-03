import swisseph as swe
from models import BirthDetails
from utils import format_longitude, get_utc_decimal_hour

def calculate_base_positions(birth: BirthDetails) -> dict:
    
    utc_year, utc_month, utc_day, utc_decimal_hour = get_utc_decimal_hour(
        birth.year, birth.month, birth.day, birth.hour, birth.minute, birth.tz
    )

    julian_day = swe.julday(utc_year, utc_month, utc_day, utc_decimal_hour)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    swe.set_topo(birth.lon, birth.lat, 0.0)
    
    # 1. THE FIX: Add swe.FLG_SPEED to force daily motion calculations
    # flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_TOPOCTR | swe.FLG_SPEED
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    chart_data = {"Julian_Day": julian_day}

    planets = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS,
        "Saturn": swe.SATURN, "Rahu": swe.TRUE_NODE 
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

    # 4. Ascendant
    cusps, ascmc = swe.houses_ex(julian_day, birth.lat, birth.lon, b'P', flags)
    chart_data["Ascendant"] = format_longitude(ascmc[0])

    return chart_data