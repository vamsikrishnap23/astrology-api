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