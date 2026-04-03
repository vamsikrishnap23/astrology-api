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