import swisseph as swe
from models import BirthDetails
from utils import get_utc_decimal_hour
from core_math import calculate_base_positions

# The standard tropical solar year used for time translation
ASTRO_YEAR_DAYS = 365.24219

def get_julian_day(details: BirthDetails) -> float:
    """Helper function to cleanly extract the exact Julian Day from a BirthDetails payload."""
    utc_y, utc_m, utc_d, utc_h = get_utc_decimal_hour(
        details.year, details.month, details.day, 
        details.hour, details.minute, details.tz
    )
    return swe.julday(utc_y, utc_m, utc_d, utc_h)

def calculate_progressed_chart(birth: BirthDetails, target: BirthDetails) -> dict:
    """
    Calculates the Secondary Progression chart (1 Day = 1 Year).
    Returns the progressed chart using your existing core engine.
    """
    # 1. Get exact Julian Days
    jd_birth = get_julian_day(birth)
    jd_target = get_julian_day(target)
    
    # 2. Calculate Exact Age in Solar Years
    age_in_years = (jd_target - jd_birth) / ASTRO_YEAR_DAYS
    
    # 3. Apply the Progression Formula (1 Day = 1 Year)
    # We add the age (as days) to the birth date
    jd_progressed = jd_birth + age_in_years
    
    # 4. Convert the Progressed JD back into a calendar date (Standard Gregorian)
    y, m, d, decimal_hour = swe.revjul(jd_progressed, 1)
    
    h_int = int(decimal_hour)
    min_int = int(round((decimal_hour - h_int) * 60))
    if min_int == 60:
        min_int, h_int = 0, h_int + 1
        
    # 5. Create a new "BirthDetails" payload representing the Progressed Date.
    # Note: Progressions always retain the original birth location coordinates!
    progressed_payload = BirthDetails(
        year=y,
        month=m,
        day=d,
        hour=h_int,
        minute=min_int,
        tz="UTC", # The converted date is strictly UTC, so we force the UTC flag
        lat=birth.lat,
        lon=birth.lon,
        ayanamsa=birth.ayanamsa,
        node_type=birth.node_type
    )
    
    # 6. Run it through your existing, highly-tested core engine
    progressed_chart = calculate_base_positions(progressed_payload)
    
    # Add a metadata tag so the UI knows exactly what progressed age this represents
    progressed_chart["Metadata"] = {
        "Progressed_Age": round(age_in_years, 4),
        "Progressed_Date_UTC": f"{y}-{m:02d}-{d:02d} {h_int:02d}:{min_int:02d}"
    }
    
    return progressed_chart