from features.lords import get_advanced_lords

def get_occupying_house(planet_lon: float, houses: dict) -> int:
    """
    Checks the planet's longitude against the 12 house cusps to find its placement.
    Safely handles the 360-degree wraparound (e.g., from Pisces back to Aries).
    """
    for i in range(1, 13):
        current_cusp = houses[f"House_{i}"]["longitude_360"]
        next_house = i + 1 if i < 12 else 1
        next_cusp = houses[f"House_{next_house}"]["longitude_360"]

        if current_cusp < next_cusp:
            if current_cusp <= planet_lon < next_cusp:
                return i
        else: # Wraparound condition
            if planet_lon >= current_cusp or planet_lon < next_cusp:
                return i
    return 1

def build_advanced_tables(chart_data: dict) -> dict:
    planetary_table = []
    house_table = []
    
    # 1. Build Planetary Table as an Array (matches UI Table format perfectly)
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    
    for planet in planets:
        if planet in chart_data:
            data = chart_data[planet]
            lon = data["longitude_360"]
            lords = get_advanced_lords(lon)
            
            # Find house placement
            house_num = get_occupying_house(lon, chart_data.get("Houses", {}))
            
            # Format Position as DD:MM:SS
            pos = f"{data['degree']:02d}:{data['minute']:02d}:{int(data['second']):02d}"
            
            # Append (R) for retrogrades
            planet_name = f"{planet} (R)" if data.get("is_retrograde") else planet
            
            planetary_table.append({
                "Planet": planet_name,
                "Sign": data["sign_name"][:3], # E.g., 'Sco', 'Leo', 'Ari'
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
            lords = get_advanced_lords(data["longitude_360"])
            
            pos = f"{data['degree']:02d}:{data['minute']:02d}:{int(data['second']):02d}"
            
            house_table.append({
                "House": i,
                "Sign": data["sign_name"][:3],
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