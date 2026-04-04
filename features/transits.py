# features/transits.py
from features.translator import translate # <-- ADDED IMPORT

# <-- ADDED 'lang' PARAMETER -->
def calculate_transit_relations(natal_chart: dict, transit_chart: dict, lang: str = "en") -> dict:
    """
    Calculates the relative house placement of transit planets 
    compared to the Natal Ascendant and Natal Moon.
    """
    relations = {}
    natal_asc_sign = natal_chart["Ascendant"]["sign_index"]
    natal_moon_sign = natal_chart["Moon"]["sign_index"]
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

    for planet in planets:
        if planet in transit_chart:
            transit_sign = transit_chart[planet]["sign_index"]
            transit_deg = transit_chart[planet]["degree"]
            transit_min = transit_chart[planet]["minute"]

            house_from_asc = (transit_sign - natal_asc_sign + 12) % 12 + 1
            house_from_moon = (transit_sign - natal_moon_sign + 12) % 12 + 1

            relations[planet] = {
                "planet_name": translate(planet, "planet", lang), # <-- TRANSLATED PLANET NAME
                "transit_sign_index": transit_sign,
                
                # <-- SAFELY TRANSLATE ZODIAC SIGN (Checking if it's already translated) -->
                "transit_sign_name": translate(transit_chart[planet]["sign_name"], "zodiac", lang), 
                
                "degree_format": f"{transit_deg}° {transit_min}'",
                "is_retrograde": transit_chart[planet].get("is_retrograde", False),
                "house_from_ascendant": house_from_asc,
                "house_from_moon": house_from_moon
            }

    return relations