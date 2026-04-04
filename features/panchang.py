import swisseph as swe
from utils import jd_to_utc_time
from features.translator import translate  # <-- ADDED TRANSLATION IMPORT

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

# <-- ADDED 'lang' PARAMETER HERE
def calculate_panchang(chart_data: dict, lat: float, lon: float, lang: str = "en") -> dict:
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

    # --- NEW TRANSLATION LOGIC ---
    final_vara = translate(VARAS[vara_index], "vara", lang)
    final_paksha = translate(paksham, "paksha", lang)
    final_tithi = translate(TITHIS[tithi_index], "tithi", lang)
    final_yoga = translate(YOGAS[yoga_index], "yoga", lang)
    final_karana = translate(get_karana_name(karana_index), "karana", lang)
    final_nakshatra = translate(nakshatram_name, "nakshatra", lang) # If you add TE_NAKSHATRA later

    return {
        "Paksham": final_paksha,
        "Vara": final_vara,
        "Tithi": final_tithi,
        "Nakshatram": {
            "name": final_nakshatra,
            "padam": padam,
            "full_format": f"{final_nakshatra}-{padam}"
        },
        "Yogam": final_yoga,
        "Karanam": final_karana,
        "Sunrise": jd_to_utc_time(sunrise_jd),
        "Sunset": jd_to_utc_time(sunset_jd)
    }