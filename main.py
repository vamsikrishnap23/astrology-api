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