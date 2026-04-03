import swisseph as swe

# Fixed list of Zodiac signs mapping to the 0-11 index
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def format_longitude(decimal_degree: float) -> dict:
    """
    Converts a raw 360-degree floating point into structured astrological data.
    """
    sign_index = int(decimal_degree / 30)
    sign_name = ZODIAC_SIGNS[sign_index]

    sign_degree = decimal_degree % 30
    
    d = int(sign_degree)
    m_decimal = (sign_degree - d) * 60
    m = int(m_decimal)
    s = (m_decimal - m) * 60

    return {
        "longitude_360": round(decimal_degree, 6),
        "sign_index": sign_index,  
        "sign_name": sign_name,
        "degree": d,
        "minute": m,
        "second": round(s, 2)
    }


def jd_to_utc_time(jd: float) -> str:
    """
    Converts a Julian Day fraction into a readable UTC Time string (HH:MM).
    """
    # revjul returns Year, Month, Day, and a decimal Hour (e.g., 14.5 for 2:30 PM)
    year, month, day, decimal_hour = swe.revjul(jd)
    
    hours = int(decimal_hour)
    minutes = int(round((decimal_hour - hours) * 60))
    
    # Handle overflow if minutes round up to 60
    if minutes == 60:
        minutes = 0
        hours += 1

    return f"{hours:02d}:{minutes:02d} UTC"


from datetime import datetime, timedelta, timezone

def get_utc_decimal_hour(year: int, month: int, day: int, hour: int, minute: int, tz: str):
    """
    Safely converts the provided time to UTC based on the selected timezone.
    Handles day/month/year rollovers automatically.
    """
    # 1. Determine the hour offset
    if tz == "IST":
        offset_hours = 5.5
    else:  # UTC
        offset_hours = 0.0
        
    offset_delta = timedelta(hours=offset_hours)
    local_tz = timezone(offset_delta)
    
    # 2. Create the local datetime object
    local_dt = datetime(year, month, day, hour, minute, tzinfo=local_tz)
    
    # 3. Convert exactly to UTC
    utc_dt = local_dt.astimezone(timezone.utc)
    
    # 4. Return the safely converted UTC Year, Month, Day, and Decimal Hour
    utc_decimal = utc_dt.hour + (utc_dt.minute / 60.0)
    
    return utc_dt.year, utc_dt.month, utc_dt.day, utc_decimal