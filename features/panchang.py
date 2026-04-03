import swisseph as swe
from utils import jd_to_utc_time

# --- Sanskrit Dictionaries ---
TITHIS = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", 
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi", 
    "Trayodashi", "Chaturdashi", "Purnima", # Shukla (Waxing)
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", 
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi", 
    "Trayodashi", "Chaturdashi", "Amavasya" # Krishna (Waning)
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", 
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", 
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", 
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

YOGAS = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", 
    "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", 
    "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva", 
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
]

VARAS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
MOVABLE_KARANAS = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti"]

def get_karana_name(index: int) -> str:
    """There are 60 Karanas in a lunar month. 1st is fixed, next 56 are cyclic, last 3 are fixed."""
    if index == 0: return "Kintughna"
    if index >= 57:
        fixed_end = ["Shakuni", "Chatushpada", "Naga"]
        return fixed_end[index - 57]
    return MOVABLE_KARANAS[(index - 1) % 7]

def calculate_panchang(chart_data: dict, lat: float, lon: float) -> dict:
    """Calculates all detailed Panchang limbs including Padam and Sunrise."""
    
    sun_lon = chart_data["Sun"]["longitude_360"]
    moon_lon = chart_data["Moon"]["longitude_360"]
    jd = chart_data["Julian_Day"]

    # 1. Paksham & Tithi
    moon_phase_angle = (moon_lon - sun_lon) % 360.0
    tithi_index = int(moon_phase_angle / 12.0)
    paksham = "Shukla" if tithi_index < 15 else "Krishna"

    # 2. Nakshatram & Padam
    nak_length = 360.0 / 27.0
    nak_index = int(moon_lon / nak_length)
    
    # Find how deep the moon is into the current Nakshatra
    degrees_in_nak = moon_lon % nak_length
    # Divide by 4 (since each Nakshatra has 4 padams)
    padam = int(degrees_in_nak / (nak_length / 4.0)) + 1
    nakshatram_name = NAKSHATRAS[nak_index]

    # 3. Yogam
    yoga_angle = (sun_lon + moon_lon) % 360.0
    yoga_index = int(yoga_angle / nak_length)

    # 4. Karanam
    karana_index = int(moon_phase_angle / 6.0)

    # 5. Vara (Weekday)
    vara_index = int((jd + 1.5) % 7)

    # 6. Sunrise & Sunset
    geopos = (lon, lat, 0.0) 
    
    # NEW pyswisseph signature: swe.rise_trans(jdut, body, rsmi, geopos)
    # We calculate for the previous day (jd - 1.0) to find the morning sunrise.
    rise_calc = swe.rise_trans(jd - 1.0, swe.SUN, swe.CALC_RISE, geopos)
    set_calc = swe.rise_trans(jd - 1.0, swe.SUN, swe.CALC_SET, geopos)
    
    # The function returns a nested tuple: (status_flag, (time_jd, ...))
    # We must access index [1][0] to get the actual Julian Day time.
    sunrise_jd = rise_calc[1][0]
    sunset_jd = set_calc[1][0]

    return {
        "Paksham": paksham,
        "Vara": VARAS[vara_index],
        "Tithi": TITHIS[tithi_index],
        "Nakshatram": {
            "name": nakshatram_name,
            "padam": padam,
            "full_format": f"{nakshatram_name}-{padam}"
        },
        "Yogam": YOGAS[yoga_index],
        "Karanam": get_karana_name(karana_index),
        "Sunrise": jd_to_utc_time(sunrise_jd),
        "Sunset": jd_to_utc_time(sunset_jd)
    }