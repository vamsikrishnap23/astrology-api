import swisseph as swe
from models import BirthDetails
from utils import format_longitude, get_utc_decimal_hour

def calculate_base_positions(birth: BirthDetails) -> dict:
    """
    The core ephemeris engine. Returns exact planetary positions.
    """
    # 1. Pass the new birth.tz selector to the converter
    utc_year, utc_month, utc_day, utc_decimal_hour = get_utc_decimal_hour(
        birth.year, birth.month, birth.day, birth.hour, birth.minute, birth.tz
    )

    # 2. Calculate Julian Day using the SAFE UTC time
    julian_day = swe.julday(utc_year, utc_month, utc_day, utc_decimal_hour)

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    chart_data = {"Julian_Day": julian_day}

    planets = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS,
        "Saturn": swe.SATURN, "Rahu": swe.TRUE_NODE 
    }

    # 1. Standard Planets
    for name, planet_id in planets.items():
        data, _ = swe.calc_ut(julian_day, planet_id, flags)
        chart_data[name] = format_longitude(data[0])

    # 2. Ketu
    ketu_longitude = (chart_data["Rahu"]["longitude_360"] + 180.0) % 360.0
    chart_data["Ketu"] = format_longitude(ketu_longitude)

    # 3. Ascendant
    cusps, ascmc = swe.houses_ex(julian_day, birth.lat, birth.lon, b'P', flags)
    chart_data["Ascendant"] = format_longitude(ascmc[0])

    return chart_data