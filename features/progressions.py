# features/progressions.py
import swisseph as swe
from models import BirthDetails
from utils import get_utc_decimal_hour
from core_math import calculate_base_positions

ASTRO_YEAR_DAYS = 365.24219

def get_julian_day(details: BirthDetails) -> float:
    utc_y, utc_m, utc_d, utc_h = get_utc_decimal_hour(
        details.year, details.month, details.day, 
        details.hour, details.minute, details.tz
    )
    return swe.julday(utc_y, utc_m, utc_d, utc_h)

def calculate_progressed_chart(birth: BirthDetails, target: BirthDetails) -> dict:
    jd_birth = get_julian_day(birth)
    jd_target = get_julian_day(target)
    age_in_years = (jd_target - jd_birth) / ASTRO_YEAR_DAYS
    jd_progressed = jd_birth + age_in_years
    
    y, m, d, decimal_hour = swe.revjul(jd_progressed, 1)
    h_int = int(decimal_hour)
    min_int = int(round((decimal_hour - h_int) * 60))
    if min_int == 60:
        min_int, h_int = 0, h_int + 1
        
    progressed_payload = BirthDetails(
        year=y, month=m, day=d, hour=h_int, minute=min_int,
        tz="UTC", lat=birth.lat, lon=birth.lon,
        ayanamsa=birth.ayanamsa, node_type=birth.node_type,
        lang=target.lang # <-- INJECTED REQUESTED LANGUAGE HERE
    )
    
    progressed_chart = calculate_base_positions(progressed_payload)
    
    progressed_chart["Metadata"] = {
        "Progressed_Age": round(age_in_years, 4),
        "Progressed_Date_UTC": f"{y}-{m:02d}-{d:02d} {h_int:02d}:{min_int:02d}"
    }
    
    return progressed_chart