from fastapi import FastAPI, Depends
from models import BirthDetails
from core_math import calculate_base_positions
from features.panchang import calculate_panchang

app = FastAPI(title="Vedic Astrology API")

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