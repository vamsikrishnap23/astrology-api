from fastapi import FastAPI, Depends
from models import BirthDetails
from core_math import calculate_base_positions
from features.panchang import calculate_panchang
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Vedic Astrology API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/panchang")
def get_panchang(birth: BirthDetails):
    # 1. Get base planets
    base_positions = calculate_base_positions(birth)
    
    # 2. Pass base planets AND location data to the new Panchang calculator
    panchang_data = calculate_panchang(base_positions, birth.lat, birth.lon, birth.lang)
    
    return {"status": "success", "data": panchang_data}

from features.divisional import calculate_all_vargas

# ... existing imports ...
from features.divisional import calculate_all_vargas

@app.post("/api/v1/chart/vargas")
def get_varga_charts(birth: BirthDetails):
    """
    Returns the D-1 Rasi chart alongside D-2, D-3, D-4, D-7, D-9, D-10, D-12, and D-60 charts.
    """
    # Core engine handles language internally now
    base_positions = calculate_base_positions(birth) 
    
    # Pass language specifically to the Varga generator
    all_varga_data = calculate_all_vargas(base_positions, birth.lang) 
    
    return {
        "status": "success",
        "data": all_varga_data
    }


from features.dashas import calculate_dashas

@app.post("/api/v1/chart/dashas")
def get_vimshottari_dashas(birth: BirthDetails):
    """
    Returns the complete 120-year Vimshottari Mahadasha timeline.
    """
    # 1. Get exact base longitudes
    base_positions = calculate_base_positions(birth)
    
    # 2. Run the Dasha engine (Now passing language parameter)
    dasha_timeline = calculate_dashas(base_positions, birth.lang) # <-- PASSED LANG
    
    return {
        "status": "success",
        "data": dasha_timeline
    }


# main.py
from features.advanced_tables import build_advanced_tables

@app.post("/api/v1/chart/advanced-tables")
def get_advanced_tables(birth: BirthDetails):
    """
    Returns the Planetary and House tables including Sign, Star, Sub, and Sub-Sub Lords.
    """
    base_positions = calculate_base_positions(birth)
    
    # <-- PASSED 'lang' FROM BIRTH PAYLOAD -->
    advanced_tables = build_advanced_tables(base_positions, birth.lang)
    
    return {
        "status": "success",
        "data": advanced_tables
    }


from features.ashtakavarga import get_all_bavs, calculate_sav, get_all_trikona, get_all_ekadhipatya

@app.post("/api/v1/chart/ashtakavarga")
def get_ashtakavarga_charts(birth: BirthDetails):
    """Returns the complete Ashtakavarga matrix: Raw BAV/SAV and both Reductions."""
    base_positions = calculate_base_positions(birth)
    
    # <-- PASSED 'lang' (Translations cascade through the rest automatically!) -->
    bav_data = get_all_bavs(base_positions, birth.lang)
    
    sav_data = calculate_sav(bav_data)
    total_bindus = sum(sav_data)
    
    trikona_data = get_all_trikona(bav_data)
    trikona_sav = calculate_sav(trikona_data) 
    
    ekadhi_data = get_all_ekadhipatya(trikona_data, base_positions)
    ekadhi_sav = calculate_sav(ekadhi_data)
    
    return {
        "status": "success",
        "data": {
            "BAV": bav_data,
            "SAV": sav_data,
            "Trikona": trikona_data,
            "Trikona_SAV": trikona_sav,
            "Ekadhipatya": ekadhi_data,
            "Ekadhipatya_SAV": ekadhi_sav,
            "Total_Bindus": total_bindus
        }
    }

from models import TransitRequest
from features.transits import calculate_transit_relations

@app.post("/api/v1/chart/transit")
def get_transit_chart(request: TransitRequest):
    """Returns the Natal Chart, Transit Chart, and their relative house relationships."""
    # Base charts will auto-translate because we updated core_math.py!
    natal_positions = calculate_base_positions(request.birth)
    transit_positions = calculate_base_positions(request.transit)
    
    # <-- PASS LANGUAGE DOWN TO RELATIONS ENGINE -->
    transit_relations = calculate_transit_relations(natal_positions, transit_positions, request.lang)
    
    return {
        "status": "success",
        "data": {
            "Natal_Chart": natal_positions,
            "Transit_Chart": transit_positions,
            "Transit_Relations": transit_relations
        }
    }

from features.progressions import calculate_progressed_chart
from features.transits import calculate_transit_relations

@app.post("/api/v1/chart/progression")
def get_secondary_progressions(request: TransitRequest):
    """Returns the Progressed Chart and its relation to the Natal Chart."""
    natal_positions = calculate_base_positions(request.birth)
    progressed_positions = calculate_progressed_chart(request.birth, request.transit)
    
    # <-- PASS LANGUAGE DOWN TO RELATIONS ENGINE -->
    progression_relations = calculate_transit_relations(natal_positions, progressed_positions, request.lang)
    
    return {
        "status": "success",
        "data": {
            "Natal_Chart": natal_positions,
            "Progressed_Chart": progressed_positions,
            "Progression_Relations": progression_relations
        }
    }

from models import MatchRequest
from features.ashtakootam import calculate_ashtakootam

@app.post("/api/v1/match/ashtakootam")
def get_compatibility_score(request: MatchRequest):
    """
    Returns the complete 36-point Kundali Milan scorecard.
    """
    # 1. Ensure the individual birth payloads inherit the global request language
    request.boy.lang = request.lang
    request.girl.lang = request.lang
    
    # 2. Calculate physical charts for both individuals
    boy_positions = calculate_base_positions(request.boy)
    girl_positions = calculate_base_positions(request.girl)
    
    # 3. Run the Ashtakootam master controller (passing language down)
    match_report = calculate_ashtakootam(boy_positions, girl_positions, request.lang)
    
    return {
        "status": "success",
        "data": match_report
    }

from features.shadbala import calculate_shadbala


@app.post("/api/v1/chart/shadbala")
def get_shadbala(birth: BirthDetails):
    """Returns the complete Six-Fold Planetary Strength (Shadbala)."""
    base_positions = calculate_base_positions(birth)
    varga_positions = calculate_all_vargas(base_positions) # Core automatically handles lang
    
    tz_map = {"IST": 5.5, "UTC": 0.0, "EST": -5.0, "CST": -6.0, "PST": -8.0}
    offset = tz_map.get(birth.tz, 0.0) 
    
    birth_time = {
        "hour": birth.hour, "minute": birth.minute,
        "lon": birth.lon, "tz_offset": offset,
        "jd": base_positions["Julian_Day"] 
    }
    
    # <-- PASSED 'lang' -->
    shadbala_report = calculate_shadbala(base_positions, varga_positions, birth_time, birth.lang)
    
    return {"status": "success", "data": shadbala_report}


@app.get("/health")
def health():
    return {"ok": True}