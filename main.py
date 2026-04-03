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
    panchang_data = calculate_panchang(base_positions, birth.lat, birth.lon)
    
    return {"status": "success", "data": panchang_data}

from features.divisional import calculate_all_vargas

@app.post("/api/v1/chart/vargas")
def get_varga_charts(birth: BirthDetails):
    """
    Returns the D-1 Rasi chart alongside D-2, D-3, D-4, D-7, D-9, D-10, D-12, and D-60 charts.
    """
    # 1. Get exact base longitudes
    base_positions = calculate_base_positions(birth)
    
    # 2. Run the Master Varga Engine
    all_varga_data = calculate_all_vargas(base_positions)
    
    # 3. Return the comprehensive payload
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
    # 1. Get exact base longitudes (we only need the Moon, but we reuse the core engine)
    base_positions = calculate_base_positions(birth)
    
    # 2. Run the Dasha engine
    dasha_timeline = calculate_dashas(base_positions)
    
    return {
        "status": "success",
        "data": dasha_timeline
    }


from features.advanced_tables import build_advanced_tables

@app.post("/api/v1/chart/advanced-tables")
def get_advanced_tables(birth: BirthDetails):
    """
    Returns the Planetary and House tables including Sign, Star, Sub, and Sub-Sub Lords.
    """
    base_positions = calculate_base_positions(birth)
    advanced_tables = build_advanced_tables(base_positions)
    
    return {
        "status": "success",
        "data": advanced_tables
    }
from features.ashtakavarga import get_all_bavs, calculate_sav, get_all_trikona, get_all_ekadhipatya

@app.post("/api/v1/chart/ashtakavarga")
def get_ashtakavarga_charts(birth: BirthDetails):
    """
    Returns the complete Ashtakavarga matrix: Raw BAV/SAV and both Reductions.
    """
    base_positions = calculate_base_positions(birth)
    
    # 1. Raw Calculations (Rekha)
    bav_data = get_all_bavs(base_positions)
    sav_data = calculate_sav(bav_data)
    total_bindus = sum(sav_data)
    
    # 2. First Reduction (Trikona Shodhana)
    trikona_data = get_all_trikona(bav_data)
    trikona_sav = calculate_sav(trikona_data) 
    
    # 3. Second Reduction (Ekadhipatya Shodhana)
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
    """
    Returns the Natal Chart, Transit Chart, and their relative house relationships.
    """
    # 1. Calculate both physical charts using the core engine
    natal_positions = calculate_base_positions(request.birth)
    transit_positions = calculate_base_positions(request.transit)
    
    # 2. Map the transits against the natal reference points
    transit_relations = calculate_transit_relations(natal_positions, transit_positions)
    
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
    """
    Returns the Progressed Chart and its relation to the Natal Chart.
    """
    # 1. Get the base natal chart
    natal_positions = calculate_base_positions(request.birth)
    
    # 2. Get the mathematically progressed chart
    progressed_positions = calculate_progressed_chart(request.birth, request.transit)
    
    # 3. Optional but highly recommended: Map the Progressed planets against the Natal houses!
    progression_relations = calculate_transit_relations(natal_positions, progressed_positions)
    
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
    # 1. Calculate physical charts for both individuals
    boy_positions = calculate_base_positions(request.boy)
    girl_positions = calculate_base_positions(request.girl)
    
    # 2. Run the Ashtakootam master controller
    match_report = calculate_ashtakootam(boy_positions, girl_positions)
    
    return {
        "status": "success",
        "data": match_report
    }

from features.shadbala import calculate_shadbala
@app.post("/api/v1/chart/shadbala")
def get_shadbala(birth: BirthDetails):
    """
    Returns the complete Six-Fold Planetary Strength (Shadbala).
    """
    base_positions = calculate_base_positions(birth)
    varga_positions = calculate_all_vargas(base_positions)
    
    # Convert string TZ to numeric offset for exact solar math
    tz_map = {"IST": 5.5, "UTC": 0.0, "EST": -5.0, "CST": -6.0, "PST": -8.0}
    offset = tz_map.get(birth.tz, 0.0) 
    
    # --- THE FIX: Ensure 'jd' is explicitly included here ---
    birth_time = {
        "hour": birth.hour, 
        "minute": birth.minute,
        "lon": birth.lon,
        "tz_offset": offset,
        "jd": base_positions["Julian_Day"] # This is required for Ahargana!
    }
    
    shadbala_report = calculate_shadbala(base_positions, varga_positions, birth_time)
    
    return {
        "status": "success",
        "data": shadbala_report
    }