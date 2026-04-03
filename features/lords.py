DASHA_LORDS = [
    ("Ketu", 7.0), ("Venus", 20.0), ("Sun", 6.0), ("Moon", 10.0),
    ("Mars", 7.0), ("Rahu", 18.0), ("Jupiter", 16.0), ("Saturn", 19.0),
    ("Mercury", 17.0)
]

SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", 
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", 
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", 
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", 
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_advanced_lords(longitude: float) -> dict:
    # 1. Sign Lord (SiL)
    sign_index = int(longitude / 30.0)
    sil = SIGN_LORDS[sign_index]
    
    # 2. Star Lord (StL) & Padam
    nak_length = 360.0 / 27.0
    degrees_in_nak = longitude % nak_length
    nak_index = int(longitude / nak_length)
    
    padam = int(degrees_in_nak / (nak_length / 4.0)) + 1
    star_format = f"{NAKSHATRAS[nak_index]} - {padam}"
    
    stl_index = nak_index % 9
    stl = DASHA_LORDS[stl_index][0]
    
    # 3. Sub Lord (SL)
    current_index = stl_index
    passed_deg = 0.0
    
    for _ in range(9):
        lord_name, lord_years = DASHA_LORDS[current_index]
        sl_span = (lord_years / 120.0) * nak_length
        if passed_deg + sl_span > degrees_in_nak:
            sl = lord_name
            sl_start = passed_deg
            break
        passed_deg += sl_span
        current_index = (current_index + 1) % 9
        
    # 4. Sub-Sub Lord (SSL)
    degrees_in_sl = degrees_in_nak - sl_start
    ssl_passed = 0.0
    
    for _ in range(9):
        lord_name, lord_years = DASHA_LORDS[current_index]
        ssl_span = (lord_years / 120.0) * sl_span
        if ssl_passed + ssl_span > degrees_in_sl:
            ssl = lord_name
            ssl_start = ssl_passed
            break
        ssl_passed += ssl_span
        current_index = (current_index + 1) % 9

    # 5. Sub-Sub-Sub Lord (SSSL)
    degrees_in_ssl_span = degrees_in_sl - ssl_start
    sssl_passed = 0.0
    sssl = ""
    
    for _ in range(9):
        lord_name, lord_years = DASHA_LORDS[current_index]
        sssl_span = (lord_years / 120.0) * ssl_span
        if sssl_passed + sssl_span > degrees_in_ssl_span:
            sssl = lord_name
            break
        sssl_passed += sssl_span
        current_index = (current_index + 1) % 9

    return {
        "Star": star_format,
        "SiL": sil,
        "StL": stl,
        "SL": sl,
        "SSL": ssl,
        "SSSL": sssl
    }