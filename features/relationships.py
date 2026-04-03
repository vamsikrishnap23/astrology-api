# features/relationships.py

# 1. Natural Relationship Matrix (Parashari Standard)
NAISARGIKA_MAITRI = {
    "Sun": {"Friends": ["Moon", "Mars", "Jupiter"], "Neutrals": ["Mercury"], "Enemies": ["Venus", "Saturn"]},
    "Moon": {"Friends": ["Sun", "Mercury"], "Neutrals": ["Mars", "Jupiter", "Venus", "Saturn"], "Enemies": []},
    "Mars": {"Friends": ["Sun", "Moon", "Jupiter"], "Neutrals": ["Venus", "Saturn"], "Enemies": ["Mercury"]},
    "Mercury": {"Friends": ["Sun", "Venus"], "Neutrals": ["Mars", "Jupiter", "Saturn"], "Enemies": ["Moon"]},
    "Jupiter": {"Friends": ["Sun", "Moon", "Mars"], "Neutrals": ["Saturn"], "Enemies": ["Mercury", "Venus"]},
    "Venus": {"Friends": ["Mercury", "Saturn"], "Neutrals": ["Mars", "Jupiter"], "Enemies": ["Sun", "Moon"]},
    "Saturn": {"Friends": ["Mercury", "Venus"], "Neutrals": ["Jupiter"], "Enemies": ["Sun", "Moon", "Mars"]}
}

def get_natural_relationship(planet: str, target_planet: str) -> int:
    """Returns: 1 (Friend), 0 (Neutral), -1 (Enemy)"""
    if target_planet in NAISARGIKA_MAITRI[planet]["Friends"]: return 1
    if target_planet in NAISARGIKA_MAITRI[planet]["Neutrals"]: return 0
    return -1

def get_temporary_relationship(planet_sign: int, target_sign: int) -> int:
    """
    Temporary Friends: Planets sitting in the 2nd, 3rd, 4th, 10th, 11th, or 12th house from the planet.
    Temporary Enemies: Planets sitting in the 1st, 5th, 6th, 7th, 8th, or 9th house.
    Returns: 1 (Friend), -1 (Enemy)
    """
    # Calculate distance counting the planet's sign as house 1
    distance = (target_sign - planet_sign + 12) % 12 + 1
    
    if distance in [2, 3, 4, 10, 11, 12]:
        return 1
    return -1

def get_compound_relationship(planet: str, target_planet: str, chart_data: dict) -> str:
    """
    Calculates the Panchadha Maitri (5-fold relationship).
    """
    if planet == target_planet:
        return "Own"
        
    planet_sign = chart_data[planet]["sign_index"]
    target_sign = chart_data[target_planet]["sign_index"]
    
    natural = get_natural_relationship(planet, target_planet)
    temporary = get_temporary_relationship(planet_sign, target_sign)
    
    total_score = natural + temporary
    
    # Map the sum to the 5-point scale
    if total_score == 2: return "Great_Friend"    # 1 + 1
    if total_score == 1: return "Friend"          # 1 + 0 or 0 + 1 (not possible with -1 temp)
    if total_score == 0: return "Neutral"         # 1 + -1 or -1 + 1
    if total_score == -1: return "Enemy"          # 0 + -1
    if total_score == -2: return "Great_Enemy"    # -1 + -1