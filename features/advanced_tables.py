# features/advanced_tables.py
from features.lords import get_advanced_lords
from features.translator import translate # <-- ADDED IMPORT

def get_occupying_house(planet_lon: float, houses: dict) -> int:
    """Checks the planet's longitude against the 12 house cusps to find its placement."""
    for i in range(1, 13):
        current_cusp = houses[f"House_{i}"]["longitude_360"]
        next_house = i + 1 if i < 12 else 1
        next_cusp = houses[f"House_{next_house}"]["longitude_360"]

        if current_cusp < next_cusp:
            if current_cusp <= planet_lon < next_cusp:
                return i
        else:
            if planet_lon >= current_cusp or planet_lon < next_cusp:
                return i
    return 1

# <-- ADDED 'lang' PARAMETER -->
def build_advanced_tables(chart_data: dict, lang: str = "en") -> dict:
    planetary_table = []
    house_table = []
    
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    
    # 1. Build Planetary Table
    for planet in planets:
        if planet in chart_data:
            data = chart_data[planet]
            lon = data["longitude_360"]
            
            # Pass language down to the Lords calculator
            lords = get_advanced_lords(lon, lang)
            
            house_num = get_occupying_house(lon, chart_data.get("Houses", {}))
            pos = f"{data['degree']:02d}:{data['minute']:02d}:{int(data['second']):02d}"
            
            # <-- TRANSLATE PLANET & HANDLE RETROGRADE -->
            base_planet_name = translate(planet, "planet", lang)
            planet_name = f"{base_planet_name} (R)" if data.get("is_retrograde") else base_planet_name
            
            # <-- HANDLE SIGN DISPLAY SAFELY -->
            # Use full translated name for Telugu, keep 3-letter slice for English
            sign_display = translate(data["sign_name"], "zodiac", lang) if lang != "en" else data["sign_name"][:3]
            
            planetary_table.append({
                "Planet": planet_name,
                "Sign": sign_display, 
                "Position": pos,
                "House": house_num,
                "Star": lords["Star"],
                "Sign Lord": lords["SiL"],
                "Star Lord": lords["StL"],
                "Sub Lord": lords["SL"],
                "SS Lord": lords["SSL"],
                "SSS Lord": lords["SSSL"]
            })

    # 2. Build House Table
    if "Houses" in chart_data:
        for i in range(1, 13):
            house_key = f"House_{i}"
            data = chart_data["Houses"][house_key]
            
            # Pass language down to the Lords calculator
            lords = get_advanced_lords(data["longitude_360"], lang)
            
            pos = f"{data['degree']:02d}:{data['minute']:02d}:{int(data['second']):02d}"
            
            # <-- HANDLE SIGN DISPLAY SAFELY -->
            sign_display = translate(data["sign_name"], "zodiac", lang) if lang != "en" else data["sign_name"][:3]
            
            house_table.append({
                "House": i,
                "Sign": sign_display,
                "Position": pos,
                "Star": lords["Star"],
                "Sign Lord": lords["SiL"],
                "Star Lord": lords["StL"],
                "Sub Lord": lords["SL"],
                "SS Lord": lords["SSL"],
                "SSS Lord": lords["SSSL"]
            })
            
    return {
        "Planetary_Table": planetary_table,
        "House_Table": house_table
    }