from features.ashtakootam_matrices import GANA_MAP, VASHYA_MAP, YONI_MAP
from features.ashtakootam_logic import (
    calc_varna, calc_tara, calc_graha_maitri, calc_bhakoot
)

# --- STRING TRANSLATION DICTIONARIES ---
VARNA_STR = ["Brahmin", "Kshatriya", "Vaishya", "Shoodra"]
VASHYA_STR = ["Chatuspad", "Maanav", "Jalchara", "Vanchara", "Keeta"]
GANA_STR = ["Deva", "Manushya", "Rakshasa"]
NADI_STR = ["Adi", "Madhya", "Antya"]
YONI_STR = ["Ashwa", "Gaj", "Mesh", "Sarp", "Shwan", "Marjar", "Mooshak", "Gau", "Mahish", "Vyaghra", "Mrig", "Vaanar", "Simha", "Nakul"]

NAKSHATRAS = ["Ashwini", "Bharni", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatbhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]

# --- PLANETARY LORDS (For Graha Maitri) ---
# Maps the 12 signs to their ruling planet name
SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

# --- MAPPING ARRAYS (0-Indexed) ---
SIGN_TO_VARNA = [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0] 
SIGN_TO_VASHYA = [0, 0, 1, 2, 3, 1, 1, 4, 1, 2, 1, 2] 
NAK_TO_YONI = [0, 1, 2, 3, 3, 4, 5, 2, 5, 6, 6, 7, 8, 9, 8, 9, 10, 10, 4, 11, 12, 11, 13, 0, 13, 7, 1]
NAK_TO_GANA = [0, 1, 2, 1, 0, 1, 0, 0, 2, 2, 1, 1, 0, 2, 0, 2, 0, 2, 2, 1, 1, 0, 2, 2, 1, 1, 0]
NAK_TO_NADI = [0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2]

def get_simplified_friendship(lord1: str, lord2: str) -> int:
    """Simplified fallback for Lord Friendship (0=Enemy, 1=Neutral, 2=Friend)."""
    if lord1 == lord2: return 2
    # In a production app, you would map the full 7x7 friendship matrix here.
    # For now, we return 1 (Neutral) to allow calculation.
    return 1

def calculate_ashtakootam(boy_chart: dict, girl_chart: dict) -> dict:
    
    # 1. Extract Data
    boy_sign = boy_chart["Moon"]["sign_index"]
    girl_sign = girl_chart["Moon"]["sign_index"]
    
    nak_length = 360.0 / 27.0
    boy_nak = int(boy_chart["Moon"]["longitude_360"] / nak_length)
    girl_nak = int(girl_chart["Moon"]["longitude_360"] / nak_length)

    # 2. Map to Indices
    b_varna, g_varna = SIGN_TO_VARNA[boy_sign], SIGN_TO_VARNA[girl_sign]
    b_vashya, g_vashya = SIGN_TO_VASHYA[boy_sign], SIGN_TO_VASHYA[girl_sign]
    b_yoni, g_yoni = NAK_TO_YONI[boy_nak], NAK_TO_YONI[girl_nak]
    b_gana, g_gana = NAK_TO_GANA[boy_nak], NAK_TO_GANA[girl_nak]
    b_nadi, g_nadi = NAK_TO_NADI[boy_nak], NAK_TO_NADI[girl_nak]
    
    b_lord, g_lord = SIGN_LORDS[boy_sign], SIGN_LORDS[girl_sign]

    # 3. Build the UI Match Table Array
    match_table = [
        {
            "Attribute": "Varna", "Desc": "Natural Refinement / Work",
            "Male": VARNA_STR[b_varna], "Female": VARNA_STR[g_varna],
            "Outof": 1, "Received": 1.0 if b_varna <= g_varna else 0.0
        },
        {
            "Attribute": "Vashya", "Desc": "Innate Giving / Attraction towards each other",
            "Male": VASHYA_STR[b_vashya], "Female": VASHYA_STR[g_vashya],
            "Outof": 2, "Received": VASHYA_MAP[b_vashya][g_vashya]
        },
        {
            "Attribute": "Tara", "Desc": "Comfort - Prosperity - Health",
            "Male": NAKSHATRAS[boy_nak], "Female": NAKSHATRAS[girl_nak],
            "Outof": 3, "Received": calc_tara(boy_nak, girl_nak)
        },
        {
            "Attribute": "Yoni", "Desc": "Intimate Physical",
            "Male": YONI_STR[b_yoni], "Female": YONI_STR[g_yoni],
            "Outof": 4, "Received": float(YONI_MAP[b_yoni][g_yoni])
        },
        {
            "Attribute": "Maitri", "Desc": "Friendship",
            "Male": b_lord, "Female": g_lord,
            "Outof": 5, "Received": calc_graha_maitri(get_simplified_friendship(b_lord, g_lord), get_simplified_friendship(g_lord, b_lord))
        },
        {
            "Attribute": "Gan", "Desc": "Temperament",
            "Male": GANA_STR[b_gana], "Female": GANA_STR[g_gana],
            "Outof": 6, "Received": float(GANA_MAP[b_gana][g_gana])
        },
        {
            "Attribute": "Bhakut", "Desc": "Constructive Ability / Society and Couple",
            "Male": boy_chart["Moon"]["sign_name"], "Female": girl_chart["Moon"]["sign_name"],
            "Outof": 7, "Received": calc_bhakoot(boy_sign, girl_sign)
        },
        {
            "Attribute": "Nadi", "Desc": "Progeny / Excess",
            "Male": NADI_STR[b_nadi], "Female": NADI_STR[g_nadi],
            "Outof": 8, "Received": 0.0 if b_nadi == g_nadi else 8.0
        }
    ]

    total_score = sum(row["Received"] for row in match_table)

    return {
        "Match_Table": match_table,
        "Total_Score": total_score,
        "Max_Possible": 36.0,
        "Percentage": f"{(total_score / 36.0) * 100:.2f}%"
    }