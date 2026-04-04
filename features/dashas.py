from datetime import datetime, timedelta
import calendar
import swisseph as swe
from features.translator import translate # <-- ADDED IMPORT

DASHA_LORDS = [
    ("Ketu", 7.0), ("Venus", 20.0), ("Sun", 6.0), ("Moon", 10.0),
    ("Mars", 7.0), ("Rahu", 18.0), ("Jupiter", 16.0), ("Saturn", 19.0),
    ("Mercury", 17.0)
]

def add_vedic_period(start_dt: datetime, period_years: float) -> datetime:
    """
    Replicates traditional astrology calendar math.
    1 Year = 1 Calendar Year. Fractions use 1 Month = 30 Days.
    """
    y = int(period_years)
    remainder = period_years - y
    
    total_months = remainder * 12
    m = int(total_months)
    d = int(round(((total_months - m) * 30)))
    
    # 1. Add Months and calculate overflow into Years
    new_month = start_dt.month + m
    new_year = start_dt.year + y + ((new_month - 1) // 12)
    new_month = ((new_month - 1) % 12) + 1
    
    # 2. Prevent calendar crash (e.g., Feb 29 on a non-leap year)
    max_day = calendar.monthrange(new_year, new_month)[1]
    new_day = min(start_dt.day, max_day)
    
    base_dt = datetime(new_year, new_month, new_day)
    
    # 3. Add remaining exact days
    return base_dt + timedelta(days=d)

# <-- ADDED 'lang' PARAMETER -->
def calculate_antardashas(md_lord_index: int, start_dt: datetime, md_years: float, lang: str = "en") -> list:
    """Calculates sub-periods using the exact proportion of the calendar."""
    ad_list = []
    current_dt = start_dt
    
    for i in range(9):
        ad_index = (md_lord_index + i) % 9
        ad_lord, ad_years = DASHA_LORDS[ad_index]
        
        # Proportional calculation
        ad_length_years = (md_years * ad_years) / 120.0
        end_dt = add_vedic_period(current_dt, ad_length_years)
        
        ad_list.append({
            "lord": translate(ad_lord, "planet", lang), # <-- TRANSLATED LORD
            "start_date": current_dt.strftime("%Y-%m-%d"),
            "end_date": end_dt.strftime("%Y-%m-%d")
        })
        current_dt = end_dt
        
    return ad_list

# <-- ADDED 'lang' PARAMETER -->
def calculate_dashas(chart_data: dict, lang: str = "en") -> list:
    """Calculates the True Origin Mahadasha timeline."""
    moon_lon = chart_data["Moon"]["longitude_360"]
    jd_birth = chart_data["Julian_Day"]

    y, m, d, decimal_hour = swe.revjul(jd_birth)
    h_int = int(decimal_hour)
    min_int = int(round((decimal_hour - h_int) * 60))
    if min_int == 60: min_int, h_int = 0, h_int + 1
    birth_dt = datetime(y, m, d, h_int, min_int)

    nak_length = 360.0 / 27.0
    nak_exact = moon_lon / nak_length
    nak_index = int(nak_exact)
    
    fraction_passed = nak_exact - nak_index
    md_index = nak_index % 9
    start_lord, lord_years = DASHA_LORDS[md_index]
    
    # 1. Calculate True Origin backwards from Birth Date
    days_passed_before_birth = fraction_passed * lord_years * 365.2425
    true_start_dt = birth_dt - timedelta(days=days_passed_before_birth)
    
    # Align to midnight for clean output display
    current_dt = datetime(true_start_dt.year, true_start_dt.month, true_start_dt.day)

    # 2. Build Timeline completely using Calendar Math
    timeline = []
    for i in range(9):
        current_md_index = (md_index + i) % 9
        md_lord, md_years = DASHA_LORDS[current_md_index]
        
        md_end_dt = add_vedic_period(current_dt, md_years)
        
        # <-- PASSED 'lang' DOWN TO ANTARDASHAS
        antardashas = calculate_antardashas(current_md_index, current_dt, md_years, lang) 
        
        timeline.append({
            "lord": translate(md_lord, "planet", lang), # <-- TRANSLATED LORD
            "start_date": current_dt.strftime("%Y-%m-%d"),
            "end_date": md_end_dt.strftime("%Y-%m-%d"),
            "antardashas": antardashas
        })
        
        current_dt = md_end_dt

    return timeline