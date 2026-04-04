# features/ashtakootam.py

# ==========================================
# 1. THE CLASSICAL MATRICES (B.V. Raman)
# ==========================================

GANA_MAP = [
    [6, 5, 1],
    [6, 6, 0],
    [1, 0, 6]  # Rakshasa Boy + Deva Girl = 1 (Standard accepted variant)
]

VASHYA_MAP = [
    [2.0, 1.0, 0.5, 0.0, 1.0],
    [0.0, 2.0, 1.0, 0.0, 1.0],
    [0.0, 1.0, 2.0, 0.0, 1.0],
    [0.5, 0.5, 1.0, 2.0, 0.0],
    [0.0, 1.0, 1.0, 0.0, 2.0]
]

# --- 3. TRUE YONI MATRIX (Max 4 Points) ---
# Order: Ashwa(0), Gaj(1), Mesh(2), Sarp(3), Shwan(4), Marjar(5), Mooshak(6), 
# Gau(7), Mahish(8), Vyaghra(9), Mrig(10), Vaanar(11), Simha(12), Nakul(13)

YONI_MAP = [
    [4, 2, 2, 3, 2, 2, 2, 1, 0, 1, 3, 3, 1, 2], # 0: Ashwa
    [2, 4, 3, 3, 2, 2, 2, 2, 3, 1, 2, 3, 0, 2], # 1: Gaj
    [2, 3, 4, 2, 1, 2, 1, 3, 3, 1, 2, 0, 1, 2], # 2: Mesh
    [3, 3, 2, 4, 2, 1, 1, 1, 1, 2, 2, 2, 2, 0], # 3: Sarp
    [2, 2, 1, 2, 4, 2, 1, 2, 2, 1, 0, 2, 1, 2], # 4: Shwan
    [2, 2, 2, 1, 2, 4, 0, 2, 2, 1, 3, 3, 2, 1], # 5: Marjar
    [2, 2, 1, 1, 1, 0, 4, 2, 2, 2, 2, 2, 1, 1], # 6: Mooshak
    [1, 2, 3, 1, 2, 2, 2, 4, 3, 0, 3, 2, 2, 2], # 7: Gau
    [0, 3, 3, 1, 2, 2, 2, 3, 4, 1, 2, 2, 2, 2], # 8: Mahish
    [1, 1, 1, 2, 1, 1, 2, 0, 1, 4, 1, 1, 1, 2], # 9: Vyaghra
    [3, 2, 2, 2, 0, 3, 2, 3, 2, 1, 4, 2, 1, 2], # 10: Mrig
    [3, 3, 0, 2, 2, 3, 2, 2, 2, 1, 2, 4, 1, 2], # 11: Vaanar
    [1, 0, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 4, 2], # 12: Simha
    [2, 2, 2, 0, 2, 1, 1, 2, 2, 2, 2, 2, 2, 4]  # 13: Nakul
]

NAISARGIKA_MAITRI = {
    "Sun": {"Friends": ["Moon", "Mars", "Jupiter"], "Neutrals": ["Mercury"], "Enemies": ["Venus", "Saturn"]},
    "Moon": {"Friends": ["Sun", "Mercury"], "Neutrals": ["Mars", "Jupiter", "Venus", "Saturn"], "Enemies": []},
    "Mars": {"Friends": ["Sun", "Moon", "Jupiter"], "Neutrals": ["Venus", "Saturn"], "Enemies": ["Mercury"]},
    "Mercury": {"Friends": ["Sun", "Venus"], "Neutrals": ["Mars", "Jupiter", "Saturn"], "Enemies": ["Moon"]},
    "Jupiter": {"Friends": ["Sun", "Moon", "Mars"], "Neutrals": ["Saturn"], "Enemies": ["Mercury", "Venus"]},
    "Venus": {"Friends": ["Mercury", "Saturn"], "Neutrals": ["Mars", "Jupiter"], "Enemies": ["Sun", "Moon"]},
    "Saturn": {"Friends": ["Mercury", "Venus"], "Neutrals": ["Jupiter"], "Enemies": ["Sun", "Moon", "Mars"]}
}


# ==========================================
# 2. STRING AND ARRAY MAPPINGS
# ==========================================

VARNA_STR = ["Brahmin", "Kshatriya", "Vaishya", "Shoodra"]
VASHYA_STR = ["Chatuspad", "Maanav", "Jalchara", "Vanchara", "Keeta"]
GANA_STR = ["Deva", "Manushya", "Rakshasa"]
NADI_STR = ["Adi", "Madhya", "Antya"]
YONI_STR = ["Ashwa", "Gaj", "Mesh", "Sarp", "Shwan", "Marjar", "Mooshak", "Gau", "Mahish", "Vyaghra", "Mrig", "Vaanar", "Simha", "Nakul"]

NAKSHATRAS = ["Ashwini", "Bharni", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatbhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

# Mapping Arrays
SIGN_TO_VARNA = [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0] 
SIGN_TO_VASHYA = [0, 0, 1, 2, 3, 1, 1, 4, 1, 2, 1, 2] 

# FIXED: Dhanishta (Index 22) maps to Simha (12). U.Ashadha (Index 20) maps to Nakul (13).
NAK_TO_YONI = [0, 1, 2, 3, 3, 4, 5, 2, 5, 6, 6, 7, 8, 9, 8, 9, 10, 10, 4, 11, 13, 11, 12, 0, 12, 7, 1]
NAK_TO_GANA = [0, 1, 2, 1, 0, 1, 0, 0, 2, 2, 1, 1, 0, 2, 0, 2, 0, 2, 2, 1, 1, 0, 2, 2, 1, 1, 0]
NAK_TO_NADI = [0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2]


# ==========================================
# 3. KUNDALI MILAN LOGIC
# ==========================================

def get_true_friendship(lord1: str, lord2: str) -> int:
    """Returns true friendship score: 0=Enemy, 1=Neutral, 2=Friend"""
    if lord1 == lord2: return 2
    if lord2 in NAISARGIKA_MAITRI[lord1]["Friends"]: return 2
    if lord2 in NAISARGIKA_MAITRI[lord1]["Neutrals"]: return 1
    return 0

def calc_tara(boy_nak: int, girl_nak: int) -> float:
    dist_1 = (girl_nak - boy_nak + 27) % 27 + 1
    score_1 = 0.0 if (dist_1 % 9) in [3, 5, 7] else 1.5
    
    dist_2 = (boy_nak - girl_nak + 27) % 27 + 1
    score_2 = 0.0 if (dist_2 % 9) in [3, 5, 7] else 1.5
    
    return score_1 + score_2

def calc_graha_maitri(b_feel: int, g_feel: int) -> float:
    total = b_feel + g_feel
    if total == 4: return 5.0 # Friend + Friend
    if total == 3: return 4.0 # Friend + Neutral
    if total == 2:
        if b_feel == 1 and g_feel == 1: return 3.0 # Neutral + Neutral
        return 1.0 # Friend + Enemy
    if total == 1: return 0.5 # Neutral + Enemy
    return 0.0 # Enemy + Enemy

def calc_bhakoot(boy_sign: int, girl_sign: int) -> float:
    rasi_diff = (boy_sign - girl_sign + 12) % 12
    if rasi_diff in [0, 2, 3, 6, 9, 10]:
        return 7.0
    return 0.0

def calculate_ashtakootam(boy_chart: dict, girl_chart: dict) -> dict:
    
    boy_sign = boy_chart["Moon"]["sign_index"]
    girl_sign = girl_chart["Moon"]["sign_index"]
    
    nak_length = 360.0 / 27.0
    boy_nak = int(boy_chart["Moon"]["longitude_360"] / nak_length)
    girl_nak = int(girl_chart["Moon"]["longitude_360"] / nak_length)

    b_varna, g_varna = SIGN_TO_VARNA[boy_sign], SIGN_TO_VARNA[girl_sign]
    b_vashya, g_vashya = SIGN_TO_VASHYA[boy_sign], SIGN_TO_VASHYA[girl_sign]
    b_yoni, g_yoni = NAK_TO_YONI[boy_nak], NAK_TO_YONI[girl_nak]
    b_gana, g_gana = NAK_TO_GANA[boy_nak], NAK_TO_GANA[girl_nak]
    b_nadi, g_nadi = NAK_TO_NADI[boy_nak], NAK_TO_NADI[girl_nak]
    b_lord, g_lord = SIGN_LORDS[boy_sign], SIGN_LORDS[girl_sign]

    # Use the TRUE friendship function
    b_lord_feels = get_true_friendship(b_lord, g_lord)
    g_lord_feels = get_true_friendship(g_lord, b_lord)

    match_table = [
        {
            "Attribute": "Varna", "Desc": "Natural Refinement / Work",
            "Male": VARNA_STR[b_varna], "Female": VARNA_STR[g_varna],
            "Outof": 1, "Received": 1.0 if b_varna <= g_varna else 0.0 # Lower index = Higher caste
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
            "Outof": 5, "Received": calc_graha_maitri(b_lord_feels, g_lord_feels)
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
        "Percentage": f"{(total_score / 36.0) * 100:.2f}%",
        "Dosha_Warnings": []
    }