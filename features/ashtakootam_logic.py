# features/ashtakootam_logic.py

from features.ashtakootam_matrices import GANA_MAP, VASHYA_MAP, YONI_MAP

def calc_varna(boy_varna: int, girl_varna: int) -> float:
    """
    Varna (1 Point Max) - Social duty mapping.
    1 point if Boy's Varna is >= Girl's Varna.
    """
    return 1.0 if boy_varna >= girl_varna else 0.0

def calc_tara(boy_nak: int, girl_nak: int) -> float:
    """
    Dina/Tara (3 Points Max) - Health and family happiness.
    Evaluates the 9-star cycle from both directions.
    """
    # 1. Girl from Boy
    dist_1 = (girl_nak - boy_nak + 27) % 27 + 1
    tara_1 = dist_1 % 9
    score_1 = 0.0 if tara_1 in [3, 5, 7] else 1.5
    
    # 2. Boy from Girl
    dist_2 = (boy_nak - girl_nak + 27) % 27 + 1
    tara_2 = dist_2 % 9
    score_2 = 0.0 if tara_2 in [3, 5, 7] else 1.5
    
    return score_1 + score_2

def calc_graha_maitri(boy_lord_rel: int, girl_lord_rel: int) -> float:
    """
    Graha Maitri (5 Points Max) - Mental affection.
    0 = Enemy, 1 = Neutral, 2 = Friend
    """
    if boy_lord_rel == 2 and girl_lord_rel == 2: return 5.0
    if (boy_lord_rel == 2 and girl_lord_rel == 1) or (girl_lord_rel == 2 and boy_lord_rel == 1): return 4.0
    if (boy_lord_rel == 1 and girl_lord_rel == 1) or (boy_lord_rel == 2 and girl_lord_rel == 0) or (boy_lord_rel == 0 and girl_lord_rel == 2): return 2.0
    if (boy_lord_rel == 0 and girl_lord_rel == 1) or (girl_lord_rel == 0 and boy_lord_rel == 1): return 1.0
    return 0.0

def calc_bhakoot(boy_sign: int, girl_sign: int) -> float:
    """
    Bhakoot / Rasi (7 Points Max) - General indications.
    Awards full points for specific beneficial angles.
    """
    # Calculate zero-indexed difference (0 = Same Sign, 2 = 3rd House)
    rasi_diff = (boy_sign - girl_sign + 12) % 12
    
    # Matches Maitreya: HOUSE1, HOUSE3, HOUSE4, HOUSE7, HOUSE10, HOUSE11
    if rasi_diff in [0, 2, 3, 6, 9, 10]:
        return 7.0
    return 0.0

def calc_rajju(boy_rajju_type: int, boy_rajju_aroha: int, girl_rajju_type: int, girl_rajju_aroha: int) -> float:
    """
    Rajju (4 Points Max) - Physical safety and duration of marriage.
    Extends the 36-point system to 40 points.
    """
    if boy_rajju_aroha == 0 and girl_rajju_aroha == 0 and boy_rajju_type != girl_rajju_type:
        return 4.0
    elif boy_rajju_type != girl_rajju_type and (boy_rajju_aroha != 2 or girl_rajju_aroha != 2):
        return 3.0
    elif boy_rajju_type != girl_rajju_type and boy_rajju_aroha != girl_rajju_aroha:
        return 2.0
    elif boy_rajju_type != girl_rajju_type and boy_rajju_aroha == 2 and girl_rajju_aroha == 2:
        return 1.0
    elif boy_rajju_type == girl_rajju_type:
        return 0.0
        
    return 0.0